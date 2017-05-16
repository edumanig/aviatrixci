__author__ = 'reyhong'

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
        BasePage.process_login(self)

class ActionsInCommon(AccBasePage):
    def __init__(self, driver, login_required=False):
        self.driver = driver
        AccBasePage.__init__(self, self.driver, login_required=login_required)

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


class InputUserAccountName(InputText):
    locator = UserAccountViewLocators.USER_ACCOUNT_NAME


class InputUserAccountEmail(InputText):
    locator = UserAccountViewLocators.USER_ACCOUNT_EMAIL


class SelectCloudAccountName(DropdownSelect):
    locator = UserAccountViewLocators.CLOUD_ACCOUNT_NAME_SELECT


class InputUserAccountPW(InputText):
    locator = UserAccountViewLocators.USER_ACCOUNT_PW


class InputUserAccountPW2(InputText):
    locator = UserAccountViewLocators.USER_ACCOUNT_PW2


# Account related class
class UserAccount(AccBasePage):

    input_user_account_name = InputUserAccountName()
    input_user_account_email = InputUserAccountEmail()
    select_cloud_account = SelectCloudAccountName()
    input_user_account_pw = InputUserAccountPW()
    input_user_account_pw2 = InputUserAccountPW2()
    read_user_account_table = TableData(UserAccountViewLocators.USER_ACCOUNT_INFO_TABLE)

    def __init__(self, driver, login_required=False):
        self.driver = driver
        BasePage.__init__(self, self.driver, login_required=login_required)
        self.logger = logging.getLogger(__name__)
        self.commonaction = ActionsInCommon(self.driver, True)

    # Fine the Account menu and click on it
    def navigate_to_account(self):
        try:
            account_button = self.driver.find_element(*UserAccountViewLocators.NAVIGATE_TO_USER_ACCOUNT)
            account_button.click()
        except NoSuchElementException:
            self.logger.exception("Could not navigate to user account menu")

    # Fine the Cloud Account menu and click on it
    def navigate_to_user_account(self):
        try:
            account_button = self.driver.find_element(*UserAccountViewLocators.NAVIGATE_TO_USER_ACCOUNT_TEXT)
            account_button.click()
        except NoSuchElementException:
            self.logger.exception("Could not navigate to user account menu")


    def click_new_user_account_button(self):
        try:
            new_account_button = self.driver.find_element(*UserAccountViewLocators.NEW_USER_ACCOUNT_BUTTON)
            new_account_button.click()
        except (WebDriverException, NoSuchElementException):
            self.logger.exception("Could not click New user Account button")

    def click_new_user_ok_button(self):
        return Click(UserAccountViewLocators.OK_BUTTON).clicking(self.driver)

    def new_user_account_panel_is_present(self):
        try:
            account_panel = self.driver.find_element(*UserAccountViewLocators.NEW_User_ACCOUNT_PANEL)
            if account_panel:
                return True
            return False
        except NoSuchElementException:
            self.logger.exception("Could not find New user account panel")

    # will get result message (no use)
    def is_new_user_account_created(self):
        try:
            ui.WebDriverWait(self.driver, 360).until(
                EC.visibility_of_element_located(*UserAccountViewLocators.USER_ACCOUNT_CREATED_MESSAGE))
            result_message = self.driver.find_element(*UserAccountViewLocators.USER_ACCOUNT_CREATED_MESSAGE)
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
                        self.logger.info("Site2Cloud connection %s found", name)
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
    def create_user_account(self, data ):
        #from tests.main import variables as _variables
        driver = self.driver
        #print("The user_account_name is:", user_account_name)
        try:
            self.logger.info("input user account name:" + data['user_account'])
            self.input_user_account_name = data['user_account']

            # input account email
            self.logger.info("input user account email:" + data["account_email"])
            self.input_user_account_email = data["account_email"]

            self.logger.info("select cloud account name:" + data['cloud_account'])
            self.select_cloud_account = data['cloud_account']

            # input account password
            self.logger.info("input user account password:" + data['cloud_account'])
            self.input_user_account_pw = data["account_password"]

            # input account password2
            self.logger.info("input user account password2:" + data["account_password"])
            self.input_user_account_pw2 = data["account_password"]

        except Exception as e:
            self.logger.exception("Can not create user account with exception %s", str(e))
            return False

        time.sleep(3)
        self.logger.info("click create user account button")
        assert self.click_new_user_ok_button(), "OK summit button is not found"

        expected_message = "successfully"
        if expected_message not in self.commonaction.get_message():
            self.logger.error("Can't find excepted toast message: " + expected_message)
            return False

        self.logger.info("Get toast message: " + self.commonaction.get_message())
        self.logger.info("Found excepted toast message: " + expected_message)

        self.logger.info("Close toast message")
        self.commonaction.close_message()

        # need to check the result of all the user account
        # read back whole tr contain the key word account name: _variables["cloudn_account_name"]

        user_account_result = self.read_user_account_table.get_table_data(self.driver)
        user_account_result2 = [y for x in user_account_result for y in x]
        self.logger.info("The table result is: %s" + str(','.join(user_account_result2)))

        # search whole table list
        # need to search for the acocunt name
        row_num = ""

        # get row number of the user
        for i in user_account_result:
            if data["user_account"] == i[0]:
                # self.logger.info("Found account name: "+ i[0])
                row_num = str((user_account_result.index(i)))
                break

        if not row_num:
            self.logger.error("Can't find user account name:" + data["user_account"])
            return False

        if data["user_account"] in user_account_result[int(row_num)][0]:
            self.logger.info("Found account name:" + data["user_account"])

        else:
            self.logger.error("Can't find account name:" + data["user_account"])
            return False

        # known issue: can't display the email  !!!! Mantis ID: 1409
        if data["account_email"] in user_account_result[int(row_num)][1]:
            self.logger.info("Found user account Email name:" + data["account_email"])

        else:
            self.logger.error("Can't find account Email name:" + data["account_email"])
            self.logger.info("Currently won't fail the test")
            # return False

        # check Cloud Account name present:
        if data['cloud_account'] in user_account_result[int(row_num)][2]:
            self.logger.info("Found cloud account: " + data['cloud_account'])
        else:
            self.logger.error("Can't find account: " + data['cloud_account'])
            return False

        self.logger.info("Create_user_account passed")
        return True

    def delete_user_account(self, user_account_name):
        self.logger.info("delete_user_account")
        try:
            table = self.driver.find_element(*UserAccountViewLocators.USER_ACCOUNT_INFO_TABLE)
            td_index = self.find_delete_col(table)

            ##for s2c_conn_name in s2c_conn_names:
            tr_index = self.find_delete_row(table, user_account_name)
            self.logger.info("Click 'Delete' button for User account %s", user_account_name)
            xpath = "//table/tbody/tr["+str(tr_index)+"]/td["+str(td_index)+"]/button"
            table.find_element_by_xpath(xpath).click()
            time.sleep(2)

            self.commonaction.confirm_delete()

            time.sleep(2)
            toaster_result = self.commonaction.get_message().lower()
            assert ("has been deleted" in toaster_result), "Fail to delete "+user_account_name

            self.logger.info("Close toast message")
            self.commonaction.close_message()

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.exception("Can not find the table with exception %s", str(e))
            return False

        self.logger.info("delete_user_account passed")
        return True


