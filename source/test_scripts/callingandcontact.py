import core
from core import uitestcase
import json, os.path
from cs_util import *

class CommonSettingCompare(uitestcase.UITestCase):
    # subarea = "Connectivity"
    # feature = "Bluetooth"

    def _commonSettingCompare(self,group,feature,setting):
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        # read configuration items mapping file, for reference
        f_ref = os.path.join(os.path.dirname(__file__), "ref.json").replace("\\", "/")
        f_ref_ss = self.settingutil.converter(f_ref)
        try:
            f = f_ss[group][feature][setting][0]
        except:
            self.skip("[No customization point] at [%s]" % setting)
        sequence = f_ref_ss[group][feature][setting][0]
        if sequence.has_key("ref"):
            ref_value = sequence["ref"]
            p_v = self.sx('(send (send config-manager get-setting "%s") ->string)' % ref_value)
        if f.has_key("value"):
            f_v = f["value"]
            if f_v == True or f_v == False:
                f_v = str(f_v).lower()
            # prevent if phone value is upper started
            if p_v == True or p_v == False:
                p_v = str(p_v).lower()
            r = cmp(str(f_v), str(p_v))
            status = "pass" if r == 0 else "fail"
            if status == "fail":
                self.fail("expect[%s], actual[%s]" % (f_v, p_v))
    
    def _bitmask_settings_compare(self,group,feature,st_key):
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        below_f = os.path.join(os.path.dirname(__file__), "below_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        below_f_ss = self.settingutil.converter(below_f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        f_ref = os.path.join(os.path.dirname(__file__), "ref.json").replace("\\", "/")
        f_ref_ss = self.settingutil.converter(f_ref)

        # hardcoded default value
        # a5_bits = 0b101
        # gea_bits = 0b0000111

        a5_ref_value = "./platform/INFO_PP_A5_CIPHER_ALGORITHMS"
        gea_ref_value = "./platform/INFO_PP_GEA_ALGORITHMS"
        a5_setting = "GSM A5 ciphering algorithm support"
        gea_setting = "GPRS GEA algorithm support"
        amr_f_value = 0
        amr_ref_value = "./platform/INFO_PP_CODEC_ORDER2"
        amr_setting = "Support for wide-band AMR speech"
        # get default values: a5, gea
        a5_lst = [below_f_ss["Calling and Contact"]["Calling Network settings"]["GSM A5/3 ciphering algorithm support"][0]["value"],
        below_f_ss["Calling and Contact"]["Calling Network settings"]["GSM A5/2 ciphering algorithm support"][0]["value"],
        below_f_ss["Calling and Contact"]["Calling Network settings"]["GSM A5/1 ciphering algorithm support"][0]["value"]
        ]
        gea_lst = [below_f_ss["Calling and Contact"]["Calling Network settings"]["GPRS GEA7 algorithm support"][0]["value"],
        below_f_ss["Calling and Contact"]["Calling Network settings"]["GPRS GEA6 algorithm support"][0]["value"],
        below_f_ss["Calling and Contact"]["Calling Network settings"]["GPRS GEA5 algorithm support"][0]["value"],
        below_f_ss["Calling and Contact"]["Calling Network settings"]["GPRS GEA4 algorithm support"][0]["value"],
        below_f_ss["Calling and Contact"]["Calling Network settings"]["GPRS GEA3 algorithm support"][0]["value"],
        below_f_ss["Calling and Contact"]["Calling Network settings"]["GPRS GEA2 algorithm support"][0]["value"],
        below_f_ss["Calling and Contact"]["Calling Network settings"]["GPRS GEA1 algorithm support"][0]["value"]
        ]
        a5_bits = reduce(lambda x,y: int(x)<<1|int(y), a5_lst)
        gea_bits = reduce(lambda x,y: int(x)<<1|int(y), gea_lst)
        # get default value for amr
        if below_f_ss["Calling and Contact"]["Calling Network settings"].has_key("Support for wide-band AMR speech in 2G network"):
            f_v_1 = below_f_ss["Calling and Contact"]["Calling Network settings"]["Support for wide-band AMR speech in 2G network"][0]["value"] 
            if f_v_1:
                amr_f_value = amr_f_value | 2
        if below_f_ss["Calling and Contact"]["Calling Network settings"].has_key("Support for wide-band AMR speech in 3G network"):
            f_v_2 = below_f_ss["Calling and Contact"]["Calling Network settings"]["Support for wide-band AMR speech in 3G network"][0]["value"]
            if f_v_2:
                amr_f_value = amr_f_value | 4            
        # py dict from json file
        
        for setting in f_ss[group][feature]:
            if "GSM A5" in setting and st_key in setting:
                self.comment("[group]%s --> [feature]%s -->[setting]%s" % (group,feature,setting))
                for f in f_ss[group][feature][setting]:
                    if f.has_key("value"):
                        f_v = f["value"]
                        a5_bits = self.settingutil.bhdconvert(setting, f_v, a5_bits)
                        continue
            if "GPRS GEA" in setting and st_key in setting:
                self.comment("[group]%s --> [feature]%s -->[setting]%s" % (group,feature,setting))
                for f in f_ss[group][feature][setting]:
                    if f.has_key("value"):
                        f_v = f["value"]
                        gea_bits = self.settingutil.bhdconvert(setting, f_v, gea_bits)
                        continue
            if "AMR speech in 2G network" in setting and st_key in setting:
                self.comment("[group]%s --> [feature]%s -->[setting]%s" % (group,feature,setting))
                f_v = f_ss[group][feature][setting][0]["value"]
                if f_v:
                    amr_f_value = amr_f_value | 2
                else :
                    amr_f_value = amr_f_value & 5
            if "AMR speech in 3G network" in setting and st_key in setting:
                self.comment("[group]%s --> [feature]%s -->[setting]%s" % (group,feature,setting))
                f_v = f_ss[group][feature][setting][0]["value"]
                if f_v:
                    amr_f_value = amr_f_value | 4
                else :
                    amr_f_value = amr_f_value & 3
        if "GSM A5" in st_key:
            p_v = self.sx('(send (send config-manager get-setting "%s") ->string)' % a5_ref_value)
            f_v = a5_bits
            r = cmp(str(a5_bits), str(p_v))
        if "GPRS GEA" in st_key:
            p_v = self.sx('(send (send config-manager get-setting "%s") ->string)' % gea_ref_value)
            f_v = gea_bits
            r = cmp(str(gea_bits), str(p_v))
        if "AMR speech" in st_key:
            p_v = self.sx('(send (send config-manager get-setting "%s") ->string)' % amr_ref_value)
            f_v = amr_f_value
            r = cmp(str(amr_f_value), str(p_v))             
        status = "pass" if r == 0 else "fail"
        if status == "fail":
            self.fail("expect[%s], actual[%s]" % (f_v, p_v)) 
            
    def _emergency_settings(self,group,feature,st_key): 
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        f_ref = os.path.join(os.path.dirname(__file__), "ref.json").replace("\\", "/")
        f_ref_ss = self.settingutil.converter(f_ref)        
        for setting in f_ss[group][feature]:
            if st_key in setting:                        
                if len(f_ss[group][feature][setting])>0:
                    found_it = False
                    f_e_v = f_ss[group][feature][setting][0]["value"]
                    for st in f_ref_ss[group][feature]:
                        ref_value = f_ref_ss[group][feature][st][0]["ref"]
                        p_e_v = self.sx('(send (send config-manager get-setting "%s") ->string)' % ref_value)
                        if p_e_v == f_e_v:
                            found_it = True
                            continue
                    status = "pass" if found_it ==True else "fail"
                    self.comment("----[setting][%s]%s " % (status, setting))
                    if status == "fail":
                        self.fail("expect[%s], actual[%s]" % (f_e_v, "")) 
                                
class CallingNetworkSetting(uitestcase.UITestCase):
    subarea = "Calling and Contact"
    feature = "Calling Network settings"

    def testGSML2FillBitRandomization(self):
        '''
        @tcId GSM L2 Fill Bit Randomization
        '''
        group="Calling and Contact"
        feature="Calling Network settings"
        setting="GSM L2 Fill Bit Randomization"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testFDNGPRSControl(self):
        '''
        @tcId FDN GPRS Control
        '''
        group="Calling and Contact"
        feature="Calling Network settings"
        setting="FDN GPRS Control"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
        
    def testSourceforServiceProviderName(self):
        '''
        @tcId Source for Service Provider Name
        '''
        group="Calling and Contact"
        feature="Calling Network settings"
        setting="Source for Service Provider Name"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
    
    def testCheckforPhoneUpdates(self):
        '''
        @tcId Enable/disable check for phone updates
        '''
        group="Calling and Contact"
        feature="Calling Network settings"
        setting="Enable/disable check for phone updates"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)       
    
    def testFlexiblePLMNIndicatorSupport(self):
        '''
        @tcId Flexible PLMN indicator support
        '''
        group="Calling and Contact"
        feature="Calling Network settings"
        setting="Flexible PLMN indicator support"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testEnableOrDisableVOIP(self):
        '''
        @tcId Enable or Disable VOIP
        '''
        group="Calling and Contact"
        feature="Calling Network settings"
        setting="Enable or Disable VOIP"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
    
    def testCallBarringMenuVisibility(self):
        '''
        @tcId Call barring menu visibility
        '''
        group="Calling and Contact"
        feature="Calling Network settings"
        setting="Call barring menu visibility"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
    
    def test3GFastDormancySupport(self):
        '''
        @tcId 3G Fast Dormancy support
        '''
        group="Calling and Contact"
        feature="Calling Network settings"
        setting="3G Fast Dormancy support"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
    
    def testGPRSGEAAlgorithm(self):
        '''
        @tcId GPRS GEA algorithm
        '''
        group="Calling and Contact"
        feature="Calling Network settings"
        st_key="GPRS GEA"
        csc = CommonSettingCompare(self)
        csc._bitmask_settings_compare(group,feature,st_key)
    
    def testGSMA5(self):
        '''
        @tcId GSM A5 ciphering algorithm support
        '''
        group="Calling and Contact"
        feature="Calling Network settings"
        st_key="GSM A5"
        csc = CommonSettingCompare(self)
        csc._bitmask_settings_compare(group,feature,st_key)        
    
    def testWidebandAMRSpeech(self):
        '''
        @tcId Support for wide-band AMR speech in 2G/3G
        '''
        group="Calling and Contact"
        feature="Calling Network settings"  
        st_key="AMR speech"
        csc = CommonSettingCompare(self)
        csc._bitmask_settings_compare(group,feature,st_key)

