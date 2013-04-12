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
    def test_all(self):
        """Check phone config.db settings
        @tcId all
        """
        f = os.path.join(os.path.dirname(__file__), "all.json").replace("\\", "/")
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
                    # files check
                    if "music files" in setting:
                        music_files=[]
                        for f in f_ss[group][feature][setting]:
                            music_files.append(f["value"])
                        for f in music_files:
                            r = self.settingutil.get_phone_music(f)
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]music: %s " % (status, f))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, f, 'NA'))

                    elif "profile files" in setting:
                        profile_tone_files=[]
                        for f in f_ss[group][feature][setting]:
                            profile_tone_files.append({"file": f["value"], "type": f["type"]})
                        for f in profile_tone_files:
                            r = self.settingutil.check_phone_profile_tone(f["file"])
                            # self.settingutil.addlog(setting, r)
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]profile: %s " % (status, f))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, f["file"], 'NA'))

                    elif "tone files" in setting:
                        tone_files_sys=[]
                        tone_files_non_sys=[]
                        for f in f_ss[group][feature][setting]:
                            if f["sys"] == True:
                                tone_files_sys.append({"file": f["value"], "type": f["type"]})
                            else:
                                tone_files_non_sys.append(f["value"])
                        for sf in tone_files_sys:
                            ff = sf["file"]
                            ft = sf["type"]
                            r = self.settingutil.get_phone_tone_sys(ff, ft)
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]sys tone: %s " % (status, ff))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, ff, 'NA'))
                        for nsf in tone_files_non_sys:
                            r = self.settingutil.get_phone_tone_non_sys(nsf)
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]non sys tone: %s " % (status, nsf))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, nsf, 'NA'))

                    elif "video files" in setting:
                        video_files=[]
                        for f in f_ss[group][feature][setting]:
                            video_files.append(f["value"])
                        for f in video_files:
                            r = self.settingutil.get_phone_video(f)
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]video: %s " % (status, f))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, f, 'NA'))

                    elif "graphic files" in setting:
                        graphic_files_non_sys=[]
                        graphic_files_sys=[]
                        for f in f_ss[group][feature][setting]:
                            if f["sys"] == False:
                                graphic_files_non_sys.append(f["value"])
                            else:
                                graphic_files_sys.append(f["value"])
                        for nsf in graphic_files_non_sys:
                            r = self.settingutil.get_phone_graphic_non_sys(nsf)
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]non sys graphic: %s " % (status, nsf))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, nsf, 'NA'))
                        for sf in graphic_files_sys:
                            m_count += 1
                            self.comment("---[setting]sys graphic, please manually check, %s" % sf)
                            manual_tc.append((setting, sf))

                    elif "midlet files" in setting:
                        app_files = []
                        for f in f_ss[group][feature][setting]:
                            app_files.append({"file": f["value"], "type": f["type"]})
                        for a in app_files:
                            r = self.settingutil.check_phone_app(a["file"], a["type"])
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]preloaded application: %s " % (status, a))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, a, 'NA'))

                    # config.db settings check
                    else:
                        # return upper bool: True, False
                        f_v = f_ss[group][feature][setting]["value"]
                        # return lower bool: true false
                        p_v = self.sx('(send (send config-manager get-setting "%s") ->string)' % setting)
                        # failed using util func
                        # p_v = self.settingutil.get_phone_setting(setting)
                        
                        # convert True to true
                        if f_v == True or False:
                            f_v = str(f_v).lower()
                        r = cmp(str(f_v), str(p_v))
                        # generate status from "r"
                        # self.settingutil.addlog(setting, r)
                        status = "pass" if r == 0 else "fail"
                        self.comment("---[setting][%s]%s " % (status, setting))
                        if status == "fail":
                            count += 1
                            failed_tc.append((setting, f_v, p_v))

        self.comment("---------------- failed: %d -------------------" % count)
        if len(failed_tc) != count:
            self.comment("[CRITICAL] you should not see this, pls contact developer.")
        if len(failed_tc):
            for i, tc in enumerate(failed_tc):
                self.comment("%d. %s: expect[%s] actual[%s]" % (i+1,tc[0],tc[1],tc[2]))

        self.comment("---------------- manual: %d -------------------" % m_count)
        if len(manual_tc) != m_count:
            self.comment("[CRITICAL] you should not see this, pls contact developer.")
        if len(manual_tc):
            for i, tc in enumerate(manual_tc):
                self.comment("%d. %s. %s" % (i+1,tc[0],tc[1]))

    def test_media_files(self):
        """preloaded media files check
        @tcId preloaded media files check
        """
        f = os.path.join(os.path.dirname(__file__), "all.json").replace("\\", "/")
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
                    # files check
                    if "music files" in setting:
                        music_files=[]
                        for f in f_ss[group][feature][setting]:
                            music_files.append(f["value"])
                        for f in music_files:
                            r = self.settingutil.get_phone_music(f)
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]music: %s " % (status, f))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, f, 'NA'))

                    elif "profile files" in setting:
                        profile_tone_files=[]
                        for f in f_ss[group][feature][setting]:
                            profile_tone_files.append({"file": f["value"], "type": f["type"]})
                        for f in profile_tone_files:
                            r = self.settingutil.check_phone_profile_tone(f["file"])
                            # self.settingutil.addlog(setting, r)
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]profile: %s " % (status, f))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, f["file"], 'NA'))

                    elif "tone files" in setting:
                        tone_files_sys=[]
                        tone_files_non_sys=[]
                        for f in f_ss[group][feature][setting]:
                            if f["sys"] == True:
                                tone_files_sys.append({"file": f["value"], "type": f["type"]})
                            else:
                                tone_files_non_sys.append(f["value"])
                        for sf in tone_files_sys:
                            ff = sf["file"]
                            ft = sf["type"]
                            r = self.settingutil.get_phone_tone_sys(ff, ft)
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]sys tone: %s " % (status, ff))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, ff, 'NA'))
                        for nsf in tone_files_non_sys:
                            r = self.settingutil.get_phone_tone_non_sys(nsf)
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]non sys tone: %s " % (status, nsf))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, nsf, 'NA'))

                    elif "video files" in setting:
                        video_files=[]
                        for f in f_ss[group][feature][setting]:
                            video_files.append(f["value"])
                        for f in video_files:
                            r = self.settingutil.get_phone_video(f)
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]video: %s " % (status, f))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, f, 'NA'))

                    elif "graphic files" in setting:
                        graphic_files_non_sys=[]
                        graphic_files_sys=[]
                        for f in f_ss[group][feature][setting]:
                            if f["sys"] == False:
                                graphic_files_non_sys.append(f["value"])
                            else:
                                graphic_files_sys.append(f["value"])
                        for nsf in graphic_files_non_sys:
                            r = self.settingutil.get_phone_graphic_non_sys(nsf)
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]non sys graphic: %s " % (status, nsf))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, nsf, 'NA'))
                        for sf in graphic_files_sys:
                            m_count += 1
                            self.comment("---[setting]sys graphic, please manually check, %s" % sf)
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

    def test_app_list(self):
        """Preloaded apps check
        @tcId Preloaded apps check
        """
        f = os.path.join(os.path.dirname(__file__), "all.json").replace("\\", "/")
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
                    if "folder" in setting or "midlet files" in setting:
                        app_files = []
                        for f in f_ss[group][feature][setting]:
                            app_files.append({"file": f["value"], "type": f["type"], "icon": f["icon"]})
                        for a in app_files:
                            # r = self.settingutil.check_phone_app(a["file"], a["type"], a["icon"])
                            r = self.settingutil.check_phone_app(a["file"], a["type"])
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]preloaded application or folder: %s " % (status, a))
                            if status == "fail":
                                count += 1
                                failed_tc.append((setting, a, 'NA'))

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

    def test_settings_compare(self):
        """config.db settings check
        @tcId config.db settings check
        """        
        f = os.path.join(os.path.dirname(__file__), "all.json").replace("\\", "/")
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
                    p_v = self.sx('(send (send config-manager get-setting "%s") ->string)' % setting)
                    if not isinstance(f_ss[group][feature][setting], list):
                        f_v = f_ss[group][feature][setting]["value"]
                        if f_v == True or False:
                            f_v = str(f_v).lower()
                        r = cmp(str(f_v), str(p_v))
                        # r = self.settingutil.compare_settings(f_v, p_v)
                        status = "pass" if r == 0 else "fail"
                        self.comment("---[setting][%s]%s " % (status, setting))
                        # status = "pass" if r == 0 else "fail"
                        # self.comment("------[setting][%s]%s " % (status, setting))
                        if status == "fail":
                            count += 1
                            failed_tc.append((setting, f_v, p_v))
                    elif "files" in setting:
                        continue
                    else:
                        for f in f_ss[group][feature][setting]:
                            f_v = f["value"]
                            if f_v == True or False:
                                f_v = str(f_v).lower()
                            r = cmp(str(f_v), str(p_v))
                    # failed using util func
                    # r = self.settingutil.compare_settings(f_v, p_v)
                    # p_v = self.settingutil.get_phone_setting(setting)
                            status = "pass" if r == 0 else "fail"
                            self.comment("---[setting][%s]%s " % (status, setting))
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
