import core
from core import uitestcase

import json, os.path
from cs_util import *

class SettingTest(uitestcase.UITestCase):
    subarea = "Phone Setting"
    feature = "config.db settings"
    # def setUp(self):
    #     """ Set up function. """
    #     uitestcase.UITestCase.setUp(self)
    #     self.settingutil = SettingUtil(self)

    # def tearDown(self):
    #     """ Tear down function. """
    #     uitestcase.UITestCase.tearDown(self)

    def test_compare_settings(self):
        """Method for checking phone settings
        @tcId compare settings: config.db VS static settings file
        """
        # 
        # store settings file to some location: netdrive or local
        # convert different files to py dict and return it
        # (with connected phone)	get config.db and read the settings(can I export db and then disconnect phone?)
        # (without connected phone) get config.db and read the settings using sql (need manual export config.db)
        # compare the values between settingfile(py dict) and config.db values, return flag to tag the result.
        
        f = r"C:\W-AQUA\granite\granite\test_scripts\c_variant\debug.json"

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

                    elif "profile" in setting:
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

                    elif "bluetooth" in setting:
                        self.settingutil.check_phone_bluetooth()

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
                        f_v = f_ss[group][feature][setting]["value"]
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
                        # status = "pass" if r == 0 else "fail"
                        # self.comment("------[setting][%s]%s " % (status, setting))
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
