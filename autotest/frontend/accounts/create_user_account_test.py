__author__ = 'reyhong'

import unittest,time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import autotest.lib.webui_pages.user_account as accnt
from autotest.lib.test_utils import *


class CreateUserAccount(unittest.TestCase):
    cases = testcases(__name__)

    @classmethod
    def setUpClass(cls):
        # cls.logger = avx_logger()
        cls.logger = logging.getLogger(__name__)
        # ch = logging.StreamHandler()
        # cls.logger.addHandler(ch)
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.maximize_window()

    def test_set_user_account(self):

        user_account_page = accnt.UserAccount(self.driver, login_required=True)
        time.sleep(5)

        self.logger.info("Navigating to Account")
        user_account_page.navigate_to_account()
        time.sleep(5)

        self.logger.info("Navigating to User Account")
        user_account_page.navigate_to_user_account()
        time.sleep(5)

        self.logger.info("Click the New User Account Button")
        user_account_page.click_new_user_account_button()
        time.sleep(5)

        self.logger.info("Checking account is present in the current view area...")
        # self.assertTrue(cloud_account_page.new_cloud_addount_panel_is_present(), "New Account panel is not found")

        # create cloud account
        time.sleep(3)
        self.cases.start_test('test_case_1')
        self.logger.info("Create User account.....start")

        self.assertTrue(user_account_page.create_user_account(self.cases.case_data),
                        "Create user account failed!")
        self.assertTrue(user_account_page.delete_user_account(self.cases.case_data['user_account']),
                        "delete user account: " + self.cases.case_data['user_account'] + "failed!")

        #if not (popup_win1("Temp stop the program3")):
        #    return False

        self.logger.info("User_account_test confirmed passed")
        self.cases.end_test("test_case_1")

    @classmethod
    def tearDownClass(cls):
        #print("end of the program")
        cls.driver.close()
