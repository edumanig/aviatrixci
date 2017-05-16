__author__ = 'Rong'
import logging
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from autotest.lib.common_elements import *
from autotest.lib.page_locators import *

class BasePage(object):
    """
        Class method provided by Sam
    """
    def __init__(self,driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

class UCCLogin(BasePage):
    """
        Class method provided by Sam
    """
    def match_page_tilte(self):
        try:
            return self.driver.title == "Aviatrix 2.0"
        except NoSuchElementException:
            self.logger.exception("Page title could not be found.Could not connect to UCC Web Console")

    def is_login_form_present(self):
        try:
            WebDriverWait( self.driver, 10).until(
                EC.presence_of_element_located((UCCSignInLocators.LOGIN_FORM))
            )
            login_form = self.driver.find_element(*UCCSignInLocators.LOGIN_FORM)
            return 'password?' in login_form.text
        except NoSuchElementException:
            self.logger.exception("Could not find login form")

    def login(self,uemail,passwd):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((UCCSignInLocators.USERNAME))
            )
            username = self.driver.find_element(*UCCSignInLocators.USERNAME)
            password = self.driver.find_element(*UCCSignInLocators.PASSWORD)
            sign_in_button = self.driver.find_element(*UCCSignInLocators.SIGN_IN_BUTTON)
            self.logger.debug("User name is %s",uemail)
            username.send_keys(uemail)
            self.logger.debug("Password is %s",passwd)
            password.send_keys(passwd)
            sign_in_button.submit()
        except (WebDriverException,NoSuchElementException):
            self.logger.exception("Username and Password fill in does not exist.Could not sign in UCC successfully")

    def check_for_controller(self):
        try:
            page_url = self.driver.current_url
            if "/dashboard" not in page_url:
                return False
            return True
        except NoSuchElementException:
            self.logger.exception("Login failed,Dashboard page not shown.")

#drop down,fill in  etc for upload tracelog section
class SelectGateway(DropdownSelect):
    locator = TroubleshootingPageLocator.GATEWAY_SELECT
class SubmitSuccessToaster(Toaster):
    locator = TroubleshootingPageLocator.IS_TRACELOG_SENT
# drop down,fill in  etc for ping utility section
class InputPingUtitlity(InputText):
    locator = TroubleshootingPageLocator.HOST_NAME
class OutputPingMessage(TextArea):
    locator = TroubleshootingPageLocator.PING_RESULT_TEXTAREA
# drop down,fill in  etc for command log section
class OutputCommandLog(TextArea):
    locator = TroubleshootingPageLocator.COMMAND_LOG_RESULT_TEXTAREA

class Logs(BasePage):
    select_gateway = SelectGateway()
    host_name = InputPingUtitlity()
    ping_result = OutputPingMessage()
    command_log_result = OutputCommandLog()
    tracelog_sent = SubmitSuccessToaster()

    def navigate_to_troubleshooting(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((TroubleshootingPageLocator.NAVIGATING_TO_TROUBLESHOOTING))
            )
            troubleshooting_button = self.driver.find_element(*TroubleshootingPageLocator.NAVIGATING_TO_TROUBLESHOOTING)
            troubleshooting_button.click()
            return troubleshooting_button.text
        except NoSuchElementException:
            self.logger.exception("Troubleshooting link not available.Could not navigate to Troubleshooting")

    def navigate_to_log(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.NAVIGATING_TO_TROUBLESHOOTING))
            )
            logs_button = self.driver.find_element(
                *TroubleshootingPageLocator.NAVIGATING_TO_LOGS)
            logs_button.click()
            return True
        except NoSuchElementException:
            self.logger.exception("Logs link not available.Could not navigate to Logs")

    def check_for_log_page(self):
        try:
            page_url = self.driver.current_url
            if "/tracelog" not in page_url:
                return False
            return True
        except NoSuchElementException:
            self.logger.exception("Not on the Tracelog page")

    # begin method for uploading tracelog
    def click_ok_button(self):
        try:
            ok_button = self.driver.find_element(*TroubleshootingPageLocator.OK_BUTTON)
            ok_button.click()
            return True
        except (WebDriverException,NoSuchElementException):
            self.logger.exception("OK button not avaliable.Tracelog could not be uploaded")

    def click_toaster_close_button(self):
        try:
            close_toaster = self.driver.find_element(
                *TroubleshootingPageLocator.CLOSE_TRACELOG_TOASTER)
            close_toaster.click()
            return True
        except (WebDriverException,NoSuchElementException):
            self.logger.exception("Toaster could not be close.")

    def check_toaster(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.IS_TRACELOG_SENT))
                )
            toaster = self.driver.find_element(
                    *TroubleshootingPageLocator.IS_TRACELOG_SENT)
            return True
        except (WebDriverException, NoSuchElementException,TimeoutException):
            self.logger.exception("No toaster is found")

    #begin method for ping utility
    def click_ping_button(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.PING_BUTTON))
            )
            ping_button = self.driver.find_element(
                *TroubleshootingPageLocator.PING_BUTTON)
            ping_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Ping button does not exist. Ping button could not be pressed.")

    #begin method for print command log
    def click_display_button(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.DISPLAY_BUTTON))
            )
            display_button = self.driver.find_element(
                *TroubleshootingPageLocator.DISPLAY_BUTTON)
            display_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Display button does not exit. Command log could not be shown.")

