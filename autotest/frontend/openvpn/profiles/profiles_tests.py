import unittest, logging, time
from selenium import webdriver
import autotest.lib.webui_pages.openvpn as ov
import autotest.lib.webui_pages.actions_in_common as actions
from autotest.frontend.webuitest import *
from autotest.lib.test_utils import testcases

class ProfilesTests(WebUITest):
    cases = testcases(__name__)

    def test01_set_up(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        openvpn_view = ov.OpenVPN(self.driver)

        self.logger.info("Expanding OpenVPN...")
        openvpn_view.expand_openvpn()
        time.sleep(2)
        self.logger.info("Navigating to VPN Users...")
        openvpn_view.vpn_users()
        time.sleep(10)
        self.logger.info("Checking VPN user table is present in the current view area...")
        self.assertTrue(openvpn_view.is_user_table_present(), "VPN user table is not present")

        self.cases.start_test("set_up")
        self.logger.info("Clicking Add New button...")
        self.assertTrue(openvpn_view.click_add_button(),"Failed to find Add New button")
        time.sleep(3)
        self.logger.info("Checking if add user panel is present...")
        self.assertTrue(openvpn_view.is_add_user_panel_present(),"Failed to find Add User panel")

        self.logger.info("Start to fill new user form")
        openvpn_view.fill_new_user_form(**self.cases.case_data)

        time.sleep(3)
        self.logger.info("Click OK button")
        self.assertTrue(actions_in_common.click_ok_button(),"Failed to add a vpn user")

        self.logger.info("Checking the result of adding a vpn user...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'], result, "Failed to add a vpn user")
        actions_in_common.close_message()

        time.sleep(5)
        self.logger.info("Check the user is present in VPN user table")
        self.assertTrue(openvpn_view.user_table.is_data_present(self.driver,1,self.cases.case_data['user_name']),"Failed to findthe user in VPN user table")

        self.cases.end_test("set_up")

    def test02_create_profile(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        openvpn_view = ov.OpenVPN(self.driver)

        self.logger.info("Navigating to Profiles...")
        openvpn_view.profiles()
        time.sleep(3)

        self.logger.info("Check if profile table panel is present")
        self.assertTrue(openvpn_view.is_profile_table_panel_present(),"Failed to find profile table")

        self.cases.start_test("test_case_1")
        self.logger.info('Click New Profile button')
        self.assertTrue(openvpn_view.click_new_profile(),'Failed to click New Profile button')
        self.logger.info("Check if New profile panel is present")
        self.assertTrue(openvpn_view.is_new_profile_panel_present(),"Failed to find New Profile Panel")

        time.sleep(3)
        self.logger.info("Input Profile Name")
        openvpn_view.profile_name = self.cases.case_data['profile_name']
        self.assertTrue(openvpn_view.click_ok_new_profile(),"Failed to click OK to create a Profile")

        self.logger.info("Checking the result of creating new profile...")
        result = actions_in_common.get_message()
        self.assertEqual(self.cases.expected_result['toaster'], result, "Fail to create new profile")
        actions_in_common.close_message()

        time.sleep(3)
        self.logger.info("Checking new profile in Profile table")
        self.assertTrue(openvpn_view.profile_table.is_data_present(self.driver,1, self.cases.case_data['profile_name']),"Failed to find the new profile")
        self.cases.end_test("test_case_1")

    def test03_edit_profile(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        openvpn_view = ov.OpenVPN(self.driver)

        time.sleep(5)
        self.logger.info("Start to test editing the profile")
        self.cases.start_test("test_case_2")
        self.logger.info("Click Edit button of the new profile")
        self.assertTrue(openvpn_view.click_edit_button(self.cases.case_data['profile_name']),"Failed to click Edit button")
        time.sleep(5)
        self.logger.info("Check if Profile Edit panel is present")
        self.assertTrue(openvpn_view.is_profile_edit_panel_present(),"Failed to find Profile Edit panel")

        self.logger.info('Toggle to show users associated with the Profile')
        self.assertTrue(openvpn_view.click_to_display_profile_users(),"Failed to click the button for displaying the profile users")
        time.sleep(2)

        self.logger.info('Toggle to hide Users of the profile')
        self.assertTrue(openvpn_view.click_to_display_profile_users(),
                        "Failed to click the button for displaying the profile users")
        self.cases.end_test("test_case_2")

        self.cases.start_test("test_case_3")
        self.logger.info('Click Add New to create a policy for the profile')
        self.assertTrue(openvpn_view.click_add_new_policy(),"Failed to click add new policy for the profile")

        time.sleep(5)
        self.logger.info('Fill the form for new policy')
        openvpn_view.fill_new_policy_form(**self.cases.case_data)

        self.logger.info("Click Save button for the policy")
        self.assertTrue(openvpn_view.click_policy_save_button(self.cases.case_data["target"]),'Failed to click Save button')

        self.logger.info("Update the policy")
        self.assertTrue(openvpn_view.update_policies())

        self.logger.info('check the result')
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'], result, "Failed to save the policy")
        actions_in_common.close_message()

        time.sleep(5)
        self.logger.info("Check if the policy is saved in the policy table")
        self.assertTrue(openvpn_view.policy_table.is_data_present(self.driver,2,self.cases.case_data['target']),"Failed to find the policy just created")

        self.cases.end_test('test_case_3')

    def test04_delete_policy(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        openvpn_view = ov.OpenVPN(self.driver)

        time.sleep(5)
        self.logger.info("Delete the policy for the profile")
        self.cases.start_test("test_case_4")
        self.assertTrue(openvpn_view.click_policy_delete_button(self.cases.case_data["target"]),"Failed to click Delete button")

        self.logger.info("Update the policy")
        self.assertTrue(openvpn_view.update_policies())

        self.logger.info('check the result of deleting the policy')
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'], result, "Failed to delete the policy")
        actions_in_common.close_message()

        self.logger.info("Check if the policy is saved in the policy table")
        self.assertFalse(openvpn_view.policy_table.is_data_present(self.driver, 2, self.cases.case_data['target']),
                        "Failed to find the policy just created")
        self.cases.end_test("test_case_4")

        self.logger.info("Dismiss Profile Edit panel")
        self.assertTrue(openvpn_view.dismiss_profile_edit_panel(),"Failed to click Cancel button for edting Profile")

    def test05_attach_detach_user(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        openvpn_view = ov.OpenVPN(self.driver)

        time.sleep(5)
        self.logger.info("Attach a user to the profile")
        self.cases.start_test("test_case_5")
        self.assertTrue(openvpn_view.click_attach_user_button(self.cases.case_data['profile_name']),"Failed to click Attach User button")

        time.sleep(10)
        self.logger.info("Check if Attach User panel is present")
        self.assertTrue(openvpn_view.is_attach_user_panel_present(),'Failed to find Attach User panel')

        self.logger.info("Select a VPC ID")
        openvpn_view.select_vpc_id = self.cases.case_data['vpc_id']
        time.sleep(10)
        self.logger.info('select a user')
        openvpn_view.select_user_name = self.cases.case_data['user_name']
        time.sleep(3)
        self.logger.info("Click OK button to attach the user")
        self.assertTrue(actions_in_common.click_ok_button(),"Failed to click OK button to attach user")

        self.logger.info('check the result of attaching user to the profile')
        result = actions_in_common.get_message()
        self.assertEqual(self.cases.expected_result['toaster'], result, "Failed to attach user")
        actions_in_common.close_message()
        time.sleep(5)
        self.logger.info("Check if the user is in the Users of the profile; Click Edit button of the new profile")
        self.assertTrue(openvpn_view.click_edit_button(self.cases.case_data['profile_name']), "Failed to click Edit button")
        time.sleep(5)
        self.logger.info("Check if Profile Edit panel is present")
        self.assertTrue(openvpn_view.is_profile_edit_panel_present(), "Failed to find Profile Edit panel")

        time.sleep(5)
        self.logger.info('Click to show users associated with the Profile')
        self.assertTrue(openvpn_view.click_to_display_profile_users(),
                        "Failed to click the button for displaying the profile users")
        time.sleep(5)
        self.logger.info("Check the user is listed in the user detail of the profile")
        self.assertIn(self.cases.case_data['user_name'],openvpn_view.show_profile_user_detail(),"The user is not found in the user list")

        self.cases.end_test("test_case_5")

        self.logger.info("Dismiss Profile Edit panel")
        self.assertTrue(openvpn_view.dismiss_profile_edit_panel(),
                        "Failed to click Cancel button for ediing Profile")

        time.sleep(5)
        self.cases.start_test("test_case_6")
        self.logger.info("Detach a user to the profile")
        self.assertTrue(openvpn_view.click_detach_user_button(self.cases.case_data['profile_name']), "Failed to click Detach User button")

        time.sleep(10)
        self.logger.info("Check User Form panel is present")
        self.assertTrue(openvpn_view.is_detach_user_panel_present(), 'Failed to find Detach User panel')

        self.logger.info("Select a VPC ID")
        openvpn_view.select_profile_detach_vpc_id = self.cases.case_data['vpc_id']
        time.sleep(10)
        self.logger.info('select a user')
        openvpn_view.select_profile_detach_user_name = self.cases.case_data['user_name']
        time.sleep(5)
        self.logger.info("Click OK button to detach the user")
        self.assertTrue(openvpn_view.click_detach_ok_button(), "Failed to click OK button to detach user")

        self.logger.info('check the result of detaching user from the profile')
        result = actions_in_common.get_message()
        self.assertEqual(self.cases.expected_result['toaster'], result, "Failed to detach user")
        actions_in_common.close_message()

        self.logger.info("Check the user is no longer associated with the profile; Click Edit button of the new profile")
        self.assertTrue(openvpn_view.click_edit_button(self.cases.case_data['profile_name']), "Failed to click Edit button")

        self.logger.info("Check if Profile Edit panel is present")
        self.assertTrue(openvpn_view.is_profile_edit_panel_present(), "Failed to find Profile Edit panel")

        time.sleep(5)
        self.logger.info('Click to show users associated with the Profile')
        self.assertTrue(openvpn_view.click_to_display_profile_users(),
                        "Failed to click the button for displaying the profile users")

        self.logger.info("Check the user is no longer in the user detail of the profile")
        self.assertNotIn(self.cases.case_data['user_name'], openvpn_view.show_profile_user_detail(), "The user is still present in the user list")

        self.cases.end_test("test_case_6")

        self.logger.info("Dismiss Profile Edit panel")
        self.assertTrue(openvpn_view.dismiss_profile_edit_panel(),
                        "Failed to click Cancel button for editing Profile")

    def test06_tear_down(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        openvpn_view = ov.OpenVPN(self.driver)
        time.sleep(5)
        self.logger.info("Navigating to VPN Users...")
        openvpn_view.vpn_users()
        time.sleep(5)
        self.cases.start_test("tear_down")
        self.logger.info("Delete the vpn user")
        self.assertTrue(openvpn_view.click_user_delete_button(self.cases.case_data['user_name']),"Failed to click delete button")
        self.logger.info("Click OK to delete the specified user")
        self.assertTrue(actions_in_common.confirm_ok(),"Failed to confirm for deletion")

        self.logger.info("Checking the result of deleting a VPN user...")
        result = actions_in_common.get_message()
        self.assertIn(self.cases.expected_result['toaster'], result, "Failed to delete the VPN user")
        actions_in_common.close_message()
        time.sleep(5)
        self.logger.info("Verify if the user is removed from the user table")
        self.assertFalse(openvpn_view.user_table.is_data_present(self.driver,1,self.cases.case_data['user_name']))

        self.cases.end_test("tear_down")

    def test07_delete_profile(self):
        actions_in_common = actions.ActionsInCommon(self.driver)
        openvpn_view = ov.OpenVPN(self.driver)

        self.logger.info("Navigating to Profiles...")
        openvpn_view.profiles()
        time.sleep(5)

        self.logger.info('Delete the profile')
        self.cases.start_test("test_case_7")
        self.assertTrue(openvpn_view.click_delete_profile_button(self.cases.case_data['profile_name']),"Failed to click Delete button")

        time.sleep(3)
        self.logger.info("Click OK button to delete the profile")
        self.assertTrue(actions_in_common.confirm_ok(), "Failed to click OK button to delete Profile")

        self.logger.info('Check the result of deleting the profile')
        result = actions_in_common.get_message()
        self.assertEqual(self.cases.expected_result['toaster'], result, "Failed to delete the profile")
        actions_in_common.close_message()

        self.logger.info("Check the profile is no longer in the profile list")
        self.assertFalse(openvpn_view.profile_table.is_data_present(self.driver,1,self.cases.case_data['profile_name']),"Profile is still present in the profile list")
        self.cases.end_test("test_case_7")
