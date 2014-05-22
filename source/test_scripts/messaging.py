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

class SMSSettingsTest(uitestcase.UITestCase):
    subarea = "Messaging"
    feature = "SMS Settings"

    def testMessageCenterNumberLocked(self):
        '''
        @tcId Message center number locked check
        '''
        group="Messaging"
        feature="SMS Settings"
        setting="Message center number locked"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testSMSDeliveryReportsForSIM1(self):
        '''
        @tcId SMS Delivery Reports for SIM1 check
        '''
        group="Messaging"
        feature="SMS Settings"
        setting="SMS Delivery Reports for SIM1"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testSMSDeliveryReportsForSIM2(self):
        '''
        @tcId SMS Delivery Reports for SIM2 check
        '''
        group="Messaging"
        feature="SMS Settings"
        setting="SMS Delivery Reports for SIM2"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testTimestampUsedInMessaging(self):
        '''
        @tcId Timestamp type to be used in messaging check
        '''
        group="Messaging"
        feature="SMS Settings"
        setting="Timestamp type to be used in messaging"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testSMSEncodingSupport(self):
        '''
        @tcId SMS Encoding Support check
        '''
        group="Messaging"
        feature="SMS Settings"
        setting="SMS Encoding Support"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
        
class MMSSettingsTest(uitestcase.UITestCase):
    subarea = "Messaging"
    feature = "MMS Settings"

    def testRequestMMSDeliveryReportForSIM1(self):
        '''
        @tcId Request MMS Delivery Report for SIM1 check
        '''
        group="Messaging"
        feature="MMS Settings"
        setting="Request MMS Delivery Report for SIM1"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testRequestMMSDeliveryReportForSIM2(self):
        '''
        @tcId Request MMS Delivery Report for SIM2 check
        '''
        group="Messaging"
        feature="MMS Settings"
        setting="Request MMS Delivery Report for SIM2"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testMaximumSizeForReceivedMMSMessage(self):
        '''
        @tcId Maximum size for received MMS message check
        '''
        group="Messaging"
        feature="MMS Settings"
        setting="Maximum size for received MMS message"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testMMSRetrievalModeForSIM1(self):
        '''
        @tcId MMS Retrieval mode for SIM1 check
        '''
        group="Messaging"
        feature="MMS Settings"
        setting="MMS Retrieval mode for SIM1"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testMMSRetrievalModeForSIM2(self):
        '''
        @tcId MMS Retrieval mode for SIM2 check
        '''
        group="Messaging"
        feature="MMS Settings"
        setting="MMS Retrieval mode for SIM2"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testAllowAdvertsForSIM1(self):
        '''
        @tcId Allow adverts for SIM1 check
        '''
        group="Messaging"
        feature="MMS Settings"
        setting="Allow adverts for SIM1"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
        
    def testAllowAdvertsForSIM2(self):
        '''
        @tcId Allow adverts for SIM2 check
        '''
        group="Messaging"
        feature="MMS Settings"
        setting="Allow adverts for SIM2"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testSMSToMMSConversionThresholdValue(self):
        '''
        @tcId SMS to MMS conversion threshold value check
        '''
        group="Messaging"
        feature="MMS Settings"
        setting="SMS to MMS conversion threshold value"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

class OtherMessagingSettingsTest(uitestcase.UITestCase):
    subarea = "Messaging"
    feature = "Other Messaging Settings"

    def testCellBroadcastReception(self):
        '''
        @tcId Cell Broadcast Reception check
        '''
        group="Messaging"
        feature="Other Messaging Settings"
        setting="Cell Broadcast Reception"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)
        
    def testCellBroadcastChannelsconfiguration(self):
        '''
        @tcId Cell Broadcast Channels configuration check
        '''
        group="Messaging"
        feature="Other Messaging Settings"
        setting="Cell Broadcast Channels configuration"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testPublicWarningSystemUsingCellBroadcastSupport(self):
        '''
        @tcId Public Warning system using Cell Broadcast support check
        '''
        group="Messaging"
        feature="Other Messaging Settings"
        setting="Public Warning system using Cell Broadcast support"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testTheIdentifiersOfCMASCBAndTheirDisplayPriority(self):
        '''
        @tcId The identifiers of CMAS CB and their display priority check
        '''
        group="Messaging"
        feature="Other Messaging Settings"
        setting="The identifiers of CMAS CB and their display priority."
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)

    def testUSSDExpirationTime(self):
        '''
        @tcId USSD expiration time
        '''
        group="Messaging"
        feature="Other Messaging Settings"
        setting="USSD expiration time"
        csc = CommonSettingCompare(self)
        csc._commonSettingCompare(group, feature, setting)