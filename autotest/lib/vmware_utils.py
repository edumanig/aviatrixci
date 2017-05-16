import os
import time
import subprocess
import datetime

from os import path
from tests.utils.tools.utils import *

# initiate logger
logger = create_logger(os.path.basename(__file__))

var_dicts = {}
PWD = path.dirname(path.realpath(__file__))
PWD += "\..\..\etc\\"

commands = parse_yaml(PWD + 'vmware_commands.yml')['vmware_vmrun_guest']

def _vm_exe_cli(exeCLI):
    from tests.main import variables as _variables

    proc = subprocess.Popen([commands['vmrun_prefix'],
                             commands['vmrun_par_sw'],
                             commands['vmrun_ws'],
                             commands['vmrun_par_account'],
                             _variables['vmware_guest_username'],
                             commands['vmrun_par_password'],
                             _variables['vmware_guest_pw'],
                             commands['api_run_script_in_guest'],
                             _variables['vmware_guest_location'],
                             "-activeWindow",
                             "/bin/bash",
                             exeCLI],
                            stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) = proc.communicate()
    return {'stdoutdata': stdoutdata, 'stderrdata': stderrdata}


def vm_power_on_guest():
    """
    Power on guest via workstation if needed
        - detect whether guest status is power on
        - if not, power on
    API: vmrun.exe -T ws start <path to .vmx file>
    """
    # detect whether guest status is power on
    from tests.main import variables as _variables

    proc = subprocess.Popen([commands['vmrun_prefix'], commands['vmrun_par_sw'], commands['vmrun_ws'],
                             commands['api_list_connection']], stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) = proc.communicate()

    flag = False
    tmpOutput = stdoutdata.splitlines()
    for subOutput in tmpOutput:
        if subOutput.decode(encoding='UTF-8') == _variables['vmware_guest_location']:
            flag = True
    if not flag:
        logger.info("Guest does not show up in list - \n" +
                    "Expected: " + _variables['vmware_guest_location'] + "; \n" +
                    "CLI Output: " + stdoutdata.decode(encoding='UTF-8'))
        # Power on guest
        proc = subprocess.Popen([commands['vmrun_prefix'], commands['vmrun_par_sw'], commands['vmrun_ws'],
                                 commands['api_ws_win_power_on_guest'], _variables['vmware_guest_location']],
                                stdout=subprocess.PIPE)
        (stdoutdata, stderrdata) = proc.communicate()

        logger.info("Power on guest, need to wait for 60 seconds to setup")
        time.sleep(60)

        tmpOutput = 'stdoutdata'.splitlines()
        for subOutput in tmpOutput:
            if not "Error" in subOutput.decode(encoding='UTF-8'):
                flag = True

    if flag:
        logger.info("Guest is powered on successfully")
    else:
        logger.error("Could not power on guest due to error messages below - \n" +
                     stdoutdata.decode("utf-8"))
    return flag


def vm_enable_shared_folder():
    """
    Enable and add shared folder function by two API commands
        - enableSharedFolders <path to .vmx file>
        - addSharedFolder <path to .vmx file> <share name> <path to folder on host>
    API:
        - vmrun -T ws enableSharedFolders <path to .vmx file>
        - vmrun.exe -T ws -gu bryce -gp 1234 addSharedFolder <path to .vmx file>
            <share name> <path to folder on host>
    Notes:
        If shared folder has not been created on host side, script will automatically create one
    """
    # 1.Enable shared folder function by API enableSharedFolders
    from tests.main import variables as _variables

    logger.info("Enable shared folder function by API enableSharedFolders")
    subprocess.Popen([commands['vmrun_prefix'], commands['vmrun_par_sw'], commands['vmrun_ws'],
                      commands['api_enable_shared_folder'], _variables['vmware_guest_location']],
                     stdout=subprocess.PIPE)

    # 2.Add shared folder name to create sharing function between host and guest by API addSharedFolder
    sharedFolderPath = _variables['vmware_host_shared_folder']
    lastBSIndex = sharedFolderPath.rfind('\\')
    sharedFolderName = sharedFolderPath[lastBSIndex + 1:]

    # 2.1.Check whether shared folder has been created on host; if not, create one according to environment.yml
    logger.info("Check whether shared folder has been created on host. If not, create one")
    if not os.path.exists(sharedFolderPath):
        logger.info(sharedFolderPath + " does not exist, create it now")
        os.makedirs(sharedFolderPath, exist_ok=True)

    # 2.2 Add shared folder name
    logger.info("Add shared folder name to VMware workstation")
    subprocess.Popen([commands['vmrun_prefix'], commands['vmrun_par_sw'], commands['vmrun_ws'],
                      commands['vmrun_par_account'], _variables['vmware_guest_username'],
                      commands['vmrun_par_password'], _variables['vmware_guest_pw'],
                      commands['api_add_shared_folder'], _variables['vmware_guest_location'],
                      sharedFolderName, _variables['vmware_host_shared_folder']], stdout=subprocess.PIPE)
    logger.info("Wait 5 seconds for vmware enabling/adding shared folder function")
    time.sleep(5)

    # For this test case, we enable shared folder function for testing environment, then verify
    return True


