__author__ = 'Rong'
import unittest, logging, time
from selenium import webdriver
import tests.UCC.UCCWebUI.lib.webui_pages.vnet_diagnostic as pages
import datetime

class VnetDiagnostic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
            Copy from Sam's method
        """
        from tests.main import variables as _variables

        cls.logger = logging.getLogger(__name__)
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        gw_url = _variables["uccURL"]
        cls.driver.get(gw_url)
        UCCLogin = pages.UCCLogin(cls.driver)
        cls.logger.info("Checking if UCC web UI is loaded")
        cls.assertTrue(UCCLogin.match_page_tilte(),"UCC web UI is not loaded successfully")
        cls.logger.info("Checking if login page is loaded")
        cls.assertTrue(UCCLogin.is_login_form_present(),"Login page is not loaded successfully")
        cls.logger.info("Logging in UCC...")
        UCCLogin.login(_variables["login_username"],_variables["login_password"])
        cls.assertTrue(UCCLogin.check_for_controller(),
                       "Dashboard Page is loaded correctly")
        time.sleep(5)

    """
             Note:There a few things that needed to be changed for smooth run
             Please refer back to vnet_diagnostic_tests
             Also test_assert_cloud() is for Azure ARM only(so please change the UCC info
             accordingly


    """
    def test_assert_cloud(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Navigating to Troubleshooting")
        title = vnetdiagnostic_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title,
                         "Troubleshooting link does not exist")
        self.logger.info("Navigating to VNet Diagnostic")
        vnetdiagnostic_view.navigate_to_vnetdiagnostics()
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)
        """
        Azure ARM does not use this service, this checks for situation where service
        does not exist
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != "Azure ARM":
            try:
                vnetdiagnostic_view.select_cloud_type = "Azure ARM"
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             "Azure ARM",
                             "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != "azure":
            try:
                vnetdiagnostic_view.select_account_name = "azure"
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             "azure",
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "display_route"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "display_route"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["display_route"],
                             "VNet test does not exist.")
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(60)
        self.assertTrue(vnetdiagnostic_view.check_toaster_existence(),"Error:This cloud support cloud service,aborting the test")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),
                        "Close button does not exist")
        self.logger.info(
            "Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
            "Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                         "Toaster not closed")
        self.logger.info(
            "Toaster closed")



    def test_display_nonexiting_route_table_detail(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)
        """
        Type in a nonexisiting route table, should show an error toaster
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "route_table_details"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "route_table_details"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["route_table_details"],
                             "VNet test does not exist.")
        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name = "controller-e"
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(10)
        result = vnetdiagnostic_view.output_textarea
        self.assertNotIn("\"Location\"", result,
                      "Error:Test shown result,aborting this negative testing")
        vnetdiagnostic_view.click_close_button()
        time.sleep(5)

    def test_add_existing_route_table(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Navigating to Troubleshooting")
        title = vnetdiagnostic_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title,
                         "Troubleshooting link does not exist")
        self.logger.info("Navigating to VNet Diagnostic")
        vnetdiagnostic_view.navigate_to_vnetdiagnostics()
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                         "Not on the VNet Diagnostic page")
        time.sleep(10)
        """
        Add a route table that is already existing
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "add_route_table"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "add_route_table"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["add_route_table"],
                             "VNet test does not exist.")
        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name = "controller-n-eu"
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Current Location on dropdown menu  is : " + vnetdiagnostic_view.select_location)
        if vnetdiagnostic_view.select_location != _variables[
            "location"]:
            try:
                vnetdiagnostic_view.select_location = _variables[
                    "location"]
                self.logger.info(
                    "The location to be tested is:"
                    + vnetdiagnostic_view.select_location)
            except:
                self.logger.exception(
                    "Could not change to the selected location")
            self.assertEqual(vnetdiagnostic_view.select_location,
                             _variables["location"],
                             "Location does not exist.")
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                         "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(60)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug("The message shown is:%s", result)
        self.assertNotIn("Succeeded", result,
                      "Error:Route table added, aborting this negative testing")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),
                        "Close button does not exist")
        self.logger.info(
            "Close the toaster")
        self.logger.info(
            "Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
            "Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                         "Toaster not closed")
        self.logger.info(
            "Toaster closed")

    def test_delete_nonexisting_route_table(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Delete a route table that does not exist, should give erroneous message
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "delete_route_table"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "delete_route_table"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["delete_route_table"],
                             "VNet test does not exist.")
        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name = "controller-n"
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Check for the Go button")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button does exist and clicked")
        time.sleep(60)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug("The message shown is:%s", result)
        self.assertNotIn("Succeeded", result,
                      "Error:Successfully deleting the route table, aborting this negative testing")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),
                        "Close button does not exist")
        self.logger.info(
            "Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
            "Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                         "Toaster not closed")
        self.logger.info(
            "Toaster closed")

    def test_list_nonexisting_route_table(self):

        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        List a subnet and route table of an nonexisting route, will show error message
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "list_route_subnet"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "list_route_subnet"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["list_route_subnet"],
                             "VNet test does not exist.")
        self.logger.info(
            "Enter VNet name:")
        vnetdiagnostic_view.vnet_name = "controller-n-"
        self.logger.info(vnetdiagnostic_view.vnet_name)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist, proceed to click the Go button")
        time.sleep(10)
        result = vnetdiagnostic_view.output_textarea
        self.assertNotIn("\"AddressPrefix\"", result,
                            "Error:This VNet has ssociated subnet array,aborting the negative test")
        vnetdiagnostic_view.click_close_button()
        time.sleep(5)

    def test_list_nonexitence_effective_route(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)
        """
        List an non-exsting instance's effective route
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)
        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "list_effective_route"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "list_effective_route"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["list_effective_route"],
                             "VNet test does not exist.")
        self.logger.info(
            "Enter Instance ID:")
        vnetdiagnostic_view.instance_id = "instance-eu"
        self.logger.info(vnetdiagnostic_view.instance_id)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(10)
        result = vnetdiagnostic_view.output_textarea
        self.assertNotIn("\"EffectiveRoute\"", result, "Error:No route table associate with this instance")
        vnetdiagnostic_view.click_close_button()
        time.sleep(5)

    def test_add_route_to_nonexistence_route_table(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Add a route to a nonexisting route table,should have an erroneous message
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "add_route"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "add_route"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                            _variables["add_route"],
                             "VNet test does not exist.")
        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name = "controller-w-"
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Enter route name:")
        vnetdiagnostic_view.route_name = _variables["route_name"]
        self.logger.info(vnetdiagnostic_view.route_name)
        self.logger.info(
            "Enter CIDR:")
        vnetdiagnostic_view.cidr = _variables["cidr"]
        self.logger.info(vnetdiagnostic_view.cidr)
        self.logger.info(
            "Enter Next Hop IP:")
        vnetdiagnostic_view.next_hop_ip = _variables["next_hop_id"]
        self.logger.info(vnetdiagnostic_view.next_hop_ip)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        time.sleep(10)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug(
            "Toaster message:" + result)
        self.assertNotIn("Succeeded", result, "Error:Adding route is successful, aborting this negative testing")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),"Close button does not exist")
        self.logger.info(
                 "Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
                 "Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                              "Toaster not closed")
        self.logger.info(
              "Toaster closed")


    def test_add_route_to_route_table_with_weird_CIDR(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                         "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Add a route to a route table with weird CIDR,should show erroneous message
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "add_route"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "add_route"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["add_route"],
                             "VNet test does not exist.")
        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name = _variables["route_table_detail_name"]
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Enter route name:")
        vnetdiagnostic_view.route_name = _variables["route_name"]
        self.logger.info(vnetdiagnostic_view.route_name)
        self.logger.info(
            "Enter CIDR:")
        vnetdiagnostic_view.cidr = "10.0.0.0"
        self.logger.info(vnetdiagnostic_view.cidr)
        self.logger.info(
            "Enter Next Hop IP:")
        vnetdiagnostic_view.next_hop_ip = _variables["next_hop_id"]
        self.logger.info(vnetdiagnostic_view.next_hop_ip)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        time.sleep(10)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug(
            "Toaster message:" + result)
        self.assertNotIn("Succeeded", result, "Error:Successfully adding a route table,aborting the negative testing")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),"Close button does not exist")
        self.logger.info(
                 "Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
                 "Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                              "Toaster not closed")
        self.logger.info(
              "Toaster closed")

    def test_delete_route_of_route_table_with_nonexisting_route_table_name(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Delete a route of a route table with non-existing route table, might show error
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "delete_route"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "delete_route"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["delete_route"],
                             "VNet test does not exist.")
        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name = "controller-w-"
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Enter route name:")
        vnetdiagnostic_view.route_name = _variables["route_name"]
        self.logger.info(vnetdiagnostic_view.route_name)
        self.logger.info(
            "Check for the Go button")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button does exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug(
            "Toaster message:" + result)
        self.assertNotIn("Succeeded",result,"Error:Successfully deleting the route table, aborting the negative test")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),"Close button does not exist")
        self.logger.info(
                      "Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
                     "Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                                   "Toaster not closed")
        self.logger.info(
                   "Toaster closed")
    def test_delete_route_of_route_table(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Delete a route of a route table
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "delete_route"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "delete_route"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["delete_route"],
                             "VNet test does not exist.")
        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name = _variables["route_table_detail_name"]
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Enter route name:")
        vnetdiagnostic_view.route_name = "routes"
        self.logger.info(vnetdiagnostic_view.route_name)
        self.logger.info(
            "Check for the Go button")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button does exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug(
            "Toaster message:" + result)
        self.assertNotIn("Succeeded",result,"Error:Successfully deleting the route table, aborting the negative test")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),"Close button does not exist")
        self.logger.info(
                      "Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
                     "Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                                   "Toaster not closed")
        self.logger.info(
                   "Toaster closed")

    def test_turn_ip_fwd_on_nonexisting_instance(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                              "Not on the VNet Diagnostic page")
        time.sleep(10)
        """
        Turn IP fwd on for a nonexisting instance, will shown an erroneous message
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "turn_ip_on"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "turn_ip_on"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["turn_ip_on"],
                             "VNet test does not exist.")
        self.logger.info(
            "Enter Instance ID:")
        vnetdiagnostic_view.instance_id = "route"
        self.logger.info(vnetdiagnostic_view.instance_id)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.info(
            "Toaster message:" + result)
        self.assertNotIn("Succeeded", result, "Error:Successfully turned IP forward on, aborting this negative test")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),"Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                                        "Toaster not closed")
        self.logger.info(
                        "Toaster closed")

    def test_turn_ip_forward_off_on_nonexisting_instance(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Turn IP fwd off on nonexisting instance
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "turn_ip_off"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "turn_ip_off"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["turn_ip_off"],
                             "VNet test does not exist.")
        self.logger.info(
            "Enter Instance ID:")
        vnetdiagnostic_view.instance_id = "route"
        self.logger.info(vnetdiagnostic_view.instance_id)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.info(
            "Toaster message:" + result)
        self.assertNotIn("Succeeded", result, "Error:IP foward turned off, aborting this negative test")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),
                        "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
            "Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                         "Toaster not closed")
        self.logger.info(
            "Toaster closed")

    def test_get_ip_forward_of_non_existence_instance(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                             "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Get IP foward of a nonexisitng instance
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "get_ip_fwd"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "get_ip_fwd"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["get_ip_fwd"],
                             "VNet test does not exist.")
        self.logger.info(
            "Enter Instance ID:")
        vnetdiagnostic_view.instance_id = "route"
        self.logger.info(vnetdiagnostic_view.instance_id)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug(
            "Toaster message:" + result)
        self.assertFalse("abled" in result, "Error:Successfully getting the IP forward status, aborting the negative test")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),
                            "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                          "Toaster not closed")
        self.logger.info("Toaster closed")

    def test_associate_subnet_with_nonexistence_route_table(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                                 "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Associating subnet with a route table that does not exist
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")

        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")

        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "associate_subnet"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "associate_subnet"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["associate_subnet"],
                             "VNet test does not exist.")

        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name = "controller-n-"
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Enter VNet name:")
        vnetdiagnostic_view.vnet_name = _variables["associate_vnet_name"]
        self.logger.info(vnetdiagnostic_view.vnet_name)
        self.logger.info(
            "Enter subnet:")
        vnetdiagnostic_view.subnet = _variables["associate_vnet_subnet"]
        self.logger.info(vnetdiagnostic_view.subnet)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug(
            "Toaster message:" + result)
        self.assertNotIn("Succeeded", result, "Error:Successfully added route table, aborting the negative testing")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),
                                "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                             "Toaster not closed")
        self.logger.info("Toaster closed")

    def test_associate_subnet_with_vnet_name(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                                 "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Associating subnet with vnet that does not exist
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")

        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")

        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "associate_subnet"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "associate_subnet"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["associate_subnet"],
                             "VNet test does not exist.")

        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name = _variables["associate_vnet_route_table"]
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Enter VNet name:")
        vnetdiagnostic_view.vnet_name = "subnet-associate-"
        self.logger.info(vnetdiagnostic_view.vnet_name)
        self.logger.info(
            "Enter subnet:")
        vnetdiagnostic_view.subnet = _variables["associate_vnet_subnet"]
        self.logger.info(vnetdiagnostic_view.subnet)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug(
            "Toaster message:" + result)
        self.assertNotIn("Succeeded", result, "Error:Successfully adding route table, aborting the negative testing")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),
                                "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                             "Toaster not closed")
        self.logger.info("Toaster closed")

    def test_associate_existing_subnet(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Associating an existing associated subnet
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")

        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")

        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "associate_subnet"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "associate_subnet"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["associate_subnet"],
                             "VNet test does not exist.")

        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name = "controller-n-eu"
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Enter VNet name:")
        vnetdiagnostic_view.vnet_name = "controller-eu-existent-vnet"
        self.logger.info(vnetdiagnostic_view.vnet_name)
        self.logger.info(
            "Enter subnet:")
        vnetdiagnostic_view.subnet = "Subnet-2"
        self.logger.info(vnetdiagnostic_view.subnet)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug(
            "Toaster message:" + result)
        self.assertNotIn("Succeeded", result,
                         "Error:Successfully adding route table, aborting the negative testing")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),
                        "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
            "Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                         "Toaster not closed")
        self.logger.info("Toaster closed")

    def test_dissociate_subnet_with_nonexisting_route_table(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Dissociating subnet with a route table that does not exist
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")

        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")

        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "disociate_subnet"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "disociate_subnet"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["disociate_subnet"],
                             "VNet test does not exist.")

        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name ="controller-n"
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Enter VNet name:")
        vnetdiagnostic_view.vnet_name = _variables["associate_vnet_name"]
        self.logger.info(vnetdiagnostic_view.vnet_name)
        self.logger.info(
            "Enter subnet:")
        vnetdiagnostic_view.subnet = _variables["associate_vnet_subnet"]
        self.logger.info(vnetdiagnostic_view.subnet)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug(
            "Toaster message:" + result)
        self.assertNotIn("Succeeded", result, "Error:Successfully disassociating the route table, aborting the negative test")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),
                                "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                             "Toaster not closed")
        self.logger.info("Toaster closed")

    def test_dissociate_subnet_nonexistence_vnet(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Dissociating subnet from nonexisting vnet, should have errenous message
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")

        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")

        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "disociate_subnet"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "disociate_subnet"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["disociate_subnet"],
                             "VNet test does not exist.")

        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name = _variables[
            "associate_vnet_route_table"]
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Enter VNet name:")
        vnetdiagnostic_view.vnet_name = "subnet-associate-"
        self.logger.info(vnetdiagnostic_view.vnet_name)
        self.logger.info(
            "Enter subnet:")
        vnetdiagnostic_view.subnet = _variables["associate_vnet_subnet"]
        self.logger.info(vnetdiagnostic_view.subnet)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug(
            "Toaster message:" + result)
        self.assertNotIn("Succeeded", result,
                      "Error:Successfully dissociating route table,aborting the negative test")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),
                        "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
            "Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                         "Toaster not closed")
        self.logger.info("Toaster closed")

    def test_dissociate_subnet_with_a_nonexisting_subnet(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Dissociate subnet that does not exist
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")

        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")

        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "disociate_subnet"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "disociate_subnet"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["disociate_subnet"],
                             "VNet test does not exist.")

        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name = _variables[
            "associate_vnet_route_table"]
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Enter VNet name:")
        vnetdiagnostic_view.vnet_name = _variables["associate_vnet_name"]
        self.logger.info(vnetdiagnostic_view.vnet_name)
        self.logger.info(
            "Enter subnet:")
        vnetdiagnostic_view.subnet = "subnet"
        self.logger.info(vnetdiagnostic_view.subnet)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug(
            "Toaster message:" + result)
        self.assertNotIn("Succeeded", result,
                      "Error:Sucessfully dissociating the route table,aborting the negative test")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),
                        "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
            "Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                         "Toaster not closed")
        self.logger.info("Toaster closed")

    def test_dissociate_subnet_with_a_subnet_that_is_dissociated(self):
        from tests.main import variables as _variables
        vnetdiagnostic_view = pages.VNetDiagnostic(self.driver)
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(),
                        "Not on the VNet Diagnostic page")
        time.sleep(10)

        """
        Dissociate subnet that is already dissociated
        """
        self.logger.info(
            "Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != _variables[
            "cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = _variables[
                    "cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:"
                    + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception(
                    "Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type,
                             _variables["cloud_type"],
                             "Cloud type does not exist.")

        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")

        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != _variables[
            "disociate_subnet"]:
            try:
                vnetdiagnostic_view.select_test_type = _variables[
                    "disociate_subnet"]
                self.logger.info(
                    "The VNet test to be tested is:"
                    + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception(
                    "Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type,
                             _variables["disociate_subnet"],
                             "VNet test does not exist.")

        self.logger.info(
            "Enter route table name:")
        vnetdiagnostic_view.route_table_name = _variables[
            "associate_vnet_route_table"]
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info(
            "Enter VNet name:")
        vnetdiagnostic_view.vnet_name = _variables["associate_vnet_name"]
        self.logger.info(vnetdiagnostic_view.vnet_name)
        self.logger.info(
            "Enter subnet:")
        vnetdiagnostic_view.subnet = _variables["associate_vnet_subnet"]
        self.logger.info(vnetdiagnostic_view.subnet)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug(
            "Toaster message:" + result)
        self.assertNotIn("Succeeded", result,
                      "Error:Sucessfully dissociating the route table,aborting the negative test")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),
                        "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
            "Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster_existence(),
                         "Toaster not closed")
        self.logger.info("Toaster closed")

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()