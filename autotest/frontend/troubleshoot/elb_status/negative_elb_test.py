__author__ = 'Rong'
import unittest, logging, time
from selenium import webdriver
import tests.UCC.UCCWebUI.lib.webui_pages.elb_diagnostic as pages
import datetime
import boto.ec2.elb
class ELBPageTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        class and methods provided by Sam
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
             Please refer back to elb_tests

    """
    def test_elb_status(self):
        from tests.main import variables as _variables

        elb_diagnostic_view = pages.ELB_Diagnostic(self.driver)
        self.logger.info("Navigating to Troubleshooting")
        title = elb_diagnostic_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title,
                         "Troubleshooting link does not exist")
        self.logger.info("Navigating to ELB Status")
        elb_diagnostic_view.navigate_to_elb_status()
        self.logger.info("Check if ELB Status is the right page")
        self.assertTrue(elb_diagnostic_view.current_url(),"Not on the ELB Status page")
        time.sleep(10)

        """
        Check whether the cloud provide ELB service
        """
        self.logger.info("Check if the current account has ELB service")
        self.assertTrue( elb_diagnostic_view.check_toaster(),
                      "ELB service is supported in this type of cloud,aborting negative testing")
        time.sleep(10)
        self.logger.info("Closing the toaster...")
        self.assertTrue(elb_diagnostic_view.click_toaster_close_button(),
                        "Close button does not exist")
        self.logger.info(
            "Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
            "Check for toaster to see if it is really closed,might show exception..")
        self.assertFalse(elb_diagnostic_view.check_toaster(),
                         "Toaster is not closed")
        self.logger.info(
            "Run diagnostic test toaster closed")




    @classmethod
    def tearDownClass(cls):
        cls.driver.close()