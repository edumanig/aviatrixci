__author__ = 'lmxiang'

import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from GUI.v2.lib.common_elements import *
from tests.utils.test_utils import avx_logger
import GUI.v2.site2cloud.s2c_conn as pages


class S2C_Conn_Import(unittest.TestCase):
    """
    Import new site2cloud connection
    """

    @classmethod
    def setUpClass(cls):
        #cls.logger = logging.getLogger()
        cls.logger =avx_logger()
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.maximize_window()

    def test_s2c_import(self):
        config_file = "C:\\Users\\lmxiang\\Desktop\\vpc-01992565-ProdVPC-conn123 (1).txt"
        vpc_id = "vpc-54372631"
        conn_name = "s2c-regression"

        self.logger.info("Start Importing Site2Cloud Connection")

        s2c_view = pages.S2C_New(self.driver, login_required=True)
        self.logger.info("Navigating to Site2Cloud")
        s2c_view.navigate_to_s2c()
        time.sleep(5)

        self.logger.info("Check if Site2Cloud is present in the current view area...")
        assert s2c_view.match_view_title(),"Site2Cloud view is not present"
        time.sleep(5)

        self.logger.info("Click 'Add New' button to create a new site2cloud connection...")
        s2c_view.new_button = "new"
        time.sleep(5)

        elm = self.driver.find_element_by_xpath("//input[@type='file']")
        elm.send_keys(config_file)
        time.sleep(5)

        s2c_view.select_vpc_id = vpc_id
        self.logger.debug("Site2Cloud VPC ID/VNet Name: %s", vpc_id)

        s2c_view.input_conn_name = conn_name
        self.logger.debug("Site2Cloud Connection Name: %s", conn_name)
        time.sleep(5)

        s2c_view.ok_button = "ok"
        time.sleep(5)
        toaster_result = s2c_view.s2c_toaster.lower()
        assert ("successfully" in toaster_result),"Fail to create Site2Cloud connection: "+toaster_result
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__ == "__main__":
    unittest.main()