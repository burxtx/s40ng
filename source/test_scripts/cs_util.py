# coding: utf-8
# author: Ethan
import json, re
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
	def cpf2phone(self, s):
		# used for converting media file type name to phone displayed
		s_words = s.split(" ")
		new_words = []
		new_words.append(s_words[0])
		for word in s_words[1:]:
			new_word = word.lower()
			new_words.append(new_word)
		return " ".join(new_words)
	
	def bhdconvert(self, setting, value, bits):
		if "GSM A5" in setting:
			bit_index = re.findall(r"GSM A5/(\d+) ciphering algorithm support", setting)[0]
		if "GPRS GEA" in setting:
			bit_index = re.findall(r"GPRS GEA(\d+) algorithm support", setting)[0]
		if value == True:
			swap =  1 << int(bit_index)-1
			bits = bits | swap
		elif value == False:
			swap = ~(1 << int(bit_index)-1)
			bits = bits & swap
		return bits

	def get_phone_setting(self, setting):
	    # read phone config.db
	    value = self.sx('(send (send config-manager get-setting "%s") ->string)' % setting)
	    return value
	# check files from phone
	def get_phone_music(self, f=None):
		# get non system music files from Music
		self.tc.navigate('Music')
		self.tc.select("Songs")
		# get rid of file type: e.g.".mp3"
		f = f.split(".")[0]
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
		if "Alarm" in ft:
			ft = "Alarm tone"
		if "Message" in ft:
			ft = "Message tone"
		if "Ring" in ft:
			if self.tc.check("Ringtone"):
				self.tc.select("Ringtone")
			elif self.tc.check("SIM1 ringtone"):
				self.tc.select("SIM1 ringtone")
			else:
				self.tc.comment("[ERROR] Oops, something went wrong")
			r = -1 if self.tc.check(f) == False else 0
			self.tc.exit()
			return r
		if "Alert" in ft:
			ft = "Reminder tone"
		self.tc.select(ft)
		r = -1 if self.tc.check(f) == False else 0
		self.tc.exit()
		return r
		
	def check_phone_profile_tone(self, f=None, ft=None):
		self.tc.navigate('Settings')
		self.tc.select('Sounds and vibra')
		self.tc.comment(ft)
		ft = self.cpf2phone(ft)
		self.tc.comment(ft)
		r = -1 if self.tc.check(f, relatedTo=ft) == False else 0
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
		# get rid of file type: e.g.".mp3"
		f = f.split(".")[0]
		r = -1 if self.tc.check(f) == False else 0
		self.tc.exit()
		return r

	def get_phone_graphic_non_sys(self, f=None):
		self.tc.navigate('Files')
		self.tc.select('Phone memory')
		self.tc.select('Photos')
		r = -1 if self.tc.check(f) == False else 0
		self.tc.exit()
		return r

	def check_phone_app(self, app, remove=False, icon=None):
		if "NokiaChat" or "NokiaGift" in app:
			app = app.replace("Nokia", "")
		app = "*" + app + "*"
		r = -1 if self.tc.check(app) == False else 0
		# judge app removal attribute
		if remove:
			r = -1 if r == 0 else 0
			return r
		# judge app found or not
		else:
			if r == -1:
				return r
			# if app found, open it then check icon(icon check not implemented)
			elif r == 0:
				self.tc.select(app)
				self.tc.exit()
				if icon:
					r = self.tc.compareImage('reference_files\\images\\app_list_folder', timeout=10000)
					self.tc.comment(r)
				return r
				
	def check_bmk(self, bmk, inapplist="1", inbrowser="0", icon=None):
		# judge if in app list or folder
		if inapplist != "1" and inapplist != "0":
			self.tc.select(inapplist)
			r = -1 if self.tc.check(bmk) == False else 0
		if inapplist == "1":
			# judge if folder name is "1"
			if self.tc.check("1"):
				self.tc.select("1")
			r = -1 if self.tc.check(bmk) == False else 0
		if inapplist == "0":
			r = 0 if self.tc.check(bmk) == False else -1
		# if icon:
		# 	r2 = self.tc.check(icon)
		self.tc.exit()
		return r

    # check phone UI
	def check_phone_bluetooth_ui(self, visible=True, device_name="Nokia 501"):
		img = "widgets/bool-on-dark" if visible == True else "widgets/bool-off-dark"
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

	def check_phone_time_date_ui(self, timeformat24h=True, nitz_update=True, dateformat="DD-MM-YYYY"):
		tf24h = 'widgets/switch-bg-on-dark' if timeformat24h == True else 'widgets/switch-bg-off-dark'
		nitz = 'widgets/switch-bg-on-dark' if nitz_update == True else 'widgets/switch-bg-off-dark'
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

	def check_phone_network_ui(self, auto_update=False):
		auto_update_opt = 'widgets/switch-bg-on-dark' if auto_update == True else 'widgets/switch-bg-off-dark'
		self.tc.navigate("Settings")
		self.tc.select("Phone update")
		# Phone ui updated from 'Get update' to "check via mobile data"
		r = self.tc.check(auto_update_opt, relatedTo="Check via mobile data")
		if not r:
			self.tc.fail("[fail] phone update incorrect")
		self.tc.exit()
		return r

	def check_phone_sms_ui(self, delivery_report=True, num_lock=False, sim1=False, sim2=False):
		delivery_report_opt = "widgets/switch-bg-on-dark" if delivery_report == True else "widgets/switch-bg-off-dark"
		self.tc.navigate("Settings")
		self.tc.select("Messaging")
		# check if DS or SS
		if sim1:
			r1 = self.tc.check(delivery_report_opt, relatedTo="SIM1//Delivery reports")
		if sim2:
			r1 = self.tc.check(delivery_report_opt, relatedTo="SIM2//Delivery reports")
		else:
			r1 = self.tc.check(delivery_report_opt, relatedTo="Delivery reports")
		if not r1:
			self.tc.fail("[fail] sms delivery report incorrect")

		if num_lock == False:
			num_lock_opt = "Add number"
			r2 = self.tc.check(num_lock_opt, relatedTo="Message center")
			if not r2:
				self.tc.fail("[fail] sms center number locked")
		else:
			r2 = True if self.tc.check("Message center") else False
		return r1, r2

	def check_phone_mms_ui(self, delivery_report=True, allow_adverts=True, reception=1):
		delivery_report_opt = "widgets/switch-bg-on-dark" if delivery_report == True else "widgets/switch-bg-off-dark"
		allow_adverts_opt = "widgets/switch-bg-on-dark" if allow_adverts == True else "widgets/switch-bg-off-dark"
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

	def check_phone_certificate(self, cer):
		self.tc.navigate("Settings")
		self.tc.select("Certificates in use")
		cer = cer[0:5]+"*"
		self.tc.comment(cer)
		r = self.tc.check(cer)
		self.tc.exit()
		return r

	def check_operator_channel(self, channel="", flag=False):
		self.tc.navigate("Settings")
		self.tc.select("Operator messages")
		r1 = r2 = True
		opt = "widgets/switch-bg-on-dark" if flag == True else "widgets/switch-bg-off-dark"
		r1 = self.tc.check(opt, relatedTo="Operator messages")
		if not r1:
			self.tc.comment("[fail] Cell broadcast reception is incorrect")
		if channel != "":
			if not self.tc.check("Channels"):
				# self.tc.select("Operator messages")
				self.tc.select("*Receive messages*", relatedTo="Operator messages")
			r2 = self.tc.check("*"+channel+"*", relatedTo="Channels")
			if not r2:
				self.tc.comment("[fail] Channel is incorrect")
		self.tc.exit()
		return r1, r2

	def check_main_menu(self):
		# r = self.tc.check(item, occurrence=int(position))
		for item in self.tc.read.texts():
			self.tc.comment(item)


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