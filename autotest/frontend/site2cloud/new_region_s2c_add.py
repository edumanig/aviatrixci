__author__ = 'lmxiang'

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from GUI.v2.lib.common_elements import *
from tests.utils.test_utils import avx_logger
import GUI.v2.site2cloud.s2c_conn as pages


class New_Region_S2C_Add(unittest.TestCase):
    """
    Add new site2cloud connection
    """

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(__name__)
        #cls.logger =avx_logger()
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.maximize_window()

    def test_s2c_add(self):
        self.logger.info("Start Adding Site2Cloud Connection")
        s2c_data = []
        basic_data = {"01.description":"Basic unmapped site2cloud connection",
                      "06.enable_ha":"deselect",
                      "02.vpc_id":"vpc-4cf63c25",
                      "03.conn_type":"Unmapped",
                      "08.primary_gw":"was-mum-no-vpn-1",
                      "04.conn_name":"ProdConn",
                      "05.customer_gw_ip":"10.100.0.6",
                      "customer_nw_real":"10.101.0.0/16"
                      }
        s2c_data.append(basic_data)

        mapped_data = {"01.description":"Mapped site2cloud connection",
                       "06.enable_ha":"deselect",
                       "02.vpc_id":"vpc-4cf63c25",
                       "03.conn_type":"Mapped",
                       "08.primary_gw":"was-mum-no-vpn-1",
                       "04.conn_name":"ProdMapped",
                       "05.customer_gw_ip":"10.100.0.7",
                       "customer_nw_real":"10.102.0.0/16",
                       "customer_nw_virtual":"10.202.0.0/16",
                       "cloud_sub_real":"20.102.0.0/16",
                       "cloud_sub_virtual":"20.202.0.0/16"
                       }
        s2c_data.append(mapped_data)

        null_data = {"01.description":"Null encryption",
                     "06.enable_ha":"deselect",
                     "02.vpc_id":"vpc-4cf63c25",
                     "03.conn_type":"Unmapped",
                     "08.primary_gw":"was-mum-no-vpn-1",
                     "04.conn_name":"ProdNull",
                     "05.customer_gw_ip":"10.100.0.8",
                     "customer_nw_real":"10.103.0.0/16",
                     "cloud_sub_real":"20.103.0.0/16",
                     "07.null_encr":"select"
                     }
        s2c_data.append(null_data)

        ha_unmapped_data = {"01.description":"Site2cloud unmapped HA",
                            "06.enable_ha":"select",
                            "02.vpc_id":"vpc-4cf63c25",
                            "03.conn_type":"Unmapped",
                            "08.primary_gw":"was-mum-no-vpn-1",
                            "09.backup_gw":"aws-mum-vpn-nat-elb",
                            "04.conn_name":"ProdUnmappedHA",
                            "05.customer_gw_ip":"10.100.0.9",
                            "customer_nw_real":"10.104.0.0/16",
                            "cloud_sub_real":"20.104.0.0/16",
                            "07.null_encr":"deselect"
                            }
        s2c_data.append(ha_unmapped_data)

        ha_mapped_data = {"01.description": "Site2cloud mapped HA",
                          "06.enable_ha":"select",
                          "02.vpc_id":"vpc-4cf63c25",
                          "03.conn_type":"Mapped",
                          "08.primary_gw":"was-mum-no-vpn-1",
                          "09.backup_gw":"aws-mum-vpn-nat-elb",
                          "04.conn_name":"ProdMappedHA",
                          "05.customer_gw_ip":"10.100.0.10",
                          "customer_nw_real":"10.105.0.0/16",
                          "customer_nw_virtual":"10.205.0.0/16",
                          "cloud_sub_real": "20.105.0.0/16",
                          "cloud_sub_virtual": "20.205.0.0/16",
                          "07.null_encr": "deselect"
                          }
        s2c_data.append(ha_mapped_data)

        s2c_view = pages.S2C_New(self.driver, login_required=True)
        self.logger.info("Navigating to Site2Cloud")
        s2c_view.navigate_to_s2c()
        time.sleep(10)

        self.logger.info("Check if Site2Cloud is present in the current view area...")
        assert s2c_view.match_view_title(),"Site2Cloud view is not present"

        self.logger.info("Fill site2cloud connection creation data")

        for data in s2c_data:
            """
            if data['HA'].lower() == "enable" and s2c_view.is_ha_enabled():
                self.logger.info("Site2Cloud HA is already enabled. No action needed...")
            elif data['HA'].lower() == "enable" and not s2c_view.is_ha_enabled():
                self.logger.info("Site2Cloud HA is disabled. Enable it now...")
                time.sleep(5)
                s2c_view.ha_switch_button = "select"
                toaster_result = s2c_view.s2c_toaster.lower()
                assert ("success" in toaster_result), "Fail to enable HA"
                time.sleep(5)
            elif data['HA'].lower() == "disable" and not s2c_view.is_ha_enabled():
                self.logger.info("Site2Cloud HA is already disabled. No action needed...")
            elif data['HA'].lower() == "disable" and s2c_view.is_ha_enabled():
                self.logger.info("Site2Cloud HA is enabled. Disable it now...")
                self.logger.info("Disable Site2Cloud HA...")
                time.sleep(5)
                s2c_view.ha_switch_button = "deselect"
                time.sleep(10)
                toaster_result = s2c_view.s2c_toaster.lower()
                assert ("success" in toaster_result), "Fail to disable HA"
                time.sleep(5)
            else:
                self.logger.error("Wrong value for HA. Either 'enable' or 'disable'. Abort...")
                return False
            """
            self.logger.info("Click 'Add New' button to create a new site2cloud connection...")
            s2c_view.new_button = "new"
            time.sleep(10)

            assert s2c_view.fill_conn_fields(**data),"Fail to fill in Site2Cloud connection fields"
            s2c_view.ok_button = "ok"
            time.sleep(10)
            toaster_result = s2c_view.s2c_toaster.lower()
            assert ("success" in toaster_result),"Fail to create Site2Cloud connection: "+toaster_result
            time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__ == "__main__":
    unittest.main()