import core
from core import uitestcase

import json, os.path
from cs_util import *

class UiTest(uitestcase.UITestCase):
    subarea = "Connectivity"
    feature = "Bluetooth"
    # def setUp(self):
    #     """ Set up function. """
    #     uitestcase.UITestCase.setUp(self)
    #     self.settingutil = SettingUtil(self)

    # def tearDown(self):
    #     """ Tear down function. """
    #     uitestcase.UITestCase.tearDown(self)
    # f = os.path.join(os.path.dirname(__file__), "all.json").replace("\\", "/")
    def test_bluetooth_ui(self):
        """Check phone bluetooth UI settings
        @tcId Bluetooth ui
        """

        f = os.path.join(os.path.dirname(__file__), "all.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        count = 0
        failed_tc = []
        m_count = 0
        manual_tc = []

        s = []
        # py dict from json file
        for group in f_ss:
            self.comment("[group] %s" % group)
            for feature in f_ss[group]:
                if "bluetooth" in feature:
                    for setting in f_ss[group][feature]:
                        f_s = f_ss[group][feature][setting]
                        s.append(f_s)
                    r1, r2 = self.settingutil.check_phone_bluetooth_ui(visible=s[0]["value"], device_name=s[1]["value"])
                    status = "pass" if r1 and r2 else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))

    def test_time_date_ui(self):
        """Check phone time and date UI settings
        @tcId Time and Date ui
        """

        f = os.path.join(os.path.dirname(__file__), "all.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        count = 0
        failed_tc = []
        m_count = 0
        manual_tc = []

        s = []
        # py dict from json file
        for group in f_ss:
            self.comment("[group] %s" % group)
            for feature in f_ss[group]:
                if "time_and_date" in feature:
                    for setting in f_ss[group][feature]:
                        f_s = f_ss[group][feature][setting]
                        s.append(f_s)
                    r1, r2, r3 = self.settingutil.check_phone_time_date_ui()
                    status = "pass" if r1 and r2 and r3 else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))