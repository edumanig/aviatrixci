from autotest.lib.common_elements import *
from autotest.lib.page_locators import *
from selenium import webdriver
import logging, time
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from autotest.lib.webui_pages.basepage import BasePage

class InputCustomVersion(InputText):
    locator = SettingsLocators.CUSTOM_VERSION

class Upgrade(BasePage):
    custom_version = InputCustomVersion()

    def wait_page_load(self):
        try:
            loader = self.driver.find_element(*SettingsLocators.PAGE_SPINNER)
            self.logger.info("waiting for page to completely load")
            while loader.is_displayed() is True:
                time.sleep(1)
            return True
        except StaleElementReferenceException:
            pass
        except:
            self.logger.exception("error: cannot find spinner")

    def navigate_to_settings(self):
        return Click(SettingsLocators.NAVIGATE_TO_SETTINGS).clicking(self.driver)

    def navigate_to_upgrade(self):
        return Click(SettingsLocators.NAVIGATE_TO_UPGRADE).clicking(self.driver)

    def check_upgrade_page(self):
        try:
            ui.WebDriverWait(self.driver, 8).until(EC.visibility_of_element_located(SettingsLocators.CHECK_UPGRADE_PAGE))
            check_page = self.driver.find_elements(*SettingsLocators.CHECK_UPGRADE_PAGE)
            return check_page[0].text == 'upgrade to the latest'
        except NoSuchElementException:
            self.logger.exception("could not view upgrade")

    def get_current_version(self):
        return self.driver.find_element(*SettingsLocators.CURRENT_VERSION)

    def click_custom_version_upgrade(self):
        return Click(SettingsLocators.UPGRADE_RELEASE_VERSION).clicking(self.driver)

    def click_latest_version_upgrade(self):
        return Click(SettingsLocators.UPGRADE_LATEST).clicking(self.driver)

    def is_upgrade_complete(self):
        try:
            wait = WebDriverWait(self.driver, 360)
            wait.until(EC.presence_of_element_located(SettingsLocators.SERVICE_UNAVAILABLE))
            return True
        except TimeoutException:
            self.logger.exception("Error: too much time, cannot find service unavailable")

    def is_restart_complete(self):
        try:
            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.presence_of_element_located(UCCSignInLocators.LOGIN_FORM))
        except TimeoutException:
            self.logger.exception("Error: too much time")