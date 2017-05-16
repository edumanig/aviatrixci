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
For Gateway
==========================================================================================
"""

class SelectCloudType(DropdownSelect):
    locator = GatewayViewLocators.CLOUD_TYPE_SELECT

class SelectAccountName(DropdownSelect):
    locator = GatewayViewLocators.ACCOUNTNAME_SELECT

class SelectRegion(DropdownSelect):
    locator = GatewayViewLocators.REGION_SELECT

class SelectZone(DropdownSelect):
    locator = GatewayViewLocators.ZONE_SELECT

class SelectBackupGatewayZone(DropdownSelect):
    locator = GatewayViewLocators.BKUPGW_ZONE_SELECT

class SelectPublicSubnet(DropdownSelect):
    locator = GatewayViewLocators.PUBLIC_SUBNET_SELECT

class SelectGatewaySize(DropdownSelect):
    locator = GatewayViewLocators.GATEWAY_SIZE_SELECT

class SelectVPCID(DropdownSelect):
    locator = GatewayViewLocators.VPC_ID_SELECT

class InputGatewayName(InputText):
    locator = GatewayViewLocators.GATEWAY_NAME

class CheckEnableNAT(Checkbox):
    selectedlocator = GatewayViewLocators.ENABLE_NAT_CHECKBOX_IS_SELECTED
    clicklocator = GatewayViewLocators.ENABLE_NAT_CHECKBOX_CLICK

class CheckVPNAccess(Checkbox):
    selectedlocator = GatewayViewLocators.VPN_ACCESS_CHECKBOX_IS_SELECTED
    clicklocator = GatewayViewLocators.VPN_ACCESS_CHECKBOX_CLICK

class InputVPNCIDR(InputText):
    locator = GatewayViewLocators.VPN_CIDR_BLOCK

class Select2StepAuth(DropdownSelect):
    locator = GatewayViewLocators.TWO_STEP_AUTH_SELECT

class InputMaxConnection(InputText):
    locator = GatewayViewLocators.MAX_CONNECTIONS

class EnableSplitTunnel(RadioButton):
    yesclicklocator = GatewayViewLocators.SPLIT_TUNNEL_MODE_YES_CLICK
    yesselectedlocator = GatewayViewLocators.SPLIT_TUNNEL_MODE_YES_IS_SELECTED
    noclicklocator = GatewayViewLocators.SPLIT_TUNNEL_MODE_NO_CLICK
    noselectedlocator = GatewayViewLocators.SPLIT_TUNNEL_MODE_NO_IS_SELECTED

class EnableELB(RadioButton):
    yesclicklocator = GatewayViewLocators.ENABLE_ELB_YES_CLICK
    yesselectedlocator = GatewayViewLocators.ENABLE_ELB_YES_IS_SELECTED
    noclicklocator = GatewayViewLocators.ENABLE_ELB_NO_CLICK
    noselectedlocator = GatewayViewLocators.ENABLE_ELB_NO_IS_SELECTED

class InputELBName(InputText):
    locator = GatewayViewLocators.ELB_NAME

class EnableClientCertSharing(RadioButton):
    yesclicklocator = GatewayViewLocators.ENABLE_CLIENT_CERT_SHARING_YES_CLICK
    yesselectedlocator = GatewayViewLocators.ENABLE_CLIENT_CERT_SHARING_YES_IS_SELECTED
    noclicklocator = GatewayViewLocators.ENABLE_CLIENT_CERT_SHARING_NO_CLICK
    noselectedlocator = GatewayViewLocators.ENABLE_CLIENT_CERT_SHARING_NO_IS_SELECTED

class EnablePBR(Checkbox):
    selectedlocator = GatewayViewLocators.ENABLE_PBR_IS_SELECTED
    clicklocator =  GatewayViewLocators.ENABLE_PBR_CLICK

class InputPBRSubnet(InputText):
    locator = GatewayViewLocators.PBR_SUBNET

class InputPBRDefaultGateway(InputText):
    locator = GatewayViewLocators.PBR_DEFAULT_GATEWAY

class EnablePBRNATLogging(Checkbox):
    selectedlocator = GatewayViewLocators.PBR_LOGGING_IS_SELECTED
    clicklocator = GatewayViewLocators.PBR_LOGGING_CLICK

class EnableLDAP(Checkbox):
    selectedlocator = GatewayViewLocators.ENABLE_LDAP_IS_SELECTED
    clicklocator = GatewayViewLocators.ENABLE_LDAP_CLICK

class InputLDAPServer(InputText):
    locator = GatewayViewLocators.LDAP_SERVER

class CheckLDAPUseSSL(Checkbox):
    selectedlocator = GatewayViewLocators.LDAP_USE_SSL_IS_SELECTED
    clicklocator = GatewayViewLocators.LDAP_USE_SSL_CLICK

class InputBindDN(InputText):
    locator = GatewayViewLocators.BIND_DN

class InputLDAPPassword(InputText):
    locator = GatewayViewLocators.LDAP_PASSWORD

class InputBaseDN(InputText):
    locator = GatewayViewLocators.BASE_DN

class InputUsernameAttribute(InputText):
    locator = GatewayViewLocators.USERNAME_ATTRIBUTE

class InputGroupMembershipDN(InputText):
    locator = GatewayViewLocators.GROUP_MEMBERSHIP_DN

class InputLDAPUser(InputText):
    locator = GatewayViewLocators.LDAP_USER

class CheckSaveTemplate(Checkbox):
    selectedlocator = GatewayViewLocators.SAVE_TEMPLATE_IS_SELECTED
    clicklocator = GatewayViewLocators.SAVE_TEMPLATE_CLICK

class InputPolicySrc(InputText):
    locator = GatewayViewLocators.POLICY_SRC_IP

class InputPolicyDst(InputText):
    locator = GatewayViewLocators.POLICY_DST_IP

class SelectPolicyProtocol(DropdownSelect):
    locator = GatewayViewLocators.POLICY_PROTOCOL

class InputPortRange(InputText):
    locator = GatewayViewLocators.POLICY_PORT_RANGE

class SelectPolicyAction(DropdownSelect):
    locator = GatewayViewLocators.POLICY_ACTION

class SelectPolicyPacketLog(DropdownSelect):
    locator = GatewayViewLocators.POLICY_LOGGING

class SelectGatewayResize(DropdownSelect):
    locator = GatewayViewLocators.GATEWAY_RESIZING_SELECT

class SelectItemsPerPage(DropdownSelect):
    locator = GatewayViewLocators.ITEMS_PER_PAGE


class Gateway(BasePage):
    select_cloud_type = SelectCloudType()
    select_account_name = SelectAccountName()
    select_region = SelectRegion()
    select_zone = SelectZone()
    select_backup_gateway_zone = SelectBackupGatewayZone()
    select_vpc_id = SelectVPCID()
    gateway_name = InputGatewayName()
    select_public_subnet = SelectPublicSubnet()
    select_gateway_size = SelectGatewaySize()
    check_enable_nat = CheckEnableNAT()
    check_vpn_access = CheckVPNAccess()
    vpn_cidr = InputVPNCIDR()
    select_2_step_auth = Select2StepAuth()
    max_connections = InputMaxConnection()
    enable_split_tunnel = EnableSplitTunnel()
    enable_elb = EnableELB()
    elb_name = InputELBName()
    enable_client_cert_sharing = EnableClientCertSharing()
    enable_pbr = EnablePBR()
    pbr_subnet = InputPBRSubnet()
    pbr_default_gateway = InputPBRDefaultGateway()
    enable_pbr_nat_logging = EnablePBRNATLogging()
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
    policy_src = InputPolicySrc()
    policy_dst = InputPolicyDst()
    port_range = InputPortRange()
    select_policy_protocol = SelectPolicyProtocol()
    select_policy_action = SelectPolicyAction()
    select_policy_packet_log = SelectPolicyPacketLog()
    select_gateway_resize = SelectGatewayResize()
    select_items_per_page = SelectItemsPerPage()

    gateway_table = TableData(GatewayViewLocators.GATEWAY_TABLE_FOR_TABLE)
    policy_table = TableData(GatewayViewLocators.POLICY_TABLE_FOR_TABLE)
    new_security_policy_button = Click(GatewayViewLocators.NEW_SECURITY_POLICY_BUTTON)
    save_deploy_policies_button = Click(GatewayViewLocators.SAVE_DEPLOY_POLICIES)
    reset_policy_button = Click(GatewayViewLocators.RESET_TO_DEFAULT_BUTTON)

    def navigate_to_gateway(self):
        return Click(GatewayViewLocators.NAVIGATE_TO_GATEWAY).clicking(self.driver)

    def is_gateway_table_present(self):
        return IsObjectPresent(GatewayViewLocators.GATEWAY_TABLE).check_now(self.driver,"Gateway table")

    def click_new_gateway_button(self):
        return Click(GatewayViewLocators.NEW_GATEWAY_BUTTON).clicking(self.driver)

    def new_gateway_panel_is_present(self):
        return IsObjectPresent(GatewayViewLocators.NEW_GATEWAY_PANEL).check_now(self.driver,"Create Gateway panel")

    def fill_new_gateway_fields(self,**kwargs):
        field_list = ["01.cloud_type", "02.account_name", "03.region", "04.vpc_id", "05.vnet_name","06.gateway_name",
                      "public_subnet", "zone","gateway_size", "enable_nat", "07.vpn_access","vpn_cidr_block", "two_step_auth", "max_connection",
                      "split_tunnel_mode","08.enable_elb","elb_name","enable_client_cert_sharing","09.enable_pbr","pbr_subnet","pbr_default_gateway","pbr_nat_logging",
                      "10.enable_ldap","ldap_server","check_ldap_use_ssl","bind_dn","ldap_password","base_dn","username_attribute","group_membership_dn","ldap_user","save_template"]

        conf_data = OrderedDict(sorted(kwargs.items()))
        for key, value in conf_data.items():
            if not key in field_list:
                self.logger.error("Invalid Gateway configuration fields. Abort...")
                return False
            try:
                if key.lower() == "01.cloud_type":
                    self.select_cloud_type = value
                    time.sleep(10)
                if key.lower() == "02.account_name":
                    self.select_account_name = value
                    time.sleep(3)
                if key.lower() == "03.region":
                    self.select_region = value
                    time.sleep(15)
                if key.lower() == "04.vpc_id":
                    self.select_vpc_id = value
                    time.sleep(10)
                if key.lower() == "05.vnet_name":
                    self.select_vpc_id = value
                    time.sleep(10)
                if key.lower() == "06.gateway_name":
                    self.gateway_name = value
                if key.lower() == "public_subnet":
                    self.select_public_subnet = value
                    time.sleep(3)
                if key.lower() == "zone":
                    self.select_zone = value
                    time.sleep(3)
                if key.lower() == "gateway_size":
                    self.select_gateway_size = value
                    time.sleep(3)
                    time.sleep(3)
                if key.lower() == "enable_nat":
                    self.check_enable_nat = value
                if key.lower() == "07.vpn_access":
                    self.check_vpn_access = value
                    time.sleep(3)
                if key.lower() == "vpn_cidr_block":
                    self.vpn_cidr = value
                if key.lower() == "two_step_auth":
                    self.select_2_step_auth = value
                if key.lower() == "max_connection":
                    self.max_connections = value
                if key.lower() == "split_tunnel_mode":
                    self.enable_split_tunnel = value
                    time.sleep(3)
                if key.lower() == "08.enable_elb":
                    self.enable_elb = value
                    self.logger.info("Enable ELB is set to "+value)
                    time.sleep(3)
                if key.lower() == "elb_name":
                    self.elb_name = value
                if key.lower() == "enable_client_cert_sharing":
                    self.enable_client_cert_sharing = value
                if key.lower() == "09.enable_pbr":
                    self.enable_pbr = value
                if key.lower() == "pbr_subnet":
                    self.pbr_subnet = value
                if key.lower() == "pbr_default_gateway":
                    self.pbr_default_gateway = value
                if key.lower() == "pbr_nat_logging":
                    self.enable_pbr_nat_logging = value
                if key.lower() == "10.enable_ldap":
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
                return False
        return True

    def check_progress_box(self):
        try:
            ui.WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(GatewayViewLocators.GATEWAY_PROGRESS_BOX))
            self.logger.info("Waiting for the progress box to disappear... ")
            ui.WebDriverWait(self.driver, 720).until(
                EC.invisibility_of_element_located(GatewayViewLocators.GATEWAY_PROGRESS_BOX))
            self.logger.info("Progress Box is gone. Check the result...")
        except TimeoutException:
            self.logger.exception("Progress box is still present")
            self.close_progress_box()

    def close_progress_box(self):
        if IsObjectPresent(GatewayViewLocators.GATEWAY_PROGRESS_BOX).check_now(self.driver,"Progress Box"):
            self.logger.info("Close the progress box")
            return Click(GatewayViewLocators.CLOSE_PROGRESS_BOX).clicking(self.driver)

    def select_gateway_in_table(self, gw_name):
        gw_info = self.get_all_gateway_info("table")

        for x in range(len(gw_info)):
            if gw_name == gw_info[x].text.split("\n")[0]:
                time.sleep(2)
                gw_info[x].click()
                break
        else:
            self.logger.error("Couldn't find {} in the table".format(gw_name))

    def click_edit_gateway(self):
        return Click(GatewayViewLocators.EDIT_GATEWAY_BUTTON).clicking(self.driver)

    def click_delete_button(self):
         return Click(GatewayViewLocators.DELETE_GATEWAY_BUTTON).clicking(self.driver)

    """
    def delete_gateway(self,value):
        return self.gateway_table.click_button_in_the_row(self.driver,2,10,value,GatewayViewLocators.DELETE_GATEWAY_BUTTON)
    """


    def is_edit_panel_present(self):
        """
        try:
            ui.WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(GatewayViewLocators.EDIT_PANEL_TITLE))
            panel = self.driver.find_element(*GatewayViewLocators.EDIT_PANEL_TITLE)
            return panel.text.lower() == "edit {}".format(gwname)

        except TimeoutException:
            self.logger.exception("Could not find the panel to edit the specified gateway.")
        """
        return IsObjectPresent(GatewayViewLocators.EDIT_PANEL).check_now(self.driver,"Edit Panel")

    def show_gateway_details(self):
        try:
            detail_button = self.driver.find_element(*GatewayViewLocators.GATEWAY_DETAIL)
            detail_button.click()
            detail_box = self.driver.find_element(*GatewayViewLocators.DETAIL_BOX)
            return detail_box.text
        except NoSuchElementException:
            self.logger.exception("Could not display the gateway details")

    def click_enable_ha(self):
        return Click(GatewayViewLocators.ENABLE_HA_BUTTON).clicking(self.driver)

    def click_force_switchover(self):
        return Click(GatewayViewLocators.FORCE_SWITCHOVER_BUTTON).clicking(self.driver)

    def click_disable_ha(self):
        return Click(GatewayViewLocators.DISABLE_HA_BUTTON).clicking(self.driver)

    def click_create_hagw_button(self):
        return Click(GatewayViewLocators.CREATE_HAGW_BUTTON).clicking(self.driver)

    def fill_security_policy_form(self, **kwargs):
        field_list = ["source","destination","protocol", "protocol_port", "action", "logging"]

        conf_data = OrderedDict(sorted(kwargs.items()))
        for key, value in conf_data.items():
            if not key in field_list:
                self.logger.error("Invalid Gateway configuration fields. Abort...")
                return False
            try:
                if key.lower() == "source":
                    self.policy_src = value
                    time.sleep(1)
                if key.lower() == "destination":
                    self.policy_dst = value
                    time.sleep(1)
                if key.lower() == "protocol":
                    self.select_policy_protocol = value
                    time.sleep(1)
                if key.lower() == "protocol_port":
                    time.sleep(1)
                    self.port_range = value
                if key.lower() == "action":
                    time.sleep(1)
                    self.select_policy_action = value
                if key.lower() == "logging":
                    time.sleep(1)
                    self.select_policy_packet_log = value

            except NoSuchElementException as e:
                self.logger.exception("Gateway field exception: {}".format(e))
                return False
        return True

    def save_policy_inline(self, dest_value):
        return self.policy_table.click_button_in_the_row(self.driver, 2, 7, dest_value, GatewayViewLocators.SAVE_POLICY_INLINE)

    def click_inline_new_policy(self, value):
        return self.policy_table.click_button_in_the_row(self.driver, 2, 7, value,
                                                         GatewayViewLocators.NEW_POLICY_INLINE)
    def click_inline_cancel(self, value):
        return self.policy_table.click_button_in_the_row(self.driver, 2, 7, value,
                                                         GatewayViewLocators.CANCEL_POLICY_INLINE)
    def delete_saved_policy(self, dest_value):
        return self.policy_table.click_button_in_the_row(self.driver, 2, 7, dest_value,
                                                          GatewayViewLocators.DELETE_SAVED_POLICY)

    def click_change_button(self):
        return Click(GatewayViewLocators.GATEWAY_SIZE_CHANGE_BUTTON).clicking(self.driver)

    def close_edit_panel(self):
        return Click(GatewayViewLocators.CLOSE_EDIT_PANEL).clicking(self.driver)

    def set_items_per_page(self,value):
        if value in ["5","10","20"]:
            self.select_items_per_page = value
            time.sleep(5)
        else:
            self.logger.error("invalid value for pagination")

    def get_all_gateway_info(self, type = "info"):
        self.set_items_per_page("20")

        try:
            gw_rows = self.driver.find_elements(*GatewayViewLocators.GATEWAY_ROWS)
            if gw_rows and type == "info":
                return [x.text.split("\n") for x in gw_rows]
            if gw_rows and type == "table":
                return gw_rows

        except NoSuchElementException:
            self.logger.exception("Couldn't find the gateway row")


    def get_specific_gateway_row(self,gw_name, type = "info"):
        if type == "table":
            gw_info = self.get_all_gateway_info("table")
        else:
            gw_info = self.get_all_gateway_info()

        for x in range(len(gw_info)):
            if gw_name == gw_info[x][0]:
                return gw_info[x]
        else:
            self.logger.error("Couldn't find the specified gateway in the table")

    def is_gateway_present_in_table(self,gw_name):
        gw_info = self.get_all_gateway_info()

        if gw_info:
            for x in range(len(gw_info)):
                if gw_name == gw_info[x][0]:
                    return True
            else:
                self.logger.error("Specified gateway is not found in the table")











"""
==========================================================================================
For Settings > License
==========================================================================================
"""

class CustomerID(InputText):
    locator = SettingsLocators.CUSTOMER_ID

class License(BasePage):
    customer_id = CustomerID()


    def expand_settings(self):
        settings =self.driver.find_element(*SettingsLocators.SETTINGS_ICON)
        settings.click()

    def license_view(self):
        license = self.driver.find_element(*SettingsLocators.LICENSE)
        license.click()

