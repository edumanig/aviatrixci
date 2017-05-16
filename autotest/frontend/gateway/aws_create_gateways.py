import unittest, logging, time
from selenium import webdriver
import autotest.lib.webui_pages.gateway as gateway
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases

class CreateGatewayTest(WebUITest):
    cases = testcases(__name__)
    case_list = cases.data

    def test_create_aws_gateways(self):
        gateway_view = gateway.Gateway(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)
        time.sleep(15)

        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(10)
        self.logger.info("Checking Gateway is present in the current view area...")
        self.assertTrue(gateway_view.is_gateway_table_present(), "Gateway view is not present")

        self.logger.info("Start to create various config for new gateways on AWS")

        for case in self.case_list:

            self.cases.start_test(case)
            self.logger.info("Clicking New Gateway button")
            gateway_view.click_new_gateway_button()
            time.sleep(5)
            self.assertTrue(gateway_view.new_gateway_panel_is_present(), "New Gateway panel is not found")

            assert gateway_view.fill_new_gateway_fields(**self.cases.case_data), "Failed to fill in Gateway configuration fields"

            time.sleep(1)
            self.logger.info("Clicking OK to create New Gateway...")
            self.assertTrue(actions_in_common.click_ok_button(), "Failed to click OK for new gateway")

            actions_in_common.wait_progress_bar()
            self.logger.info("Checking the result of creating new gateway...")
            result = actions_in_common.get_message()
            self.assertIn(self.cases.expected_result['toaster']+ self.cases.case_data['06.gateway_name'], result, "Fail to create a new gateway")
            actions_in_common.close_message()

            time.sleep(10)
            self.logger.info("Checking new gateway's state in gateway table")
            self.assertEquals(gateway_view.gateway_table.check_specific_row_data(self.driver, self.cases.case_data['06.gateway_name'], 2), self.cases.expected_result['status'],
                              "Gateway state is not up.")

            self.cases.end_test(case)

