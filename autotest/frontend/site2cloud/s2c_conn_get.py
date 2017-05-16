__author__ = 'lmxiang'

import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from GUI.v2.lib.common_elements import *
from tests.utils.test_utils import avx_logger
import GUI.v2.site2cloud.s2c_conn as pages


class S2C_Conn_Get(unittest.TestCase):
    """
    Get the details about a Site2Cloud connection including:
     - VPC ID/VNet Name
     - Status
     - Aviatrix Gateway
     - Customer Gateway IP
     - Customer Network
     - Cloud Network
    Get the tunnel details including:
     - Tunnel ID
     - Gateway Name
     - Gateway Public IP
     - Tunnel Status
     - Status Last Changed
    Get connection details including:
     - Connection Type
     - Local CIDR
     - Remote CIDR
    """

    @classmethod
    def setUpClass(cls):
        cls.logger = avx_logger()
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.maximize_window()

    def test_s2c_get(self):
        self.logger.info("Start Site2Cloud Connection Test - Get")

        s2c_view = pages.S2C_View(self.driver, login_required=True)
        self.logger.info("Navigating to Site2Cloud")
        s2c_view.navigate_to_s2c()
        time.sleep(5)

        self.logger.info("Check if Site2Cloud is present in the current view area...")
        assert s2c_view.match_view_title(),"Site2Cloud view is not present"

        # find the values of all table elements of connection 'ProdConn'
        s2c_conn_name = "ProdConn"
        self.logger.info("Retrieve connection details about %s", s2c_conn_name)
        s2c_conn_elements = ["VPC ID/VNet Name",
                             "Status",
                             "Aviatrix Gateway",
                             "Customer Gateway IP",
                             "Customer Network",
                             "Cloud Network"]
        for element in s2c_conn_elements:
            s2c_element = s2c_view.get_s2c_element(s2c_conn_name, element)
            assert (s2c_element), "Fail to find Site2Cloud element"

        self.logger.info("--------------------------------------------------------")
        self.logger.info("Retrieve tunnel details about %s", s2c_conn_name)
        s2c_view.find_s2c_conn(s2c_conn_name)
        time.sleep(10)
        tunnel_details = s2c_view.tunnel_table
        for elem in tunnel_details:
            for key, value in elem.items():
                self.logger.info("%s : %s" % (key, value))

        self.logger.info("--------------------------------------------------------")
        self.logger.info("Retrieve connection details about %s", s2c_conn_name)
        conn_details = s2c_view.get_conn_details()
        self.logger.info(conn_details)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()