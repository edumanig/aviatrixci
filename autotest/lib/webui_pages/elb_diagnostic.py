__author__ = 'Rong'
import logging
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from autotest.lib.common_elements import *
from autotest.lib.page_locators import *
import boto.ec2.elb
from boto.exception import NoAuthHandlerFound

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
            self.logger.exception("Could not connect to UCC Web Console")

    def is_login_form_present(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (UCCSignInLocators.LOGIN_FORM))
            )
            login_form = self.driver.find_element(*UCCSignInLocators.LOGIN_FORM)
            return 'password?' in login_form.text
        except NoSuchElementException:
            self.logger.exception("Could not find login form")

    def login(self,uemail,passwd):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (UCCSignInLocators.USERNAME))
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
            self.logger.exception("Could not sign in UCC successfully")

    def check_for_controller(self):
        try:
            page_url = self.driver.current_url
            if "/dashboard" not in page_url:
                return False
            return True
        except NoSuchElementException:
            self.logger.exception("Login failed")

#drop down,fill in  etc for ELB Status
class SelectVNetName(DropdownSelect):
    locator = TroubleshootingPageLocator.SELECT_VPC_ID
class ToasterMessage(Toaster):
    locator =  TroubleshootingPageLocator.SUCCESS_MESSAGE_TOASTER

class ELB_Diagnostic(BasePage):
    select_vnet_name = SelectVNetName()
    success_toaster = ToasterMessage()

    def click_toaster_close_button(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.CLOSE_SUCCESS_TOASTER))
            )
            close_toaster = self.driver.find_element(
                *TroubleshootingPageLocator.CLOSE_SUCCESS_TOASTER)
            close_toaster.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception("Toaster could not be close.")

    def check_toaster(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.SUCCESS_MESSAGE_TOASTER))
            )
            toaster = self.driver.find_element(
                *TroubleshootingPageLocator.SUCCESS_MESSAGE_TOASTER)
            return True
        except (WebDriverException, NoSuchElementException,TimeoutException):
            self.logger.exception("No toaster is found")

    def navigate_to_troubleshooting(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.NAVIGATING_TO_TROUBLESHOOTING))
            )
            troubleshooting_button = self.driver.find_element(
                *TroubleshootingPageLocator.NAVIGATING_TO_TROUBLESHOOTING)
            troubleshooting_button.click()
            return troubleshooting_button.text
        except NoSuchElementException:
            self.logger.exception("Could not navigate to Troubleshooting")
    def navigate_to_elb_status(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.NAVIGATING_TO_ELBDIAGNOSTIC))
            )
            elb_status_button = self.driver.find_element(
                *TroubleshootingPageLocator.NAVIGATING_TO_ELBDIAGNOSTIC)
            elb_status_button.click()
        except NoSuchElementException:
            self.logger.exception("Could not navigate to ELB Status")

    def current_url(self):
        try:
            page_url = self.driver.current_url
            if "/elbstatus" not in page_url:
                return False
            return True
        except NoSuchElementException:
            self.logger.exception("Login failed")

    def click_delete_button(self):
        try:
            delete_button = self.driver.find_element(
                *TroubleshootingPageLocator.DELETE_ELB_BUTTON)
            delete_button.click()
            return True
        except (WebDriverException,NoSuchElementException):
            self.logger.exception("Delete button could not pressed," +
                                  "ELB would not be deleted")

    def is_lb_present(self):
        try:
            lb_name = self.driver.find_element(*TroubleshootingPageLocator.LB_NAME)
            return True
        except NoSuchElementException:
            self.logger.exception("There is not ELB attached")

    def lb_name_information(self):
        try:
            lb_name = self.driver.find_element(*TroubleshootingPageLocator.LB_NAME)
            return lb_name.text
        except TimeoutException:
            self.logger.exception("Fail to get LB Name")

    def check_popup_exist(self):
        try:
            self.driver.find_element(
                *TroubleshootingPageLocator.DELETE_ELB_POP_UP_HEADING)
            return True
        except NoSuchElementException:
            self.logger.exception("No popup box is found")

    def click_pop_up_ok_button(self):
        try:
            ok_button = self.driver.find_element(
                *TroubleshootingPageLocator.POPUP_BOX_OK_BUTTON)
            ok_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "OK button not pressed,operation will not proceed")

    def click_pop_up_cancel_button(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.POPUP_BOX_CANCEL_BUTTON))
            )
            cancel_button = self.driver.find_element(
                *TroubleshootingPageLocator.POPUP_BOX_CANCEL_BUTTON)
            cancel_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Cancel button pressed, operation will not proceed")

    #check for the elb to confirm delete
    def connecting_to_aws(self):
        try:
            conn = boto.ec2.elb.connect_to_region('us-west-2')
            elb_list = conn.get_all_load_balancers()
            return len(elb_list)
        except NoAuthHandlerFound:
            self.logger.exception("The connection could not be made, check if you have the right config file")
            return -1