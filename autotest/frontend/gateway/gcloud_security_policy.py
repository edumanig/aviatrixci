import unittest, logging, time
from selenium import webdriver
import tests.UCC.UCCWebUI.lib.webui_pages.gateway as pages
from tests.UCC.UCCWebUI.testsuites.webuitest import *


class SecurityPolicy(WebUITest):

    def test_security_policy(self):
        gateway_view = pages.Gateway(self.driver)
        actions_in_common = pages.ActionsInCommon(self.driver)
        time.sleep(10)

        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(10)
        self.logger.info("Checking Gateway is present in the current view area...")
        self.assertTrue(gateway_view.is_gateway_table_present(), "Gateway view is not present")

        self.logger.info("Clicking on the gateway to edit it...")
        gateway_view.gateway_table.click_row_to_edit(self.driver, 'gc-wus-no-vpn-2')
        time.sleep(5)

        self.logger.info("Click Add New button for new Security Policy")
        self.assertTrue(gateway_view.new_security_policy_button.click_button(self.driver),"Failed to find Add New button for Security Policy")

        self.logger.info("Input Source")
        gateway_view.policy_src = "196.168.0.6"
        time.sleep(3)
        self.logger.info("Input Destination")
        gateway_view.policy_dst = "www.yahoo.com"
        time.sleep(3)
        self.logger.info("Select Policy Action")
        gateway_view.select_policy_action = "Deny"
        time.sleep(3)
        self.logger.info("Select Policy Packet logging")
        gateway_view.select_policy_packet_log = "on"
        self.logger.info("Click Save to save the policy")
        self.assertTrue(gateway_view.save_policy_input("www.yahoo.com"), "Failed to click the button to save the policy input")

        time.sleep(3)
        self.logger.info("Click inline Add New button for policy")
        self.assertTrue(gateway_view.click_inline_new_policy("www.yahoo.com"),"Failed to click inline Add New button for policy")

        time.sleep(3)
        self.logger.info("Click Save button to save and deploy the policies")
        self.assertTrue(gateway_view.save_deploy_policies_button.click_button(self.driver),"Failed to click Save button to deploy the policies")

        self.logger.info("Check the result of saving policies")
        result = actions_in_common.get_message()
        self.assertIn("Security policy rules have been updated", result, "Failed to save the security policies")
        actions_in_common.close_message()

        self.logger.info("Delete the saved policy")
        self.assertTrue(gateway_view.delete_saved_policy("www.yahoo.com"),"Failed to click delete button")

        time.sleep(3)
        self.logger.info("Click Reset to Default")
        self.assertTrue(gateway_view.reset_policy_button.click_button(self.driver)),"failed to click the button to reset the security policy"

        time.sleep(3)
        self.logger.info("Clicking OK to delete all security policies...")
        actions_in_common.confirm_delete()
        self.logger.info("Check the result of resetting the policy")
        result = actions_in_common.get_message()
        self.assertIn("security policy rules have been reset. User needs to re-configure all the security policy rules, and VPC peering pairs for this VPC", result, "Failed to reset the security policy")
        actions_in_common.close_message()







