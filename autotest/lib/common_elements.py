import logging,time
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from autotest.lib.page_locators import *
from autotest.lib.cloudn_utils import handle_alert
from autotest.lib.test_utils import get_test_data


class DropdownSelect(object):
    logger = logging.getLogger(__name__)

    def __set__(self, instance, value):
        driver = instance.driver

        try:
            ui.WebDriverWait(driver, 20).until(EC.visibility_of_element_located(self.locator))
            self.logger.debug("Selecting the specified %s",value)
            select = Select(driver.find_element(*self.locator))
            return select.select_by_visible_text(value)
        except TimeoutException:
            self.logger.exception("Dropdown menu is not present yet.")

    def __get__(self, instance, owner):
        driver = instance.driver
        try:
            ui.WebDriverWait(driver, 20).until(EC.visibility_of_element_located(self.locator))
            select = Select(driver.find_element(*self.locator))
            return select.first_selected_option.text
        except TimeoutException:
            self.logger.exception("Dropdown menu is not present yet.")


class InputText(object):
    logger = logging.getLogger(__name__)

    def __set__(self, instance, value):
        driver = instance.driver

        try:
            ui.WebDriverWait(driver, 20).until(EC.visibility_of_element_located(self.locator))
            textbox = driver.find_element(*self.locator)
            #textbox.click()
            textbox.clear()
            return textbox.send_keys(value)
        except TimeoutException:
            self.logger.exception("Textbox is not present yet.")

    def __get__(self, instance, owner):
        driver = instance.driver

        try:
            ui.WebDriverWait(driver, 20).until(EC.visibility_of_element_located(self.locator))
            textbox = driver.find_element(*self.locator)
            return textbox.get_attribute("value")
        except TimeoutException:
            self.logger.exception ("Textbox field is not found.")


class Checkbox(object):
    logger = logging.getLogger(__name__)

    def __set__(self, instance, value):
        driver = instance.driver
        try:
            ui.WebDriverWait(driver, 20).until(EC.visibility_of_element_located(self.clicklocator))

            chbox = driver.find_element(*self.clicklocator)
            chbox_is_selected = driver.find_element(*self.selectedlocator)

            if value.lower() == "select" and chbox_is_selected.is_selected():
                self.logger.info("Checkbox is already selected")
            elif value.lower() == "deselect" and not chbox_is_selected.is_selected():
                self.logger.info("Checkbox is not selected")
            else:
                chbox.click()

        except TimeoutException:
            self.logger.exception("Checkbox is not present yet.")

    def __get__(self, instance, owner):
        driver = instance.driver
        try:
            ui.WebDriverWait(driver, 20).until(EC.visibility_of_element_located(self.clicklocator))

            chbox = driver.find_element(*self.selectedlocator)
            return chbox.is_selected()

        except TimeoutException:
            self.logger.exception("Checkbox is not present yet.")


class RadioButton(object):
    logger = logging.getLogger(__name__)

    def __set__(self, instance, value):
        driver = instance.driver
        try:
            ui.WebDriverWait(driver, 20).until(EC.visibility_of_element_located(self.yesclicklocator))

            yesclick = driver.find_element(*self.yesclicklocator)
            yesisselected = driver.find_element(*self.yesselectedlocator)
            noclick = driver.find_element(*self.noclicklocator)
            noisselected = driver.find_element(*self.noselectedlocator)

            if value.lower() == "yes":
                if yesisselected.is_selected():
                    self.logger.info("Yes is already selected")
                else:
                    yesclick.click()

            if value.lower() == "no":
                if noisselected.is_selected():
                    self.logger.info("No is already selected")
                else:
                    noclick.click()

        except TimeoutException:
            self.logger.exception("Radio button is not present yet.")

    def __get__(self, instance, owner):
        driver = instance.driver
        try:
            ui.WebDriverWait(driver, 20).until(EC.visibility_of_element_located(self.yesclicklocator))

            yesselected = driver.find_element(*self.yesselectedlocator)

            if yesselected.is_selected():
                return "Yes"
            return "No"

        except TimeoutException:
            self.logger.exception("Radio button is not present yet.")


