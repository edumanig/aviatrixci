__author__ = 'Rong'

import unittest, logging, time, platform,datetime
from selenium import webdriver
import autotest.lib.webui_pages.diagnostics as diag
from autotest.run_autotest import config
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases

#test used to test upload tracelog
class DiagnosticsPageTest(WebUITest):
    cases = testcases(__name__)

    """
     Note:There a few things that needed to be changed for smooth run
     1)in config file:
       -uccURL
       -login_username
       -login_password(These only need to be change for once and the test should be able to run)
       -gateway_name_troubleshooting(input a gateway exist on your controller)
       -vpn_username(input a vpc user on your controller)
       -database_name(Name of a database,i think i choose a common one but you should check)
       -collection_name(Collection name change with Database name, so you need to change it)
       -diagnostic_input_document(Document name from database,the one i use is wrong, so if you
       found one...)

    """
    def test02_run_gateway_diagnostic(self):
        diagnostic_view = diag.Diagnostics(self.driver)
        time.sleep(3)
        """
        Run a diagnostic test with chosen gateway and make sure it is successful
        """
        self.cases.start_test("test_case_2")
        self.logger.info("Current Gateway name on dropdown menu is : " + diagnostic_view.select_gateway)

        if diagnostic_view.select_gateway != self.cases.case_data["gateway_name"]:
            try:
                diagnostic_view.select_gateway = self.cases.case_data["gateway_name"]
                self.logger.info ("The Gateway to run a Diagnostic test on is:" + diagnostic_view.select_gateway)
            except:
                self.logger.exception("Could not change to the selected Gateway name")
            self.assertEqual(diagnostic_view.select_gateway, self.cases.case_data["gateway_name"], "Gateway name does not exist.")
        try:
            self.logger.info("Select Controller option...")
            diagnostic_view.check_controller = "select"
        except:
            self.logger.exception("Could not select Controller option.. ")
            self.assertFalse(diagnostic_view.check_controller)
        self.logger.info("Assert if the Run button exist")
        self.assertTrue(diagnostic_view.click_run_button(), "Run button does not exist")
        self.logger.info("Run button exist and clicked")
        time.sleep(100)
        result = diagnostic_view.toaster_message
        self.logger.info("Checking toaster message, will pass the test if toaster message is correct")
        self.assertIn(self.cases.expected_result["toaster"], result, "Diagnostic test could not be run")
        self.logger.info("The message shown is:%s", result)
        time.sleep(10)
        self.logger.info("Closing the toaster...")
        self.assertTrue(diagnostic_view.click_toaster_close_button(), "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed,might show exception..")
        self.assertFalse(diagnostic_view.check_toaster(),"Toaster is not closed")
        self.logger.info("Toaster closed")

        self.cases.end_test("test_case_2")

        time.sleep(2)
        """
        Run a diagnostic test and record the result in logger and txt file
        """
        self.cases.start_test("test_case_3")
        self.logger.info("Current Gateway Name on dropdown menu is : " + diagnostic_view.select_gateway)
        """
        try:
            self.logger.info("Select Controller option...")
            diagnostic_view.check_controller = "select"
        except:
            self.logger.exception("Could not select Controller option.. ")
            self.assertFalse(diagnostic_view.check_controller)
        self.logger.info(
            "Run the test again to make sure the result is new")
        self.assertTrue(diagnostic_view.click_run_button(),
                        "Run button does not exist")
        self.logger.info(
            "Run button exist and clicked")
        time.sleep(100)
        result = diagnostic_view.toaster_message
        self.assertIn("Finished running diagnostic tests", result,
                      "Diagnostic test could not be run")
        time.sleep(10)
        diagnostic_view.click_toaster_close_button()
        time.sleep(5)
        self.logger.info(
            "Test has finnish running, continue....")
        """
        self.logger.info("Assert if the Show button exist")
        self.assertTrue(diagnostic_view.click_show_button(), "Shown button does not exist")
        self.logger.info("Show button exist and clicked")
        result = diagnostic_view.diagnostic_result
        print(result)
        if self.cases.case_data["gateway_name"] != "none":
            self.assertNotEqual("{\n    \"diagnostics_results\": {}\n}", result, "The test was not run properly, please try again")
        self.assertTrue(self.cases.case_data["gateway_name"] in result,"Ending the test, please press Run to run the test first and try again")
        self.logger.info("Gateway Diagnostic Result:\n" + result)
        file_name = ('gateway_diagnostic_{:%Y%m%d-%H%M%S}.txt'.format(datetime.datetime.now()))
        if platform.system() == "Windows":
            save_path_file_name = "results\\temp\\" + file_name
        else:
            save_path_file_name = "results//temp//" + file_name
        gateway_diagnostic_result_file = open(save_path_file_name, "w")
        gateway_diagnostic_result_file.write('Gateway Diagnostic logged at: {:%Y-%m-%d %H:%M:%S}\n'.format(datetime.datetime.now()))
        gateway_diagnostic_result_file.write(result + "\n")
        gateway_diagnostic_result_file.close()
        self.logger.info("Gateway diagnostic result also saved at: " + save_path_file_name)
        diagnostic_view.click_close_button()

        self.cases.end_test("test_case_3")

        time.sleep(3)
        """
        Run and submit a diagnostic with choose gateway and make sure it is successful
        """
        self.cases.start_test("test_case_4")
        self.logger.info("Current Gateway name on dropdown menu is : " + diagnostic_view.select_gateway)
        """
        if diagnostic_view.select_gateway != _variables[
            "gateway_name_troubleshooting"]:
            try:
                diagnostic_view.select_gateway = _variables[
                    "gateway_name_troubleshooting"]
                self.logger.info(
                    "The Gateway to be diagnosed" + diagnostic_view.select_gateway)
            except:
                self.logger.exception(
                    "Could not change to the selected gateway name")
            self.assertEqual(diagnostic_view.select_gateway,
                             _variables["gateway_name_troubleshooting"],
                             "Gateway name does not exist.")
        try:
            self.logger.info("Select Controller option...")
            diagnostic_view.check_controller = "select"
        except:
            self.logger.exception("Could not select Controller option.. ")
            self.assertFalse(diagnostic_view.check_controller)
        self.logger.info(
            "Run the test again to make sure the result is new")
        self.assertTrue(diagnostic_view.click_run_button(),
                        "Run button does not exist")
        self.logger.info(
            "Run button exist and clicked")
        time.sleep(100)
        result = diagnostic_view.toaster_message
        self.assertIn("Finished running diagnostic tests", result,
                          "Diagnostic test could not be run")
        time.sleep(10)
        diagnostic_view.click_toaster_close_button()
        time.sleep(5)
        self.logger.info(
                "Test has finnish running, continue....")
        """
        self.logger.info("Assert if the Submit button exist")
        self.assertTrue(diagnostic_view.click_submit_button(), "Submit button does not exist")
        self.logger.info("Submit button exist and clicked")
        time.sleep(50)
        result = diagnostic_view.toaster_message
        self.logger.info("Checking toaster message, will pass the test if toaster message is correct")
        self.assertIn(self.cases.expected_result['toaster'], result, "Diagnostic could not be submitted")
        self.logger.info("The message shown is:%s", result)
        time.sleep(5)
        self.logger.info("Will close the toaster..")
        self.assertTrue(diagnostic_view.click_toaster_close_button(), "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(3)
        self.logger.info("Check for toaster to see if it is really closed")
        self.assertFalse(diagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info("Toaster closed")

        self.cases.end_test("test_case_4")

    def test01_vpn_user_diagnostic(self):
        diagnostic_view = diag.Diagnostics(self.driver)
        self.logger.info("Navigating to Troubleshooting")
        title = diagnostic_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title, "Troubleshooting link does not exist")
        self.logger.info("Navigating to Diagnostic")
        diagnostic_view.navigate_to_diagnostics()
        self.logger.info("Check if Diagnostic is the right page")
        self.assertTrue(diagnostic_view.current_url(), "Not on the Diagnostic page")
        time.sleep(10)

        """
        Fill the VPN username and run a test.Record the result in logger and save
        in txt file
        """
        self.logger.info("Start to run CPN USer Diag")
        self.cases.start_test("test_case_1")
        self.logger.info("Input into VPN username:")
        diagnostic_view.vpn_user = self.cases.case_data["vpn_username"]
        self.logger.info(diagnostic_view.vpn_user)
        self.logger.info("Assert if the Go button exist")
        self.assertTrue(diagnostic_view.click_go_button(), "Go button does not exist")
        self.logger.info("Go button exist and clicked")

        diagnostic_view.wait_for_show_results_present()
        result = diagnostic_view.vpn_diagnostic_message
        self.assertNotEqual("[]", result, "VPN user does not exist or not connected")
        self.logger.info("VPN User Diagnostic Result:\n" + result)
        file_name = ('vpn_user_diagnostic_{:%Y%m%d-%H%M%S}.txt'.format(datetime.datetime.now()))
        if platform.system() == "Windows":
            save_path_file_name = "results\\temp\\" + file_name
        else:
            save_path_file_name = "results//temp//" + file_name
        vpn_result_file = open(save_path_file_name, "w")
        vpn_result_file.write('VPN diagnostic result logged at: {:%Y-%m-%d %H:%M:%S}\n'.format(datetime.datetime.now()))
        vpn_result_file.write(result)
        vpn_result_file.close()
        self.logger.info("VPN User diagnostic saved at: " + save_path_file_name)

        self.cases.end_test("test_case_1")


