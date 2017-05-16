__author__ = 'Rong'
import unittest, logging, time
from selenium import webdriver
import autotest.lib.webui_pages.vnet_diagnostics as vnetdiag
import datetime
import platform
from autotest.run_autotest import config
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases


class VnetDiagnostic(WebUITest):
    cases = testcases(__name__)

    """
            Note:There a few things that needed to be changed for smooth run
            1)in config file:
              -uccURL
              -login_username
              -login_password(These only need to be change for once and the test should be able to run)
              -cloud_type(This support Azure classic only so you shouldn't be changing this)
              -azure_classic_account_name(Change to your account name)
              -route_table_detail_name(Change to a route table you have in your controller)
              -new_route_table_name(a new route table you want to add to your account,
              this would be delete in a latter step,so..)
              -location(location where you want this route table)
              -list_vnet_name(change to a VNet under your account)
             -instance_name(Instance on your account)
             -route_name(a new route you want to add in the route table,will be deleted in the latter process)
             -cidr(cidr block that goes with route_name)
             -next_hop_id(an ip address for route table)
             -associate_vnet_route_table(a route you want to associate a subnet with,will be dissociate in latter stage)
             -associate_vnet_name(name of the vnet of the subnet)
             -associate_vnet_subnet(name of the subnet )

        """
    def test03_all_route_table(self):
        vnetdiagnostic_view = vnetdiag.VNetDiagnostic(self.driver)

        time.sleep(2)
        """
        Choose display all route table and save the result
        """
        self.logger.info("Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)
        self.cases.start_test("test_case_3")
        """
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
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view. select_account_name)

        if vnetdiagnostic_view. select_account_name != _variables[
            "azure_classic_account_name"]:
            try:
                vnetdiagnostic_view. select_account_name = _variables[
                    "azure_classic_account_name"]
                self.logger.info(
                    "The account name to be tested is:"
                    + vnetdiagnostic_view. select_account_name)
            except:
                self.logger.exception(
                    "Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view. select_account_name,
                             _variables["azure_classic_account_name"],
                             "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)
        """
        if vnetdiagnostic_view.select_test_type != self.cases.case_data["display_route"]:
            try:
                vnetdiagnostic_view.select_test_type = self.cases.case_data["display_route"]
                self.logger.info("The VNet test to be tested is:" + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception("Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type, self.cases.case_data["display_route"], "VNet test does not exist.")
        self.logger.info("Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(), "Go button does not exist")
        self.logger.info("Go button exist and clicked")
        time.sleep(10)
        result = vnetdiagnostic_view.output_textarea
        self.assertIn("\"Name\"", result, "No route table associate with this cloud account")
        self.logger.info("Route Table Result:\n" + result)
        file_name = (
            'all_route_table_information_{:%Y%m%d-%H%M%S}.txt'.format(datetime.datetime.now()))
        if platform.system() == "Windows":
            save_path_file_name = "results\\temp\\" + file_name
        else:
            save_path_file_name = "results//temp//" + file_name
        route_table_result_file = open(save_path_file_name, "w")
        route_table_result_file.write(
            'Route table logged at: {:%Y-%m-%d %H:%M:%S}\n'.format(datetime.datetime.now()))
        route_table_result_file.write(result + "\n")
        route_table_result_file.close()
        self.logger.info("Route table result also saved at: " + save_path_file_name)
        vnetdiagnostic_view.click_close_button()
        time.sleep(5)

        self.cases.end_test("test_case_3")

    def test04_route_table_detail(self):
        vnetdiagnostic_view = vnetdiag.VNetDiagnostic(self.driver)
        time.sleep(2)
        """
        Choose display route table and detail
        """
        self.logger.info("Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)
        self.cases.start_test("test_case_4")
        """
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
        """
        if vnetdiagnostic_view.select_test_type != self.cases.case_data["route_table_details"]:
            try:
                vnetdiagnostic_view.select_test_type = self.cases.case_data["route_table_details"]
                self.logger.info("The VNet test to be tested is:" + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception("Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type, self.cases.case_data["route_table_details"], "VNet test does not exist.")
        self.logger.info("Enter route table name:")
        vnetdiagnostic_view.route_table_name = self.cases.case_data["new_route_table_name"]
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info("Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(), "Go button does not exist")
        self.logger.info("Go button exist and clicked")
        time.sleep(10)
        result = vnetdiagnostic_view.output_textarea
        self.assertIn(self.cases.expected_result["output"], result,
                      "No route table associate with this route table name")
        self.logger.info("Route Table Detail Result:\n" + result)
        file_name = ('route_table_details_{:%Y%m%d-%H%M%S}.txt'.format(datetime.datetime.now()))
        if platform.system() == "Windows":
            save_path_file_name = "results\\temp\\" + file_name
        else:
            save_path_file_name = "results//temp//" + file_name

        route_table_details_result_file = open(save_path_file_name, "w")
        route_table_details_result_file.write('Route table details logged at: {:%Y-%m-%d %H:%M:%S}\n'.format( datetime.datetime.now()))
        route_table_details_result_file.write(result + "\n")
        route_table_details_result_file.close()
        self.logger.info("Route table detail result also saved at: " + save_path_file_name)
        vnetdiagnostic_view.click_close_button()
        time.sleep(3)
        self.cases.end_test("test_case_4")

    def test01_add_route_table(self):
        vnetdiagnostic_view = vnetdiag.VNetDiagnostic(self.driver)

        self.logger.info("Navigating to Troubleshooting")
        title = vnetdiagnostic_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title, "Troubleshooting link does not exist")
        self.logger.info("Navigating to VNet Diagnostic")
        vnetdiagnostic_view.navigate_to_vnetdiagnostics()
        self.logger.info("Check if VNet Diagnostic is the right page")
        self.assertTrue(vnetdiagnostic_view.current_url(), "Not on the VNet Diagnostic page")
        time.sleep(10)
        """
        Add a route table
        """
        self.cases.start_test("test_case_1")
        self.logger.info("Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)

        if vnetdiagnostic_view.select_cloud_type != self.cases.case_data["cloud_type"]:
            try:
                vnetdiagnostic_view.select_cloud_type = self.cases.case_data["cloud_type"]
                self.logger.info(
                    "The cloud type to be tested is:" + vnetdiagnostic_view.select_cloud_type)
            except:
                self.logger.exception("Could not change to the selected cloud type")
            self.assertEqual(vnetdiagnostic_view.select_cloud_type, self.cases.case_data["cloud_type"], "Cloud type does not exist.")
        self.logger.info(
            "Current Account Name on dropdown menu  is : " + vnetdiagnostic_view.select_account_name)

        if vnetdiagnostic_view.select_account_name != self.cases.case_data["azure_classic_account_name"]:
            try:
                vnetdiagnostic_view.select_account_name = self.cases.case_data["azure_classic_account_name"]
                self.logger.info("The account name to be tested is:" + vnetdiagnostic_view.select_account_name)
            except:
                self.logger.exception("Could not change to the selected account name")
            self.assertEqual(vnetdiagnostic_view.select_account_name, self.cases.case_data["azure_classic_account_name"], "Account name does not exist.")
        self.logger.info(
            "Current VNet Test on dropdown menu  is : " + vnetdiagnostic_view.select_test_type)

        if vnetdiagnostic_view.select_test_type != self.cases.case_data["add_route_table"]:
            try:
                vnetdiagnostic_view.select_test_type = self.cases.case_data["add_route_table"]
                self.logger.info("The VNet test to be tested is:" + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception("Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type, self.cases.case_data["add_route_table"], "VNet test does not exist.")
        self.logger.info("Enter route table name:")
        vnetdiagnostic_view.route_table_name = self.cases.case_data["new_route_table_name"]
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info("Current Location on dropdown menu  is : " + vnetdiagnostic_view.select_location)
        if vnetdiagnostic_view.select_location != self.cases.case_data["location"]:
            try:
                vnetdiagnostic_view.select_location = self.cases.case_data["location"]
                self.logger.info("The location to be tested is:" + vnetdiagnostic_view.select_location)
            except:
                self.logger.exception("Could not change to the selected location")
            self.assertEqual(vnetdiagnostic_view.select_location, self.cases.case_data["location"], "Location does not exist.")
        self.logger.info("Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(), "Go button does not exist")
        self.logger.info("Go button exist and clicked")
        time.sleep(60)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug("The message shown is:%s", result)
        self.assertIn(self.cases.expected_result["toaster"], result, "Error adding the route table,please check the debug message")
        time.sleep(10)
        self.logger.info("Checking for toaster button, preparing to close toaster")
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(), "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info("Toaster closed")

        self.cases.end_test("test_case_1")

    def test13_delete_route_table(self):
        vnetdiagnostic_view = vnetdiag.VNetDiagnostic(self.driver)
        time.sleep(2)
        """
        Delete a route table
        """
        self.logger.info("Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)
        self.cases.start_test("test_case_13")
        """
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
        """
        if vnetdiagnostic_view.select_test_type != self.cases.case_data["delete_route_table"]:
            try:
                vnetdiagnostic_view.select_test_type = self.cases.case_data["delete_route_table"]
                self.logger.info("The VNet test to be tested is:" + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception("Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type, self.cases.case_data["delete_route_table"], "VNet test does not exist.")
        self.logger.info("Enter route table name:")
        vnetdiagnostic_view.route_table_name = self.cases.case_data["new_route_table_name"]
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info("Check for the Go button")
        self.assertTrue(vnetdiagnostic_view.click_go_button(), "Go button does not exist")
        self.logger.info("Go button does exist and clicked")
        time.sleep(60)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug("The message shown is:%s", result)
        self.assertIn(self.cases.expected_result["toaster"], result, "Error delete the route table,please check the debug message")
        time.sleep(10)
        self.logger.info("Check for close button for toaster")
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(), "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info("Toaster closed")
        self.cases.end_test("test_case_13")

    def test05_list_route_table(self):
        vnetdiagnostic_view = vnetdiag.VNetDiagnostic(self.driver)

        time.sleep(2)

        """
        List a subnet and route table
        """
        self.logger.info("Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)
        self.cases.start_test("test_case_5")
        """
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
        """
        if vnetdiagnostic_view.select_test_type != self.cases.case_data["list_route_subnet"]:
            try:
                vnetdiagnostic_view.select_test_type = self.cases.case_data["list_route_subnet"]
                self.logger.info("The VNet test to be tested is:" + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception("Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type, self.cases.case_data["list_route_subnet"], "VNet test does not exist.")
        self.logger.info("Enter VNet name:")
        vnetdiagnostic_view.vnet_name = self.cases.case_data["list_vnet_name"]
        self.logger.info(vnetdiagnostic_view.vnet_name)
        self.logger.info("Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(), "Go button does not exist")
        self.logger.info("Go button exist, proceed to click the Go button")
        time.sleep(10)
        result = vnetdiagnostic_view.output_textarea
        self.assertIn(self.cases.expected_result["output"], result, "This VNet has not associated subnet array")
        self.logger.info("Subnet Array:\n" + result)
        file_name = ('subnet_array_associate_route_table{:%Y%m%d-%H%M%S}.txt'.format(datetime.datetime.now()))
        if platform.system() == "Windows":
            save_path_file_name = "results\\temp\\" + file_name
        else:
            save_path_file_name = "results//temp//" + file_name
        route_table_subnet_result_file = open(save_path_file_name, "w")
        route_table_subnet_result_file.write(
            'Route table and associated subnet array logged at: {:%Y-%m-%d %H:%M:%S}\n'.format(datetime.datetime.now()))
        route_table_subnet_result_file.write(result + "\n")
        route_table_subnet_result_file.close()
        self.logger.info("Route table and associated subnet array result also saved at: " + save_path_file_name)
        vnetdiagnostic_view.click_close_button()
        time.sleep(5)
        self.cases.end_test("test_case_5")

    def test06_list_effective_route(self):
        vnetdiagnostic_view = vnetdiag.VNetDiagnostic(self.driver)
        time.sleep(2)
        """
        List a instance's effective route
        """
        self.logger.info("Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)
        self.cases.start_test("test_case_6")
        """
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
        """
        if vnetdiagnostic_view.select_test_type != self.cases.case_data["list_effective_route"]:
            try:
                vnetdiagnostic_view.select_test_type = self.cases.case_data["list_effective_route"]
                self.logger.info("The VNet test to be tested is:" + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception("Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type, self.cases.case_data["list_effective_route"], "VNet test does not exist.")
        self.logger.info("Enter Instance ID:")
        vnetdiagnostic_view.instance_id = self.cases.case_data["instance_name"]
        self.logger.info(vnetdiagnostic_view.instance_id)
        self.logger.info("Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(), "Go button does not exist")
        self.logger.info("Go button exist and clicked")
        time.sleep(10)
        self.logger.info("Check if this type of cloud could do this test,might show exception if no toaster is present...")
        self.assertFalse(vnetdiagnostic_view.output_toaster,"This type of cloud does not support this test")
        result = vnetdiagnostic_view.output_textarea
        self.assertNotIn(self.cases.expected_result["notinoutput"], result, "This instance is not deployed in a virtual network, please try with another instance")
        self.assertIn(self.cases.expected_result["output"], result, "No route table associate with this instance")
        self.logger.info("Subnet Array:\n" + result)
        file_name = ('instance_and_associated_route_table{:%Y%m%d-%H%M%S}.txt'.format(datetime.datetime.now()))
        if platform.system() == "Windows":
            save_path_file_name = "results\\temp\\" + file_name
        else:
            save_path_file_name = "results//temp//" + file_name
        route_table_subnet_result_file = open(save_path_file_name, "w")
        route_table_subnet_result_file.write('Instance route table logged at: {:%Y-%m-%d %H:%M:%S}\n'.format(datetime.datetime.now()))
        route_table_subnet_result_file.write(result + "\n")
        route_table_subnet_result_file.close()
        self.logger.info("Instance route table also saved at: " + save_path_file_name)
        vnetdiagnostic_view.click_close_button()
        time.sleep(5)
        self.cases.end_test("test_case_6")

    def test02_add_route_to_route_table(self):
        vnetdiagnostic_view = vnetdiag.VNetDiagnostic ( self.driver )

        time.sleep (2)
        """
        Add a route to a route table
        """
        self.logger.info("Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)
        self.cases.start_test("test_case_2")
        """
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
        """
        if vnetdiagnostic_view.select_test_type != self.cases.case_data["add_route"]:
            try:
                vnetdiagnostic_view.select_test_type = self.cases.case_data["add_route"]
                self.logger.info("The VNet test to be tested is:" + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception("Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type, self.cases.case_data["add_route"], "VNet test does not exist.")
        self.logger.info("Enter route table name:")
        vnetdiagnostic_view.route_table_name = self.cases.case_data["new_route_table_name"]
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info("Enter route name:")
        vnetdiagnostic_view.route_name = self.cases.case_data["route_name"]
        self.logger.info(vnetdiagnostic_view.route_name)
        self.logger.info("Enter CIDR:")
        vnetdiagnostic_view.cidr = self.cases.case_data["cidr"]
        self.logger.info(vnetdiagnostic_view.cidr)
        self.logger.info("Enter Next Hop IP:")
        vnetdiagnostic_view.next_hop_ip = self.cases.case_data["next_hop_id"]
        self.logger.info(vnetdiagnostic_view.next_hop_ip)
        self.logger.info("Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(), "Go button does not exist")
        time.sleep(10)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug("Toaster message:" + result)
        self.assertIn(self.cases.expected_result["toaster"], result, "Error adding route table please check debugging message")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),"Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(3)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info("Toaster closed")

        self.cases.end_test("test_case_2")

    def test12_delete_route_of_route_table(self):
        vnetdiagnostic_view = vnetdiag.VNetDiagnostic(self.driver)
        time.sleep(2)
        """
        Delete a route of a route table
        """
        self.logger.info("Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)
        self.cases.start_test("test_case_12")
        """
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
        """
        if vnetdiagnostic_view.select_test_type != self.cases.case_data["delete_route"]:
            try:
                vnetdiagnostic_view.select_test_type = self.cases.case_data["delete_route"]
                self.logger.info("The VNet test to be tested is:" + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception("Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type, self.cases.case_data["delete_route"], "VNet test does not exist.")
        self.logger.info("Enter route table name:")
        vnetdiagnostic_view.route_table_name = self.cases.case_data["new_route_table_name"]
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info("Enter route name:")
        vnetdiagnostic_view.route_name = self.cases.case_data["route_name"]
        self.logger.info(vnetdiagnostic_view.route_name)
        self.logger.info("Check for the Go button")
        self.assertTrue(vnetdiagnostic_view.click_go_button(), "Go button does not exist")
        self.logger.info("Go button does exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug("Toaster message:" + result)
        self.assertIn(self.cases.expected_result["toaster"],result,"Error delete route table check error message for details")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),"Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info("Toaster closed")
        self.cases.end_test("test_case_12")

    def test09_turn_ip_fwd_on(self):
        vnetdiagnostic_view = vnetdiag.VNetDiagnostic(self.driver)
        time.sleep(2)
        """
        Turn IP fwd on
        """
        self.logger.info("Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)
        self.cases.start_test("test_case_9")
        """
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
        """
        if vnetdiagnostic_view.select_test_type != self.cases.case_data["turn_ip_on"]:
            try:
                vnetdiagnostic_view.select_test_type = self.cases.case_data["turn_ip_on"]
                self.logger.info("The VNet test to be tested is:" + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception("Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type, self.cases.case_data["turn_ip_on"], "VNet test does not exist.")
        self.logger.info("Enter Instance ID:")
        vnetdiagnostic_view.instance_id = self.cases.case_data["instance_name"]
        self.logger.info(vnetdiagnostic_view.instance_id)
        self.logger.info("Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(), "Go button does not exist")
        self.logger.info("Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.info("Toaster message:" + result)
        self.assertIn(self.cases.expected_result['toaster'], result, "Error turn IP forward ON")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(),"Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info("Toaster closed")
        self.cases.end_test("test_case_9")

    def test11_turn_ip_forward_off(self):
        vnetdiagnostic_view = vnetdiag.VNetDiagnostic(self.driver)
        time.sleep(2)
        """
        Turn IP fwd off
        """
        self.logger.info("Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)
        self.cases.start_test("test_case_11")
        """
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
        """
        if vnetdiagnostic_view.select_test_type != self.cases.case_data["turn_ip_off"]:
            try:
                vnetdiagnostic_view.select_test_type = self.cases.case_data["turn_ip_off"]
                self.logger.info("The VNet test to be tested is:" + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception("Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type, self.cases.case_data["turn_ip_off"], "VNet test does not exist.")
        self.logger.info("Enter Instance ID:")
        vnetdiagnostic_view.instance_id = self.cases.case_data["instance_name"]
        self.logger.info(vnetdiagnostic_view.instance_id)
        self.logger.info("Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(), "Go button does not exist")
        self.logger.info("Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.info("Toaster message:" + result)
        self.assertIn(self.cases.expected_result['toaster'], result, "Error turn IP forward OFF")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(), "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info("Toaster closed")
        self.cases.end_test("test_case_11")

    def test10_get_ip_forward(self):
        vnetdiagnostic_view = vnetdiag.VNetDiagnostic(self.driver)
        time.sleep(2)
        """
        Get status of IP forward
        """
        self.logger.info("Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)
        self.cases.start_test("test_case_10")
        """
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
        """
        if vnetdiagnostic_view.select_test_type != self.cases.case_data["get_ip_fwd"]:
            try:
                vnetdiagnostic_view.select_test_type = self.cases.case_data["get_ip_fwd"]
                self.logger.info("The VNet test to be tested is:" + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception("Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type, self.cases.case_data["get_ip_fwd"], "VNet test does not exist.")
        self.logger.info("Enter Instance ID:")
        vnetdiagnostic_view.instance_id = self.cases.case_data["instance_name"]
        self.logger.info(vnetdiagnostic_view.instance_id)
        self.logger.info("Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(), "Go button does not exist")
        self.logger.info("Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug("Toaster message:" + result)
        self.assertTrue(self.cases.expected_result["toaster"] in result, "Error adding route table,please check toast message")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(), "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info("Toaster closed")
        self.cases.end_test("test_case_10")

    def test07_associate_subnet(self):
        vnetdiagnostic_view = vnetdiag.VNetDiagnostic(self.driver)

        time.sleep(2)

        """
        Associating VNet/subnet to a route table
        """
        self.logger.info("Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)
        self.cases.start_test("test_case_7")
        """
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
        """
        if vnetdiagnostic_view.select_test_type != self.cases.case_data["associate_subnet"]:
            try:
                vnetdiagnostic_view.select_test_type = self.cases.case_data["associate_subnet"]
                self.logger.info("The VNet test to be tested is:" + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception("Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type, self.cases.case_data["associate_subnet"], "VNet test does not exist.")

        self.logger.info("Enter route table name:")
        vnetdiagnostic_view.route_table_name = self.cases.case_data["new_route_table_name"]
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info("Enter VNet name:")
        vnetdiagnostic_view.vnet_name = self.cases.case_data["list_vnet_name"]
        self.logger.info(vnetdiagnostic_view.vnet_name)
        self.logger.info("Enter subnet:")
        vnetdiagnostic_view.subnet = self.cases.case_data["associate_vnet_subnet"]
        self.logger.info(vnetdiagnostic_view.subnet)
        self.logger.info("Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(), "Go button does not exist")
        self.logger.info("Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug("Toaster message:" + result)
        self.assertIn(self.cases.expected_result['toaster'], result, "Error associating the subnet,check for error message")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(), "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info("Toaster closed")
        self.cases.end_test("test_case_7")

    def test08_dissociate_subnet(self):
        vnetdiagnostic_view = vnetdiag.VNetDiagnostic(self.driver)
        time.sleep(3)

        """
         Dissociating VNet/subnet to a route table
        """
        self.logger.info("Current cloud type on dropdown menu  is : " + vnetdiagnostic_view.select_cloud_type)
        self.cases.start_test("test_case_8")
        """
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
        """
        if vnetdiagnostic_view.select_test_type != self.cases.case_data["disociate_subnet"]:
            try:
                vnetdiagnostic_view.select_test_type = self.cases.case_data["disociate_subnet"]
                self.logger.info("The VNet test to be tested is:" + vnetdiagnostic_view.select_test_type)
            except:
                self.logger.exception("Could not change to the selected VNet test")
            self.assertEqual(vnetdiagnostic_view.select_test_type, self.cases.case_data["disociate_subnet"], "VNet test does not exist.")

        self.logger.info("Enter route table name:")
        vnetdiagnostic_view.route_table_name = self.cases.case_data["new_route_table_name"]
        self.logger.info(vnetdiagnostic_view.route_table_name)
        self.logger.info("Enter VNet name:")
        vnetdiagnostic_view.vnet_name = self.cases.case_data["list_vnet_name"]
        self.logger.info(vnetdiagnostic_view.vnet_name)
        self.logger.info("Enter subnet:")
        vnetdiagnostic_view.subnet = self.cases.case_data["associate_vnet_subnet"]
        self.logger.info(vnetdiagnostic_view.subnet)
        self.logger.info("Assert if the Go button exist")
        self.assertTrue(vnetdiagnostic_view.click_go_button(), "Go button does not exist")
        self.logger.info("Go button exist and clicked")
        time.sleep(30)
        result = vnetdiagnostic_view.output_toaster
        self.logger.debug("Toaster message:" + result)
        self.assertIn(self.cases.expected_result['toaster'], result, "Error dissociating the subnet, check for the error message")
        time.sleep(10)
        self.assertTrue(vnetdiagnostic_view.click_toaster_close_button(), "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed might have exception notice due to lack of toaster")
        self.assertFalse(vnetdiagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info("Toaster closed")
        self.cases.end_test("test_case_8")
