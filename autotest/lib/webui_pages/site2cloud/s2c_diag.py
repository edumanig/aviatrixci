from GUI.v2.lib.common_elements import *
from GUI.v2.lib.page_locators import *
from GUI.v2.site2cloud.s2c_base import S2C_Base

class SelectVPCID(DropdownSelect):
    locator = S2CViewLocators.DIAG_VPC_ID

class SelectConnection(DropdownSelect):
    locator = S2CViewLocators.DIAG_CONNECTION

class SelectGateway(DropdownSelect):
    locator = S2CViewLocators.DIAG_GATEWAY

class SelectAction(DropdownSelect):
    locator = S2CViewLocators.DIAG_ACTION

class OkButton(ActionButton):
    locator = S2CViewLocators.DIAG_OK_BTN

class DiagResult(OutputPanel):
    locator = S2CViewLocators.DIAG_OUTPUT

class S2C_Diag(S2C_Base):
    select_vpc_id = SelectVPCID()
    select_conn = SelectConnection()
    select_gw = SelectGateway()
    select_action = SelectAction()
    ok_button = OkButton()
    diag_result = DiagResult()

    def __init__(self, driver, login_required=False):
        self.driver = driver
        S2C_Base.__init__(self, self.driver, login_required=login_required)

    def fill_conn_fields(self, **kwargs):
        field_list = ["vpc_id", "conn", "gateway", "action"]

        for key, value in kwargs.items():
            if not key in field_list:
                self.logger.error("Invalid Site2Cloud diagnostics fields. Abort...")
                return False
            try:
                if key.lower() == "vpc_id":
                    self.select_vpc_id = value
                    self.logger.debug("Site2Cloud VPC ID/VNet Name: %s", value)
                if key.lower() == "conn":
                    time.sleep(2)
                    self.select_conn = value
                    self.logger.debug("Site2Cloud Connection: %s", value)
                if key.lower() == "gateway":
                    time.sleep(2)
                    self.select_gw = value
                    self.logger.debug("Site2Cloud Gateway: %s", value)
                if key.lower() == "action":
                    self.select_action = value
                    self.logger.debug("Site2Cloud Action: %s", value)
            except NoSuchElementException as e:
                self.logger.exception("Site2Cloud diagnostics fill fields exception: %s", str(e))
                return False
        return True