class ContactSettings(uitestcase.UITestCase):
    subarea = "Calling and Contact"
    feature = "Contact Settings" 
    
    def testIntelligentDigitsInCLI(self):
        '''
        @tcId Intelligent digits in CLI matching
        '''
        group="Calling and Contact"
        feature="Contact Settings"
        setting="Intelligent digits in CLI matching"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting) 
    
    def testPhonebookADN(self):
        '''
        @tcId Phonebook ADN before PD CLI matching
        '''
        group="Calling and Contact"
        feature="Contact Settings"
        setting="Phonebook ADN before PD CLI matching"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
        
    def testSupportastarkey(self):
        '''
        @tcId Support a star key in number matching
        '''
        group="Calling and Contact"
        feature="Contact Settings"
        setting="Support a star key in number matching"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)         
    
    def testExactNumberMatching(self):
        '''
        @tcId Exact number matching
        '''
        group="Calling and Contact"
        feature="Contact Settings"
        setting="Exact number matching"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
    
    def testCommonPCNHandset(self):
        '''
        @tcId CPHS/CSP Common PCN Handset support
        '''
        group="Calling and Contact"
        feature="Contact Settings"
        setting="CPHS/CSP Common PCN Handset support"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)    
    
    def testSortContactsBy(self):
        '''
        @tcId Sort contacts by
        '''
        group="Calling and Contact"
        feature="Contact Settings"
        setting="Sort contacts by"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
    
    def testPhonebookSDNCLI(self):
        '''
        @tcId Phonebook SDN CLI matching
        '''
        group="Calling and Contact"
        feature="Contact Settings"
        setting="Phonebook SDN CLI matching"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)        
    
    def testPhonebookCalling(self):
        '''
        @tcId Phonebook Calling line Identification
        '''
        group="Calling and Contact"
        feature="Contact Settings"
        setting="Phonebook Calling line Identification"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

