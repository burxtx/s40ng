from contextlib import closing
import random
import hashlib
import re
import copy
import cone.confml.model
import cone.public.api
import cone.public.exceptions
import cone.storage.zipstorage

CPF_ID_METADATA_NAMESPACE = "http://www.nokia.com/xml/cpf-id/1"
CPF_META_TAG = "configuration-property"

# Help functions from VBR tools
def open_cpf(cpf_file, create_default_view=True, mode='r'):
    """
    Open the given CPF and optionally create the default view using the
    active root.
    """
    project = None
    config = None
    try:
        project = cone.public.api.Project(cone.storage.zipstorage.ZipStorage(cpf_file, mode))
        active_root = get_active_root(project)
        if active_root is None:
            raise RuntimeError("No configurations in the CPF")
        config = project.get_configuration(active_root)
        if create_default_view:
            config.get_default_view()
    except ImportError:
        raise
    except Exception:
        if project: project.close()
        raise
    return project, config

def get_active_root(project):
    """
    Return the active root configuration for the given api.Project instance.
    @return: The name of the active root if there is one, or None if the
        CPF contains no configurations.
    """
    active_root = project.get_storage().get_active_configuration()
    configs = sorted(project.list_configurations())
    if not configs:
        log.info("CPF contains no configurations")
        return None

    if not active_root:
        active_root = configs[0]
        log.debug("No active root, using %s" % active_root)
    elif active_root and active_root not in configs:
        log.debug("Active root %s does not exist, using %s" % (active_root, configs[0]))
        active_root = configs[0]

    return active_root
    
def transform_cone_meta(meta):
    """
    Transform a ConE metadata structure into a dictionary.
    """
    CONFML_NAMESPACES = ["http://www.s60.com/xml/confml/2", "http://www.s60.com/xml/confml/1"]

    metadata_dict = {}
    if meta:
        for prop in meta.array:
            if prop.ns == CPF_ID_METADATA_NAMESPACE and 'name' in prop.attrs and 'value' in prop.attrs:
                name = prop.attrs['name']
                value = prop.attrs['value']
                metadata_dict[(prop.ns, name)] = value
            elif not prop.ns or prop.ns in CONFML_NAMESPACES:
                metadata_dict[(None, prop.tag)] = prop.value

    return metadata_dict
    
class _IterationContext(object):
    def __init__(self):
        self.recurse = True

def _iterate_cone_objects(root):
    """
    Iterate through all child objects under the given ConE object.
    @param root: The object whose children to iterate through.
    @return: Yield tuple (obj, iteration_context) for each child object.
        If iteration_context.recurse is set to False, then the current
        object's children won't be traversed.
    """
    itercontext = _IterationContext()
    for obj in root._objects():
        itercontext.recurse = True
        yield obj, itercontext
        if itercontext.recurse:
            for r in _iterate_cone_objects(obj):
                yield r
    
class ImportCache(object):

    # Use a singleton object to allow caching Nones
    NOTFOUND = object()

    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.inserts = 0
        self.cache = {}

    def create_cached(self, key, create, create_args):
        value = self.cache.get(key, self.NOTFOUND)
        if value is self.NOTFOUND:
            self.misses += 1
            value = create(*create_args)
            self.cache[key] = value
        else:
            self.hits += 1
        return value

    def get_or_create_cached(self, key, get_or_create, get_or_create_args):
        value = self.cache.get(key, self.NOTFOUND)
        if value is self.NOTFOUND:
            self.misses += 1
            value, created = get_or_create(*get_or_create_args)
            self.cache[key] = value
            if created:
                self.inserts += 1
        else:
            self.hits += 1
        return value

class SlottedBase(object):
    def __init__(self, **kwargs):
        for name in self.__slots__:
            setattr(self, name, kwargs.get(name))

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        else:
            for name in self.__slots__:
                if getattr(self, name) != getattr(other, name):
                    return False
            return True

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        attrdata = []
        for name in self.__slots__:
            attrdata.append('%s=%r' % (name, getattr(self, name)))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrdata))

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return unicode(repr(self))