def vm_verify_shared_folder():
    """
    Verify whether shared function and folder exists in guest
    API: vmrun -T ws listDirectoryInGuest <path to .vmx file> <directory path on guest>
    """
    from tests.main import variables as _variables

    sharedFolderPath = _variables['vmware_guest_shared_folder']
    lastBSIndex = sharedFolderPath.rfind('/')
    sharedPath = sharedFolderPath[0:lastBSIndex + 1]
    sharedFolderName = sharedFolderPath[lastBSIndex + 1:]

    proc = subprocess.Popen([commands['vmrun_prefix'], commands['vmrun_par_sw'], commands['vmrun_ws'],
                             commands['vmrun_par_account'], _variables['vmware_guest_username'],
                             commands['vmrun_par_password'], _variables['vmware_guest_pw'],
                             commands['api_list_directory'], _variables['vmware_guest_location'],
                             sharedPath], stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) = proc.communicate()

    flag = False
    tmpOutput = stdoutdata.splitlines()
    for subOutput in tmpOutput:
        logger.info(subOutput.decode(encoding='UTF-8'))
        if subOutput.decode(encoding='UTF-8') == sharedFolderName:
            flag = True
    if flag:
        logger.info('Found shared folder at %s', sharedFolderName)
    else:
        logger.error('Could not find shared folder in vmrun cli output - \n' +
                    'Expected: ' + sharedFolderName + '; \n' +
                    'CLI Output: ' + stdoutdata.decode(encoding='UTF-8'))
    return flag


def vm_pre_check():
    """
        1) Verify whether OpenVPN folder and Record folder exists; if not, create them for testing
        Location:
            ./Shared Folder
        2) If OpenVPN folder exists, clean up latest_<guestID>_*_ping.rst and latest_<guestID>_*_openvpn.log etc
    """
    from tests.main import variables as _variables

    if not os.path.exists(_variables["vmware_host_shared_folder"]):
        logger.info(_variables["vmware_host_shared_folder"] + " does not exist, create it now\n")
        logger.info("After creating the shared folder by automation, user need to copy " +
                     "*.ovpn and open.auth to <shared folder> on host.")
        os.makedirs(_variables["vmware_host_shared_folder"], exist_ok=True)

    logger.info("Clean up latest _<guestID>_*_ping.rst and latest_<guestID>_*_openvpn.log\n")

    for file in os.listdir(_variables["vmware_host_shared_folder"]):
        if (file.endswith(".rst") and _variables["vmware_guest_username"] in file) \
                or (file.endswith(".log") and _variables["vmware_guest_username"] in file):
            logger.info("Remove existing pingresult and openvpn.log files")
            os.remove(os.path.join(_variables["vmware_host_shared_folder"], file))

    return True


def vm_openvpn_disconnect():
    """
    run 'killall -9 openvpn' to disconnect openvpn client connection
    """
    from tests.main import variables as _variables

    exeCLI = "echo %s | sudo -S killall -9 openvpn" % (_variables['vmware_guest_pw'])
    logger.info("CLI for executing kill all openvpn process -\n %s" % exeCLI)
    _vm_exe_cli(exeCLI)
    time.sleep(2)
    return True


