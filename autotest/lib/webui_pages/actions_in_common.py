import logging
from lxml import etree
from lxml.cssselect import CSSSelector
from collections import OrderedDict
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
For all actions in common
==========================================================================================
"""
class InputPassphrase(InputText):
    locator = ActionsInCommonLocators.ENABLE_SSH

class ActionsInCommon(BasePage):
    input_passphrase = InputPassphrase()

    def enable_ssh(self,passph):
        try:
            ui.WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(ActionsInCommonLocators.PASSPHRASE_FORM))
            pass_form = self.driver.find_element(*ActionsInCommonLocators.PASSPHRASE_FORM)
            if pass_form:
                self.input_passphrase = passph
        except TimeoutException:
            self.logger.exception("Took too long to load Enable SSH page")

    def match_view_title(self,sub_title):
        try:
            view_title = self.driver.find_element(*ActionsInCommonLocators.VIEW_TITLE)
            return view_title.text.lower() == sub_title
        except NoSuchElementException:
            self.logger.exception("Could not view the settings for {}".format(sub_title))

    def click_ok_button(self):
        return Click(ActionsInCommonLocators.SUBMIT_OK_BUTTON).submitting(self.driver)

    def click_cancel_button(self):
        return Click(ActionsInCommonLocators.SUBMIT_CANCEL_BUTTON).clicking(self.driver)

    def confirm_cancel(self):
        return Click(ActionsInCommonLocators.CONFIRM_CANCEL).clicking(self.driver)

    def wait_progress_bar(self):
        try:
            ui.WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(ActionsInCommonLocators.PROGRESS_BAR))
            self.logger.info("Waiting for the progress bar to disappear... ")
            ui.WebDriverWait(self.driver, 600).until(
                EC.invisibility_of_element_located(ActionsInCommonLocators.PROGRESS_BAR))
            self.logger.info("Progress bar is gone. Checking the result...")
        except TimeoutException:
            self.logger.exception("Progress bar is still present")

    def confirm_ok(self):
        return Click(ActionsInCommonLocators.CONFIRM_OK).clicking(self.driver)

    def cancel_edit(self):
        return Click(ActionsInCommonLocators.EDIT_CANCEL_BUTTON).clicking(self.driver)

    def get_message(self):
        try:
            ui.WebDriverWait(self.driver, 300).until(
                EC.visibility_of_element_located(ActionsInCommonLocators.TOASTER_MESSAGE))
            result_message = self.driver.find_element(*ActionsInCommonLocators.TOASTER_MESSAGE)
            return result_message.text
        except TimeoutException:
            self.logger.exception("Failed to get the resulting message of the action.")

    def close_message(self):
        return Click(ActionsInCommonLocators.CLOSE_MESSGAE).clicking(self.driver)

    def get_current_version(self):
        result = Click(ActionsInCommonLocators.HELP).clicking(self.driver)
        if result:
            try:
                cur_v = self.driver.find_element(*ActionsInCommonLocators.CURRENT_VERSION)
                if cur_v:
                    return cur_v.text
            except NoSuchElementException:
                self.logger.exception("Could not locate current version")
        else:
            return result



"""
==========================================================================================
For Login page
==========================================================================================
"""

class UCCLogin(BasePage):

    def match_page_tilte(self):
        try:
            return self.driver.title == "Aviatrix 2.0"
        except NoSuchElementException:
            self.logger.exception("Could not connect to UCC Web Console")

    def is_login_form_present(self):
        try:
            login_form = self.driver.find_element(*UCCSignInLocators.LOGIN_FORM)
            return 'password?' in login_form.text
        except NoSuchElementException:
            self.logger.exception("Could not find login form")

    def login(self,uemail,passwd):
        try:
            username = self.driver.find_element(*UCCSignInLocators.USERNAME)
            password = self.driver.find_element(*UCCSignInLocators.PASSWORD)
            sign_in_button = self.driver.find_element(*UCCSignInLocators.SIGN_IN_BUTTON)

            self.logger.debug("User name is %s",uemail)
            username.clear()
            username.send_keys(uemail)
            self.logger.debug("Password is %s",passwd)
            password.clear()
            password.send_keys(passwd)
            sign_in_button.submit()
        except (WebDriverException,NoSuchElementException):
            self.logger.exception("Could not sign in UCC successfully")

    def log_in_ok(self):
        return IsObjectPresent(Dashboardlocators.MAP).check_now(self.driver,"Login Form")

