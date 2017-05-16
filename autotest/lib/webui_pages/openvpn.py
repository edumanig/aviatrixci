import logging
from collections import OrderedDict
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from autotest.lib.common_elements import *
from autotest.lib.page_locators import *
from autotest.lib.webui_pages.basepage import BasePage


"""
==========================================================================================
For OpenVPN
==========================================================================================
"""

class SelectUserVPCID(DropdownSelect):
    locator = OpenVPNLocators.USER_VPC_ID

class SelectUserLBNAME(DropdownSelect):
    locator = OpenVPNLocators.USER_LB_NAME

class InputUserName(InputText):
    locator = OpenVPNLocators.USER_NAME

class InputUserEmail(InputText):
    locator = OpenVPNLocators.USER_EMAIL

class AssociateProfile(Checkbox):
    selectedlocator = OpenVPNLocators.PROFILE_IS_SELECT
    clicklocator = OpenVPNLocators.PROFILE_CLICK

class SelectProfileName(DropdownSelect):
    locator = OpenVPNLocators.PROFILE_NAME

class SelectGEOVPNCloudType(DropdownSelect):
    locator = OpenVPNLocators.GEO_VPN_CLOUD

class SelectGeoVPNAccountName(DropdownSelect):
    locator = OpenVPNLocators.GEO_VPN_ACCOUNT_NAME

class InputGeoVPNDomainName(InputText):
    locator = OpenVPNLocators.GEO_VPN_DOMAIN_NAME

class InputGeoVPNServiceName(InputText):
    locator = OpenVPNLocators.GEO_VPN_SERVICE_NAME

class SelectGeoVPNELBDNSName(DropdownSelect):
    locator = OpenVPNLocators.GEO_VPN_ELB_DNS_NAME

class InputCACert(InputText):
    locator = OpenVPNLocators.CA_CERT

class InputServerCert(InputText):
    locator = OpenVPNLocators.SERVER_CERT

class InputServerPrivateKey(InputText):
    locator = OpenVPNLocators.SERVER_PRIVATE_KEY

class InputCRLDistURI(InputText):
    locator = OpenVPNLocators.CRL_DIST_URI

class InputCRLUpdateInterval(InputText):
    locator = OpenVPNLocators.CRL_UPDATE_INTERVAL

class SelectVPNConfigVPCID(DropdownSelect):
    locator = OpenVPNLocators.VPC_ID

class SelectVPNConfigLBName(DropdownSelect):
    locator = OpenVPNLocators.LB_NAME

class InputProfileName(InputText):
    locator = OpenVPNLocators.PROFILE_NAME

class SelectBasePolicy(DropdownSelect):
    locator = OpenVPNLocators.BASE_POLICY

class SelectPolicyProtocol(DropdownSelect):
    locator = OpenVPNLocators.PROFILE_EDIT_SELECT_PROTOCOL

class InputTargetCIDR(InputText):
    locator = OpenVPNLocators.PROFILE_EDIT_TARGET

class InputPolicyPort(InputText):
    locator = OpenVPNLocators.PROFILE_EDIT_PORT

class SelectPolicyAction(DropdownSelect):
    locator = OpenVPNLocators.PROFILE_EDIT_SELECT_ACTION

class SelectUserName(DropdownSelect):
    locator = OpenVPNLocators.USER_NAME

class SelectProfileDetachVPCID(DropdownSelect):
    locator = OpenVPNLocators.PROFILE_DETACH_USER_VPC_ID

class SelectProfileDetachUserName(DropdownSelect):
    locator = OpenVPNLocators.PROFILE_DETACH_USER_USER_NAME


