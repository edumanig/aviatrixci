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
For Datacenter Extension
==========================================================================================
"""
class SelectCloudType(DropdownSelect):
    locator = DatacenterExtensionLocators.CLOUD_TYPE

class SelectAccountName(DropdownSelect):
    locator = DatacenterExtensionLocators.ACCOUNT_NAME

class SelectRegion(DropdownSelect):
    locator = DatacenterExtensionLocators.REGION

class InputGatewayName(InputText):
    locator = DatacenterExtensionLocators.GATEWAY_NAME

class SelectGatewaySize(DropdownSelect):
    locator = DatacenterExtensionLocators.GATEWAY_SIZE

class SelectCIDR(DropdownSelect):
    locator = DatacenterExtensionLocators.CIDR

class EnableInternetAccess(Checkbox):
    selectedlocator = DatacenterExtensionLocators.INTERNET_ACCESS_IS_SELECT
    clicklocator = DatacenterExtensionLocators.INTERNET_ACCSES_CLICK

class EnablePublicSubnet(Checkbox):
    selectedlocator = DatacenterExtensionLocators.PUBLIC_SUBNET_IS_SELECT
    clicklocator = DatacenterExtensionLocators.PUBLIC_SUBNET_CLICK

class EnableVPNAccess(Checkbox):
    selectedlocator = DatacenterExtensionLocators.VPN_ACCESS_IS_SELECT
    clicklocator = DatacenterExtensionLocators.VPN_ACCESS_CLICK

class Select2StepAuth(DropdownSelect):
    locator = DatacenterExtensionLocators.TWO_STEP_AUTH_SELECT

class InputMaxConnection(InputText):
    locator = DatacenterExtensionLocators.MAX_CONNECTIONS

class EnableSplitTunnel(RadioButton):
    yesclicklocator = DatacenterExtensionLocators.SPLIT_TUNNEL_MODE_YES_CLICK
    yesselectedlocator = DatacenterExtensionLocators.SPLIT_TUNNEL_MODE_YES_IS_SELECTED
    noclicklocator = DatacenterExtensionLocators.SPLIT_TUNNEL_MODE_NO_CLICK
    noselectedlocator = DatacenterExtensionLocators.SPLIT_TUNNEL_MODE_NO_IS_SELECTED

class InputAdditionalCIDRs(InputText):
    locator = DatacenterExtensionLocators.ADDITIONAL_CIDRS

class InputNameservers(InputText):
    locator = DatacenterExtensionLocators.NAMESERVERS

class InputSearchDomains(InputText):
    locator = DatacenterExtensionLocators.SEARCH_DOMAINS

class EnableELB(RadioButton):
    yesclicklocator = DatacenterExtensionLocators.ENABLE_ELB_YES_CLICK
    yesselectedlocator = DatacenterExtensionLocators.ENABLE_ELB_YES_IS_SELECTED
    noclicklocator = DatacenterExtensionLocators.ENABLE_ELB_NO_CLICK
    noselectedlocator = DatacenterExtensionLocators.ENABLE_ELB_NO_IS_SELECTED

class EnableClientCertSharing(RadioButton):
    yesclicklocator = DatacenterExtensionLocators.ENABLE_CLIENT_CERT_SHARING_YES_CLICK
    yesselectedlocator = DatacenterExtensionLocators.ENABLE_CLIENT_CERT_SHARING_YES_IS_SELECTED
    noclicklocator = DatacenterExtensionLocators.ENABLE_CLIENT_CERT_SHARING_NO_CLICK
    noselectedlocator = DatacenterExtensionLocators.ENABLE_CLIENT_CERT_SHARING_NO_IS_SELECTED

class EnableLDAP(Checkbox):
    selectedlocator = DatacenterExtensionLocators.ENABLE_LDAP_IS_SELECTED
    clicklocator = DatacenterExtensionLocators.ENABLE_LDAP_CLICK

class InputLDAPServer(InputText):
    locator = DatacenterExtensionLocators.LDAP_SERVER

class CheckLDAPUseSSL(Checkbox):
    selectedlocator = DatacenterExtensionLocators.LDAP_USE_SSL_IS_SELECTED
    clicklocator = DatacenterExtensionLocators.LDAP_USE_SSL_CLICK

class InputBindDN(InputText):
    locator = DatacenterExtensionLocators.BIND_DN

class InputLDAPPassword(InputText):
    locator = DatacenterExtensionLocators.LDAP_PASSWORD

class InputBaseDN(InputText):
    locator = DatacenterExtensionLocators.BASE_DN

class InputUsernameAttribute(InputText):
    locator = DatacenterExtensionLocators.USERNAME_ATTRIBUTE

class InputGroupMembershipDN(InputText):
    locator = DatacenterExtensionLocators.GROUP_MEMBERSHIP_DN

class InputLDAPUser(InputText):
    locator = DatacenterExtensionLocators.LDAP_USER

class CheckSaveTemplate(Checkbox):
    selectedlocator = DatacenterExtensionLocators.SAVE_TEMPLATE_IS_SELECTED
    clicklocator = DatacenterExtensionLocators.SAVE_TEMPLATE_CLICK


class DatacenterExtension(BasePage):
    select_cloud_type = SelectCloudType()
    select_account_name = SelectAccountName()
    select_region = SelectRegion()
    gateway_name = InputGatewayName()
    select_cidr = SelectCIDR()
    select_gateway_size = SelectGatewaySize()
    enable_internet_access = EnableInternetAccess()
    enable_public_subnet = EnablePublicSubnet()
    enable_vpn_access = EnableVPNAccess()
    select_2_step_auth = Select2StepAuth()
    max_connections = InputMaxConnection()
    enable_split_tunnel = EnableSplitTunnel()
    enable_elb = EnableELB()
    enable_client_cert_sharing = EnableClientCertSharing()
    enable_ldap = EnableLDAP()
    ldap_server = InputLDAPServer()
    check_ldap_use_ssl = CheckLDAPUseSSL()
    bind_dn = InputBindDN()
    ldap_password = InputLDAPPassword()
    base_dn = InputBaseDN()
    username_attribute = InputUsernameAttribute()
    group_membership_dn = InputGroupMembershipDN()
    ldap_user = InputLDAPUser()
    save_template = CheckSaveTemplate()

    def navigate_to_datacenter_extension(self):
        return Click(DatacenterExtensionLocators.NAVIGATE_TO_DATACENTER_EXT).clicking(self.driver)

    def create_panel_is_present(self):
        return IsObjectPresent(DatacenterExtensionLocators.CREATE_PANEL).check_now(self.driver,"Create VPC/VNet panel")

    def fill_create_vpc_form(self,**kwargs):
        field_list = ["01.cloud_type", "02.account_name", "03.region", "04.cidr", "05.gateway_name",
                      "enable_public_subnet", "enable_internet_access","gateway_size", "06.vpn_access", "two_step_auth", "max_connection",
                      "07.split_tunnel_mode","enable_elb","enable_client_cert_sharing",
                      "08.enable_ldap","ldap_server","check_ldap_use_ssl","bind_dn","ldap_password","base_dn","username_attribute","group_membership_dn","ldap_user","save_template"]

        conf_data = OrderedDict(sorted(kwargs.items()))
        for key, value in conf_data.items():
            if not key in field_list:
                self.logger.error("Invalid Gateway configuration fields. Abort...")
                return False
            try:
                if key.lower() == "01.cloud_type":
                    self.select_cloud_type = value
                    time.sleep(5)
                if key.lower() == "02.account_name":
                    self.select_account_name = value
                    time.sleep(2)
                if key.lower() == "03.region":
                    self.select_region = value
                    time.sleep(2)
                if key.lower() == "04.cidr":
                    self.select_cidr = value
                    time.sleep(10)
                if key.lower() == "05.gateway_name":
                    self.gateway_name = value
                if key.lower() == "enable_public_subnet":
                    self.enable_public_subnet = value
                    time.sleep(3)
                if key.lower() == "enable_internet_access":
                    self.enable_internet_access = value
                    time.sleep(1)
                if key.lower() == "gateway_size":
                    self.select_gateway_size = value
                    time.sleep(3)
                if key.lower() == "06.vpn_access":
                    self.enable_vpn_access = value
                    time.sleep(3)
                if key.lower() == "two_step_auth":
                    self.select_2_step_auth = value
                if key.lower() == "max_connection":
                    self.max_connections = value
                if key.lower() == "07.split_tunnel_mode":
                    self.enable_split_tunnel = value
                    time.sleep(3)
                if key.lower() == "enable_elb":
                    self.enable_elb = value
                    time.sleep(1)
                if key.lower() == "enable_client_cert_sharing":
                    self.enable_client_cert_sharing = value
                if key.lower() == "08.enable_ldap":
                    self.enable_ldap = value
                if key.lower() == "ldap_server":
                    self.ldap_server = value
                if key.lower() == "check_ldap_use_ssl":
                    self.check_ldap_use_ssl = value
                if key.lower() == "bind_dn":
                    self.bind_dn = value
                if key.lower() == "ldap_password":
                    self.ldap_password = value
                if key.lower() == "base_dn":
                    self.base_dn = value
                if key.lower() == "username_attribute":
                    self.username_attribute = value
                if key.lower() == "group_membership_dn":
                    self.group_membership_dn = value
                if key.lower() == "ldap_user":
                    self.ldap_user =value
                if key.lower() == "save_template":
                    self.save_template = value
            except NoSuchElementException as e:
                self.logger.exception("Gateway field exception: {}".format(e))
        return True

