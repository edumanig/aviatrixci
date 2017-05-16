__author__ = 'lmxiang'

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from autotest.lib.common_elements import *
import autotest.lib.webui_pages.site2cloud.s2c_conn as pages
from autotest.lib.test_utils import testcases

class S2C_Conn_Change(unittest.TestCase):
    cases = testcases(__name__)
    """
    Change existing Site2Cloud connection configuration including
     - Customer network CIDRs
     - Cloud network CIDRs
    """

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(pages.__name__)
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.maximize_window()

    def test_s2c_customer_nw(self):
        self.logger.info("Start to change Site2Cloud customer network configuration ")

        s2c_view = pages.S2C_View(self.driver, login_required=True)
        self.logger.info("Navigating to Site2Cloud")
        s2c_view.navigate_to_s2c()
        time.sleep(20)

        self.logger.info("Check if Site2Cloud is present in the current view area...")
        assert s2c_view.match_view_title(),"Site2Cloud view is not present"

        self.cases.start_test("test_case_1")
        s2c_conn_name = self.cases.case_data['conn_name']

        try:
            # Find the site2cloud connection and click on it
            s2c_view.find_s2c_conn(s2c_conn_name)
            time.sleep(10)

            # Start to change customer network
            self.logger.info("Change Site2Cloud customer network")
            s2c_view.change_customer_network(self.cases.case_data['customer_nw_real'])
            time.sleep(10)
            toaster_result = s2c_view.change_toaster.lower()
            assert (self.cases.expected_result['toaster'] in toaster_result), "Fail to change Site2Cloud customer network"
            time.sleep(10)

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.debug("Can not change customer network with exception %s", str(e))
            assert False

        self.cases.end_test("test_case_1")

    def test_s2c_cloud_nw(self):
        self.logger.info("Start to change Site2Cloud cloud network configuration")

        s2c_view = pages.S2C_View(self.driver, login_required=True)
        self.logger.info("Navigating to Site2Cloud")
        s2c_view.navigate_to_s2c()
        time.sleep(5)

        self.logger.info("Check if Site2Cloud is present in the current view area...")
        assert s2c_view.match_view_title(),"Site2Cloud view is not present"

        self.cases.start_test("test_case_2")
        s2c_conn_name = self.cases.case_data['conn_name']

        try:
            # Find the site2cloud connection and click on it
            s2c_view.find_s2c_conn(s2c_conn_name)
            time.sleep(5)

            # Start to change customer network
            self.logger.info("Change Site2Cloud cloud network")
            s2c_view.change_cloud_network(self.cases.case_data['cloud_sub_real'])
            time.sleep(10)
            toaster_result = s2c_view.change_toaster.lower()
            assert (self.cases.expected_result['toaster'] in toaster_result), "Fail to change Site2Cloud cloud network"
            time.sleep(10)

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.debug("Can not change cloud network with exception %s", str(e))
            assert False
        self.cases.end_test("test_case_2")

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__ == "__main__":
    unittest.main()