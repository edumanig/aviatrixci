__author__ = 'Rong'
import unittest, logging, time
from selenium import webdriver
import tests.UCC.UCCWebUI.lib.webui_pages.diagnostics as pages
import datetime

#test used to test upload tracelog
class DiagnosticsPageTest(unittest.TestCase):

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

        cls.logger.info("Checking if we are logged in to the first page")
        cls.assertTrue(UCCLogin.check_for_controller(),
                       "Dashboard Page is loaded correctly")

    """
         Note:There a few things that needed to be changed for smooth run
         Please refer back to diagnostic_tests

    """
    def test_show_gateway_diagnostic_without_run(self):
        from tests.main import variables as _variables

        diagnostic_view = pages.Diagnostics(self.driver)
        self.logger.info("Check if Diagnostic is the right page")
        self.assertTrue(diagnostic_view.current_url(),
                             "Not on the Diagnostic page")
        time.sleep(10)

        """
        Show a gateway diagnostic without running a gateway diagnostic.It would
        show a gateway result of something else due to not refreshing the cache
        """
        self.logger.info(
            "Current Gateway Name on dropdown menu is : " + diagnostic_view.select_gateway)

        if diagnostic_view.select_gateway != _variables[
            "gateway_name_troubleshooting"]:
            try:
                diagnostic_view.select_gateway = _variables[
                    "gateway_name_troubleshooting"]
                self.logger.info(
                    "The Gateway to be diagnosed" + diagnostic_view.select_gateway)
            except:
                self.logger.exception(
                    "Could not change to the selected Gateway name")
            self.assertEqual(diagnostic_view.select_gateway,
                             _variables["gateway_name_troubleshooting"],
                             "Gateway name does not exist.")
        try:
            self.logger.info("Select Controller option...")
            diagnostic_view.check_controller = "select"
        except:
            self.logger.exception("Could not select Controller option.. ")
        self.logger.info(
            "Assert if the Show button exist")
        self.assertTrue(diagnostic_view.click_show_button(),
                        "Shown button does not exist")
        self.logger.info(
            "Show button exist and clicked")
        self.logger.info(
            "Check if the information is actually the gateway information, will pass if it is not")
        result = diagnostic_view.diagnostic_result
        if _variables["gateway_name_troubleshooting"] != "none" :
            self.assertNotEqual("{\n    \"diagnostics_results\": {}\n}", result,
                                "The test was not run properly, please try again")
        self.assertTrue(_variables["gateway_name_troubleshooting"] not in result,"The gateway shown is correct,aborting this negative test")

    def test_nonexistence_vpn_user_diagnostic(self):
        from tests.main import variables as _variables

        diagnostic_view = pages.Diagnostics(self.driver)
        self.logger.info("Navigating to Troubleshooting")
        title = diagnostic_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title,
                         "Troubleshooting link does not exist")
        self.logger.info("Navigating to Diagnostic")
        diagnostic_view.navigate_to_diagnostics()
        self.logger.info("Check if Diagnostic is the right page")
        self.assertTrue(diagnostic_view.current_url(),
                        "Not on the Diagnostic page")
        time.sleep(10)
        """
        Fill in a non-existence VPN and check if the information is correct
        """
        self.logger.info("Input into VPN username:")
        diagnostic_view.vpn_user = "rong"
        self.logger.info(diagnostic_view.vpn_user)
        self.logger.info(
            "Assert if the Go button exist")
        self.assertTrue(diagnostic_view.click_go_button(),
                        "Go button does not exist")
        self.logger.info(
            "Go button exist and clicked")
        time.sleep(30)
        result = diagnostic_view.vpn_diagnostic_message
        self.assertEqual("[]", result,
                            "VPN user exist,abort this negative test")

    def test_dump_nonexistence_document(self):
        from tests.main import variables as _variables

        diagnostic_view = pages.Diagnostics(self.driver)
        self.logger.info("Navigating to Troubleshooting")
        title = diagnostic_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title,
                         "Troubleshooting link does not exist")
        self.logger.info("Navigating to Diagnostic")
        diagnostic_view.navigate_to_diagnostics()
        self.logger.info("Check if Diagnostic is the right page")
        self.assertTrue(diagnostic_view.current_url(),
                        "Not on the Diagnostic page")
        time.sleep(10)

        """
        Input in a Document that does not exist and press the Dump Document button
        Check if there is an error
        """
        self.logger.info("The document to be dumped is:")
        diagnostic_view.input_document = "key:value"
        self.logger.info(diagnostic_view.input_document)
        self.logger.info("Find the Dump Document ..")
        self.assertTrue(diagnostic_view.click_dump_document_button(),
                        "Dump Document button does not exist")
        self.logger.info(
            "Dump Document button exist and clicked")
        time.sleep(10)
        self.logger.info(
            "Check for error message,will pass if error message is shown")
        result = diagnostic_view.is_error_message_shown()
        self.assertIn("Error:", result,
                      "There is no error,aborting the negative test")
        time.sleep(10)
        self.assertTrue(diagnostic_view.click_toaster_close_button(),
                        "Close button does not exist")
        self.logger.info(
            "Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
            "Check for toaster to see if it is really closed")
        self.assertFalse(diagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info(
            "Toaster closed")

    def test_delete_document(self):
        from tests.main import variables as _variables

        diagnostic_view = pages.Diagnostics(self.driver)
        self.logger.info("Navigating to Troubleshooting")
        title = diagnostic_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title,
                         "Troubleshooting link does not exist")
        self.logger.info("Navigating to Diagnostic")
        diagnostic_view.navigate_to_diagnostics()
        self.logger.info("Check if Diagnostic is the right page")
        self.assertTrue(diagnostic_view.current_url(),
                        "Not on the Diagnostic page")
        time.sleep(10)

        """
        Input to the document some erroneous value and continue the process
        """
        self.logger.info("The document to be deleted is:")
        diagnostic_view.input_document = "key:value"
        self.logger.info(diagnostic_view.input_document)
        self.logger.info("Checking if the Delete Document button exist")
        self.assertTrue( diagnostic_view.click_delete_document_button(),
                        "Delete Document button does not exist")
        self.logger.info(
            "Delete Document button exist and clicked")
        self.logger.info(
            "Check for pop up and assume pop up has the right message..")
        time.sleep(5)
        assert diagnostic_view.confirm_pop_up_exist, "No pop up is shown"
        self.logger.info(
            "Pop-up exist..")
        self.logger.info(
            "Assert if the OK button exist")
        self.assertTrue(diagnostic_view.click_pop_up_ok_button(),
                        "OK button does not exist")
        self.logger.info("Pop up okay, click ok to start the process")
        time.sleep(100)
        self.logger.info(
            "Check for error message,will pass if error message is shown")
        result = diagnostic_view.is_error_message_shown()
        self.assertIn("Error:", result,
                      "There is no error,aborting the negative test")
        time.sleep(10)
        self.assertTrue(diagnostic_view.click_toaster_close_button(),
                        "Close button does not exist")
        self.logger.info(
            "Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
            "Check for toaster to see if it is really closed")
        self.assertFalse(diagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info(
            "Toaster closed")



    @classmethod
    def tearDownClass(cls):
        cls.driver.close()