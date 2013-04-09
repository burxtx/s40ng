# coding: utf-8
# author: Ethan
import json
import os.path
import core
from core import uitestcase

class SettingUtil(uitestcase.UITestCase):
	def __init__(self, tc):
		self.tc = tc
		
	def converter(self, ftype):
	    # convert file type to py dict
	    f = open(ftype)
	    if isinstance(f, file):
	        s = json.load(f)
	    f.close()
	    return s

	def get_phone_setting(self, setting):
	    # read phone config.db
	    value = self.sx('(send (send config-manager get-setting "%s") ->string)' % setting)
	    return value
	# check files from phone
	def get_phone_music(self, f=None):
		# get non system music files from Music
		self.tc.navigate('Music')
		self.tc.select("Songs")
		r = -1 if self.tc.check(f) == False else 0
		self.tc.exit()
		return r

	def get_phone_tone_non_sys(self, f=None):
		self.tc.navigate('Files')
		self.tc.select('Phone memory')
		self.tc.select('Tones')
		r = -1 if self.tc.check(f) == False else 0
		self.tc.exit()
		return r

	def get_phone_tone_sys(self, f=None, ft=None):
		self.tc.navigate('Settings')
		self.tc.select('Sounds and vibra')
		# select tone type
		self.tc.select(ft)
		r = -1 if self.tc.check(f) == False else 0
		self.tc.exit()
		return r
		
	def check_phone_profile_tone(self, f=None):
		self.tc.navigate('Settings')
		self.tc.select('Sounds and vibra')
		r = -1 if self.tc.check(f) == False else 0
		self.tc.exit()
		return r
				# self.tc.comment("[fail once] tone: %s" % f["file"])
				# self.tc.select(f["type"])
				# self.tc.tryExpect(f["file"])
				# self.tc.comment("[fail twice] should not be here")
				# self.tc.back()
			# else:
			# 	self.tc.comment("[pass] profile tone: %s" % f["file"])
			# 	self.tc.exit.back()
			# 	return 0

	def get_phone_video(self, f=None):
		self.tc.navigate("Videos")
		self.tc.check(f)
		r = -1 if self.tc.check(f) == False else 0
		self.tc.exit()

	def get_phone_graphic_non_sys(self, f=None):
		self.tc.navigate('Files')
		self.tc.select('Phone memory')
		self.tc.select('Photos')
		r = -1 if self.tc.check(f) == False else 0
		self.tc.exit()
		return r
    # check phone UI
	def check_phone_bluetooth(self, fv):
		self.tc.navigate("Settings")
		self.tc.select("Bluetooth")
		if not self.tc.check("Visible"):
			self.tc.select("Bluetooth")
		if self.tc.check("Visible"):
			pv = self.tc.check("widgets/bool-on-dark")
		else:
			self.tc.comment('"Visible" option is not displayed.')
			pv = False
		r = cmp(str(fv), str(pv))
		self.tc.exit()
		return r, pv

	def check_phone_app(self, app, remove=False):
		r = -1 if self.tc.check(app) == False else 0
		if r == -1:
			if remove:
				return 0
			return r
		else:
			self.tc.select(app)
		self.tc.exit()
		return r

	# def compare_settings(self, fv, pv):
	# 	# convert True to true
	# 	if fv == True or False:
	# 		fv = str(fv).lower()
 #        r = cmp(str(fv), str(pv))
 #        return r

	# def check_phone_messaging(self):
		# self.tc.navigate("Settings")

	# def check_phone_contacts(self):
		# self.tc.navigate("Settings")

	# def check_phone_time_and_date(self):
		# self.tc.navigate("Settings")

	# def addlog(self, setting='', res):
	# 	status = "pass" if res == 0 else "fail"
	# 	self.comment("---[setting][%s]%s " % (status, setting))