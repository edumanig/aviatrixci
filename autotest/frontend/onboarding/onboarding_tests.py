import unittest, logging, time, os
from selenium import webdriver
import autotest.lib.webui_pages.onboarding as onbding
import autotest.lib.webui_pages.account as accnt
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
from autotest.run_autotest import cloud_account
from autotest.lib.test_utils import testcases


class OnboardingTests(WebUITest):
    cases = testcases(__name__)
    case_list = cases.data

    def test_add_customer_id(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        onboarding_view = onbding.Onboarding(self.driver)

        self.logger.info("Navigate to Onboarding")
        onboarding_view.navigate_to_onboarding()
        time.sleep(5)

        self.cases.start_test("test_case_1")
        self.logger.info("Select AWS to Enter Customer ID")
        onboarding_view.select_cloud_type(self.cases.case_data['cloud_name'])
        time.sleep(5)
        onboarding_view.customer_id = self.cases.case_data['customer_id']
        self.logger.info("Click Save button")
        onboarding_view.click_save_button()

        self.logger.info("Checking the result of creating new gateway...")
        result = actions_in_common.get_message()
        self.assertEqual(self.cases.expected_result['toaster'], result,
                      "Fail to save customer id")
        actions_in_common.close_message()
        self.cases.end_test("test_case_1")
        self.cases.data.pop("test_case_1",None)


    def test_create_accounts(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        onboarding_view = onbding.Onboarding(self.driver)
        accnt_view = accnt.Account(self.driver)

        self.logger.info("start to create an account for specified cloud type")

        for case in self.case_list:

            self.cases.start_test(case)

            if 'account_number' in self.cases.case_data:
                self.cases.case_data['account_number'] = cloud_account['aws_account_info']['account_number']
            if 'access_key' in self.cases.case_data:
                self.cases.case_data['access_key'] = cloud_account['aws_account_info']['access_keyid']
            if 'secret_key' in self.cases.case_data:
                self.cases.case_data['secret_key'] = cloud_account['aws_account_info']['secret_key']
            if 'subscription_id' in self.cases.case_data:
                self.cases.case_data['subscription_id'] = cloud_account['azure_account_info']['subscription_id']
            if 'app_endpoint' in self.cases.case_data:
                self.cases.case_data['app_endpoint'] = cloud_account['azure_account_info']['tenant_id']
            if 'client_id' in self.cases.case_data:
                self.cases.case_data['client_id'] = cloud_account['azure_account_info']['client_id']
            if 'client_secret' in self.cases.case_data:
                self.cases.case_data['client_secret'] = cloud_account['azure_account_info']['client_secret']
            if 'project_id' in self.cases.case_data:
                self.cases.case_data['project_id'] = cloud_account['gcloud_account_info']['project_id']
            if 'project_credentials' in self.cases.case_data:
                self.cases.case_data['project_credentials'] = os.path.abspath(cloud_account['gcloud_account_info']['project_credentials'])

            self.logger.info("Create an account for {}".format(self.cases.case_data['cloud_name']))
            onboarding_view.select_cloud_type(self.cases.case_data['cloud_name'])
            time.sleep(5)

            assert onboarding_view.fill_create_account_form(**self.cases.case_data), "Failed to fill Create Account form"

            time.sleep(1)
            self.logger.info("Click Create button to submit Create Account form")
            self.assertTrue(onboarding_view.click_create_button(), "Failed to click Create button")

            self.logger.info("Checking the result of creating new account...")
            result = actions_in_common.get_message()
            self.assertEqual(self.cases.expected_result['toaster']+ self.cases.case_data['email'], result, "Fail to create an account")
            actions_in_common.close_message()

            time.sleep(10) # wait for new account to be reflected in the account table
            self.logger.info("Verify the account in Accounts > Cloud Accounts")
            accnt_view.navigate_to_account()
            accnt_view.navigate_to_cloud_account()
            time.sleep(3)
            self.assertIn(accnt_view.cloud_account_table.check_specific_row_data(self.driver,self.cases.case_data['account_name'],2),self.cases.case_data['cloud_name']+',',"Failed to find the account or cloud type is incorrect")

            self.logger.info("Delete the account")
            self.assertTrue(accnt_view.delete_cloud_account(self.cases.case_data['account_name']))

            self.cases.end_test(case)

            self.logger.info("Navigate to Onboarding")
            onboarding_view.navigate_to_onboarding()
            time.sleep(5)
