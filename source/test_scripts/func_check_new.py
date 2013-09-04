import core
from core import uitestcase

import json, os.path
from cs_util import *

class UiTest(uitestcase.UITestCase):
    subarea = "UI & Func"
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
        """Phone bluetooth UI settings
        @tcId Bluetooth ui
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        count = 0
        failed_tc = []
        m_count = 0
        manual_tc = []
        # default NDT value
        device_name = "Nokia 501"
        visible = True
        # py dict from json file
        for group in f_ss:
            self.comment("[group] %s" % group)
            for feature in f_ss[group]:
                if "Bluetooth" in feature:
                    for setting in f_ss[group][feature]:
                        if "Device name" in setting:
                            device_name = f_ss[group][feature][setting][0]["value"]
                        if "Bluetooth visibility" in setting:
                            visible = f_ss[group][feature][setting][0]["value"]
                    r1, r2 = self.settingutil.check_phone_bluetooth_ui(visible=visible, device_name=device_name)
                    status = "pass" if r1 and r2 else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))
                    if status == "fail":
                        self.fail("[Result] %s: Failed" % feature)

    def test_time_date_ui(self):
        """Phone time and date UI settings
        @tcId Time and Date ui
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        count = 0
        failed_tc = []
        m_count = 0
        manual_tc = []
        # default NDT value
        timeformat24h = True
        nitz_update = True
        dateformat = "DD-MM-YYYY"
        # py dict from json file
        for group in f_ss:
            self.comment("[group] %s" % group)
            for feature in f_ss[group]:
                if "Time and Date Settings" in feature:
                    for setting in f_ss[group][feature]:
                        if "NITZ" in setting:
                            nitz_update = f_ss[group][feature][setting][0]["value"]
                        if "Date" in setting:
                            dateformat = f_ss[group][feature][setting][0]["value"]
                        if "Time" in setting:
                            timeformat24h = f_ss[group][feature][setting][0]["value"]
                    r1, r2, r3 = self.settingutil.check_phone_time_date_ui(timeformat24h=timeformat24h, nitz_update=nitz_update, dateformat=dateformat)
                    status = "pass" if r1 and r2 and r3 else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))
                    if status == "fail":
                        self.fail("[Result] %s: Failed" % feature)

    #def test_phone_network_ui(self):
    #    """Phone network UI settings
    #    @tcId phone update ui
    #    """
    #    f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
    #    self.settingutil = SettingUtil(self)
    #    f_ss = self.settingutil.converter(f)
    #    # f_ss = json.loads(xml2json(source))
    #    # read configuration items mapping file, for reference
    #    count = 0
    #    failed_tc = []
    #    m_count = 0
    #    manual_tc = []
    #    # py dict from json file
    #    for group in f_ss:
    #        self.comment("[group] %s" % group)
    #        for feature in f_ss[group]:
    #            if "Calling Network settings" in feature:
    #                for setting in f_ss[group][feature]:
    #                    if "Enable/disable check for phone updates" in setting:
    #                        auto_update = f_ss[group][feature][setting][0]["value"]
    #                r = self.settingutil.check_phone_network_ui(auto_update=auto_update)
    #                status = "pass" if r else "fail"
    #                self.comment("--[feature][%s]%s" % (status, feature))
    #                if status == "fail":
    #                    self.fail("[Result] %s: Failed" % feature)

    def test_phone_sms_ui(self):
        """Phone sms UI settings
        @tcId phone sms ui
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        count = 0
        failed_tc = []
        m_count = 0
        manual_tc = []
        # Default NDT value
        delivery_report_ss = delivery_report1 = delivery_report2 = True
        num_lock = False
        dual_sim1 = dual_sim2 =False
        # py dict from json file
        for group in f_ss:
            self.comment("[group] %s" % group)
            for feature in f_ss[group]:
                if "SMS Settings" in feature:
                    for setting in f_ss[group][feature]:
                        if "SMS Delivery Reports" == setting:
                            delivery_report_ss = f_ss[group][feature][setting][0]["value"]

                        if "SMS Delivery Reports for SIM1" == setting:
                            delivery_report1 = f_ss[group][feature][setting][0]["value"]
                            dual_sim1 = True

                        if "SMS Delivery Reports for SIM2" == setting:
                            delivery_report2 = f_ss[group][feature][setting][0]["value"]
                            dual_sim2 = True

                        if "Message center number locked" in setting:
                            num_lock = f_ss[group][feature][setting][0]["value"]
                    r1, r2 = self.settingutil.check_phone_sms_ui(delivery_report=delivery_report_ss, num_lock=num_lock, sim1=dual_sim1, sim2=dual_sim2)
                    status = "pass" if r1 and r2 else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))
                    if status == "fail":
                        self.fail("[Result] %s: Failed" % feature)

    def test_phone_mms_ui(self):
        """Phone mms UI settings
        @tcId phone mms ui
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        count = 0
        failed_tc = []
        m_count = 0
        manual_tc = []
        # default NDT value
        delivery_report = True
        allow_adverts = True
        reception = 1
        # py dict from json file
        for group in f_ss:
            self.comment("[group] %s" % group)
            for feature in f_ss[group]:
                if "MMS Settings" in feature:
                    for setting in f_ss[group][feature]:
                        if "MMS Delivery Report" in setting:
                            delivery_report = f_ss[group][feature][setting][0]["value"]
                        if "Allow adverts" in setting:
                            allow_adverts = f_ss[group][feature][setting][0]["value"]
                        if "MMS Retrieval mode" in setting:
                            reception = int(f_ss[group][feature][setting][0]["value"])
                    r1, r2, r3 = self.settingutil.check_phone_mms_ui(delivery_report=delivery_report, allow_adverts=allow_adverts, reception=reception)
                    status = "pass" if r1 and r2 and r3 else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))
                    if status == "fail":
                        self.fail("[Result] %s: Failed" % feature)

    def test_phone_voice_mail_ui(self):
        """Phone voice mailbox number
        @tcId phone voice mailbox number ui
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        failed_tc = []
        m_count = 0
        manual_tc = []
        # NDT default value
        voicemail_num = ""
        # py dict from json file
        for group in f_ss:
            self.comment("[group] %s" % group)
            for feature in f_ss[group]:
                if "Voicemail box Settings" in feature:
                    for setting in f_ss[group][feature]:
                        if "Voice mail" in setting:
                            voicemail_num = f_ss[group][feature][setting][0]["value"]
                    r = self.settingutil.check_phone_voicemail_ui(voicemail_num=voicemail_num)
                    status = "pass" if r else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))
                    if status == "fail":
                        self.fail("[Result] %s: Failed" % feature)

    def test_phone_certificate(self):
        """Phone certificates
        @tcId phone certificates ui
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        failed_tc = []
        m_count = 0
        manual_tc = []
        # py dict from json file
        for group in f_ss:
            self.comment("[group] %s" % group)
            for feature in f_ss[group]:
                if "Customer certificates" in feature:
                    self.comment("--[feature] %s" % feature)
                    for setting in f_ss[group][feature]:
                        # if "Voice mail" in setting:
                        #     voicemail_num = f_ss[group][feature][setting][0]["value"]
                        r = self.settingutil.check_phone_certificate(setting)
                        status = "pass" if r else "fail"
                        self.comment("----[setting][%s]%s" % (status, setting))
                        if status == "fail":
                            self.fail("[Result] %s: Failed" % feature)

    def test_operator_messages(self):
        """
        @tcId operator messages
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        failed_tc = []
        m_count = 0
        manual_tc = []
        flag = False
        cb_channels = ""
        pb_channels = ""
        customer_account = ""
        # py dict from json file
        for group in f_ss:
            
            for feature in f_ss[group]:
                if "Other Messaging Settings" in feature :
                    self.comment("[group] %s -->[feature] %s" % (group,feature))
                    for setting in f_ss[group][feature]:
                        if "Cell Broadcast Reception" in setting:
                            flag = f_ss[group][feature][setting][0]["value"]
                        if "Cell Broadcast Channels configuration" in setting:
                            cb_channels = f_ss[group][feature][setting][0]["value"]
                        if "The identifiers of CMAS CB and their display priority." in setting:
                            pb_channels = f_ss[group][feature][setting][0]["value"]
                        if "Customer Account" in setting:
                            if f_ss[group][feature][setting][0].has_key('Account Name'):
                                customer_account = f_ss[group][feature][setting][0]["Account Name"]
                    r1, r2, r3= self.settingutil.check_operator_channel(flag, cb_channels, pb_channels)
                    r4 = self.settingutil.check_customer_account(customer_account)
                    status = "pass" if r1 and r2 and r3 and r4 else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))
                    if status == "fail":
                        self.fail("[Result] %s: Failed" % feature)
                        
    def test_nokia_improvement_program(self):
        """Nokia improvement program
        @tcId nokia improvement program ui
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        count = 0
        failed_tc = []
        m_count = 0
        manual_tc = []
        # py dict from json file
        for group in f_ss:            
            for feature in f_ss[group]:
                if "Device Activation Client" in feature:
                    self.comment("[group] %s -->[feature] %s" % (group,feature))
                    for setting in f_ss[group][feature]:
                        if "Nokia Improvement Program" in setting:
                            is_improvement = f_ss[group][feature][setting][0]["value"]
                    r = self.settingutil.check_nokia_improvement(is_improvement = is_improvement)
                    status = "pass" if r else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))
                    if status == "fail":
                        self.fail("[Result] %s: Failed" % feature)            
    
    def test_mobile_data_settings(self):
        """mobile_data_settings
        @tcId mobile data settings ui
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        count = 0
        failed_tc = []
        m_count = 0
        manual_tc = []
        flag2 = False
        flag2_v = False
        # py dict from json file
        for group in f_ss:            
            for feature in f_ss[group]:
                if "Mobile Data Settings" in feature:
                    self.comment("[group] %s -->[feature] %s" % (group,feature))
                    for setting in f_ss[group][feature]:
                        if "Mobile Data Usage When no Wi-Fi available" in setting:
                            flag = f_ss[group][feature][setting][0]["value"]                        
                        if "Mobile Data Connection Mode" in setting:
                            flag2 = True            
                            flag2_v = f_ss[group][feature][setting][0]["value"]
                    r , r2 = self.settingutil.check_mobile_data_settings(flag = flag, flag2 = flag2, flag2_v = flag2_v)
                    status = "pass" if r and r2 else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))
                    if status == "fail":
                        self.fail("[Result] %s: Failed" % feature)     
    
    def test_emergency_call(self):
        """emergency call
        @tcId emergency call func
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        count = 0
        failed_tc = []
        m_count = 0
        manual_tc = []
        # py dict from json file
        for group in f_ss:            
            for feature in f_ss[group]:
                if "Emergency Calls" in feature:
                    self.comment("[group] %s -->[feature] %s" % (group,feature))
                    for setting in f_ss[group][feature]:
                        number = f_ss[group][feature][setting][0]["value"]
                        r = self.settingutil.check_emergency_call(number)
                    status = "pass" if r else "fail"
                    self.comment("--[feature][%s]%s" % (status, feature))
                    if status == "fail":
                        self.fail("[Result] %s: Failed" % feature)
    # def test_main_menu(self):
    #     """Check main menu
    #     @tcId tile content
    #     """
    #     f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
    #     self.settingutil = SettingUtil(self)
    #     f_ss = self.settingutil.converter(f)
    #     # f_ss = json.loads(xml2json(source))
    #     # read configuration items mapping file, for reference
    #     failed_tc = []
    #     m_count = 0
    #     manual_tc = []
    #     # py dict from json file
    #     for group in f_ss:
    #         self.comment("[group] %s" % group)
    #         for feature in f_ss[group]:
    #             for setting in f_ss[group][feature]:
    #                 if "Tile content" in setting:
    #                     self.comment("--[feature] %s" % feature)
    #                     # if "Voice mail" in setting:
    #                     item = f_ss[group][feature][setting][0]["Content item"]
    #                     position = f_ss[group][feature][setting][0]["Position"]
    #                     r = self.settingutil.check_main_menu()
    #                     self.comment(r)
    #                     status = "pass" if r else "fail"
    #                     self.comment("----[setting][%s]%s" % (status, setting))
    #                     if status == "fail":
    #                         self.fail("[Result] %s: Failed" % feature)

