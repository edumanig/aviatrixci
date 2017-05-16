import unittest, logging, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.lib.test_utils import get_test_data


class WebUITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.login_data = get_test_data("frontend.webuitest")
        cls.logger = logging.getLogger(__name__)
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.maximize_window()
        cls.logger.info('Enable ssh connection')
        _url = cls.login_data['base_url']
        ssh_url = _url + "/#/enable_ssh"
        cls.driver.get(ssh_url)
        time.sleep(5)
        actions_in_common = actions.ActionsInCommon(cls.driver)
        actions_in_common.enable_ssh(cls.login_data['passphrase'])
        actions_in_common.click_ok_button()
        time.sleep(3)
        cls.driver.get(_url)
        time.sleep(10)
        UCCLogin = actions.UCCLogin(cls.driver)
        cls.logger.info("Checking if UCC web UI is loaded")
        cls.assertTrue(UCCLogin.match_page_tilte(), "UCC web UI is not loaded successfully")

        cls.logger.info("Checking if login page is loaded")
        cls.assertTrue(UCCLogin.is_login_form_present(), "Login page is not loaded successfully")

        cls.logger.info("Logging in UCC...")
        UCCLogin.login(cls.login_data["username"], cls.login_data["password"])
        time.sleep(20)

        cls.logger.info("Checking if login is successful")
        cls.assertTrue(UCCLogin.log_in_ok(), "Could not log in UCC. Check the username and/or the password.")

    """
    @classmethod
    def tearDownClass(cls):
       cls.driver.close()
    """