class Value(SlottedBase):
    """
    Class representing a raw value read from ConfML, with possible name-ID
    mapping resolved.
    """
    __slots__ = ('value', 'localpath', 'targetpath', 'remotepath',
                 'display_name', 'map_source_sequence', 'map_key', 'mapping_error')

    def get_simplified_value(self):
        """
        Return a simplified version of this value if possible, i.e. only the
        value attribute if only that is set, otherwise the value object itself.
        """
        if self.localpath is None and self.targetpath is None and \
                self.remotepath is None and self.display_name is None and \
                self.map_source_sequence is None and self.map_key is None and \
                self.mapping_error is None:
            return self.value
        else:
            return self

    def __repr__(self):
        attrdata = []
        for name in self.__slots__:
            v = getattr(self, name)
            if v is not None:
                attrdata.append('%s=%r' % (name, v))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrdata))

    def __copy__(self):
        new_value = Value()
        for name in self.__slots__:
            setattr(new_value, name, getattr(self, name))
        return new_value

    def __deepcopy__(self, memo):
        return self.__copy__()

    def as_tuple(self):
        """
        Return this value as a tuple, suitable e.g. for use as a dictionary key.
        """
        return tuple([getattr(self, n) for n in self.__slots__])

    def copy_with_overrides(self, **kwargs):
        """
        Create a copy of this Value instance, but with some attributes overridden.
        """
        new_value = self.__copy__()
        for name in self.__slots__:
            if name in kwargs:
                setattr(new_value, name, kwargs[name])
        return new_value

