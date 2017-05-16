from collections import OrderedDict
from autotest.lib.common_elements import *
from autotest.lib.page_locators import *
from autotest.lib.webui_pages.site2cloud.s2c_base import S2C_Base


class NewButton(ActionButton):
    locator = S2CViewLocators.ADD_NEW

class SelectVPCID(DropdownSelect):
    locator = S2CViewLocators.VPC_ID

class SelectConnectionType(DropdownSelect):
    locator = S2CViewLocators.CONNECTION_TYPE

class SelectPrimaryGateway(DropdownSelect):
    locator = S2CViewLocators.PRIMARY_GATEWAY

class SelectBackupGateway(DropdownSelect):
    locator = S2CViewLocators.BACKUP_GATEWAY

class InputConnectionName(InputText):
    locator = S2CViewLocators.CONNECTION_NAME

class InputCustomerGatewayIPAddress(InputText):
    locator = S2CViewLocators.CUSTOMER_GATEWAY_IP_ADDRESS

class InputCustomerBackupGatewayIP(InputText):
    locator = S2CViewLocators.CUSTOMER_BACKUP_GATEWAY_IP

class InputCustomerNetworkReal(InputText):
    locator = S2CViewLocators.CUSTOMER_NETWORK_REAL

class InputCustomerNetworkVirtual(InputText):
    locator = S2CViewLocators.CUSTOMER_NETWORK_VIRTUAL

class InputCloudSubnetReal(InputText):
    locator = S2CViewLocators.CLOUD_SUBNET_REAL

class InputCloudSubnetVirtual(InputText):
    locator = S2CViewLocators.CLOUD_SUBNET_VIRTUAL

class InputPreSharedKey(InputText):
    locator = S2CViewLocators.PRE_SHARED_KEY

class InputPreSharedKeyBackup(InputText):
    locator = S2CViewLocators.PRE_SHARED_KEY_BKUP

class PrivateRouteEncryption(Checkbox):
    clicklocator =  S2CViewLocators.PRIMARY_ROUTE_ENCRYPTION_CLICK
    selectedlocator = S2CViewLocators.PRIMARY_ROUTE_ENCRYPTION_IS_SELECTED

class EnableNullEncryption(Checkbox):
    clicklocator = S2CViewLocators.NULL_ENCRYPTION_CLICK
    selectedlocator = S2CViewLocators.NULL_ENCRYPTION_IS_SELECTED

"""
class HASwitchButton(SwitchButton):
    status = S2CViewLocators.HA_SWITCH_STATUS
    enable = S2CViewLocators.HA_SWITCH_ENABLE
    disable = S2CViewLocators.HA_SWITCH_DISABLE
"""

class CheckEnableHA(Checkbox):
    selectedlocator = S2CViewLocators.ENABLE_HA_IS_SELECTED
    clicklocator = S2CViewLocators.ENABLE_HA_CLICK

class OkButton(ActionButton):
    locator = S2CViewLocators.OK_BUTTON

class CancelButton(ActionButton):
    locator = S2CViewLocators.CANCEL_BUTTON

class S2CToaster(ToasterLM):
    toaster = S2CViewLocators.S2C_TOASTER
    toaster_closer = S2CViewLocators.S2C_TOASTER_CLOSER

class ConnTable(Table):
    locator = S2CViewLocators.CONN_TABLE

class ConfigVendor(DropdownSelect):
    locator = S2CViewLocators.CONFIG_VENDOR

class ConfigPlatform(DropdownSelect):
    locator = S2CViewLocators.CONFIG_PLATFORM

class ConfigSoftware(DropdownSelect):
    locator = S2CViewLocators.CONFIG_SOFTWARE

class ConfigDownloadBtn(ActionButton):
    locator = S2CViewLocators.CONFIG_DWLD_BTN

class ChangeCustomerNetwork(InputText):
    locator = S2CViewLocators.CHANGE_CUSTOMER_NW

class ChangeCustomerNetworkBtn(ActionButton):
    locator = S2CViewLocators.CHANGE_CUSTOMER_NW_BTN

class ChangeCloudNetwork(InputText):
    locator = S2CViewLocators.CHANGE_CLOUD_NW

class ChangeCloudNetworkBtn(ActionButton):
    locator = S2CViewLocators.CHANGE_CLOUD_NW_BTN

