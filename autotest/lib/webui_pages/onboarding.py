import logging
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from autotest.lib.common_elements import *
from autotest.lib.page_locators import *
from autotest.lib.webui_pages.basepage import BasePage

"""
==========================================================================================
For Onboarding
==========================================================================================
"""
class InputCustomerID(InputText):
    locator = OnboardingLocators.CUSTOMER_ID

class InputAccountName(InputText):
    locator = OnboardingLocators.ACCOUNT_NAME

class InputEMail(InputText):
    locator = OnboardingLocators.EMAIL

class InputPassword(InputText):
    locator = OnboardingLocators.PASSWORD

class InputConfirmPaasword(InputText):
    locator = OnboardingLocators.COMFIRM_PASSWORD

class InputAWSAccountNumber(InputText):
    locator = OnboardingLocators.AWS_ACCOUNT_NUMBER

class InputAWSAccessKey(InputText):
    locator = OnboardingLocators.AWS_ACCESS_KEY

class InputAWSSecretKey(InputText):
    locator = OnboardingLocators.AWS_SECRET_KEY

class InputAvtxAppARN(InputText):
    locator = OnboardingLocators.AVTX_APP_ARN

class InputAvtxEC2ARN(InputText):
    locator = OnboardingLocators.AVTX_EC2_ARN

class InputARMSubscriptionID(InputText):
    locator = OnboardingLocators.ARM_SUBSCPT_ID

class InputAppEndpoint(InputText):
    locator = OnboardingLocators.APP_ENDPOINT

class InputClientID(InputText):
    locator = OnboardingLocators.CLIENT_ID

class InputClientSecret(InputText):
    locator = OnboardingLocators.CLIENT_SECRET

class InputGcloudProjectID(InputText):
    locator = OnboardingLocators.GCLOUD_PROJECT_ID

class InputGcloudProjectCredentials(InputText):
    locator = OnboardingLocators.GCLOUD_PROJECT_CREDENTIALS

class InputCloudTrailBucket(InputText):
    locator = OnboardingLocators.GOV_CLOUDTRAIL_BUCKET

class Onboarding(BasePage):
    customer_id = InputCustomerID()
    account_name = InputAccountName()
    email = InputEMail()
    password = InputPassword()
    confirm_password = InputConfirmPaasword()
    aws_account_number = InputAWSAccountNumber()
    aws_access_key =InputAWSAccessKey()
    aws_secret_key = InputAWSSecretKey()
    avtx_app_arn = InputAvtxAppARN()
    avtx_ec2_arn = InputAvtxEC2ARN()
    arm_subscription_id = InputARMSubscriptionID()
    arm_app_endpoint = InputAppEndpoint()
    arm_client_id = InputClientID()
    arm_client_secret = InputClientSecret()
    gcloud_project_id = InputGcloudProjectID()
    gcloud_project_credentials = InputGcloudProjectCredentials()
    cloudtrail_bucket = InputCloudTrailBucket()

    def navigate_to_onboarding(self):
        return Click(OnboardingLocators.NAVIGATE_TO_ONBOARDING).clicking(self.driver)

    def select_cloud_type(self, cloud_name):
        cloud_types = ["AWS","Azure ARM","Gcloud","AWS GOV","Azure Classic","Azure CHINA"]
        if not cloud_name in cloud_types:
            self.logger.error("Invalid Cloud Type. Abort...")
            return False
        if " " in cloud_name:
            cloud_name = cloud_name.replace(" ","_")
        return Click(OnboardingLocators.__dict__[cloud_name.upper()]).clicking(self.driver)

    def fill_create_account_form(self, **kwargs):
        field_list = ["cloud_name","customer_id","account_name", "email", "password", "confirm_password", "account_number", "access_key","secret_key","app_arn","ec2_arn","subscription_id","app_endpoint","client_id","client_secret","project_id","project_credentials","cloudtrail_bucket"]

        for key, value in kwargs.items():
            if not key in field_list:
                self.logger.error("Invalid Gateway configuration fields. Abort...")
                return False
            try:
                if key.lower() == "customer_id":
                    self.customer_id = value
                if key.lower() == "account_name":
                    self.account_name = value
                if key.lower() == "email":
                    self.email = value
                if key.lower() == "password":
                    self.password = value
                if key.lower() == "confirm_password":
                    self.confirm_password = value
                if key.lower() == "account_number":
                    self.aws_account_number = value
                if key.lower() == "access_key":
                    self.aws_access_key = value
                if key.lower() == "secret_key":
                    self.aws_secret_key = value
                if key.lower() == "app_arn":
                    self.avtx_app_arn = value
                if key.lower() == "ec2_arn":
                    self.avtx_ec2_arn = value
                if key.lower() == "subscription_id":
                    self.arm_subscription_id = value
                if key.lower() == "app_endpoint":
                    self.arm_app_endpoint = value
                if key.lower() == "client_id":
                    self.arm_client_id = value
                if key.lower() == "client_secret":
                    self.arm_client_secret = value
                if key.lower() == "project_id":
                    self.gcloud_project_id = value
                if key.lower() == "project_credentials":
                    self.gcloud_project_credentials = value
                if key.lower() == "cloudtrail_bucket":
                    self.cloudtrail_bucket = value

            except NoSuchElementException as e:
                self.logger.exception("Gateway field exception: {}".format(e))
        return True

    def click_save_button(self):
        return Click(OnboardingLocators.SAVE_BUTTON).clicking(self.driver)

    def click_create_button(self):
        return Click(OnboardingLocators.CREATE_BUTTON).clicking(self.driver)