class Click(object):

    def __init__(self,locator):
        self.locator = locator
        self.logger = logging.getLogger(__name__)

    def clicking(self,driver):
        try:
            ui.WebDriverWait(driver, 20).until(EC.visibility_of_element_located(self.locator))
            clickable = driver.find_element(*self.locator)
            if clickable:
                clickable.click()
                return True
        except (TimeoutException,NoSuchElementException):
            self.logger.exception("Could not find something clickable to click")

    def submitting(self,driver):
        try:
            ui.WebDriverWait(driver, 20).until(EC.visibility_of_element_located(self.locator))
            submittable = driver.find_element(*self.locator)
            if submittable:
                submittable.submit()
                return True
        except (TimeoutException,NoSuchElementException):
            self.logger.exception("Could not find something submittable to submit")


class IsObjectPresent:
    def __init__(self,locator):
        self.locator = locator
        self.logger = logging.getLogger(__name__)

    def check_now(self,driver,obj_name):
        try:
            ui.WebDriverWait(driver, 30).until(EC.visibility_of_element_located(self.locator))
            obj = driver.find_element(*self.locator)
            if obj:
                return True
            return False
        except (TimeoutException,NoSuchElementException):
            self.logger.exception("Could not find {}".format(obj_name))


class TableData(object):
    
    def __init__(self,locator):
        self.locator = locator
        self.logger = logging.getLogger(__name__)

    def get_row_data(self,driver):
        self.driver = driver
        row_data = []
        try:
            ui.WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.locator)))

            table_rows = driver.find_elements(By.CSS_SELECTOR, self.locator + " tbody tr")
            for rowlement in table_rows:
                row_data.append(rowlement.text)

            return row_data
        except TimeoutException:
            self.logger.exception("Could not findthe table.")

    def get_table_data(self, driver):
        self.driver = driver
        row_data = []
        i = 1
        j = 0
        try:
            ui.WebDriverWait(driver, 20).until(EC.visibility_of_element_located(self.locator))
            temp_locator = self.locator
            table_id = self.driver.find_elements(temp_locator[0], temp_locator[1] + " tbody tr")

            for x in table_id:
                ap_tag = " tbody tr:nth-child("+str(i)+")"
                table_rows = self.driver.find_element(temp_locator[0], temp_locator[1] + ap_tag)
                tds = table_rows.find_elements_by_tag_name('td')
                row_data.append([])

                for td in tds:
                    row_data[j].append(td.text)

                j += 1
                i += 1
            return row_data

        except TimeoutException:
            self.logger.exception("Could not find the table.")

    def get_column_data(self,driver,column):
        self.driver = driver

        try:
            ui.WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.locator)))

            table_column = driver.find_element(By.CSS_SELECTOR, self.locator + " thead")

            if column > 0 and column <= len(table_column.text) + 1:
                datalocator = self.locator + " tbody tr td:nth-of-type({})".format(column)
                tr = self.driver.find_elements(By.CSS_SELECTOR, datalocator)
                return [x.text for x in tr]
            else:
                self.logger.error("No such column")
                return None
        except TimeoutException:
            self.logger.exception("Panel with table is not present yet.")

    def check_specific_row_data(self,driver,rowvalue,columnnum,sp_column=None):

        data = self.get_row_data(driver)
        if data:
            for row in data:
                if sp_column is None:
                    if rowvalue in row:
                        return row.split()[columnnum]
                else:
                    if rowvalue == row.split()[sp_column]:
                        return row.split()[columnnum]
        return None

    def is_data_present(self,driver,column,value):
        self.driver = driver

        data = self.get_column_data(driver,column)
        if value in data:
            return True
        self.logger.error("No such value in the specified row")
        return False

    def click_row_to_edit(self,driver,value):
        self.driver = driver
        if self.locator == GatewayViewLocators.GATEWAY_TABLE_FOR_TABLE:
            col = 2
        else:
            col = 1
        try:
            data = self.get_column_data(driver, col)
            selected = -1
            for i, x in enumerate(data):
                if x == value:
                    selected = i
            if self.locator == Dashboardlocators.VPN_USER_TABLE_FOR_TABLE:
                datalocator = self.locator + " tbody tr td:nth-of-type({}) .fake-link".format(col)
            else:
                datalocator = self.locator + " tbody tr td:nth-of-type({})".format(col)
            tr = self.driver.find_elements(By.CSS_SELECTOR, datalocator)
            tr[selected].click()

        except:
            self.logger.exception("Could not click the selected value.")

    def click_button_in_the_row(self, driver, column1,column2, value, sublocator = None):
        self.driver = driver
        try:
            data = self.get_column_data(driver, column1)
            if data is None:
                self.logger.error('Get column data returns None')
                return False

            row_num = -1
            for i,x in enumerate(data):
                if x == value:
                    row_num = i

            if self.locator == GatewayViewLocators.GATEWAY_TABLE_FOR_TABLE:
                if row_num != 0 : row_num = int(row_num/2)

            if sublocator is not None:
                buttonlocator = self.locator + " tbody tr td:nth-of-type({}) {}".format(column2, sublocator)
            else:
                buttonlocator = self.locator + " tbody tr td:nth-of-type({})".format(column2)

            button_column = self.driver.find_elements(By.CSS_SELECTOR, buttonlocator)
            button_column[row_num].click()
            return True

        except:
            self.logger.exception("Could not click the specified button.")


