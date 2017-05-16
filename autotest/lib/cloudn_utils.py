__author__ = 'lmxiang'

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException


def login(driver, baseURL):
    driver.maximize_window()
    #driver.get(baseURL + "/login.php")
    driver.get(baseURL)
    my_username = driver.find_element_by_id("username")
    my_password = driver.find_element_by_id("password")
    my_username.send_keys("admin")
    my_password.send_keys("password")
    driver.find_element_by_id("save").click()
    wait = WebDriverWait(driver, 5)
    try:
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))
        return True
    except(NoSuchElementException, TimeoutException):
        return False


def wait_expectation_id(driver, timeout, logger, id_value, exception_msg):
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(EC.presence_of_element_located((By.ID, id_value)))
        return 0
    except(NoSuchElementException, TimeoutException) as e:
        logger.error(exception_msg + str(e))
        return 1


def wait_expectation_class(driver, timeout, logger, class_name, exception_msg):
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        return 0
    except(NoSuchElementException, TimeoutException) as e:
        logger.error(exception_msg + str(e))
        return 1


def wait_expectation_xpath_text(driver, timeout, logger, xpath_value, expected_msg, exception_msg):
    wait = WebDriverWait(driver, timeout)
    try:
        _body = wait.until(EC.presence_of_element_located((By.XPATH, xpath_value)))
        if expected_msg in _body.text:
            logger.debug("Expected message shows up: " + expected_msg)
            return 0
        else:
            logger.error("Expected message doesn't show up: " + expected_msg)
            logger.error("Error message shows up: " + _body.text)
            return 1
    except(NoSuchElementException, TimeoutException) as e:
        logger.error(exception_msg + str(e))
        return 1


def wait_expectation_text_id(driver, timeout, logger, id_value, expected_msg, exception_msg):
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(EC.text_to_be_present_in_element((By.ID, id_value), expected_msg))
        _body = driver.find_element_by_id(id_value)
        if expected_msg in _body.text:
            logger.debug("Expected message shows up: " + expected_msg)
            return 0
        else:
            logger.error("Expected message doesn't show up: " + expected_msg)
            logger.error("Error message shows up: " + _body.text)
            return 1
    except(NoSuchElementException, TimeoutException) as e:
        _body = driver.find_element_by_id(id_value)
        logger.exception(exception_msg + str(e))
        logger.exception("Error message shows up: %s" % _body.text)
        return 1


def wait_expectation_xpath_id(driver, timeout, logger, xpath_value, id_value, expected_msg, exception_msg):
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_value)))
        _body = driver.find_element_by_id(id_value)
        if expected_msg in _body.text:
            logger.debug("Expected message shows up: " + expected_msg)
            return 0
        else:
            logger.error("Expected message doesn't show up: " + expected_msg)
            logger.error("Error message shows up: " + _body.text)
            return 1
    except(NoSuchElementException, TimeoutException) as e:
        logger.error(exception_msg + str(e))
        return 1


def wait_expectation_xpath_class(driver, timeout, logger, xpath_value, class_value, expected_msg, exception_msg):
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath_value)))
        _body = driver.find_element_by_class_name(class_value)
        if expected_msg in _body.text:
            logger.debug("Expected message shows up: " + expected_msg)
            return True
        else:
            logger.error("Expected message doesn't show up: " + expected_msg)
            logger.error("Error message shows up: " + _body.text)
            return False
    except(NoSuchElementException, TimeoutException) as e:
        logger.error(exception_msg + str(e))
        return False


def close_alert_and_get_its_text(self):
    try:
        alert = self.driver.switch_to_alert()
    except NoAlertPresentException as e:
        return None

    try:
        if self.accept_next_alert:
            alert.accept()
        else:
            alert.dismiss()
        return alert.text
    except:
        return None
    finally:
        self.accept_next_alert = True


def handle_alert(self, action="confirm"):
    try:
        self.driver.switch_to_alert()
    except NoAlertPresentException as e:
        return None

    try:
        if action.lower()=="confirm":
            self.driver.find_element_by_css_selector("button[ng-click='ok()']").click()
            return True
        elif action.lower()=="cancel":
            self.driver.find_element_by_css_selector("button[ng-click='cancel()']").click()
            return True
        else:
            return False
    except:
        return False
