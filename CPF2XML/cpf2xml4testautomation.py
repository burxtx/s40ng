import sys
import pprint
import datetime
import os.path
from optparse import OptionParser
from cone.public import api
from lxml import etree
from cpf_import import CPFReader, Value
from contextlib import closing

#Element REFs
VERSIO = '0.9'
TESTAUTOMATION_REF = 'testautomation'
METADATA_REF = 'metadata'
METADATA_CHILD_GENERATION_TIME_REF = 'xmlgenerationtime'
METADATA_CHILD_VERSION_REF = 'cpf2xmlversion'
METADATA_CHILD_INPUT_REF = 'inputfile'
METADATA_CHILD_XML_REF = 'cpf2xml-metadata'
METADATA_CHILD_REF = 'cpf-metadata'
METADATA_CPF_CHILD_REF = 'cpf-property'
LAYERS_REF = 'layers'
LAYER_REF = 'layer'
NAME_REF = 'name'
FEATURES_REF = 'features'
FEATURE_REF = 'feature'
SETTING_REF = 'setting'
REFERENCE_REF = 'reference'
TYPE_REF = 'type'
DESCRIPTION_REF = 'description'
VALUE_REF = 'value'
LOCALPATH_REF = 'localpath'
TARGETPATH_REF = 'targetpath'
REMOTEPATH_REF = 'remotepath'
CONTENT_REF = 'content'
FILE_REF = 'file'
PATH_REF = 'path'
SIZE_REF = 'size'
SHA1_REF = 'sha1'
FOCUS_LAYER_REF = 'focus-layer'
DEFAULT_VALUE_FROM_BELOW_REF = 'all-below-layers'
FROM_REF = 'from'
NAME_IN_SELECTION_REF = 'name-in-selection'
MAIN_VIEW_REF = 'main-view'
SUB_VIEW_REF = 'sub-view'
SUB_SETTING_REF = 'subsetting'
SEQUENCE_REF = 'sequence'
DISPLAY_NAME_REF = 'display-name'
MAP_SOURCE_SEQUENCE_REF = 'map-source-sequence'
MAP_KEY_REF = 'map-key'
MAPPING_ERROR_REF = 'mapping-error'
SELECTION_REF = 'selection'