"""
    Classes created by Rong Huang
"""
class TextArea(object):
    logger = logging.getLogger(__name__)

    def __get__(self, instance, owner):
        driver = instance.driver

        try:
            ui.WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located(self.locator))
            textarea = driver.find_element(*self.locator)
            return textarea.get_attribute("value")
        except TimeoutException:
            self.logger.exception ("Textarea is not present yet.")

class Toaster(object):
    logger = logging.getLogger(__name__)

    def __get__(self, instance, owner):
        driver = instance.driver

        try:
            ui.WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(self.locator))
            toaster = driver.find_element(*self.locator)
            return toaster.text
        except TimeoutException:
            self.logger.exception ("Toaster is not present yet.")

"""
    Classes created by Liming
"""

#copy out the message from a toaster message
class ToasterLM(object):
    logger = logging.getLogger()

    def __get__(self, instance, owner):
        driver = instance.driver
        try:
            ui.WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located(self.toaster))
            toaster = driver.find_element(*self.toaster)
            toaster_result = toaster.text
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.exception ("Toaster exception: %s", str(e))
            return ""

        try:
            ui.WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located(self.toaster_closer))
            close_btn = driver.find_element(*self.toaster_closer)
            close_btn.click()
            time.sleep(10)
        except NoSuchElementException:
            self.logger.exception("Toaster can not be closed.")
            return ""

        return toaster_result


class BasePage(object):
    def __init__(self, driver, login_required=False):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.login_required = login_required
        self.login_data = get_test_data("frontend.webuitest")

    def match_page_title(self):
        try:
            return self.driver.title == "Aviatrix Cloud Controller"
        except NoSuchElementException:
            self.logger.exception("Could not connect to UCC Web Console")

    def is_login_form_present(self):
        try:
            login_form = self.driver.find_element(*UCCSignInLocators.LOGIN_FORM)
            return 'password?' in login_form.text
        except NoSuchElementException:
            self.logger.exception("Could not find login form")

    def login(self, uemail, passwd):
        try:
            username = self.driver.find_element(*UCCSignInLocators.USERNAME)
            password = self.driver.find_element(*UCCSignInLocators.PASSWORD)
            sign_in_button = self.driver.find_element(*UCCSignInLocators.SIGN_IN_BUTTON)

            self.logger.debug("User name is %s", uemail)
            username.send_keys(uemail)
            self.logger.debug("Password is %s", passwd)
            password.send_keys(passwd)
            sign_in_button.submit()
        except (WebDriverException, NoSuchElementException):
            self.logger.exception("Could not sign in UCC successfully")

    def log_in_ok(self):
        try:
            self.driver.find_element(*UCCSignInLocators.IS_SIGN_IN_OK)
            return True
        except NoSuchElementException:
            self.logger.exception("Login failed")

    def process_login(self):
        self.logger.debug("The login required is: " + str(self.login_required) )
        if self.login_required:

            self.logger.debug("Login required")
            base_url = self.login_data['base_url']
            self.driver.get(base_url)
            time.sleep(10)

            self.logger.info("Checking if UCC web UI is loaded")
            if not self.match_page_title():
                self.logger.error("UCC web UI can not be loaded successfully")
                return False
            time.sleep(10)
            self.logger.info("Checking if login page is loaded")
            if not self.is_login_form_present():
                self.logger.error("Login page can not be loaded successfully")
                return False
            time.sleep(2)
            self.logger.info("Logging in UCC...")
            self.login(self.login_data["username"],self.login_data["password"])
            time.sleep(15)

            self.logger.info("Checking if login is successful")
            if not self.log_in_ok():
                self.logger.error("Could not log in UCC. Check the username and/or the password.")
                return False
        return True

