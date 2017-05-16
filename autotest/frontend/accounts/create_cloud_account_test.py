
import unittest
import logging
import time, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import autotest.lib.webui_pages.account as accnt
from autotest.run_autotest import cloud_account
from autotest.lib.test_utils import *


class CreateCloudAccount(unittest.TestCase):
    cases = testcases(__name__)

    @classmethod
    def setUpClass(cls):
        #cls.logger = avx_logger()
        cls.logger = logging.getLogger(__name__)
        # ch = logging.StreamHandler()
        # cls.logger.addHandler(ch)
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.maximize_window()

    def test_set_cloud_account(self):
        cloud_account_page = accnt.Account(self.driver, login_required=True)
        time.sleep(5)

        self.logger.info("Navigating to Account")
        cloud_account_page.navigate_to_account()
        time.sleep(5)

        self.logger.info("Navigating to Cloud Account")
        cloud_account_page.navigate_to_cloud_account()
        time.sleep(5)

        self.logger.info("Click the New Cloud Account Button")
        cloud_account_page.click_new_cloud_account_button()
        time.sleep(5)

        self.logger.info("Checking account is present in the current view area...")
        # self.assertTrue(cloud_account_page.new_cloud_addount_panel_is_present(), "New Account panel is not found")

        # create cloud account
        time.sleep(3)
        self.cases.start_test("test_case_1")
        self.logger.info("Create cloud account.....start")

        self.cases.case_data["aws_account_number"] = cloud_account["aws_account_info"]["account_number"]
        self.cases.case_data["aws_access_keyid"] = cloud_account["aws_account_info"]["access_keyid"]
        self.cases.case_data["aws_secret_key"] = cloud_account["aws_account_info"]["secret_key"]
        self.cases.case_data["azure_subscript_id"] = cloud_account["azure_account_info"]["subscription_id"]
        self.cases.case_data["arm_tenant_id"] = cloud_account["azure_account_info"]["tenant_id"]
        self.cases.case_data["arm_client_id"] = cloud_account["azure_account_info"]["client_id"]
        self.cases.case_data["arm_client_secret"] = cloud_account["azure_account_info"]["client_secret"]
        self.cases.case_data["gce_project_id"] = cloud_account["gcloud_account_info"]["project_id"]
        self.cases.case_data["gce_credential"] = os.path.abspath(cloud_account["gcloud_account_info"]["project_credentials"])


        self.assertTrue(cloud_account_page.create_cloud_account(self.cases.case_data,aws=True, arm=True, gce=True, azure=True, azurecn=False, awsgov=False), "Create cloud account failed!")
        self.cases.end_test("test_case_1")
        self.cases.start_test("test_case_2")
        self.assertTrue(cloud_account_page.delete_cloud_account(self.cases.case_data["account_name"]), "delete cloud account: "+self.cases.case_data["account_name"]+"failed!")
        self.cases.end_test("test_case_2")

        self.logger.info("Cloud_account_test confirmed passed")

    @classmethod
    def tearDownClass(cls):
        #print("end of the program")
        cls.driver.close()

