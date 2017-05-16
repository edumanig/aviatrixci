import unittest, time
import autotest.lib.webui_pages.gateway as gw
import autotest.lib.webui_pages.openvpn as opvn
import autotest.lib.webui_pages.dashboard as dashbd
import autotest.lib.webui_pages.elb_diagnostic as elbdiag
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
import autotest.lib.backend_utils as backut
from autotest.lib.test_utils import delete_files_in_directory
from autotest.run_autotest import config
from autotest.lib.test_utils import testcases
from autotest.lib.vpc_utils import *

class OpenVPNE2E(WebUITest):
    cases = testcases(__name__)

    def test01_create_vpn_gateway(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        gateway_view = gw.Gateway(self.driver)

        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(10)

        self.logger.info("Clicking New Gateway button")
        gateway_view.click_new_gateway_button()
        time.sleep(2)

        self.cases.start_test("test_case_1")
        self.logger.info('Start to create a gateway with VPN access and LDAP enabled')
        assert gateway_view.fill_new_gateway_fields(
            **self.cases.case_data), "Failed to fill in Gateway configuration fields"

        time.sleep(1)
        self.logger.info("Clicking OK to create New Gateway...")
        self.assertTrue(actions_in_common.click_ok_button(), "Failed to click OK for new gateway")

        gateway_view.check_progress_box()
        self.logger.info("Checking the result of creating new gateway...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'] + self.cases.case_data['06.gateway_name'], result,
                      "Fail to create a new gateway")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Checking new gateway's state in gateway table")
        self.assertEquals(gateway_view.get_specific_gateway_row(self.cases.case_data["gateway_name"])[1],self.cases.expected_result["status"], "Gateway state is not up.")

        self.cases.end_test("test_case_1")

    def test02_create_vpn_user(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        openvpn_view = opvn.OpenVPN(self.driver)

        self.logger.info("Expanding OpenVPN...")
        openvpn_view.expand_openvpn()

        self.logger.info("Navigating to VPN Users...")
        openvpn_view.vpn_users()
        time.sleep(10)

        self.cases.start_test("test_case_2")
        self.logger.info("Clicking Add New button...")
        self.assertTrue(openvpn_view.click_add_button(), "Failed to find Add New button")
        time.sleep(3)

        self.logger.info("Start to fill new user form")
        openvpn_view.fill_new_user_form(**self.cases.case_data)

        time.sleep(3)
        self.logger.info("Click OK button")
        self.assertTrue(actions_in_common.click_ok_button(), "Failed to add a vpn user")

        self.logger.info("Checking the result of adding a vpn user...")
        result = actions_in_common.get_message()
        self.assertIn("has been added to", result, "Failed to add a vpn user")
        actions_in_common.close_message()

        time.sleep(5)
        self.logger.info("Check if the user is present in VPN user table")
        self.assertTrue(
            openvpn_view.user_table.is_data_present(self.driver, 1, self.cases.case_data['user_name']),
            "Failed to find the user in VPN user table")

        self.cases.end_test("test_case_2")

        self.logger.info("Enable the setting to display VPN client's Public IP address")
        self.cases.start_test("test_case_3")
        self.logger.info("Navigate to Configuration under OpenVPN")
        openvpn_view.configuration()
        time.sleep(5)
        cur_status = openvpn_view.check_config_status(self.cases.case_data["toggle_status"])
        self.logger.info("Current status of public IP display is {}".format(cur_status))
        if cur_status.lower() == "disabled":
            self.logger.info("Enabling the setting to display Access Public IP")
            openvpn_view.click_to_change_status(self.cases.case_data["toggle_status"])
            result = actions_in_common.get_message()
            self.assertEqual(self.cases.expected_result['toaster'], result, "Failed to enable public IP display")
            actions_in_common.close_message()
        else:
            self.logger.error('Public IP Display is enabled already.')

        self.cases.end_test("test_case_3")


    def test03_verify_openvpn_tunnel(self):
        ssh = backut.SSHCmd()
        self.cases.start_test('test_case_4')
        vpn_config_dir = os.path.abspath(config['download']['attachment_download'])
        delete_files_in_directory(vpn_config_dir)
        self.logger.info("Download OpenVPN configuration file from email attachment ...")
        file_path = download_openvpn_config(self.driver, self.logger,
                                            self.cases.case_data["user_email"],
                                            self.cases.case_data["email_password"])

        self.logger.info("Connect the instance/VM via SSH")
        ssh.ssh_connect(self.cases.case_data["client_ip"], self.cases.case_data["ssh_username"], self.cases.case_data["ssh_password"])

        self.logger.info("Upload the OpenVPN configuration file %s to OpenVPN client ...", file_path)
        openvpn_conf_remote_file = "/home/ubuntu/" + os.path.basename(file_path)
        self.assertTrue(ssh.upload_file(file_path, openvpn_conf_remote_file))
        time.sleep(15)
        ldap_auth = os.path.abspath(self.cases.case_data['auth_file'])
        remote_auth_file = "/home/ubuntu/" + os.path.basename(ldap_auth)
        self.logger.info("Upload the LDAP auth file %s to OpenVPN client ...", ldap_auth)
        self.assertTrue(ssh.upload_file(ldap_auth, remote_auth_file))
        time.sleep(15)

        self.logger.info("Launch OpenVPN client on instance/VM {}".format(self.cases.case_data['client_ip']))
        self.assertTrue(ssh.run_openvpn(openvpn_conf_remote_file, remote_auth_file))

        time.sleep(45)
        self.logger.info("Verify OpenVPN connection from instance/VM {}".format(self.cases.case_data['client_ip']))
        openvpn_log_path = self.cases.case_data['log_path']
        self.assertTrue(ssh.verify_by_log(openvpn_log_path, self.cases.expected_result['message']))
        time.sleep(15)

        self.logger.info("Ping the instance/VM {} behind the VPN Gateway".format(self.cases.case_data["target_ip"]))
        self.assertTrue(ssh.ping_private_ip_of_instance(self.cases.case_data["target_ip"]))

        self.logger.info("Ping the website {} to ensure it's the full tunnel".format(self.cases.case_data["target_website"]))
        self.assertTrue(ssh.ping_private_ip_of_instance(self.cases.case_data["target_website"]))

        ssh.ssh_disconnect()
        self.cases.end_test("test_case_4")

    def test04_verify_vpn_user_on_dashboard(self):
        dashboard = dashbd.Dashboard(self.driver)

        self.logger.info("Navigating to Dashboard")
        dashboard.navigate_to_dashboard()
        time.sleep(10)
        self.logger.info('Verify the VPN user is displayed in Active VPN Users')
        self.cases.start_test("test_case_5")
        self.assertTrue(
            dashboard.vpn_user_table.is_data_present(self.driver, 1, self.cases.case_data['active_user_name']),
            "VPN user is not found in VPN user table")
        self.logger.info('Verify the landing gateway is correct')
        self.assertEqual(dashboard.vpn_user_table.check_specific_row_data(self.driver,self.cases.case_data['active_user_name'],4),self.cases.expected_result['landing_gateway'])
        self.logger.info("Verify Access Public IP is correct")
        self.assertEqual(dashboard.vpn_user_table.check_specific_row_data(self.driver, self.cases.case_data['active_user_name'], 3),self.cases.expected_result['access_public_ip'])
        self.logger.info("Verify the Virtual IP is correct")
        self.assertEqual(dashboard.vpn_user_table.check_specific_row_data(self.driver,self.cases.case_data['active_user_name'],2),self.cases.expected_result['virtual_ip'])
        self.logger.info("Verify the Profile is correct")
        self.assertEqual(
            dashboard.vpn_user_table.check_specific_row_data(self.driver, self.cases.case_data['active_user_name'], 1),
            self.cases.expected_result['profile'])
        self.cases.end_test("test_case_5")

    def test05_verify_when_disconnected(self):
        ssh = backut.SSHCmd()
        dashboard = dashbd.Dashboard(self.driver)

        self.logger.info("Start to verify the results when the VPN is disconnected")
        self.cases.start_test("test_case_6")

        self.logger.info("Connect the instance/VM via SSH")
        ssh.ssh_connect(self.cases.case_data["client_ip"], self.cases.case_data["ssh_username"],
                        self.cases.case_data["ssh_password"])

        self.logger.info("Terminate the openvpn client on the remote host")
        self.assertTrue(ssh.terminate_openvpn())

        self.logger.info("Expect to fail Ping test with the instance/VM {} behind the VPN Gateway".format(self.cases.case_data["target_ip"]))
        self.assertFalse(ssh.ping_private_ip_of_instance(self.cases.case_data["target_ip"], retry=3))
        ssh.ssh_disconnect()

        self.logger.info("Verify the user is no longer displayed in Active VPN Users")
        time.sleep(10)
        self.assertFalse(
            dashboard.vpn_user_table.is_data_present(self.driver, 1, self.cases.case_data['active_user_name']),
            "VPN user is not found in VPN user table")

        self.cases.end_test("test_case_6")

    def test06_delete_vpn_user_gateway(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        gateway_view = gw.Gateway(self.driver)
        openvpn_view = opvn.OpenVPN(self.driver)

        self.logger.info("Disable Access Public IP on dashboard")
        self.cases.start_test("test_case_7")
        self.logger.info("Navigate to Configuration under OpenVPN")
        openvpn_view.configuration()
        time.sleep(5)
        self.logger.info("Disabling the setting to display Access Public IP")
        openvpn_view.click_to_change_status(self.cases.case_data["toggle_status"])
        actions_in_common.confirm_ok()
        result = actions_in_common.get_message()
        self.assertEqual(self.cases.expected_result['toaster'], result, "Failed to disable public IP display")
        actions_in_common.close_message()

        self.cases.end_test("test_case_7")

        self.logger.info("Navigating to VPN Users...")
        openvpn_view.vpn_users()
        time.sleep(5)
        self.cases.start_test("test_case_8")
        self.logger.info("Delete the VPN user {}".format(self.cases.case_data["user_name"]))
        self.assertTrue(openvpn_view.click_user_delete_button(self.cases.case_data["user_name"]), "Failed to click delete button")
        self.logger.info("Click OK to delete the user")
        self.assertTrue(actions_in_common.confirm_ok(), "Failed to confirm for deletion")

        self.logger.info("Checking the result of deleting the VPN user...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.case_data["user_name"]+ self.cases.expected_result["toaster"], result, "Failed to delete a VPN user")
        actions_in_common.close_message()
        time.sleep(5)
        self.logger.info("Verify if the user is removed from the user table")
        self.assertFalse(openvpn_view.user_table.is_data_present(self.driver, 1, self.cases.case_data["user_name"]))

        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(15)

        self.logger.info("Try to click Delete button of the specified gateway...")
        gateway_view.select_gateway_in_table(self.cases.case_data["gateway_name"])
        self.assertTrue(gateway_view.click_delete_button(), "Failed to click Delete button for the gateway")

        time.sleep(10)
        self.logger.info("Clicking OK to delete the specified gateway...")
        actions_in_common.confirm_ok()

        actions_in_common.wait_progress_bar()
        self.logger.info("Checking the result of deleting the gateway...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.case_data['gateway_name'] + self.cases.expected_result['toaster_gw'], result,
                      "Failed to delete the gateway")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Verifying deleted gateway is no longer in gateway list")
        self.assertFalse(gateway_view.is_gateway_present_in_table(self.cases.case_data["gateway_name"]),
                         "Found the specified gateway")

        self.cases.end_test("test_case_8")

    def test07_delete_elb(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        elb_diag = elbdiag.ELB_Diagnostic(self.driver)

        self.logger.info("Navigating to Troubleshooting")
        title = elb_diag.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title,
                         "Troubleshooting link does not exist")
        self.logger.info("Navigating to ELB Status")
        elb_diag.navigate_to_elb_status()
        self.logger.info("Check if ELB Status is the right page")
        self.assertTrue(elb_diag.current_url(), "Not on the ELB Status page")
        time.sleep(10)

        self.cases.start_test("test_case_9")
        self.logger.info("Check if the current account has ELB service")
        if elb_diag.check_toaster() == True:
            time.sleep(10)
            self.logger.info(
                "This cloud does not support ELB,closing the toaster...")
            self.assertTrue(
                elb_diag.click_toaster_close_button(),
                "Close button does not exist")
            self.logger.info(
                "Check for toaster to see if it is really closed,might shown exeptions")
            time.sleep(5)
            self.assertFalse(elb_diag.check_toaster(),
                             "Toaster not closed")
            self.logger.info(
                "Toaster closed")
        else:
            self.logger.info(
                "This cloud support ELB, moving on....")

        self.logger.info(
            "Current VPC/VNet name on dropdown menu is : " + elb_diag.select_vnet_name)
        if elb_diag.select_vnet_name != self.cases.case_data["vpc_id"]:
            try:
                elb_diag.select_vnet_name = self.cases.case_data["vpc_id"]
                self.logger.info("The VNet name to be deleted:" + elb_diag.select_vnet_name)
            except:
                self.logger.exception("Could not change to the selected VNet name")
            self.assertEqual(elb_diag.select_vnet_name, self.cases.case_data["vpc_id"],
                             "VNet does not exist")
        time.sleep(10)
        self.logger.info("Checking for ELB..will fail if no ELB is attached")
        self.assertTrue(elb_diag.is_lb_present(),
                        "There is no ELB attach with this VNet")
        lb_name = elb_diag.lb_name_information()
        self.logger.info("Information of the deleted ELB:" + lb_name)
        self.logger.info("Check for the delete button to delete the ELB..")
        self.assertTrue(elb_diag.click_delete_button(),
                        "Delete button does not exist")
        self.logger.info("Delete button exist and clicked")
        self.logger.info(
            "Check for pop up and assume pop up has the right message..")
        assert elb_diag.check_popup_exist, "No pop up is shown"

        self.logger.info("Pop up okay, click OK to start the process")
        self.assertTrue(elb_diag.click_pop_up_ok_button(),
                        "OK button does not exist")

        result = actions_in_common.get_message()
        self.assertEqual(self.cases.expected_result['toaster'], result, "Failed to enable public IP display")
        actions_in_common.close_message()

        self.cases.end_test("test_case_9")
