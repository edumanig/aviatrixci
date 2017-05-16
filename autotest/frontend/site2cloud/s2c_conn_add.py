__author__ = 'lmxiang'

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from autotest.lib.common_elements import *
import autotest.lib.webui_pages.site2cloud.s2c_conn as pages
from autotest.lib.test_utils import testcases


class S2C_Conn_Add(unittest.TestCase):
    """
    Add new site2cloud connection
    """
    cases = testcases(__name__)
    case_list = cases.data

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(pages.__name__)
        #cls.logger =avx_logger()
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        #cls.driver.maximize_window()

    def test_s2c_add(self):
        self.logger.info("Start Adding Site2Cloud Connection")

        s2c_view = pages.S2C_New(self.driver, login_required=True)
        self.logger.info("Navigating to Site2Cloud")
        s2c_view.navigate_to_s2c()
        time.sleep(10)

        self.logger.info("Check if Site2Cloud is present in the current view area...")
        assert s2c_view.match_view_title(),"Site2Cloud view is not present"

        self.logger.info("Fill site2cloud connection creation data")

        for case in sorted(self.case_list):

            self.cases.start_test(case)
            """
            if data['HA'].lower() == "enable" and s2c_view.is_ha_enabled():
                self.logger.info("Site2Cloud HA is already enabled. No action needed...")
            elif data['HA'].lower() == "enable" and not s2c_view.is_ha_enabled():
                self.logger.info("Site2Cloud HA is disabled. Enable it now...")
                time.sleep(5)
                s2c_view.ha_switch_button = "select"
                toaster_result = s2c_view.s2c_toaster.lower()
                assert ("success" in toaster_result), "Fail to enable HA"
                time.sleep(5)
            elif data['HA'].lower() == "disable" and not s2c_view.is_ha_enabled():
                self.logger.info("Site2Cloud HA is already disabled. No action needed...")
            elif data['HA'].lower() == "disable" and s2c_view.is_ha_enabled():
                self.logger.info("Site2Cloud HA is enabled. Disable it now...")
                self.logger.info("Disable Site2Cloud HA...")
                time.sleep(5)
                s2c_view.ha_switch_button = "deselect"
                time.sleep(10)
                toaster_result = s2c_view.s2c_toaster.lower()
                assert ("success" in toaster_result), "Fail to disable HA"
                time.sleep(5)
            else:
                self.logger.error("Wrong value for HA. Either 'enable' or 'disable'. Abort...")
                return False
            """
            self.logger.info("Click 'Add New' button to create a new site2cloud connection...")
            s2c_view.new_button = "new"
            time.sleep(10)

            assert s2c_view.fill_conn_fields(**self.cases.case_data),"Fail to fill in Site2Cloud connection fields"
            s2c_view.ok_button = "ok"
            time.sleep(10)
            toaster_result = s2c_view.s2c_toaster.lower()
            assert (self.cases.expected_result['toaster'] in toaster_result),"Fail to create Site2Cloud connection: "+toaster_result
            time.sleep(10)

            self.cases.end_test(case)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__ == "__main__":
    unittest.main()