#Switch between enabled and disabled such as 'Enable HA' for Site2Cloud
class SwitchButton(object):
    logger = logging.getLogger()

    def __set__(self, instance, value):
        driver = instance.driver
        if value.lower() == "enable":
            try:
                driver.find_element(*self.status)
                self.logger.debug("Switch already in Enabled mode. Skip.")
                return True
            except NoSuchElementException:
                self.logger.debug("Switch in Disabled mode. Try to enable it.")
                driver.find_element(*self.enable).click()
                time.sleep(5)
        elif value.lower() == "disable":
            try:
                driver.find_element(*self.status)
                self.logger.debug("Switch in Enabled mode. Try to disable it.")
                driver.find_element(*self.disable).click()
                handle_alert(instance)
            except NoSuchElementException:
                self.logger.debug("Switch already in Disabled mode. Skip.")
                return True
        else:
            self.logger.error("Has to be either 'enable' or 'disable'. Abort...")
            return False
        return True

    def __get__(self, instance, owner):
        driver = instance.driver
        try:
            driver.find_element(*self.status)
            self.logger.debug("Switch in Enabled mode.")
            return "Enabled"
        except NoSuchElementException:
            self.logger.debug("Switch in Disabled mode.")
            return "Disabled"

class ActionButton(object):
    logger = logging.getLogger()

    def __set__(self, instance, value):
        driver = instance.driver
        try:
            ui.WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(self.locator))
            button = driver.find_element(*self.locator)
            self.logger.debug("Find %s button. Click it...", value)
            button.click()
            return True
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.debug("Can not find %s button with exception %s", (value, str(e)))

    def __get__(self, instance, owner):
        driver = instance.driver
        try:
            ui.WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(self.locator))
            driver.find_element(*self.locator)
            self.logger.debug("Find the button.")
            return True
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.debug("Can not find the button with exception %s.", str(e))

class OutputPanel(object):
    logger = logging.getLogger()

    def __get__(self, instance, owner):
        driver = instance.driver
        try:
            output = driver.find_element(*self.locator)
            self.logger.debug("Find the output panel.")
            wait = 10
            while not output.text and wait:
                time.sleep(1)
                wait = wait -1
            return output.text
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.debug("Can not find the output panel with exception %s", str(e))
            return None

class Table(object):
    logger = logging.getLogger()

    def __get__(self, instance, owner):
        driver = instance.driver
        thlist = []
        tblist = []
        try:
            table = driver.find_element(*self.locator)
            for tr in table.find_elements_by_tag_name('tr'):
                tdlist = []
                if tr.find_elements_by_tag_name('th'):
                    ths = tr.find_elements_by_tag_name('th')
                    for th in ths:
                        if not th.text:
                            thtext = "Button"
                            thlist.append(thtext)
                        else:
                            thlist.append(th.text)
                if tr.find_elements_by_tag_name('td'):
                    tds = tr.find_elements_by_tag_name('td')
                    for td in tds:
                        tdlist.append(td.text)
                    dictionary = dict(zip(thlist, tdlist))
                    tblist.append(dictionary)
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.debug("Can not find the table with exception %s", str(e))
        return tblist


