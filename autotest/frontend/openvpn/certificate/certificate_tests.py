import unittest, logging, time
from selenium import webdriver
import tests.UCC.UCCWebUI.lib.webui_pages.gateway as pages
from tests.UCC.UCCWebUI.testsuites.webuitest import *

class CertificateTests(WebUITest):

    def test01_import_certificates(self):
        actions_in_common = pages.ActionsInCommon(self.driver)
        openvpn_view = pages.OpenVPN(self.driver)
        time.sleep(10)
        self.logger.info("Expanding OpenVPN...")
        openvpn_view.expand_openvpn()
        time.sleep(5)
        self.logger.info("Navigating to Certificate...")
        openvpn_view.certificate()
        time.sleep(5)

        self.logger.info("Check if import panel is present")
        self.assertTrue(openvpn_view.is_import_panel_present(),"Failed to find import panel")

        time.sleep(5)
        self.logger.info("Input CA Certificate")
        openvpn_view.ca_cert = "/home/autopilot/CA.crt"
        time.sleep(5)
        self.logger.info("Input Server Certificate")
        openvpn_view.server_cert = "/home/autopilot/server.crt"
        time.sleep(5)
        self.logger.info("Input Server Private Key")
        openvpn_view.server_private_key = "/home/autopilot/server.key"
        #openvpn_view.crl_dist_uri = "http://"
        #openvpn_view.crl_update_interval = "20"

        time.sleep(5)
        self.logger.info('Click Import button')
        self.assertTrue(actions_in_common.click_ok_button(), "Failed to click to import certificate")

        time.sleep(5)
        self.logger.info("Checking the result of importing cert")
        result = actions_in_common.get_message()
        self.assertIn("Error: VPN gateways found. Please delete them before importing third-party certificates.", result, "Successfully imported cert")
        actions_in_common.close_message()

    def test02_download_vpn_config(self):
        actions_in_common = pages.ActionsInCommon(self.driver)
        openvpn_view = pages.OpenVPN(self.driver)
        time.sleep(10)

        self.logger.info("Check the download panel is present")
        self.assertTrue(openvpn_view.is_download_vpn_conf_panel_present(),"Failed to find the download panel")

        self.logger.info("Select VPC ID")
        openvpn_view.select_vpc_id = "vpc-1cbdac79"
        time.sleep(5)
        self.logger.info("Select LB name")
        openvpn_view.select_lb_name = "Aviatrix-vpc-1e163c790x3434840d"

        time.sleep(5)
        self.logger.info("Click Download button")
        self.assertTrue(openvpn_view.click_download_button(),"Failed to click Download button")