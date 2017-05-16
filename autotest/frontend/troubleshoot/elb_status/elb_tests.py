__author__ = 'Rong'
import unittest, logging, time
from selenium import webdriver
import autotest.lib.webui_pages.elb_diagnostic as es
import autotest.lib.webui_pages.gateway as gw
import autotest.lib.webui_pages.actions_in_common as actions
import datetime
import boto.ec2.elb
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases

class ELBPageTest(WebUITest):
    cases = testcases(__name__)

    """
        Note:There a few things that needed to be changed for smooth run
        1)in config file:
          -uccURL
          -login_username
          -login_password(These only need to be change for once and the test should be able to run)
          -vpc_id(Any of the gateway's vpc_id that you have that uses ELB)
        2)others:
        this test uses boto to check for backend whether the elb has been compeletly deleted.If you have not used boto
        you can comment out the lines.If you have boto IAM set up, please change connecting_to_aws function in
        elb_diagnostic to the region where the VPC is at
    """
    #Creaete an elb enabled gateway for this test
    def test01_set_up(self):
        gateway_view = gw.Gateway(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)
        time.sleep(10)

        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(10)
        self.logger.info("Checking Gateway is present in the current view area...")
        self.assertTrue(gateway_view.is_gateway_table_present(), "Gateway view is not present")

        self.cases.start_test("set_up")
        self.logger.info("Clicking New Gateway button")
        gateway_view.click_new_gateway_button()
        self.assertTrue(gateway_view.new_gateway_panel_is_present(), "New Gateway panel is not found")

        """
        Create a new gateway in eu-central-1, VPN access: enabled, ELB: enabled, LDAP disabled.
        """
        self.logger.info("Start to create a new gateways on AWS")

        assert gateway_view.fill_new_gateway_fields(**self.cases.case_data), "Failed to fill in Gateway configuration fields"

        time.sleep(1)
        self.logger.info("Clicking OK to create New Gateway...")
        self.assertTrue(actions_in_common.click_ok_button(), "Failed to click OK for new gateway")

        actions_in_common.wait_progress_bar()
        self.logger.info("Checking the result of creating new gateway...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'] + self.cases.case_data['06.gateway_name'], result, "Fail to create a new gateway")
        actions_in_common.close_message()

        time.sleep(10)
        self.logger.info("Checking new gateway's state in gateway table")
        self.assertEquals(
            gateway_view.gateway_table.check_specific_row_data(self.driver, self.cases.case_data['06.gateway_name'],
                                                               2), self.cases.expected_result['status'],
            "Gateway state is not up.")

        self.cases.end_test("set_up")

    def test02_elb_status(self):
        elb_diagnostic_view = es.ELB_Diagnostic(self.driver)
        time.sleep(10)
        self.logger.info("Navigating to Troubleshooting")
        title = elb_diagnostic_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title,
                         "Troubleshooting link does not exist")
        self.logger.info("Navigating to ELB Status")
        elb_diagnostic_view.navigate_to_elb_status()
        self.logger.info("Check if ELB Status is the right page")
        self.assertTrue(elb_diagnostic_view.current_url(),"Not on the ELB Status page")
        time.sleep(10)

        """
        Choose the VNet,take down the information of the ELB and store in logger
        and save the txt file and delete the ELB
        """
        self.cases.start_test("test_case_1")
        self.logger.info("Check if the current account has ELB service")
        if elb_diagnostic_view.check_toaster() == True:
            time.sleep(10)
            self.logger.info (
                "This cloud does not support ELB,closing the toaster..." )
            self.assertTrue (
                elb_diagnostic_view.click_toaster_close_button ( ) ,
                "Close button does not exist" )
            self.logger.info (
                "Check for toaster to see if it is really closed,might shown exeptions" )
            time.sleep(5)
            self.assertFalse ( elb_diagnostic_view.check_toaster ( ) ,
                               "Toaster not closed" )
            self.logger.info (
                "Toaster closed" )
        else:
            self.logger.info (
                "This cloud support ELB, moving on...." )
        #NOTE:can comment out next 3 line if you don't use boto
        #elb_number = elb_diagnostic_view.connecting_to_aws()
        #self.assertNotEqual(None, elb_number,
        #                    "Something is wrong with the AWS connection,the ELB could not be located")
        self.logger.info(
            "Current VNet name on dropdown menu is : " + elb_diagnostic_view.select_vnet_name)
        if elb_diagnostic_view.select_vnet_name != self.cases.case_data["vpc_id"]:
            try:
                elb_diagnostic_view.select_vnet_name = self.cases.case_data["vpc_id"]
                self.logger.info("The VNet name to be deleted:" + elb_diagnostic_view.select_vnet_name)
            except:
                self.logger.exception("Could not change to the selected VNet name")
            self.assertEqual(elb_diagnostic_view.select_vnet_name, self.cases.case_data["vpc_id"], "VNet does not exist")
        time.sleep(10)
        self.logger.info("Checking for ELB..will fail if no ELB is attached")
        self.assertTrue(elb_diagnostic_view.is_lb_present(),
                         "There is no ELB attach with this VNet")
        lb_name = elb_diagnostic_view.lb_name_information()
        self.logger.info("Information of the deleted ELB:" + lb_name)
        self.logger.info("Check for the delete button to delete the ELB..")
        self.assertTrue(elb_diagnostic_view.click_delete_button(),
                        "Delete button does not exist")
        self.logger.info("Delete button exist and clicked")
        self.logger.info(
            "Check for pop up and assume pop up has the right message..")
        assert elb_diagnostic_view.check_popup_exist, "No pop up is shown"
        # self.logger.info("Pop up okay, click Cancel to abort the process")
        # self.assertTrue( elb_diagnostic_view.click_pop_up_cancel_button(),
        #                 "Cancel button does not exist")
        # self.logger.info("Cancel button exist and clicked")
        # time.sleep(10)
        # self.logger.info("Check if pop up message is completely gone,will pass if pop up is gone, might show exception")
        # self.assertFalse(elb_diagnostic_view.check_popup_exist(),"Pop-up window is not closed")
        self.logger.info("Pop up okay, click OK to start the process")
        self.assertTrue(elb_diagnostic_view.click_pop_up_ok_button(),
                        "OK button does not exist")
        time.sleep(120)
        result = elb_diagnostic_view.success_toaster
        self.logger.info("The message shown is:%s", result)
        self.assertIn(self.cases.expected_result['toaster'], result,
                      "ELB could not be deleted")
        time.sleep(10)
        self.logger.info(
            "Closing the toaster...")
        self.assertTrue(elb_diagnostic_view.click_toaster_close_button(),
                        "Close button does not exist")
        self.logger.info(
            "Close button exist and clicked")
        time.sleep(5)
        self.logger.info(
            "Check for toaster to see if it is really closed,might shown exceptions")
        self.assertFalse(elb_diagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info(
            "Toaster closed")
        self.cases.end_test("test_case_1")
        # NOTE:can comment out next 5 line if you don't use boto
        # self.logger.info("Check on aws website whether the ELB has been completly deleted..")
        # self.logger.info(
        #     "Might show exception, its normal")
        # self.assertTrue(lb_name not in elb_diagnostic_view.connecting_to_aws(),
        #                     "ELB not successfully deleted on AWS website")
        # self.assertFalse(elb_diagnostic_view.is_lb_present(),
        #                 "Controller still shows existence of ELB even through it is deleted")

        # delete teh elb enabled gateway for this test

    def test03_tear_down(self):
        gateway_view = gw.Gateway(self.driver)
        actions_in_common = actions.ActionsInCommon(self.driver)

        self.logger.info("Navigating to Gateway")
        gateway_view.navigate_to_gateway()
        time.sleep(10)

        self.logger.info("Checking Gateway is present in the current view area...")
        self.assertTrue(gateway_view.is_gateway_table_present(), "Gateway view is not present")

        self.cases.start_test("tear_down")
        self.logger.info("check if the specified gateway exists...")
        self.assertTrue(gateway_view.gateway_table.is_data_present(self.driver, 2, self.cases.case_data["gateway_name"]),
                        "Could not find the specified gateway")
        time.sleep(10)
        self.logger.info("Deleting the specified gateway...")
        self.assertTrue(gateway_view.delete_gateway(self.cases.case_data["gateway_name"]),
                        "Failed to click Delete button for the specified gateway")

        time.sleep(10)
        self.logger.info("Clicking OK to delete the specified gateway...")
        actions_in_common.confirm_ok()

        time.sleep(5)
        self.logger.info("Checking the result of deleting gateway...it takes a while")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result["toaster"], result, "Fail to delete a new gateway")

        time.sleep(10)
        self.logger.info("Verifying deleted gateway is no longer in gateway list")
        self.assertFalse(gateway_view.gateway_table.is_data_present(self.driver, 2, self.cases.case_data["gateway_name"]),
                         "Found the specified gateway")
        actions_in_common.close_message()
        self.cases.end_test("tear_down")