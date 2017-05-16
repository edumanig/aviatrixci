import unittest, logging, time, os
from selenium import webdriver
from autotest.lib.webui_pages import gateway,advanced_config
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases


class CreateVPCPool(WebUITest):
    cases = testcases(__name__)

    def test_set_up(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        gateway_view = gateway.Gateway(self.driver)
        adconfig = advanced_config.AdvancedConfig(self.driver)
        time.sleep(10)

        self.logger.info("Expanding Advanced Config...")
        adconfig.expand_advanced_config()
        time.sleep(3)
        self.logger.info("Navigate to Create VPC Pool")
        adconfig.navigate_to_create_vpc_pool()
        time.sleep(5)

        self.cases.start_test('set_up_vpc')
        self.logger.info("Clicking Create button...")
        adconfig.click_create_button()
        self.assertTrue(adconfig.create_pool_panel_is_present(), "Create VPC Pool panel is not found")

        time.sleep(5)
        adconfig.fill_new_vpc_fields(**self.cases.case_data)

        time.sleep(3)
        self.logger.info("Clicking Create to create a VPC Pool...")
        adconfig.submit_create_button()

        self.logger.info("Checking the result of creating a VPC Pool...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'] + self.cases.expected_result['pool_name'], result, "Failed to create a new VPC")
        actions_in_common.close_message()
        vpc_id = adconfig.vpc_pool_table.check_specific_row_data(self.driver, self.cases.case_data['pool_name'],4) + "--" + self.cases.case_data['pool_name'] + "001"
        self.cases.end_test('set_up_vpc')

        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(10)

        self.cases.start_test('set_up_gateway')
        self.cases.case_data['gateway1']['04.vpc_id'] = vpc_id
        self.cases.case_data['gateway2']['04.vpc_id'] = vpc_id
        for gw in self.cases.case_data:

            self.logger.info("Clicking New Gateway button")
            gateway_view.click_new_gateway_button()
            time.sleep(5)
            self.assertTrue(gateway_view.new_gateway_panel_is_present(), "New Gateway panel is not found")

            assert gateway_view.fill_new_gateway_fields(**self.cases.case_data[gw]), "Failed to fill in Gateway configuration fields"

            time.sleep(1)
            self.logger.info("Clicking OK to create New Gateway...")
            self.assertTrue(actions_in_common.click_ok_button(), "Failed to click OK for new gateway")

            actions_in_common.wait_progress_bar()
            self.logger.info("Checking the result of creating new gateway...")
            result = actions_in_common.get_message()
            self.assertIn(self.cases.expected_result['toaster']+ self.cases.case_data[gw]['06.gateway_name'], result, "Fail to create a new gateway")
            actions_in_common.close_message()

        self.cases.end_test('set_up_gateway')

