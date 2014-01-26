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
    def cpf2phone2(self, s):
        # another version for cpf2phone(), translate en to textID
        if "Email" in s:
            s = "nEspZfTVd1aMGuhRiLrr4OZ"
        elif "Message" in s:
            s = "naJBfedkDqkWCF5fRgefg0Q"
        elif "Alarm" in s:
            s = "n4kdK77AlNT9csHoHUu5eZe"
        elif "Reminder" in s:
            s = "nvuTOvN44pThHOsZXah1yQV"
        elif "Push" in s:
            s = "nvNXFy0mTTMbsMMLvTxVahQ"
        elif "SIM1 Ringtone" == s:
            s = "nQ3GdAgPc2hctWzezJkNFlp"
        elif "SIM2 Ringtone" == s:
            s = "nIdiICvyqaL7angsKBL4J9v"
        elif "Ringtone" == s:
            s = "nKSmLJn7WZD0UXH8fxOToFQ"
        return s

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
    # check media files from phone
    def get_phone_music(self, f=None):
        # get non system music files from Music
        self.tc.navigate('nrf38HL_3U0GzWB4QIbha7A') # (Music)
        self.tc.select("nGvEiS2nF-kChHMM29cV6zg") # (Songs)
        # get rid of file type: e.g.".mp3"
        f = f.split(".")[0]
        r = -1 if self.tc.check(f) == False else 0
        self.tc.exit()
        return r
    def get_phone_memory_music(self, f=None):
        pass
    def get_phone_tone_non_sys(self, f=None):
        self.tc.navigate('nTcnBNaw1uP6xnG1qtrpbtA') # (Files)
        self.tc.select('nuYCeSjyprUScP5eyLL-zqw') # (Phone memory)
        self.tc.select('nd3ZdGMKNf0GCgPzZZK86Fg') # (Tones)
        r = -1 if self.tc.check(f) == False else 0
        self.tc.exit()
        return r

    def get_phone_tone_sys(self, f=None, ft=None):
        self.tc.navigate('nP6YDmTdaqE2U0eXQBadWwg') # (Settings)
        self.tc.select('nHRsBbwRbmQJkNHowX6zSW8') # (Sounds and vibra)
        # select tone type
        if "Alarm" in ft: # (Alarm)
            ft = "n4kdK77AlNT9csHoHUu5eZe" # (Alarm tone)
        if "Message" in ft: # (Message)
            ft = "naJBfedkDqkWCF5fRgefg0Q" # (Message tone)
        if "Ring" in ft:
            if self.tc.check("nKSmLJn7WZD0UXH8fxOToFQ"): # (Ringtone)
                self.tc.select("nKSmLJn7WZD0UXH8fxOToFQ") # (Ringtone)
            elif self.tc.check("nQ3GdAgPc2hctWzezJkNFlp"): # (SIM1 ringtone)
                self.tc.select("nQ3GdAgPc2hctWzezJkNFlp") # (SIM1 ringtone)
            else:
                self.tc.comment("[ERROR] Oops, something went wrong")
            r = -1 if self.tc.check(f) == False else 0
            self.tc.exit()
            return r
        if "Alert" in ft:
            ft = "nvuTOvN44pThHOsZXah1yQV" # (Reminder tone)
        self.tc.select(ft)
        r = -1 if self.tc.check(f) == False else 0
        self.tc.exit()
        return r
        
    def check_phone_profile_tone(self, f=None, ft=None):
        self.tc.navigate('nP6YDmTdaqE2U0eXQBadWwg') # (Settings)
        self.tc.select('nHRsBbwRbmQJkNHowX6zSW8') # (Sounds and vibra)
        ft = self.cpf2phone2(ft)
        r = -1 if self.tc.check(f, relatedTo=ft) == False else 0
        self.tc.exit()
        return r
                # self.tc.comment("[fail once] tone: %s" % f["file"])
                # self.tc.select(f["type"])
                # self.tc.tryExpect(f["file"])
                # self.tc.comment("[fail twice] should not be here")
                # self.tc.back()
            # else:
            #     self.tc.comment("[pass] profile tone: %s" % f["file"])
            #     self.tc.exit.back()
            #     return 0

    def get_phone_video(self, f=None):
        self.tc.navigate("nL9i6QbDGske_5ld7GEJWYw") # (Videos)
        self.tc.check(f)
        # get rid of file type: e.g.".mp3"
        f = f.split(".")[0]
        r = -1 if self.tc.check(f) == False else 0
        self.tc.exit()
        return r

    def get_phone_graphic_non_sys(self, f=None):
        self.tc.navigate('nTcnBNaw1uP6xnG1qtrpbtA') # (Files)
        self.tc.select('nuYCeSjyprUScP5eyLL-zqw') # (Phone memory)
        self.tc.select('n_bT8twBoO0SggW2aLhX0jQ') # (Photos)
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
        #     r2 = self.tc.check(icon)
        self.tc.exit()
        return r

    # check phone UI
    def check_phone_bluetooth_ui(self, visible, device_name):
        img = "widgets/bool-on-dark" if visible == True else "widgets/bool-off-dark"
        self.tc.navigate("nP6YDmTdaqE2U0eXQBadWwg") # (Settings)
        self.tc.select("nSKlSLpTSAEGpb_3DSouY7w") # (Bluetooth)
        if not self.tc.check("n62J85edzT0T1VFh02LhDyB"): # (Visible)
            self.tc.select("widgets/switch-bg-off-dark", relatedTo="nSKlSLpTSAEGpb_3DSouY7w") # (Bluetooth)
        if self.tc.check("n62J85edzT0T1VFh02LhDyB"): # (Visible)
            r = self.tc.check(img, relatedTo='n62J85edzT0T1VFh02LhDyB') # (Visible)
            if not r:
                self.tc.fail("[fail] bluetooth visible incorrect")
        else:
            self.tc.comment('"Visible" option is not displayed.')
            r = False
        if device_name:
            r2 = self.tc.check(device_name, relatedTo="n_cNST38ix06zcgs1iuShZg") # (Device name)
            if not r2:
                self.tc.fail("[fail] bluetooth device name is incorrect")
            self.tc.exit()
            return r, r2
        self.tc.exit()
        return r

    def check_phone_time_date_ui(self, timeformat24h, nitz_update, dateformat):
        tf24h = '24-hour clock' if timeformat24h == True else '12-hour clock'
        # tf24h = 'widgets/switch-bg-on-dark' if timeformat24h == True else 'widgets/switch-bg-off-dark'
        nitz = 'widgets/switch-bg-on-dark' if nitz_update == True else 'widgets/switch-bg-off-dark'
        self.tc.navigate("nP6YDmTdaqE2U0eXQBadWwg") # (Settings)
        self.tc.select("nK8Fa6ELAX0_Q0lqZHRYuQA") # (Time and date)

        r3 = self.tc.check(nitz, relatedTo="nSuy8tLNYY0aXpGkDP9w1Qw") # (Set automatically)
        if not r3:
            self.tc.fail("[fail] nitz incorrect")
        r1 = self.tc.check(dateformat, relatedTo="nL0fIeyzTLECEY-I4Cgq3hQ") # (Date format)
        if not r1:
            self.tc.comment("[manual] please manually check date format")
        r2 = self.tc.check(tf24h, relatedTo="noSQOOdIy4kG4OYvp7urJ_w") # (Time format)
        if not r2:
            self.tc.fail("[fail] time format incorrect")
        self.tc.exit()
        return r1, r2, r3

    def check_phone_network_ui(self, auto_update=False):
        auto_update_opt = 'widgets/switch-bg-on-dark' if auto_update == True else 'widgets/switch-bg-off-dark'
        self.tc.navigate("nP6YDmTdaqE2U0eXQBadWwg") # (Settings)
        self.tc.select("n1LGfRsdkGzVtpbW5khwOXn") # (Phone update)
        # Phone ui updated from 'Get update' to "check via mobile data"
        r = self.tc.check(auto_update_opt, relatedTo="Check via mobile data")
        if not r:
            self.tc.fail("[fail] phone update incorrect")
        self.tc.exit()
        return r

    def check_phone_sms_ui(self, delivery_report_1, num_lock, delivery_report_2=None, dual=False):
        delivery_report_opt_1 = "widgets/switch-bg-on-dark" if delivery_report_1 else "widgets/switch-bg-off-dark"
        delivery_report_opt_2 = "widgets/switch-bg-on-dark" if delivery_report_2 else "widgets/switch-bg-off-dark"
        # delivery_report_opt_1 = "nv3QRA238SUKYbG-FDnpGTw" if delivery_report_1 else "n3obwYFAQkka58MD98utRTA" # (Yes) # (No)
        # delivery_report_opt_2 = "nv3QRA238SUKYbG-FDnpGTw" if delivery_report_2 else "n3obwYFAQkka58MD98utRTA" # (Yes) # (No)

        self.tc.navigate("nP6YDmTdaqE2U0eXQBadWwg") # (Settings)
        self.tc.select("nopeC8kE_okiWerqcmwYDbA") # (Messaging)
        self.tc.check("nnPfCfUKN1UeqQxmSkHeGU2") # (Text message settings)
        # check if DS or SS
        if dual:
            # if SIM card is empty, give message
            unempty_1 = self.tc.tryExpect("nLWWCDTGszODgKbCqvl511g") # (SIM1)
            if unempty_1:
                r1_1 = self.tc.tryExpect(delivery_report_opt_1, relatedTo="nLWWCDTGszODgKbCqvl511g//n1ocIwPRxc91sODUhFnz21o")# (SIM1)#(Delivery reports)
            else:
                self.tc.comment("[Oops] Maybe SIM1 is empty")
                r1_1 = False
            unempty_2 = self.tc.tryExpect("nGG3fTuTHN7PXE5DeIQqU5R") # (SIM2)
            if unempty_2:
                r1_2 = self.tc.tryExpect(delivery_report_opt_2, relatedTo="nGG3fTuTHN7PXE5DeIQqU5R//n1ocIwPRxc91sODUhFnz21o")#(SIM2)#(Delivery reports)
            else:
                self.tc.comment("[Oops] Maybe SIM2 is empty")
                r1_2 = False
            if r1_1 and r1_2:
                r1 = True
            else:
                if not r1_1:
                    self.tc.comment("[fail] SIM1 sms delivery report incorrect")
                if not r1_2:
                    self.tc.comment("[fail] SIM2 sms delivery report incorrect")
                r1 = False
        else:
            r1 = self.tc.expect(delivery_report_opt_1, relatedTo='nnPfCfUKN1UeqQxmSkHeGU2//n1ocIwPRxc91sODUhFnz21o')# (Text message settings) # (Delivery reports)
            if not r1:
                self.tc.comment("[fail] SS sms delivery report incorrect")
        # check message centre
        mc = self.tc.check("n1YQSAhckQkKel4i22xY3kg")#(Message centre)
        r2 = mc^num_lock
        if not r2:
            self.tc.comment("[fail] sms center number lock is incorrect")
        return r1, r2

    def check_phone_mms_ui(self, delivery_report_1, allow_adverts_1, reception_1, delivery_report_2=None, allow_adverts_2=None, reception_2=None, dual=False):
        delivery_report_opt_1 = "widgets/switch-bg-on-dark" if delivery_report_1 else "widgets/switch-bg-off-dark"
        allow_adverts_opt_1 = "widgets/switch-bg-on-dark" if allow_adverts_1 else "widgets/switch-bg-off-dark"
        delivery_report_opt_2 = "widgets/switch-bg-on-dark" if delivery_report_2 else "widgets/switch-bg-off-dark"
        allow_adverts_opt_2 = "widgets/switch-bg-on-dark" if allow_adverts_2 else "widgets/switch-bg-off-dark"
        reception_opt = {"1":"nqiS2Sc0CqEiVtVzDK_lrZw", "2":"nPFIakEhTT8egavEUCbHJrV", "3":"nS6_XgM9yIUWDnPkuArBdJQ", "4":"nk3O_tC198US-hSpK7XDHNA"} # (Always) # (Only when mobile data is on) # (Manually) # (Off)
        self.tc.navigate("nP6YDmTdaqE2U0eXQBadWwg") # (Settings)
        self.tc.select("nopeC8kE_okiWerqcmwYDbA") # (Messaging)
        self.tc.check("nxU8aiSOxDDFx6pTEKnI2iH") # (MMS settings)
        if dual:
            unempty_1 = self.tc.tryExpect("nLWWCDTGszODgKbCqvl511g") # (SIM1)
            if unempty_1:
                #(SIM1) #(Delivery reports)
                r1_1 = self.tc.tryExpect(delivery_report_opt_1, relatedTo="nLWWCDTGszODgKbCqvl511g//n1ocIwPRxc91sODUhFnz21o")
                r2_1 = self.tc.tryExpect(reception_opt[reception_1], relatedTo="nLWWCDTGszODgKbCqvl511g//n32sMoMMXMT75yENRBRsSsL")#(SIM1)#(MMS reception)
                r3_1 = self.tc.tryExpect(allow_adverts_opt_1, relatedTo="nLWWCDTGszODgKbCqvl511g//niHrIvI97C6oyb7XnOp7qDr")#(SIM1)#(Allow adverts)
            else:
                self.tc.comment("[Oops] Maybe SIM1 slot is empty")
                r1_1 = r2_1 = r3_1 = False
            self.tc.gesture.swipe((60,319),(60,10))
            unempty_2 = self.tc.tryExpect("nGG3fTuTHN7PXE5DeIQqU5R") # (SIM2)
            if unempty_2:
                r3_2 = self.tc.check(allow_adverts_opt_2, relatedTo="nxU8aiSOxDDFx6pTEKnI2iH//nGG3fTuTHN7PXE5DeIQqU5R//niHrIvI97C6oyb7XnOp7qDr")#(MMS settings)#(SIM2)#(Allow adverts)
                r2_2 = self.tc.check(reception_opt[reception_2], relatedTo="nxU8aiSOxDDFx6pTEKnI2iH//nGG3fTuTHN7PXE5DeIQqU5R//n32sMoMMXMT75yENRBRsSsL")#(MMS settings)#(SIM2)#(MMS reception)
                r1_2 = self.tc.check(delivery_report_opt_2, relatedTo="nxU8aiSOxDDFx6pTEKnI2iH//nGG3fTuTHN7PXE5DeIQqU5R//n1ocIwPRxc91sODUhFnz21o")#(MMS settings)#(SIM2)#(Delivery reports)
            else:
                self.tc.comment("[Oops] Maybe SIM2 slot is empty")
                r1_2 = r2_2 = r3_2 = False
            if r1_1 and r1_2:
                r1 = True
            else:
                if not r1_1:
                    self.tc.comment("[fail] SIM1 MMS delivery report incorrect")
                if not r1_2:
                    self.tc.comment("[fail] SIM2 MMS delivery report incorrect")
                r1 = False
            if r2_1 and r2_2:
                r2 = True
            else:
                if not r2_1:
                    self.tc.comment("[fail] SIM1 MMS reception incorrect")
                if not r2_2:
                    self.tc.comment("[fail] SIM2 MMS reception incorrect")
                r2 = False
            if r3_1 and r3_2:
                r3 = True
            else:
                if not r3_1:
                    self.tc.comment("[fail] SIM1 MMS adverts incorrect")
                if not r3_2:
                    self.tc.comment("[fail] SIM2 MMS adverts incorrect")
                r3 = False
        else:
            r1 = self.tc.check(delivery_report_opt_1, relatedTo="nxU8aiSOxDDFx6pTEKnI2iH//n1ocIwPRxc91sODUhFnz21o")#(MMS settings)#(Delivery reports)
            r2 = self.tc.check(reception_opt[reception_1], relatedTo="nxU8aiSOxDDFx6pTEKnI2iH//n32sMoMMXMT75yENRBRsSsL")#(MMS settings)#(MMS reception)
            r3 = self.tc.check(allow_adverts_opt_1, relatedTo="nxU8aiSOxDDFx6pTEKnI2iH//niHrIvI97C6oyb7XnOp7qDr")#(MMS settings)#(Allow adverts)
            if not r1:
                self.tc.comment("[fail] SS MMS delivery report incorrect")
            if not r2:
                self.tc.comment("[fail] SS MMS reception incorrect")
            if not r3:
                self.tc.comment("[fail] SS MMS adverts incorrect")
        return r1, r2, r3
        
    def check_phone_voicemail_ui(self, voicemail_num="123"):
        self.tc.navigate("nP6YDmTdaqE2U0eXQBadWwg") # (Settings)
        self.tc.select("nnT9SW58e7kiv4W57E8DKZQ") # (Calls)
        r = self.tc.check(voicemail_num, relatedTo="n3ETTgGPZunmmwVPB7AqLLT", timeout=30000) # (Voice mailbox)
        if not r:
            self.tc.fail("[fail] voice mailbox number incorrect")
        self.tc.exit()
        return r

    def check_phone_certificate(self, cer):
        self.tc.navigate("nP6YDmTdaqE2U0eXQBadWwg") # (Settings)
        self.tc.select("n2nuDOKVzLOiml0yGbGlIA3") # (Certificates in use)
        cer = cer[0:5]+"*"
        self.tc.comment(cer)
        r = self.tc.check(cer)
        self.tc.exit()
        return r

    def check_operator_channel(self, flag=False, cb_channels="", pb_channels = ""  ):
        self.tc.navigate("nP6YDmTdaqE2U0eXQBadWwg") # (Settings)
        self.tc.select("nKW3a3R7Gp0eEgTuVkb2LYA") # (Operator messages)
        r1 = r2 = r3 = True
        opt = "widgets/switch-bg-on-dark" if flag == True else "widgets/switch-bg-off-dark"
        r1 = self.tc.check(opt)
        if not r1:
            self.tc.fail("[fail] Cell broadcast reception is incorrect")
        
        # check CB channels
        if cb_channels != "":
            r2 = False
            l = cb_channels.split (",")
            self.tc.comment(l)
            if not flag:
                self.tc.select ("widgets/switch-bg-off-dark")
            if self.tc.check("ncXVIEXysz0aD2epLoaot5A"): # (Channels)
                self.tc.select("ncXVIEXysz0aD2epLoaot5A") # (Channels)
                for ch in l:
                    r2 = self.tc.check (ch)
                    if not r2: 
                        self.tc.comment ("Channel %s is not found" % ch)
                        break            
            self.tc.back()
            if not flag:                
                self.tc.select ("widgets/switch-bg-on-dark")
            if not r2:
                self.tc.fail("[fail] CB Channels checking failed")            
        
        # check PB channels
        if pb_channels != "":
            r3 = False
            if not flag:
                self.tc.select ("widgets/switch-bg-off-dark")        
            l1 = []
            l = pb_channels.split(',')
            for m in l:
                l1.append(m.split (':'))
            d = dict (l1)
            self.tc.comment(d)
            if self.tc.check("ncXVIEXysz0aD2epLoaot5A"): # (Channels)
                self.tc.select("ncXVIEXysz0aD2epLoaot5A") # (Channels)
                for ch in d:
                    r3 = self.tc.check (ch)
                    if not r3: 
                        self.tc.comment ("Channel %s is not found" % ch)
                        break            
            self.tc.back()
            if not flag:                    
                self.tc.select ("widgets/switch-bg-on-dark")
            if not r3:
                self.tc.fail("[fail] PB Channels checking failed")                        
        self.tc.exit()
        return r1, r2, r3

    def check_nokia_improvement(self, is_improvement = False):
        status_opt = "widgets/switch-bg-on-dark" if is_improvement == True else "widgets/switch-bg-off-dark"
        self.tc.navigate("nP6YDmTdaqE2U0eXQBadWwg") # (Settings)
        self.tc.select("nOG8SGsCh8xs1N7obFSlg8h") # (Improvement program)
        r = self.tc.check(status_opt)
        if not r:
            self.tc.fail("[failed] Improvement program wrong result")
        self.tc.exit()
        return r            
    
    def check_mobile_data_settings(self, flag=False, flag2=False, flag2_v=False):
        r = r2 = True
        status_opt = "widgets/switch-bg-on-dark" if flag==True else "widgets/switch-bg-off-dark"
        self.tc.navigate("nP6YDmTdaqE2U0eXQBadWwg") # (Settings)
        # Dual SIM 
        if self.tc.check ("nMpXGiFKwETLgr9dXXyi1rC"): # (Dual SIM)
            self.tc.select("nMpXGiFKwETLgr9dXXyi1rC") # (Dual SIM)
        # Single SIM
        elif self.tc.check ("nHyKBqFbZmTlK7ZxO1IIWhT"): # (Mobile data)
            self.tc.select("nHyKBqFbZmTlK7ZxO1IIWhT") # (Mobile data)
        # Check mobile data switch
        r = self.tc.check(status_opt)
        if not r:
            self.tc.fail("[failed] Mobile data usage status wrong")
        # Check mobile data connection mode
        if flag2:
            if not flag:
                self.tc.select (status_opt)                 
            r2 = self.tc.check ("nkwwbKks0P1WVAOFGxnKSde", relatedTo = "nNHbdxSrfSTh901oXXcktXX") if flag2_v==False else self.tc.check ("nB9fxtWahqIr8C73K1k2Imf", relatedTo = "nNHbdxSrfSTh901oXXcktXX") # (When needed) # (Data connection mode) # (Always online) # (Data connection mode)
            if not flag: 
                status_opt = "widgets/switch-bg-on-dark"
                self.tc.select (status_opt)
            if not r2: 
                self.tc.fail ("[failed] Mobile data connection mode wrong")
        self.tc.exit()
        return r , r2
    
    def check_emergency_call(self, number=None):
        self.tc.navigate('nMVhfaecLikGJ1PI3AMH4mQ') # (Phone)
        self.tc.input.write(number)
        self.tc.expect(number, timeout = 2000)#verify the input is displaying correctly.
        self.tc.select('voice-call-application/answer-call')
        if not self.tc.check('nrWSeF_nDfUyOo8lW2iTl_w', timeout = 2000): # (Emergency call)
            self.tc.fail('[fail] Dial emergency call: %s' % number)
            self.tc.exit()
            return False
        else:
            self.tc.select('voice-call-application/reject-call')
            self.tc.exit()
            return True

    def check_customer_account (self, cc_account):
        self.tc.navigate("nP61VAbxwpzDgEJM7n5avHb") # (Accounts)
        self.tc.select("toolbar/toolbar-bg-light")
        r = self.tc.check(cc_account)
        if not r:
            self.tc.fail("[fail] customer account checking failed")
        self.tc.exit()
        return r
    
    def check_mmc_content(self, ftype, f_list):
        results = []
        self.tc.navigate("nTcnBNaw1uP6xnG1qtrpbtA") # (Files)
        self.tc.select("nlCsfnv6r-E2w-giKfsctTw") # (Memory card)
        self.tc.select("?xtra")
        self.tc.select(ftype)
        for f in f_list:
            r = self.tc.check(f)
            if not r:
                self.tc.comment("[fail] %s not found from %s folder" % (f, ftype))
                results.append(f)
            else:
                self.tc.comment("[pass] %s found from %s folder" % (f, ftype))
        self.tc.exit()
        return results
    # def compare_settings(self, fv, pv):
    #     # convert True to true
    #     if fv == True or False:
    #         fv = str(fv).lower()
 #        r = cmp(str(fv), str(pv))
 #        return r

    # def check_phone_messaging(self):
        # self.tc.navigate("nP6YDmTdaqE2U0eXQBadWwg") # (Settings)

    # def check_phone_contacts(self):
        # self.tc.navigate("nP6YDmTdaqE2U0eXQBadWwg") # (Settings)

    # def check_phone_time_and_date(self):
        # self.tc.navigate("nP6YDmTdaqE2U0eXQBadWwg") # (Settings)

    # def addlog(self, setting='', res):
    #     status = "pass" if res == 0 else "fail"
    #     self.comment("---[setting][%s]%s " % (status, setting))
