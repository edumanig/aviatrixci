import unittest, logging, time, platform,datetime
from selenium import webdriver
import autotest.lib.webui_pages.diagnostics as diag
from autotest.run_autotest import config
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases


class DBDiagnosticsPageTest(WebUITest):
    cases = testcases(__name__)

    def test06_restart_server(self):
        diagnostic_view = diag.Diagnostics(self.driver)
        time.sleep(3)

        """
        Tries to restart the server and cancel the process
        """
        self.logger.info("Assert if the Restart Server button exist")
        self.assertTrue(diagnostic_view.click_restart_server_button(), "Restart Server button does not exist")
        self.logger.info("Restart Server button exist and clicked")
        self.logger.info("Check for pop-up ..")
        time.sleep(5)
        assert diagnostic_view.confirm_pop_up_exist, "No pop-up is shown"
        self.logger.info("Assert if the Cancel button exist")
        self.assertTrue(diagnostic_view.click_pop_up_cancel_button(), "Cancel button does not exist")
        self.logger.info("Cancel button exist and clicked")
        time.sleep(10)
        self.logger.info("Check for pop-up,will pass if pop-up is gone,might show exception")
        self.assertFalse(diagnostic_view.check_popup_exist(),"Pop-up not close even after cancel is pressed")

        self.cases.end_test("test_case_6")
        """
        self.logger.info(
            "Assert if the OK button exist")
        self.assertTrue(diagnostic_view.click_pop_up_ok_button(),
                        "OK button does not exist")
        self.logger.info("Pop up okay, click OK to start the process")
        time.sleep(100)
        """

    def test03_drop_database(self):
        diagnostic_view = diag.Diagnostics(self.driver)
        time.sleep(3)

        """
        Tries to start the Drop Database process and cancel the process
        """
        self.cases.start_test("test_case_3")
        self.logger.info("Current Database name on dropdown menu is : " + diagnostic_view.select_database)

        if diagnostic_view.select_database != self.cases.case_data["database_name"]:
            try:
                diagnostic_view.select_database = self.cases.case_data["database_name"]
                self.logger.info("The Database to be dropped is : " + diagnostic_view.select_database)
            except:
                self.logger.exception("Could not change to the selected gateway name")
            self.assertEqual(diagnostic_view.select_database, self.cases.case_data["database_name"], "Database does not exist.")
        time.sleep(5)
        self.logger.info("Find the Drop Database button")
        self.assertTrue(diagnostic_view.click_drop_database_button(), "Drop Database button does not exist")
        self.logger.info("Drop Database button exist and clicked")
        self.logger.info("Check for pop-up and assume pop-up has the right message..")
        time.sleep(5)
        assert diagnostic_view.confirm_pop_up_exist, "No pop up is shown"
        self.logger.info("Assert if the Cancel button exist")
        self.assertTrue(diagnostic_view.click_pop_up_cancel_button(), "Cancel button does not exist")
        self.logger.info("Pop-up okay, click Cancel to abort the process")
        time.sleep(10)
        self.logger.info("Check for pop-up,will pass if pop-up is gone,might show exception")
        self.assertFalse(diagnostic_view.check_popup_exist(),"Pop-up not close even after cancel is pressed")
        self.cases.end_test("test_case_3")
        """
        self.logger.info(
            "Assert if the OK button exist")
        self.assertTrue(diagnostic_view.click_pop_up_ok_button(),
                        "OK button does not exist")
        self.logger.info("Pop up okay, click OK to start the process")
        time.sleep(10)
        """

    def test04_dump_collection(self):
        diagnostic_view = diag.Diagnostics(self.driver)
        time.sleep(3)

        """
        Tries to choose the Collection Name and continue the Dump Collection
        process. Then record the Dump Collection in a txt file and in logger
        """
        self.cases.start_test("test_case_4")
        self.logger.info("Checking the name on Database to ensure passing of this test")
        self.logger.info(
                "Current Database name on dropdown menu is : " + diagnostic_view.select_database)

        if diagnostic_view.select_database != self.cases.case_data["database_name"]:
            try:
                self.logger.info(
                    "Not the right database name,change it to the right one")
                diagnostic_view.select_database = self.cases.case_data["database_name"]
                self.logger.info("The Database to be dropped is : " + diagnostic_view.select_database)
            except:
                self.logger.exception("Could not change to the selected gateway name")
            self.assertEqual(diagnostic_view.select_database, self.cases.case_data["database_name"], "Database does not exist.")
        time.sleep(5)
        self.logger.info(
            "Current Collection Name on dropdown menu is : " + diagnostic_view.select_collection_name)

        if diagnostic_view.select_collection_name != self.cases.case_data["collection_name"]:
            try:
                diagnostic_view.select_collection_name = self.cases.case_data["collection_name"]
                self.logger.info(
                    "The Collection Name to be dumped:" + diagnostic_view.select_collection_name)
            except:
                self.logger.exception(
                    "Could not change to the selected Collection Name")
            self.assertEqual(diagnostic_view.select_collection_name, self.cases.case_data["collection_name"], "Collection name is not correct")
        time.sleep(5)
        self.logger.info("Assert if the Dump Collection button exist")
        self.assertTrue(diagnostic_view.click_dump_collection_button(), "Dump Collection button does not exist")
        self.logger.info("Dump Collection button exist and clicked")
        time.sleep(30)
        result = diagnostic_view.dump_collection_result
        self.assertNotEqual("[]", result,  "Dump Collection has no result")
        self.logger.info("Dump Collection Result:\n" + result)
        file_name = (
            'dump_collection_result_{:%Y%m%d-%H%M%S}.txt'.format(
                datetime.datetime.now()))
        if platform.system() == "Windows":
            save_path_file_name = "results\\temp\\" + file_name
        else:
            save_path_file_name = "results//temp//" + file_name
        dump_collection_result_file = open(save_path_file_name, "w")
        dump_collection_result_file.write('Dump collection result logged at: {:%Y-%m-%d %H:%M:%S}\n'.format(datetime.datetime.now()))
        dump_collection_result_file.write(result)
        dump_collection_result_file.close()
        self.logger.info("Dump collection result also saved at: " + save_path_file_name)
        diagnostic_view.click_close_dump_collection_button()

        self.cases.end_test("test_case_4")

    def test01_delete_collection(self):
        diagnostic_view = diag.Diagnostics(self.driver)
        time.sleep(10)

        self.logger.info("Navigating to Troubleshooting")
        title = diagnostic_view.navigate_to_troubleshooting()
        self.assertEqual("Troubleshoot", title, "Troubleshooting link does not exist")
        self.logger.info("Navigating to DB Diagnostic")
        diagnostic_view.navigate_to_dbdiagnostics()
        self.logger.info("Check if Diagnostic is the right page")
        self.assertTrue(diagnostic_view.dbdiag_url(), "Not on DB Diagnostics page")
        time.sleep(10)
        """
        Tries to use Delete Collection to delete collection but
        cancel the process
        """
        self.cases.start_test("test_case_1")
        self.logger.info("Checking the name on Database to ensure passing of this test")
        self.logger.info("Current Database name on dropdown menu is : " + diagnostic_view.select_database)

        if diagnostic_view.select_database != self.cases.case_data["database_name"]:
            try:
                self.logger.info(
                    "Not the right database name,change it to the right one")
                diagnostic_view.select_database = self.cases.case_data["database_name"]

                self.logger.info(
                    "The Database to be dropped is : " + diagnostic_view.select_database)
            except:
                self.logger.exception(
                    "Could not change to the selected gateway name")
            self.assertEqual(diagnostic_view.select_database, self.cases.case_data["database_name"], "Database does not exist.")
        time.sleep(5)
        self.logger.info(
            "Current Collection Name on dropdown menu  is : " + diagnostic_view.select_collection_name)

        if diagnostic_view.select_collection_name != self.cases.case_data["collection_name"]:
            try:
                diagnostic_view.select_collection_name = self.cases.case_data["collection_name"]
                self.logger.info("The Collection Name to be deleted is:"+ diagnostic_view.select_collection_name)
            except:
                self.logger.exception(
                    "Could not change to the selected Collection Name")
            self.assertEqual(diagnostic_view.select_collection_name, self.cases.case_data["collection_name"], "Collection name does not exist.")
        time.sleep(5)
        self.logger.info("Assert if the Delete Collection button exist")
        self.assertTrue(diagnostic_view.click_delete_dump_collection_button(), "Delete Collection button does not exist")
        self.logger.info("Delete Collection button exist and clicked")
        self.logger.info("Check for pop-up and assume pop-up has the right message..")
        time.sleep(5)
        assert diagnostic_view.confirm_pop_up_exist, "No pop-up is shown"
        self.logger.info("Assert if the Cancel button exist")
        self.assertTrue(diagnostic_view.click_pop_up_cancel_button(), "Cancel button does not exist")
        self.logger.info("Pop-up okay, click Cancel to abort the process")
        time.sleep(10)
        self.logger.info("Check for pop-up,will pass if pop-up is gone,might show exceptions")
        self.assertFalse(diagnostic_view.check_popup_exist(),"Pop-up not close even after cancel is pressed")
        self.cases.end_test("test_case_1")
        """
        self.logger.info(
            "Assert if the OK button exist")
        self.assertTrue(diagnostic_view.click_pop_up_ok_button(),
                        "OK button does not exist")
        self.logger.info("Pop up okay, click OK to start the process")
        time.sleep(10)
        """

    def test05_dump_document(self):
        diagnostic_view = diag.Diagnostics(self.driver)
        time.sleep(3)

        """
        Input in the Document and press the Dump Document button
        Check if there is an error
        """
        self.cases.start_test("test_case_5")
        self.logger.info("The document to be dumped is:")
        diagnostic_view.input_document = self.cases.case_data["diagnostic_input_document"]
        self.logger.info(diagnostic_view.input_document)
        self.logger.info("Find the Dump Document ..")
        self.assertTrue(diagnostic_view.click_dump_document_button(), "Dump Document button does not exist")
        self.logger.info("Dump Document button exist and clicked")
        time.sleep(10)
        self.logger.info("Check for error message,will pass if error message is shown")
        result = diagnostic_view.is_error_message_shown()
        #NOTE:If you do not have any good Document value,just use assertIn to pass this test instead of assertNotIn,if not other test queued after this would fail to
        self.assertIn("Error:", result, "Document key:value does not exist,try other key:value")
        self.logger.info("The message shown is:%s", result)
        time.sleep(10)
        self.assertTrue(diagnostic_view.click_toaster_close_button(), "Close button does not exist")
        self.logger.info("Close button exist and clicked")
        time.sleep(5)
        self.logger.info("Check for toaster to see if it is really closed,might show exceptions")
        self.assertFalse(diagnostic_view.check_toaster(), "Toaster not closed")
        self.logger.info("Toaster closed")

        self.cases.end_test("test_case_5")

    def test02_delete_document(self):
        diagnostic_view = diag.Diagnostics(self.driver)
        time.sleep(3)

        """
        Input to the document and tries to delete the document and cancel the
        process
        """
        self.cases.start_test("test_case_2")
        self.logger.info("The document to be deleted is:")
        diagnostic_view.input_document = self.cases.case_data["diagnostic_input_document"]
        self.logger.info(diagnostic_view.input_document)
        self.logger.info("Checking if the Delete Document button exist")
        self.assertTrue( diagnostic_view.click_delete_document_button(), "Delete Document button does not exist")
        self.logger.info("Delete Document button exist and clicked")
        self.logger.info("Check for pop up and assume pop up has the right message..")
        time.sleep(5)
        assert diagnostic_view.confirm_pop_up_exist, "No pop up is shown"
        self.logger.info("Pop-up exist..")
        self.logger.info("Assert if the Cancel button exist")
        self.assertTrue(diagnostic_view.click_pop_up_cancel_button(), "Cancel button does not exist")
        self.logger.info("Cancel button exist and clicked")
        self.logger.info("Pop-up okay, click Cancel to abort the process")
        time.sleep(10)
        self.assertFalse(diagnostic_view.check_popup_exist(), "Pop-up not close even after cancel is pressed")

        self.cases.end_test("test_case_2")
        """
        self.logger.info(
            "Assert if the OK button exist")
        self.assertTrue(diagnostic_view.click_pop_up_ok_button(),
                        "OK button does not exist")
        self.logger.info("Pop up okay, click ok to start the process")
        time.sleep(10)
        """