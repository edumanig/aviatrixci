from selenium.webdriver.common.by import By


class ActionsInCommonLocators:
    #VIEW_TITLE = (By.TAG_NAME, 'h1')
    HELP = (By.LINK_TEXT,"Help")
    CURRENT_VERSION = (By.CSS_SELECTOR,"[uib-dropdown-menu=''] .ng-binding")

    SUBMIT_OK_BUTTON = (By.CSS_SELECTOR, "[type='submit']")
    SUBMIT_CANCEL_BUTTON = (By.CSS_SELECTOR, "[ng-click='hidePanel()']")

    CONFIRM_POPUP = (By.CSS_SELECTOR, ".modal-content")
    CONFIRM_OK = (By.CSS_SELECTOR, ".ng-binding.btn-primary")
    CONFIRM_CANCEL = (By.CSS_SELECTOR, "[ng-click='cancel()']")

    TOASTER_MESSAGE = (By.CSS_SELECTOR, "div.toast-message")
    CLOSE_MESSGAE = (By.CSS_SELECTOR, ".toast-close-button")

    EDIT_CANCEL_BUTTON = (By.CSS_SELECTOR,"[ng-click='hideEditPanel()']")

    PASSPHRASE_FORM = (By.CSS_SELECTOR,"[dw-loading='enable_ssh_frm']")
    ENABLE_SSH = (By.ID,"passphrase")
    PROGRESS_BAR = (By.TAG_NAME, "h4")
    SPINNING_WHEEL = (By.CSS_SELECTOR, "div.dw-spinner")

class UCCSignInLocators:
    LOGIN_FORM = (By.CSS_SELECTOR, ".login_main")
    USERNAME = (By.ID, "inputEmail")
    PASSWORD = (By.ID, "inputPassword")
    SIGN_IN_BUTTON = (By.CSS_SELECTOR,".btn-auth" )
    #Rey
    IS_SIGN_IN_OK = (By.CSS_SELECTOR, "i.fa.fa-server")

class Dashboardlocators:
    NAVIGATE_TO_DASHBOARD = (By.CSS_SELECTOR,".ion-android-home")
    MAP = (By.ID, "amChartMap")
    GATEWAYS = (By.CSS_SELECTOR,"svg [role='menuitem']")
    GREEN_LINK = (By.CSS_SELECTOR,"svg [stroke='green']")
    RED_LINK = (By.CSS_SELECTOR, "svg [stroke='red']")

    USER_TABLE_TILTE = (By.CSS_SELECTOR,"dashboard-table .panel-title")
    VPN_USER_TABLE_FOR_TABLE = "dashboard-table .table"
    VPN_HISTORY_TABLE = (By.CSS_SELECTOR,"h4")
    VPN_HISTORY_CLOSE_BUTTON = (By.CSS_SELECTOR,"button.close")


class OnboardingLocators:
    NAVIGATE_TO_ONBOARDING = (By.CSS_SELECTOR,".ion-plane")
    AWS = (By.LINK_TEXT,"AWS")
    AZURE_ARM = (By.LINK_TEXT,"Azure ARM")
    GCLOUD = (By.LINK_TEXT,"Gcloud")
    AWS_GOV = (By.LINK_TEXT,"AWS GOV")
    AZURE_CLASSIC = (By.LINK_TEXT,"Azure")
    AZURE_CHINA = (By.LINK_TEXT,"Azure CHINA")

    CUSTOMER_ID = (By.ID, 'customer_id')
    SAVE_BUTTON = (By.CSS_SELECTOR,"[dw-loading='step1'] [type='submit']")
    ACCOUNT_NAME = (By.ID,"account_name")
    EMAIL = (By.ID,"account_email_addr")
    PASSWORD = (By.ID,"account_password")
    COMFIRM_PASSWORD = (By.ID,"account_password2")

    AWS_ACCOUNT_NUMBER = (By.ID,"account_number")
    AWS_ACCESS_KEY = (By.ID,"account_access_key")
    AWS_SECRET_KEY =(By.ID,"account_secret_access_key")
    GOV_ACCOUNT_NUMBER = (By.ID,"awsgovcloud_account_number")
    GOV_ACCESS_KEY = (By.ID,"awsgovcloud_access_key")
    GOV_SECRET_KEY = (By.ID,"awsgovcloud_secret_key")
    GOV_CLOUDTRAIL_BUCKET = (By.ID,"trail_status")

    IAM_BASED_SELECT = (By.XPATH,"//input[@type='checkbox']")
    IAM_BASED_CLICK = (By.CSS_SELECTOR, ".checkbox-inline")
    AVTX_APP_ARN = (By.ID,"aws_role_arn")
    AVTX_EC2_ARN = (By.ID, "aws_role_ec2")

    ARM_SUBSCPT_ID = (By.ID,"arm_subscription_id")
    APP_ENDPOINT = (By.ID,"arm_ad_tenant_id")
    CLIENT_ID = (By.ID,"arm_ad_client_id")
    CLIENT_SECRET = (By.ID,"arm_ad_client_secret")

    GCLOUD_PROJECT_ID = (By.ID,"project")
    GCLOUD_PROJECT_CREDENTIALS = (By.ID,"gcloud_project_credentials")

    CREATE_BUTTON = (By.CSS_SELECTOR,"[dw-loading='step4'] [type='submit']")


