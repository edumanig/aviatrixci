__author__ = 'lmxiang'

"""
Prerequisites:
- Create two VPCs called VPC1 and VPC2. VPC1 is the cloud side and VPC2 simulates on-prem
- Launch two gateways in VPC1. GW1_PRI is the primary gateway for HA and GW1_BKP is the backup gateway for HA
- Launch one gateway in VPC2.
- Launch one ubuntu instance in VPC1 as the source of ping traffic
- Launch one ubuntu instance in VPC2 as the destination of ping traffic
- Specify a folder at test machine for site2cloud configuration template download

Test Procedures:
- Create one site2cloud connection at GW1
- Download the configuration template with 'Aviatrix' as vendor from GW1
- Create one site2cloud connection at GW2 by importing the configuration template downloaded from GW1
- Send pings from ubuntu VM in VPC1 to ubuntu VM in VPC2 and check the ping success rate
- Check tunnel status at both GW1 and GW2
- Delete the site2cloud connections at both GW1 and GW2

Site2cloud Connection Types:
- unmapped, without HA
- mapped, without HA
- ummapped with HA
- mapped with HA
- unmapped and null encryption
"""

import unittest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from autotest.lib.common_elements import *
from autotest.lib.test_utils import find_files_in_directory, delete_files_in_directory
from autotest.lib.vpc_utils import ssh_from_instance, ping_from_instance
import autotest.lib.webui_pages.site2cloud.s2c_conn as s2cc
from autotest.run_autotest import config
from autotest.lib.test_utils import testcases

