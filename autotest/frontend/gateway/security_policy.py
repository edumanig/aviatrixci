import unittest, logging, time
from selenium import webdriver
import autotest.lib.webui_pages.gateway as gw
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases


class SecurityPolicy(WebUITest):
    cases = testcases(__name__)

    def test_security_policy(self):
        gateway_view = gw.Gateway(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)

        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(15)

        self.logger.info("Checking Gateway is present in the current view area...")
        self.assertTrue(gateway_view.is_gateway_table_present(), "Gateway view is not present")

        self.logger.info("Clicking on the gateway to edit it...")
        self.cases.start_test("test_case_1")
        gateway_view.gateway_table.click_row_to_edit(self.driver, self.cases.case_data['gateway_name'])
        self.assertTrue(gateway_view.is_edit_panel_present(),"Failed to find the edit panel")
        time.sleep(8)

        self.logger.info("Click Add New button for new Security Policy")
        self.assertTrue(gateway_view.new_security_policy_button.clicking(self.driver),"Failed to find Add New button for Security Policy")
        time.sleep(2)
        self.logger.info("Click Save without filling the fields for policy")
        gateway_view.save_policy_inline("")

        self.logger.info("Checking the toaster message")
        result = actions_in_common.get_message()
        self.assertEqual(self.cases.expected_result['toaster'], result,
                         "Unexpectedly saved the policy")
        actions_in_common.close_message()
        self.cases.end_test("test_case_1")

        time.sleep(2)
        self.cases.start_test("test_case_2")
        self.logger.info("Input Source")
        gateway_view.policy_src = self.cases.case_data['source']
        gateway_view.save_policy_inline("")

        self.logger.info("Checking the toaster message")
        result = actions_in_common.get_message()
        self.assertEqual(self.cases.expected_result['toaster'], result,
                         "Unexpectedly saved the policy")
        actions_in_common.close_message()
        self.cases.end_test("test_case_2")

        time.sleep(2)
        self.cases.start_test("test_case_3")
        self.logger.info("Input Source, Destination and Protocol but leave Port empty")
        gateway_view.fill_security_policy_form(**self.cases.case_data)

        gateway_view.save_policy_inline(self.cases.case_data['destination'])

        self.logger.info("Checking the toaster message")
        result = actions_in_common.get_message()
        self.assertEqual(self.cases.expected_result['toaster'], result,
                         "Unexpectedly saved the policy")
        actions_in_common.close_message()
        self.cases.end_test("test_case_3")

        time.sleep(2)
        self.cases.start_test("test_case_4")
        self.logger.info("Start to fill the fields for new security policy")
        gateway_view.fill_security_policy_form(**self.cases.case_data)
        time.sleep(1)
        self.logger.info("Click Save to save the policy")
        self.assertTrue(gateway_view.save_policy_inline(self.cases.case_data['destination']), "Failed to click the button to save the policy")
        self.cases.end_test("test_Case_4")
        time.sleep(2)

        self.cases.start_test("test_case_5")
        self.logger.info("Click inline Add New button for policy")
        self.assertTrue(gateway_view.click_inline_new_policy(self.cases.case_data['destination']),"Failed to click inline Add New button for policy")
        time.sleep(3)
        gateway_view.fill_security_policy_form(**self.cases.case_data['new_policy'])
        time.sleep(2)
        self.assertTrue(gateway_view.save_policy_inline(""),
                        "Failed to click the button to save the policy")
        time.sleep(2)
        self.logger.info("Click inline Add New button again")
        self.assertTrue(gateway_view.click_inline_new_policy(self.cases.case_data['destination']),
                        "Failed to click inline Add New button for policy")
        time.sleep(2)
        self.logger.info("Click inline Cancel button")
        self.assertTrue(gateway_view.click_inline_cancel(""),"Failed to click inline Cancel button for policy")
        self.cases.end_test("test_case_5")

        time.sleep(2)
        self.cases.start_test("test_case_6")
        self.logger.info("Click Save button to deploy the policies")
        self.assertTrue(gateway_view.save_deploy_policies_button.clicking(self.driver),"Failed to click Save button to deploy the policies")
        self.logger.info("Check the toaster message")
        result = actions_in_common.get_message()
        self.assertEqual(self.cases.case_data['gateway_name']+self.cases.expected_result['toaster'], result, "Failed to save the security policies")
        actions_in_common.close_message()
        self.cases.end_test("test_case_6")

        time.sleep(2)
        self.cases.start_test("test_case_7")
        self.logger.info("Click inline delete button")
        self.assertTrue(gateway_view.delete_saved_policy(self.cases.case_data['destination1']),"Failed to click delete button")
        self.logger.info("Verify the policy cannot be found in Security Policy table")
        self.assertFalse(gateway_view.policy_table.is_data_present(self.driver,2,self.cases.case_data['destination1']),"Unexpectedly found the policy")
        time.sleep(2)
        self.assertTrue(gateway_view.delete_saved_policy(self.cases.case_data['destination2']),
                        "Failed to click delete button")
        self.assertFalse(gateway_view.policy_table.is_data_present(self.driver, 2, self.cases.case_data['destination2']),
                         "Unexpectedly found the policy")
        self.logger.info("Save the changes")
        self.assertTrue(gateway_view.save_deploy_policies_button.clicking(self.driver),
                        "Failed to click Save button to deploy the policies")
        time.sleep(5)
        self.cases.end_test("test_case_7")
        """
        time.sleep(2)
        self.logger.info("Click the button Reset to Default")
        self.assertTrue(gateway_view.reset_policy_button.clicking(self.driver)),"failed to click the button to reset the security policy"

        time.sleep(3)
        self.logger.info("Clicking OK to delete all security policies...")
        actions_in_common.confirm_delete()
        self.logger.info("Check the toaster message")
        result = actions_in_common.get_message()
        self.assertIn("security policy rules have been reset. User needs to re-configure all the security policy rules, and VPC peering pairs for this VPC", result, "Failed to reset the security policy")
        actions_in_common.close_message()

        """





