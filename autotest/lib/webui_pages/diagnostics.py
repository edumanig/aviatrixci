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
            WebDriverWait(self.driver, 10).until(
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

#drop down,fill in  etc for diagnostic section
class SelectGateway(DropdownSelect):
    locator = TroubleshootingPageLocator.SELECT_GATEWAY
class CheckController(Checkbox):
    selectedlocator = TroubleshootingPageLocator.CONTROLLER_CHECKBOX_IS_SELECTED
    clicklocator = TroubleshootingPageLocator.CONTROLLER_CHECKBOX_CLICK
class SubmitSuccessToaster(Toaster):
    locator = TroubleshootingPageLocator.IS_RESULT_SUBMIT
class OutputDiagnosticMessage(TextArea):
    locator = TroubleshootingPageLocator.SHOW_RESULT_TEXTAREA
#drop down,fill in  etc for VPN User Diagnostic
class InputVPNUserName(InputText):
    locator = TroubleshootingPageLocator.VPN_USERNAME
class OutputVPNDiagnosticMessage(TextArea):
    locator = TroubleshootingPageLocator.SHOW_VPN_DIAGNOSTIC_TEXTAREA
#drop down,fill in  etc for DB Diagnostics
class SelectDatabase(DropdownSelect):
    locator = TroubleshootingPageLocator.SELECT_DATABASE_NAME
class SelectCollectionName(DropdownSelect):
    locator = TroubleshootingPageLocator.SELECT_COLLECTION_NAME
class OutputDumpCollectionMessage(TextArea):
    locator = TroubleshootingPageLocator.DUMP_COLLECTION_RESULT_TEXTAREA
class InputDocument(InputText):
    locator = TroubleshootingPageLocator.DOCUMENT
class PopUpMessage(InputText):
    locator = TroubleshootingPageLocator.DOCUMENT

class Diagnostics(BasePage):

    select_gateway = SelectGateway()
    check_controller = CheckController()
    toaster_message = SubmitSuccessToaster()
    diagnostic_result = OutputDiagnosticMessage()
    vpn_user = InputVPNUserName()
    vpn_diagnostic_message = OutputVPNDiagnosticMessage()
    select_database = SelectDatabase()
    select_collection_name = SelectCollectionName()
    dump_collection_result = OutputDumpCollectionMessage()
    input_document = InputDocument()


    #move to troubleshooting section and then to diagnostic
    def navigate_to_troubleshooting(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.NAVIGATING_TO_TROUBLESHOOTING))
            )
            troubleshooting_button = self.driver.find_element(
                *TroubleshootingPageLocator.NAVIGATING_TO_TROUBLESHOOTING)
            troubleshooting_button.click()
            return troubleshooting_button.text
        except NoSuchElementException:
            self.logger.exception("Could not navigate to Troubleshooting")

    def navigate_to_diagnostics(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.NAVIGATING_TO_DIAGNOSTIC))
            )
            diagnostic_button = self.driver.find_element(
                *TroubleshootingPageLocator.NAVIGATING_TO_DIAGNOSTIC)
            diagnostic_button.click()
        except NoSuchElementException:
            self.logger.exception("Could not navigate to Diagnostics")

    def navigate_to_dbdiagnostics(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.NAVIGATE_TO_DBDIAGNOSTICS))
            )
            diagnostic_button = self.driver.find_element(
                *TroubleshootingPageLocator.NAVIGATE_TO_DBDIAGNOSTICS)
            diagnostic_button.click()
        except NoSuchElementException:
            self.logger.exception("Could not navigate to DB Diagnostics")

    def current_url(self):
        try:
            page_url = self.driver.current_url
            if "/diagnostics" not in page_url:
                return False
            return True
        except NoSuchElementException:
            self.logger.exception("Could not navigate to the Diagnostic page")

    def dbdiag_url(self):
        try:
            page_url = self.driver.current_url
            if "/dbdiagnostics" not in page_url:
                return False
            return True
        except NoSuchElementException:
            self.logger.exception("Could not navigate to DB Diagnostic page")

    #library for diagnostics panel
    def click_toaster_close_button(self):
        try:
            close_toaster = self.driver.find_element(
                *TroubleshootingPageLocator.CLOSE_TOASTER_BUTTON)
            close_toaster.click()
            return True
        except (WebDriverException,NoSuchElementException):
            self.logger.exception("Toaster could not be close.")

    def check_toaster(self):
        try:
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.IS_RESULT_SUBMIT))
            )
            toaster = self.driver.find_element(
                *TroubleshootingPageLocator.IS_RESULT_SUBMIT)
            return True
        except (WebDriverException,NoSuchElementException,TimeoutException):
            self.logger.exception("No toaster is found")

    def click_run_button(self):
        try:
            run_button = self.driver.find_element(
                *TroubleshootingPageLocator.RUN_BUTTON)
            run_button.click()
            return True
        except (WebDriverException,NoSuchElementException):
            self.logger.exception("Run button could not be pressed, " +
                                  "gateway diagnostic could not be run.")

    def click_show_button(self):
        try:
            show_button = self.driver.find_element(
                *TroubleshootingPageLocator.SHOW_BUTTON)
            show_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Show button could not be pressed," +
                "gateway diagnostic could not be shown")

    def click_close_button(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.CLOSE_RESULT_TEXTAREA_BUTTON))
            )
            close_button = self.driver.find_element(
                *TroubleshootingPageLocator.CLOSE_RESULT_TEXTAREA_BUTTON)
            close_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Gateway diagnostic result could not be closed " +
                "or the result is not present.")

    def click_submit_button(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.SUBMIT_BUTTON))
            )
            submit_button = self.driver.find_element(
                *TroubleshootingPageLocator.SUBMIT_BUTTON)
            submit_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Submit button could not be pressed," +
                "gateway diagnostic could not be submitted")

    # library for VPN user diagnostic panel
    def click_go_button(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.VPN_DIAGNOSTIC_GO_BUTTON))
            )
            go_button = self.driver.find_element(
                *TroubleshootingPageLocator.VPN_DIAGNOSTIC_GO_BUTTON)
            go_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Go button could not be pressed,VPN Diagnostic could not be run")

    def click_close_vpndiagnostic_button(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.CLOSE_VPN_DIAGNOSTIC_TEXTAREA_BUTTON))
            )
            close_button = self.driver.find_element(
                *TroubleshootingPageLocator.CLOSE_VPN_DIAGNOSTIC_TEXTAREA_BUTTON)
            close_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "VPN diagnostic result could not be closed " +
                "or the result does not exist.")

    # library for DB diagnostic panel NEED TO CHANGE
    def confirm_pop_up_exist(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (
                    TroubleshootingPageLocator.CLOSE_VPN_DIAGNOSTIC_TEXTAREA_BUTTON))
            )
            view_title = self.driver.find_element(
                *TroubleshootingPageLocator.POPUP_BOX_HEADER)
            return view_title.text.lower() == "confirm"
        except NoSuchElementException:
            self.logger.exception("No warning pop-up after button is pressed")

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
            cancel_button = self.driver.find_element(
                *TroubleshootingPageLocator.POPUP_BOX_CANCEL_BUTTON)
            cancel_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Cancel button pressed, operation will not proceed")

    def check_popup_exist(self):
        try:
            self.driver.find_element(
                *TroubleshootingPageLocator.POPUP_BOX_HEADER)
            return True
        except NoSuchElementException:
            self.logger.exception("No popup box is found")

    def click_restart_server_button(self):
        try:
            restart_server_button = self.driver.find_element(
                *TroubleshootingPageLocator.RESTART_SERVER_BUTTON)
            restart_server_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Restart Server button could not be pressed")

    def click_drop_database_button(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.DROP_DATABASE_BUTTON )))
            drop_database_button = self.driver.find_element(
                *TroubleshootingPageLocator.DROP_DATABASE_BUTTON )
            drop_database_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Drop Database button could not be pressed.")

    def click_dump_collection_button(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.DUMP_COLLECTION_BUTTON)))
            dump_collection_button = self.driver.find_element(
                *TroubleshootingPageLocator.DUMP_COLLECTION_BUTTON)
            dump_collection_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Dump Collection button could not be pressed ")

    def click_close_dump_collection_button(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.CLOSE_DUMP_COLLECTION_RESULT_TEXTAREA_BUTTON)))
            close_button = self.driver.find_element(
                *TroubleshootingPageLocator.CLOSE_DUMP_COLLECTION_RESULT_TEXTAREA_BUTTON)
            close_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Dump Collection result could not be closed " +
                "or the result does not exist")

    def click_delete_dump_collection_button(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.DELETE_COLLECTION_BUTTON)))
            delete_collection_button = self.driver.find_element(
                *TroubleshootingPageLocator.DELETE_COLLECTION_BUTTON)
            delete_collection_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Delete Collection button could not be pressed ")

    def click_dump_document_button(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.DUMP_DOCUMENT_BUTTON)))
            delete_document_button = self.driver.find_element(
                *TroubleshootingPageLocator.DUMP_DOCUMENT_BUTTON)
            delete_document_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Delete Document button could not be pressed.")

    def is_error_message_shown(self):
        try:
            ui.WebDriverWait(self.driver, 40).until(
                EC.visibility_of_element_located(
                    TroubleshootingPageLocator.ERROR_MESSAGE_TOASTER))
            result_message = self.driver.find_element(
                *TroubleshootingPageLocator.ERROR_MESSAGE_TOASTER)
            return result_message.text
        except TimeoutException:
            self.logger.exception("No error message is present")

    def click_delete_document_button(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (TroubleshootingPageLocator.DELETE_DOCUMENT_BUTTON)))
            delete_document_button = self.driver.find_element(
                *TroubleshootingPageLocator.DELETE_DOCUMENT_BUTTON)
            delete_document_button.click()
            return True
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Delete Document button could not be pressed")

    def wait_for_show_results_present(self):
        try:
            WebDriverWait(self.driver, 180).until(
                EC.presence_of_element_located(
                    (
                    TroubleshootingPageLocator.SHOW_RESULTS_PANEL))
            )
        except (TimeoutException,NoSuchElementException):
            self.logger.exception("Caould not find Show Results")

    def check_current_status(self, onlocator):
        try:
            on_Status = self.driver.find_element(*onlocator)
            if on_Status.is_displayed():
                return "on"
            else:
                return "off"
        except (WebDriverException, NoSuchElementException):
            self.logger.exception(
                "Could not find the status")

    def toggle_setting(self, onlocator, offlocator,status):
        try:
            if self.check_current_status(onlocator) == "on":
                if status.lower() == "on":
                    self.logger.info("The setting is on already")
                elif status.lower() == "off":
                    self.logger.info("Disable the setting")
                    on_status = self.driver.find_element(*onlocator)
                    if on_status:
                        on_status.click()
            elif  self.check_current_status(onlocator) == "off":
                if status.lower() == "off":
                    self.logger.info("The setting is off already")
                elif status.lower() == "on":
                    self.logger.info("Enable the setting")
                    off_status = self.driver.find_element(*offlocator)
                    if off_status:
                        off_status.click()

            else:
                self.logger.error('Cloud not find current status')

        except (WebDriverException, NoSuchElementException):
            self.logger.exception("Could not determine or set the status")

    def change_security_setting(self, status):
        self.toggle_setting(TroubleshootingPageLocator.ENABLE_SECURITY, TroubleshootingPageLocator.DISABLE_SECURITY, status)