class EmergencyCalls(uitestcase.UITestCase):
    subarea = "Calling and Contact"
    feature = "Emergency Calls"
    
    def testOperatorEmergencyNumber(self):
        '''
        @tcId Country and Operator variant Emergency number
        '''
        group="Calling and Contact"
        feature="Emergency Calls"
        setting="Country and Operator variant Emergency number"    
        csc = CommonSettingCompare(self)
        csc._emergency_settings(group,feature,setting)

class VoiceMailboxSeting(uitestcase.UITestCase):
    subarea = "Calling and Contact"
    feature = "Voicemail box Settings"
    
    def testVoiceMailOverrideNumber(self):
        '''
        @tcId Voice mail override number
        '''
        group="Calling and Contact"
        feature="Voicemail box Settings"
        setting="Voice mail override number"    
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

class OhterCallSettings(uitestcase.UITestCase):
    subarea = "Calling and Contact"
    feature = "Other Call Settings"
    
    def testClearCodeSupport(self):
        '''
        @tcId Clear Code support
        '''
        group="Calling and Contact"
        feature="Other Call Settings"
        setting="Clear Code support"    
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
    
    def testTwoDigitDialing(self):
        '''
        @tcId Two Digit Dialing
        '''
        group="Calling and Contact"
        feature="Other Call Settings"
        setting="Two Digit Dialing"    
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)    
        
    def test2gRATinfo(self):
        '''
        @tcId 2g RAT info
        '''
        group="Calling and Contact"
        feature="Other Call Settings"
        setting="2g RAT info"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def test35gRATinfo(self):
        '''
        @tcId 3.5g RAT info
        '''
        group="Calling and Contact"
        feature="Other Call Settings"
        setting="3.5g RAT info"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting) 
    
    def testPDPContext(self):
        '''
        @tcId PDP context activation restriction enabled
        '''
        group="Calling and Contact"
        feature="Other Call Settings"
        setting="PDP context activation restriction enabled"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)  
    
    def testHSSCCHLessOperation(self):
        '''
        @tcId HS-SCCH less operation
        '''
        group="Calling and Contact"
        feature="Other Call Settings"
        setting="HS-SCCH less operation"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
    
    def testEnhancedFractionalDPCH(self):
        '''
        @tcId Enhanced fractional DPCH
        '''
        group="Calling and Contact"
        feature="Other Call Settings"
        setting="Enhanced fractional DPCH"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting) 
    
    def testEnableContinuousPacket(self):
        '''
        @tcId Enable Continuous Packet Connectivity features
        '''
        group="Calling and Contact"
        feature="Other Call Settings"
        setting="Enable Continuous Packet Connectivity features"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)   
    
    def testVamosLevelSupport(self):
        '''
        @tcId Vamos level support
        '''
        group="Calling and Contact"
        feature="Other Call Settings"
        setting="Vamos level support"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)    