class GatewayViewLocators:
    NAVIGATE_TO_GATEWAY = (By.CSS_SELECTOR, "i.fa.fa-server")
    GATEWAY_TABLE = (By.CSS_SELECTOR,"[dw-loading='gateway_table']")
    GATEWAY_TABLE_FOR_TABLE = "[dw-loading='gateway_table'] .table"

    NEW_GATEWAY_BUTTON = (By.CSS_SELECTOR,"[ng-click='showGatewayForm()']")

    NEW_GATEWAY_PANEL = (By.CSS_SELECTOR,"[bb-panel-title='Create a new Gateway']")

    CLOUD_TYPE_SELECT = (By.CSS_SELECTOR,"[ng-model='newgateway.cloud_type']")

    ACCOUNTNAME_SELECT = (By.CSS_SELECTOR,"[ng-model='newgateway.account_name']")

    REGION_SELECT = (By.CSS_SELECTOR,"[ng-change='onRegionChange()']")
    ZONE_SELECT = (By.CSS_SELECTOR,"[ng-model='newgateway.zone']")
    BKUPGW_ZONE_SELECT = (By.ID,"bkupgw_zone")

    VPC_ID_SELECT = (By.CSS_SELECTOR,"[ng-model='newgateway.vpc_id']")

    GATEWAY_NAME = (By.CSS_SELECTOR,"[ng-model='newgateway.gateway_name']")

    PUBLIC_SUBNET_SELECT = (By.CSS_SELECTOR,"[ng-model='newgateway.public_subnet']")

    GATEWAY_SIZE_SELECT = (By.CSS_SELECTOR,"[ng-model='newgateway.vpc_size']")

    VPN_ACCESS_CHECKBOX_IS_SELECTED = (By.XPATH,"(//input[@type='checkbox'])[2]")
    VPN_ACCESS_CHECKBOX_CLICK = (By.XPATH,"//div[2]/label/span")

    ENABLE_NAT_CHECKBOX_IS_SELECTED = (By.XPATH,"//input[@type='checkbox']")
    ENABLE_NAT_CHECKBOX_CLICK = (By.XPATH,"//label/span")

    VPN_CIDR_BLOCK = (By.CSS_SELECTOR,"[ng-model='newgateway.vpn_cidr_block']")
    TWO_STEP_AUTH_SELECT = (By.CSS_SELECTOR,"[ng-model='newgateway.enable_otp']")
    MAX_CONNECTIONS = (By.CSS_SELECTOR,"[ng-model='newgateway.max_conn']")

    SPLIT_TUNNEL_MODE_YES_IS_SELECTED = (By.XPATH,"//div[5]/div[2]/label/input")
    SPLIT_TUNNEL_MODE_YES_CLICK = (By.XPATH,"//div[5]/div[2]/label/span")

    SPLIT_TUNNEL_MODE_NO_IS_SELECTED = (By.XPATH,"//label[2]/input")
    SPLIT_TUNNEL_MODE_NO_CLICK = (By.XPATH,"//label[2]/span")

    ENABLE_ELB_YES_IS_SELECTED = (By.XPATH,"//div[7]/div[2]/label/input")
    ENABLE_ELB_YES_CLICK = (By.XPATH,"//div[7]/div[2]/label/span")

    ENABLE_ELB_NO_IS_SELECTED = (By.XPATH,"//div[7]/div[2]/label[2]/input")
    ENABLE_ELB_NO_CLICK = (By.XPATH,"//div[7]/div[2]/label[2]/span")

    ELB_NAME = (By.CSS_SELECTOR,"[ng-model='newgateway.elb_name']")

    ENABLE_CLIENT_CERT_SHARING_YES_IS_SELECTED = (By.XPATH,"//div[9]/div[2]/label/input")
    ENABLE_CLIENT_CERT_SHARING_YES_CLICK = (By.XPATH,"//div[9]/div[2]/label/span")
    ENABLE_CLIENT_CERT_SHARING_NO_IS_SELECTED = (By.XPATH, "//div[9]/div[2]/label[2]/input")
    ENABLE_CLIENT_CERT_SHARING_NO_CLICK = (By.XPATH, "//div[9]/div[2]/label[2]/span")

    ENABLE_PBR_IS_SELECTED =(By.CSS_SELECTOR,"[ng-model='newgateway.enable_pbr']")
    ENABLE_PBR_CLICK = (By.XPATH,"//div[11]/div/label/span")
    PBR_SUBNET = (By.CSS_SELECTOR,"[ng-model='newgateway.pbr_subnet']")
    PBR_DEFAULT_GATEWAY = (By.CSS_SELECTOR,"[ng-model='newgateway.pbr_default_gateway']")

    PBR_LOGGING_IS_SELECTED = (By.CSS_SELECTOR, "[ng-model='newgateway.pbr_logging']")
    PBR_LOGGING_CLICK = (By.XPATH,"//div[2]/div/label/span")

    ENABLE_LDAP_IS_SELECTED = (By.XPATH, "//div[12]/div/label/input")
    ENABLE_LDAP_CLICK = (By.XPATH,"//div[12]/div/label/span")

    LDAP_SERVER = (By.CSS_SELECTOR,"[ng-model='newgateway.ldap_server']")

    LDAP_USE_SSL_IS_SELECTED = (By.CSS_SELECTOR,"[ng-model='newgateway.ldap_use_ssl']")
    LDAP_USE_SSL_CLICK = (By.XPATH,"//div[14]/div[2]/div/label/span")

    BIND_DN = (By.CSS_SELECTOR,"[ng-model='newgateway.ldap_bind_dn']")
    LDAP_PASSWORD = (By.CSS_SELECTOR,"[ng-model='newgateway.ldap_password']")
    BASE_DN = (By.CSS_SELECTOR,"[ng-model='newgateway.ldap_base_dn']")
    USERNAME_ATTRIBUTE = (By.CSS_SELECTOR,"[ng-model='newgateway.ldap_username_attribute']")
    GROUP_MEMBERSHIP_DN = (By.CSS_SELECTOR,"[ng-model='newgateway.ldap_additional_ladp_req']")
    LDAP_USER = (By.CSS_SELECTOR,"[ng-model='newgateway.ldap_user']")

    TEST_LDAP_BUTTON = (By.CSS_SELECTOR,"[ng-click='testLDAP()']")

    SAVE_TEMPLATE_IS_SELECTED = (By.CSS_SELECTOR, "[ng-model='newgateway.save_template']")
    SAVE_TEMPLATE_CLICK = (By.XPATH, "//div[9]/div/label/span")

    OK_BUTTON = (By.XPATH,"//button[@type='submit']")
    CANCEL_BUTTON = (By.XPATH,"//button[@ng-click='hidePanel()']")
    GATEWAY_PROGRESS_BOX = (By.CSS_SELECTOR, ".modal-dialog .modal-body")
    CLOSE_PROGRESS_BOX = (By.CSS_SELECTOR, ".modal-dialog .btn-danger")

    EDIT_GATEWAY_BUTTON = (By.CSS_SELECTOR,"[ng-click='startEdit(gridApi.selection.getSelectedRows()[0])']")
    DELETE_GATEWAY_BUTTON = (By.CSS_SELECTOR,"[ng-click='deleteGatewayInGrid(gridApi.selection.getSelectedRows()[0])']")
    VIEW_INSTANCE_BUTTON = (By.CSS_SELECTOR,"[ng-click='viewInstance()']")
    GATEWAY_ROWS = (By.CSS_SELECTOR, ".ui-grid-row")
    ITEMS_PER_PAGE = (By.CSS_SELECTOR,"#gateway-list-grid select")

    EDIT_PANEL = (By.CSS_SELECTOR,"[ng-show='showEditPanel']")
    EDIT_PANEL_TITLE = (By.CSS_SELECTOR,".panel-title.ng-binding")
    GATEWAY_DETAIL = (By.CSS_SELECTOR,"i.ion-navicon-round.fake-link")
    DETAIL_BOX = (By.CSS_SELECTOR,"pre.ng-binding")

    BACKUP_GATEWAY_SUBNET = (By.ID, "bkupgw_subnet")
    ENABLE_HA_BUTTON = (By.CSS_SELECTOR, "[confirm='Are you sure to enable HA?']")
    DISABLE_HA_BUTTON = (By.CSS_SELECTOR, "[confirm='Are you sure to disable HA?']")
    FORCE_SWITCHOVER_BUTTON = (By.CSS_SELECTOR, "[ng-click='forceSwitchover()']")

    CREATE_HAGW_BUTTON =(By.CSS_SELECTOR,"[ng-click='createPeerHAGW()']")

    ALLOW_ALL_BUTTON = (By.CSS_SELECTOR, "[ng-model='currentGateway.policy.base_policy'][value='allow-all']")
    DENY_ALL_BUTTON = (By.CSS_SELECTOR, "[ng-model='currentGateway.policy.base_policy'][value='deny-all']")

    ENABLE_PACKET_LOGGING_IS_SELECTED = (By.CSS_SELECTOR, "[title='Log packets that match the Base Policy.']")
    ENABLE_PACKET_LOGGING_CLICK = (By.XPATH, "(//input[@type='checkbox'])[8]")

    RESET_TO_DEFAULT_BUTTON = (By.CSS_SELECTOR, "[ng-click='reset_action()']")
    POLICY_TABLE_FOR_TABLE = "[dw-loading='edit_gateway_form'] table"
    NEW_SECURITY_POLICY_BUTTON = (By.CSS_SELECTOR, "[ng-click='addNewPolicy()']")
    POLICY_SRC_IP = (By.NAME, "s_ip")
    POLICY_DST_IP = (By.NAME, "d_ip")
    POLICY_PROTOCOL = (By.NAME, "protocol")
    POLICY_PORT_RANGE = (By.NAME, "port")
    POLICY_ACTION = (By.NAME, "deny_allow")
    POLICY_LOGGING = (By.NAME, "log_enable")
    SAVE_POLICY_INLINE = ".btn-primary[type='submit']"
    CANCEL_POLICY_INLINE = "[shown='inserted == item'] .btn-default"
    NEW_POLICY_INLINE = ".btn-primary[ng-click='addPolicy($index+1)']"
    SAVE_DEPLOY_POLICIES = (By.CSS_SELECTOR, "[ng-click='savePolicy()']")
    DELETE_SAVED_POLICY = ".btn-danger"

    GATEWAY_RESIZING_SELECT = (By.CSS_SELECTOR,"[ng-model='changeFrm.gw_size']")
    GATEWAY_SIZE_CHANGE_BUTTON = (By.CSS_SELECTOR,"[dw-loading='edit_gateway_form'] [type='submit']")

    CLOSE_EDIT_PANEL =(By.CSS_SELECTOR,"[ng-click='hideEditPanel()']")