def vm_host2guest_connection():
    """
    Verify whether the connection was established successfully between host and guest
    API: vmrun -T ws list
    """
    from tests.main import variables as _variables

    proc = subprocess.Popen([commands['vmrun_prefix'], commands['vmrun_par_sw'], commands['vmrun_ws'],
                             commands['api_list_connection']], stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) = proc.communicate()

    flag = False
    tmpOutput = stdoutdata.splitlines()
    for subOutput in tmpOutput:
        if subOutput.decode(encoding='UTF-8') == _variables['vmware_guest_location']:
            flag = True
    if flag:
        logger.info("Connection was established successfully between host and guest")
    else:
        logger.error("Failed to establish connection between host and guest")
    return flag


def vm_verify_openvpn_config():
    global var_dicts
    """
    Verify openvpn configuration etc - *.ovpn and openvpn.auth on guest
        - verify etc under /mnt/hgfs/<shared folder>/OpenVPN on guest
        - script will load those two etc automatically
    Notes:
        User must create/copy *.ovpn and openvpn.auth to shared folder/OpenVPN on host by manually.
        Since shared folder is sharing between host and guest, we verify etc on /mnt/hgfs/VMSharedFolder of guest
            -   openvpn.auth format:
                    <account>       <--- first line
                    <password>      <--- second line
    """
    # verify 2 etc under /mnt/hgfs/VMSharedFolder/ on guest
    from tests.main import variables as _variables

    checkFiles = [".ovpn", "openvpn.auth"]
    proc = subprocess.Popen([commands['vmrun_prefix'], commands['vmrun_par_sw'], commands['vmrun_ws'],
                             commands['vmrun_par_account'], _variables['vmware_guest_username'],
                             commands['vmrun_par_password'], _variables['vmware_guest_pw'],
                             commands['api_list_directory'], _variables['vmware_guest_location'],
                             _variables['vmware_guest_shared_folder']], stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) = proc.communicate()

    tmpOutput = stdoutdata.splitlines()

    for subCheckFile in checkFiles:
        for subOutput in tmpOutput:
            if subCheckFile in subOutput.decode(encoding='UTF-8'):
                logger.debug("vmrun cli - " + stdoutdata.decode(encoding='UTF-8') +
                             "; check file - " + subCheckFile)
    auth_found = False
    ovpn_found = False
    for file in os.listdir(_variables['vmware_host_shared_folder']):
        if file.endswith(".auth"):
            var_dicts['openVPNAUTH'] = file
            logger.info('openvpn.auth file is found')
            auth_found = True
        if file.endswith(".ovpn"):
            var_dicts['openVPNOVPN'] = file
            # modify_openvpn_config(logger, file)
            logger.info('.opvn file is found')
            ovpn_found = True

    if auth_found and ovpn_found:
        logger.info("Found all openvpn configurations in shared folder")
        return True
    else:
        logger.error("Could not find all openvpn configurations in shared folder/OpenVPN - \n" +
                     "Expected: *.ovpn and openvpn.auth; \n" +
                     "CLI Output: " + stdoutdata.decode(encoding='UTF-8'))
        return False


def vm_copy_file_host2guest(filePathHost):
    """
    Verify copyFileFromHostToGuest API command can be sent successfully
        - copy file from host to the shared directory at guest
        - verify whether the file exists at the shared directory at guest
    API: vmrun -T ws copyFileFromHostToGuest <path to .vmx file> <file path on host> <file path in guest>
    """
    from tests.main import variables as _variables

    lastBSIndex = filePathHost.rfind('\\')
    fileName = filePathHost[lastBSIndex + 1:]
    homeSpacePath = _variables['vmware_guest_shared_folder']
    filePathGuest = "%s/%s" % (homeSpacePath, fileName)
    logger.info("Location of copy file at host is %s", filePathHost)
    logger.info("Location of copy file at guest is - %s", filePathGuest)

    # Execute copyFileFromHostToGuest API
    proc = subprocess.Popen([commands['vmrun_prefix'], commands['vmrun_par_sw'], commands['vmrun_ws'],
                             commands['vmrun_par_account'], _variables['vmware_guest_username'],
                             commands['vmrun_par_password'], _variables['vmware_guest_pw'],
                             commands['api_copy_file_host2guest'], _variables['vmware_guest_location'],
                             filePathHost, filePathGuest], stdout=subprocess.PIPE)
    time.sleep(2)

    # Verify whether file exists at correct location
    proc = subprocess.Popen([commands['vmrun_prefix'], commands['vmrun_par_sw'], commands['vmrun_ws'],
                             commands['vmrun_par_account'], _variables['vmware_guest_username'],
                             commands['vmrun_par_password'], _variables['vmware_guest_pw'],
                             commands['api_list_directory'], _variables['vmware_guest_location'],
                             homeSpacePath], stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) = proc.communicate()

    flag = False
    tmpOutput = stdoutdata.splitlines()
    for subOutput in tmpOutput:
        if subOutput.decode(encoding='UTF-8') == fileName:
            logger.debug("vmrun cli - " + stdoutdata.decode(encoding='UTF-8'))
            flag = True
    if flag:
        logger.info('Found file %s in vmrun cli output', fileName)
    else:
        logger.error('Could not find file in vmrun cli output - \n' +
                    'Expected: ' + fileName + '; \n' +
                    'CLI Output: ' + stdoutdata.decode(encoding='UTF-8'))
    return flag


