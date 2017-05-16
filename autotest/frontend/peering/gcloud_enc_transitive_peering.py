import unittest, logging, time
from selenium import webdriver
from autotest.lib.webui_pages import peering as prng
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases

class CreateENCPeering(WebUITest):
    cases = testcases(__name__)

    def test01_create_enc_peering(self):
        peering_view = prng.Peering(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)

        self.logger.info("Navigating to Peering")
        peering_view.navigate_to_peering()
        time.sleep(30)
        self.logger.info("Checking ENC peering is present in the current view area...")
        self.assertTrue(peering_view.is_enc_peering_table_present(), "Peering view is not present")

        self.logger.info("Clicking New Peering button")
        self.assertTrue(peering_view.click_new_enc_peering_button(),"Failed to click New ENC Peering buton")

        time.sleep(10)
        self.logger.info("Check if New ENC Peering Panel is present")
        self.assertTrue(peering_view.is_new_enc_peering_panel_present(),"Failed to find New ENC Peering panel")

        self.cases.start_test("test_case_1")
        self.logger.info("Select Gateway 1 for ENC peering")
        peering_view.select_vpc1 = self.cases.case_data['gateway1']
        time.sleep(3)
        self.logger.info("Select Gateway 2 for ENC peering")
        peering_view.select_vpc2 = self.cases.case_data['gateway2']
        time.sleep(3)

        self.logger.info("Click OK button to create a peering")
        self.assertTrue(actions_in_common.click_ok_button(), "Failed to click OK button for new ENC Peering")

        time.sleep(5)
        self.logger.info("Checking the result of creating the ENC peering...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'], result, "Unexpectedly created the ENC peering")
        actions_in_common.close_message()
        self.cases.end_test("test_case_1")

        self.cases.start_test("test_case_2")
        self.logger.info("Select Gateway 1 for ENC peering")
        peering_view.select_vpc1 = self.cases.case_data['gateway1']
        time.sleep(3)
        self.logger.info("Select Gateway 2 for ENC peering")
        peering_view.select_vpc2 = self.cases.case_data['gateway2']
        time.sleep(3)

        self.logger.info("Click OK button to create a peering")
        self.assertTrue(actions_in_common.click_ok_button(), "Failed to click OK button for new ENC Peering")

        time.sleep(5)
        self.logger.info("Checking the result of creating the ENC peering...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'], result, "Unexpectedly created the ENC peering")
        actions_in_common.close_message()
        self.cases.end_test("test_case_2")

        self.cases.start_test("test_case_3")
        self.logger.info("Select Gateway 1 for ENC peering")
        peering_view.select_vpc1 = self.cases.case_data['gateway1']
        time.sleep(3)
        self.logger.info("Select Gateway 2 for ENC peering")
        peering_view.select_vpc2 = self.cases.case_data['gateway2']
        time.sleep(3)

        self.logger.info("Click OK button to create a peering")
        self.assertTrue(actions_in_common.click_ok_button(),"Failed to click OK button for new ENC Peering")

        time.sleep(5)
        self.logger.info("Checking the result of creating the ENC peering...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'], result, "Fail to create the ENC peering")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Checking new ENC peering is found in ENC peering table")
        self.assertEqual(peering_view.enc_peering_table.check_specific_row_data(self.driver,self.cases.case_data['gateway1'],1),self.cases.case_data['gateway2'],"Failed to find the ENC peering in the table")
        self.cases.end_test("test_case_3")

    def test02_transitive_peering(self):
        peering_view = prng.Peering(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)

        self.logger.info("Create a transitive peering")
        self.assertTrue(peering_view.click_transitive_peering_tab(), "Failed to navigate to Transitive Peering")

        time.sleep(5)
        self.logger.info("Click New Peering for Transitive peering")
        self.assertTrue(peering_view.click_new_transitive_peering_button()
                        , "Failed to click New Peering button for Transitive peering")

        time.sleep(5)
        self.logger.info("Check if new Transitive peering panel is present")
        self.assertTrue(peering_view.is_new_transitive_peering_panel_present(), "Failed to find New Transitive Panel")

        self.cases.start_test("test_case_4")
        self.logger.info("Select the source gateway")
        peering_view.select_source_gateway = self.cases.case_data['source']

        time.sleep(5)
        self.logger.info("Select Nexthop gateway")
        peering_view.select_nexthop_gateway = self.cases.case_data['nexthop']

        time.sleep(5)
        self.logger.info("Input Destination CIDR")
        peering_view.destination_cidr = self.cases.case_data['destination_cidr']

        self.logger.info("Click OK button to create a transitive peering")
        self.assertTrue(peering_view.click_new_transitive_peering_ok_button(),
                        "Failed to click OK button for new transitive Peering")

        time.sleep(5)
        self.logger.info("Checking the result of creating the Transitive peering...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'], result, "Unexpectedly created the transitive peering")
        actions_in_common.close_message()
        self.cases.end_test('test_case_4')

        time.sleep(3)
        self.cases.start_test("test_case_5")
        self.logger.info("Select the source gateway")
        peering_view.select_source_gateway = self.cases.case_data['source']
        time.sleep(5)
        self.logger.info("Select Nexthop gateway")
        peering_view.select_nexthop_gateway = self.cases.case_data['nexthop']

        time.sleep(5)
        self.logger.info("Input Destination CIDR")
        peering_view.destination_cidr = self.cases.case_data['destination_cidr']

        self.logger.info("Click OK button to create a transitive peering")
        self.assertTrue(peering_view.click_new_transitive_peering_ok_button(),
                        "Failed to click OK button for new transitive Peering")

        time.sleep(5)
        self.logger.info("Checking the result of creating the Transitive peering...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'], result, "Fail to create the Transitive peering")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Checking new Transitive peering is found in Transitive peering table")
        self.assertEqual(peering_view.transitive_peering_table.check_specific_row_data(self.driver, self.cases.case_data['source'], 1),
                         self.cases.case_data['nexthop'], "Failed to find the Transitive peering in the table")
        self.cases.end_test("test_case_5")

        self.cases.start_test("test_case_6")
        self.logger.info("Delete the Transitive peering")
        self.assertTrue(peering_view.click_delete_transitive_peering_button(self.cases.case_data['source']),
                        "Failed to click the button for deleting the Transitive peering")

        time.sleep(5)
        self.logger.info("Clicking OK to delete the specified peering...")
        actions_in_common.confirm_ok()

        self.logger.info("Checking the result...")
        result = actions_in_common.get_message()
        self.assertIn("have been deleted", result, "Failed to delete the Transitive peering")

        time.sleep(10)
        self.logger.info("Verifying deleted peering is no longer in Transitive peering table")
        self.assertFalse(peering_view.transitive_peering_table.is_data_present(self.driver, 1, self.cases.case_data["source"]),
                         "Unexpectedly found the specified Transitive peering")
        actions_in_common.close_message()
        self.cases.end_test("test_Case_6")

    def test03_create_enc_peering_over_aws(self):
        peering_view = prng.Peering(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)

        self.logger.info("Start to test encrypted Peering with Over AWS Peering")
        peering_view.click_enc_peering_tab()
        time.sleep(5)

        self.cases.start_test("test_case_7")
        self.logger.info("Click New Peering button")
        self.assertTrue(peering_view.click_new_enc_peering_button(), "Failed to click New ENC Peering buton")

        time.sleep(5)
        self.logger.info("Check if New ENC Peering Panel is present")
        self.assertTrue(peering_view.is_new_enc_peering_panel_present(), "Failed to find New ENC Peering panel")

        self.logger.info("Select Gateway 1 for ENC peering")
        peering_view.select_vpc1 = self.cases.case_data["gateway1"]
        time.sleep(3)
        self.logger.info("Select Gateway 2 for ENC peering")
        peering_view.select_vpc2 = self.cases.case_data["gateway2"]
        time.sleep(3)

        self.logger.info("enable Over AWS Peering")
        peering_view.check_over_aws_peering = "select"

        self.logger.info("Click OK button to create a peering")
        self.assertTrue(actions_in_common.click_ok_button(), "Failed to click OK button for new ENC Peering over AWS Peering")

        self.logger.info("Checking the result of creating the ENC peering...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'], result, "Unexpectedly created the ENC peering over AWS Peering")
        actions_in_common.close_message()

        self.cases.end_test("test_case_7")

    def test04_delete_enc_peering(self):
        peering_view = prng.Peering(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)

        self.logger.info("Delete the ENC peering")
        self.cases.start_test("test_case_8")
        self.assertTrue(peering_view.click_delete_enc_peering_button(self.cases.case_data["gateway1"]),
                        "Failed to click the button for deleting the ENC peering")

        time.sleep(5)
        self.logger.info("Clicking OK to delete the specified peering...")
        actions_in_common.confirm_ok()

        self.logger.info("Checking the result of deleting the ENC peering")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result["toaster"], result, "Failed to delete the ENC peering")

        time.sleep(10)
        self.logger.info("Verifying deleted peering is no longer in ENC peering table")
        self.assertFalse(peering_view.enc_peering_table.is_data_present(self.driver, 1, self.cases.case_data["gateway1"]),
                         "Unexpectedly found the specified ENC peering")
        actions_in_common.close_message()

        self.cases.end_test("test_case_8")