"""
    For Account and User Account (Rey)
"""

class AccountViewLocators:
    #NAVIGATE_TO_ACCOUNT = (By.CSS_SELECTOR, "ion-ios-people")
    NAVIGATE_TO_CLOUD_ACCOUNT = (By.XPATH, "//li[3]/a/span")
    NAVIGATE_TO_CLOUD_ACCOUNT_TEXT = (By.LINK_TEXT, "Cloud Accounts")
    NEW_CLOUD_ACCOUNT_BUTTON = (By.XPATH, "//button[@type='button']")
    NEW_CLOUD_ACCOUNT_NAME = (By.XPATH, "//input[@id='account_name']")
    NEW_ACCOUNT_PANEL = (By.XPATH, "//label[contains(.,'Cloud Type')]")
    NEW_ACCOUNT_EMAIL = (By.XPATH,"//input[@id='account_email_addr']")
    NEW_ACCOUNT_PW = (By.XPATH,"//input[@id='account_password']")
    NEW_ACCOUNT_PW2 = (By.XPATH, "//input[@id='account_password2']")

    AWS_ACCOUNT_CHECKBOX_IS_SELECTED = (By.XPATH, "//input[@type='checkbox']")
    AWS_ACCOUNT_CHECKBOX_CLICK = (By.XPATH, "//label/span")
    AWS_ACCOUNT_NUM = (By.XPATH, "//input[@id='account_number']")
    AWS_ACCOUNT_ACCESS_KEY = (By.ID, "account_access_key")
    AWS_ACCOUNT_SECRET_KEY = (By.ID, "account_secret_access_key")

    GCE_ACCOUNT_CHECKBOX_IS_SELECTED = (By.XPATH, "(//input[@type='checkbox'])[3]")
    GCE_ACCOUNT_CHECKBOX_CLICK = (By.XPATH, "//div[3]/label/span")
    GCE_ACCOUNT_PROJECT_ID = (By.ID, "project")
    GCE_ACCOUNT_CREDENTIALS = (By.ID, "gcloud_project_credentials")

    ARM_ACCOUNT_CHECKBOX_IS_SELECTED = (By.XPATH, "(//input[@type='checkbox'])[4]")
    ARM_ACCOUNT_CHECKBOX_CLICK = (By.XPATH, "//div[4]/div/label/span")
    ARM_ACCOUNT_SUB_ID = (By.ID, "arm_subscription_id")
    ARM_TENANT_ID = (By.ID, "arm_ad_tenant_id")
    ARM_CLIENT_ID = (By.ID, "arm_ad_client_id")
    ARM_CLIENT_SECRET = (By.ID, "arm_ad_client_secret")

    AZURE_ACCOUNT_CHECKBOX_IS_SELECTED = (By.XPATH, "(//input[@type='checkbox'])[2]")
    AZURE_ACCOUNT_CHECKBOX_CLICK = (By.XPATH, "//div[2]/label/span")
    AZURE_ACCOUNT_SUB_ID = (By.ID, "azure_subscription_id")

    GOV_ACCOUNT_CHECKBOX_IS_SELECTED = (By.XPATH, "(//input[@type='checkbox'])[5]")
    GOV_ACCOUNT_CHECKBOX_CLICK = (By.XPATH, "//div[4]/div[2]/label/span")
    GOV_ACCOUNT_NUM = (By.ID, "awsgovcloud_account_number")
    GOV_ACCOUNT_ACCESS_KEY = (By.ID, "awsgovcloud_access_key")
    GOV_ACCOUNT_SECRET_KEY = (By.ID, "awsgovcloud_secret_key")
    GOV_TRAIL_BUCKET = (By.ID, "trail_status")

    AZCN_ACCOUNT_CHECKBOX_IS_SELECTED = (By.XPATH, "(//input[@type='checkbox'])[6]")
    AZCN_ACCOUNT_CHECKBOX_CLICK = (By.XPATH, "//div[4]/div[3]/label/span")
    AZCN_ACCOUNT_SUB_ID = (By.ID, "azurechinacloud_subscription_id")

    OK_BUTTON = (By.XPATH, "//button[@type='submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[@ng-click='hidePanel()']")
    ACCOUNT_CREATED_MESSAGE = (By.CSS_SELECTOR, "div.toast-message")
    ACCOUNT_CREATED_MESSAGE_CLOSE = (By.CSS_SELECTOR, "button.toast-close-button.ng-scope")
    ACCOUNT_CREATED_MESSAGE_ERROR = (By.CSS_SELECTOR, "div.toast.toast-error")

    ACCOUNT_INFO_TABLE = (By.CSS_SELECTOR, "table.aws-accounts-table")
    ACCOUNT_TABLE_FOR_DATA = "table.aws-accounts-table"


class UserAccountViewLocators:
    NAVIGATE_TO_USER_ACCOUNT = (By.XPATH, "//li[3]/a/span")
    NAVIGATE_TO_USER_ACCOUNT_TEXT = (By.LINK_TEXT, "Account Users")
    NEW_USER_ACCOUNT_BUTTON = (By.XPATH, "//button[@type='button']")
    NEW_USER_ACCOUNT_PANEL = (By.XPATH, "//h3[contains(.,'Add a new user')]")
    USER_ACCOUNT_NAME = (By.XPATH, "//input[@id='username']")
    USER_ACCOUNT_EMAIL = (By.XPATH, "//input[@id='user_email']")
    CLOUD_ACCOUNT_NAME_SELECT = (By.ID, "account_name")
    USER_ACCOUNT_PW = (By.XPATH, "//input[@id='passwd']")
    USER_ACCOUNT_PW2 = (By.XPATH, "//input[@id='passwd2']")
    OK_BUTTON = (By.XPATH, "//button[@type='submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[@ng-click='hidePanel()']")
    USER_OLD_PASSWD = (By.ID, "old_passwd")
    USER_NEW_PW = (By.ID, "passwd3")
    USER_NEW_PW2 = (By.ID, "passwd4")
    USER_ACCOUNT_CREATED_MESSAGE = (By.CSS_SELECTOR, "div.toast-message")
    USER_ACCOUNT_CREATED_MESSAGE_CLOSE = (By.CSS_SELECTOR, "button.toast-close-button.ng-scope")
    USER_ACCOUNT_CREATED_MESSAGE_ERROR = (By.CSS_SELECTOR, "div.toast.toast-error")

    ACCOUNT_INFO_TABLE = (By.CSS_SELECTOR, "table.aws-accounts-table")
    OK_BUTTON = (By.CSS_SELECTOR, "[ba-panel-title='Add a new user'] [type='submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[@ng-click='hidePanel()']") #wrong
    USER_ACCOUNT_INFO_TABLE = (By.CSS_SELECTOR, "table.peering-table")

