__author__ = 'lmxiang'

import unittest
import os,logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from autotest.lib.common_elements import *
#from autotest.lib.test_utils import avx_logger
from autotest.lib.test_utils import find_files_in_directory, delete_files_in_directory
import autotest.lib.webui_pages.site2cloud.s2c_conn as pages
from autotest.run_autotest import config
from autotest.lib.test_utils import testcases


class S2C_Conn_Config(unittest.TestCase):
    cases = testcases(__name__)

    """
    Download configuration template for existing Site2Cloud connection
     - Cisco ASA
     - Aviatrix
     - Generic
    """

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(pages.__name__)
        chrome_options = Options()
        # folder used for Chrome to download files
        cls.dir_path = os.path.abspath(config['download']['autotest_download'])
        cls.logger.info("Chrome download path has been set to {}".format(cls.dir_path))
        prefs = {"download.default_directory" : cls.dir_path}
        chrome_options.add_experimental_option("prefs",prefs)
        chrome_options.add_argument("--disable-extensions")
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.maximize_window()

    def test_s2c_config(self):
        self.logger.info("Start Site2Cloud Connection ")

        s2c_view = pages.S2C_View(self.driver, login_required=True)
        self.logger.info("Navigating to Site2Cloud")
        s2c_view.navigate_to_s2c()
        time.sleep(15)

        self.logger.info("Check if Site2Cloud is present in the current view area...")
        assert s2c_view.match_view_title(),"Site2Cloud view is not present"

        delete_files_in_directory(self.dir_path)
        self.cases.start_test("test_case_1")
        try:
            # Find the site2cloud connection and click on it
            s2c_view.find_s2c_conn(self.cases.case_data['conn_name'])
            time.sleep(5)

            # Start to download its configuration templates for config 1-4
            for conf in self.cases.case_data:
                if "config" in conf:
                    self.logger.info("Input the values for {}".format(conf))
                    for keys,values in self.cases.case_data[conf].items():
                        self.logger.info("%s : %s" % (keys, values))
                    s2c_view.download_config(self.cases.case_data[conf]["vendor"], self.cases.case_data[conf]["platform"], self.cases.case_data[conf]["software"])
                time.sleep(15)

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.debug("Can not find the table with exception %s", str(e))
            assert False
        self.cases.end_test("test_case_1")

        # Search download folder for all template files starting with 'vpc-01992565'
        self.cases.start_test("test_case_2")
        download_files = find_files_in_directory(self.dir_path, self.cases.case_data['partial_file_name'])
        for file in download_files:
            self.logger.info(file)

        # If the number of downloaded files matches the number of config templates, test passes
        if len(download_files) == int(self.cases.expected_result['file_count']):
            self.logger.info("Total number of configuration files download: %s" % str(len(download_files)))
            assert True
        else:
            self.logger.error("Failed to download all configuration templates")
            assert False

        self.cases.end_test("test_case_2")
        delete_files_in_directory(self.dir_path)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__ == "__main__":
    unittest.main()