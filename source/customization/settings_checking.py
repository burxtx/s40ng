import os
import core
from core import uitestcase
from utils.nodeutils import NodeUtils
import datetime
from interfaces.c_srv import srv_info

class testBed(uitestcase.UITestCase):

    subarea = "Test subarea"
    feature = "Test feature"

    def getSettings(self):
        """Method for checking phone settings

        @tcId do some settings checking against config-settings.sx file
        """

        import os
        import re
        location = r'C:\Mustang\Tools\Granite_1.1.2\test_scripts\customization'
        file = 'config-settings.sx'

        now = datetime.datetime.now()
        sec = int(now.second)
        min = int(now.minute)
        hour = int(now.hour)
        day = int(now.day)
        month = int(now.month)
        year = int(now.year)
        resultfile = "%d%02d%02d_%02d%02d_%02d_result_of_%s.txt" % (year, month, day, hour, min, sec, file)

        result_folder = os.path.abspath( os.path.join( core.FW_conf['test_result_dir'],"variant_settings_check") )
        if not os.path.isdir(result_folder):
            os.mkdir(result_folder)

        try:
            f = open(os.path.join(location, file), 'r')
        except:
            self.fail('could not open settings')

        okSettings = []
        failedSettings = {}
        missingFiles = []
        foundFiles = []
        warnings = []

        for line in f:
            m = re.search('.*set-setting.?"(.*)" "?(.+)"?.*\)', line)

            if m:
                setting = m.group(1)
                value = m.group(2).split('"')[0]
                phoneSetting= self.sx('(send (send config-manager get-setting "%s") ->string)' % setting)

                if phoneSetting != value:

                    if failedSettings.has_key(setting):
                        warnings.append('Setting %s is defined multiple times in sx configuration file.' % setting)

                    failedSettings[setting] = [value, phoneSetting]

                else:
                    okSettings.append(setting)

                if 'file:' in value: # this is a setting referring to a file in phone, check that it exist as well
                    # sp is the target path file system root
                    filename = 'c:/sp/' + re.sub('file:/*', '', value)
                    debug.brf('checking does %s exist' % filename)
                    if not self.file.fileExists(filename):
                        missingFiles.append(value)
                    else:
                        foundFiles.append(value)

            else:
                #debug.brf('no settings from configuration line:')
                #debug.brf(line)
                pass

        f.close()

        try:
            resfile = open(os.path.join(result_folder, resultfile), 'w')
        except:
            self.fail('could not open result file for writing')

        resfile.write('--- Build variant checking results ---\n\n')
        resfile.write('SW version:\n%s\n' % unicode(srv_info.getSwVersion(self),'Latin-1').replace('\0',''))
        if okSettings:
            debug.brf('These settings were ok:')
            resfile.write('\nThese settings were ok:\n')
            for s in okSettings:
                debug.brf('   %s' % s)
                resfile.write('   %s\n' % s)

        if len(failedSettings) > 0:
            msg = 'These settings were failed:'
            debug.brf(msg)
            resfile.write('\n%s\n' % msg )
            for i in failedSettings:
                msg = '%s:\n  Configuration [%s]\n  Phone value [%s]' % (i, failedSettings[i][0], failedSettings[i][1])
                debug.brf(msg)
                resfile.write('%s\n' % msg)

        elif len(okSettings) == 0:
            msg = 'NO SETTINGS CHECKED'
            debug.brf(msg)
            resfile.write('%s\n' % msg )
        else:
            msg = 'ALL CHECKED SETTINGS OK'
            debug.brf(msg)
            resfile.write('%s\n' % msg )

        if len(foundFiles) > 0:
            msg = 'These files were OK / found from phone:'
            debug.brf(msg)
            resfile.write('\n%s\n' % msg)
            for f in foundFiles:
                debug.brf(f)
                resfile.write('%s\n' % f)

        if len(missingFiles) > 0:
            msg = 'These files were missing from phone:'
            debug.brf(msg)
            resfile.write('\n%s\n' % msg)
            for f in missingFiles:
                debug.brf(f)
                resfile.write('%s\n' % f)
        elif len(foundFiles) == 0:
            msg = 'No content files checking done'
            debug.brf(msg)
            resfile.write('%s\n' % msg )
        else:
            msg = 'ALL CONTENT FILES FOUND FROM PHONE'
            debug.brf(msg)
            resfile.write('%s\n' % msg )

        if warnings:
            msg = 'warnings encountered:\n'
            debug.brf(msg)
            resfile.write(msg)
            for w in warnings:
                debug.brf(w)
                resfile.write('%s\n' % w)

        resfile.close()

        if len(okSettings) == 0 and len(failedSettings) == 0:
            self.fail('ERROR: No settings checked!')
        elif len(failedSettings) > 0 or len(missingFiles) > 0:
            self.fail('All settings were NOT OK.')