# ---------------------------------------------------------------------
# Class to generate XML file
# ---------------------------------------------------------------------
class Cpf2Xml4TestAutomation:

  def __init__(self, filename):
    # Read data from CPF by using VBR reporting tools
    self.inputfilename = filename
    #self.datastructure = read_configuration_dict(filename)
    with closing(CPFReader(filename)) as reader:
      self.datastructure = reader.read_configuration_dict()
      rootname = reader.get_active_root()
      
    #with open('test_map.txt', 'w') as f: pprint.pprint(self.datastructure, stream=f)
    
    # Create root for XML
    self.root = etree.Element(TESTAUTOMATION_REF)
    # Create metadata with timestamp
    self.metadata = etree.SubElement(self.root, METADATA_REF)
    self.AddCpf2XmlMetadataToOutputXml()
    # Create layers element
    self.layers = etree.SubElement(self.root, LAYERS_REF)
    
    # Create cone APIs
    # Create a new storage to a cpf file and give it to the project.
    project = api.Project(api.Storage.open(self.inputfilename, 'r'))

    # Find resource of root file
    config = project.get_configuration(rootname)
    config_root = config.get_root_configuration()
    self.dview = config_root.get_default_view()
    
    # Create view list for settings
    self.view = config_root.get_view(config_root.list_views()[0])
    self.settingviewdict = {}
    self.PopulateViewDict()
    
    self.featurelistForManifest = []

    project.close()

  def AddCpf2XmlMetadataToOutputXml(self):
    # Called from __init__
    element_xmlmetadata = etree.SubElement(self.metadata, METADATA_CHILD_XML_REF)
    element_generationtime = etree.SubElement(element_xmlmetadata, METADATA_CHILD_GENERATION_TIME_REF)
    element_generationtime.text = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
    element_version = etree.SubElement(element_xmlmetadata, METADATA_CHILD_VERSION_REF)
    element_version.text = VERSIO
    element_input = etree.SubElement(element_xmlmetadata, METADATA_CHILD_INPUT_REF)
    element_input.text = self.inputfilename

  def PrintDataStructureToFile(self, filename):
    if self.datastructure != None:
      with open(filename, 'w') as f: pprint.pprint(self.datastructure, stream=f)    
    else:
      with open(filename, 'w') as f: pprint.pprint('No data', stream=f)

  def GenerateOutputXml(self, filename, printToScreen=False):
    if printToScreen == True:
      print etree.tostring(self.root, pretty_print=True)
    else:
      f = open(filename, 'w')
      f.write(etree.tostring(self.root, pretty_print=True))
      f.close()
  
  def AddCpfMetadataToOutputXml(self):
    element_cpfmetadata = etree.SubElement(self.metadata, METADATA_CHILD_REF)
    for (namespace, name), value in sorted(self.datastructure['metadata'].iteritems()):
      element = etree.SubElement(element_cpfmetadata, METADATA_CPF_CHILD_REF)
      if name:
        element.set('name', name)
      if value:
        element.set('value', value)

  def AddLayersToOutputXml(self, addLayerContent=False, specificLayerFocusSubString=None, addDefaultValuesToFocus=False):
    nextIsDefaultValueLayer = False
    # Go through layers
    for layer_dict in reversed(self.datastructure['layers']):
      # Check if data is needed from this layer
      if specificLayerFocusSubString is not None and nextIsDefaultValueLayer == False:
        if layer_dict.get('_name').find(specificLayerFocusSubString) == -1:
          continue
      
      if specificLayerFocusSubString is not None and nextIsDefaultValueLayer == False:
        element_layer = etree.SubElement(self.layers, FOCUS_LAYER_REF)
        element_layer.set(NAME_REF, layer_dict.get('_name'))
      elif nextIsDefaultValueLayer == True:
        element_layer = etree.SubElement(self.layers, DEFAULT_VALUE_FROM_BELOW_REF)
        element_layer.set(FROM_REF, layer_dict.get('_name'))
      else:
        element_layer = etree.SubElement(self.layers, LAYER_REF)
        element_layer.set(NAME_REF, layer_dict.get('_name'))
      
      # Go through features from current layer
      element_features = etree.SubElement(element_layer, FEATURES_REF)
      if nextIsDefaultValueLayer == True:
        used_setting_values = 'all_setting_values'
      else:
        used_setting_values = 'layer_setting_values'
      featureDict = {}
      for ref, value_dict in sorted(layer_dict[used_setting_values].iteritems()):
        # Check if feature is already added. If yes, merge settings to same feature
        featureRef = (ref.split('.'))[0]
        element_feature = None
        if featureRef in featureDict.keys():
           element_feature = featureDict[featureRef]
        if element_feature == None:
          element_feature = etree.SubElement(element_features, FEATURE_REF)
          element_feature.set(REFERENCE_REF, featureRef)
          element_feature.set(NAME_REF, value_dict['setting']['feature'].get('_name'))
          featureDict[featureRef] = element_feature
          if specificLayerFocusSubString is not None:
              if layer_dict.get('_name').find(specificLayerFocusSubString) != -1:
                  self.featurelistForManifest.append((featureRef, value_dict['setting']['feature'].get('_name')))
          else:
              if layer_dict.get('_name').find('customer') != -1:
                  self.featurelistForManifest.append((featureRef, value_dict['setting']['feature'].get('_name')))

        # Create setting element from feature
        element_setting = etree.SubElement(element_feature, SETTING_REF)
        element_reference = etree.SubElement(element_setting, REFERENCE_REF)
        element_reference.text = ref
        element_name = etree.SubElement(element_setting, NAME_REF)
        if value_dict['setting'].get('_name') is not None:
          element_name.text = value_dict['setting'].get('_name')
        element_type = etree.SubElement(element_setting, TYPE_REF)
        if value_dict['setting'].get('_type') is not None:
          element_type.text = value_dict['setting'].get('_type')
        element_desc = etree.SubElement(element_setting, DESCRIPTION_REF)
        if value_dict['setting'].get('_desc') is not None:
          element_desc.text = value_dict['setting'].get('_desc')
        
        # Add names of views to setting element
        viewnames = self.FindViewNamesBySetting(ref)
        if element_type.text == 'sequence' and len(viewnames) == 0:
          for subRef, subValue_dict in sorted(value_dict['setting']['subsettings']):
            viewnames = self.FindViewNamesBySetting(ref + '.' + subRef)
            if len(viewnames) > 0:
              break
        element_main_view = etree.SubElement(element_setting, MAIN_VIEW_REF)
        element_sub_view = etree.SubElement(element_setting, SUB_VIEW_REF)
        if len(viewnames) > 0:
          element_main_view.text = viewnames[0]
          if len(viewnames) > 1:
            element_sub_view.text = viewnames[1]
        
        # Handle subsettings for sequences
        subsettingsTypesDictionary = {}
        if element_type.text == 'sequence':
          for subRef, subValue_dict in sorted(value_dict['setting']['subsettings']):
            element_subSetting = etree.SubElement(element_setting, SUB_SETTING_REF)
            element_Subreference = etree.SubElement(element_subSetting, REFERENCE_REF)
            element_Subreference.text = ref + '.' + subRef
            element_Subname = etree.SubElement(element_subSetting, NAME_REF)
            if subValue_dict['_name'] is not None:
              element_Subname.text = subValue_dict['_name']
            element_Subtype = etree.SubElement(element_subSetting, TYPE_REF)
            if subValue_dict['_type'] is not None:
              subsettingsTypesDictionary[subRef] = subValue_dict['_type']
              element_Subtype.text = subValue_dict['_type']
            element_Subdesc = etree.SubElement(element_subSetting, DESCRIPTION_REF)
            if subValue_dict['_name'] is not None:
              element_Subdesc.text = subValue_dict['_name']

        # Check value from here
        if element_type.text == 'sequence':
          element_data = etree.SubElement(element_setting, VALUE_REF)
          for sequnceValuelist in value_dict['_value']:
            element_sequence = etree.SubElement(element_data, SEQUENCE_REF)
            for key, value in sequnceValuelist.iteritems():
              subType = None
              for subKey, subValue in subsettingsTypesDictionary.iteritems():
                if subKey == key:
                  subType = subValue
              if isinstance(value, Value) and subType != 'multiSelection':
                self.CreateElementsForValue(value, element_sequence, ref, False, True, key)
              elif value is not None:
                if subType == 'multiSelection':
                  for subValue in value:
                    element_sequenceSelection = etree.SubElement(element_sequence, SELECTION_REF)
                    if isinstance(subValue, Value):
                      self.CreateElementsForValue(subValue, element_sequenceSelection, ref, True, True, key)
                    else:
                      element_sequenceData = etree.SubElement(element_sequenceSelection, VALUE_REF)
                      element_sequenceData.set(REFERENCE_REF, ref + '.' + key)                    
                      element_sequenceData.text = subValue
                      if subValue is not None:
                        text = self.FindOptionNameByValue(ref + '.' + key, value)
                        if text is not None:
                          element_sequenceData.set(NAME_IN_SELECTION_REF, text)
                else:
                  element_sequenceData = etree.SubElement(element_sequence, VALUE_REF)
                  element_sequenceData.set(REFERENCE_REF, ref + '.' + key)
                  element_sequenceData.text = value
                  # If type is selection or multiselection, add text that is visible in tools
                  if subType == 'selection':
                    if value is not None:
                      text = self.FindOptionNameByValue(ref + '.' + key, value)
                      if text is not None:
                        element_sequenceData.set(NAME_IN_SELECTION_REF, text)
                
              else:
                continue
                # Empty values are not written in sequence
                # element_sequenceData = etree.SubElement(element_sequence, VALUE_REF)
                # element_sequenceData.set(REFERENCE_REF, ref + '.' + key)

        elif isinstance(value_dict['_value'], Value) and element_type.text != 'multiSelection':
          self.CreateElementsForValue(value_dict['_value'], element_setting, ref, False, False)
        elif value_dict['_value'] is not None:
          if element_type.text == 'multiSelection':
            for value in value_dict['_value']:
              element_selection = etree.SubElement(element_setting, SELECTION_REF)
              if isinstance(value, Value):
                self.CreateElementsForValue(value, element_selection, ref, True, False)
              else:
                element_data = etree.SubElement(element_selection, VALUE_REF)
                element_data.text = value
                # If type is selection or multiselection, add text that is visible in tools
                if value is not None:
                  text = self.FindOptionNameByValue(ref, value)
                  if text is not None:
                    element_data.set(NAME_IN_SELECTION_REF, text)
          else:
            value = value_dict['_value']
            element_data = etree.SubElement(element_setting, VALUE_REF)
            element_data.text = value
            # If type is selection or multiselection, add text that is visible in tools
            if element_type.text == 'selection':
              if value is not None:
                text = self.FindOptionNameByValue(ref, value)
                if text is not None:
                  element_data.set(NAME_IN_SELECTION_REF, text)
          
        else: #None
          element_data = etree.SubElement(element_setting, VALUE_REF)

      if addLayerContent == True:
        # Go through content items from current layer
        element_content = etree.SubElement(element_layer, CONTENT_REF)
        if nextIsDefaultValueLayer == True:
          used_content_values = 'all_content'
        else:
          used_content_values = 'layer_content'
        for path, entry in sorted(layer_dict[used_content_values].iteritems()):
          element_file = etree.SubElement(element_content, FILE_REF)
          element_path = etree.SubElement(element_file, PATH_REF)
          element_path.text = path
          element_size = etree.SubElement(element_file, SIZE_REF)
          element_sha1 = etree.SubElement(element_file, SHA1_REF)
          if entry is not None:
            element_size.text = str(entry[0])
            element_sha1.text = str(entry[1])
      
      if specificLayerFocusSubString is not None and addDefaultValuesToFocus == True:
        if nextIsDefaultValueLayer == False:
          nextIsDefaultValueLayer = True
        else:
          break

  def CreateElementsForValue(self, value, parent_element, ref, selection_name=False, add_reference=False, key=None):
    settingTuple = value.as_tuple()
    if settingTuple[0] is not None:
      element_value = etree.SubElement(parent_element, VALUE_REF)
      if add_reference:
        element_value.set(REFERENCE_REF, ref + '.' + key)
      element_value.text = settingTuple[0]
      if selection_name:
        text = self.FindOptionNameByValue(ref, settingTuple[0])
        if text is not None:
          element_data.set(NAME_IN_SELECTION_REF, text)
    if settingTuple[1] is not None:
      element_value = etree.SubElement(parent_element, VALUE_REF)
      if add_reference:
        element_value.set(REFERENCE_REF, ref + '.' + key + '.' + LOCALPATH_REF)
      else:
        element_value.set(REFERENCE_REF, LOCALPATH_REF)
      element_value.text = settingTuple[1]
    if settingTuple[2] is not None:
      element_value = etree.SubElement(parent_element, VALUE_REF)
      if add_reference:
        element_value.set(REFERENCE_REF, ref + '.' + key + '.' + TARGETPATH_REF)
      else:
        element_value.set(REFERENCE_REF, TARGETPATH_REF)
      element_value.text = settingTuple[2]
    if settingTuple[3] is not None:
      element_value = etree.SubElement(parent_element, VALUE_REF)
      if add_reference:
        element_value.set(REFERENCE_REF, ref + '.' + key + '.' + REMOTEPATH_REF)
      else:
        element_value.set(REFERENCE_REF, REMOTEPATH_REF)
      element_value.text = settingTuple[3]
    if settingTuple[4] is not None:
      element_value = etree.SubElement(parent_element, DISPLAY_NAME_REF)
      if add_reference:
        element_value.set(REFERENCE_REF, ref + '.' + key)
      element_value.text = settingTuple[4]
    if settingTuple[5] is not None:
      element_value = etree.SubElement(parent_element, MAP_SOURCE_SEQUENCE_REF)
      if add_reference:
        element_value.set(REFERENCE_REF, ref + '.' + key)
      element_value.text = settingTuple[5]
    if settingTuple[6] is not None:
      element_value = etree.SubElement(parent_element, MAP_KEY_REF)
      if add_reference:
        element_value.set(REFERENCE_REF, ref + '.' + key)
      element_value.text = settingTuple[6]
    if settingTuple[7] is not None:
      element_value = etree.SubElement(parent_element, MAPPING_ERROR_REF)
      if add_reference:
        element_value.set(REFERENCE_REF, ref + '.' + key)
      element_value.text = settingTuple[7]

  def FindOptionNameByValue(self, settingRef, value):
    feature = self.dview.get_feature(settingRef)
    optionlist = feature.list_options()
    for option in optionlist:
      optionElem = feature.get_option(option)
      if optionElem.get_value() == value:
        return optionElem.get_name()
    return None
    
  def PopulateViewDict(self):
    # Called from __init__
    if len(self.settingviewdict.keys()) == 0:
      maingroupnamelist = self.view.list_groups()
      for maingroupname in maingroupnamelist:
        maingroupElement = self.view.get_group(maingroupname)
        subgroupnamelist = maingroupElement.list_groups()
        for subgroupname in subgroupnamelist:
          subgroupElement = maingroupElement.get_group(subgroupname)
          settingReflist = subgroupElement.list_features()
          for settingRef in settingReflist:
            setting = subgroupElement.get_feature(settingRef)
            self.settingviewdict[setting._obj.fqr] = [maingroupname, subgroupname]

  def FindViewNamesBySetting(self, inputSettingRef):
    if inputSettingRef in self.settingviewdict.keys():
      return self.settingviewdict[inputSettingRef]
    return []


