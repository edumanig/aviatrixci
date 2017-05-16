"""
==========================================================================================
For Advanced Config
==========================================================================================
"""
import logging
from collections import OrderedDict
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from autotest.lib.common_elements import *
from autotest.lib.page_locators import *
from autotest.lib.webui_pages.basepage import BasePage


class SelectCloudType(DropdownSelect):
    locator = AdvancedConfigLocators.CLOUD_TYPE

class SelectAccountName(DropdownSelect):
    locator = AdvancedConfigLocators.ACCOUNT_NAME

class InputPoolName(InputText):
    locator = AdvancedConfigLocators.POOL_NAME

class InputNumberOfVPCs(InputText):
    locator = AdvancedConfigLocators.NUMBER_OF_VPCS

class InputVPCCIDR(InputText):
    locator = AdvancedConfigLocators.VPC_CIDR

class SelectVPCRegion(DropdownSelect):
    locator = AdvancedConfigLocators.VPC_REGION


class AdvancedConfig(BasePage):
    select_cloud_type = SelectCloudType()
    select_account_name = SelectAccountName()
    pool_name = InputPoolName()
    number_of_vpcs = InputNumberOfVPCs()
    vpc_cidr = InputVPCCIDR()
    select_vpc_region = SelectVPCRegion()
    vpc_pool_table = TableData(AdvancedConfigLocators.POOL_TABLE_FOR_TABLE)

    def expand_advanced_config(self):
        return Click(AdvancedConfigLocators.EXPAND_ADVANCED_CONFIG).clicking(self.driver)

    def navigate_to_create_vpc_pool(self):
        return Click(AdvancedConfigLocators.CREATE_VPC_POOL).clicking(self.driver)

    def click_create_button(self):
        return Click(AdvancedConfigLocators.CREATE_BUTTON).clicking(self.driver)

    def create_pool_panel_is_present(self):
        return IsObjectPresent(AdvancedConfigLocators.CREATE_POOL_FORM).check_now(self.driver,"Create VPC Pool panel")

    def fill_new_vpc_fields(self, **kwargs):
        field_list = ["cloud_type", "account_name", "vpc_region", "vpc_cidr", "pool_name", "number", "vpc_id"]

        conf_data = OrderedDict(sorted(kwargs.items()))
        for key, value in conf_data.items():
            if not key in field_list:
                self.logger.error("Invalid Gateway configuration fields. Abort...")
                return False
            try:
                if key.lower() == "cloud_type":
                    self.select_cloud_type = value
                if key.lower() == "pool_name":
                    self.pool_name = value
                if key.lower() == "account_name":
                    self.select_account_name = value
                if key.lower() == "vpc_region":
                    self.select_vpc_region = value
                    time.sleep(3)
                if key.lower() == "vpc_cidr":
                    self.vpc_cidr = value
                    time.sleep(2)
                if key.lower() == "number":
                    self.number_of_vpcs = value
            except NoSuchElementException as e:
                self.logger.exception("Gateway field exception: {}".format(e))
        return True

    def submit_create_button(self):
        return Click(AdvancedConfigLocators.CREATE_SUBMIT_BUTTON).clicking(self.driver)

    def is_vpc_pool_table_present(self):
        return IsObjectPresent(AdvancedConfigLocators.VPC_POOL_TABLE).check_now(self.driver,"VPC pool table")

    def delete_vpc_pool(self, poolname):
        return self.vpc_pool_table.click_button_in_the_row(self.driver,1,6,poolname,AdvancedConfigLocators.DELETE_POOL_BUTTON)

