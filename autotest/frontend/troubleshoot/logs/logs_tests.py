__author__ = 'Rong'

import unittest, logging, time, platform, datetime
from selenium import webdriver
import autotest.lib.webui_pages.logs as logs
from autotest.run_autotest import config
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases
#please check config uccURL


class LogsPageTest(WebUITest):
    cases = testcases(__name__)

    """
         Note:There a few things that needed to be changed for smooth run
         1)in config file:
           -uccURL
           -login_username
           -login_password(These only need to be change for once and the test should be able to run)
           -gateway_name_troubleshooting(input a gateway exist on your controller)
           -host name(input a website,or you can use mine)


    """

    def test_upload_tracelog(self):
        log_view = logs.Logs(self.driver)

        self.logger.info("Check if test is on the right page")
        self.assertTrue(log_view.check_for_log_page(), "Tracelog Page is loaded correctly")
        """
        Upload a Tracelog and make sure it is submitted
        """
        self.cases.start_test("test_case_3")
        self.logger.info(
            "Current Gateway Name on dropdown menu is : " + log_view.select_gateway)

        if log_view.select_gateway != self.cases.case_data["gateway_name"]:
            try:
                log_view.select_gateway = self.cases.case_data["gateway_name"]
                self.logger.info("The Gateway information to be sent is" + log_view.select_gateway)
            except:
                self.logger.exception(
                    "Could not change to the selected Gateway Name")
            self.assertEqual(log_view.select_gateway, self.cases.case_data["gateway_name"], "Gateway Name does not exist")
        time.sleep(10)
        self.logger.info("Assert if the OK button exist")
        self.assertTrue(log_view.click_ok_button(), "OK button does not exist")
        self.logger.info("OK button exist and clicked")
        time.sleep(60)
        result = log_view.tracelog_sent
        self.logger.info("Check if the message is correct")
        self.logger.info("The message shown is:%s", result)
        self.assertIn(self.cases.expected_result["toaster"], result, "Tracelog could not be sent")
        time.sleep(10)
        self.logger.info("Close the toaster to keep the test going")
        self.assertTrue(log_view.click_toaster_close_button(), "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed, might shown exceptions")
        self.assertFalse(log_view.check_toaster(), "Toaster not closed")
        self.logger.info("Toaster closed")

        self.cases.end_test("test_case_3")

    def test_display_command_log(self):
        log_view = logs.Logs(self.driver)

        self.logger.info("Navigating to Troubleshooting")
        title = log_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title,
                         "Troubleshooting link does not exist")
        self.logger.info("Navigating to Logs")
        log_view.navigate_to_log()
        self.assertTrue(log_view.check_for_log_page(),
                        "Tracelog Page is loaded correctly")
        time.sleep(10)

        """
        Press Display to display Command Log,store the Command Log
        information both in logger and in txt format
        """
        self.cases.start_test("test_case_1")
        self.logger.info(
            "Check for the Display button to see if it exist..")
        self.assertTrue(log_view.click_display_button(),
                        "Display button does not exist")
        self.logger.info("Display button exists. Click Display button to display Command Log, Log might be long...")
        time.sleep(20)
        result = log_view.command_log_result
        self.assertNotEqual("", result,
                            "Nothing is shown in command log.There is an error.")
        self.logger.info("Command Log:\n" + result)
        file_name = (
            'command_log_{:%Y%m%d-%H%M%S}.txt'.format(datetime.datetime.now()))
        if platform.system() == "Windows":
            save_path_file_name = "results\\temp\\" + file_name
        else:
            save_path_file_name = "results//temp//" + file_name
        command_log_file = open(save_path_file_name, "w")
        command_log_file.write('Command Log result logged at: {:%Y-%m-%d %H:%M:%S}\n'.format(datetime.datetime.now()))
        command_log_file.write(result + "\n")
        command_log_file.close()
        self.logger.info("Command log result also saved at: " + save_path_file_name)
        self.cases.end_test("test_case_1")

    def test_ping_utility(self):
        log_view = logs.Logs(self.driver)
        self.logger.info("Check if test is on the right page")
        self.assertTrue(log_view.check_for_log_page(),
                        "Tracelog Page is loaded correctly")
        """
        Try to ping google.com and record the ping result in logger and in a
        txt file
        """
        self.cases.start_test("test_case_2")
        self.logger.info("The host name to be pinged is:")
        log_view.host_name = self.cases.case_data['host_name_to_ping']
        self.logger.info(log_view.host_name)
        self.logger.info(
            "Assert if the Ping button exist")
        self.assertTrue(log_view.click_ping_button(),
                        "Ping button does not exist")
        self.logger.info(
            "Ping button exist and clicked")
        time.sleep(20)
        result = log_view.ping_result
        self.assertNotEqual("",result,"Nothing is shown in Ping text area")
        self.assertTrue(self.cases.expected_result['not_in_ping_text'] not in result,"Something is wrong with the connection, please check the ping result")
        self.logger.info("Ping Result:\n" + result)
        file_name = (
            'ping_result_{:%Y%m%d-%H%M%S}.txt'.format(datetime.datetime.now()))
        if platform.system() == "Windows":
            save_path_file_name = "results\\temp\\" + file_name
        else:
            save_path_file_name = "results//temp//" + file_name
        ping_result_file = open(save_path_file_name,"w")
        ping_result_file.write(
            'Ping result logged at: {:%Y-%m-%d %H:%M:%S}\n'.format(
                datetime.datetime.now()))
        ping_result_file.write(result + "\n")
        ping_result_file.close()
        self.logger.info("Ping result also saved at: " +save_path_file_name)

        self.cases.end_test("test_case_2")