def vm_copy_file_guest2host(fileFolderHost):
    """
    Verify copyFileFromGuestToHost API command can be sent successfully
        - copy file from guest to host
            - execute API to copy file from guest to host
        - verify whether the file exists in host
    API: vmrun -T ws copyFileFromGuestToHost <path to .vmx file> <file path on host> <file path in guest>
    """
    global var_dicts
    from tests.main import variables as _variables

    logger.info("File will be copied from guest to host at %s", fileFolderHost)
    homeSpacePath = _variables['vmware_guest_shared_folder']

    for fileName in [var_dicts['openVPNLogFile'], var_dicts['pingGuestFile']]:
        if "openvpn.log" in os.path.basename(fileName):
            filePathHost = os.path.join(fileFolderHost, "openvpn.log")
        if "ping.rst" in os.path.basename(fileName):
            filePathHost = os.path.join(fileFolderHost, "ping.rst")
        logger.info("Copy %s from guest vm to host at %s" % (fileName, fileFolderHost))

        lastBSIndex = filePathHost.rfind('\\')

        # Verify whether the file exists at guest
        proc = subprocess.Popen([commands['vmrun_prefix'], commands['vmrun_par_sw'], commands['vmrun_ws'],
                                 commands['vmrun_par_account'], _variables['vmware_guest_username'],
                                 commands['vmrun_par_password'], _variables['vmware_guest_pw'],
                                 commands['api_list_directory'], _variables['vmware_guest_location'],
                                 homeSpacePath], stdout=subprocess.PIPE)
        (stdoutdata, stderrdata) = proc.communicate()

        flag = False
        tmpOutput = stdoutdata.splitlines()
        for subOutput in tmpOutput:
            if subOutput.decode(encoding='UTF-8') == os.path.basename(fileName):
                logger.debug("vmrun cli - " + stdoutdata.decode(encoding='UTF-8'))
                flag = True
        if flag:
            logger.info('Found file %s in vmrun cli output', fileName)
        else:
            logger.error('Could not find file in vmrun cli output - \n' +
                        'Expected: ' + fileName + '; \n' +
                        'CLI Output: ' + stdoutdata.decode(encoding='UTF-8'))
            return None

        # Execute copyFileFromGuestToHost API
        proc = subprocess.Popen([commands['vmrun_prefix'], commands['vmrun_par_sw'], commands['vmrun_ws'],
                                 commands['vmrun_par_account'], _variables['vmware_guest_username'],
                                 commands['vmrun_par_password'], _variables['vmware_guest_pw'],
                                 commands['api_copy_file_guest2host'], _variables['vmware_guest_location'],
                                 fileName, filePathHost], stdout=subprocess.PIPE)
        time.sleep(2)

        # Verify whether file is exists in Windows host
        if os.path.exists(filePathHost):
            logger.info('Found file %s in host', fileName)
        else:
            logger.error('Could not find file in host - \n' +
                        'Expected: ' + fileName + '; \n' +
                        'Host Output: ' + os.listdir(filePathHost[:lastBSIndex]))
            return None

    return filePathHost


