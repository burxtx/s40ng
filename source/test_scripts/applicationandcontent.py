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
                
class PreloadedMedia(uitestcase.UITestCase):
    subarea = "Application and Content"
    feature = "Preloaded Media"
    
    def testGraphicFiles(self):
        """preloaded media
        @tcId Graphic Files
        """
        group="Applications and Content"
        feature="Preloaded Media"
        setting="Graphic Files"  
        graphic_files_non_sys_path = 'c:\\sp\\usr\\_phone\\_my_pictures\\'
        graphic_files_sys_path = 'c:\\sp\\system_files\\images\\_system_wallpaper\\'
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)        
        try:
            f_ss[group][feature][setting][0]
        except:
            self.skip("[No customization value] at [%s]" % setting)
        for f in f_ss[group][feature][setting]:
            if f["System File"] == False:                
                r = self.file.fileExists(graphic_files_non_sys_path + f["Graphic file"])                
            else:
                r = self.file.fileExists(graphic_files_sys_path + f["Graphic file"])
            status = "pass" if r == True else "fail"
            self.comment("----[setting][%s]%s " % (status, setting))
            if status == "fail":
                self.fail("expect[%s], actual[%s]" % (f["Graphic file"], "N/A"))                  

    def testMusicFiles(self):
        """preloaded media
        @tcId Music Files
        """
        group="Applications and Content"
        feature="Preloaded Media"
        setting="Music Files"  
        music_files_non_sys_path = 'c:\\sp\\usr\\_phone\\_my_music\\'            
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)        
        try:
            f_ss[group][feature][setting][0]
        except:
            self.skip("[No customization value] at [%s]" % setting)
        for f in f_ss[group][feature][setting]:
            r = self.file.fileExists(music_files_non_sys_path + f["Music file"])                
            status = "pass" if r == True else "fail"
            self.comment("----[setting][%s]%s " % (status, setting))
            if status == "fail":
                self.fail("expect[%s], actual[%s]" % (f["Music file"], "N/A"))
    
    def testToneFiles(self):
        """preloaded media
        @tcId Tone Files
        """
        group="Applications and Content"
        feature="Preloaded Media"
        setting="Tone Files"  
        tone_files_non_sys_path = 'c:\\sp\\usr\\_phone\\_my_tones\\'
        tone_files_sys_path_message = 'c:\\sp\\system_files\\audio\\_system_messagetones\\'
        tone_files_sys_path_alert = 'c:\\sp\\system_files\\audio\\_system_alerttones\\'
        tone_files_sys_path_alarm = 'c:\\sp\\system_files\\audio\\_system_alarmtones\\'
        tone_files_sys_path_ring = 'c:\\sp\\system_files\\audio\\_system_ringtones\\'
        tone_files_sys_path_misc = 'c:\\sp\\system_files\\audio\\misc_tones\\'
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)        
        try:
            f_ss[group][feature][setting][0]
        except:
            self.skip("[No customization value] at [%s]" % setting)
        for f in f_ss[group][feature][setting]:
            if f["System File"] == False:                
                r = self.file.fileExists(tone_files_non_sys_path + f["Tone file"])                
            elif f["Tone Type"] == "AlarmTones":
                r = self.file.fileExists(tone_files_sys_path_alarm + f["Tone file"])
            elif f["Tone Type"] == "AlertTones":
                r = self.file.fileExists(tone_files_sys_path_alert + f["Tone file"])
            elif f["Tone Type"] == "MessageTones":
                r = self.file.fileExists(tone_files_sys_path_message+ f["Tone file"]) 
            elif f["Tone Type"] == "RingingTones":
                r = self.file.fileExists(tone_files_sys_path_ring + f["Tone file"])            
            status = "pass" if r == True else "fail"
            self.comment("----[setting][%s]%s " % (status, setting))
            if status == "fail":
                self.fail("expect[%s], actual[%s]" % (f["Tone file"], "N/A"))
                
    def testVideoFiles(self):
        """preloaded media
        @tcId Video Files
        """
        group="Applications and Content"
        feature="Preloaded Media"
        setting="Video Files"  
        video_files_non_sys_path = 'c:\\sp\\usr\\_phone\\_my_videos\\'            
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)        
        try:
            f_ss[group][feature][setting][0]
        except:
            self.skip("[No customization value] at [%s]" % setting)
        for f in f_ss[group][feature][setting]:
            r = self.file.fileExists(video_files_non_sys_path + f["Video file"])                
            status = "pass" if r == True else "fail"
            self.comment("----[setting][%s]%s " % (status, setting))
            if status == "fail":
                self.fail("expect[%s], actual[%s]" % (f["Video file"], "N/A"))


