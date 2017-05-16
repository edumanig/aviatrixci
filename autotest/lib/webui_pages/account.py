import logging
import time
import unittest
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from autotest.lib.common_elements import *
from autotest.lib.page_locators import *

# from AviatrixTesting.tests.UCC.UCCWebUI.lib.page_locators import AccountViewLocators

class AccBasePage(BasePage):
    def __init__(self, driver, login_required=False):
        self.driver = driver
        BasePage.__init__(self, self.driver, login_required=login_required)
        self.logger = logging.getLogger(__name__)
        if login_required:
            BasePage.process_login(self)

class ActionsInCommon(AccBasePage):
    def __init__(self, driver, login_required=False):
        self.driver = driver
        AccBasePage.__init__(self, self.driver)

    #def __init__(self, driver, login_required=False):
    #    super(driver, login_required)

    def match_view_title(self,sub_title):
        try:
            view_title = self.driver.find_element(*ActionsInCommonLocators.VIEW_TITLE)
            return view_title.text.lower() == sub_title
        except NoSuchElementException:
            self.logger.exception("Could not view the settings for {}".format(sub_title))

    def click_ok_button(self):
        try:
            ok_button = self.driver.find_element(*ActionsInCommonLocators.SUBMIT_OK_BUTTON)
            if ok_button:
                ok_button.submit()
                return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception("Failed to submit")
            return False

    def click_cancel_button(self):
        try:
            cancel_button = self.driver.find_element(*ActionsInCommonLocators.SUBMIT_CANCEL_BUTTON)
            cancel_button.click()
        except (WebDriverException,NoSuchElementException):
            self.logger.exception("Failed to cancel")

    def cancel_delete(self):
        try:
            ui.WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(ActionsInCommonLocators.CONFIRM_POPUP))
            cancel_button = self.driver.find_element(*ActionsInCommonLocators.CONFIRM_CANCEL)
            cancel_button.click()
        except TimeoutException:
            self.logger.exception("Could not find the one for deletion.")

    def confirm_delete(self):
        try:
            ui.WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(ActionsInCommonLocators.CONFIRM_POPUP))
            ok_button = self.driver.find_element(*ActionsInCommonLocators.CONFIRM_OK)
            if ok_button:
                ok_button.click()
                return True
        except TimeoutException:
            self.logger.exception("Could not find the one for deletion.")
            return False

    # for toast message
    def get_message(self):
        try:
            ui.WebDriverWait(self.driver, 300).until(
                EC.visibility_of_element_located(ActionsInCommonLocators.TOASTER_MESSAGE))
            result_message = self.driver.find_element(*ActionsInCommonLocators.TOASTER_MESSAGE)
            return result_message.text
        except TimeoutException:
            self.logger.exception("Failed to get the resulting message of the action.")

    def close_message(self):
        try:
            close_msg = self.driver.find_element(*ActionsInCommonLocators.CLOSE_MESSGAE)
            close_msg.click()
        except WebDriverException:
            self.logger.exception("Failed to dismiss the message box.")

    def check_toaster_has_close(self):
    #check for presence of the toaster after is is closed to prevent toaster piling up
        try:
            ui.WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(ActionsInCommonLocators.TOASTER_MESSAGE))
            ok_button = self.driver.find_element(*ActionsInCommonLocators.TOASTER_MESSAGE)
            return False
        except (WebDriverException,NoSuchElementException):
            self.logger.exception("Successfully closed toaster")
            return True

    def spinning_wheel(self):
        try:
            ui.WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    ActionsInCommonLocators.SPINNING_WHEEL))
            page_spinner = self.driver.find_element(*ActionsInCommonLocators.SPINNING_WHEEL)
            while page_spinner.is_displayed() == True:
                time.sleep(1)
            return True

        except StaleElementReferenceException:
            self.logger.exception("Stale element error")
            return False
        except:
            self.logger.exception("Other exception check note")
            return False


class InputAccountName(InputText):
    locator = AccountViewLocators.NEW_CLOUD_ACCOUNT_NAME

class InputAccountEmail(InputText):
    locator = AccountViewLocators.NEW_ACCOUNT_EMAIL

class InputAccountPW(InputText):
    locator = AccountViewLocators.NEW_ACCOUNT_PW