class ImportConfigBtn(ActionButton):
    locator = S2CViewLocators.IMPORT_CONFIG_BTN

class ImportConfigFile(InputText):
    locator = S2CViewLocators.IMPORT_CONFIG_FILE

class TunnelTable(Table):
    locator = S2CViewLocators.TUNNEL_TABLE

class S2C_New(S2C_Base):
    """
    GUI components and functions for Site2Cloud 'Add New' page
    """
    new_button = NewButton()
    select_vpc_id = SelectVPCID()
    select_conn_type = SelectConnectionType()
    select_primary_gw = SelectPrimaryGateway()
    select_backup_gw = SelectBackupGateway()
    input_conn_name = InputConnectionName()
    input_customer_gw_ip = InputCustomerGatewayIPAddress()
    input_customer_backup_gw_ip = InputCustomerBackupGatewayIP
    input_customer_nw_real = InputCustomerNetworkReal()
    input_customer_nw_virtual = InputCustomerNetworkVirtual()
    input_cloud_sub_real = InputCloudSubnetReal()
    input_cloud_sub_virtual = InputCloudSubnetVirtual()
    input_pre_shared_key = InputPreSharedKey()
    input_pre_shared_key_backup = InputPreSharedKeyBackup()
    private_route_encryption = PrivateRouteEncryption()
    #ha_switch_button = HASwitchButton()
    check_enable_ha = CheckEnableHA()
    enable_null_encryption = EnableNullEncryption()
    ok_button = OkButton()
    cancel_button = CancelButton()
    s2c_toaster = S2CToaster()
    import_config_btn = ImportConfigBtn()
    import_config_file = ImportConfigFile()

    def __init__(self, driver, login_required=False):
        self.driver = driver
        S2C_Base.__init__(self, self.driver, login_required=login_required)

    def is_ha_enabled(self):
        """
        Check if site2cloud HA is enabled or not
        :return: True if HA is enabled; False if HA is disabled
        """
        try:
            self.driver.find_element_by_css_selector("span.checked")
            self.logger.info("Site2Cloud HA is enabled")
            return True
        except NoSuchElementException:
            self.logger.info("Site2Cloud HA is disabled")
            return False

    def fill_conn_fields(self, **kwargs):
        """
        Fill the fields for a new site2cloud connection
        :param kwargs: parameters for the new site2cloud connection
        :return: True or False
        """
        field_list = ["01.description","06.enable_ha", "02.vpc_id", "03.conn_type", "08.primary_gw", "09.backup_gw",
                      "04.conn_name", "05.customer_gw_ip", "customer_nw_real", "customer_nw_virtual",
                      "private_route_encr", "cloud_sub_real", "cloud_sub_virtual",
                      "07.null_encr","customer_backup_gw_ip"]

        oindata = OrderedDict(sorted(kwargs.items()))
        for key, value in oindata.items():
            if not key in field_list:
                self.logger.error("Invalid Site2Cloud connection fields. Abort...")
                return False
            try:
                if key.lower() == "01.description":
                    self.logger.info(value)
                if key.lower() == "02.vpc_id":
                    self.select_vpc_id = value
                    time.sleep(5)
                    self.logger.debug("Site2Cloud VPC ID/VNet Name: %s", value)
                if key.lower() == "03.conn_type":
                    time.sleep(5)
                    self.select_conn_type = value
                    self.logger.debug("Site2Cloud Connection Type: %s", value)
                if key.lower() == "06.enable_ha":
                    time.sleep(3)
                    self.check_enable_ha = value
                    self.logger.info("Site2Cloud Enable HA is {}".format(value))
                if key.lower() == "07.null_encr":
                    time.sleep(3)
                    self.enable_null_encryption = value
                    self.logger.info("Site2Cloud Enable Null Encryption is {}".format(value))
                if key.lower() == "08.primary_gw":
                    time.sleep(10)
                    self.select_primary_gw = value
                    self.logger.debug("Site2Cloud Primary Gateway: %s", value)
                if key.lower() == "09.backup_gw":
                    time.sleep(5)
                    self.select_backup_gw = value
                    self.logger.debug("Site2Cloud Backup Gateway: %s", value)
                if key.lower() == "04.conn_name":
                    time.sleep(3)
                    self.input_conn_name = value
                    self.logger.debug("Site2Cloud Connection Name: %s", value)
                if key.lower() == "05.customer_gw_ip":
                    time.sleep(3)
                    self.input_customer_gw_ip = value
                    self.logger.debug("Site2Cloud Customer Gateway IP Address: %s", value)
                if key.lower() == "customer_backup_gw_ip":
                    time.sleep(3)
                    self.input_customer_backup_gw_ip = value
                    self.logger.debug("Site2Cloud Customer Backup Gateway IP Address: %s", value)
                if key.lower() == "customer_nw_real":
                    time.sleep(3)
                    self.input_customer_nw_real = value
                    self.logger.debug("Site2Cloud Customer Network Real: %s", value)
                if key.lower() == "customer_nw_virtual":
                    time.sleep(3)
                    self.input_customer_nw_virtual = value
                    self.logger.debug("Site2Cloud Customer Network Virtual: %s", value)
                if key.lower() == "cloud_sub_real":
                    time.sleep(3)
                    self.input_cloud_sub_real = value
                    self.logger.debug("Site2Cloud Cloud Subnet Real: %s", value)
                if key.lower() == "cloud_sub_virtual":
                    time.sleep(3)
                    self.input_cloud_sub_virtual = value
                    self.logger.debug("Site2Cloud Cloud Subnet Virtual: %s", value)
                if key.lower() == "private_route_encr":
                    time.sleep(3)
                    self.private_route_encryption = value
                    self.logger.debug("Site2Cloud Private Route Encryption: %s", value)
            except NoSuchElementException as e:
                self.logger.exception("Site2Cloud connection fill fields exception: %s", str(e))
                return False
        return True

    def click_import_button(self):
        return Click(S2CViewLocators.IMPORT_CONFIG_BTN).clicking(self.driver)

    def input_file_name_for_import(self,fpath):
        filelement = self.driver.find_element(*S2CViewLocators.IMPORT_CONFIG_FILE)
        if filelement:
            filelement.send_keys(fpath)