class CPFReader(object):
    """
    Class used for reading configurations from a CPF file into a dictionary format
    suitable for inserting into the DB. 
    """

    def __init__(self, cpf_path):
        self._project = open_cpf(cpf_path, create_default_view=False, mode='r')[0]
        self._feature_cache = ImportCache()
        self._setting_cache = ImportCache()
        #: Dictionary mapping Value instances that contain a name-ID mapped value
        #: to their corresponding settings, used when resolving name-ID mappings
        self._mapped_value_to_setting = {}

        self.active_root = get_active_root(self._project)

    def get_active_root(self):
        return self.active_root

    def close(self):
        if self._project is not None:
            self._project.close()
            self._feature_cache = ImportCache()
            self._setting_cache = ImportCache()
            self._mapped_value_to_setting = {}

    def read_configuration_dict(self, root=None, values_only=False):
        layers = []
        if not root:
            root = self.active_root

        config = self._project.get_configuration(root)

        metadata = transform_cone_meta(config.meta)
        config_name = config.name

        # Find all layer objects included in the configuration root
        layer_objs = []
        for obj in config._objects():
            if isinstance(obj, cone.public.api.ConfigurationProxy):
                layer_objs.append(obj)

        # Create a temporary configuration for resolving layered content
        while True:
            temp_config_name = 'temp_config_%s.confml' % random.random()
            if temp_config_name not in self._project.list_configurations():
                break
        tempconf = self._project.create_configuration(temp_config_name)

        # All settings found so far, by FQR (fully qualified reference, e.g. 'FooFeature.FooSetting')
        setting_objects = {}
        # All data objects used in value determination found so far, by FQR
        all_data_objects = {}
        # All values found so far, by FQR
        all_values = {}

        for layer_obj in layer_objs:
            # Collect setting and data objects from the layer
            layer_data_objects = {}
            for obj, itercontext in _iterate_cone_objects(layer_obj):
                if isinstance(obj, cone.confml.model.ConfmlSetting):
                    # Found a top-level setting (directly under a feature),
                    # store and don't go any deeper
                    itercontext.recurse = False
                    setting_objects[obj.fqr] = obj
                elif isinstance(obj, cone.confml.model.ConfmlData):
                    if obj.attr != 'data' or obj.template:
                        # Not a data object, or is a template data object
                        # -> ignore and don't go any deeper
                        itercontext.recurse = False
                        continue
                    # Found a data object, store it if it's a top-level data
                    # object (two-part FQR -> has one '.', e.g. 'Fea.Setting'),
                    # and don't go any deeper
                    fqr = obj.fqr
                    if fqr.count('.') == 1:
                        layer_data_objects.setdefault(fqr, []).append(obj)
                        itercontext.recurse = False

            # Resolve the values for the layer
            layer_values = {}
            for fqr, setting_obj in setting_objects.iteritems():
                modified_on_layer = fqr in layer_data_objects
                if modified_on_layer or fqr not in all_values:
                    # Value modified on current layer, or not resolved yet at all,
                    # -> resolve the value
                    value, all_data_objects[fqr] = self._resolve_setting_value(
                        setting_obj, all_data_objects.get(fqr), layer_data_objects.get(fqr))
                    value = {'_value': value,
                             'setting': self._get_setting_dict(setting_obj)}
                    # Update current all values dictionary
                    all_values[fqr] = value

                if modified_on_layer:
                    layer_values[fqr] = all_values[fqr]

            # Handle name-ID mapped values
            for ref, d in all_values.items():
                value = d['_value']
                if d['setting']['_type'] == 'sequence':
                    resolved_value = []
                    for item in value:
                        resolved_item = {}
                        for subref, subvalue in item.iteritems():
                            resolved_item[subref] = self._resolve_name_id_mapped_value(subvalue, all_values, setting_objects)
                        resolved_value.append(resolved_item)
                else:
                    resolved_value = self._resolve_name_id_mapped_value(value, all_values, setting_objects)
                if resolved_value is not value and resolved_value != value:
                    # Value has been changed, override the value entry for the setting
                    d = d.copy()
                    d['_value'] = resolved_value
                    all_values[ref] = d
                    if ref in layer_values:
                        layer_values[ref] = d

            # Get the layer content by adding the current layer into the
            # temporary root and getting the layered content from there
            tempconf.include_configuration(layer_obj.path)
            all_content = self._transform_cone_layered_content(
                self._project, tempconf.layered_content(empty_folders=True))
            layer_content = self._transform_cone_layered_content(
                self._project, tempconf.layered_content(layers=[-1], empty_folders=True))

            # Make a copy to make sure that name-ID mapping handling
            # doesn't cause unwanted side-effects.
            all_values, layer_all_values = all_values.copy(), all_values

            # If we're asked to return only values and no setting information, 
            # change the value entries to contain only the value
            if values_only:
                for ref in layer_all_values.keys():
                    layer_all_values[ref] = layer_all_values[ref]['_value']
                for ref in layer_values.keys():
                    layer_values[ref] = layer_values[ref]['_value']

            layers.append({'_name': layer_obj.name,
                           '_path': layer_obj.path,
                           'all_setting_values': layer_all_values,
                           'layer_setting_values': layer_values,
                           'all_content': all_content,
                           'layer_content': layer_content})

        result = {'layers': layers,
                  'metadata': metadata}
        if config_name:
            result['_name'] = config_name
        return result

    def log_cache_stats(self):
        print ('Setting cache hits:   %s' % self._setting_cache.hits)
        print ('Setting cache misses: %s' % self._setting_cache.misses)
        print ('Feature cache hits:   %s' % self._feature_cache.hits)
        print ('Feature cache misses: %s' % self._feature_cache.misses)

    def _get_feature_dict(self, feature):
        return self._feature_cache.create_cached(
            key=id(feature),
            create=self._create_feature_dict,
            create_args=(feature,))

    def _create_feature_dict(self, feature):
        entry = {'_name': feature.name}
        if feature.desc:
            entry['_desc'] = feature.desc
        return entry

    def _get_setting_dict(self, setting):
        return self._setting_cache.create_cached(
            key=id(setting),
            create=self._create_setting_dict,
            create_args=(setting,))

    def _create_setting_dict(self, setting):
        feature_dict = self._get_feature_dict(setting._find_parent(type=cone.confml.model.ConfmlFeature))
        entry = {'_type': setting.type,
                 'feature': feature_dict}
        if setting.name:
            entry['_name'] = setting.name
        if setting.desc:
            entry['_desc'] = setting.desc
        if setting.type == 'sequence':
            entry['subsettings'] = []
            for ref in setting.list_features():
                entry['subsettings'].append((ref, self._get_setting_dict(setting._get(ref))))
            template_data_obj = self._get_sequence_setting_template_data_object(setting)
            if template_data_obj is not None:
                entry['template'] = self._resolve_sequence_item_value(setting, template_data_obj)
        return entry

    def _resolve_name_id_mapped_value(self, value, setting_values, setting_objects):
        """
        Resolve name-ID mapped value for the given value if necessary.
        @param value: The value, or tuple of values.
        @param setting_values: Dictionary containing all known setting values.
        @param setting_objects: Dictionary containing all known setting objects.
        @return: The modified value, or the original value if no name-ID mapping
            resolution was necessary.
        """
        if isinstance(value, tuple):
            # The value is not a Value instance, but a tuple
            # -> it's a multi-selection value
            # -> call _resolve_name_id_mapped_value for each sub-value
            result = []
            for v in value:
                result.append(self._resolve_name_id_mapped_value(v, setting_values, setting_objects))
            return tuple(result)
        if not isinstance(value, Value):
            return value

        if not value.map_source_sequence or not value.map_key:
            # Not a mapped value or invalid mapping, no need to resolve
            return value

        # Get the setting object this value is for
        setting_obj = self._mapped_value_to_setting[value]

        # Clear the value in case it has already been resolved successfully
        # on the previous layer, but on this layer the mapped value is different
        value = copy.copy(value)
        value.value = None
        value.display_name = None
        value.mapping_error = None

        # Add the newly created value to the map also
        self._mapped_value_to_setting[value] = setting_obj

        # Get the source sequence setting
        seq_setting = setting_objects.get(value.map_source_sequence)
        if not seq_setting:
            value.mapping_error = "Mapping source sequence '%s' does not exist" % value.map_source_sequence
            return value
        if seq_setting.type != 'sequence':
            value.mapping_error = "Mapping source setting '%s' is not a sequence setting" % value.map_source_sequence
            return value

        # Get the source sequence value
        seq_value = setting_values.get(value.map_source_sequence)
        if not seq_value:
            value.mapping_error = "Value for mapping source sequence '%s' does not exist" % value.map_source_sequence
            return value
        seq_subsettings = dict(seq_value['setting']['subsettings'])
        seq_value = seq_value['_value']

        # Get sub-setting references
        map_key_ref = seq_setting.mapKey
        map_value_ref = seq_setting.mapValue
        display_name_ref = seq_setting.displayName or ''
        if not map_key_ref:
            value.mapping_error = 'No mapKey defined in source sequence %s' % value.map_source_sequence
            return value
        if not map_value_ref:
            value.mapping_error = 'No mapValue defined in source sequence %s' % value.map_source_sequence
            return value

        # Get possible sub-setting reference overrides from the setting option
        map_value_ref_overridden = False
        display_name_ref_overridden = False
        for opt in setting_obj._objects(type=cone.public.api.Option):
            if (opt.map or '').replace('/', '.') == value.map_source_sequence:
                if opt.map_value:
                    map_value_ref_overridden = True
                    map_value_ref = opt.map_value
                if opt.display_name:
                    display_name_ref_overridden = True
                    display_name_ref = opt.display_name
        map_key_ref = map_key_ref.replace('/', '.')
        if map_key_ref.count('.') < 1 and seq_subsettings.get(map_key_ref, {}).get('_type') in ('file', 'folder'):
            map_key_ref += '.localPath'
        map_value_ref = map_value_ref.replace('/', '.')
        if map_value_ref.count('.') < 1 and seq_subsettings.get(map_value_ref, {}).get('_type') in ('file', 'folder'):
            map_value_ref += '.localPath'
        display_name_ref = display_name_ref.replace('/', '.')
        if display_name_ref.count('.') < 1 and seq_subsettings.get(display_name_ref, {}).get('_type') in ('file', 'folder'):
            display_name_ref += '.localPath'

        # Check that the key, value and display name sub-settings exist
        if map_key_ref.split('.')[0] not in seq_subsettings:
            value.mapping_error = "Invalid mapKey in source sequence %s: no sub-setting with ref '%s'" % (value.map_source_sequence, map_key_ref)
            return value
        if map_value_ref.split('.')[0] not in seq_subsettings:
            if map_value_ref_overridden:
                value.mapping_error = "Invalid mapValue override in option: sub-setting '%s' does not exist under source sequence '%s'" % (map_value_ref, value.map_source_sequence)
            else:
                value.mapping_error = "Invalid mapValue in source sequence %s: no sub-setting with ref '%s'" % (value.map_source_sequence, map_value_ref)
        if display_name_ref and display_name_ref.split('.')[0] not in seq_subsettings:
            if display_name_ref_overridden:
                value.mapping_error = "Invalid displayName override in option: sub-setting '%s' does not exist under source sequence '%s'" % (display_name_ref, value.map_source_sequence)
            else:
                value.mapping_error = "Invalid displayName in source sequence %s: no sub-setting with ref '%s'" % (value.map_source_sequence, display_name_ref)

        # Find the sequence item that is mapped
        seq_item = None
        for item in seq_value:
            if self._get_string_value_from_sequence_item(item, map_key_ref) == value.map_key:
                seq_item = item
                break
        if seq_item is None:
            value.mapping_error = "No item-setting in source sequence '%s' matches key '%s'" % (value.map_source_sequence, value.map_key)
            return value

        value.value = self._get_string_value_from_sequence_item(item, map_value_ref)
        if display_name_ref:
            value.display_name = self._get_string_value_from_sequence_item(item, display_name_ref)
        return value

    def _get_string_value_from_sequence_item(self, item, ref):
        """
        Return the string value of the given sub-setting from the given sequence item.
        @param item: The sequence item, e.g. {'SubSetting1': 'foo', 'SubSetting2': 'bar',
                                              'FileSubSetting': Value(localpath='foo.txt')}
        @param ref: The sub-setting reference to get the string value by. For simple sub-settings
            it must be only the sub-setting reference part, e.g. 'SubSetting1', and for file
            and folder sub-settings it must contain the sub-ref, e.g. 'FileSubSetting.localPath'.
        """
        refparts = ref.split('.')
        if len(refparts) < 1 or len(refparts) > 2:
            raise Exception('Invalid ref: %r' % ref)

        value = item.get(refparts[0])
        if isinstance(value, Value) and len(refparts) > 1:
            if refparts[1] == 'localPath':
                value = value.localpath
            elif refparts[1] == 'targetPath':
                value = value.targetpath
            elif refparts[1] == 'remotePath':
                value = value.remotepath

        if isinstance(value, basestring):
            return value

    def _resolve_setting_value(self, setting_obj, all_data_objs, layer_data_objs):
        """
        Resolve the value for the given setting object based on the given data objects.
        @param setting_obj: The setting object whose value to resolve.
        @param all_data_objs: All data objects currently found for the setting.
        @param layer_data_objs: Data objects found for the setting on the current layer.
        @return: Tuple (value, used_data_objs), where value is the resolved value, and
            used_data_objs is a list of the data objects included in the the value's resolution.
        """
        if setting_obj.type == 'sequence':
            return self._resolve_sequence_setting_value(setting_obj, all_data_objs, layer_data_objs)
        elif setting_obj.type == 'multiSelection':
            return self._resolve_multiselection_setting_value(setting_obj, all_data_objs, layer_data_objs)
        elif setting_obj.type in ('file', 'folder'):
            return self._resolve_file_or_folder_setting_value(setting_obj, all_data_objs, layer_data_objs)
        else:
            return self._resolve_simple_setting_value(setting_obj, all_data_objs, layer_data_objs)

    def _resolve_sequence_setting_value(self, setting_obj, all_data_objs, layer_data_objs):
        value = []
        used_data_objs = self._resolve_sequence_data_objects(all_data_objs, layer_data_objs)
        for data_obj in used_data_objs:
            value.append(self._resolve_sequence_item_value(setting_obj, data_obj))
        return value, used_data_objs

    def _resolve_sequence_data_objects(self, all_data_objs, layer_data_objs):
        """
        Resolve the list of data objects in the correct order based on which to resolve a sequence value.
        """
        all_data_objs = all_data_objs or []
        layer_data_objs = layer_data_objs or []
        result = []
        if layer_data_objs:
            # Data on the current layer, include based on the extension policy
            extension_policy = self._get_sequence_extension_policy(layer_data_objs)
            if extension_policy == 'prefix':
                result = layer_data_objs + all_data_objs
            elif extension_policy == 'append':
                result = all_data_objs + layer_data_objs
            else:
                result = layer_data_objs
        else:
            # No data on the current layer
            result = all_data_objs

        if len(result) == 1 and len(result[0]._objects()) == 0:
            # Empty sequence marker (single data element with no sub-elements)
            return []

        return result

    def _get_sequence_extension_policy(self, data_objs):
        for data_obj in data_objs or []:
            if data_obj.policy:
                return data_obj.policy
        return None

    def _resolve_multiselection_setting_value(self, setting_obj, all_data_objs, layer_data_objs):
        if layer_data_objs:
            used_data_objs = layer_data_objs
        elif all_data_objs:
            used_data_objs = all_data_objs
        else:
            used_data_objs = []

        value = self._convert_multiselection_data_to_value(setting_obj, used_data_objs)

        return value, used_data_objs

    def _convert_multiselection_data_to_value(self, setting, data_objects):
        if len(data_objects) == 1:
            d = data_objects[0]

            # Special handling for cases where the data is in the old format
            # (pre-2.88 ConfML spec)
            if d.value is not None:
                if setting.OLD_STYLE_DATA_PATTERN.match(d.value):
                    return tuple([v.rstrip('"').lstrip('"') for v in \
                                   d.value.split('" "')])

            # Single data object with empty="true" means that nothing is
            # selected
            if d.empty:
                return ()

        # Read each data value (or name-ID mapped value) into result
        result = []
        for data_obj in data_objects:
            if data_obj.map:
                value = self._name_id_mapping_string_to_value(data_obj.map, setting)
            else:
                value = data_obj.value
            if value:
                result.append(value)

        # Handle None in the result (data element with no text data)
        if None in result:
            # If the empty string is a valid option, change the None to that,
            # otherwise ignore
            index = result.index(None)
            if '' in setting.get_valueset():
                result[index] = ''
            else:
                del result[index]

        return tuple(result)

    def _resolve_file_or_folder_setting_value(self, setting_obj, all_data_objs, layer_data_objs):
        used_data_objs = (all_data_objs or []) + (layer_data_objs or [])
        localpath = None
        targetpath = None
        remotepath = None
        for data_obj in used_data_objs:
            localpath = self._get_sub_data_value(data_obj, 'localPath') or localpath
            targetpath = self._get_sub_data_value(data_obj, 'targetPath') or targetpath
            remotepath = self._get_sub_data_value(data_obj, 'remotePath') or remotepath
        value = Value(localpath=self._normalize_localpath(localpath),
                      targetpath=targetpath,
                      remotepath=remotepath)
        return value.get_simplified_value(), used_data_objs

    def _get_sub_data_value(self, data_obj, subref):
        try:
            d = data_obj._get(subref)
            return d.value
        except cone.public.exceptions.NotFound:
            return None

    def _resolve_simple_setting_value(self, setting_obj, all_data_objs, layer_data_objs):
        # Use the last data object
        if layer_data_objs:
            data_obj = layer_data_objs[-1]
        elif all_data_objs:
            data_obj = all_data_objs[-1]
        else:
            data_obj = None

        value = None
        if data_obj is not None:
            if data_obj.map:
                value = self._name_id_mapping_string_to_value(data_obj.map, setting_obj)
            elif data_obj.value:
                value = data_obj.value
        return value, [data_obj] if data_obj is not None else []

    def _name_id_mapping_string_to_value(self, mapping_string, setting):
        pattern = r"^([\w/]+)\[@key='(.*)'\]$"
        m = re.match(pattern, mapping_string)
        value = Value()
        if m is None:
            value.mapping_error = 'Malformed mapping expression: %s' % mapping_string
        else:
            value.map_source_sequence = m.group(1).replace('/', '.')
            value.map_key = m.group(2)
            self._mapped_value_to_setting[value] = setting
        return value

    def _resolve_sequence_item_value(self, sequence_setting, data_obj):
        """
        Resolve the value of a single sequence item of the given sequence setting.
        """
        result = {}
        for ref in sequence_setting.list_features():
            subsetting = sequence_setting._get(ref)

            # Collect data objects for the sub-setting
            sub_data_objs = []
            for sub_obj in data_obj._objects():
                if isinstance(sub_obj, cone.public.api.Data) and sub_obj.ref == ref:
                    sub_data_objs.append(sub_obj)

            result[ref], _ = self._resolve_setting_value(subsetting, sub_data_objs, None)
        return result

    def _get_sequence_setting_template_data_object(self, setting):
        """
        Return the template data object for the given sequence setting.
        """
        setting_fqr = setting.fqr

        # Find the configuration the setting is defined under
        configuration = setting.find_parent(type=cone.public.api.Configuration)

        # Find the first template data element for the setting under that configuration
        for obj, _ in _iterate_cone_objects(configuration):
            if isinstance(obj, cone.public.api.Data) and obj.template and \
                    obj.attr == 'data' and obj.fqr == setting_fqr:
                return obj

        return None

    def _transform_cone_layered_content(self, project, layered_content):
        """
        Transform a dictionary returned by a call to layered_content() into
        a dictionary that can be used to insert the content into the DB.
        """
        layered_content = layered_content.flatten()
        storage = project.get_storage()
        result = {}

        for contentpath, fullpath in layered_content.iteritems():
            contentpath = self._normalize_localpath(contentpath)
            if storage.is_folder(fullpath):
                result[contentpath] = None
            else:
                size = 0
                sha1 = hashlib.sha1()
                with closing(storage.open_resource(fullpath, 'rb')) as f:
                    while True:
                        d = f.read(64 * 1024)
                        if d:
                            size += len(d)
                            sha1.update(d)
                        else:
                            break
                result[contentpath] = (size, sha1.hexdigest())

        # Remove redundant folder entries (leave only empty folders)
        all_names = result.keys()
        for key, value in list(result.iteritems()):
            if value is None and any(map(lambda x: x.startswith(key + '/'), all_names)):
                del result[key]

        return result

    def _normalize_localpath(self, localpath):
        """
        Normalize a ConfML localPath so that it doesn't contain backslashes
        and no trailing slashes.
        """
        if localpath:
            return localpath.replace('\\', '/').rstrip('/')
        else:
            return localpath