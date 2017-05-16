"""
Test scenario: New certificate for security concerns is addressed and is deployed to the gateways.
Upgrade to 121516.166 or later and disable the HTTPS cert
Downgrade to the latest release  112816 and create two gateways then upgrade to the current version 121516.
Then enable the HTTPS cert.
Cloud type tested: AWS, ARM and Gcloud
"""

import unittest, logging, time, os
from selenium import webdriver
from autotest.lib.webui_pages import upgrade as upgd
from autotest.lib.webui_pages import gateway
import autotest.lib.webui_pages.diagnostics as diag
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.lib.backend_utils import SSHCmd
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases

class SecurityWithCertificateTest(WebUITest):
    cases = testcases(__name__)

    def test01_upgrade_to_latest(self):
        upgrade_view = upgd.Upgrade(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)
        diagnostic_view = diag.Diagnostics(self.driver)
        relogin = actions.UCCLogin(self.driver)

        self.logger.info("Navigating to Settings")
        upgrade_view.navigate_to_settings()
        time.sleep(1)

        self.logger.info("Navigating to Upgrade")
        upgrade_view.navigate_to_upgrade()
        time.sleep(2)
        upgrade_view.check_upgrade_page()
        self.logger.info("At upgrade page")

        self.cases.start_test("test_case_1")
        self.logger.info("Upgrade to a custom release")
        upgrade_view.custom_version = self.cases.case_data["custom_version"]
        self.logger.info("Click Upgrade to Custom version")
        upgrade_view.click_custom_version_upgrade()

        actions_in_common.wait_progress_bar()
        time.sleep(3)
        self.logger.info("Sign in again to check the current version")
        relogin.login(self.cases.case_data['username'], self.cases.case_data["password"])
        time.sleep(6)

        self.logger.info("Check current version under Help")
        time.sleep(10)
        current_version = actions_in_common.get_current_version()
        self.logger.info("Current version is " + current_version)
        self.assertIn(self.cases.expected_result['custom_version'], current_version)

        self.logger.info("Navigating to Troubleshooting")
        title = diagnostic_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title, "Troubleshooting link does not exist")
        self.logger.info("Navigating to Diagnostic")
        diagnostic_view.navigate_to_diagnostics()
        self.logger.info("Check if Diagnostic is the right page")
        self.assertTrue(diagnostic_view.current_url(), "Not on the Diagnostic page")
        time.sleep(10)

        self.logger.info("Disable Security")
        diagnostic_view.change_security_setting("off")
        actions_in_common.wait_progress_bar()
        time.sleep(15)

        self.logger.info("Navigating to Settings")
        upgrade_view.navigate_to_settings()
        time.sleep(1)
        self.logger.info("Navigating to Upgrade")
        upgrade_view.navigate_to_upgrade()
        time.sleep(2)
        self.logger.info('Click Upgrade to the latest')
        upgrade_view.click_latest_version_upgrade()

        actions_in_common.wait_progress_bar()
        time.sleep(10)
        self.logger.info("Sign in again to check the current version")
        relogin.login(self.cases.case_data['username'], self.cases.case_data["password"])
        time.sleep(6)

        self.logger.info("Check current version under Help")
        time.sleep(10)
        current_version = actions_in_common.get_current_version()
        self.logger.info("Current version is " + current_version)
        self.assertIn(self.cases.expected_result['latest_version'], current_version)

        self.cases.end_test("test_case_1")

    def test02_create_2_gateways(self):
        gateway_view = gateway.Gateway(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)

        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(10)
        self.logger.info("Checking Gateway is present in the current view area...")
        self.assertTrue(gateway_view.is_gateway_table_present(), "Gateway view is not present")

        self.logger.info("Start to create 2 gateways for AWS, ARM and Gcloud respectively")
        self.cases.start_test("test_case_2")

        for gw in self.cases.case_data:
            self.logger.info("Click New Gateway button")
            gateway_view.click_new_gateway_button()
            time.sleep(5)
            self.assertTrue(gateway_view.new_gateway_panel_is_present(), "New Gateway panel is not found")

            assert gateway_view.fill_new_gateway_fields(**self.cases.case_data[gw]), "Failed to fill in Gateway configuration fields"

            time.sleep(1)
            self.logger.info("Clicking OK to create New Gateway...")
            self.assertTrue(actions_in_common.click_ok_button(), "Failed to click OK for new gateway")

            actions_in_common.wait_progress_bar()
            self.driver.refresh()
            time.sleep(15)
            self.logger.info("Checking new gateway's state in gateway table")
            self.assertEquals(gateway_view.gateway_table.check_specific_row_data(self.driver, self.cases.case_data[gw]['06.gateway_name'], 2), self.cases.expected_result['status'],
                              "Gateway state is not up.")

        self.cases.end_test("test_case_2")

    def test03_upgrade_to_preview(self):
        upgrade_view = upgd.Upgrade(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)
        relogin = actions.UCCLogin(self.driver)
        gateway_view = gateway.Gateway(self.driver)
        diagnostic_view = diag.Diagnostics(self.driver)
        sshc = SSHCmd()
        time.sleep(5)

        gateway_public_ip_addresses = {}

        self.logger.info("Navigating to Settings")
        upgrade_view.navigate_to_settings()
        time.sleep(1)

        self.logger.info("Navigating to Upgrade")
        upgrade_view.navigate_to_upgrade()
        time.sleep(2)

        self.cases.start_test("test_case_3")
        self.logger.info("Input the custom release version")
        upgrade_view.custom_version = self.cases.case_data["custom_version"]
        self.logger.info("Click Upgrade to Custom version")
        upgrade_view.click_custom_version_upgrade()

        actions_in_common.wait_progress_bar()
        time.sleep(3)
        self.logger.info("Sign in again to check the current version")
        relogin.login(self.cases.case_data['username'], self.cases.case_data["password"])
        time.sleep(6)

        self.logger.info("Check current version under Help")
        time.sleep(10)
        current_version = actions_in_common.get_current_version()
        self.logger.info("Current version is " + current_version)
        self.assertIn(self.cases.expected_result['custom_version'], current_version)

        self.logger.info("Start to verify the cert is not deployed because the setting is disabled")
        self.logger.info("Get the gateway's public IP")
        gateway_view.navigate_to_gateway()
        time.sleep(15)

        for gw_name in self.cases.case_data['gateway_names']:
            if "arm" in gw_name:
                column_no = 10
            else:
                column_no = 8
            self.logger.info(
                gw_name + "'s public IP is " + gateway_view.gateway_table.check_specific_row_data(self.driver, gw_name,
                                                                                                  column_no))
            gateway_public_ip_addresses[gw_name] = gateway_view.gateway_table.check_specific_row_data(self.driver,
                                                                                                      gw_name,
                                                                                                      column_no)


        self.logger.info("SSH connect Controller")
        hostip = self.cases.case_data['hostip']
        user = self.cases.case_data['ssh_user']
        passwd = self.cases.case_data['ssh_password']
        kf = os.path.abspath(self.cases.case_data['key_filename'])
        sshc.ssh_connect(hostip,user,passwd,kf)

        for gw, gw_ip in gateway_public_ip_addresses.items():
            to_gw = "wget --spider -S https://{} 2>&1 | grep 'insecurely'".format(gw_ip)
            cmd_putput1 = sshc.send_command(to_gw)
            self.logger.info(" output of the command: " + ''.join(cmd_putput1))
            self.assertIn(self.cases.expected_result['response'], cmd_putput1[0])
            scom = " wget --spider -S https://{} 2>&1 | grep 'insecurely'".format(hostip)
            if 'arm' in gw:
                keyname = gw + ".key"
            else:
                keyname = gw + ".pem"
            to_controller = "sudo ssh -o StrictHostKeyChecking=no -i /var/cloudx/{} ubuntu@{}".format(keyname,
                                                                                                      gw_ip) + scom
            cmd_putput2 = sshc.send_command(to_controller)
            self.logger.info(" output of the command: " + ''.join(cmd_putput2))
            self.assertIn(self.cases.expected_result['response'], cmd_putput2[0])

        self.logger.info("Start to test when the certificate is deployed")
        self.logger.info("Enable security with HTTPS certificate")

        self.logger.info("Navigating to Troubleshooting")
        title = diagnostic_view.navigate_to_troubleshooting()
        self.logger.info("Navigating to Diagnostic")
        diagnostic_view.navigate_to_diagnostics()
        time.sleep(10)

        self.logger.info("Enable Security")
        diagnostic_view.change_security_setting("on")
        time.sleep(20)
        actions_in_common.wait_progress_bar()
        time.sleep(15)

        for gw, gw_ip in gateway_public_ip_addresses.items():
            to_gw = "sudo wget --spider -S https://{} --certificate=/etc/ssl/certs/ctrl.crt --private-key=/etc/ssl/private/ctrl.key --ca-certificate=/etc/ssl/certs/ca.pem 2>&1 | grep HTTP/".format(gw_ip)
            cmd_output1 = sshc.send_command(to_gw)
            self.logger.info(" output of the command: " + ''.join(cmd_output1))
            self.assertIn(self.cases.expected_result['response_code'], cmd_output1[0])
            scom = " wget --spider -S https://{} 2>&1 | grep HTTP/".format(hostip)
            if 'arm' in gw:
                keyname = gw + ".key"
            else:
                keyname = gw + ".pem"
            to_controller = "sudo ssh -o StrictHostKeyChecking=no -i /var/cloudx/{} ubuntu@{}".format(keyname,
                                                                                                      gw_ip) + scom
            cmd_output2 = sshc.send_command(to_controller)
            self.logger.info(" output of the command: " + ''.join(cmd_output2))
            self.assertIn(self.cases.expected_result['response_code'], cmd_output2[0])

        self.logger.info("Start to delete those 2 gateways for AWS, ARM and Gcloud created for this test")
        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(10)

        for gw_name in self.cases.case_data['gateway_names']:
            gateway_view.delete_gateway(gw_name)
            time.sleep(3)
            self.logger.info("Clicking OK to delete the specified gateway...")
            actions_in_common.confirm_ok()

            actions_in_common.wait_progress_bar()
            self.driver.refresh()
            time.sleep(15)
            self.logger.info("Verifying deleted gateway is no longer in gateway list")
            self.assertFalse(gateway_view.gateway_table.is_data_present(self.driver, 2, gw_name),
                             "Found the specified gateway")
            time.sleep(5)

        self.cases.end_test("test_case_3")



