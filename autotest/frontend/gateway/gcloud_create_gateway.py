import unittest, logging, time
from selenium import webdriver
import tests.UCC.UCCWebUI.lib.webui_pages.gateway as pages
from tests.UCC.UCCWebUI.testsuites.webuitest import *


class CreateGCloudGateway(WebUITest):

    def test01_create_gcloud_gateway_no_vpn(self):
        #from tests.main import variables as _variables

        gateway_view = pages.Gateway(self.driver)
        actions_in_common = pages.ActionsInCommon(self.driver)
        time.sleep(10)

        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(10)
        self.logger.info("Checking Gateway is present in the current view area...")
        self.assertTrue(gateway_view.is_gateway_table_present(), "Gateway view is not present")

        self.logger.info("Clicking New Gateway button")
        gateway_view.click_new_gateway_button()

        self.assertTrue(gateway_view.new_gateway_panel_is_present(),"New Gateway panel is not found")

        """
        Create a new gcloud gateway in us-central-1 and disable VPN access
        """
        time.sleep(5)
        self.logger.info("select Cloud Type Gcloud")
        gateway_view.select_cloud_type = "Gcloud"
        time.sleep(20)

        self.logger.info ("Select VPC ID")
        gateway_view.select_vpc_id = "gc-auto-1"

        time.sleep(15)
        self.logger.info("Input new gateway name...")
        gateway_view.gateway_name = "gc-cus-1"

        self.logger.info("Select Gcloud Zone")
        gateway_view.select_zone =  "us-central1-b"
        time.sleep(10)
        try:
            self.logger.info("Deselecting VPN access...")
            time.sleep(5)
            gateway_view.check_vpn_access = "deselect"

        except:
            self.logger.exception("Could not disable VPN access")
        self.assertFalse(gateway_view.check_vpn_access)

        """
        try:
            self.logger.info("Current Enable ELB setting is "+ gateway_view.enable_elb)
            self.logger.info("Trying to disable ELB for this new Gateway")
            time.sleep(5)
            gateway_view.enable_elb = "no"
        except:
            self.logger.error("Could not disable ELB")
        self.assertEqual(gateway_view.enable_elb, "No", "Could not disable ELB")
        """

        time.sleep(5)
        self.logger.info("Clicking OK to create New Gateway...")
        self.assertTrue(actions_in_common.click_ok_button(), "Failed to click OK for new gateway")

        time.sleep(5)
        self.logger.info("Checking the result of creating new gateway...it takes a while")
        result = actions_in_common.get_message()
        self.assertIn("Successfully created Gateway",result,"Fail to create a new gateway")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Checking new gateway's state in gateway table")
        self.assertEquals(gateway_view.gateway_table.check_specific_row_data(self.driver,"gc-cus-1",2),"up", "Gateway state is not up.")

    def test02_create_gcloud_gateway_vpn_elb(self):
        gateway_view = pages.Gateway(self.driver)
        actions_in_common = pages.ActionsInCommon(self.driver)
        time.sleep(10)


        self.logger.info("Clicking New Gateway button")
        gateway_view.click_new_gateway_button()

        self.assertTrue(gateway_view.new_gateway_panel_is_present(), "New Gateway panel is not found")

        """
        Create a new gateway in us-east-1, VPN access: enabled, ELB: enabled, LDAP disabled.
        """

        time.sleep(10)
        self.logger.info("Select VPC ID")
        gateway_view.select_vpc_id = "gc-auto-2"
        time.sleep(10)
        self.logger.info("Input Gatewy Name")
        gateway_view.gateway_name = "gc-eus-1"
        time.sleep(3)
        self.logger.info("Select Gcloud Zone")
        gateway_view.select_zone = "us-east1-b"
        time.sleep(10)
        self.logger.info("Check VPN access")
        gateway_view.check_vpn_access = "select"

        time.sleep(5)
        self.logger.info("Input VPN CIDR Block")
        gateway_view.vpn_cidr = "192.168.7.0/24"

        self.logger.info("Disable split tunnel mode")
        gateway_view.enable_split_tunnel = 'no'
        time.sleep(5)
        self.logger.info("enable ELB")
        gateway_view.enable_elb = "yes"

        self.logger.info("Disable Client Certificate Sharing")
        gateway_view.enable_client_cert_sharing = 'no'

        time.sleep(5)
        self.logger.info("Disable LDAP")
        gateway_view.enable_ldap = "deselect"

        time.sleep(5)
        self.logger.info("Clicking OK to create New Gateway...")
        self.assertTrue(actions_in_common.click_ok_button(),"Failed to click OK for new gateway")

        time.sleep(5)
        self.logger.info("Checking the result of creating new gateway...it takes a while")
        result = actions_in_common.get_message()
        self.assertIn("Successfully created Gateway", result, "Fail to create a new gateway")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Checking new gateway's state in gateway table")
        self.assertEquals(gateway_view.gateway_table.check_specific_row_data(self.driver, "gc-eus-1", 2), "up",
                          "Gateway state is not up.")

    def test03_no_vpn_gateway_ha_resize(self):
        #from tests.main import variables as _variables

        gateway_view = pages.Gateway(self.driver)
        actions_in_common = pages.ActionsInCommon(self.driver)
        time.sleep(10)

        self.logger.info("check if the specified gateway exists...")
        self.assertTrue(gateway_view.gateway_table.is_data_present(self.driver, 2, "gc-cus-1"),"Could not find the specified gateway")

        self.logger.info("Clicking on the gateway to edit it...")
        gateway_view.gateway_table.click_row_to_edit(self.driver,'gc-cus-1')

        self.logger.info("Verifying if the edit panel is present for the specified gateway...")
        self.assertTrue(gateway_view.is_edit_panel_present("gc-cus-1"),"Edit panel is not present")

        time.sleep(10)
        self.logger.info("Select Backup Gateway Zone")
        gateway_view.select_backup_gateway_zone = "us-central1-c"
        time.sleep(3)
        self.logger.info("Clicking Enable HA button...")
        gateway_view.click_enable_ha()
        result = actions_in_common.get_message()
        self.assertIn("HA enable: Successfully completed",result,"Failed to enable HA")
        actions_in_common.close_message()
        self.logger.info("Give it some tiem to create the backup gateway...")
        time.sleep(60)
        self.logger.info("Click Force Switchover button")
        self.assertTrue(gateway_view.click_force_switchover(),"Failed to click Force Switchover")
        result = actions_in_common.get_message()
        self.assertIn("HA test: Successfully completed", result, "Failed to Force Switchover")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Try to resize the AWS gateway")
        gateway_view.select_gateway_resize = "n1-standard-1"
        time.sleep(5)
        self.logger.info('Click Change button')
        self.assertTrue(gateway_view.click_change_button(),"Failed to click Change button")
        time.sleep(5)
        result = actions_in_common.get_message()
        self.assertIn("Error: HA enabled gateway", result, "Unexpectedly resized the gateway")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Click Disable HA button")
        self.assertTrue(gateway_view.click_disable_ha(), "Failed to click Disable HA button")
        result = actions_in_common.get_message()
        self.assertIn("HA disable: Successfully completed ", result, "Failed to Disable HA")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Try to resize the AWS gateway")
        gateway_view.select_gateway_resize = "n1-standard-1"
        time.sleep(3)
        self.logger.info('Click Change button')
        self.assertTrue(gateway_view.click_change_button(), "Failed to click Change button")
        time.sleep(5)
        result = actions_in_common.get_message()
        self.assertIn("Successfully updated gateway size", result, "Failed to resize the gateway")
        actions_in_common.close_message()

        self.logger.info("Close Edit panel")
        self.assertTrue(actions_in_common.cancel_edit(),"Failed to close Gateway Edit panel")


    def test04_vpn_gateway_ha_resize(self):
        #these tests below are supposed to fail
        gateway_view = pages.Gateway(self.driver)
        actions_in_common = pages.ActionsInCommon(self.driver)
        time.sleep(15)

        self.logger.info("check if the specified gateway exists...")
        self.assertTrue(gateway_view.gateway_table.is_data_present(self.driver, 2, "gc-eus-1"),"Could not find the specified gateway")

        self.logger.info("Clicking on the gateway to edit it...")
        gateway_view.gateway_table.click_row_to_edit(self.driver,'gc-eus-1')
        time.sleep(10)
        self.logger.info("Verifying if the edit panel is present for the specified gateway...")
        self.assertTrue(gateway_view.is_edit_panel_present("gc-eus-1"),"Edit panel is not present")

        time.sleep(5)
        self.logger.info("Clicking Enable HA button...")
        gateway_view.click_enable_ha()
        result = actions_in_common.get_message()
        self.assertIn("Error: HA is not supported on VPN gateway",result,"Unexpectedly enabled HA")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Try to resize the AWS gateway")
        gateway_view.select_gateway_resize = "n1-standard-1"
        time.sleep(3)
        self.logger.info('Click Change button')
        self.assertTrue(gateway_view.click_change_button(),"Failed to click Change button")
        time.sleep(5)
        result = actions_in_common.get_message()
        self.assertIn("resizing is not supported", result, "Unexpectedly resized the gateway")
        actions_in_common.close_message()

        self.logger.info("Close Edit panel")
        self.assertTrue(actions_in_common.cancel_edit(), "Failed to close Gateway Edit panel")

    def test05_delete_gateway(self):
        gateway_view = pages.Gateway(self.driver)
        actions_in_common = pages.ActionsInCommon(self.driver)
        time.sleep(15)

        self.logger.info("check if the specified gateway exists...")
        self.assertTrue(gateway_view.gateway_table.is_data_present(self.driver,2,"gc-cus-1"),"Could not find the specified gateway")

        self.logger.info("Try to click Delete button of the specified gateway...")
        self.assertTrue(gateway_view.delete_gateway("gc-cus-1"),"Failed to click Delete button for the gateway")
        time.sleep(10)
        self.logger.info("Cancel to delete gateway...")
        actions_in_common.cancel_delete()
        time.sleep(10)
        self.logger.info("Delete the specified gateway...")
        self.assertTrue(gateway_view.delete_gateway("gc-cus-1"), "Failed to click Delete button for the gateway")

        time.sleep(10)
        self.logger.info("Clicking OK to delete the specified gateway...")
        actions_in_common.confirm_delete()

        time.sleep(5)
        self.logger.info("Checking the result of deleting gateway...it takes a while")
        result = actions_in_common.get_message()
        self.assertIn("deleted successfully", result, "Failed to delete the gateway")

        time.sleep(10)
        self.logger.info("Verifying deleted gateway is no longer in gateway list")
        self.assertFalse(gateway_view.gateway_table.is_data_present(self.driver, 2, "gc-cus-1"),"Found the specified gateway")
        actions_in_common.close_message()

    def test06_delete_gateway(self):
        gateway_view = pages.Gateway(self.driver)
        actions_in_common = pages.ActionsInCommon(self.driver)
        time.sleep(10)

        self.logger.info("check if the specified gateway exists...")
        self.assertTrue(gateway_view.gateway_table.is_data_present(self.driver,2,"gc-eus-1"),"Could not find the specified gateway")
        time.sleep(10)
        self.logger.info("Try to click Delete button of thje specified gateway...")
        self.assertTrue(gateway_view.delete_gateway("gc-eus-1"), "Failed to click Delete button for the gateway")

        time.sleep(10)
        self.logger.info("Clicking OK to delete the specified gateway...")
        actions_in_common.confirm_delete()

        time.sleep(5)
        self.logger.info("Checking the result of deleting gateway...it takes a while")
        result = actions_in_common.get_message()
        self.assertIn("deleted successfully ", result, "Failed to delete the gateway")

        time.sleep(10)
        self.logger.info("Verifying deleted gateway is no longer in gateway list")
        self.assertFalse(gateway_view.gateway_table.is_data_present(self.driver, 2, "gc-eus-1"),"Found the specified gateway")
        actions_in_common.close_message()