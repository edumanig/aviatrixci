import logging
from lxml import etree
from lxml.cssselect import CSSSelector
from collections import OrderedDict
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from autotest.lib.common_elements import *
from autotest.lib.page_locators import *
from autotest.lib.webui_pages.basepage import BasePage


"""
==========================================================================================
For Dashboard
==========================================================================================
"""


class Dashboard(BasePage):
    peering_info = {}
    gateway_list = []
    total_enc_peering = 0

    vpn_user_table = TableData(Dashboardlocators.VPN_USER_TABLE_FOR_TABLE)

    def navigate_to_dashboard(self):
        return Click(Dashboardlocators.NAVIGATE_TO_DASHBOARD).clicking(self.driver)

    def get_gateways(self):
        gateways_info=[]
        gateways_on_map = self.driver.find_elements(*Dashboardlocators.GATEWAYS)
        stale = False
        while stale is not True:
            try:
                gateways_on_map[0].get_attribute("aria-lable")
            except StaleElementReferenceException:
                stale = True

        self.logger.info("Get the current info of gateways on map...")
        gateways_on_map = self.driver.find_elements(*Dashboardlocators.GATEWAYS)

        for gateway_element in gateways_on_map:
            gateways_info.append(gateway_element.get_attribute('aria-label'))

        return gateways_info

    def check_peering_links(self):
        red_links = []
        green_links = []

        get_links = self.driver.find_elements(*Dashboardlocators.GREEN_LINK)
        if get_links is None:
            get_links = self.driver.find_elements(*Dashboardlocators.RED_LINK)
            if get_links is None:
                self.logger.info("Can't find any peering links on the map")
        stale = False
        while stale is not True:
            try:
                if get_links:
                    get_links[0].get_attribute("d")
                else: stale = True
            except StaleElementReferenceException:
                stale = True

        green_links = self.driver.find_elements(*Dashboardlocators.GREEN_LINK)
        red_links = self.driver.find_elements(*Dashboardlocators.RED_LINK)

        if green_links:
            self.logger.info("Checking green links...")
            for i in range(len(green_links),2):
                if green_links[i].get_attribute("d") != green_links[i+1].get_attribute("d"):
                    self.logger.info("Incorrect green link found")
                    return False

        if red_links:
            self.logger.info("Checking red links...")
            for i in range(len(red_links),2):
                if red_links[i].get_attribute("d") != red_links[i+1].get_attribute("d"):
                    self.logger.info("Incorrect red link found")
                    return False

        if len(green_links) != 0 or len(red_links) != 0:
            self.logger.info("checking total links found on map matches total peering tunnels...")
            if (len(green_links)+len(red_links))/2 != self.total_enc_peering:
                self.logger.debug("Total links found on the map: "+str(int((len(green_links)+len(red_links))/2)) )
                self.logger.debug("Total peering tunnels in peering table: " + str(self.total_enc_peering))
                self.logger.info("Total cncrypted peering tunnel is not the same as that of the peering table")
                return False
        return True

    def check_gateways(self):
        gateway_name_on_map = []
        current_gateways = self.get_gateways()
        for gw in current_gateways:
            gateway_name_on_map.append(gw[:gw.find("<br>")])

        for gateway_name in self.gateway_list:
            if gateway_name:
                if not gateway_name in gateway_name_on_map:
                    self.logger.debug(gateway_name + " is not found on dashboard map")
                    return False
                else:
                    self.logger.debug(gateway_name + " is found on current map")
        return True

    def get_peering_info(self):
        current_gateways = self.get_gateways()
        peering_info_on_map = {}

        if current_gateways:
            for gw in current_gateways:
                if "table" in gw:
                    gw_name = gw[:gw.find("<br>")]
                    tbl = gw[gw.find("<table"):]
                    sel = CSSSelector('tbody tr td')
                    tbl_element = sel(etree.XML(tbl))
                    tbl_data = [d.text for d in tbl_element]

                    for i in range(0,len(tbl_data),2):
                        peering_info_on_map.setdefault(gw_name, {})[tbl_data[i]] = tbl_data[i+1]
        return peering_info_on_map

    def check_peering_info(self):
        current_peerings = self.get_peering_info()

        self.logger.info("Checking the peered gateway info ...")
        if current_peerings.keys() != self.peering_info.keys():
            self.logger.error("Total peered gateways do not match when compared to the peering table")
            return False
        for key in current_peerings.keys():
            if current_peerings[key].keys() != self.peering_info[key].keys():
                self.logger.error("Not all peered gateways are found for the gateway")
                return False
            if None in current_peerings[key].values() or "N/A ms" in current_peerings[key].values():
                self.logger.error("Latency is empty or N/A")
                return False
        return True

    def is_vpn_session_table_present(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(Dashboardlocators.VPN_HISTORY_TABLE))
            session_table = self.driver.find_element(*Dashboardlocators.VPN_HISTORY_TABLE)
            if session_table:
                if session_table.text == "VPN session history":
                    return True
            return False
        except (TimeoutException,NoSuchElementException,StaleElementReferenceException):
            self.logger.exception("Could not find VPN session table panel")

    def get_total_user_count(self):
        try:
            panel_title = self.driver.find_element(*Dashboardlocators.USER_TABLE_TILTE)
            if panel_title:
                return panel_title.text[-1]
            return None
        except NoSuchElementException:
            self.logger.exception("Failed to find the panel title for Active VPN USER ")

    def close_history_panel(self):
        return Click(Dashboardlocators.VPN_HISTORY_CLOSE_BUTTON).clicking(self.driver)

    def discconect_vpn_user(self,value):
        vpn_user_table = TableData(Dashboardlocators.VPN_USER_TABLE_FOR_TABLE)
        vpn_user_table.click_button_in_the_row(self.driver, 1, 7, value,"[confirm='Are you sure about disconnecting this user?']")