# ---------------------------------------------------------------------
# Class to generate Manifest XML file
# ---------------------------------------------------------------------
class Manifest4TestAutomation:
    def __init__(self):
        tempfile = open('manifest_template.xml', 'r')
        manifest_template = tempfile.read()
        tempfile.close()
        parser = etree.XMLParser(remove_blank_text=True)
        self.root = etree.XML(manifest_template, parser)

    def AddTestGroupsToManifest(self, featurelistForManifest, ignore_feature_list, package_dict, package_mandatory_dict):
        suiteslist = self.root.findall('{http://nokia.com/NwWP/TestRunner}Suites')
        for suites in suiteslist:
            suitelist = suites.findall('{http://nokia.com/NwWP/TestRunner}Suite')
            if len(suitelist) > 0:
                suitelist[0].set('spkgs', self.GenerateAllPackagesString(package_dict, package_mandatory_dict))
                counter = 1
                added_refs = []
                for ref, name in featurelistForManifest:
                    if ref not in ignore_feature_list:
                        if ref not in added_refs: 
                            test_element = etree.SubElement(suitelist[0], 'Test')
                            test_element.set('id', 'test_' + str(counter))
                            test_element.set('name', name)
                            test_element.set('type', 'ymtf')
                            test_element.set('params', '-tests ' + ref)
                            test_element.set('assembly', 'dll_tuxnet')
                            test_element.set('timeout', '43200')
                            counter = counter + 1
                            added_refs.append(ref)
                break
    
    def GenerateAllPackagesString(self, package_dict, package_mandatory_dict):
        packages = ''
        for value in package_dict.itervalues():
            packages = packages + value + ' '
        for value in package_mandatory_dict.itervalues():
            packages = packages + value + ' '
        if packages != '':
            packages = packages[0:-1]
        return packages
    
    def AddPackagesToManifest(self, featurelistForManifest, ignore_feature_list, package_dict, package_mandatory_dict, feature_package_dict):
        temp_packages_to_add_list = []
        for key in package_mandatory_dict.iterkeys():
            temp_packages_to_add_list.append(key)
        for ref, name in featurelistForManifest:
            if ref not in ignore_feature_list:
                if ref in feature_package_dict:
                    packages = feature_package_dict[ref].split(';')
                    for package in packages:
                        temp_packages_to_add_list.append(package)
        packages_to_add_list = []
        for item in temp_packages_to_add_list:
            if item not in packages_to_add_list:
                packages_to_add_list.append(item)
        packages_to_add_list.sort()
        
        packagelist = self.root.findall('{http://nokia.com/NwWP/TestRunner}Spkgs')
        if len(packagelist) > 0:
            added_refs = []
            for item in packages_to_add_list:
                if item in package_dict:
                    package_element = etree.SubElement(packagelist[0], 'Spkg')
                    package_element.set('id', package_dict[item])
                    package_element.text = item
                elif item in package_mandatory_dict:
                    package_element = etree.SubElement(packagelist[0], 'Spkg')
                    package_element.set('id', package_mandatory_dict[item])
                    package_element.text = item
        
    def GenerateOutputXml(self, filename):
        f = open(filename, 'w')
        f.write(etree.tostring(self.root, pretty_print=True))
        f.close()


