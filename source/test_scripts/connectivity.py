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
            if f_v == True or f_v == False:
                f_v = str(f_v).lower()
            # prevent if phone value is upper started
            if p_v == True or p_v == False:
                p_v = str(p_v).lower()
            r = cmp(str(f_v), str(p_v))
            status = "pass" if r == 0 else "fail"
            if status == "fail":
                self.fail("expect[%s], actual[%s]" % (f_v, p_v))

class BluetoothTest(uitestcase.UITestCase):
    subarea = "Connectivity"
    feature = "Bluetooth"

    def testBluetoothDeviceName(self):
        '''
        @tcId device name check
        '''
        group="Connectivity"
        feature="Bluetooth settings"
        setting="Device name"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testBluetoothVisibility(self):
        '''
        @tcId visibility check
        '''
        group="Connectivity"
        feature="Bluetooth settings"
        setting="Bluetooth visibility"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

class MobileDataTest(uitestcase.UITestCase):
    subarea = "Connectivity"
    feature = "Mobile Data Settings"

    def testMobileDataUsageWhenNoWifi(self):
        '''
        @tcId Mobile Data Usage When no Wi-Fi available check
        '''
        group="Connectivity"
        feature="Mobile Data Settings"
        setting="Mobile Data Usage When no Wi-Fi available"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testRoamingMobileDataUsage(self):
        '''
        @tcId Roaming mobile data usage check
        '''
        group="Connectivity"
        feature="Mobile Data Settings"
        setting="Roaming mobile data usage"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testHideDataConnectionMode(self):
        '''
        @tcId Enable to hide data connection mode menu settings with When Needed
        '''
        group="Connectivity"
        feature="Mobile Data Settings"
        setting="Enable to hide data connection mode menu settings with When Needed."
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