class AdvancedConfigLocators:
    EXPAND_ADVANCED_CONFIG = (By.CSS_SELECTOR, "i.fa.fa-cube")
    CREATE_VPC_POOL = (By.CSS_SELECTOR,"[href='#/envstamping/vpcpool']")

    CREATE_BUTTON = (By.CSS_SELECTOR,"[ng-click='startNew()']")
    POOL_TABLE_FOR_TABLE = "[dw-loading='pool_table'] .table"

    CLOUD_TYPE = (By.ID, "cloud_type")
    ACCOUNT_NAME = (By.ID,"account_name")
    POOL_NAME = (By.ID, "pool_name")
    NUMBER_OF_VPCS = (By.ID, "num_of_vpcs")
    VPC_CIDR = (By.ID, "vpc_cidr")
    VPC_REGION = (By.ID,"vpc_region")

    CREATE_POOL_FORM = (By.CSS_SELECTOR,"[dw-loading='add_pool_form']")
    CREATE_SUBMIT_BUTTON = (By.CSS_SELECTOR,"[type='submit']")
    CREATE_CANCEL_BUTTON = (By.CSS_SELECTOR,"[ng-click='hidePanel()']")

    VPC_POOL_TABLE = (By.CSS_SELECTOR,"[dw-loading='pool_table']")
    DELETE_POOL_BUTTON = "[confirm='Are you sure to delete this pool?']"

    #Join Function starts here
    JOIN_FUNCTION = (By.CSS_SELECTOR,"[href='#/envstamping/join']")
    JOIN_GATEWAY_PANEL = (By.CSS_SELECTOR,"[dw-loading='gateway_table']")
    JOIN_GATEWAY_TABLE_FOR_TABLE = "[dw-loading='gateway_table'] table"

    CONNECT_BUTTON = (By.CSS_SELECTOR,"[ng-click='showGatewayForm()']")
    JOIN_CREATE_PANEL = (By.CSS_SELECTOR,"[bb-panel-title='Connect Legacy VPC/VNet']")
    FORCE_SWITCHOVER = "[confirm='Are you sure to force switchover?']"
    DELETE_BUTTON = "[confirm='Are you sure to disconnect this gateway?']"
    ALLOW_SUBNET_BUTTON = "[ng-click='allowSubnet(item)']"
    DELETE_SUBNET_BUTTON = "[ng-click='deleteSubnet(item)']"

    #Connect Form  of Join Function seems to share the New Gateway form of UCC. Use the Gateway locators.
    ALLOW_SUBNET_PANEL = (By.CSS_SELECTOR,"[dw-loading='allow_form']")
    ALLOW_LOCAL_CIDR = (By.ID,"allow_cidr")
    ALLOW_SUBNET_OK_BUTTON = (By.CSS_SELECTOR,"[dw-loading='allow_form'] [type='submit']")
    ALLOW_SUBNET_CANCEL_BUTTON = (By.CSS_SELECTOR,"[ng-click='hideAllowPanel()']")

    DELETE_SUBNET_PANEL = (By.CSS_SELECTOR,"[dw-loading='delete_form']")
    DELETE_LOCAL_CIDR = (By.ID,"delete_cidr")
    DELETE_SUBNET_OK_BUTTON = (By.CSS_SELECTOR,"[dw-loading='delete_form'] [type='submit']")
    DELETE_SUBNET_CANCEL_BUTTON = (By.CSS_SELECTOR,"[ng-click='hideDeletePanel()']")


class PeeringLocators:
    NAVIGATE_TO_PEERING = (By.CSS_SELECTOR, "[href='#/peering']")

    ENCRYPTED_PEERING = (By.CSS_SELECTOR, "[heading='Encrypted Peering']")
    #TRANSITIVE_PEERING = (By.CSS_SELECTOR, "[heading='Transitive Peering']")

    ENC_PEERING_TABLE = (By.CSS_SELECTOR, "[dw-loading='enc_peering_table']")
    ENC_PEERING_TABLE_FOR_TABLE = "[dw-loading='enc_peering_table'] .table"
    NEW_ENC_PEERING_BUTTON = (By.CSS_SELECTOR,"[ng-click='startCreation()']")
    NEW_ENC_PEERING_PANEL = (By.CSS_SELECTOR,"[bb-panel-title='Add a new peering']")

    PEERING_VPC1 = (By.ID, "vpc1")
    PEERING_VPC2 = (By.ID, "vpc2")
    OVER_AWS_PEERING_IS_SELECTED = (By.XPATH,"//input[@type='checkbox']")
    OVER_AWS_PEERING_CLICK = (By.CSS_SELECTOR,".checkbox-inline")

    DIAG_DROPDOWN = "[data-toggle='dropdown']"
    DELETE_PEERING_BUTTON = "[confirm='Are you sure to unpeer this?']"

    """
    For Peering (Ryan Liu)
    """
    #TransitivePeeringPageLocator
    # Class attributes that represent web-elements from "Transitive-Peering" page/panel
    TRANSITIVE_PEERING = (By.LINK_TEXT, "Transitive Peering")

    NEW_TRANSITIVE_PEERING_BUTTON = (By.CSS_SELECTOR, "[ng-click='startTransCreation()']")
    NEW_TRANSITIVE_PEERING_PANEL = (By.CSS_SELECTOR,"[ng-show='showTransPanel']")
    DESTINATION_CIDR = (By.ID,"cidr")
    NEW_TRANSITIVE_PEERING_OK_BUTTON = (By.CSS_SELECTOR,"[dw-loading='trans_peering_panel'] [type='submit']")

    TRANSITIVE_PEERING_TABLE = (By.CSS_SELECTOR, "[dw-loading='trans_peering_table']")
    TRANSITIVE_PEERING_TABLE_FOR_TABLE = "[dw-loading='trans_peering_table'] table"

    SOURCE_GATEWAY = (By.CSS_SELECTOR,"[ng-model='currentTransPeering.source']")
    NEXTHOP_GATEWAY = (By.CSS_SELECTOR,"[ng-model='currentTransPeering.nexthop']")


