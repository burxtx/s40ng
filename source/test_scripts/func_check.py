import core
from core import uitestcase

import json, os.path
from cs_util import *

class UiTest(uitestcase.UITestCase):
    subarea = "Customization"
    feature = "Phone UI"
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
                    r1, r2 = self.settingutil.check_phone_bluetooth_ui(
                        visible=s[0]["value"], device_name=s[1]["value"])
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
                    r1, r2, r3 = self.settingutil.check_phone_time_date_ui(
                        dateformat=s[1]["value"], timeformat24h=s[0]["value"], nitz_update=s[2]["value"])
                    status = "pass" if r1 and r2 and r3 else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))

    def test_phone_network_ui(self):
        """Check phone network UI settings
        @tcId phone update ui
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
                if "calling_network_settings" in feature:
                    for setting in f_ss[group][feature]:
                        if "update-manager" in setting:
                            f_s = f_ss[group][feature][setting]
                            s.append(f_s)
                    r = self.settingutil.check_phone_network_ui(auto_update=s[0]["value"])
                    status = "pass" if r else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))

    def test_phone_sms_ui(self):
        """Check phone sms UI settings
        @tcId phone sms ui
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
                if "sms_settings" in feature:
                    for setting in f_ss[group][feature]:
                        f_s = f_ss[group][feature][setting]
                        s.append(f_s)
                    r1, r2 = self.settingutil.check_phone_sms_ui(
                        delivery_report=s[1]["value"], num_lock=s[2]["value"])
                    status = "pass" if r1 and r2 else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))

    def test_phone_mms_ui(self):
        """Check phone mms UI settings
        @tcId phone mms ui
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
                if "mms_settings" in feature:
                    for setting in f_ss[group][feature]:
                        f_s = f_ss[group][feature][setting]
                        s.append(f_s)
                    r1, r2, r3 = self.settingutil.check_phone_mms_ui(
                        delivery_report=s[1]["value"], allow_adverts=s[3]["value"], reception=s[2]["value"])
                    status = "pass" if r1 and r2 and r3 else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))

    def test_phone_voice_mail_ui(self):
        """Check phone voice mailbox number
        @tcId phone voice mailbox number ui
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
                if "voicemail_box_settings" in feature:
                    for setting in f_ss[group][feature]:
                        f_s = f_ss[group][feature][setting]
                        s.append(f_s)
                    r = self.settingutil.check_phone_voicemail_ui(voicemail_num=s[0]["value"])
                    status = "pass" if r else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))