class OpenVPN(BasePage):
    select_user_vpc_id = SelectUserVPCID()
    select_user_lb_name = SelectUserLBNAME()
    user_name = InputUserName()
    user_email = InputUserEmail()
    associate_profile = AssociateProfile()
    select_profile_name = SelectProfileName()
    select_geo_vpn_cloud_type = SelectGEOVPNCloudType()
    select_geo_vpn_account_name = SelectGeoVPNAccountName()
    geo_vpn_domain_name = InputGeoVPNDomainName()
    geo_vpn_service_name = InputGeoVPNServiceName()
    select_geo_vpn_elb_dns_name = SelectGeoVPNELBDNSName()
    ca_cert = InputCACert()
    server_cert = InputServerCert()
    server_private_key = InputServerPrivateKey()
    crl_dist_uri = InputCRLDistURI()
    crl_update_interval = InputCRLUpdateInterval()
    select_vpc_id = SelectVPNConfigVPCID()
    select_lb_name = SelectVPNConfigLBName()
    profile_name = InputProfileName()
    select_base_policy = SelectBasePolicy()
    select_policy_protocol = SelectPolicyProtocol()
    target_cidr = InputTargetCIDR()
    policy_port = InputPolicyPort()
    select_policy_action = SelectPolicyAction()
    select_user_name = SelectUserName()
    select_profile_detach_vpc_id = SelectProfileDetachVPCID()
    select_profile_detach_user_name = SelectProfileDetachUserName()

    user_table = TableData(OpenVPNLocators.VPN_USERS_TABLE_FOR_TABLE)
    profile_table = TableData(OpenVPNLocators.PROFILE_TABLE_FOR_TABLE)
    policy_table = TableData(OpenVPNLocators.PROFILE_POLICY_TABLE_for_TABLE)

    def expand_openvpn(self):
        return Click(OpenVPNLocators.EXPAND_OPENVPN).clicking(self.driver)

    def vpn_users(self):
        return Click(OpenVPNLocators.VPN_USERS).clicking(self.driver)

    def is_user_table_present(self):
        return IsObjectPresent(OpenVPNLocators.VPN_USERS_TABLE).check_now(self.driver,"VPN User table")

    def click_add_button(self):
        return Click(OpenVPNLocators.ADD_USER_BUTTON).clicking(self.driver)

    def is_add_user_panel_present(self):
        return IsObjectPresent(OpenVPNLocators.ADD_USER_PANEL).check_now(self.driver,"Add User panel")

    def fill_new_user_form(self, **kwargs):
        field_list = ["id_vpc", "lb_name", "user_email", "associate_profile", "user_name", "profile_name"]

        conf_data = OrderedDict(sorted(kwargs.items()))
        for key, value in conf_data.items():
            if not key in field_list:
                self.logger.error("Invalid New User fields. Abort...")
                return False
            try:
                if key.lower() == "id_vpc":
                    self.select_user_vpc_id = value
                    time.sleep(3)
                if key.lower() == "associate_profile":
                    self.associate_profile = value
                if key.lower() == "lb_name":
                    self.select_user_lb_name = value
                if key.lower() == "user_name":
                    self.user_name = value
                if key.lower() == "user_email":
                    self.user_email = value
                if key.lower() == "profile_name":
                    self.select_profile_name = value
            except NoSuchElementException as e:
                self.logger.exception("Gateway field exception: {}".format(e))
        return True

    def click_reissue_button(self,value):
        return self.user_table.click_button_in_the_row(self.driver,1,6,value,OpenVPNLocators.REISSUE_BUTTON)

    def click_user_delete_button(self,value):
        return self.user_table.click_button_in_the_row(self.driver,1,6,value,OpenVPNLocators.USER_DELETE_BUTTON)

    def configuration(self):
        return Click(OpenVPNLocators.CONFIGURATION).clicking(self.driver)

    def is_public_ip_display_panel_present(self):
        return IsObjectPresent(OpenVPNLocators.DISPLAY_PUBLIC_IP_PANEL).check_now(self.driver,"Public IP Display panel")

    def click_to_change_status(self,locator):
        try:
            if locator.lower() == "public ip display":
                status = self.driver.find_element(*OpenVPNLocators.DISPLAY_PUBLIC_IP)
            elif locator.lower() == "geo vpn":
                status = self.driver.find_element(*OpenVPNLocators.GEO_CLOUD_STATUS)
            if status:
                status.click()
                return True
        except NoSuchElementException:
            self.logger.exception("Could not find the status bar to click")

    def check_config_status(self,locator):
        try:
            if locator.lower() == "public ip display":
                status = self.driver.find_element(*OpenVPNLocators.DISPLAY_PUBLIC_IP)
            elif locator.lower() == "geo vpn":
                status = self.driver.find_element(*OpenVPNLocators.GEO_CLOUD_STATUS)
            if status:
                return status.text

        except NoSuchElementException:
            self.logger.exception("Could not find the status bar to click")
            return None

    def is_geo_vpn_enable_panel_present(self):
        return IsObjectPresent(OpenVPNLocators.GEO_VPN_ENABLE_PANEL).check_now(self.driver,"Geo VPN Config")

    def certificate(self):
        return Click(OpenVPNLocators.CERTIFICATE).clicking(self.driver)

    def is_import_panel_present(self):
        return IsObjectPresent(OpenVPNLocators.IMPORT_PANEL).check_now(self.driver,"Import Cert Config")

    def is_download_vpn_conf_panel_present(self):
        return IsObjectPresent(OpenVPNLocators.DOWNLOAD_PANEL).check_now(self.driver,"Download Config panel")

    def click_download_button(self):
        return Click(OpenVPNLocators.DOWNLAOD_BUTTON).clicking(self.driver)

    def profiles(self):
        return Click(OpenVPNLocators.PROFILES).clicking(self.driver)

    def is_profile_table_panel_present(self):
        return IsObjectPresent(OpenVPNLocators.PROFILE_TABLE_PANEL).check_now(self.driver,"Profile table")

    def click_new_profile(self):
        return Click(OpenVPNLocators.NEW_PROFILE_BUTTON).clicking(self.driver)

    def is_new_profile_panel_present(self):
        return IsObjectPresent(OpenVPNLocators.NEW_PROFILE_PANEL).check_now(self.driver,"New Profile form")

    def click_ok_new_profile(self):
        return Click(OpenVPNLocators.NEW_PROFILE_OK_BUTTON).clicking(self.driver)

    def click_edit_button(self,value):
        return self.profile_table.click_button_in_the_row(self.driver,1,2,value,OpenVPNLocators.PROFILE_EDIT_BUTTON)

    def is_profile_edit_panel_present(self):
        return IsObjectPresent(OpenVPNLocators.PROFILE_EDIT_PANEL).check_now(self.driver,"Edit Profile panel")

    def click_to_display_profile_users(self):
        return Click(OpenVPNLocators.PROFILE_EDIT_SHOW_USERS_BUTTON).clicking(self.driver)

    def click_add_new_policy(self):
        return Click(OpenVPNLocators.PROFILE_EDIT_ADD_NEW_BUTTON).clicking(self.driver)

    def fill_new_policy_form(self, **kwargs):
        field_list = ["protocol", "target", "protocol_port", "action"]

        conf_data = OrderedDict(sorted(kwargs.items()))
        for key, value in conf_data.items():
            if not key in field_list:
                self.logger.error("Invalid New Policy fields. Abort...")
                return False
            try:
                if key.lower() == "protocol":
                    self.select_policy_protocol = value
                    time.sleep(1)
                if key.lower() == "protocol_port":
                    self.policy_port = value
                if key.lower() == "target":
                    self.target_cidr = value
                if key.lower() == "action":
                    self.select_policy_action = value
            except NoSuchElementException as e:
                self.logger.exception("Gateway field exception: {}".format(e))
        return True

    def click_policy_save_button(self):
        return Click(OpenVPNLocators.PROFILE_EDIT_SAVE_BUTTON).clicking(self.driver)

    def click_policy_delete_button(self):
        return self.policy_table.click_button_in_the_row(self.driver,2,5,"www.yahoo.com",OpenVPNLocators.PROFILE_POLICY_TABLE_DELETE_BUTTON)

    def click_profile_edit_cancel_button(self):
        return Click(OpenVPNLocators.PROFILE_EDIT_CANCEL_BUTTON).clicking(self.driver)

    def click_attach_user_button(self):
        return self.profile_table.click_button_in_the_row(self.driver,1,2,"autotest101",OpenVPNLocators.PROFILE_ATTACH_USER_BUTTON)

    def is_attach_user_panel_present(self):
        return IsObjectPresent(OpenVPNLocators.PROFILE_ATTACH_USER_PANEL).check_now(self.driver,"Attach User form")

    def is_detach_user_panel_present(self):
        return IsObjectPresent(OpenVPNLocators.PROFILE_DETACH_USER_PANEL).check_now(self.driver,"Detach User form")

    def show_profile_user_detail(self):
        try:
            show_detail = self.driver.find_element(*OpenVPNLocators.PROFILE_EDIT_SHOW_USER_DETAIL)
            if show_detail:
                return show_detail.text
        except (WebDriverException, NoSuchElementException):
            self.logger.exception("Could not click Cancel button")
            return None

    def click_detach_user_button(self):
        return self.profile_table.click_button_in_the_row(self.driver,1,2,"autotest101",OpenVPNLocators.PROFILE_DETACH_USER_BUTTON)

    def click_detach_ok_button(self):
        return Click(OpenVPNLocators.PROFILE_DETACH_OK_BUTTON).submitting(self.driver)

    def click_delete_profile_button(self,value):
        return self.profile_table.click_button_in_the_row(self.driver,1,2,value,OpenVPNLocators.PROFILE_DELETE_BUTTON)