# ---------------------------------------------------------------------
# Main code for cpf2xml4testautomation class
# This class creates XML file for test automation purposes based
# on cpf_import functionalities from VBR reporting scripts
# ---------------------------------------------------------------------
def main(argv):
  usage = 'usage: cpf2xml4testautomation.py -inputfile <cpffile>.cpf [-outputfile <output>.xml] [-screen] [-content] [-metadata] [-focuslayer configurator] [-defaultvalues]'
  parser = OptionParser(usage = usage)
  parser.add_option(
                    '-i', '--inputfile', dest='inputfile', action='store',
                    help='Give input CPF filename', default=None)
  parser.add_option(
                    '-o', '--outputfile', dest='outputfile', action='store',
                    help='Give output XML filename', default='output.xml')
  parser.add_option(
                    '-s', '--screen', action='store_true', dest='screen',
                    help='Add parameter if you want to print output to screen', default=False)
  parser.add_option(
                    '-c', '--content', action='store_true', dest='content',
                    help='Add parameter if you want to add content to outputfile', default=False)
  parser.add_option(
                    '-m', '--metadata', action='store_true', dest='metadata',
                    help='Add parameter if you want to add CPF related metadata to outputfile', default=False)
  parser.add_option(
                    '-f', '--focuslayer', dest='focuslayer', action='store',
                    help='Give substring of layer you want to focus', default=None)
  parser.add_option(
                    '-d', '--defaultvalues', action='store_true', dest='defaultvalues',
                    help='Add parameter if you want to add defaultvalue layer when focusing certain layer', default=False)
  parser.add_option(
                    '-a', '--manifest', action='store_true', dest='manifest',
                    help='Add parameter if you want to create manifest file for testing', default=False)
                    
  
  options, _ = parser.parse_args(argv)
  microsoft_package_list = []
  feature_package_dict = {}
  package_dict = {}
  package_mandatory_dict = {}
  ignore_feature_list = []
  manifest_template = ''
  
  if options.manifest == True:
    if os.path.isfile('manifest_template.xml') and os.path.isfile('config.xml'):
      # Read configuration
      tree = etree.parse('config.xml')
      packageslist = tree.findall('msfttestroot-packages')
      if len(packageslist) > 0:
          packages = packageslist[0].findall('package')
          for package in packages:
              microsoft_package_list.append(package.text)
      packageslist = tree.findall('features-and-packages')
      if len(packageslist) > 0:
          packages = packageslist[0].findall('packages')
          for package in packages:
              data = package.text
              key = package.get('feature')
              feature_package_dict[key] = data
      packageslist = tree.findall('testpackages')
      if len(packageslist) > 0:
          packages = packageslist[0].findall('testpackage')
          for package in packages:
              data = package.text
              key = package.get('id')
              mandatory = package.get('mandatory-for-all')
              if mandatory is not None:
                  package_mandatory_dict[key] = data
              else:
                  package_dict[key] = data
      featureslist = tree.findall('ignore-features')
      if len(featureslist) > 0:
          features = featureslist[0].findall('feature')
          for feature in features:
              ignore_feature_list.append(feature.text)
    else:
      print 'Required file(s) missing: manifest_template.xml and/or config.xml'
      return
    
  if options.inputfile != None:
    cpf2xml = Cpf2Xml4TestAutomation(options.inputfile)
    if options.metadata == True:
      cpf2xml.AddCpfMetadataToOutputXml()
    cpf2xml.AddLayersToOutputXml(options.content, options.focuslayer, options.defaultvalues)
    cpf2xml.GenerateOutputXml(options.outputfile, options.screen)
    
    if options.manifest == True:
      featurelistForManifest = cpf2xml.featurelistForManifest
      ManifestGenerator = Manifest4TestAutomation()
      ManifestGenerator.AddTestGroupsToManifest(featurelistForManifest, ignore_feature_list, package_dict, package_mandatory_dict)
      ManifestGenerator.AddPackagesToManifest(featurelistForManifest, ignore_feature_list, package_dict, package_mandatory_dict, feature_package_dict)
      ManifestGenerator.GenerateOutputXml('TestManifest.xml')

  else:
    print 'Please give inputfile parameter'
    return

if __name__ == '__main__':
    sys.exit(main(sys.argv))