class S2C_Tests(unittest.TestCase):
    """
    Site2Cloud end-to-end solution tests
    """
    cases = testcases(__name__)
    case_list = cases.data

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(s2cc.__name__)
        chrome_options = Options()
        # folder used for Chrome to download files
        cls.dir_path = os.path.abspath(config['download']['autotest_download'])
        prefs = {"download.default_directory": cls.dir_path}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-extensions")
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.maximize_window()

    def test_s2c(self):
        s2c_new = s2cc.S2C_New(self.driver, login_required=True)
        s2c_view = s2cc.S2C_View(self.driver, login_required=False)
        self.logger.info("Navigating to Site2Cloud")
        s2c_new.navigate_to_s2c()
        time.sleep(5)

        self.logger.info("Get the data for the following tests")
        self.cases.start_test("dummy")
        cloud_region = self.cases.case_data['cloud_region']
        VPC1_VM_ID = self.cases.case_data['VPC1_VM_ID']
        VPC1_VM_PUB_IP = self.cases.case_data["VPC1_VM_PUB_IP"]
        VPC2_VM_PRV_IP = self.cases.case_data["VPC2_VM_PRV_IP"]
        VPC2_VM_VIRT_PRV_IP = self.cases.case_data["VPC2_VM_VIRT_PRV_IP"]
        ssh_key_file = self.cases.case_data["ssh_key_file"]
        host_key_file = self.cases.case_data["host_key_file"]
        ssh_key = os.path.abspath(ssh_key_file)
        host_key = os.path.abspath(host_key_file)
        VPC2_ID = self.cases.case_data["VPC2_ID"]
        GW2_s2c_conn_name = self.cases.case_data["GW2_s2c_conn_name"]
        gw2_primary_gateway = self.cases.case_data["gw2_primary_gateway"]
        gw2_primary_gateway_backup = self.cases.case_data["gw2_primary_gateway_backup"]

        tunnel_status_check_retries = 10
        GW1_tunnel_up = False
        GW2_tunnel_up = False

        config = self.cases.case_data["s2c_config"]
        self.cases.end_test("dummy")

        self.logger.info("Start Adding Site2Cloud Connection on Gateway1")

        self.logger.info("Check if Site2Cloud is present in the current view area...")
        assert s2c_new.match_view_title(), "Site2Cloud view is not present"

        for case in self.case_list:
            if "test_case" in case:
                delete_files_in_directory(self.dir_path)
                self.cases.start_test(case)

                self.logger.info("Click 'Add New' button to create a new site2cloud connection...")
                s2c_new.new_button = "new"
                time.sleep(5)

                assert s2c_new.fill_conn_fields(**self.cases.case_data), "Fail to fill in Site2Cloud connection fields"
                s2c_new.ok_button = "ok"
                time.sleep(10)
                toaster_result = s2c_new.s2c_toaster.lower()
                assert (self.cases.expected_result[
                            'toaster'] in toaster_result), "Fail to create Site2Cloud connection: " + toaster_result
                time.sleep(10)

                self.logger.info("Download configuration template...")

                try:
                    # Find the site2cloud connection and click on it
                    s2c_view.find_s2c_conn(self.cases.case_data["04.conn_name"])
                    time.sleep(5)

                    # Start to download its configuration template
                    for keys,values in config.items():
                        self.logger.info("%s : %s" % (keys, values))
                    s2c_view.download_config(config["vendor"], config["platform"], config["software"])
                    time.sleep(20)
                except (TimeoutException, NoSuchElementException) as e:
                    self.logger.debug("Can not find the table with exception %s", str(e))
                    assert False

                # Search download folder to find the config file
                config_file_name = self.cases.case_data["02.vpc_id"] + "-" + self.cases.case_data["04.conn_name"] + ".txt"
                config_file = find_files_in_directory(self.dir_path, config_file_name)
                if not config_file:
                    self.logger.error("Can't find the downloaded configuration file %s", config_file_name)
                    assert False
                else:
                    config_file_abs = os.path.join(self.dir_path, config_file_name)
                    self.logger.info("Downloaded configuration file is %s", config_file_abs)

                self.logger.info("Start Importing Site2Cloud Connection")

                #s2c_new_gw2 = s2cc.S2C_New(self.driver, login_required=False)

                self.logger.info("Click 'Add New' button to create a new site2cloud connection...")
                s2c_new.new_button = "new"
                time.sleep(5)

                s2c_new.click_import_button()
                time.sleep(3)
                s2c_new.input_file_name_for_import(config_file_abs)
                time.sleep(5)

                s2c_new.select_vpc_id = VPC2_ID
                self.logger.debug("Site2Cloud VPC ID/VNet Name: %s", VPC2_ID)

                s2c_new.input_conn_name = GW2_s2c_conn_name
                self.logger.debug("Site2Cloud Connection Name: %s", GW2_s2c_conn_name)
                time.sleep(5)

                s2c_new.select_primary_gw = gw2_primary_gateway
                if self.cases.case_data["06.enable_ha"] == "select":
                    s2c_new.input_pre_shared_key_backup = s2c_new.input_pre_shared_key
                    s2c_new.select_backup_gw = gw2_primary_gateway_backup

                s2c_new.ok_button = "ok"
                time.sleep(5)
                toaster_result = s2c_new.s2c_toaster.lower()
                assert (self.cases.expected_result['toaster'] in toaster_result), "Fail to create Site2Cloud connection: " + toaster_result
                time.sleep(5)

                self.logger.info("SSH into the VM in VPC1")
                ssh_client = ssh_from_instance(self.logger, cloud_region, VPC1_VM_ID,
                                               VPC1_VM_PUB_IP, ssh_key, host_key, "ubuntu")

                self.logger.info("Ping the target IP %s", VPC2_VM_PRV_IP)
                if self.cases.case_data['03.conn_type'].lower() == "unmapped":
                    self.assertTrue(ping_from_instance(self.logger, ssh_client, VPC2_VM_PRV_IP))
                if self.cases.case_data['03.conn_type'].lower() == "mapped":
                    self.assertTrue(ping_from_instance(self.logger, ssh_client, VPC2_VM_VIRT_PRV_IP))

                self.logger.info("Check site2cloud %s tunnel status" % self.cases.case_data["04.conn_name"])
                for retry in range(0, tunnel_status_check_retries):
                    self.driver.refresh()
                    time.sleep(10)
                    GW1_status = s2c_view.get_s2c_element(self.cases.case_data["04.conn_name"], "Status")
                    self.logger.info("site2cloud tunnel status: " + GW1_status)
                    if "up" in GW1_status.lower():
                        GW1_tunnel_up = True
                        break
                    else:
                        self.logger.info("site2cloud tunnel current status: %s", GW1_status)
                        time.sleep(5)
                if GW1_tunnel_up:
                    self.logger.info("site2cloud %s tunnel is up", self.cases.case_data["04.conn_name"])
                    assert True
                else:
                    self.logger.error("site2cloud %s tunnel not up", self.cases.case_data["04.conn_name"])
                    assert False

                    self.logger.info("Check site2cloud %s tunnel status" % GW2_s2c_conn_name)
                for retry in range(0, tunnel_status_check_retries):
                    self.driver.refresh()
                    time.sleep(10)
                    GW2_status = s2c_view.get_s2c_element(GW2_s2c_conn_name, "Status")
                    self.logger.info("site2cloud tunnel status: " + GW2_status)
                    if "up" in GW2_status.lower():
                        GW2_tunnel_up = True
                        break
                    else:
                        time.sleep(5)
                if GW2_tunnel_up:
                    self.logger.info("site2cloud %s tunnel is up", GW2_s2c_conn_name)
                    assert True
                else:
                    self.logger.error("site2cloud %s tunnel not up", GW2_s2c_conn_name)
                    assert False

                s2c_conn_names = [self.cases.case_data["04.conn_name"], GW2_s2c_conn_name]
                for s2c_conn_name in s2c_conn_names:
                    s2c_view.delete_conn(s2c_conn_name)
                    toaster_result = s2c_view.s2c_toaster.lower()
                    assert (self.cases.expected_result['toaster'] in toaster_result), "Fail to delete " + s2c_conn_name

                self.cases.end_test(case)

        delete_files_in_directory(self.dir_path)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()