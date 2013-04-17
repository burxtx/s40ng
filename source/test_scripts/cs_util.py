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

	def check_phone_app(self, app, remove=False, icon=None):
		r = -1 if self.tc.check(app) == False else 0
		# app not found
		if r == -1:
			if remove:
				return 0
			return r
		# app is found
		else:
			# if icon is uploaded
			if icon:
				r = self.tc.compareImage('reference_files\\images\\app_list_folder', timeout=10000)
				self.tc.comment(r)
				# if r == -1:
				# 	return r
			self.tc.select(app)
		self.tc.exit()
		return r
		
    # check phone UI
	def check_phone_bluetooth_ui(self, visible=True, device_name=None):
		img = "widgets/bool-on-dark" if visible else "widgets/bool-off-dark"
		self.tc.navigate("Settings")
		self.tc.select("Bluetooth")
		if not self.tc.check("Visible"):
			self.tc.select("widgets/switch-bg-off-dark", relatedTo="Bluetooth")
		if self.tc.check("Visible"):
			r = self.tc.check(img, relatedTo='Visible')
			if not r:
				self.tc.fail("[fail] bluetooth visible incorrect")
		else:
			self.tc.comment('"Visible" option is not displayed.')
			r = False
		if device_name:
			r2 = self.tc.check(device_name, relatedTo="Device name")
			if not r2:
				self.tc.fail("[fail] bluetooth device name is incorrect")
			self.tc.exit()
			return r, r2
		self.tc.exit()
		return r

	def check_phone_time_date_ui(self, dateformat="YYYY-MM-DD", timeformat24h=True, nitz_update=True):
		tf24h = 'widgets/switch-bg-on-dark' if timeformat24h else 'widgets/switch-bg-off-dark'
		nitz = 'widgets/switch-bg-on-dark' if nitz_update else 'widgets/switch-bg-off-dark'
		self.tc.navigate("Settings")
		self.tc.select("Time and date")

		r3 = self.tc.check(nitz, relatedTo="Set automatically")
		if not r3:
			self.tc.fail("[fail] nitz incorrect")
		r1 = self.tc.check(dateformat, relatedTo="Date format")
		if not r1:
			self.tc.fail("[fail] date format incorrect")
		r2 = self.tc.check(tf24h, relatedTo="Time format")
		if not r2:
			self.tc.fail("[fail] time format incorrect")
			
		self.tc.exit()
		return r1, r2, r3

	def check_phone_network_ui(self, auto_update=True):
		auto_update_opt = 'widgets/switch-bg-on-dark' if auto_update else 'widgets/switch-bg-off-dark'
		self.tc.navigate("Settings")
		self.tc.select("Phone update")
		r = self.tc.check(auto_update_opt, relatedTo="Get updates")
		if not r:
			self.tc.fail("[fail] phone update incorrect")
		self.tc.exit()
		return r

	def check_phone_sms_ui(self, delivery_report=True, num_lock=False):
		delivery_report_opt = "widgets/switch-bg-on-dark" if delivery_report else "widgets/switch-bg-off-dark"

		self.tc.navigate("Settings")
		self.tc.select("Messaging")
		r1 = self.tc.check(delivery_report_opt, relatedTo="Delivery reports")
		if not r1:
			self.tc.fail("[fail] sms delivery report incorrect")
		if not num_lock:
			num_lock_opt = "Add number"
			r2 = self.tc.check(num_lock_opt, relatedTo="Message center")
			if not r2:
				self.tc.fail("[fail] sms center number locked")
		else:
			r2 = self.tc.check("Message center")
			if not r2:
				r2 = True
		self.tc.exit()
		return r1, r2

	def check_phone_mms_ui(self, delivery_report=True, allow_adverts=True, reception=1):
		delivery_report_opt = "widgets/switch-bg-on-dark" if delivery_report else "widgets/switch-bg-off-dark"
		allow_adverts_opt = "widgets/switch-bg-on-dark" if allow_adverts else "widgets/switch-bg-off-dark"
		reception_opt = {1:"Automatic", 2:"Manual", 3:"Off", 4:"Off"}
		self.tc.navigate("Settings")
		self.tc.select("Messaging")
		r1 = self.tc.check(allow_adverts_opt, relatedTo="Allow adverts")
		if not r1:
			self.tc.fail("[fail] allow adverts incorrect")
		r2 = self.tc.check(delivery_report_opt, relatedTo="Delivery reports")
		if not r2:
			self.tc.fail("[fail] mms delivery report incorrect")
		r3 = self.tc.check(reception_opt[reception], relatedTo="MMS reception")
		if not r3:
			self.tc.fail("[fail] mms reception incorrect")
		return r1, r2, r3
		
	def check_phone_voicemail_ui(self, voicemail_num="123"):
		self.tc.navigate("Settings")
		self.tc.select("Calls")
		r = self.tc.check(voicemail_num, relatedTo="Voice mailbox")
		if not r:
			self.tc.fail("[fail] voice mailbox number incorrect")
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