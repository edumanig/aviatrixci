import unittest, logging, time
from selenium import webdriver
import tests.UCC.UCCWebUI.lib.webui_pages.gateway as pages
from tests.UCC.UCCWebUI.testsuites.webuitest import *

class GcloudENCTransitivePeering(WebUITest):

    def test01_create_enc_peering(self):
        peering_view = pages.Peering(self.driver)
        actions_in_common = pages.ActionsInCommon(self.driver)
        time.sleep(10)

        self.logger.info("Navigating to Peering")
        peering_view.navigate_to_peering()
        time.sleep(10)
        self.logger.info("Checking ENC peering is present in the current view area...")
        self.assertTrue(peering_view.is_enc_peering_table_present(), "Peering view is not present")

        self.logger.info("Clicking New Peering button")
        self.assertTrue(peering_view.click_new_enc_peering_button(),"Failed to click New ENC Peering buton")

        time.sleep(10)
        self.logger.info("Check if New ENC Peering Panel is present")
        self.assertTrue(peering_view.is_new_enc_peering_panel_present(),"Failed to find New ENC Peering panel")

        actions_in_common.description_of_test_case("Encrypted Peering: Both gateways are the same")
        self.logger.info("Select Gateway 1 for ENC peering")
        peering_view.select_vpc1 = "gc-wus-no-vpn-2"
        time.sleep(5)
        self.logger.info("Select Gateway 2 for ENC peering")
        peering_view.select_vpc2 = "gc-wus-no-vpn-2"
        time.sleep(5)

        self.logger.info("Click OK button to create a peering")
        self.assertTrue(actions_in_common.click_ok_button(), "Failed to click OK button for new ENC Peering")

        time.sleep(5)
        self.logger.info("Checking the result of creating the ENC peering...")
        result = actions_in_common.get_message()
        self.assertIn("Error: A VPC cannot peer to itself", result, "Unexpectedly created the ENC peering")
        actions_in_common.close_message()

        actions_in_common.description_of_test_case("Encrypted Peering: Create an Encrypted Peering successfully")
        self.logger.info("Select Gateway 1 for ENC peering")
        peering_view.select_vpc1 = "gc-wus-no-vpn-2"
        time.sleep(5)
        self.logger.info("Select Gateway 2 for ENC peering")
        peering_view.select_vpc2 = "gc-eus-no-vpn-1"
        time.sleep(5)

        self.logger.info("Click OK button to create a peering")
        self.assertTrue(actions_in_common.click_ok_button(),"Failed to click OK button for new ENC Peering")

        time.sleep(5)
        self.logger.info("Checking the result of creating the ENC peering...")
        result = actions_in_common.get_message()
        self.assertIn("have been peered. Bidirectional ping success.", result, "Fail to create the ENC peering")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Checking new ENC peering is found in ENC peering table")
        self.assertEqual(peering_view.enc_peering_table.check_specific_row_data(self.driver,"gc-wus-no-vpn-2",1),"gc-eus-no-vpn-1","Failed to find the ENC peering in the table")

    def test02_transitive_peering(self):
        peering_view = pages.Peering(self.driver)
        actions_in_common = pages.ActionsInCommon(self.driver)

        self.logger.info("Create a transitive peering")
        self.assertTrue(peering_view.click_transitive_peering_tab(), "Failed to navigate to Transitive Peering")

        time.sleep(10)
        self.logger.info("Click New Peering for Transitive peering")
        self.assertTrue(peering_view.click_new_transitive_peering_button()
                        , "Failed to click New Peering button for Transitive peering")

        time.sleep(5)
        self.logger.info("Check if new Transitive peering panel is present")
        self.assertTrue(peering_view.is_new_transitive_peering_panel_present(), "Failed to find New Transitive Panel")

        actions_in_common.description_of_test_case(
            "Transitive Peering: No ENC peering between source and nexthop gateways")
        self.logger.info("Select the source gateway")
        peering_view.select_source_gateway = "gc-wus-no-vpn-1"

        time.sleep(5)
        self.logger.info("Select Nexthop gateway")
        peering_view.select_nexthop_gateway = "gc-wus-no-vpn-2"

        time.sleep(5)
        self.logger.info("Input Destination CIDR")
        peering_view.destination_cidr = '10.100.0.0/20'

        self.logger.info("Click OK button to create a transitive peering")
        self.assertTrue(peering_view.click_new_transitive_peering_ok_button(),
                        "Failed to click OK button for new transitive Peering")

        time.sleep(5)
        self.logger.info("Checking the result of creating the Transitive peering...")
        result = actions_in_common.get_message()
        self.assertIn("are NOT peered", result, "Unexpectedly created the transitive peering")
        actions_in_common.close_message()

        time.sleep(5)
        actions_in_common.description_of_test_case(
            "Transitive Peering: No support for Transitive Peering on Gcloud")
        self.logger.info("Select the source gateway")
        peering_view.select_source_gateway = "gc-wus-no-vpn-2"

        time.sleep(5)
        self.logger.info("Select Nexthop gateway")
        peering_view.select_nexthop_gateway = "gc-eus-no-vpn-1"

        time.sleep(5)
        self.logger.info("Input Destination CIDR")
        peering_view.destination_cidr = '10.100.0.0/20'

        self.logger.info("Click OK button to create a transitive peering")
        self.assertTrue(peering_view.click_new_transitive_peering_ok_button(),
                        "Failed to click OK button for new transitive Peering")

        time.sleep(5)
        self.logger.info("Checking the result of creating the Transitive peering...")
        result = actions_in_common.get_message()
        self.assertIn("Error: Transitive peering not supported for Azure or ARM or Gcloud.", result, "Unexpectedly created the Transitive peering")
        actions_in_common.close_message()

    def test03_delete_enc_peering(self):
        peering_view = pages.Peering(self.driver)
        actions_in_common = pages.ActionsInCommon(self.driver)
        time.sleep(10)

        self.logger.info("Click Encrypted Peering tab")
        peering_view.click_enc_peering_tab()
        time.sleep(10)

        self.logger.info("Delete the ENC peering")
        self.assertTrue(peering_view.click_delete_enc_peering_button("gc-wus-no-vpn-2"),
                        "Failed to click the button for deleting the ENC peering")

        time.sleep(5)
        self.logger.info("Clicking OK to delete the specified peering...")
        actions_in_common.confirm_delete()

        self.logger.info("Checking the result of deleting the ENC peering")
        result = actions_in_common.get_message()
        self.assertIn("peer have been deleted", result, "Failed to delete the ENC peering")

        time.sleep(10)
        self.logger.info("Verifying deleted peering is no longer in ENC peering table")
        self.assertFalse(peering_view.enc_peering_table.is_data_present(self.driver, 1, "gc-wus-no-vpn-2"),
                         "Unexpectedly found the specified ENC peering")
        actions_in_common.close_message()