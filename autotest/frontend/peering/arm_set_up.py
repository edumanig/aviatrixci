import unittest, logging, time, os
from selenium import webdriver
from autotest.lib.webui_pages import peering
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
from autotest.lib.arm_utils import *
from autotest.run_autotest import cloud_account
from autotest.lib.webui_pages import gateway
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.lib.test_utils import testcases


class ARMPeering(WebUITest):
    cases = testcases(__name__)
    case_list = cases.data

    def test_arm_set_up(self):
        subscription_id = cloud_account['azure_account_info']['subscription_id']
        tenant_id = cloud_account['azure_account_info']['tenant_id']
        client_id = cloud_account['azure_account_info']['client_id']
        client_secret = cloud_account['azure_account_info']['client_secret']

        crendtls = get_ad_sp_credential(tenant_id, client_id, client_secret)

        self.cases.start_test("set_up_vnet")
        self.logger.info("start to set up Resource group")
        #create_resource_group(subscription_id,crendtls,self.cases.case_data['region'],self.cases.case_data['resource_group'])
        self.logger.info("start to create VNet")
        #create_virtual_network(subscription_id,crendtls,self.cases.case_data['region'],self.cases.case_data['resource_group'],self.cases.case_data['vnet_name'],self.cases.case_data['subnet_name'],self.cases.case_data['cidr'],self.cases.case_data['subnet_cidr'])
        self.cases.end_test('set_up_vnet')

    def test_new_region_size(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        gateway_view = gateway.Gateway(self.driver)
        time.sleep(10)

        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(10)


        for case in self.case_list:
            if 'test_case' in case:
                self.cases.start_test(case)
                self.logger.info("Clicking New Gateway button")
                gateway_view.click_new_gateway_button()
                time.sleep(5)
                self.assertTrue(gateway_view.new_gateway_panel_is_present(), "New Gateway panel is not found")

                assert gateway_view.fill_new_gateway_fields(
                    **self.cases.case_data), "Failed to fill in Gateway configuration fields"

                time.sleep(1)
                self.logger.info("Clicking OK to create New Gateway...")
                self.assertTrue(actions_in_common.click_ok_button(), "Failed to click OK for new gateway")

                actions_in_common.wait_progress_bar()
                self.logger.info("Checking the result of creating new gateway...")
                result = actions_in_common.get_message()
                self.assertIn(self.cases.expected_result['toaster'] + self.cases.case_data['06.gateway_name'], result,
                              "Fail to create a new gateway")
                actions_in_common.close_message()
                time.sleep(60)
                gateway_view.delete_gateway(self.cases.case_data['06.gateway_name'])
                time.sleep(3)
                self.logger.info("Clicking OK to delete the specified gateway...")
                actions_in_common.confirm_delete()

                actions_in_common.wait_progress_bar()
                self.logger.info("Checking the result of deleting gateway...it takes a while")
                result = actions_in_common.get_message()
                self.assertIn("has been deleted", result, "Failed to delete the gateway")
                actions_in_common.close_message()

                self.cases.end_test(case)

