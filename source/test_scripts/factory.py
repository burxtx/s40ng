# from material import template
from lxml import etree
import json

source = "1317d2_test_automation_input.xml"
tag_focus_layer = "focus-layer"
tag_setting = 'setting'
tag_main_view = 'main-view'
tag_sub_view = 'sub-view'
tag_setting_name = tag_sub_setting_name = 'name'
tag_value = 'value'
tag_subsetting = 'subsetting'
tag_reference = 'reference'
tag_sequence = 'sequence'
py_all = {}
py_group_list = []
py_feature_list = []
py_setting_list = []

tree = etree.parse(source)
focus_layer_node = tree.iter(tag_focus_layer)
for layer in focus_layer_node:
	setting_node = layer.iter(tag_setting)
	for setting in setting_node:
		mainview_node = setting.iter(tag_main_view)
		for mainview in mainview_node:
			group = mainview.text
			if group:
				if not py_all.has_key(group):
					py_all[group] = {}

		subview_node = setting.iter(tag_sub_view)
		for subview in subview_node:
			feature = subview.text
			if feature and group:
				# print "--[feature] %s" % feature
				if not py_all[group].has_key(feature):
					py_all[group][feature]={}

		name_node = setting.findall('.//name')
		setting_name = name_node[0].text
		if setting_name and feature and group:
			# print "---[setting] %s" % setting_name
			if not py_all[group][feature].has_key(setting_name):
				py_all[group][feature][setting_name]=[]
		# handle multi settings
		# handle sequence
		sequence_node = setting.findall('.//value/sequence')
		if sequence_node:
			for i, sequence in enumerate(sequence_node):
				if setting_name and feature and group:
					py_all[group][feature][setting_name].append({})

				sub_value_node = sequence.findall('.//*')
				if sub_value_node:
					for sub_value in sub_value_node:
						subsetting_node = setting.iter(tag_subsetting)
						for subsetting in subsetting_node:
							ref_node = subsetting.findall('.//reference')
							sub_setting_name_node = subsetting.findall('.//name')
							ref = ref_node[0].text
							sub_setting_name = sub_setting_name_node[0].text
							if ref in sub_value.attrib['reference']:
								if sub_value.text and setting_name and feature and group:
									py_all[group][feature][setting_name][i][sub_setting_name]=sub_value.text

		else:
			value_node = setting.iter(tag_value)
			for value in value_node:
				value = value.text
				if value and setting_name and feature and group:
					# if py_all[group][feature].has_key(setting_name):
					# print "----[expect value] %s" % value
					py_all[group][feature][setting_name].append({tag_value:value})
					# print py_all

print json.dumps(py_all, indent=4)
# further plan: directly grep py_group_list from Nuage Variant Summary page, or even Accept360
py_group_list = []
py_feature_list = []
py_setting_list = []

for group in py_group_list:
    py_all[group] = {}
    for feature in py_feature_list:
        py_all[group][feature] = {}
