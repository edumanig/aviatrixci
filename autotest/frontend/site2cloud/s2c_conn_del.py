__author__ = 'lmxiang'

import unittest,logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from autotest.lib.common_elements import *
from autotest.lib.test_utils import avx_logger
from autotest.lib.cloudn_utils import handle_alert
import autotest.lib.webui_pages.site2cloud.s2c_conn as pages
from autotest.lib.test_utils import testcases


class S2C_Conn_Del(unittest.TestCase):
    cases = testcases(__name__)
    """
    Delete Site2Cloud connection from a list of connection names
    """

    @classmethod
    def setUpClass(cls):
        #cls.logger = logging.getLogger()
        cls.logger = logging.getLogger(pages.__name__)
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.maximize_window()

    def test_s2c_del(self):
        self.logger.info("Start Site2Cloud Connection Test - Delete")

        s2c_view = pages.S2C_View(self.driver, login_required=True)
        self.logger.info("Navigating to Site2Cloud")
        s2c_view.navigate_to_s2c()
        time.sleep(5)

        self.logger.info("Check if Site2Cloud is present in the current view area...")
        assert s2c_view.match_view_title(),"Site2Cloud view is not present"

        self.cases.start_test("test_case_1")
        s2c_conn_names = self.cases.case_data['s2c_conn_names']

        for s2c_conn_name in s2c_conn_names:
            s2c_view.delete_conn(s2c_conn_name)
            toaster_result = s2c_view.s2c_toaster.lower()
            assert (self.cases.expected_result['toaster'] in toaster_result), "Fail to delete " + s2c_conn_name

        self.cases.end_test("test_case_1")

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__ == "__main__":
    unittest.main()