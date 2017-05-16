import unittest, logging, time
from selenium import webdriver
import tests.UCC.UCCWebUI.lib.webui_pages.gateway as pages
from tests.UCC.UCCWebUI.testsuites.webuitest import *

class ConfigurationTests(WebUITest):

    def test01_public_ip_dispaly(self):
        actions_in_common = pages.ActionsInCommon(self.driver)
        openvpn_view = pages.OpenVPN(self.driver)

        self.logger.info("Expanding OpenVPN...")
        openvpn_view.expand_openvpn()

        self.logger.info("Navigating to Configuration...")
        openvpn_view.configuration()
        time.sleep(15)
        self.logger.info("Checking if Public IP Display Panel is present in the current view area...")
        assert openvpn_view.is_public_ip_display_panel_present(), "Public IP Display Panel is not present"

        self.logger.info("Check the current status for Public IP display: " )
        status = openvpn_view.check_config_status("public ip display")
        if status and status == "Disabled":
            self.logger.info("Enable Public IP Dispaly")
            self.assertTrue(openvpn_view.click_to_change_status("public ip display"), "Failed to click Public IP dispaly status")
        #TODO : Currently this takes forever for UI to return. Can't continue without the fix

        status = openvpn_view.check_config_status("public ip display")
        if status and status == "Enabled":
            self.logger.info("Disable Public IP display")
            self.assertTrue(openvpn_view.click_to_change_status("public ip display"),"Failed to click Public IP dispaly status")

            actions_in_common.confirm_delete()
            self.logger.info("Check the result of changing status for Public IP disaplay")
            result = actions_in_common.get_message()
            self.assertIn("Success", result, "Fail to disable Public IP display")
            actions_in_common.close_message()
        else:
            self.logger.error("Can't find current status. Abort.")

    def test02_geo_vpn(self):
        actions_in_common = pages.ActionsInCommon(self.driver)
        openvpn_view = pages.OpenVPN(self.driver)
        time.sleep(10)
        openvpn_view.select_geo_vpn_cloud_type = "AWS"
        self.assertEqual(openvpn_view.select_geo_vpn_cloud_type,"AWS","Failed to set the cloud type for Geo VPN")

        status = openvpn_view.check_config_status("geo vpn")
        if status and status == "Disabled":
            self.logger.info("Enable Geo VPN")
            self.assertTrue(openvpn_view.click_to_change_status("geo vpn"),
                            "Failed to click Geo VPN status")
            self.assertTrue(openvpn_view.is_geo_vpn_enable_panel_present(),"Failed to find Geo VPN Enable panel")
            time.sleep(5)
            self.logger.info("Input Account Name")
            openvpn_view.select_geo_vpn_account_name = "ucc-101"
            time.sleep(5)
            self.logger.info("Input Domain Name")
            openvpn_view.geo_vpn_domain_name = "avtxautotest.com"
            time.sleep(5)
            self.logger.info("Input Service Name")
            openvpn_view.geo_vpn_service_name = "geoautoservice"
            self.logger.info("Select ELB DNS Name")
            openvpn_view.select_geo_vpn_elb_dns_name = ""

            self.assertTrue(actions_in_common.click_ok_button(), "Could not click OK to enable Geo VPN")

        status = openvpn_view.check_config_status("geo vpn")
        if status and status == "Enabled":
            self.loggger.info("Disable Ge VPN")
            self.assertTrue(openvpn_view.click_to_change_status("geo vpn"),
                            "Failed to click Geo VPN status")

            #TODO check the result







