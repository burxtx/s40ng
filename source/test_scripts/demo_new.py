import core
from core import uitestcase
import json, os.path
from cs_util import *

class SettingTest(uitestcase.UITestCase):
    subarea = "Customization"
    feature = "Nuage settings"
    # def setUp(self):
    #     """ Set up function. """
    #     uitestcase.UITestCase.setUp(self)
    #     self.settingutil = SettingUtil(self)

    # def tearDown(self):
    #     """ Tear down function. """
    #     uitestcase.UITestCase.tearDown(self)
    # f = os.path.join(os.path.dirname(__file__), "all.json").replace("\\", "/")

    def test_media_files(self):
        """preloaded media files check
        @tcId preloaded media files check
        """
        f = os.path.join(os.path.dirname(__file__), "auto_test_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        count = 0
        failed_tc = []
        m_count = 0
        manual_tc = []
        # py dict from json file
        for group in f_ss:
            self.comment("[group] %s" % group)
            for feature in f_ss[group]:
                self.comment("--[feature] %s" % feature)
                if "Profile Settings" in feature:
                    for setting in f_ss[group][feature]:
                        profile_tone_files=[]
                        if len(f_ss[group][feature][setting]) > 2:
                            self.comment("[Oops] Something went wrong...")
                            continue
                        f = f_ss[group][feature][setting][0]
                        # f_path = f_ss[group][feature][setting][1]
                        # profile_tone_files.append({"file": f_name["value"], "type": setting})
                        # for f in f_ss[group][feature][setting]:
                        #     profile_tone_files.append({"file": f["value"], "type": f["type"]})
                        r = self.settingutil.check_phone_profile_tone(f["value"], setting)
                        status = "pass" if r == 0 else "fail"
                        self.comment("----[setting][%s]profile: %s " % (status, f["value"]))
                        if status == "fail":
                            count += 1
                            failed_tc.append((setting, f["value"], 'NA'))

                        # for f in profile_tone_files:
                        #     r = self.settingutil.check_phone_profile_tone(f["file"])
                        #     # self.settingutil.addlog(setting, r)
                        #     status = "pass" if r == 0 else "fail"
                        #     self.comment("---[setting][%s]profile: %s " % (status, f))
                        #     if status == "fail":
                        #         count += 1
                        #         failed_tc.append((setting, f["file"], 'NA'))
                for setting in f_ss[group][feature]:
                    # files check
                    # for sequence in setting:
                    if "Music Files" in setting:
                        music_files=[]
                        for f in f_ss[group][feature][setting]:
                            music_files.append(f["Music file"])
                        for f in music_files:
                            r = self.settingutil.get_phone_music(f)
                            status = "pass" if r == 0 else "fail"
                            self.comment("----[setting][%s]music: %s " % (status, f))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, f, 'NA'))

                    # elif "profile files" in setting:
                    #     profile_tone_files=[]
                    #     for f in f_ss[group][feature][setting]:
                    #         profile_tone_files.append({"file": f["value"], "type": f["type"]})
                    #     for f in profile_tone_files:
                    #         r = self.settingutil.check_phone_profile_tone(f["file"])
                    #         # self.settingutil.addlog(setting, r)
                    #         status = "pass" if r == 0 else "fail"
                    #         self.comment("---[setting][%s]profile: %s " % (status, f))
                    #         if status == "fail":
                    #             count += 1
                    #             failed_tc.append((setting, f["file"], 'NA'))

                    elif "Tone Files" in setting:
                        tone_files_sys=[]
                        tone_files_non_sys=[]
                        for f in f_ss[group][feature][setting]:
                            if f["System File"] == "true":
                                tone_files_sys.append({"file": f["Tone file"], "type": f["Tone Type"]})
                            else:
                                tone_files_non_sys.append(f["Tone file"])
                        for sf in tone_files_sys:
                            ff = sf["file"]
                            ft = sf["type"]
                            r = self.settingutil.get_phone_tone_sys(ff, ft)
                            status = "pass" if r == 0 else "fail"
                            self.comment("----[setting][%s]sys tone: %s " % (status, ff))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, ff, 'NA'))
                        for nsf in tone_files_non_sys:
                            r = self.settingutil.get_phone_tone_non_sys(nsf)
                            status = "pass" if r == 0 else "fail"
                            self.comment("----[setting][%s]non sys tone: %s " % (status, nsf))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, nsf, 'NA'))

                    elif "Video Files" in setting:
                        video_files=[]
                        for f in f_ss[group][feature][setting]:
                            video_files.append(f["Video file"])
                        for f in video_files:
                            r = self.settingutil.get_phone_video(f)
                            status = "pass" if r == 0 else "fail"
                            self.comment("----[setting][%s]video: %s " % (status, f))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, f, 'NA'))

                    elif "Graphic Files" in setting:
                        graphic_files_non_sys=[]
                        graphic_files_sys=[]
                        for f in f_ss[group][feature][setting]:
                            if f["System File"] == "false":
                                graphic_files_non_sys.append(f["Graphic file"])
                            else:
                                graphic_files_sys.append(f["Graphic file"])
                        for nsf in graphic_files_non_sys:
                            r = self.settingutil.get_phone_graphic_non_sys(nsf)
                            status = "pass" if r == 0 else "fail"
                            self.comment("----[setting][%s]non sys graphic: %s " % (status, nsf))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, nsf, 'NA'))
                        for sf in graphic_files_sys:
                            m_count += 1
                            self.comment("----[setting]sys graphic, please manually check, %s" % sf)
                            manual_tc.append((setting, sf))

        self.comment("---------------- media files failed: %d -------------------" % count)
        if len(failed_tc) != count:
            self.comment("[CRITICAL] you should not see this, pls contact developer.")
        if len(failed_tc):
            for i, tc in enumerate(failed_tc):
                self.comment("%d. %s: expect[%s] actual[%s]" % (i+1,tc[0],tc[1],tc[2]))

        self.comment("---------------- media files manual: %d -------------------" % m_count)
        if len(manual_tc) != m_count:
            self.comment("[CRITICAL] you should not see this, pls contact developer.")
        if len(manual_tc):
            for i, tc in enumerate(manual_tc):
                self.comment("%d. %s. %s" % (i+1,tc[0],tc[1]))
        if count > 0:
            self.fail("[Result] Check media files failed")

    def test_app_list(self):
        """Preloaded apps check
        @tcId Preloaded apps check
        """
        f = os.path.join(os.path.dirname(__file__), "auto_test_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        count = 0
        failed_tc = []
        m_count = 0
        manual_tc = []
        # py dict from json file
        for group in f_ss:
            self.comment("[group] %s" % group)
            for feature in f_ss[group]:
                self.comment("--[feature] %s" % feature)
                for setting in f_ss[group][feature]:
                    # if "midlet files" in setting:
                    if "Midlet Files" in setting:
                        for f in f_ss[group][feature][setting]:
                            r = self.settingutil.check_phone_app(f["Midlet name"])
                            status = "pass" if r == 0 else "fail"
                            self.comment("----[setting][%s]Preloaded midlet: %s " % (status, f["Midlet name"]))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, f["Midlet name"], 'NA'))
                    elif "Midlet removal" in setting:
                        for f in f_ss[group][feature][setting]:
                            r = self.settingutil.check_phone_app(f["Midlet name"], remove=True)
                            status = "pass" if r == 0 else "fail"
                            self.comment("----[setting][%s]Removed midlet: %s " % (status, f["Midlet name"]))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, f["Midlet name"], 'NA'))
                    elif "Bookmark" in setting:
                        for f in f_ss[group][feature][setting]:
                            r = self.settingutil.check_bmk(f["Name"], inbrowser=f["Show in browser"], inapplist=f["Show in application list"])
                            status = "pass" if r == 0 else "fail"
                            self.comment("----[setting][%s]Preloaded bookmark: %s " % (status, f["Name"]))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, f["Name"], 'NA'))


        self.comment("---------------- application list check failed: %d -------------------" % count)
        if len(failed_tc) != count:
            self.comment("[CRITICAL] you should not see this, pls contact developer.")
        if len(failed_tc):
            for i, tc in enumerate(failed_tc):
                self.comment("%d. %s: expect[%s] actual[%s]" % (i+1,tc[0],tc[1],tc[2]))

        self.comment("---------------- application list check manual: %d -------------------" % m_count)
        if len(manual_tc) != m_count:
            self.comment("[CRITICAL] you should not see this, pls contact developer.")
        if len(manual_tc):
            for i, tc in enumerate(manual_tc):
                self.comment("%d. %s. %s" % (i+1,tc[0],tc[1]))
        if count > 0:
            self.fail("[Result] Check applications failed")

    def test_settings_compare(self):
        """config.db settings check
        @tcId config.db settings check
        """        
        f = os.path.join(os.path.dirname(__file__), "auto_test_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        f_ref = os.path.join(os.path.dirname(__file__), "ref.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ref_ss = self.settingutil.converter(f_ref)

        count = 0
        failed_tc = []
        m_count = 0
        manual_tc = []
        # py dict from json file
        for group in f_ss:
            self.comment("[group] %s" % group)
            for feature in f_ss[group]:
                self.comment("--[feature] %s" % feature)
                for setting in f_ss[group][feature]:
                    # if len(f_ref_ss[group][feature][setting]) == 1:
                    sequence = f_ref_ss[group][feature][setting][0]
                    if sequence.has_key("ref"):
                        value = sequence["ref"]
                        p_v = self.sx('(send (send config-manager get-setting "%s") ->string)' % value)
                        # this setting value range is 0 and 2
                        if value == "./platform/INFO_PP_CODEC_ORDER2" and p_v == "2":
                            p_v = "true"

                    for f in f_ss[group][feature][setting]:
                        if sequence.has_key("value"):
                            f_v = f["value"]
                            # handle profile settings which is different from others
                            if "Profile Settings" in feature or "Graphic UI Settings" in feature:
                                f_v = "file://"+f_ss[group][feature][setting][1]["value"]+f_ss[group][feature][setting][0]["value"]
                            # if f_v == "true" or f_v == "false":
                            #     f_v == bool(f_v)
                            if f_v == True or f_v == False:
                                f_v = str(f_v).lower()
                            r = cmp(str(f_v), str(p_v))
                    # failed using util func
                    # r = self.settingutil.compare_settings(f_v, p_v)
                    # p_v = self.settingutil.get_phone_setting(setting)
                            status = "pass" if r == 0 else "fail"
                            self.comment("----[setting][%s]%s " % (status, setting))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, f_v, p_v))


        self.comment("---------------- settings check failed: %d -------------------" % count)
        if len(failed_tc) != count:
            self.comment("[CRITICAL] you should not see this, pls contact developer.")
        if len(failed_tc):
            for i, tc in enumerate(failed_tc):
                self.comment("%d. %s: expect[%s] actual[%s]" % (i+1,tc[0],tc[1],tc[2]))

        self.comment("---------------- settings check manual: %d -------------------" % m_count)
        if len(manual_tc) != m_count:
            self.comment("[CRITICAL] you should not see this, pls contact developer.")
        if len(manual_tc):
            for i, tc in enumerate(manual_tc):
                self.comment("%d. %s. %s" % (i+1,tc[0],tc[1]))
        if count > 0:
            self.fail("[Result] Check config.db settings failed")
