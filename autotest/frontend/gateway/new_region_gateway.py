import unittest, logging, time
from selenium import webdriver
import tests.UCC.UCCWebUI.lib.webui_pages.gateway as pages
from tests.UCC.UCCWebUI.testsuites.webuitest import *


class CreateGateway(WebUITest):

    def test01_create_aws_gateway_no_vpn(self):
        from tests.main import variables as _variables

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
        Create a new gateway in new region and disable VPN access
        """
        time.sleep(5)
        self.logger.info("select Cloud Type AWS")
        gateway_view.select_cloud_type = "AWS"
        time.sleep(5)
        gateway_view.select_region = "ap-south-1"

        time.sleep(10)

        gateway_view.select_vpc_id = "vpc-f937e590--aws-india"

        time.sleep(5)
        self.logger.info("Input new gateway name...")
        gateway_view.gateway_name = "aws-ind--no-vpn-2"

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
        self.assertEquals(gateway_view.gateway_table.check_specific_row_data(self.driver,"aws-ind--no-vpn-2",2),"up", "Gateway state is not up.")

    def test02_create_aws_gateway_vpn_elb(self):
        gateway_view = pages.Gateway(self.driver)
        actions_in_common = pages.ActionsInCommon(self.driver)
        time.sleep(15)

        self.logger.info("Clicking New Gateway button")
        gateway_view.click_new_gateway_button()

        self.assertTrue(gateway_view.new_gateway_panel_is_present(), "New Gateway panel is not found")

        """
        Create a new gateway in new region, VPN access: enabled, ELB: enabled, LDAP disabled.
        """

        time.sleep(10)
        self.logger.info("Select AWS Region")
        gateway_view.select_region = "ap-south-1"
        time.sleep(10)
        self.logger.info("Select VPC ID")
        gateway_view.select_vpc_id = "vpc-4cf63c25--aws-mumbai"
        time.sleep(10)
        self.logger.info("Input Gatewy Name")
        gateway_view.gateway_name = "aws-ind-vpn-elb-2"
        time.sleep(5)
        self.logger.info("Check VPN access")
        gateway_view.check_vpn_access = "select"

        time.sleep(5)
        self.logger.info("Input VPN CIDR Block")
        gateway_view.vpn_cidr = "192.168.0.0/20"

        time.sleep(10)
        self.logger.info("Enable ELB")
        try:
            self.logger.info("Current Enable ELB setting is "+ gateway_view.enable_elb)
            self.logger.info("Trying to enable ELB for this new Gateway")
            time.sleep(5)
            gateway_view.enable_elb = "yes"
        except:
            self.logger.error("Could not enable ELB")
            self.assertEqual(gateway_view.enable_elb, "No", "Could not enable ELB")

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
        self.assertEquals(gateway_view.gateway_table.check_specific_row_data(self.driver, "aws-ind-vpn-elb-2", 2), "up",
                          "Gateway state is not up.")

    def test03_no_vpn_gateway_ha_resize(self):
        #from tests.main import variables as _variables

        gateway_view = pages.Gateway(self.driver)
        actions_in_common = pages.ActionsInCommon(self.driver)
        time.sleep(10)

        self.logger.info("check if the specified gateway exists...")
        self.assertTrue(gateway_view.gateway_table.is_data_present(self.driver, 2, "aws-ind--no-vpn-2"),"Could not find the specified gateway")

        self.logger.info("Clicking on the gateway to edit it...")
        gateway_view.gateway_table.click_row_to_edit(self.driver,'aws-ind--no-vpn-2')

        self.logger.info("Verifying if the edit panel is present for the specified gateway...")
        self.assertTrue(gateway_view.is_edit_panel_present("aws-ind--no-vpn-2"),"Edit panel is not prensent")

        time.sleep(10)
        self.logger.info("Checking the details of the gateway")
        self.assertIn("VPC Name: aws-ind--no-vpn-2",gateway_view.show_gateway_details(), "Failed to show the details of the gateway.")

        self.logger.info("Clicking Enable HA button...")
        gateway_view.click_enable_ha()
        result = actions_in_common.get_message()
        self.assertIn("is HA enabled",result,"Failed to enable HA")
        actions_in_common.close_message()

        time.sleep(90)
        self.logger.info("Click Force Switchover button")
        self.assertTrue(gateway_view.click_force_switchover(),"Failed to click Force Switchover")
        result = actions_in_common.get_message()
        self.assertIn("has been switched over to the backup Gateway", result, "Failed to Force Switchover")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Try to resize the AWS gateway")
        gateway_view.select_gateway_resize = "m3.medium"
        time.sleep(5)
        self.logger.info('Click Change button')
        self.assertTrue(gateway_view.click_change_button(),"Failed to click Change button")
        time.sleep(5)
        result = actions_in_common.get_message()
        self.assertIn("Error: HA enabled gateway", result, "Unexpectedly resized the gateway")
        actions_in_common.close_message()

        time.sleep(5)
        self.logger.info("Click Disable HA button")
        self.assertTrue(gateway_view.click_disable_ha(), "Failed to click Disable HA button")
        result = actions_in_common.get_message()
        self.assertIn("is HA disabled", result, "Failed to Disable HA")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Try to resize the AWS gateway")
        gateway_view.select_gateway_resize = "t2.medium"
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
        time.sleep(10)

        self.logger.info("check if the specified gateway exists...")
        self.assertTrue(gateway_view.gateway_table.is_data_present(self.driver, 2, "aws-ind-vpn-elb-2"),"Could not find the specified gateway")

        self.logger.info("Clicking on the gateway to edit it...")
        gateway_view.gateway_table.click_row_to_edit(self.driver,'aws-ind-vpn-elb-2')
        time.sleep(10)
        self.logger.info("Verifying if the edit panel is present for the specified gateway...")
        self.assertTrue(gateway_view.is_edit_panel_present("aws-ind-vpn-elb-2"),"Edit panel is not prensent")
        time.sleep(10)
        self.logger.info("Clicking Enable HA button...")
        gateway_view.click_enable_ha()
        result = actions_in_common.get_message()
        self.assertIn("Error: HA is not supported on VPN gateway",result,"Unexpectedly enabled HA")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Try to resize the AWS gateway")
        gateway_view.select_gateway_resize = "m3.medium"
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
        time.sleep(10)

        self.logger.info("check if the specified gateway exists...")
        self.assertTrue(gateway_view.gateway_table.is_data_present(self.driver,2,"aws-ind--no-vpn-2"),"Could not find the specified gateway")

        self.logger.info("Try to click Delete button of the specified gateway...")
        self.assertTrue(gateway_view.delete_gateway("aws-ind--no-vpn-2"),"Failed to click Delete button for the gateway")
        time.sleep(10)
        self.logger.info("Cancel to delete gateway...")
        actions_in_common.cancel_delete()
        time.sleep(10)
        self.logger.info("Delete the specified gateway...")
        self.assertTrue(gateway_view.delete_gateway("aws-ind--no-vpn-2"), "Failed to click Delete button for the gateway")

        time.sleep(10)
        self.logger.info("Clicking OK to delete the specified gateway...")
        actions_in_common.confirm_delete()

        time.sleep(5)
        self.logger.info("Checking the result of deleting gateway...it takes a while")
        result = actions_in_common.get_message()
        self.assertIn("has been deleted.", result, "Failed to delete the gateway")

        time.sleep(10)
        self.logger.info("Verifying deleted gateway is no longer in gateway list")
        self.assertFalse(gateway_view.gateway_table.is_data_present(self.driver, 2, "aws-ind--no-vpn-2"),"Found the specified gateway")
        actions_in_common.close_message()

    def test06_delete_gateway(self):
        gateway_view = pages.Gateway(self.driver)
        actions_in_common = pages.ActionsInCommon(self.driver)
        time.sleep(10)

        self.logger.info("check if the specified gateway exists...")
        self.assertTrue(gateway_view.gateway_table.is_data_present(self.driver,2,"aws-ind-vpn-elb-2"),"Could not find the specified gateway")
        time.sleep(10)
        self.logger.info("Try to click Delete button of thje specified gateway...")
        self.assertTrue(gateway_view.delete_gateway("aws-ind-vpn-elb-2"), "Failed to click Delete button for the gateway")

        time.sleep(10)
        self.logger.info("Clicking OK to delete the specified gateway...")
        actions_in_common.confirm_delete()

        time.sleep(5)
        self.logger.info("Checking the result of deleting gateway...it takes a while")
        result = actions_in_common.get_message()
        self.assertIn("has been deleted.", result, "Failed to delete the gateway")

        time.sleep(10)
        self.logger.info("Verifying deleted gateway is no longer in gateway list")
        self.assertFalse(gateway_view.gateway_table.is_data_present(self.driver, 2, "aws-ind-vpn-elb-2"),"Found the specified gateway")
        actions_in_common.close_message()