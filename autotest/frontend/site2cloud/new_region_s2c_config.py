__author__ = 'lmxiang'

import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from GUI.v2.lib.common_elements import *
from tests.utils.test_utils import avx_logger
from tests.utils.test_utils import find_files_in_directory
import GUI.v2.site2cloud.s2c_conn as pages


class S2C_Conn_Config(unittest.TestCase):
    """
    Download configuration template for existing Site2Cloud connection
     - Cisco ASA
     - Aviatrix
     - Generic
    """

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(__name__)
        chrome_options = Options()
        # folder used for Chrome to download files
        cls.dir_path = "//home//autopilot//TADownloads"
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

        s2c_conn_name = "ProdConn"
        config1 = {"vendor":"Cisco",
                   "platform":"ASA 5500 Series",
                   "software":"ASA 8.2+"
                   }

        config2 = {"vendor":"Cisco",
                   "platform":"ASA 5500 Series",
                   "software":"ASA 9.x"
                   }

        config3 = {"vendor":"Aviatrix",
                   "platform":"UCC",
                   "software":"1.0"
                   }

        config4 = {"vendor":"Generic",
                   "platform":"Generic",
                   "software":"Vendor independent"
                   }

        # list of all configuration templates to be downloaded
        configs = [config1, config2, config3, config4]

        try:
            # Find the site2cloud connection and click on it
            s2c_view.find_s2c_conn(s2c_conn_name)
            time.sleep(5)

            # Start to download its configuration templates for config 1-4
            for config in configs:
                for keys,values in config.items():
                    self.logger.info("%s : %s" % (keys, values))
                s2c_view.download_config(config["vendor"], config["platform"], config["software"])
                time.sleep(15)
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.debug("Can not find the table with exception %s", str(e))
            assert False

        # Search download folder for all template files starting with 'vpc-01992565'
        download_files = find_files_in_directory(self.dir_path, "vpc-4cf63c25*")
        for file in download_files:
            self.logger.info(file)

        # If the number of downloaded files matches the number of config templates, test passes
        if len(download_files) == len(configs):
            self.logger.info("Total number of configuration files download: %s" % str(len(download_files)))
            assert True
        else:
            self.logger.error("Failed to download all configuration templates")
            assert False

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__ == "__main__":
    unittest.main()