class InputAccountPW2(InputText):
    locator = AccountViewLocators.NEW_ACCOUNT_PW2

# AWS
class CheckAWS(Checkbox):
    selectedlocator = AccountViewLocators.AWS_ACCOUNT_CHECKBOX_IS_SELECTED
    clicklocator = AccountViewLocators.AWS_ACCOUNT_CHECKBOX_CLICK

class AWSAccountNum(InputText):
    locator = AccountViewLocators.AWS_ACCOUNT_NUM

class AWSAccocuntAccKey(InputText):
    locator = AccountViewLocators.AWS_ACCOUNT_ACCESS_KEY

class AWSAccocuntsecKey(InputText):
    locator = AccountViewLocators.AWS_ACCOUNT_SECRET_KEY

#GCE
class CheckGCE(Checkbox):
    selectedlocator = AccountViewLocators.GCE_ACCOUNT_CHECKBOX_IS_SELECTED
    clicklocator = AccountViewLocators.GCE_ACCOUNT_CHECKBOX_CLICK

class GCEProjectID(InputText):
    locator = AccountViewLocators.GCE_ACCOUNT_PROJECT_ID

class GCECredential(InputText):
    locator = AccountViewLocators.GCE_ACCOUNT_CREDENTIALS

#ARM
class CheckARM(Checkbox):
    selectedlocator = AccountViewLocators.ARM_ACCOUNT_CHECKBOX_IS_SELECTED
    clicklocator = AccountViewLocators.ARM_ACCOUNT_CHECKBOX_CLICK

class ARMSubID(InputText):
    locator = AccountViewLocators.ARM_ACCOUNT_SUB_ID

class ARMTenantID(InputText):
    locator = AccountViewLocators.ARM_TENANT_ID

class ARMClientID(InputText):
    locator = AccountViewLocators.ARM_CLIENT_ID

class ARMClientSecID(InputText):
    locator = AccountViewLocators.ARM_CLIENT_SECRET

#GOV
class CheckGOV(Checkbox):
    selectedlocator = AccountViewLocators.GOV_ACCOUNT_CHECKBOX_IS_SELECTED
    clicklocator = AccountViewLocators.GOV_ACCOUNT_CHECKBOX_CLICK

class GOVAccountNum(InputText):
    locator = AccountViewLocators.GOV_ACCOUNT_NUM

class GOVAccocuntAccKey(InputText):
    locator = AccountViewLocators.GOV_ACCOUNT_ACCESS_KEY

class GOVAccocuntsecKey(InputText):
    locator = AccountViewLocators.GOV_ACCOUNT_SECRET_KEY

class GOVTrailBucket(InputText):
    locator = AccountViewLocators.GOV_TRAIL_BUCKET

#Azure
class CheckAzure(Checkbox):
    selectedlocator = AccountViewLocators.AZURE_ACCOUNT_CHECKBOX_IS_SELECTED
    clicklocator = AccountViewLocators.AZURE_ACCOUNT_CHECKBOX_CLICK

class AzureSubID(InputText):
    locator = AccountViewLocators.AZURE_ACCOUNT_SUB_ID

#Azure China
class CheckAzureCN(Checkbox):
    selectedlocator = AccountViewLocators.AZCN_ACCOUNT_CHECKBOX_IS_SELECTED
    clicklocator = AccountViewLocators.AZCN_ACCOUNT_CHECKBOX_CLICK

class AzureCNSubID(InputText):
    locator = AccountViewLocators.AZCN_ACCOUNT_SUB_ID