def vm_create_openvpn_log():
    """
    Execute linux command on guest
        - Create openvpn.log file by executing linux command
            sudo /bin/touch /shared_directory/<guestID>_<timestamp>_openvpn.log
            -
    API: vmrun -T ws runScriptInGuest <path to .vmx file> -activeWindow -interactive
        <directory path on guest> <script text>
    """
    global var_dicts
    from tests.main import variables as _variables

    guestID = _variables['vmware_guest_username']

    timeStamp = '{:%Y%m%d%H%M}'.format(datetime.datetime.now())
    idTimeStamp = "%s_%s" % (guestID, timeStamp)
    var_dicts['idTimeStamp'] = idTimeStamp

    openVPNLog = "%s_openvpn.log" % idTimeStamp
    openVPNLogFile = "%s/%s" % (_variables['vmware_guest_shared_folder'], openVPNLog)
    var_dicts['openVPNLogFile'] = openVPNLogFile

    exeCLI = "echo %s | sudo -S touch %s" % (_variables['vmware_guest_pw'], openVPNLogFile)
    logger.info("CLI for creating a %s on guest  - \n %s" % (openVPNLogFile, exeCLI))

    # Creating a /shared_directory/<guestID>_<timestamp>_openvpn.log file
    _vm_exe_cli(exeCLI)
    time.sleep(1)

    # Verify whether the openvpn.log exists
    proc = subprocess.Popen([commands['vmrun_prefix'], commands['vmrun_par_sw'], commands['vmrun_ws'],
                             commands['vmrun_par_account'], _variables['vmware_guest_username'],
                             commands['vmrun_par_password'], _variables['vmware_guest_pw'],
                             commands['api_list_directory'], _variables['vmware_guest_location'],
                             _variables['vmware_guest_shared_folder']], stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) = proc.communicate()

    flag = False
    tmpOutput = stdoutdata.splitlines()
    for subOutput in tmpOutput:
        if subOutput.decode(encoding='UTF-8') == openVPNLog:
            logger.debug("vmrun cli - " + stdoutdata.decode(encoding='UTF-8'))
            flag = True
    if flag:
        logger.info('After executing linux cmd, ' +
                    'openvpn.log with timestamp already exists at %s', _variables['vmware_guest_shared_folder'])
        return openVPNLogFile
    else:
        logger.error('After executing linux cmd, ' +
                "openvpn.log with timstamp doesn't exist at %s -  \n", _variables['vmware_guest_shared_folder'] +
                "\n" +
                "CLI Output: " + stdoutdata.decode(encoding='UTF-8'))
        return None


def vm_exe_openvpn_prog():
    """
    Execute openvpn client on guest
    API: vmrun -T ws runScriptInGuest <path to .vmx file> -activeWindow -interactive
        <directory path on guest> <script text>
    """
    global var_dicts
    from tests.main import variables as _variables

    # Execute openvpn program
    openVPNOVPNPath = "%s/%s" % (_variables['vmware_guest_shared_folder'], var_dicts['openVPNOVPN'])
    openVPNAUTHPath = "%s/%s" % (_variables['vmware_guest_shared_folder'], var_dicts['openVPNAUTH'])

    exeCLI = "echo %s | sudo -S openvpn --mktun --dev tun0" % (_variables['vmware_guest_pw'])
    _vm_exe_cli(exeCLI)
    time.sleep(2)

    exeCLI = "echo %s | sudo -S openvpn " \
             "--config %s --auth-user-pass %s " \
             "--log %s --daemon &" % (_variables['vmware_guest_pw'], openVPNOVPNPath,
                                      openVPNAUTHPath, var_dicts['openVPNLogFile'])
    logger.info("CLI for executing openvpn program with argseters -\n %s" % exeCLI)
    outputs = _vm_exe_cli(exeCLI)
    time.sleep(5)

    # Execute ls linux command to make sure previous command work properly
    exeCLI = "/bin/ls"
    outputs = _vm_exe_cli(exeCLI)

    # Verify whether the openvpn works properly by checking PID
    # Store output of ps cli into buffer.txt in shared folder
    bufGuestPath = "%s/%s" %(_variables['vmware_guest_shared_folder'], 'buffer.txt')
    exeCLI = "/bin/ps -C openvpn -o pid= > %s" % (bufGuestPath)
    outputs = _vm_exe_cli(exeCLI)
    time.sleep(1)

    flag = False
    bufHostPath = "%s\\%s" % (_variables['vmware_host_shared_folder'], 'buffer.txt')
    bufSize = os.stat(bufHostPath)
    if bufSize.st_size:
        flag = True
        logger.info("After executing openvpn cmd, it created a PID in ps cli as expected")
    else:
        logger.error("After executing openvpn cmd, it didn't create a PID in ps cli" )

    return flag


