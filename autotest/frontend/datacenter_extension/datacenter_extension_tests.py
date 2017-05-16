import unittest, logging, time
from selenium import webdriver
import autotest.lib.webui_pages.gateway as gw
import autotest.lib.webui_pages.datacenter_extension as de
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases

class CreateVPCTest(WebUITest):
    cases = testcases(__name__)
    case_list = cases.data

    def test_create_vpc(self):
        gateway_view = gw.Gateway(self.driver)
        datacenter_ext = de.DatacenterExtension(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)

        for case in self.case_list:
            self.cases.start_test(case)

            self.logger.info("Navigating to Datacenter Extension")
            datacenter_ext.navigate_to_datacenter_extension()
            time.sleep(15)
            self.logger.info("Checking if Create VPC/VNet form is present in the current view area...")
            self.assertTrue(datacenter_ext.create_panel_is_present(), "Create Form is not present")

            self.logger.info("Start to create various config for new VPCs and its gateways on AWS")
            assert datacenter_ext.fill_create_vpc_form(
                **self.cases.case_data), "Failed to fill Create VPC form"

            time.sleep(1)
            self.logger.info("Clicking Launch to create VPC...")
            self.assertTrue(actions_in_common.click_ok_button(), "Failed to click Launch for new VPC")

            actions_in_common.wait_progress_bar()
            self.logger.info("Checking the result of creating new gateway...")
            result = actions_in_common.get_message()
            self.assertIn(self.cases.expected_result['toaster_create'], result,
                          "Fail to create a new Datacenter Extension")
            actions_in_common.close_message()

            time.sleep(3)
            self.logger.info("Navigating to Gateway")
            self.logger.info("Checking new gateway's state in gateway table")
            gateway_view.navigate_to_gateway()
            time.sleep(10)
            self.assertEquals(
                gateway_view.gateway_table.check_specific_row_data(self.driver, self.cases.case_data['05.gateway_name'],
                                                                   2), self.cases.expected_result['status'],
                "Gateway state is not up.")

            time.sleep(60)
            self.logger.info("Delete the gateway and datacenter extension...")
            gateway_view.delete_gateway(self.cases.case_data['05.gateway_name'])
            time.sleep(3)
            self.logger.info("Clicking OK to delete the specified gateway...")
            actions_in_common.confirm_ok()

            actions_in_common.wait_progress_bar()
            self.logger.info("Checking the result of deleting the gateway...")
            result = actions_in_common.get_message()
            self.assertIn(self.cases.case_data['05.gateway_name'] + self.cases.expected_result['toaster_delete'], result,
                          "Failed to delete the gateway")
            actions_in_common.close_message()

            time.sleep(30)
            self.logger.info("Verifying deleted gateway is no longer in gateway list")
            self.assertFalse(gateway_view.gateway_table.is_data_present(self.driver, 2, self.cases.case_data['05.gateway_name']),
                             "Unexpectedly found the specified gateway")

            self.cases.end_test(case)