class OpenVPNLocators:
    EXPAND_OPENVPN = (By.CSS_SELECTOR,".ion-android-wifi")
    VPN_USERS = (By.CSS_SELECTOR,"[href='#/openvpn/users']")
    CONFIGURATION = (By.CSS_SELECTOR,"[href='#/openvpn/configuration']")
    CERTIFICATE = (By.CSS_SELECTOR,"[href='#/openvpn/certificate']")
    PROFILES = (By.CSS_SELECTOR,"[href='#/openvpn/profiles']")

    VPN_USERS_TABLE = (By.CSS_SELECTOR,"[dw-loading='vpn_users_table']")
    VPN_USERS_TABLE_FOR_TABLE = "[dw-loading='vpn_users_table'] table"
    ADD_USER_BUTTON = (By.CSS_SELECTOR,"[ng-click='startCreation()']")
    ADD_USER_PANEL = (By.CSS_SELECTOR,"[dw-loading='vpn_users_form']")
    USER_VPC_ID = (By.ID, "vpc_id2")
    USER_LB_NAME = (By.ID, "lb_name")
    USER_NAME = (By.ID,"username")
    USER_EMAIL = (By.ID,"user_email")
    USER_DELETE_BUTTON = "[confirm='Are you sure to delete this VPN user?']"
    PROFILE_IS_SELECT = (By.CSS_SELECTOR,"[ng-model='addFormData.use_profile']")
    PROFILE_CLICK =(By.CSS_SELECTOR, "label span")
    PROFILE_NAME = (By.ID,"profile_name")
    REISSUE_BUTTON = "[ng-click='reissueCert(item.vpc_id, item._id)']"

    DISPLAY_PUBLIC_IP_PANEL = (By.CSS_SELECTOR,"[dw-loading='public_ip_display_panel']")
    DISPLAY_PUBLIC_IP = (By.CSS_SELECTOR,"[ng-model='public_ip_display_status.status']")
    GEO_VPN_CLOUD = (By.CSS_SELECTOR,"[ng-change='onCloudTypeUpdate()']")
    GEO_CLOUD_STATUS = (By.CSS_SELECTOR,"[ng-change='changeGeoStatus']")
    GEO_VPN_ENABLE_PANEL = (By.CSS_SELECTOR,"[dw-loading='geo_vpn_form']")
    GEO_VPN_ACCOUNT_NAME = (By.ID,"account_name")
    GEO_VPN_DOMAIN_NAME = (By.ID, "domain_name")
    GEO_VPN_SERVICE_NAME = (By.ID, "vpn_service_name")
    GEO_VPN_ELB_DNS_NAME = (By.ID, "elb_dns_name")

    IMPORT_PANEL = (By.CSS_SELECTOR,"[dw-loading='import_panel']")
    CA_CERT = (By.ID,"ca_cert")
    SERVER_CERT = (By.ID,"server_cert")
    SERVER_PRIVATE_KEY = (By.ID, "server_private_key")
    CRL_DIST_URI = (By.ID,"crl_dist_uri")
    CRL_UPDATE_INTERVAL = (By.ID,"crl_update_interval")

    DOWNLOAD_PANEL = (By.CSS_SELECTOR,"[dw-loading='download_panel']")
    VPC_ID = (By.ID,"vpc_id")
    LB_NAME = (By.ID,"lb_name")
    DOWNLAOD_BUTTON = (By.CSS_SELECTOR,"[ng-click='downloadVPNConf()']" )

    PROFILE_TABLE_PANEL = (By.CSS_SELECTOR,"[dw-loading='profile_table']")
    PROFILE_TABLE_FOR_TABLE = "[dw-loading='profile_table'] table"
    NEW_PROFILE_BUTTON = (By.CSS_SELECTOR,"[ng-click='startCreation()']")
    NEW_PROFILE_PANEL = (By.CSS_SELECTOR,"[dw-loading='profile_form']")
    BASE_POLICY = (By.ID, "base_policy")
    NEW_PROFILE_OK_BUTTON = (By.CSS_SELECTOR,"[dw-loading='profile_form'] [type='submit']")
    NEW_PROFILE_CANCEL_BUTTON = (By.CSS_SELECTOR,"[ng-click='hideProfileForm()']")

    PROFILE_EDIT_BUTTON = ".fa-pencil-square-o"
    PROFILE_EDIT_PANEL = (By.CSS_SELECTOR,"[dw-loading='policy_table']")
    PROFILE_EDIT_SHOW_USERS_BUTTON = (By.CSS_SELECTOR,".ion-navicon-round")
    PROFILE_EDIT_SHOW_USER_DETAIL = (By.CSS_SELECTOR,"[ng-show='showDetail']")
    PROFILE_EDIT_ADD_NEW_BUTTON = (By.CSS_SELECTOR,"[ng-click='addRow()']")
    PROFILE_EDIT_SELECT_PROTOCOL = (By.CSS_SELECTOR,"[name='protocol']")
    PROFILE_EDIT_TARGET = (By.CSS_SELECTOR,"[name='target']")
    PROFILE_EDIT_TARGET_BUTTON = (By.CSS_SELECTOR,".fa-table")
    PROFILE_EDIT_PORT = (By.CSS_SELECTOR,"[name='port']")
    PROFILE_EDIT_SELECT_ACTION = (By.CSS_SELECTOR,"[name='action']")
    PROFILE_EDIT_UPDATE = (By.CSS_SELECTOR,"[ng-click='savePolicy()']")
    PROFILE_EDIT_POLICY_SAVE_BUTTON = ".editable-table-button[type='submit']"
    PROFILE_EDIT_POLICY_CANCEL_BUTTON = ".btn-default"
    PROFILE_EDIT_POLICY_INSERT_RULE = ".btn-primary"
    PROFILE_EDIT_POLICY_DELETE_BUTTON = ".btn-danger"
    PROFILE_TARGET_CIDR_PANEL = (By.CSS_SELECTOR,"[dw-loading='profile_modal']")
    PROFILE_TARGET_CLOUD_TYPE = (By.ID,"cloud_type")
    PROFILE_TARGET_ACCOUNT_NAME = (By.ID,"account_name")
    PROFILE_TARGET_REGION = (By.ID,"region")
    PROFILE_TARGET_VPC_ID = (By.ID,"vpc_id")
    PROFILE_TARGET_SUBNET = (By.ID,"subnet")
    PROFILE_TARGET_OK_BUTTON = (By.CSS_SELECTOR,"[dw-loading='profile_modal'] [type='submit']")
    PROFILE_TARGET_CANCEL_BUTTON = (By.CSS_SELECTOR,"[dw-loading='profile_modal'] [ng-click='$dismiss()']")
    PROFILE_POLICY_TABLE_for_TABLE = "[dw-loading='policy_table'] table"
    PROFILE_EDIT_CANCEL_BUTTON = (By.CSS_SELECTOR,"[ng-click='hidePolicyTable()']")

    PROFILE_ATTACH_USER_BUTTON = ".fa-plus-circle"
    PROFILE_DETACH_USER_BUTTON = ".fa-minus-circle"
    PROFILE_DELETE_BUTTON = "[confirm='Are you sure to delete this profile?']"
    PROFILE_ATTACH_USER_PANEL = (By.CSS_SELECTOR,"[dw-loading='attach_users_form']")
    PROFILE_DETACH_USER_PANEL = (By.CSS_SELECTOR,"[dw-loading='detach_users_form']")
    PROFILE_DETACH_USER_VPC_ID = (By.CSS_SELECTOR,"[ng-model='detachUsersFormData.vpc_id']")
    PROFILE_DETACH_USER_USER_NAME = (By.CSS_SELECTOR,"[ng-model='detachUsersFormData.username']")
    PROFILE_DETACH_OK_BUTTON = (By.CSS_SELECTOR,"[dw-loading='detach_users_form'] [type='submit']")

