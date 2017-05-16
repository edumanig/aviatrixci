import unittest, logging, time
from selenium import webdriver
import tests.UCC.UCCWebUI.lib.webui_pages.gateway as pages


class InputLicense(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from tests.main import variables as _variables

        cls.logger = logging.getLogger(__name__)
        cls.driver = webdriver.Chrome()
        #cls.driver.maximize_window()
        gw_url = _variables["uccURL"] + '/preview/'
        cls.driver.get(gw_url)
        time.sleep(10)
        UCCLogin = pages.UCCLogin(cls.driver)
        cls.logger.info("Checking if UCC web UI is loaded")
        cls.assertTrue(UCCLogin.match_page_tilte(),"UCC web UI is not loaded successfully")

        cls.logger.info("Checking if login page is loaded")
        cls.assertTrue(UCCLogin.is_login_form_present(),"Login page is not loaded successfully")

        cls.logger.info("Logging in UCC...")
        UCCLogin.login(_variables["login_username"],_variables["login_password"])
        time.sleep(20)

        cls.logger.info("Checking if login is successful")
        cls.assertTrue(UCCLogin.log_in_ok(),"Could not log in UCC. Check the username and/or the password.")

    def test_input_license(self):
        license_view = pages.License(self.driver)

        license_view.expand_settings()
        time.sleep(3)
        license_view.license_view()

        time.sleep(5)
        #license_view.customer_id = '@3d4%bfd'
