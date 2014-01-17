import core
from core import uitestcase
import json, os.path
from cs_util import *

class MediaFilesTest(uitestcase.UITestCase):
    subarea = "Application and Content"
    feature = "Preloaded Media & UI"
    # def setUp(self):
    #     """ Set up function. """
    #     uitestcase.UITestCase.setUp(self)
    #     self.settingutil = SettingUtil(self)

    # def tearDown(self):
    #     """ Tear down function. """
    #     uitestcase.UITestCase.tearDown(self)
    # f = os.path.join(os.path.dirname(__file__), "all.json").replace("\\", "/")

    def test_preloaded_media_files(self):
        """preloaded media
        @tcId preloaded media, Profile Settings
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
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
                        if len(f_ss[group][feature][setting]) != 2:
                            self.comment("[Skip] %s will be covered in config.db check..." % setting)
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
                            if f["System File"] == True:
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
                            if f["System File"] == False:
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

    def test_mmc_preloaded_files(self):
        """preloaded memory card media files & app
        @tcId memory card media & app file check
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        below_f = os.path.join(os.path.dirname(__file__), "below_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        below_f_ss = self.settingutil.converter(below_f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
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
                    # files check
                    # for sequence in setting:
                    if "Pre-loaded Music clips to Memory Card" == setting:
                        ftype = "music"
                        music_files=[]
                        for f in f_ss[group][feature][setting]:
                            music_files.append(f["Pre-loaded music clips file"])
                        results = self.settingutil.check_mmc_content(ftype, music_files)
                        for r in results:
                            self.comment("----[setting][fail] mmc preloaded music file: %s" % r)
                            count += 1
                            failed_tc.append((setting, r, 'NA'))

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

                    elif "Pre-loaded lockscreen images to Memory Card" == setting:
                        ftype = "wallpaper"
                        img_files=[]
                        for f in f_ss[group][feature][setting]:
                            img_files.append(f["Pre-loaded images file for lockscreen"])
                        results = self.settingutil.check_mmc_content(ftype, img_files)
                        for r in results:
                            self.comment("----[setting][fail] mmc preloaded image file: %s" % r)
                            count += 1
                            failed_tc.append((setting, r, 'NA'))

                    elif "Pre-loaded Video clips to Memory Card" == setting:
                        ftype = "videos"
                        video_files=[]
                        for f in f_ss[group][feature][setting]:
                            video_files.append(f["Pre-loaded video clips file"])
                        results = self.settingutil.check_mmc_content(ftype, video_files)
                        for r in results:
                            self.comment("----[setting][fail] mmc preloaded video file: %s" % r)
                            count += 1
                            failed_tc.append((setting, r, 'NA'))

                    elif "Pre-loaded Tone clips to Memory Card" == setting:
                        ftype = "tones"
                        tone_files=[]
                        for f in f_ss[group][feature][setting]:
                            tone_files.append(f["Pre-loaded Tone file"])
                        results = self.settingutil.check_mmc_content(ftype, tone_files)
                        for r in results:
                            self.comment("----[setting][fail] mmc preloaded tone file: %s" % r)
                            count += 1
                            failed_tc.append((setting, r, 'NA'))

                    elif "Preloaded Applications on Memory Card" == setting:
                        ftype = "applications"
                        java_files=[]
                        for f in f_ss[group][feature][setting]:
                            java_files.append(f["Jar File"])
                        results = self.settingutil.check_mmc_content(ftype, java_files)
                        for r in results:
                            self.comment("----[setting][fail] mmc preloaded app java file: %s" % r)
                            count += 1
                            failed_tc.append((setting, r, 'NA'))

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

class ApplicationsTest(uitestcase.UITestCase):
    subarea = "Application and Content"
    feature = "Preloaded Applications"
    # def setUp(self):
    #     """ Set up function. """
    #     uitestcase.UITestCase.setUp(self)
    #     self.settingutil = SettingUtil(self)

    # def tearDown(self):
    #     """ Tear down function. """
    #     uitestcase.UITestCase.tearDown(self)
    # f = os.path.join(os.path.dirname(__file__), "all.json").replace("\\", "/")

    def test_app_list(self):
        """Preloaded Applications
        @tcId Preloaded Applications, Bookmarks, Customer Folder, Homepage URL
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
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
                    elif "Home Page URL for Application List" in setting:
                        for f in f_ss[group][feature][setting]:
                            r = self.settingutil.check_bmk(f["Name in Application List Editor"], inapplist=f["Show in application list"])
                            status = "pass" if r == 0 else "fail"
                            self.comment("----[setting][%s]Preloaded homepage url: %s " % (status, f["Name in Application List Editor"]))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, f["Name in Application List Editor"], 'NA'))


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


class ConfigSettingsTest(uitestcase.UITestCase):
    subarea = "Config.db"
    feature = "All features"
    # def setUp(self):
    #     """ Set up function. """
    #     uitestcase.UITestCase.setUp(self)
    #     self.settingutil = SettingUtil(self)

    # def tearDown(self):
    #     """ Tear down function. """
    #     uitestcase.UITestCase.tearDown(self)
    # f = os.path.join(os.path.dirname(__file__), "all.json").replace("\\", "/")

    def test_settings_compare(self):
        """config.db settings check
        @tcId config.db settings check
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        f_ref = os.path.join(os.path.dirname(__file__), "ref.json").replace("\\", "/")
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
                # --------------- skip feature check ---------------------------
                if "Customer certificates" in feature or "Memory Card Content" in feature \
                   or "Browser Settings" in feature or "Emergency Calls" in feature:
                    continue
                for setting in f_ss[group][feature]:
                    # --------------- skip setting check ---------------------------
                    # run in func and UI test case
                    if "Operator message" in setting:
                        self.comment("----[setting][skip] %s" % setting)
                        continue
                    # handle if new setting is added, but tc not developed - Manual checking cases
                    if not f_ref_ss[group].has_key(feature) or not f_ref_ss[group][feature].has_key(setting):
                        manual_tc.append((setting, f_ss[group][feature][setting][0]))
                        m_count += 1
                        self.comment("----[setting][skip] %s" % setting)
                        continue
                    # move to the bitmask setting tesc case
                    if "GSM A5" in setting or "GPRS GEA" in setting or "wide-band AMR speech" in setting:
                        self.comment("----[setting][skip] %s" % setting)
                        continue
                    # ---------------------------------------------------
                    sequence = f_ref_ss[group][feature][setting][0]
                    if sequence.has_key("ref"):
                        ref_value = sequence["ref"]
                        p_v = self.sx('(send (send config-manager get-setting "%s") ->string)' % ref_value)
                    f = f_ss[group][feature][setting][0]
                    if f.has_key("value"):
                        f_v = f["value"]
                        # handle profile settings which is different from others
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
                        self.comment("----[setting][%s]%s " % (status, setting))
                        if status == "fail":
                            count += 1
                            failed_tc.append((setting, f_v, p_v))

        self.comment("---------------- settings failed: %d -------------------" % count)
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

    def test_bitmask_settings_compare(self):
        """config.db bitmask settings check
        @tcId Calling Network settings: GEA, A5, AMR_speech algorithm support
        """
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        below_f = os.path.join(os.path.dirname(__file__), "below_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)
        below_f_ss = self.settingutil.converter(below_f)
        # f_ss = json.loads(xml2json(source))
        # read configuration items mapping file, for reference
        f_ref = os.path.join(os.path.dirname(__file__), "ref.json").replace("\\", "/")
        f_ref_ss = self.settingutil.converter(f_ref)

        count = 0
        failed_tc = []
        m_count = 0
        manual_tc = []
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
        for group in f_ss:
            for feature in f_ss[group]:
                for setting in f_ss[group][feature]:
                    if "GSM A5" in setting:
                        self.comment("[group]%s --> [feature]%s -->[setting]%s" % (group,feature,setting))
                        for f in f_ss[group][feature][setting]:
                            if f.has_key("value"):
                                f_v = f["value"]
                                a5_bits = self.settingutil.bhdconvert(setting, f_v, a5_bits)
                                continue
                    if "GPRS GEA" in setting:
                        self.comment("[group]%s --> [feature]%s -->[setting]%s" % (group,feature,setting))
                        for f in f_ss[group][feature][setting]:
                            if f.has_key("value"):
                                f_v = f["value"]
                                gea_bits = self.settingutil.bhdconvert(setting, f_v, gea_bits)
                                continue
                    if "AMR speech in 2G network" in setting:
                        self.comment("[group]%s --> [feature]%s -->[setting]%s" % (group,feature,setting))
                        f_v = f_ss[group][feature][setting][0]["value"]
                        if f_v:
                            amr_f_value = amr_f_value | 2
                    if "AMR speech in 3G network" in setting:
                        self.comment("[group]%s --> [feature]%s -->[setting]%s" % (group,feature,setting))
                        f_v = f_ss[group][feature][setting][0]["value"]
                        if f_v:
                            amr_f_value = amr_f_value | 4
        a5_p_v = self.sx('(send (send config-manager get-setting "%s") ->string)' % a5_ref_value)
        gea_p_v = self.sx('(send (send config-manager get-setting "%s") ->string)' % gea_ref_value)
        amr_p_v = self.sx('(send (send config-manager get-setting "%s") ->string)' % amr_ref_value)
        r_a5 = cmp(str(a5_bits), str(a5_p_v))
        r_gea = cmp(str(gea_bits), str(gea_p_v))
        r_amr = cmp(str(amr_f_value), str(amr_p_v))
                    # failed using util func
                    # r = self.settingutil.compare_settings(f_v, p_v)
                    # p_v = self.settingutil.get_phone_setting(setting)
        #comp a5
        status = "pass" if r_a5 == 0 else "fail"
        self.comment("----[setting][%s]%s " % (status, a5_setting))
        if status == "fail":
            count += 1
            failed_tc.append((a5_setting, a5_bits, a5_p_v))
        #comp gea
        status = "pass" if r_gea == 0 else "fail"
        self.comment("----[setting][%s]%s " % (status, gea_setting))
        if status == "fail":
            count += 1
            failed_tc.append((gea_setting, gea_bits, gea_p_v))
        #comp amr
        status = "pass" if r_amr == 0 else "fail"
        self.comment("----[setting][%s]%s " % (status, amr_setting))
        if status == "fail":
            count += 1
            failed_tc.append((amr_setting, amr_f_value, amr_p_v))	

        self.comment("---------------- settings failed: %d -------------------" % count)
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
