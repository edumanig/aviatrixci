__author__ = 'lmxiang'

import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from GUI.v2.lib.common_elements import *
import GUI.v2.site2cloud.s2c_diag as pages
from tests.utils.test_utils import avx_logger

class S2C_Diag_Tests(unittest.TestCase):
    """
    Run diagnostics on an existing Site2Cloud connection including:
     - show logs
     - show security association details
     - show service status
     - show configuration
     - show security policy details
     - restart service
    """

    @classmethod
    def setUpClass(cls):

        cls.logger = avx_logger()
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.maximize_window()

    def test_s2c_diag(self):
        action_list = ["Show logs", "Show security association details", "Show service status",
                       "Show configuration", "Show security policy details", "Restart service"]

        s2c_view = pages.S2C_Diag(self.driver, login_required=True)
        time.sleep(10)

        self.logger.info("Navigating to Site2Cloud")
        s2c_view.navigate_to_s2c()

        time.sleep(15)
        self.logger.info("Check if Site2Cloud is present in the current view area...")
        assert s2c_view.match_view_title(),"Site2Cloud view is not present"

        time.sleep(5)
        self.logger.info("Select Site2Cloud Diagnostics")
        assert s2c_view.select_tab(), "Site2Cloud diagnostics is not present"

        # Run all diagnostics functions for the following connection
        for action in action_list:
            s2c_action = {"vpc_id":"vpc-54372631",
                          "conn":"ProdConn",
                          "gateway":"ProdGW",
                          "action":action
                          }
            time.sleep(5)
            self.logger.info("Fill in fields for Site2Cloud diagnostics")
            assert s2c_view.fill_conn_fields(**s2c_action),"Fail to fill in Site2Cloud diagnostics fields"
            s2c_view.ok_button = "ok"
            self.logger.info("Copy out the diagnostics results")
            output = s2c_view.diag_result
            assert output, "Fail to get diagnostics results"
            self.logger.info("Diagnostics results: " + output)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__ == "__main__":
    unittest.main()