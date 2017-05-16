import unittest, logging, time, os
from selenium import webdriver
from autotest.lib.webui_pages import advanced_config
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases


class CreateVPCPool(WebUITest):
    cases = testcases(__name__)

    def test_create_vpc(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        adconfig = advanced_config.AdvancedConfig(self.driver)
        time.sleep(10)

        self.logger.info("Expanding Advanced Config...")
        adconfig.expand_advanced_config()
        time.sleep(3)
        self.logger.info("Navigate to Create VPC Pool")
        adconfig.navigate_to_create_vpc_pool()
        time.sleep(5)

        self.cases.start_test('test_case_1')
        self.logger.info("Clicking Create button...")
        adconfig.click_create_button()
        self.assertTrue(adconfig.create_pool_panel_is_present(), "Create VPC Pool panel is not found")

        time.sleep(2)
        adconfig.fill_new_vpc_fields(**self.cases.case_data)

        time.sleep(3)
        self.logger.info("Clicking Create to create a VPC Pool...")
        adconfig.submit_create_button()

        self.logger.info("Checking the result of creating a VPC Pool...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'] + self.cases.expected_result['pool_name'], result, "Failed to create a new VPC")
        actions_in_common.close_message()

        self.cases.end_test('test_case_1')

    def test_delete_vpc_pool(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        adconfig = advanced_config.AdvancedConfig(self.driver)
        time.sleep(5)

        self.logger.info("checking VPC pool table is present...")
        self.assertTrue(adconfig.is_vpc_pool_table_present(), "VPC pool table is not found")

        self.cases.start_test("test_case_2")
        self.logger.info('Selecting the pool name to delete...')
        adconfig.delete_vpc_pool(self.cases.case_data['pool_name'])

        self.logger.info("Confirm to delete...")
        actions_in_common.confirm_ok()

        self.logger.info("Checking the result...")
        result = actions_in_common.get_message()
        self.assertEqual(self.cases.expected_result['toaster']+self.cases.case_data['pool_name'], result, "Fail to delete the VPC pool")

        time.sleep(5)
        self.logger.info("Verifying deleted pool is no longer in the list")
        self.assertFalse(adconfig.vpc_pool_table.is_data_present(self.driver,1,self.cases.case_data['pool_name']),
                         "Found the specified pool")
        actions_in_common.close_message()

        self.cases.end_test("test_case_2")
