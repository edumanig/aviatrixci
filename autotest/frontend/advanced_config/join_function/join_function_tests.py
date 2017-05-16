import unittest, logging, time
from selenium import webdriver
import autotest.lib.webui_pages.gateway as gtwy
import autotest.lib.webui_pages.advanced_config as ac
import autotest.lib.webui_pages.join_function as jf
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases

class JoinFunctionTest(WebUITest):
    cases = testcases(__name__)

    def test01_create_join_gateway(self):
        gateway_view = gtwy.Gateway(self.driver)
        adconfig = ac.AdvancedConfig(self.driver)
        join_func = jf.JoinFunction(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)

        self.logger.info("Expanding Advanced Config...")
        adconfig.expand_advanced_config()
        self.logger.info("Navigate to Join Function")
        join_func.navigate_to_join_function()
        time.sleep(5)
        self.logger.info("Check if Join Gateway table is present in the current view...")
        self.assertTrue(join_func.join_gateway_panel_is_present(), "Join Gateway table is not present")

        self.cases.start_test('test_case_1')
        self.logger.info("Start to create gateways on existing VPC/VNet")

        for gw in self.cases.case_data:
            self.logger.info("Clicking Connect button")
            join_func.click_connect_button()
            time.sleep(5)
            self.assertTrue(join_func.join_create_panel_is_present(), "Create Connect panel is not found")

            assert gateway_view.fill_new_gateway_fields(
                **self.cases.case_data[gw]), "Failed to fill in Gateway configuration fields"

            time.sleep(1)
            self.logger.info("Clicking OK to create New Gateway...")
            self.assertTrue(actions_in_common.click_ok_button(), "Failed to click OK for new Join gateway")

            actions_in_common.wait_progress_bar()
            time.sleep(60)
            result = actions_in_common.get_message()
            self.assertIn(self.cases.expected_result['toaster'], result, "Fail to create a new gateway")
            actions_in_common.close_message()

            time.sleep(20)
            self.logger.info("Check if new Join gateway is listed in the table")
            self.assertTrue(join_func.join_gateway_table.is_data_present(self.driver, 1, self.cases.case_data[gw]['06.gateway_name']), "Gateway name is not found.")

        self.cases.end_test("test_case_1")

    def test02_subnet_test(self):
        join_func = jf.JoinFunction(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)

        self.logger.info("Start to add and delete the subnet")
        self.cases.start_test("test_case_2")

        for gw in self.cases.case_data:
            self.logger.info("Click Allow Subnet button")
            join_func.click_allow_seubnet(self.cases.case_data[gw]['gateway_name'])
            time.sleep(2)
            self.assertTrue(join_func.allow_subnet_panel_is_present(), "Allow Subnet panel is not found")

            join_func.allow_local_cidr = self.cases.case_data[gw]['local_cidr']
            self.logger.info("Click OK to allow this local CIDR")
            join_func.click_allow_subnet_ok()

            self.logger.info("Checking the result: Allow Subnet...")
            result = actions_in_common.get_message()
            self.assertIn(self.cases.expected_result['toaster_allow'], result,
                          "Fail to allow subnet for the Join gateway")
            actions_in_common.close_message()

            self.logger.info("Delete the subnet")
            join_func.click_delete_subnet(self.cases.case_data[gw]['gateway_name'])
            time.sleep(2)
            self.assertTrue(join_func.delete_subnet_panel_is_present(), "Delete Subnet panel is not found")

            self.logger.info("The local CIDR should be available for Delete Subnet")
            join_func.select_delete_local_cidr = self.cases.case_data[gw]['local_cidr']

            self.logger.info("Click OK to delete this local CIDR from the Join Gateway")
            join_func.click_delete_subnet_ok()

            self.logger.info("Checking the result: Delete Subnet...")
            result = actions_in_common.get_message()
            self.assertIn(self.cases.case_data[gw]['local_cidr'] + self.cases.expected_result['toaster_delete'] + self.cases.case_data[gw]['gateway_name'], result,
                          "Fail to delete subnet from the Join gateway")
            actions_in_common.close_message()

        self.cases.end_test("test_case_2")

    def test03_delete_join_gateway(self):
        join_func = jf.JoinFunction(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)

        self.logger.info("Start to delete the Join gateway")
        self.cases.start_test("test_case_3")

        for gw_name in self.cases.case_data:
            self.logger.info("Click Delete button")
            join_func.delete_join_gateway(self.cases.case_data[gw_name])

            time.sleep(3)
            self.logger.info("Clicking OK to delete the specified gateway...")
            actions_in_common.confirm_ok()

            actions_in_common.wait_progress_bar()
            time.sleep(60)
            result = actions_in_common.get_message()
            self.assertIn(self.cases.expected_result['toaster'], result, "Fail to create a new gateway")
            actions_in_common.close_message()

            time.sleep(20)
            self.logger.info("Verifying deleted Join gateway is no longer found in the Join Gateway table")
            self.assertFalse(
                join_func.join_gateway_table.is_data_present(self.driver, 1, self.cases.case_data[gw_name]),
                "Unexpectedly found the specified gateway")

        self.cases.end_test("test_case_3")















