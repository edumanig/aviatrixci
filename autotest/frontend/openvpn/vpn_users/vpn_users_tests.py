import unittest, logging, time
from selenium import webdriver
import autotest.lib.webui_pages.openvpn as ov
import autotest.lib.webui_pages.gateway as gw
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases

class VPNUserSTests(WebUITest):
    cases = testcases(__name__)

    def test_new_vpn_user(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        openvpn_view = ov.OpenVPN(self.driver)
        gateway_view = gw.Gateway(self.driver)

        self.logger.info("Expanding OpenVPN...")
        openvpn_view.expand_openvpn()

        self.logger.info("Navigating to VPN Users...")
        openvpn_view.vpn_users()
        time.sleep(5)
        self.logger.info("Checking VPN user table is present in the current view area...")
        assert openvpn_view.is_user_table_present(), "VPN user table is not present"

        self.cases.start_test("test_case_1")
        for user in self.cases.case_data:
            self.logger.info("Clicking Add New button...")
            self.assertTrue(openvpn_view.click_add_button(),"Failed to find Add New button")
            time.sleep(3)
            self.logger.info("Checking if add user panel is present...")
            self.assertTrue(openvpn_view.is_add_user_panel_present(),"Failed to find Add User panel")

            self.logger.info("Start to fill new user form")
            openvpn_view.fill_new_user_form(**self.cases.case_data[user])

            time.sleep(3)
            self.logger.info("Click OK button")
            self.assertTrue(actions_in_common.click_ok_button(),"Failed to add a vpn user")

            self.logger.info("Checking the result of adding a vpn user...")
            result = actions_in_common.get_message()
            self.assertIn("has been added to", result, "Failed to add a vpn user")
            actions_in_common.close_message()

            time.sleep(5)
            self.logger.info("Check if the user is present in VPN user table")
            self.assertTrue(openvpn_view.user_table.is_data_present(self.driver,1,self.cases.case_data[user]['user_name']),"Failed to findthe user in VPN user table")
        self.cases.end_test("test_case_1")

        time.sleep(5)
        self.cases.start_test("test_case_2")
        self.logger.info("Re-issue the cert")
        self.assertTrue(openvpn_view.click_reissue_button(self.cases.case_data['user_name']),"Failed to click re-issue button")
        time.sleep(3)
        self.logger.info("Checking the result of re-issueing the cert...")
        result = actions_in_common.get_message()
        self.assertIn("and an email with certificate files will be sent to "+ self.cases.case_data["user_email"], result, "Failed to re-issue a VPN user")
        actions_in_common.close_message()
        self.cases.end_test("test_case_2")

        time.sleep(3)
        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(10)
        self.cases.start_test("test_case_3")
        self.logger.info("Trying to delete the gateway")
        gateway_view.delete_gateway(self.cases.case_data['gateway_name'])
        time.sleep(5)
        self.logger.info("Clicking OK to delete the specified gateway...")
        actions_in_common.confirm_ok()

        time.sleep(5)
        self.logger.info("Checking the result of deleting gateway...expect to see an error")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'],
                      result, "Unexpectedly deleted the gateway")

        time.sleep(5)
        self.logger.info("Verifying the gateway is still present in gateway list")
        self.assertTrue(gateway_view.gateway_table.is_data_present(self.driver, 2, self.cases.case_data['gateway_name']),
                        "Failed to find the specified gateway")
        actions_in_common.close_message()
        self.cases.end_test("test_case_3")

        time.sleep(3)
        self.logger.info("Navigating to VPN Users...")
        openvpn_view.vpn_users()
        time.sleep(5)
        self.cases.start_test("test_case_4")
        self.logger.info("Delete the vpn users")

        for u_name in self.cases.case_data['user_names']:

            self.assertTrue(openvpn_view.click_user_delete_button(u_name),"Failed to click delete button")
            self.logger.info("Click OK to delete {}".format(u_name))
            self.assertTrue(actions_in_common.confirm_ok(),"Failed to confirm for deletion")

            self.logger.info("Checking the result of deleting a VPN user...")
            result = actions_in_common.get_message()
            self.assertIn(u_name + self.cases.expected_result["toaster"], result, "Failed to delete a VPN user")
            actions_in_common.close_message()
            time.sleep(5)
            self.logger.info("Verify if the user is removed from the user table")
            self.assertFalse(openvpn_view.user_table.is_data_present(self.driver,1,u_name))

        self.cases.end_test("test_case_4")