class DatacenterExtensionLocators:
    NAVIGATE_TO_DATACENTER_EXT = (By.CSS_SELECTOR,"[href='#/datacenter']")
    CREATE_PANEL = (By.CSS_SELECTOR,"[dw-loading='datacenter']")

    CLOUD_TYPE = (By.CSS_SELECTOR,"[ng-model='vpcFrm.cloud_type']")
    ACCOUNT_NAME = (By.CSS_SELECTOR,"[ng-model='vpcFrm.account_name']")
    GATEWAY_NAME = (By.CSS_SELECTOR,"[ng-model='vpcFrm.gateway_name']")
    REGION = (By.CSS_SELECTOR,"[ng-model='vpcFrm.vpc_reg']")
    CIDR = (By.CSS_SELECTOR,"[ng-model='vpcFrm.cidr']")
    GATEWAY_SIZE = (By.CSS_SELECTOR,"[ng-model='vpcFrm.vpc_size']")

    INTERNET_ACCESS_IS_SELECT = (By.XPATH,"//input[@type='checkbox']")
    INTERNET_ACCSES_CLICK = (By.XPATH,"//label/span")
    PUBLIC_SUBNET_IS_SELECT = (By.XPATH,"(//input[@type='checkbox'])[2]")
    PUBLIC_SUBNET_CLICK = (By.XPATH,"//div[2]/label/span")
    VPN_ACCESS_IS_SELECT = (By.XPATH, "(//input[@type='checkbox'])[3]")
    VPN_ACCESS_CLICK = (By.XPATH, "//div[5]/div/label/span")

    TWO_STEP_AUTH_SELECT = (By.CSS_SELECTOR,"[ng-model='vpcFrm.enable_otp']")
    MAX_CONNECTIONS = (By.CSS_SELECTOR,"[ng-model='vpcFrm.max_conn']")

    SPLIT_TUNNEL_MODE_YES_IS_SELECTED = (By.XPATH, "//div[6]/div[2]/label/input")
    SPLIT_TUNNEL_MODE_YES_CLICK = (By.XPATH, "//div[6]/div[2]/label/span")
    SPLIT_TUNNEL_MODE_NO_IS_SELECTED = (By.XPATH, "//label[2]/input")
    SPLIT_TUNNEL_MODE_NO_CLICK = (By.XPATH, "//label[2]/span")

    ADDITIONAL_CIDRS = (By.CSS_SELECTOR,"[ng-model='vpcFrm.additional_cidrs']")
    NAMESERVERS = (By.CSS_SELECTOR,"[ng-model='vpcFrm.nameservers']")
    SEARCH_DOMAINS = (By.CSS_SELECTOR,"[ng-model='vpcFrm.search_domains']")

    ENABLE_ELB_YES_IS_SELECTED = (By.XPATH, "//div[8]/div[2]/label/input")
    ENABLE_ELB_YES_CLICK = (By.XPATH, "//div[8]/div[2]/label/span")
    ENABLE_ELB_NO_IS_SELECTED = (By.XPATH, "//div[8]/div[2]/label[2]/input")
    ENABLE_ELB_NO_CLICK = (By.XPATH, "//div[8]/div[2]/label[2]/span")

    ENABLE_CLIENT_CERT_SHARING_YES_IS_SELECTED = (By.XPATH, "//div[9]/div[2]/label/input")
    ENABLE_CLIENT_CERT_SHARING_YES_CLICK = (By.XPATH, "//div[9]/div[2]/label/span")
    ENABLE_CLIENT_CERT_SHARING_NO_IS_SELECTED = (By.XPATH, "//div[9]/div[2]/label[2]/input")
    ENABLE_CLIENT_CERT_SHARING_NO_CLICK = (By.XPATH, "//div[9]/div[2]/label[2]/span")

    ENABLE_LDAP_IS_SELECTED = (By.XPATH, "(//input[@type='checkbox'])[5]")
    ENABLE_LDAP_CLICK = (By.XPATH, "//div[10]/div/label/span")

    LDAP_SERVER = (By.CSS_SELECTOR, "[ng-model='vpcFrm.ldap_server']")

    LDAP_USE_SSL_IS_SELECTED = (By.XPATH, "(//input[@type='checkbox'])[6]")
    LDAP_USE_SSL_CLICK = (By.XPATH, "//div[2]/div/label/span")
    CLIENT_CERTIFICATE = (By.CSS_SELECTOR,"[ng-model='vpcFrm.client_cert']")
    CA_CERTIFICATE = (By.CSS_SELECTOR,"[ng-model='vpcFrm.ca_cert']")

    BIND_DN = (By.CSS_SELECTOR, "[ng-model='vpcFrm.ldap_bind_dn']")
    LDAP_PASSWORD = (By.CSS_SELECTOR, "[ng-model='vpcFrm.ldap_password']")
    BASE_DN = (By.CSS_SELECTOR, "[ng-model='vpcFrm.ldap_base_dn']")
    USERNAME_ATTRIBUTE = (By.CSS_SELECTOR, "[ng-model='vpcFrm.ldap_username_attribute']")
    GROUP_MEMBERSHIP_DN = (By.CSS_SELECTOR, "[ng-model='vpcFrm.ldap_additional_ladp_req']")
    LDAP_USER = (By.CSS_SELECTOR, "[ng-model='vpcFrm.ldap_user']")

    TEST_LDAP_BUTTON = (By.CSS_SELECTOR, "[ng-click='testLDAP()']")

    SAVE_TEMPLATE_IS_SELECTED = (By.XPATH, "(//input[@type='checkbox'])[7]")
    SAVE_TEMPLATE_CLICK = (By.XPATH, "//div[7]/div/label/span")

"""
    For Settings - Upgrade, backup & Restore and License (Brian Liu)
"""

class SettingsLocators:
    #LICENSE = (By.LINK_TEXT, "License")

    # DASHBOARD_PAGE = (By.XPATH, "//*[contains(text(), 'Dashboard')]")

    NAVIGATE_TO_SETTINGS = (By.CSS_SELECTOR, "i.fa.fa-cog")

    X_BUTTON = (By.CSS_SELECTOR, "button.toast-close-button")

    PAGE_SPINNER = (By.CSS_SELECTOR, "div.dw-spinner")

    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.toast.toast-success")

    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.toast.toast-error")
    # UPGRADE-------------------------------------------------------

    NAVIGATE_TO_UPGRADE = (By.CSS_SELECTOR, "i.fa.fa-level-up")

    CHECK_UPGRADE_PAGE = (By.TAG_NAME, "h3")

    CUSTOM_VERSION = (By.XPATH, "//*[@id='release_version']")

    CURRENT_VERSION = (By.XPATH, "//*[contains(text(), 'UserConnect')]")

    UPGRADE_RELEASE_VERSION = (By.XPATH, "//button[1][@type='submit']")

    UPGRADE_LATEST = (By.XPATH, "//button[@type='button']")

    UPGRADE_ERROR = (By.XPATH, "//*[contains(text(), 'Error')]")

    SERVICE_UNAVAILABLE = (By.XPATH, "//*[contains(text(), 'Service Unavailable')]")

    # ---------------------------------------------------------------

    # BACKUP-------------------------------------------------

    NAVIGATE_TO_BACKUP_RESTORE = (By.CSS_SELECTOR, "i.fa.fa-database")

    VIEW_TITLE_BACKUP = (By.XPATH, "//*[contains(text(), 'Backup & Restore')]")

    BACKUP_CLOUD_TYPE = (By.XPATH, "//*[@id='cloud_type_1']")

    BACKUP_ACCOUNT_NAME = (By.XPATH, "//*[@id='account_name']")

    BACKUP_AWS_S3_BUCKET = (By.ID, "s3_bucket_name")

    BACKUP_AZUREARM_REGION = (By.ID, "region")

    BACKUP_AZUREARM_STORAGE_NAME = (By.ID, "storage_name")

    BACKUP_AZUREARM_CONTAINER_NAME = (By.ID, "container_name")

    BACKUP_ENABLE = (By.XPATH, "//button[1][@type='submit']")

    BACKUP_DISABLE = (By.CSS_SELECTOR, "button.btn.btn-danger")

    # -----------------------------------------------------------------

    # RESTORE----------------------------------------------------------

    RESTORE_CLOUD_TYPE = (By.ID, "cloud_type")

    AWS_ACCESS_KEY = (By.XPATH, "//*[@id='aws_access_key']")

    AWS_SECRET_KEY = (By.XPATH, "//*[@id='aws_secret_key']")

    AWS_BUCKET_NAME = (By.XPATH, "//*[@id='aws_bucket_name']")

    AWS_FILE_NAME = (By.XPATH, "//*[@id='file_name']")

    RESTORE_AZUREARM_SUBSCRIPTION_ID = (By.ID, "azure_subscription_id")

    RESTORE_AZUREARM_APPLICATION_ENDPOINT = (By.ID, "arm_application_endpoint")

    RESTORE_AZUREARM_APPLICATION_CLIENT_ID = (By.ID, "arm_application_client_id")

    RESTORE_AZUREARM_APPLICATION_CLIENT_SECRET = (By.ID, "arm_application_client_secret")

    RESTORE_AZUREARM_STORAGE_NAME = (By.ID, "azure_storage_name")

    RESTORE_AZUREARM_CONTAINER_NAME = (By.ID, "azure_container_name")

    RESTORE_AZUREARM_FILE_NAME = (By.ID, "file_name")

    RESTORE_BUTTON = (By.CSS_SELECTOR, "i.fa.fa-refresh")

    # LICENSE------------------------------------------------------------------

    VIEW_TITLE_LICENSE = (By.XPATH, "//*[contains(text(),'License')]")

    NAVIGATE_TO_LICENSE = (By.CSS_SELECTOR, "i.fa.fa-credit-card")

    SAVE_BUTTON = (By.CSS_SELECTOR, "i.fa.fa-save")

    REFRESH_BUTTON = (By.CSS_SELECTOR, "i.fa.fa-rotate-right")

    DEFAULT_CUSTOMER_ID = (By.ID, "customer_id")

    CUSTOMER_ID = (By.XPATH, "//*[@id='customer_id']")

    INFO_LICENSE_NUMBER = (By.XPATH, "//td[@class='ng-binding'][1]")

    INFO_LICENSE_TYPE = (By.XPATH, "//td[@class='ng-binding'][2]")

    INFO_LICENSE_EXPIRATION = (By.XPATH, "//td[@class='ng-binding'][3]")

    INFO_LICENSE_ALLOCATED = (By.XPATH, "//td[@class='ng-binding'][4]")

    INFO_LICENSE_ISSUED = (By.XPATH, "//td[@class='ng-binding'][5]")

    INFO_LICENSE_QUANTITY = (By.XPATH, "//td[@class='ng-binding'][6]")

