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
For Join Function
==========================================================================================
"""
class InputAllowLocalCIDR(InputText):
    locator = AdvancedConfigLocators.ALLOW_LOCAL_CIDR

class SelectDeleteLocalCIDR(DropdownSelect):
    locator = AdvancedConfigLocators.DELETE_LOCAL_CIDR


class JoinFunction(BasePage):
    allow_local_cidr = InputAllowLocalCIDR()
    select_delete_local_cidr = SelectDeleteLocalCIDR()
    join_gateway_table = TableData(AdvancedConfigLocators.JOIN_GATEWAY_TABLE_FOR_TABLE)

    def navigate_to_join_function(self):
        return Click(AdvancedConfigLocators.JOIN_FUNCTION).clicking(self.driver)

    def join_gateway_panel_is_present(self):
        return IsObjectPresent(AdvancedConfigLocators.JOIN_GATEWAY_PANEL).check_now(self.driver,"Join Gateway panel")

    def join_create_panel_is_present(self):
        return IsObjectPresent(AdvancedConfigLocators.JOIN_CREATE_PANEL).check_now(self.driver,"Join Create Connect panel")

    def click_connect_button(self):
        return Click(AdvancedConfigLocators.CONNECT_BUTTON).clicking(self.driver)

    #Use the Gateway's method to fill the form for creating new gateway.

    def delete_join_gateway(self,value):
        return self.join_gateway_table.click_button_in_the_row(self.driver,1,9,value,AdvancedConfigLocators.DELETE_BUTTON)

    def click_allow_seubnet(self,value):
        return self.join_gateway_table.click_button_in_the_row(self.driver, 1, 9, value,
                                                               AdvancedConfigLocators.ALLOW_SUBNET_BUTTON)

    def click_delete_subnet(self,value):
        return self.join_gateway_table.click_button_in_the_row(self.driver, 1, 9, value,
                                                               AdvancedConfigLocators.DELETE_SUBNET_BUTTON)

    def allow_subnet_panel_is_present(self):
        return IsObjectPresent(AdvancedConfigLocators.ALLOW_SUBNET_PANEL).check_now(self.driver,"Allow Subnet panel")

    def delete_subnet_panel_is_present(self):
        return IsObjectPresent(AdvancedConfigLocators.DELETE_SUBNET_PANEL).check_now(self.driver,"Delete Subnet panel")

    def click_allow_subnet_ok(self):
        return Click(AdvancedConfigLocators.ALLOW_SUBNET_OK_BUTTON).submitting(self.driver)

    def click_allow_subnet_cancel(self):
        return Click(AdvancedConfigLocators.ALLOW_SUBNET_CANCEL_BUTTON).clicking(self.driver)

    def click_delete_subnet_ok(self):
        return Click(AdvancedConfigLocators.DELETE_SUBNET_OK_BUTTON).submitting(self.driver)

    def click_delete_subnet_cancel(self):
        return Click(AdvancedConfigLocators.DELETE_SUBNET_CANCEL_BUTTON).clicking(self.driver)





