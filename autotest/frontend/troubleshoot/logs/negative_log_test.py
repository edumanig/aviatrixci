__author__ = 'Rong'
import unittest, logging, time
from selenium import webdriver
import tests.UCC.UCCWebUI.lib.webui_pages.logs as pages
import datetime
#please check config uccURL
class LogsPageTest(unittest.TestCase):

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
                Please refer back to logs_tests

       """
    def test_ping_utility_with_nonexisting_website(self):
        from tests.main import variables as _variables

        log_view = pages.Logs(self.driver)
        self.logger.info("Navigating to Troubleshooting")
        title = log_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title,
                         "Troubleshooting link does not exist")
        self.logger.info("Navigating to Logs")
        log_view.navigate_to_log()
        self.assertTrue(log_view.check_for_log_page(),
                        "Tracelog Page is loaded correctly")
        """
        Try to ping nonexisting website,should not show any result
        """
        self.logger.info("The host name to be pinged is:")
        log_view.host_name = "www.19920307.com"
        self.logger.info(log_view.host_name)
        self.logger.info(
            "Assert if the Ping button exist")
        self.assertTrue(log_view.click_ping_button(),
                        "Ping button does not exist")
        self.logger.info(
            "Ping button exist and clicked")
        time.sleep(20)
        result = log_view.ping_result
        self.assertEqual("",result,"Erroneous result,aborting negative test")

    def test_ping_utility_with_unpingable_website(self):
        from tests.main import variables as _variables

        log_view = pages.Logs(self.driver)
        self.logger.info("Navigating to Troubleshooting")
        title = log_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title,
                         "Troubleshooting link does not exist")
        self.logger.info("Navigating to Logs")
        log_view.navigate_to_log()
        self.assertTrue(log_view.check_for_log_page(),
                        "Tracelog Page is loaded correctly")
        """
        Try to ping an IP with no internet gateway/connection,should show 100% package lost
        """
        self.logger.info("The host name to be pinged is:")
        log_view.host_name = "52.164.255.161"
        self.logger.info(log_view.host_name)
        self.logger.info(
            "Assert if the Ping button exist")
        self.assertTrue(log_view.click_ping_button(),
                        "Ping button does not exist")
        self.logger.info(
            "Ping button exist and clicked")
        time.sleep(20)
        result = log_view.ping_result
        self.assertNotEqual("",result,"Nothing is shown in Ping text area")
        self.assertFalse("100% packet loss" not in result,
                        "Connection is okay, aborting this negative testing")



    @classmethod
    def tearDownClass(cls):
        cls.driver.close()