"""
    For Troubleshooting (Rong Huang)
"""

class TroubleshootingPageLocator:
    # Navigating to troubleshooting page
    NAVIGATING_TO_TROUBLESHOOTING = (By.LINK_TEXT, "Troubleshoot")

    # pages/links under troubleshooting
    NAVIGATING_TO_LOGS = (By.LINK_TEXT, "Logs")
    NAVIGATING_TO_DIAGNOSTIC = (By.LINK_TEXT, "Diagnostics")
    NAVIGATING_TO_VNETDIAGNOSTIC = (By.LINK_TEXT, "VNet Diagnostics")
    NAVIGATING_TO_ELBDIAGNOSTIC = (By.LINK_TEXT, "ELB Status")
    NAVIGATE_TO_DBDIAGNOSTICS = (By.LINK_TEXT,"DB Diagnostics")

    # logs
    # upload tracelog section
    GATEWAY_SELECT = (By.XPATH, "//select")
    OK_BUTTON = (By.CSS_SELECTOR, "button.btn.btn-primary")
    IS_TRACELOG_SENT = (By.CSS_SELECTOR, "div.toast-message")
    CLOSE_TRACELOG_TOASTER = (By.CSS_SELECTOR, "button.toast-close-button.ng-scope")
    # ping utility section
    HOST_NAME = (By.XPATH, "//input[@placeholder='www.google.com']")
    PING_BUTTON = (By.XPATH, "//i[@class='ion-arrow-swap']")
    PING_RESULT_TEXTAREA = (By.XPATH, "//textarea[@class='pingresult_textarea ng-binding']")
    # command log section
    DISPLAY_BUTTON = (By.XPATH, "//i[@class='fa fa-list-alt']")
    COMMAND_LOG_RESULT_TEXTAREA = (By.XPATH, "//textarea[@class='commandlog_textarea ng-binding ng-scope']")

    # diagnostic page element
    # diagnostics section
    SELECT_GATEWAY = (By.XPATH, "//select[@ng-model='diagFrm.gw_name']")
    CONTROLLER_CHECKBOX_IS_SELECTED = (By.XPATH, "//input[@type='checkbox']")
    CONTROLLER_CHECKBOX_CLICK = (By.XPATH, "//label/span")
    RUN_BUTTON = (By.CSS_SELECTOR, "button.btn.btn-primary")
    IS_DIAGNOSTIC_RAN = (By.CSS_SELECTOR, "div.toast-message")
    SHOW_BUTTON = (By.CSS_SELECTOR, "[dw-loading='diag_panel'] [ng-click='showDiagFrm()']")
    SHOW_RESULTS_PANEL = (By.CSS_SELECTOR,"[ng-show='showResultsPanel']")
    SHOW_RESULT_TEXTAREA = (By.TAG_NAME, "textarea")
    CLOSE_RESULT_TEXTAREA_BUTTON = (By.CSS_SELECTOR, "[ng-show='showResultsPanel'] [ng-click='hideResultsPanel()']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "[dw-loading='diag_panel'] [ng-click='submitDiagFrm()']")
    IS_RESULT_SUBMIT = (By.CSS_SELECTOR, "div.toast-message")
    CLOSE_TOASTER_BUTTON = (By.CSS_SELECTOR, "button.toast-close-button.ng-scope")
    # vpn user diagnostic section
    VPN_USERNAME = (By.XPATH, "//input[@placeholder='Username']")
    VPN_DIAGNOSTIC_GO_BUTTON = (By.XPATH, "(//button[@type='submit'])[2]")
    SHOW_VPN_DIAGNOSTIC_TEXTAREA = (By.XPATH, "//textarea[@class='diagresult_textarea ng-binding ng-scope']")
    CLOSE_VPN_DIAGNOSTIC_TEXTAREA_BUTTON = (
        By.XPATH, "//button[@class='btn btn-danger ng-scope']")

    ENABLE_SECURITY = (By.CSS_SELECTOR,"[ng-model='secFrm.status'] span.on")
    DISABLE_SECURITY = (By.CSS_SELECTOR,"[ng-model='secFrm.status'] span.off")

    # database section
    POPUP_BOX_HEADER = (By.CSS_SELECTOR, "h3.modal-title.ng-binding")
    POPUP_BOX_MESSAGE = (By.CSS_SELECTOR, "//div[8]/div/div/div[2]")
    POPUP_BOX_CANCEL_BUTTON = (
        By.XPATH, "//button[@class='btn btn-default ng-binding']")
    POPUP_BOX_OK_BUTTON = (
        By.XPATH, "//button[@class='btn btn-primary ng-binding']")
    RESTART_SERVER_BUTTON = (
        By.CSS_SELECTOR, "[confirm='Are you sure to restart the server?']")
    SELECT_DATABASE_NAME = (By.XPATH, "//select[@id='db_name']")
    DROP_DATABASE_BUTTON = (
        By.CSS_SELECTOR, "[confirm='Are you sure to drop this database?']")
    SELECT_COLLECTION_NAME = (By.XPATH, "//select[@ng-model='dbdiagFrm.collection_name']")
    DUMP_COLLECTION_BUTTON = (By.CSS_SELECTOR, "[ng-click='dumpCollection()']")
    DUMP_COLLECTION_RESULT_TEXTAREA = (By.XPATH, "//textarea[@class='diagresult_textarea ng-binding ng-scope']")
    CLOSE_DUMP_COLLECTION_RESULT_TEXTAREA_BUTTON = (By.XPATH, "//button[@class='btn btn-danger ng-scope']")
    DELETE_COLLECTION_BUTTON = (
        By.CSS_SELECTOR, "[confirm='Are you sure to delete this collection?']")
    DOCUMENT = (By.XPATH, "//input[@placeholder='(Key:Value)']")
    DUMP_DOCUMENT_BUTTON = (By.CSS_SELECTOR, ".btn-mm[type='submit']")
    DUMP_DOCUMENT_RESULT_TEXTAREA = (By.XPATH, "//textarea[@class='diagresult_textarea ng-binding ng-scope']")
    CLOSE_DUMP_DOCUMENT_RESULT_TEXTAREA_BUTTON = (
        By.XPATH, "//button[@class='btn btn-danger ng-scope']")
    ERROR_MESSAGE_TOASTER = (By.CSS_SELECTOR, "div.toast-message")
    DELETE_DOCUMENT_BUTTON = (By.CSS_SELECTOR, "[ng-click='deleteDocument()']")

    # vnet diagnostic page element
    VNET_DIAGNOSTIC_PAGE_TITLE = (By.CSS_SELECTOR, "h1.al-title.ng-binding")
    SELECT_CLOUD_TYPE = (By.XPATH, "//select[@ng-model='routeDiagFrm.cloud_type']")
    SELECT_ACCOUNT_NAME = (By.XPATH, "//select[@ng-model='routeDiagFrm.account_name']")
    SELECT_TOOL = (By.XPATH, "//select[@ng-model='routeDiagFrm.tool']")
    VNET_DIAGNOSTIC_GO_BUTTON = (By.XPATH, "//button[@type='submit']")
    # extra fill in for all the different options
    ROUTE_TABLE_NAME = (By.XPATH, "//input[@placeholder='Route Table Name']")
    SELECT_ROUTE_TABLE_LOCATION = (By.XPATH, "//select[@ng-model='routeDiagFrm.vpc_reg']")
    VNET_NAME = (By.XPATH, "//input[@placeholder='VNet Name']")
    INSTANCE_ID = (By.XPATH, "//input[@placeholder='Instance ID']")
    ROUTE_NAME = (By.XPATH, "//input[@placeholder='Route Name']")
    CIDR = (By.XPATH, "//input[@placeholder='CIDR']")
    NEXT_HOP_IP = (By.XPATH, "//input[@placeholder='Next Hop IP']")
    SUBNET = (By.XPATH, "//input[@placeholder='Subnet']")
    # result of each test
    VNET_RESULT_TEXTAREA = (By.XPATH, "//textarea[@class='diagresult_textarea ng-binding ng-scope']")
    VNET_RESULT_TEXTAREA_CLOSE_BUTTON = (
        By.XPATH, "//button[@class='btn btn-danger ng-scope']")
    VNET_TOASTER = (By.CSS_SELECTOR, "div.toast-message")
    VNET_TOASTER_CLOSE = (By.CSS_SELECTOR, "button.toast-close-button.ng-scope")

    # elb diagnostic page element
    ELB_DIAGNOSTIC_PAGE_TITLE = (By.CSS_SELECTOR, "h1.al-title.ng-binding")
    SELECT_VPC_ID = (By.XPATH, "//select[@ng-model='vpcs.currentOption']")
    DELETE_ELB_BUTTON = (By.XPATH, "//button[@type='button']")
    LB_NAME = (By.CSS_SELECTOR, "td.ng-binding")
    DELETE_ELB_POP_UP_HEADING = (By.CSS_SELECTOR, "h3.modal-title.ng-binding")
    DELETE_ELB_POPUP_BOX_CANCEL_BUTTON = (
        By.XPATH, "//button[@class='btn btn-default ng-binding']")
    DELETE_ELB_POPUP_BOX_OK_BUTTON = (
        By.XPATH, "//button[@class='btn btn-primary ng-binding']")
    SUCCESS_MESSAGE_TOASTER = (By.CSS_SELECTOR, "div.toast-message")
    CLOSE_SUCCESS_TOASTER = (
        By.CSS_SELECTOR, "button.toast-close-button.ng-scope")

"""
    For Site2Cloud (Liming)
"""

class S2CViewLocators:
    NAVIGATE_TO_S2C = (By.CSS_SELECTOR, "i.ion-upload")

    VIEW_TITLE = (By.CSS_SELECTOR, "li.active")

    ADD_NEW = (By.XPATH, "//button[@type='button']")

    # VPC_ID = (By.XPATH, "//select[@ng-change='onAddFormVpcIDUpdate()']")
    VPC_ID = (By.ID, "vpc_id2")

    CONNECTION_TYPE = (By.ID, "conn_type")

    PRIMARY_GATEWAY = (By.ID, "gateway")

    BACKUP_GATEWAY = (By.ID, "gw_name2")

    CONNECTION_NAME = (By.ID, "conn_name")

    CUSTOMER_GATEWAY_IP_ADDRESS = (By.ID, "customer_ip_address")
    CUSTOMER_BACKUP_GATEWAY_IP = (By.ID,"peer_ip2")

    CUSTOMER_NETWORK_REAL = (By.ID, "customer_network")

    CUSTOMER_NETWORK_VIRTUAL = (By.ID, "customer_network_virtual")

    ENABLE_HA_IS_SELECTED = (By.XPATH,"//input[@type='checkbox']")
    ENABLE_HA_CLICK = (By.XPATH,"//label/span")

    PRIMARY_ROUTE_ENCRYPTION_CLICK = (By.ID, "private_route_encryption")
    PRIMARY_ROUTE_ENCRYPTION_IS_SELECTED = ()

    CLOUD_SUBNET_REAL = (By.ID, "cloud_subnet")

    CLOUD_SUBNET_VIRTUAL = (By.ID, "cloud_subnet_virtual")

    PRE_SHARED_KEY = (By.ID,"presk")
    PRE_SHARED_KEY_BKUP = (By.ID,"presk2")

    NULL_ENCRYPTION_CLICK = (By.XPATH, "//div[3]/label/span")
    NULL_ENCRYPTION_IS_SELECTED = (By.XPATH,"(//input[@type='checkbox'])[3]")

    #HA_SWITCH_STATUS = (By.CSS_SELECTOR, "span.checked")
    #HA_SWITCH_ENABLE = (By.CSS_SELECTOR, "span.off")
    #HA_SWITCH_DISABLE = (By.CSS_SELECTOR, "span.on")

    OK_BUTTON = (By.XPATH, "//button[@type='submit']")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "button.btn.btn-danger")

    S2C_TOASTER = (By.CSS_SELECTOR, "div.toast-message")
    S2C_TOASTER_CLOSER = (By.CSS_SELECTOR, "button.toast-close-button")

    DIAG_TAB = (By.XPATH, "(//a[contains(text(),'Diagnostics')])[3]")

    DIAG_VPC_ID = (By.XPATH, "//select[@ng-change='onDiagFormVpcIDUpdate()']")

    DIAG_CONNECTION = (By.XPATH, "//select[@ng-change='onDiagFormConnNameUpdate()']")

    DIAG_GATEWAY = (By.XPATH, "//select[@ng-model='diagFormData.gw_name']")

    DIAG_ACTION = (By.XPATH, "//select[@ng-model='diagFormData.subaction']")

    DIAG_OK_BTN = (By.XPATH, "(//button[@type='submit'])[5]")

    DIAG_OUTPUT = (By.XPATH, "//div[@class='panel-body']/pre")

    CONN_TABLE = (By.CSS_SELECTOR, "table.aws-accounts-table")

    CONFIG_VENDOR = (By.XPATH, "//select[@ng-model='editFrm.gw_vendor']")

    CONFIG_PLATFORM = (By.XPATH, "//select[@ng-model='editFrm.gw_platform']")

    CONFIG_SOFTWARE = (By.XPATH, "//select[@ng-model='editFrm.gw_software']")

    CONFIG_DWLD_BTN = (By.XPATH, "(//button[@type='submit'])[2]")

    CHANGE_CUSTOMER_NW = (By.XPATH, "//input[@ng-model='editFrm.customer_network']")

    CHANGE_CUSTOMER_NW_BTN = (By.XPATH, "(//button[@type='submit'])[3]")

    CHANGE_CLOUD_NW = (By.XPATH, "//input[@ng-model='editFrm.cloud_network']")

    CHANGE_CLOUD_NW_BTN = (By.XPATH, "(//button[@type='submit'])[4]")

    TUNNEL_TABLE = (By.CSS_SELECTOR, "table.table-striped")

    CONN_DETAILS_HAMBURGER = (By.CSS_SELECTOR, "i.ion-navicon-round.fake-link")

    CONN_DETAILS_INFO = (By.XPATH, "//pre[@ng-show='showDetail']")

    IMPORT_CONFIG_BTN = (By.XPATH, "(//button[@type='button'])[4]")

    IMPORT_CONFIG_FILE = (By.CSS_SELECTOR, "input[type=\"file\"]")