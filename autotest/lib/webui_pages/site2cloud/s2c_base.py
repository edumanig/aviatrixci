import logging
from autotest.lib.common_elements import *
from autotest.lib.page_locators import *

class S2C_Base(BasePage):
    """
    Parent class of 'S2C_New', 'S2C_View' in s2c_conn.py
    Parent class of 'S2c_Diag' in s2c_diag.py
    """

    def __init__(self, driver, login_required=False):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        BasePage.__init__(self, self.driver, login_required=login_required)
        if login_required:
            BasePage.process_login(self)

    def navigate_to_s2c(self):
        """
        Navigate to site2cloud page
        :return: True or False
        """
        try:
            s2c_button = self.driver.find_element(*S2CViewLocators.NAVIGATE_TO_S2C)
            s2c_button.click()
            time.sleep(15)
            return True
        except NoSuchElementException:
            self.logger.exception("Could not navigate to Site2Cloud")
            return False

    def match_view_title(self):
        """
        Verify if site2cloud page is loaded correctly
        :return: True or False
        """
        try:
            view_title = self.driver.find_element(*S2CViewLocators.VIEW_TITLE).text
            if view_title.lower() in ["diagnostics", "site2cloud"]:
                return True
            else:
                self.logger.error("Should be 'Diagnostics' or 'Site2Cloud'")
                self.logger.error("%s found instead", view_title.lower())
                return False
        except NoSuchElementException:
            self.logger.exception("Could not view site2cloud settings")
            return False

    def select_tab(self):
        """
        Select 'Diagnostics' tab at site2cloud page
        :return: True or False
        """
        try:
            diag_tab = self.driver.find_element(*S2CViewLocators.DIAG_TAB)
            self.logger.debug("Click Site2Cloud diagnostics tab")
            diag_tab.click()
            return True
        except NoSuchElementException:
            self.logger.exception("Could not click Site2Cloud diagnostics tab")
            return False