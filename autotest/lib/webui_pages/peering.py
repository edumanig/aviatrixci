import logging
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
For Peering
==========================================================================================
"""
class SelectPeeringVPC1(DropdownSelect):
    locator = PeeringLocators.PEERING_VPC1

class SelectPeeringVPC2(DropdownSelect):
    locator = PeeringLocators.PEERING_VPC2

class CheckOverAWSPeering(Checkbox):
    selectedlocator = PeeringLocators.OVER_AWS_PEERING_IS_SELECTED
    clicklocator = PeeringLocators.OVER_AWS_PEERING_CLICK

class SelectSourceGateway(DropdownSelect):
    locator = PeeringLocators.SOURCE_GATEWAY

class SelectNexthopGateway(DropdownSelect):
    locator = PeeringLocators.NEXTHOP_GATEWAY

class InputDestinationCIDR(InputText) :
    locator = PeeringLocators.DESTINATION_CIDR


class Peering(BasePage):
    select_vpc1 = SelectPeeringVPC1()
    select_vpc2 = SelectPeeringVPC2()
    check_over_aws_peering = CheckOverAWSPeering()
    select_source_gateway = SelectSourceGateway()
    select_nexthop_gateway = SelectNexthopGateway()
    destination_cidr = InputDestinationCIDR()
    enc_peering_table = TableData(PeeringLocators.ENC_PEERING_TABLE_FOR_TABLE)
    transitive_peering_table = TableData(PeeringLocators.TRANSITIVE_PEERING_TABLE_FOR_TABLE)

    def navigate_to_peering(self):
        return Click(PeeringLocators.NAVIGATE_TO_PEERING).clicking(self.driver)

    def click_transitive_peering_tab(self):
        return Click(PeeringLocators.TRANSITIVE_PEERING).clicking(self.driver)

    def click_enc_peering_tab(self):
        return Click(PeeringLocators.ENCRYPTED_PEERING).clicking(self.driver)

    def is_enc_peering_table_present(self):
        return IsObjectPresent(PeeringLocators.ENC_PEERING_TABLE).check_now(self.driver,"Encrypted Peering table")

    def click_new_enc_peering_button(self):
        return Click(PeeringLocators.NEW_ENC_PEERING_BUTTON).clicking(self.driver)

    def click_new_transitive_peering_button(self):
        return Click(PeeringLocators.NEW_TRANSITIVE_PEERING_BUTTON).clicking(self.driver)

    def is_new_enc_peering_panel_present(self):
        return IsObjectPresent(PeeringLocators.NEW_ENC_PEERING_PANEL).check_now(self.driver,"New Encrypted Peering panel")

    def is_new_transitive_peering_panel_present(self):
        return IsObjectPresent(PeeringLocators.NEW_TRANSITIVE_PEERING_PANEL).check_now(self.driver,"New Transitive Peering panel")

    def click_new_transitive_peering_ok_button(self):
        return Click(PeeringLocators.NEW_TRANSITIVE_PEERING_OK_BUTTON).clicking(self.driver)

    def click_delete_enc_peering_button(self,value):
        return self.enc_peering_table.click_button_in_the_row(self.driver, 1, 5, value, PeeringLocators.DELETE_PEERING_BUTTON)

    def click_delete_transitive_peering_button(self,value):
        return self.transitive_peering_table.click_button_in_the_row(self.driver, 1, 4, value, PeeringLocators.DELETE_PEERING_BUTTON)

    def get_peering_data(self):
        peering_mapping = {}
        enc_peering_number = 0
        try:
            row_data = Peering.enc_peering_table.get_row_data(self.driver)
            if row_data is not None:
                enc_peering_number = len(row_data)
                self.logger.debug("Peering tunnels found in peering table are "+str(enc_peering_number))
                for row in row_data:
                    vpc_peer = row.split()[:2]
                    peering_mapping.setdefault(vpc_peer[0],{})[vpc_peer[1]] = 1
                    peering_mapping.setdefault(vpc_peer[1],{})[vpc_peer[0]] = 1
            return peering_mapping, enc_peering_number
        except:
            self.logger.exception("Could not get the peering data.")
