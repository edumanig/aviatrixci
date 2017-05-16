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
            return self.driver.title == "Aviatrix Cloud Controller"
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


#drop down,fill in  etc for VNET diagnostic
class SelectCloudType(DropdownSelect):
    locator = TroubleshootingPageLocator.SELECT_CLOUD_TYPE
class SelectAccountName(DropdownSelect):
    locator = TroubleshootingPageLocator.SELECT_ACCOUNT_NAME
class SelectTestType(DropdownSelect):
    locator = TroubleshootingPageLocator.SELECT_TOOL
class OutputTextareaMessage(TextArea):
    locator = TroubleshootingPageLocator.VNET_RESULT_TEXTAREA
class InputRouteTableName(InputText):
        locator = TroubleshootingPageLocator.ROUTE_TABLE_NAME
class SelectLocation(DropdownSelect):
    locator = TroubleshootingPageLocator.SELECT_ROUTE_TABLE_LOCATION
class ToasterMessage(Toaster):
    locator = TroubleshootingPageLocator.VNET_TOASTER
class InputVNetName(InputText):
    locator = TroubleshootingPageLocator.VNET_NAME
class InputInstanceID(InputText):
    locator = TroubleshootingPageLocator.INSTANCE_ID
class InputRouteName(InputText):
    locator = TroubleshootingPageLocator.ROUTE_NAME
class InputCIDR(InputText):
    locator = TroubleshootingPageLocator.CIDR
class InputNextHopIP(InputText):
    locator = TroubleshootingPageLocator.NEXT_HOP_IP
class InputSubnet(InputText):
    locator = TroubleshootingPageLocator.SUBNET

class VNetDiagnostic(BasePage):

    select_cloud_type = SelectCloudType()
    select_account_name = SelectAccountName()
    select_test_type = SelectTestType()
    output_textarea = OutputTextareaMessage()
    route_table_name = InputRouteTableName()
    select_location = SelectLocation()
    output_toaster = ToasterMessage()
    vnet_name = InputVNetName()
    instance_id = InputInstanceID()
    route_name = InputRouteName()
    cidr = InputCIDR()
    next_hop_ip = InputNextHopIP()
    subnet = InputSubnet()
    #move to troubleshooting section and then to diagnostic
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

    def navigate_to_vnetdiagnostics(self):
        try:
            WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (TroubleshootingPageLocator.NAVIGATING_TO_VNETDIAGNOSTIC)))
            vnetdiagnostic_button = self.driver.find_element(
                *TroubleshootingPageLocator.NAVIGATING_TO_VNETDIAGNOSTIC)
            vnetdiagnostic_button.click()
        except NoSuchElementException:
            self.logger.exception("Could not navigate to  VNet Diagnostics")

    def current_url(self):
        try:
            page_url = self.driver.current_url
            if "/vnetdiagnostics" not in page_url:
                return False
            return True
        except NoSuchElementException:
            self.logger.exception("Login failed")

    def click_go_button(self):
        try:
            go_button = self.driver.find_element(
                *TroubleshootingPageLocator.VNET_DIAGNOSTIC_GO_BUTTON)
            go_button.click()
            return True
        except (WebDriverException,NoSuchElementException):
            self.logger.exception("Go button could not be pressed, " +
                                  "VNet Diagnostics could not be run.")

    def click_close_button(self):
        try:
            close_button = self.driver.find_element(
                *TroubleshootingPageLocator.VNET_RESULT_TEXTAREA_CLOSE_BUTTON)
            close_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "VNet Diagnostic could not closed" +
                "or the result is not present.")

    def check_toaster ( self ):
        try:
            WebDriverWait ( self.driver , 20 ).until (
                EC.presence_of_element_located (
                    (TroubleshootingPageLocator.VNET_TOASTER) )
            )
            toaster = self.driver.find_element (
                *TroubleshootingPageLocator.VNET_TOASTER )
            return True
        except (WebDriverException , NoSuchElementException,TimeoutException):
            self.logger.exception ( "Successfully closed toaster" )

    def click_toaster_close_button(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.VNET_TOASTER_CLOSE))
            )
            close_toaster = self.driver.find_element(
                *TroubleshootingPageLocator.VNET_TOASTER_CLOSE)
            close_toaster.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception("Toaster could not be close.")