class CustomerFolders(uitestcase.UITestCase):
    subarea = "Applications and Content"
    feature = "Customer Folders for Application List and Browser"

    def CustomerFolderInApplicationList(self):
        '''
        @tcId Customer folder in Application list
        '''
        group="Applications and Content"
        feature="Customer Folders for Application List and Browser"
        setting="Customer folder in Application list"
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
        ref_value = sequence["ref"]
        p_v = self.sx('(send (send config-manager get-setting "%s") ->string)' % ref_value)       
        f_v = f["Folder name"]         
        r = cmp(str(f_v), str(p_v))
        status = "pass" if r == 0 else "fail"
        if status == "fail":
            self.fail("expect[%s], actual[%s]" % (f_v, p_v))
                
class PreloadedApplications(uitestcase.UITestCase):
    subarea = "Applications and Content"
    feature = "Preloaded Appications"
    
    def testMidletFiles(self):
        """preloaded media
        @tcId Midlet Files
        """
        group="Applications and Content"
        feature="Preloaded Applications"
        setting="Midlet Files"  
        midlet_file_path = 'c:\\sp\\system_files\\_system_applications\\'           
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)        
        try:
            f_ss[group][feature][setting][0]
        except:
            self.skip("[No customization value] at [%s]" % setting)
        for f in f_ss[group][feature][setting]:
            r = self.file.fileExists(midlet_file_path + f["Jar File"])
            status = "pass" if r == True else "fail"
            self.comment("----[setting][%s]%s " % (status, setting))
            if status == "fail":
                self.fail("expect[%s], actual[%s]" % (f["Jar File"], "N/A"))
            
            r = self.file.fileExists(midlet_file_path + f["Jad File"])
            status = "pass" if r == True else "fail"
            self.comment("----[setting][%s]%s " % (status, setting))
            if status == "fail":
                self.fail("expect[%s], actual[%s]" % (f["Jad File"], "N/A"))    

class BookmarksHomepageURL(uitestcase.UITestCase):
    subarea = "Application and Content"
    feature = "Bookmarks and Homepage URL"
    def testBookmarks(self):
        """preloaded media
        ####@tcId Midlet Files
        """
        group="Applications and Content"
        feature="Bookmarks and Homepage URL"
        setting="Bookmark"  
        midlet_file_path = 'c:\\sp\\system_files\\_system_applications\\'           
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)        
        try:
            f_ss[group][feature][setting][0]
        except:
            self.skip("[No customization value] at [%s]" % setting)
        for f in f_ss[group][feature][setting]:
            r = self.file.fileExists(midlet_file_path + f["Jar File"])
            status = "pass" if r == True else "fail"
            self.comment("----[setting][%s]%s " % (status, setting))
            if status == "fail":
                self.fail("expect[%s], actual[%s]" % (f["Jar File"], "N/A"))    

class BrowserSettings(uitestcase.UITestCase):
    subarea = "Applications and Content"
    feature = "Browser Settings"
    def testDefaultSearchProvider(self):
        """preloaded media
        @tcId Default Search Provider
        """
        group="Applications and Content"
        feature="Browser Settings"
        setting="Default Search Provider"      
        f = os.path.join(os.path.dirname(__file__), "focus_config.json").replace("\\", "/")
        self.settingutil = SettingUtil(self)
        f_ss = self.settingutil.converter(f)        
        try:
            f_ss[group][feature][setting][0]
        except:
            self.skip("[No customization value] at [%s]" % setting)
        if f_ss[group][feature][setting][0]["value"] == "1":            
            r = self.file.fileExists("c:\\sp\\java-config\\search.xml")
            status = "pass" if r == True else "fail"
            self.comment("----[setting][%s]%s " % (status, setting))
            if status == "fail":
                self.fail("expect <search.xml> found, actual not found")
        else:
            r = self.file.fileExists("c:\\sp\\java-config\\search.xml")
            status = "pass" if r == False else "fail"
            self.comment("----[setting][%s]%s " % (status, setting))
            if status == "fail":
                self.fail("expect <search.xml> not found, actual found")   
            