class S2C_View(S2C_Base):
    """
    GUI components and functions for configuration modification and template download
    """
    conn_table = ConnTable()
    s2c_toaster = S2CToaster()
    cfg_vendor = ConfigVendor()
    cfg_platform = ConfigPlatform()
    cfg_software = ConfigSoftware()
    cfg_dnld_btn = ConfigDownloadBtn()
    change_customer_nw = ChangeCustomerNetwork()
    change_customer_nw_btn = ChangeCustomerNetworkBtn()
    change_cloud_nw_btn = ChangeCloudNetworkBtn()
    change_cloud_nw = ChangeCloudNetwork()
    change_toaster = S2CToaster()
    tunnel_table = TunnelTable()

    def __init__(self, driver, login_required=False):
        self.driver = driver
        S2C_Base.__init__(self, self.driver, login_required=login_required)

    def find_s2c_conn(self, s2c_name):
        """
        Find the connection named as 's2c_name' from the connection table and then click it
        :param s2c_name:
        :return: True or False
        """
        index = 0
        index_found = 0
        for conn in self.conn_table:
            if conn['Name'].lower() == s2c_name.lower():
                self.logger.info("Site2Cloud connection %s found", s2c_name)
                index_found = index_found + 1
                break
            if index_found:
                break
            else:
                index = index + 1

        if index_found:
            self.logger.info("Select Site2Cloud %s", s2c_name)
            if index == 0:
                xpath = "//table/tbody/tr/td[1]"
            else:
                xpath = "//table/tbody/tr[" + str(index) + "]/td[1]"
            table = self.driver.find_element(*S2CViewLocators.CONN_TABLE)
            table.find_element_by_xpath(xpath).click()
            return True
        else:
            self.logger.error("Site2Cloud connection %s not found", s2c_name)
            return False

    def find_delete_col(self, table):
        """
        Find the column of the 'delete' button in site2cloud table
        :param table: site2cloud connection table
        :return: column number of 'delete' button in the table
        """
        td_index = 1
        td_index_found = 0
        trs = table.find_elements_by_tag_name('tr')
        for tr in trs:
            ths = tr.find_elements_by_tag_name('th')
            if ths:
                for th in ths:
                    if not th.text:
                        td_index_found = td_index_found + 1
                        break
                    td_index = td_index + 1
            if td_index_found:
                break
        return td_index

    def find_delete_row(self, table, s2c_name):
        """
        Find the row of the site2cloud connection to be deleted in the table
        :param table: site2cloud connection table
        :param s2c_name: site2cloud connection name
        :return: row number of the site2cloud connection named as s2c_name
        """
        tr_index = 0
        tr_index_found = 0
        trs = table.find_elements_by_tag_name('tr')
        for tr in trs:
            tds = tr.find_elements_by_tag_name('td')
            if tds:
                for td in tds:
                    if td.text == s2c_name:
                        self.logger.info("Site2Cloud connection %s found", s2c_name)
                        tr_index_found = tr_index_found + 1
                        break
            if tr_index_found:
                break
            else:
                tr_index = tr_index + 1
        return tr_index

    def get_s2c_element(self, s2c_name, s2c_element):
        """
        Find the value of a table element for a connection named as 's2c_name'
        :param s2c_name: site2cloud connection name
        :param s2c_element: one of the following elements
            - VPC ID/VNet Name
            - Status
            - Aviatrix Gateway
            - Customer Gateway IP
            - Customer Network
            - Cloud Network
        :return: The value of the table element
        """
        for conn in self.conn_table:
            if conn['Name'].lower() == s2c_name.lower():
                self.logger.info("%s for Site2Cloud Connection %s is %s" %
                                  (s2c_element, s2c_name, conn[s2c_element]))
                return conn[s2c_element]
        return ""

    def download_config(self, vendor, platform, software):
        """
        Download the configuration template of a site2cloud connection
        :param vendor: 'Aviatrix', 'Cisco', or 'Generic'
        :param platform: platform type of each vendor
        :param software: software version of each platform
        :return: click 'Download Configuration' button to download the template
        """
        if vendor.lower() in ["aviatrix", "cisco", "generic"]:
            self.cfg_vendor = vendor
            time.sleep(5)
        else:
            self.logger.error("Vendor type is wrong. Abort...")
            return False
        if platform.lower() in ["ucc", "asa 5500 series", "generic"]:
            self.cfg_platform = platform
            time.sleep(5)
        else:
            self.logger.error("Platform type is wrong. Abort...")
            return False
        if software.lower() in ['1.0', 'asa 8.2+', 'asa 9.x', 'vendor independent']:
            self.cfg_software = software
            time.sleep(5)
        else:
            self.logger.error("Software type is wrong. Abort...")
            return False

        self.cfg_dnld_btn = "Download Configuration"

        return True

    def change_customer_network(self, CIDRs):
        """
        Change 'Customer Network' of an existing site2cloud connection
        :param CIDRs: new CIDRs of 'Customer Network'
        :return: True
        """
        self.change_customer_nw = CIDRs
        self.change_customer_nw_btn = "Change Customer Network"

        return True

    def change_cloud_network(self, CIDRs):
        """
        Change 'Cloud Network' of an existing site2cloud connection
        :param CIDRs: new CIDRs of 'Cloud Network'
        :return: True
        """
        self.change_cloud_nw = CIDRs
        self.change_cloud_nw_btn = "Change Cloud Network"

        return True

    def get_conn_details(self):
        """
        Retrieve connection details
        :return: output of connection details
        """
        try:
            self.driver.find_element(*S2CViewLocators.CONN_DETAILS_HAMBURGER).click()
            output = self.driver.find_element(*S2CViewLocators.CONN_DETAILS_INFO).text
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error("Can't get site2cloud connection details with exception %s", str(e))
            output = ""
        return output

    def delete_conn(self, conn_name):
        try:
            table = self.driver.find_element(*S2CViewLocators.CONN_TABLE)

            td_index = self.find_delete_col(table)

            tr_index = self.find_delete_row(table, conn_name)
            self.logger.debug("Click 'Delete' button for Site2Cloud %s", conn_name)
            xpath = "//table/tbody/tr[" + str(tr_index) + "]/td[" + str(td_index) + "]/button"
            table.find_element_by_xpath(xpath).click()
            time.sleep(2)
            handle_alert(self)
            time.sleep(2)
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.debug("Can not find the table with exception %s", str(e))
            return False