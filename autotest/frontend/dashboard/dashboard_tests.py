import unittest, logging, time, os
from selenium import webdriver
import autotest.lib.webui_pages.dashboard as dashbd
import autotest.lib.webui_pages.gateway as gw
import autotest.lib.webui_pages.peering as pr
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases


class DashboardTests(WebUITest):
    cases = testcases(__name__)

    def test_gateways_on_map(self):
        dashboard = dashbd.Dashboard(self.driver)
        gateway_view = gw.Gateway(self.driver)
        peering = pr.Peering(self.driver)
        time.sleep(10)

        self.logger.info("Navigating to Gateway to fetch the gateway info")
        gateway_view.navigate_to_gateway()
        time.sleep(10)

        self.logger.info("Checking Gateway is present in the current view area...")
        self.assertTrue(gateway_view.is_gateway_table_present(), "Gateway view is not present")
        dashboard.gateway_list = gateway_view.gateway_table.get_column_data(self.driver,2)

        time.sleep(5)
        self.logger.info("Navigating to Peering to fetch the gateway info")
        peering.navigate_to_peering()
        time.sleep(5)
        peering.is_enc_peering_table_present()
        time.sleep(5)
        dashboard.peering_info, dashboard.total_enc_peering = peering.get_peering_data()

        self.logger.info("Navigating to Dashboard")
        dashboard.navigate_to_dashboard()
        time.sleep(10)
        self.cases.start_test("test_case_1")
        self.cases.expected_result['total_gateway_count'] = len(dashboard.gateway_list)/2
        self.logger.info("Checking the current gateways on map")
        self.assertTrue(dashboard.check_gateways(), "Not all gateways are displayed on map")
        self.assertEqual(len(dashboard.get_gateways()),self.cases.expected_result['total_gateway_count'],"Total gateway count is not correct")
        self.cases.end_test('test_case_1')
        self.cases.start_test("test_case_2")
        self.logger.info("Checking the current peering links on map")
        self.assertTrue(dashboard.check_peering_links(), "Not all peering tunnels are displayed on map")

        self.assertTrue(dashboard.check_peering_info(),"Peering info does not match between what's on map and the peering table.")
        self.cases.end_test("test_case_2")

    def test_vpn_user_table(self):
        dashboard = dashbd.Dashboard(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)

        self.logger.info('Checking the active VPN user...')
        self.cases.start_test("test_case_3")
        self.logger.info('Check the current total count of Active VPN User')
        count = dashboard.get_total_user_count()
        self.assertEqual(count, self.cases.expected_result['total_user_before'], "Total count of Active VPN User does not match")

        self.assertTrue(dashboard.vpn_user_table.is_data_present(self.driver,1,self.cases.case_data['active_user_name']),"VPN user is not found in VPN user table")
        self.logger.info('Checking the VPN session history of the user...')
        dashboard.vpn_user_table.click_row_to_edit(self.driver,self.cases.case_data['active_user_name'])
        time.sleep(5)
        self.assertTrue(dashboard.is_vpn_session_table_present(),"Failed to display VPN session history")

        self.logger.info("Dismissing the history panel...")
        dashboard.close_history_panel()
        time.sleep(5)
        self.assertFalse(dashboard.is_vpn_session_table_present(),"Failed to close the history panel")

        self.logger.info("Disconnecting the VPN user...")
        dashboard.discconect_vpn_user(self.cases.case_data['active_user_name'])
        self.assertTrue(actions_in_common.confirm_ok(),"Operation to delete is not confirmed")

        time.sleep(5)
        self.logger.info("Checking the result of disconnection...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'], result, "Fail to disconnect the VPN user session.")

        time.sleep(5)
        self.logger.info("Verifying the VPN user is no longer found in VPN user table")
        self.assertFalse(dashboard.vpn_user_table.is_data_present(self.driver, 1, self.cases.case_data['active_user_name']),"The VPN user is still active")
        actions_in_common.close_message()

        self.logger.info('Check the current total count of Active VPN User')
        count = dashboard.get_total_user_count()
        self.assertEqual(count, self.cases.expected_result['total_user_after'],
                         "Total count of Active VPN User does not match")
        self.cases.end_test("test_case_3")







