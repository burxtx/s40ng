import core
from core import uitestcase
import json, os.path
from cs_util import *

class CommonSettingCompare(uitestcase.UITestCase):

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
            if "Profile Settings" in feature or "Graphic UI Settings" in feature:
                if setting != 'Key Tone':
                    f_v = "file://"+f_ss[group][feature][setting][1]["value"]+f_ss[group][feature][setting][0]["value"] 
            if f_v == True or f_v == False:
                f_v = str(f_v).lower()
            # prevent if phone value is upper started
            if p_v == True or p_v == False:
                p_v = str(p_v).lower()
            r = cmp(str(f_v), str(p_v))
            status = "pass" if r == 0 else "fail"
            if status == "fail":
                self.fail("expect[%s], actual[%s]" % (f_v, p_v))

class TimeAndDateSettingsTest(uitestcase.UITestCase):
    subarea = "User Interface"
    feature = "Time and Date Settings"

    def testDateFormat(self):
        '''
        @tcId Date format check
        '''
        group="User Interface"
        feature="Time and Date Settings"
        setting="Date format"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testTimeFormat(self):
        '''
        @tcId Time Format check
        '''
        group="User Interface"
        feature="Time and Date Settings"
        setting="Time Format"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testNITZ(self):
        '''
        @tcId NITZ ( Network Identity and Time Zone)  check
        '''
        group="User Interface"
        feature="Time and Date Settings"
        setting="NITZ ( Network Identity and Time Zone) "
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
        
class LanguageSettingsTest(uitestcase.UITestCase):
    subarea = "User Interface"
    feature = "Language Settings"

    def testReadSuggestedDisplayLanguageFromSIM(self):
        '''
        @tcId Read Suggested display language from SIM check
        '''
        group="User Interface"
        feature="Language Settings"
        setting="Read Suggested display language from SIM"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testSuggestedDisplayLanguage(self):
        '''
        @tcId Suggested display language check
        '''
        group="User Interface"
        feature="Language Settings"
        setting="Suggested display language"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

class OtherUISettingsTest(uitestcase.UITestCase):
    subarea = "User Interface"
    feature = "Other UI Settings"

    def testScreenToubleTap(self):
        '''
        @tcId Screen double tap check
        '''
        group="User Interface"
        feature="Other UI Settings"
        setting="Screen double tap"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

class SIMSettingsTest(uitestcase.UITestCase):
    subarea = "User Interface"
    feature = "SIM Settings"

    def testSetUpEventListForZuHauseApplication(self):
        '''
        @tcId Set Up Event List for ZuHause Application check
        '''
        group="User Interface"
        feature="SIM Settings"
        setting="Set Up Event List for ZuHause Application"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testAccessingVivoDDDAndSTKMenuFunctionsFromSIMSlot2(self):
        '''
        @tcId Accessing Vivo DDD and STK Menu functions from SIM slot2
        '''
        group="User Interface"
        feature="SIM Settings"
        setting="Accessing Vivo DDD and STK Menu functions from SIM slot2"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

class ProfileSettingsTest(uitestcase.UITestCase):
    subarea = "User Interface"
    feature = "Profile Settings"

    def testSIM1Ringtone(self):
        '''
        @tcId SIM1 Ringtone check
        '''
        group="User Interface"
        feature="Profile Settings"
        setting="SIM1 Ringtone"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testSIM2Ringtone(self):
        '''
        @tcId SIM2 Ringtone check
        '''
        group="User Interface"
        feature="Profile Settings"
        setting="SIM2 Ringtone"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testMessageTone(self):
        '''
        @tcId Message Tone check
        '''
        group="User Interface"
        feature="Profile Settings"
        setting="Message Tone"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testEmailTone(self):
        '''
        @tcId Email Tone check
        '''
        group="User Interface"
        feature="Profile Settings"
        setting="Email Tone"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testAlarmTone(self):
        '''
        @tcId Alarm Tone check
        '''
        group="User Interface"
        feature="Profile Settings"
        setting="Alarm Tone"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testReminderTone(self):
        '''
        @tcId Reminder Tone check
        '''
        group="User Interface"
        feature="Profile Settings"
        setting="Reminder Tone"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testPushNotificationsTone(self):
        '''
        @tcId Push Notifications Tone check
        '''
        group="User Interface"
        feature="Profile Settings"
        setting="Push Notifications Tone"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testKeyTone(self):
        '''
        @tcId Key Tone check
        '''
        group="User Interface"
        feature="Profile Settings"
        setting="Key Tone"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

class GraphicUISettingsTest(uitestcase.UITestCase):
    subarea = "User Interface"
    feature = "Graphic UI Settings"

    def testSystemWallpaper(self):
        '''
        @tcId System wallpaper check
        '''
        group="User Interface"
        feature="Graphic UI Settings"
        setting="System wallpaper"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testOperatorStartupGraphic(self):
        '''
        @tcId Operator Startup Graphic check
        '''
        group="User Interface"
        feature="Graphic UI Settings"
        setting="Operator Startup Graphic"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)