# Account related class
class Account(AccBasePage):

    input_account_name = InputAccountName()
    input_account_email = InputAccountEmail()
    input_account_pw = InputAccountPW()
    input_account_pw2 = InputAccountPW2()
    check_aws_cloud = CheckAWS()

    input_aws_account_num = AWSAccountNum()
    input_aws_access_key = AWSAccocuntAccKey()
    input_aws_secret_key = AWSAccocuntsecKey()

    check_gce_cloud = CheckGCE()
    input_gce_projectid = GCEProjectID()
    input_gce_credential = GCECredential()

    check_arm_cloud = CheckARM()
    input_arm_subid = ARMSubID()
    input_arm_tenantid = ARMTenantID()
    input_arm_clientid = ARMClientID()
    input_arm_secid = ARMClientSecID()

    check_gov_cloud = CheckGOV()
    input_gov_account_num = GOVAccountNum()
    input_gov_access_key = GOVAccocuntAccKey()
    input_gov_sec_key = GOVAccocuntsecKey()
    input_gov_bucket = GOVTrailBucket()

    check_azure_cloud = CheckAzure()
    input_azure_subid = AzureSubID()

    check_azcn_cloud = CheckAzureCN()
    input_azcn_subid = AzureCNSubID()
    read_account_table = TableData(AccountViewLocators.ACCOUNT_INFO_TABLE)
    cloud_account_table = TableData(AccountViewLocators.ACCOUNT_TABLE_FOR_DATA)

    def __init__(self, driver, login_required=False):
        self.driver = driver
        AccBasePage.__init__(self, self.driver, login_required=login_required)
        self.logger = logging.getLogger(__name__)
        self.commonaction = ActionsInCommon(self.driver)

    # Fine the Account menu and click on it
    def navigate_to_account(self):
        try:
            account_button = self.driver.find_element(*AccountViewLocators.NAVIGATE_TO_CLOUD_ACCOUNT)
            account_button.click()
        except NoSuchElementException:
            self.logger.exception("Could not navigate to account menu")

    # Fine the Cloud Account menu and click on it
    def navigate_to_cloud_account(self):
        try:
            account_button = self.driver.find_element(*AccountViewLocators.NAVIGATE_TO_CLOUD_ACCOUNT_TEXT)
            account_button.click()
        except NoSuchElementException:
            self.logger.exception("Could not navigate to cloud account menu")


    def click_new_cloud_account_button(self):
        try:
            new_account_button = self.driver.find_element(*AccountViewLocators.NEW_CLOUD_ACCOUNT_BUTTON)
            new_account_button.click()
        except (WebDriverException, NoSuchElementException):
            self.logger.exception("Could not click New Cloud Account button")

    def new_cloud_account_panel_is_present(self):
        try:
            #todo (need to finish)
            account_panel = self.driver.find_element(*AccountViewLocators.NEW_ACCOUNT_PANEL)
            if account_panel:
                return True
            return False
        except NoSuchElementException:
            self.logger.exception("Could not find New account panel")

    # will get result message (no use)
    def is_new_account_created(self):
        try:
            ui.WebDriverWait(self.driver, 360).until(
                EC.visibility_of_element_located(*AccountViewLocators.ACCOUNT_CREATED_MESSAGE))
            result_message = self.driver.find_element(*AccountViewLocators.ACCOUNT_CREATED_MESSAGE)
            return result_message.text
        except TimeoutException:
            self.logger.exception("Failed to locate toast message")

    # copy from Liming's s2c
    def find_delete_row(self, table, name):
        """
        Find the row of the site2cloud connection to be deleted in the table
        :param table:  table
        :param name:  name
        :return: row number of the name target
        """
        tr_index = 0
        tr_index_found = 0
        trs = table.find_elements_by_tag_name('tr')
        for tr in trs:
            tds = tr.find_elements_by_tag_name('td')
            if tds:
                for td in tds:
                    if td.text == name:
                        self.logger.info("Account name %s found", name)
                        tr_index_found = tr_index_found + 1
                        break
            if tr_index_found:
                break
            else:
                tr_index = tr_index + 1
        return tr_index

    def find_delete_col(self, table):
        """
        Find the column of the 'delete' button in table
        :param table object: table
        :return: column number of 'delete' button in the table
        """
        td_index = 1
        td_index_found = 0
        trs = table.find_elements_by_tag_name('tr')
        for tr in trs:
            ths = tr.find_elements_by_tag_name('th')
            if ths:
                for th in ths:
                    if not th.text:
                        td_index_found = td_index_found + 1
                        break
                    td_index = td_index + 1
            if td_index_found:
                break
        return td_index

    # must work with new create panel is showing up
    def create_cloud_account(self, data,aws=True, azure=False, arm=False, azurecn=False, awsgov=False, gce=False):
        self.data = data
        driver = self.driver


        # time.sleep(5)
        # input account name
        try:
            self.logger.info("input account name:" + self.data["account_name"])
            self.input_account_name = self.data["account_name"]

            # input account email
            self.logger.info("input account email:" + self.data["account_email"])
            self.input_account_email = self.data["account_email"]

            # input account password
            self.logger.info("input account password:" + self.data["account_password"])
            self.input_account_pw = self.data["account_password"]

            # input account password2
            self.logger.info("input account password2:" + self.data["account_password"])
            self.input_account_pw2 = self.data["account_password"]

        except Exception as e:
            self.logger.debug("Can not create account  with exception %s", str(e))
            return False


        try:
            if aws:
                self.logger.info("click cloud type: AWS")
                self.check_aws_cloud = "select"
                time.sleep(3)
                self.logger.info("input AWS account number:" + self.data["aws_account_number"][:6])
                self.input_aws_account_num = self.data["aws_account_number"]
                time.sleep(3)
                self.logger.info("input AWS access key:" + self.data["aws_access_keyid"][:6])
                self.input_aws_access_key = self.data["aws_access_keyid"]
                time.sleep(3)
                self.logger.info("input AWS secret key:" + self.data["aws_secret_key"][:6])
                self.input_aws_secret_key = self.data["aws_secret_key"]
                time.sleep(3)
            if azure:
                self.logger.info("click cloud type: Azure")
                self.check_azure_cloud = "select"
                time.sleep(3)
                self.logger.info("input Azure subscription number:" + self.data["azure_subscript_id"][:6])
                self.input_azure_subid = self.data["azure_subscript_id"]
                time.sleep(3)

            if arm:
                self.logger.info("click cloud type: Azure RM")
                self.check_arm_cloud = "select"
                time.sleep(3)
                self.logger.info("input ARM subscription number:" + self.data["azure_subscript_id"][:6])
                self.input_arm_subid = self.data["azure_subscript_id"]
                time.sleep(3)
                self.logger.info("input ARM tenant ID:" + self.data["arm_tenant_id"][:6])
                self.input_arm_tenantid = self.data["arm_tenant_id"]
                time.sleep(3)
                self.logger.info("input ARM client ID:" + self.data["arm_client_id"][:6])
                self.input_arm_clientid = self.data["arm_client_id"]
                time.sleep(3)
                # if any valuable contain "=" in config need to be added individual
                self.logger.info("input ARM client secret:" + self.data["arm_client_secret"][:6])
                self.input_arm_secid = self.data["arm_client_secret"]

            if azurecn:
                self.logger.info("click cloud type: Azure China")
                self.check_azcn_cloud = "select"
                time.sleep(3)
                self.logger.info("input Azure China subscription number:" + self.data["azurecn_subscript_id"][:6])
                self.input_arm_subid = self.data["azurecn_subscript_id"]
                time.sleep(3)

            if awsgov:
                self.logger.info("click cloud type: AWS GOV")
                self.check_gov_cloud = "select"
                time.sleep(3)
                self.logger.info("input AWS GOV account number:" + self.data["aws_gov_account_number"][:6])
                self.input_gov_account_num = self.data["aws_gov_account_number"]
                time.sleep(3)
                self.logger.info("input AWS GOV access key:" + self.data["aws_gov_access_keyid"][:6])
                self.input_gov_access_key = self.data["aws_gov_access_keyid"]
                time.sleep(3)
                self.logger.info("input AWS GOV secret key:" + self.data["aws_gov_secret_key"][:6])
                self.input_gov_sec_key = self.data["aws_gov_secret_key"]
                time.sleep(3)
                self.logger.info("input AWS GOV secret key:" + self.data["aws_gov_bucket"][:6])
                self.input_gov_bucket = self.data["aws_gov_bucket"]

            if gce:
                self.logger.info("click cloud type: Google cloud")
                self.check_gce_cloud = "select"
                time.sleep(3)
                self.logger.info("input GCE project ID:" + self.data["gce_project_id"][:6])
                self.input_gce_projectid = self.data["gce_project_id"]
                time.sleep(3)
                self.logger.info("input GCE credential:" + self.data["gce_credential"][:6])
                self.input_gce_credential = self.data["gce_credential"]

        except NoSuchElementException as e:
                self.logger.exception("Create Account input fields exception: %s", str(e))
                return False

        time.sleep(3)
        self.logger.info("click create account button")
        assert self.commonaction.click_ok_button(), "OK summit button is not found"

        # expected_message = "An email with instructions has been sent to " + self.data["cloudn_account_email"]
        expected_message = self.data["account_email"]

        if not expected_message in self.commonaction.get_message():
            self.logger.info("Can't find excepted toast message: " + expected_message)
            return False

        self.logger.info("Get toast message: " + self.commonaction.get_message())
        self.logger.info("Found excepted toast message: " + expected_message)

        self.logger.info("Close toast message")
        self.commonaction.close_message()




        # need to check the result of all the account
        # read back whole tr contain the key word account name: self.data["cloudn_account_name"]

        account_result = self.read_account_table.get_table_data(self.driver)
        account_result2 = [y for x in account_result for y in x]
        self.logger.info("The table result is: %s" + str(','.join(account_result2)))

        # print("The table result is: ", account_result)

        # search whole table list
        # need to search for the acocunt name
        row_num = ""

        for i in account_result:
            if self.data["account_name"] == i[0]:
                # self.logger.info("Found account name: "+ i[0])
                row_num = str((account_result.index(i)))
                break


        if not row_num:
            self.logger.info("Can't find account name:" + self.data["account_name"])
            return False


        if self.data["account_name"] in account_result[int(row_num)][0]:
            self.logger.info("Found account name:" + self.data["account_name"])

        else:
            self.logger.info("Can't find account name:" + self.data["account_name"])
            return False

        if self.data["account_email"] in account_result[int(row_num)][1]:
            self.logger.info("Found account Email name:" + self.data["account_email"])

        else:
            self.logger.info("Can't find account Email name:" + self.data["account_email"])
            return False

        # check Account type present:
        if aws:
            if "AWS" in account_result[int(row_num)][2]:
                self.logger.info("Found account type AWS")
            else:
                self.logger.info("Can't find account type AWS")
                return False

        if azure:
            if "Azure Classic" in account_result[int(row_num)][2]:
                self.logger.info("Found account type Azure Classic")
            else:
                self.logger.info("Can't find account type Azure Classic")
                return False

        if arm:
            if "Azure ARM" in account_result[int(row_num)][2]:
                self.logger.info("Found account type Azure ARM")
            else:
                self.logger.info("Can't find account type Azure ARM")
                return False

        if azurecn:
            if "Azure CHINA" in account_result[int(row_num)][2]:
                self.logger.info("Found account type Azure CHINA")
            else:
                self.logger.info("Can't find account type Azure CHINA")
                return False

        if awsgov:
            if "AWS GOV" in account_result[int(row_num)][2]:
                self.logger.info("Found account type AWS GOV")
            else:
                self.logger.info("Can't find account type AWS GOV")
                return False

        if gce:
            if "Gcloud" in account_result[int(row_num)][2]:
                self.logger.info("Found account type Gcloud")
            else:
                self.logger.info("Can't find account type Gcloud")
                return False

        self.logger.info("Create_cloud_account passed")
        return True

    def delete_cloud_account(self, account_name):
        self.logger.info("delete_cloud_account")
        try:
            table = self.driver.find_element(*AccountViewLocators.ACCOUNT_INFO_TABLE)
            td_index = self.find_delete_col(table)

            ##for s2c_conn_name in s2c_conn_names:
            tr_index = self.find_delete_row(table, account_name)
            self.logger.debug("Click 'Delete' button for Cloud account %s", account_name)
            xpath = "//table/tbody/tr["+str(tr_index)+"]/td["+str(td_index)+"]/button"
            table.find_element_by_xpath(xpath).click()
            time.sleep(2)

            self.commonaction.confirm_delete()

            time.sleep(2)
            toaster_result = self.commonaction.get_message().lower()
            assert ("has been deleted" in toaster_result), "Fail to delete "+account_name

            self.logger.info("Close toast message")
            self.commonaction.close_message()

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.debug("Can not find the table with exception %s", str(e))
            return False

        self.logger.info("delete_cloud_account passed")
        return True