def vm_verify_ping_conn(target_ip):
    """
    Execute ping function on guest to verify connectivity between client and gateway via VPN
    API: vmrun -T ws runScriptInGuest <path to .vmx file> -activeWindow -interactive
        <directory path on guest> <script text>
    """
    global var_dicts
    from tests.main import variables as _variables

    # Ping first to make sure connectivity between gateway and client
    exeCLI = "/bin/ping -c 5 %s" % target_ip
    logger.info("First time ping to verify connection -\n %s" % exeCLI)
    _vm_exe_cli(exeCLI)
    time.sleep(7)

    # Execute real ping test and store ping result

    pingResultFile = "%s_ping.rst" % var_dicts['idTimeStamp']
    pingGuestFile = "%s/%s" % (_variables['vmware_guest_shared_folder'], pingResultFile)
    var_dicts['pingGuestFile'] = pingGuestFile

    exeCLI = "/bin/ping -c 10 %s > %s" % (target_ip, pingGuestFile)
    logger.info("CLI for ping function -\n %s" % exeCLI)
    _vm_exe_cli(exeCLI)
    time.sleep(15)

    # Verify ping log exists
    logger.info("Verify that ping log file exists");
    pingRSTHostPath = "%s\\%s" % (_variables['vmware_host_shared_folder'], pingResultFile)
    if os.path.isfile(pingRSTHostPath):
        logger.info('Ping log file is created successfully')
        return pingRSTHostPath
    else:
        logger.error('Fail to create ping log file')
        return None


def vm_openvpn_test(AUTHFileHost, OVPNFileHost, filePathHost, target_ip, first_run=False):
    """
    Launch openvpn client connection on vmware guest vm;
    Ping target IP;
    Check ping success rate
    """
    global var_dicts

    if first_run:
        logger.info('Run openvpn client test on guest VM for the first time.')
        if not vm_power_on_guest():
            logger.error('Fail to power on guest VM. Abort...')
            return False

        if not vm_host2guest_connection():
            logger.error('Fail to establish connection with guest VM. Abort...')
            return False

        vm_enable_shared_folder()

        logger.info('Finish enabling shared folder')

        if not vm_verify_shared_folder():
            logger.error('Fail to verify shared folder. Abort...')
            return False

        logger.info('Finish verifying shared folder')

    if not vm_copy_file_host2guest(AUTHFileHost):
        logger.error('Fail to copy %s from host to guest', AUTHFileHost)
        return False

    if not vm_copy_file_host2guest(OVPNFileHost):
        logger.error('Fail to copy %s from host to guest', OVPNFileHost)
        return False

    if not vm_verify_openvpn_config():
        logger.error("OpenVPN config files don't exist")
        return False

    if not vm_pre_check():
        logger.error('Guest VM pre-test check fails')
        return False

    openVPNResult = vm_create_openvpn_log()
    if not openVPNResult:
        logger.error('Fail to create OpenVPN log file')
        return False

    if not vm_openvpn_disconnect():
        logger.error('Fail to disconnect current OpenVPN connection')
        return False

    if not vm_exe_openvpn_prog():
        logger.error('Fail to execute OpenVPN program')
        return False

    pingResult = vm_verify_ping_conn(target_ip)
    if not pingResult:
        logger.error('Fail to run ping tests')
        return False

    if not vm_openvpn_disconnect():
        logger.error('Fail to disconnect current OpenVPN connection')
        return False

    logger.info('print the contents of var_dicts')
    for keys, values in var_dicts.items():
        logger.info('%s: %s' % (keys, values))

    if not vm_copy_file_guest2host(filePathHost):
        logger.error('Fail to copy files from guest to folder %s at host', filePathHost)
        return False

    logger.info('OpenVPN client tests at host finished')
    return (openVPNResult, pingResult)
