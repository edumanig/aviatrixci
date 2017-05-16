import unittest, logging, time
from selenium import webdriver
import autotest.lib.webui_pages.gateway as gw
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases


class CreateGateway(WebUITest):
    cases = testcases(__name__)

    def test01_create_gcloud_gateway_no_vpn(self):
        gateway_view = gw.Gateway(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)
        time.sleep(30)

        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(10)
        self.logger.info("Checking Gateway is present in the current view area...")
        self.assertTrue(gateway_view.is_gateway_table_present(), "Gateway view is not present")

        self.logger.info("Clicking New Gateway button")
        gateway_view.click_new_gateway_button()

        self.assertTrue(gateway_view.new_gateway_panel_is_present(),"New Gateway panel is not found")
        self.cases.start_test("test_case_1")
        """
        Create a new gateway in us-west-2 and disable VPN access
        """
        time.sleep(5)
        self.logger.info("select Cloud Type Gcloud")
        gateway_view.select_cloud_type = self.cases.case_data["cloud_type"]

        time.sleep(10)
        if gateway_view.select_vpc_id != self.cases.case_data["vpc_id"]:
            try:
                gateway_view.select_vpc_id = self.cases.case_data["vpc_id"]
                self.logger.info("Selected VPC ID is " + gateway_view.select_vpc_id)
            except:
                self.logger.exception("Could not change the VPC ID")
            self.assertEqual(gateway_view.select_vpc_id, self.cases.case_data["vpc_id"], "VPC ID is not correct.")

        time.sleep(10)
        self.logger.info("Input new gateway name...")
        gateway_view.gateway_name = self.cases.case_data["gateway_name"]

        self.logger.info("Select Zone")
        gateway_view.select_zone = self.cases.case_data['zone']
        time.sleep(10)

        try:
            self.logger.info("Deselecting VPN access...")
            time.sleep(5)
            gateway_view.check_vpn_access = self.cases.case_data["vpn_access"]

        except:
            self.logger.exception("Could not disable VPN access")
        self.assertFalse(gateway_view.check_vpn_access)

        time.sleep(2)
        self.logger.info("Clicking OK to create New Gateway...")
        self.assertTrue(actions_in_common.click_ok_button(), "Failed to click OK for new gateway")

        actions_in_common.wait_progress_bar()
        self.logger.info("Checking the result of creating new gateway...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'], result, "Fail to create a new gateway")
        actions_in_common.close_message()
        time.sleep(15)
        self.logger.info("Checking new gateway's state in gateway table")
        self.assertEquals(gateway_view.gateway_table.check_specific_row_data(self.driver,self.cases.case_data["gateway_name"],2),self.cases.expected_result["status"], "Gateway state is not up.")
        self.cases.end_test("test_case_1")

    def test02_create_gcloud_gateway_vpn(self):
        gateway_view = gw.Gateway(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)
        time.sleep(10)

        self.logger.info("Clicking New Gateway button")
        gateway_view.click_new_gateway_button()

        self.assertTrue(gateway_view.new_gateway_panel_is_present(), "New Gateway panel is not found")
        self.cases.start_test("test_case_2")
        """
        Create a new gateway in eu-central-1, VPN access: enabled, ELB: disabled, LDAP disabled.
        """
        self.logger.info("select Cloud Type Gcloud")
        gateway_view.select_cloud_type = self.cases.case_data["cloud_type"]
        time.sleep(10)

        self.logger.info("Select VPC ID")
        gateway_view.select_vpc_id = self.cases.case_data["vpc_id"]
        time.sleep(10)
        self.logger.info("Input Gateway Name")
        gateway_view.gateway_name = self.cases.case_data["gateway_name"]
        time.sleep(2)
        self.logger.info("Check VPN access")
        gateway_view.check_vpn_access = self.cases.case_data["vpn_access"]

        time.sleep(5)
        self.logger.info("Input VPN CIDR Block")
        gateway_view.vpn_cidr = self.cases.case_data["vpn_cidr"]

        time.sleep(5)
        self.logger.info("Disable ELB")
        try:
            self.logger.info("Current Enable ELB setting is "+ gateway_view.enable_elb)
            self.logger.info("Trying to disable ELB for this new Gateway")
            time.sleep(5)
            gateway_view.enable_elb = self.cases.case_data["enable_elb"]
        except:
            self.logger.error("Could not disable ELB")
            self.assertEqual(gateway_view.enable_elb, "No", "Could not disable ELB")

        self.logger.info("Disable Client Certificate Sharing")
        gateway_view.enable_client_cert_sharing = self.cases.case_data['enable_client_cert_sharing']

        time.sleep(5)
        self.logger.info("Disable LDAP")
        gateway_view.enable_ldap = self.cases.case_data["enable_ldap"]

        time.sleep(5)
        self.logger.info("Clicking OK to create New Gateway...")
        self.assertTrue(actions_in_common.click_ok_button(),"Failed to click OK for new gateway")

        actions_in_common.wait_progress_bar()
        self.logger.info("Checking the result of creating new gateway...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'], result, "Fail to create a new gateway")
        actions_in_common.close_message()

        time.sleep(15)
        self.logger.info("Checking new gateway's state in gateway table")
        self.assertEquals(gateway_view.gateway_table.check_specific_row_data(self.driver, self.cases.case_data["gateway_name"], 2), self.cases.expected_result["status"],
                          "Gateway state is not up.")
        self.cases.end_test("test_case_2")

    def test03_no_vpn_gateway_ha_resize(self):

        gateway_view = gw.Gateway(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)

        self.logger.info("check if the specified gateway exists...")
        self.cases.start_test("test_case_3")
        self.assertTrue(gateway_view.gateway_table.is_data_present(self.driver, 2, self.cases.case_data["gateway_name"]),"Could not find the specified gateway")

        self.logger.info("Clicking on the gateway to edit it...")
        gateway_view.gateway_table.click_row_to_edit(self.driver,self.cases.case_data["gateway_name"])

        self.logger.info("Verifying if the edit panel is present for the specified gateway...")
        self.assertTrue(gateway_view.is_edit_panel_present(),"Edit panel is not prensent")

        time.sleep(10)
        self.logger.info("Checking the details of the gateway")
        self.assertIn(self.cases.expected_result["gateway_detail"]+self.cases.case_data["gateway_name"],gateway_view.show_gateway_details(), "Failed to show the details of the gateway.")

        self.logger.info("Select the backup zone for HA")
        gateway_view.select_backup_gateway_zone = self.cases.case_data['backup_zone']
        time.sleep(3)
        self.logger.info("Click Enable HA button")
        gateway_view.click_enable_ha()
        time.sleep(2)
        actions_in_common.confirm_ok()
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result["toaster_enable"], result, "Failed to enable HA")
        actions_in_common.close_message()

        time.sleep(90)
        self.logger.info("Click Force Switchover button")
        self.assertTrue(gateway_view.click_force_switchover(), "Failed to click Force Switchover")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result["toaster_switchover"], result, "Failed to Force Switchover")
        actions_in_common.close_message()

        self.cases.end_test("test_case_3")

        time.sleep(10)
        self.cases.start_test("test_case_4")
        self.logger.info("Try to resize the Gcloud gateway")
        gateway_view.select_gateway_resize = self.cases.case_data["resize"]
        time.sleep(5)
        self.logger.info('Click Change button')
        self.assertTrue(gateway_view.click_change_button(), "Failed to click Change button")
        time.sleep(5)
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result["toaster"], result, "Unexpectedly resized the gateway")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Click Disable HA button")
        self.assertTrue(gateway_view.click_disable_ha(), "Failed to click Disable HA button")
        time.sleep(2)
        actions_in_common.confirm_ok()
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result["toaster_disable"], result, "Failed to Disable HA")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Try to resize the Gcloud gateway")
        gateway_view.select_gateway_resize = self.cases.case_data["resize"]
        time.sleep(3)
        self.logger.info('Click Change button')
        self.assertTrue(gateway_view.click_change_button(), "Failed to click Change button")
        time.sleep(5)
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result["toaster_resize"], result, "Failed to resize the gateway")
        actions_in_common.close_message()

        self.logger.info("Close Edit panel")
        self.assertTrue(actions_in_common.cancel_edit(), "Failed to close Gateway Edit panel")
        self.cases.end_test("test_case_4")

    def test04_vpn_gateway_ha_resize(self):
        #these tests below are supposed to fail
        gateway_view = gw.Gateway(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)
        time.sleep(15)

        self.logger.info("check if the specified gateway exists...")
        self.cases.start_test("test_case_5")
        self.assertTrue(gateway_view.gateway_table.is_data_present(self.driver, 2, self.cases.case_data["gateway_name"]),"Could not find the specified gateway")

        self.logger.info("Clicking on the gateway to edit it...")
        gateway_view.gateway_table.click_row_to_edit(self.driver,self.cases.case_data["gateway_name"])
        time.sleep(10)
        self.logger.info("Verifying if the edit panel is present for the specified gateway...")
        self.assertTrue(gateway_view.is_edit_panel_present(),"Edit panel is not prensent")

        self.logger.info("Try to resize the Gcloud gateway")
        gateway_view.select_gateway_resize = self.cases.case_data["resize"]
        time.sleep(3)
        self.logger.info('Click Change button')
        self.assertTrue(gateway_view.click_change_button(),"Failed to click Change button")
        time.sleep(5)
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster_resize'], result, "Unexpectedly resized the gateway")
        actions_in_common.close_message()

        self.logger.info("Close Edit panel")
        self.assertTrue(actions_in_common.cancel_edit(), "Failed to close Gateway Edit panel")
        self.cases.end_test("test_case_5")

    def test05_delete_gateway(self):
        gateway_view = gw.Gateway(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)
        time.sleep(15)
        self.logger.info("Start to delete the gateways")

        self.cases.start_test("test_case_6")
        for gw_name in self.cases.case_data:
            self.logger.info("check if the specified gateway exists...")
            self.assertTrue(gateway_view.gateway_table.is_data_present(self.driver,2,self.cases.case_data[gw_name]),"Could not find the specified gateway")

            self.logger.info("Try to click Delete button of the specified gateway...")
            self.assertTrue(gateway_view.delete_gateway(self.cases.case_data[gw_name]),"Failed to click Delete button for the gateway")
            time.sleep(10)
            self.logger.info("Cancel to delete gateway...")
            actions_in_common.confirm_cancel()
            time.sleep(10)
            self.logger.info("Delete the specified gateway...")
            self.assertTrue(gateway_view.delete_gateway(self.cases.case_data[gw_name]), "Failed to click Delete button for the gateway")

            time.sleep(10)
            self.logger.info("Clicking OK to delete the specified gateway...")
            actions_in_common.confirm_ok()

            actions_in_common.wait_progress_bar()
            self.logger.info("Checking the toaster message")
            result = actions_in_common.get_message()
            self.assertIn(self.cases.expected_result['toaster'], result, "Fail to create a new gateway")
            actions_in_common.close_message()

            time.sleep(15)
            self.logger.info("Verifying deleted gateway is no longer in gateway list")
            self.assertFalse(gateway_view.gateway_table.is_data_present(self.driver, 2, self.cases.case_data[gw_name]),"Found the specified gateway")


        self.cases.end_test("test_case_6")