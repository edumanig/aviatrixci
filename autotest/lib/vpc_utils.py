__author__ = 'lmxiang'

import io
import socket
import sys

#import GUI.v1.login_page
import boto
import boto.ec2.elb
import boto.ec2.networkinterface
import paramiko
from boto import vpc
from paramiko.ssh_exception import SSHException, AuthenticationException

#import GUI.v1.dashboard
from autotest.lib.test_utils import *


# download the latest generated .ovpn file until success
def download_openvpn_config(driver, logger, userName, passwd, vpn_server=""):
    time.sleep(60)

    logger.info("Start to download the ovpn file")
    for i in range(0, 9):
        ovpn_file = download_email_attachment(logger, userName, passwd)
        if bool(ovpn_file):
            if vpn_server:
                if vpn_server in open(ovpn_file).read():
                    logger.info("Successfully download the ovpn file %s with VPN server as %s",
                                ovpn_file, vpn_server)
                    return ovpn_file
                else:
                    logger.error("The ovpn file %s downloaded doesn't have expected VPN server %s",
                                 ovpn_file, vpn_server)
                    return ""
            else:
                logger.info("Successfully download the latest ovpn file %s", ovpn_file)
                return ovpn_file
        else:
            time.sleep(60)

    logger.error("Fails to receive the correct ovpn file")
    return ""


# Scan downloaded OpenVPN client log file to verify the connection status if ssh_client if not provided
# If ssh_client is provided, scan remote OpenVPN log to verify the connection instead
def check_openvpn_log(logger, openvpn_log, ssh_client=""):
    logger.info("Check OpenVPN log %s to verify openvpn connection", openvpn_log)
    success = r'Initialization Sequence Completed'
    fail = "FAIL"
    if ssh_client:
        cmd1 = "sudo cat " + openvpn_log + " | grep " + "'" + success + "' \n"
        logger.info("Command used is %s", cmd1)
        ssh_result1 = execute_cmd_on_instance(logger, ssh_client, cmd1)

        for line in ssh_result1['ssh_stdout'].split('\n'):
            logger.info(line)
            if success in line:
                logger.info("OpenVPN tunnel is established properly")
                return True

        cmd2 = "sudo cat " + openvpn_log + " | grep " + "'" + fail + "' \n"
        ssh_result2 = execute_cmd_on_instance(logger, ssh_client, cmd2)

        for line in ssh_result2['ssh_stdout'].split('\n'):
            logger.info(line)
    else:
        local_path = os.path.dirname(os.path.abspath(__file__)) + "\\..\\archives\\temp"
        openvpn_local = local_path + "\\openvpn.log"
        with open(openvpn_local) as f:
            logs = f.readlines()
        for line in logs:
            if success in line:
                logger.info("OpenVPN tunnel is established properly")
                return True

    logger.error("OpenVPN tunnel is NOT established properly")
    return False


# Scan the ping result file for OpenVPN client test
def check_ping_log(logger, ping_log):
    transmitted = 0
    received = 0
    ping_pass_rate = 0.8

    with open(ping_log) as f:
        lines = f.readlines()
    for line in lines:
        stats = re.match(r'(.*) packets transmitted, (.*) received', line)
        if stats:
            transmitted += int(stats.group(1))
            received += int(stats.group(2))
    logger.debug("%d packets transmitted" % transmitted)
    logger.debug("%d packets received" % received)
    if transmitted != 0:
        success_rate = received/transmitted
        if success_rate >= ping_pass_rate:
            logger.info("ping test PASSED: success rate is %f" % success_rate)
            return True
        else:
            logger.error("ping test FAILED: success rate is %f" % success_rate)
            return False
    else:
        logger.info("No ping packet as transmitted. Failed")
        return False


# Connect to AWS VPC
def connect_aws_vpc(logger, region=""):
    from tests.main import variables as _variables
    from boto.exception import EC2ResponseError
    try:
        if not region:
            region = _variables['aws_region']
        conn = boto.vpc.connect_to_region(region,
                                          aws_access_key_id=_variables["aws_access_keyid"],
                                          aws_secret_access_key=_variables["aws_secret_key"],
                                          validate_certs=False)
    except EC2ResponseError as e:
        logger.error("VPC connection exception: " + str(e))

    return conn


# Search subnet ID from a VPC
def find_subnet_id(conn, vpc_name):
    subnet_list = conn.get_all_subnets(filters={'vpc_id': vpc_name})
    subnet_ids = [s.id for s in subnet_list]
    if subnet_ids:
        return subnet_ids[0]
    else:
        return None

# find the created user instance in a VPC
def find_user_instance_id(conn, vpc_id, ami_id):
    reservations = conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    for i in instances:
        if i.vpc_id == vpc_id and i.image_id == ami_id:
            return i.id
    return None


# find the ip address of user instance in a VPC
def find_user_instance_ip_by_vpc_id(conn, vpc_id):
    reservations = conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    for i in instances:
        if i.vpc_id == vpc_id:
            return i.private_ip_address
    return None


# find the ip address of user instance according to its ID
def find_user_instance_ip_by_instance_id(conn, instance_id):
    reservations = conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    for i in instances:
        if i.id == instance_id:
            return i.private_ip_address
    return None


# find the public ip address of user instance according to its ID
def find_user_instance_public_ip_by_instance_id(conn, instance_id):
    reservations = conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    for i in instances:
        if i.id == instance_id:
            return i.ip_address
    return None


# Check if port 22 for SSH is reachable
def test_ssh_port(ip_address):
    count = 0
    tries = 60
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while (count < tries):
        result = sock.connect_ex((ip_address, 22))
        if result == 0:
            sock.close()
            return True
        else:
            time.sleep(5)
            count += 1
    return False


# wait for the user instance entering specified 'state'
def wait_for_instance_to_be_ready(ec2_conn, logger, instance_id, state):
    # first find out instance reservation object
    rsv = ''
    for rsv in ec2_conn.get_all_instances(filters={'instance-id': instance_id}):
        break
    # loop until the instance reaches the state
    if rsv == '':
        logger.error('!instance_id %s not found', instance_id)
        return False
    r = rsv
    while r.instances[0].state != state:
        if r.instances[0].state == 'terminated' and state == 'running':
            logger.error('AWS terminated my instance %s', instance_id)
            return False
        time.sleep(5)
        for rsv in ec2_conn.get_all_instances(filters={'instance-id': instance_id}):
            if rsv.instances[0].id == instance_id:
                r = rsv
                break
    logger.info('instance is ready: %s, %s', r.instances[0].id, r.instances[0].state)
    return True


def get_one_subnet(vpc_conn, ec2_conn, vpc_id, private_subnet):
    for subnet in vpc_conn.get_all_subnets(filters={'vpc-id':vpc_id.strip()}):
        for tag in ec2_conn.get_all_tags(filters={'resource-id':subnet.id}):
            if private_subnet == 'yes':
                if 'private' in tag.value:
                    return subnet.id
            else:
                if 'public' in tag.value:
                    return subnet.id


def get_instance_name(ec2_conn, inst_id):
    inst_name = 'None'
    for tag in ec2_conn.get_all_tags(filters={'resource-id':inst_id}):
        if tag.name == 'Name':
            inst_name = tag.value
            return inst_name
    return inst_name


# Create a default security group for a VPC
def create_default_security_group(ec2_conn, logger, vpc_id):
    sec_name = 'user_profile_default_' + vpc_id

    sec_groups=ec2_conn.get_all_security_groups(filters={'group_name':sec_name})
    if not sec_groups:
        sec_group = ec2_conn.create_security_group(sec_name, sec_name, vpc_id)
        ec2_conn.authorize_security_group(group_id=sec_group.id, ip_protocol='tcp', from_port=22, to_port=22, cidr_ip='0.0.0.0/0')
        ec2_conn.authorize_security_group(group_id=sec_group.id, ip_protocol='tcp', from_port=443, to_port=443, cidr_ip='0.0.0.0/0')
        ec2_conn.authorize_security_group(group_id=sec_group.id, ip_protocol='icmp', from_port=-1, to_port=-1, cidr_ip='0.0.0.0/0')
        logger.debug("Create a new security group: " + sec_group.id)
    else:
        sec_group=sec_groups[0]
        logger.debug("Use existing security group: " + sec_group.id)

    return sec_group.id


# create an user instance
def create_user_instance(driver, logger, vpc_name, cloud_region, ami_id, key,
                         vpc_id="", vpc_subnet_id="", need_public_ip=False, write_result=False):
    from tests.main import variables as _variables
    vpc_conn = vpc.connect_to_region(cloud_region)
    ec2_conn = boto.ec2.connect_to_region(cloud_region)

    # create an user instance in the first subnet of every VPC
    # if vpc_id is not provided, it is cloudn-test VPC. otherwise, it is legacy VPC
    if not vpc_id:
        vpc_id = GUI.v1.dashboard.DashBoard(driver).find_vpc_id(vpc_name)

    logger.info("VPC ID for creating user instance is %s", vpc_id)

    # make sure the security group used allows ICMP traffic
    if vpc_id:
        sec_group_id = create_default_security_group(ec2_conn, logger, vpc_id)
        logger.info("Security group ID is %s", sec_group_id)
        if not vpc_subnet_id:
            vpc_subnet_id = get_one_subnet(vpc_conn, ec2_conn, vpc_id, "no")
        """
        if not vpc_subnet_id:
            vpc_subnet_id = get_one_subnet(vpc_conn, ec2_conn, vpc_id, "yes")
        """
        logger.info("VPC subnet ID is %s", vpc_subnet_id)

        if need_public_ip:
            logger.debug("Public IP address is required for creating this instance")
            interface = boto.ec2.networkinterface.NetworkInterfaceSpecification(subnet_id=vpc_subnet_id,
                                                                                groups=[sec_group_id],
                                                                                associate_public_ip_address=True)
            interfaces = boto.ec2.networkinterface.NetworkInterfaceCollection(interface)
            rsv = ec2_conn.run_instances(ami_id,
                                         key_name=key,
                                         instance_type=_variables["aws_instance_type"],
                                         network_interfaces=interfaces)
        else:
            rsv = ec2_conn.run_instances(ami_id,
                                         key_name=key,
                                         subnet_id=vpc_subnet_id,
                                         instance_type=_variables["aws_instance_type"],
                                         security_group_ids=[sec_group_id])

        instance = rsv.instances[0]
        wait_for_instance_to_be_ready(ec2_conn, logger, instance.id, "running")
        instance.add_tag("Name", vpc_name+"_inst")
        logger.info("Instance %s is created for VPC %s" % (instance.id, vpc_name))

        if write_result:
            result_writer(vpc_name, "Instance_Creation", "Passed")

        private_ip_addr = find_user_instance_ip_by_instance_id(vpc_conn, instance.id)

        if need_public_ip:
            public_ip_addr = find_user_instance_public_ip_by_instance_id(ec2_conn, instance.id)
            inst_info = {'instance_id': instance.id, 'sec_grp_id': sec_group_id,
                         'private_ip': private_ip_addr, 'region': cloud_region,
                         'public_ip': public_ip_addr}
        else:
            inst_info = {'instance_id': instance.id, 'sec_grp_id': sec_group_id, 'region': cloud_region,
                         'private_ip': private_ip_addr}
    else:
        logger.error("Instance for VPC %s can't be created", vpc_name)
        if write_result:
            result_writer(vpc_name, "Instance_Creation", "Failed")
        inst_info = {}

    return inst_info


# launch SSH client
# keyLoc is a string of the location of the key file
def launch_ssh_client(logger, target_ip, ssh_username, ssh_password):
    logger.info("*** Launch SSH Session to %s" % target_ip)

    logger.info("Wait for port 22 of %s to be reachable", target_ip)
    if test_ssh_port(target_ip):
        logger.debug("%s port 22 is reachable", target_ip)
    else:
        logger.error("%s port 22 is unreachable. Abort", target_ip)
        return None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(target_ip, username=ssh_username, password=ssh_password)
        return ssh
    except SSHException as e:
        logger.error("Couldn't SSH into %s due to SSHException %s" % (target_ip, str(e)))
        return None
    except AuthenticationException as e:
        logger.error("Couldn't SSH into %s due to AuthenticationException %s" % (target_ip, str(e)))
        return None
    except socket.error as e:
        logger.error("SSH into %s socket error %s" % (target_ip, str(e)))
        return None


# close SSH client
def close_ssh_client(logger, ssh_client):
    if ssh_client.get_transport().is_active():
        logger.info("SSH Client closed")
        ssh_client.close()


# modify ip routes of the user instance connected to local cloudn-test
def modify_ip_route(logger, action, net, mask, gw, dev):
    from tests.main import variables as _variables
    command = "echo %s | sudo -S route %s -net %s netmask %s gw %s dev %s" % (
        _variables["cloudn_instance_password"],
        action, net, mask, gw, dev)
    # ssh into the instance connected to local cloudn-test
    ssh = launch_ssh_client(logger,
                            _variables["cloudn_instance_ip"],
                            _variables["cloudn_instance_username"],
                            ssh_password=_variables["cloudn_instance_password"])

    logger.info("Route modification: " + command)
    # modify routing table with static route
    if not ssh:
        return False

    stdin, stdout, stderr = ssh.exec_command(command + "\n")
    data = stdout.readlines()
    for line in data:
        logger.debug(line)
    close_ssh_client(logger, ssh)
    return True


# Issue 'sudo ifconfig eth0 down' on primary gateway to deactivate it. This will trigger 'Status Checks'
# failure on EC2 instance. Pls make sure you disable clish on cloudn-test controller first
def deactivate_primary_gw(logger, vpc_name, gw_ip):
    from tests.main import variables as _variables
    command = 'sudo ssh -o "StrictHostKeyChecking no" -i ' + '/var/cloudx/' + \
              vpc_name + '.pem ubuntu@' + gw_ip + ' "sudo ifconfig eth0 down"'

    # ssh into cloudn-test controller
    ssh = launch_ssh_client(logger, _variables["cloudn_ip"], "admin", "password")
    if not ssh:
        return False

    logger.info("Issue 'sudo ifconfig eth0 down' ...")
    ssh.exec_command(command + "\n")
    return True


# Install OpenVPN client on EC2 instance
def install_openvpn_client(logger, ssh_client):
    command = "sudo apt-get -y install openvpn"

    logger.info("Install OpenVPN client ...")

    ssh_result = execute_cmd_on_instance(logger, ssh_client, command)
    for line in ssh_result['ssh_stdout'].split('\n'):
        logger.debug(line)
    return True


# Close OpenVPN client connection on EC2 instance
def close_openvpn_client_instance(logger, ssh_client):
    logger.info("Terminate OpenVPN connection")
    openvpn_cmd = "sudo killall openvpn"

    ssh_result = execute_cmd_on_instance(logger, ssh_client, openvpn_cmd)
    for line in ssh_result['ssh_stdout'].split('\n'):
        logger.debug(line)
    return True


# Upload file to EC2 instance
def sftp_upload_instance(logger, ssh_client, local_file, remote_file):
    logger.info("Upload local file %s to remote file %s", local_file, remote_file)
    ssh_client.put_file(local_file, remote_file)
    file_name = os.path.basename(remote_file)
    # Verify if the file is copied properly
    command = "ls -al | grep " + file_name
    ssh_result = execute_cmd_on_instance(logger, ssh_client, command)
    if file_name in ssh_result['ssh_stdout']:
        logger.info("%s is uploaded successfully", file_name)
        return True
    else:
        logger.error("%s is not uploaded successfully", file_name)
        return False


# Download file from EC2 instance
def sftp_download_instance(logger, ssh_client, local_file, remote_file):
    logger.info("Download remote file %s to local file %s", remote_file, local_file)
    ssh_client.get_file(remote_file, local_file)
    file_name = os.path.basename(remote_file)
    # Verify if the file is copied properly
    if os.path.exists(local_file):
        logger.info("%s is downloaded successfully", file_name)
        return True
    else:
        logger.error("%s is not downloaded successfully", file_name)
        return False


# Ping AWS User instance
def ping_aws_user_instance(logger, ssh_client, aws_instance_ip, vpc_info):
    ping_passed = 0

    for i in range(10):
        if ping_passed:
            break
        else:
            stdin, stdout, stderr = ssh_client.exec_command("ping " + aws_instance_ip + " -c 10\n")
            data = stdout.readlines()

            for line in data:
                logger.debug(line)
                rate = re.search("(\d+)%", line)
                if rate:
                    if int(rate.group(1)) < 20:
                        ping_passed = 1
        time.sleep(5)

    if ping_passed:
        logger.info("Pings to instance %s in VPC/VNet %s passed" % (aws_instance_ip, vpc_info))
        #result_writer(vpc_info, "Instance_Pings", "Passed")
        return True
    else:
        logger.error("Pings to instance %s in VPC/VNet %s failed" % (aws_instance_ip, vpc_info))
        #result_writer(vpc_info, "Instance_Pings", "Failed")
        return False


# Terminate OpenVPN client session
def close_openvpn_client(logger, ssh_client):
    from tests.main import variables as _variables
    pw = _variables["cloudn_instance_password"]
    logger.info("Terminate OpenVPN connection")
    openvpn_cmd = "echo %s | sudo -S killall openvpn\n" % pw
    ssh_client.exec_command(openvpn_cmd)


# Launch OpenVPN client from an EC2 instance
def launch_openvpn_instance(logger, ssh_client, config_file, auth_file):
    logger.info("Wait for OpenVPN server to come up before launching the client ...")
    time.sleep(120)

    openvpn_cmd1 = "sudo openvpn --mktun --dev tun0\n"
    openvpn_cmd2 = "sudo openvpn --config %s --auth-user-pass %s " \
                   "--log /var/log/openvpn.log --daemon &\n" % (config_file, auth_file)
    openvpn_cmd = openvpn_cmd1 + openvpn_cmd2
    logger.debug("openvpn client launch command: %s", openvpn_cmd)

    status, stdout, stderr = ssh_client.run(openvpn_cmd)
    logger.debug("Launch OpenVPN client status is " + str(status))

    output = stdout.decode('utf-8')

    for line in output.split('\n'):
        logger.debug(line)

    return True


# Ping from an EC2 instance and verify if the ping success rate is ok
def ping_from_instance(logger, ssh_client, target_ip):
    logger.info("Send pings to %s", target_ip)
    ping_cmds = "ping %s -c 10" % target_ip
    ssh_result = execute_cmd_on_instance(logger, ssh_client, ping_cmds)

    transmitted = 0
    received = 0
    ping_pass_rate = 0.8

    for line in ssh_result['ssh_stdout'].split('\n'):
        logger.info(line)
        stats = re.match(r'(.*) packets transmitted, (.*) received', line)
        if stats:
            transmitted = int(stats.group(1))
            received = int(stats.group(2))
    logger.debug("%d packets transmitted" % transmitted)
    logger.debug("%d packets received" % received)
    if transmitted != 0:
        success_rate = received/transmitted
        if success_rate >= ping_pass_rate:
            logger.info("ping test PASSED: success rate is %f" % success_rate)
            return True
        else:
            for line in ssh_result['ssh_stdout'].split('\n'):
                logger.debug(line)
            logger.error("ping test FAILED: success rate is %f" % success_rate)
            return False
    else:
        logger.info("No ping packet as transmitted. Failed")
        return False


# Launch OpenVPN client from the user instance connected to CloudN and ping
# the user instance in VPC
def openvpn_ping(driver, logger, openvpn_config, openvpn_auth, vpc_name, target_ip, vpc_id="",
                 openvpn_connect=True, openvpn_disconnect=True, retries=1):
    from tests.main import variables as _variables
    ping_times = 10

    # GUI.login_page.LoginPage(driver).login()

    # find the VPC ID associated with the VPC name, such as VPC31, from the dashboard
    if not vpc_id:
        vpc_id = GUI.v1.dashboard.DashBoard(driver).find_vpc_id(vpc_name)

    if vpc_id:
        # use boto to find out the AWS user instance's IP address
        # instance_ip = find_user_instance_ip_by_vpc_id(ec2_conn, vpc_id)

        # ssh into the instance connected to local cloudn-test
        ssh = launch_ssh_client(logger,
                                _variables["cloudn_instance_ip"],
                                _variables["cloudn_instance_username"],
                                _variables["cloudn_instance_password"]
                                )

        if not ssh:
            return False

        channel = ssh.invoke_shell()
        channel.settimeout(None)
        stdin = channel.makefile('wb')
        stdout = channel.makefile('rb', 10240)

        if openvpn_connect:
            # remove existing ping and openvpn log etc
            logger.debug("Remove existing pingtest and openvpn log etc")
            stdin.write('''
            echo password | sudo -S rm -f /var/log/openvpn.log\n
            echo password | sudo -S rm -f /var/log/pingtest.log\n
            '''
                        )

            # Touch to create new ping and openvpn log etc
            logger.debug("Touch pingtest and openvpn log etc")
            stdin.write('''
            echo password | sudo -S touch /var/log/openvpn.log\n
            echo password | sudo -S touch /var/log/pingtest.log\n
            '''
                        )

            logger.debug("Change permission of openvpn and pingtest log etc")
            stdin.write('''
            echo password | sudo -S chmod 777 /var/log/openvpn.log\n
            echo password | sudo -S chmod 777 /var/log/pingtest.log\n
            '''
                        )

            # Kill running openvpn process if any
            logger.debug("Kill running openvpn process if any")
            stdin.write('''
            echo password | sudo -S killall openvpn\n
            '''
                        )


        ping_cmds = "ping %s -c 1 | tee /var/log/pingtest.log\n" % target_ip
        for i in range(1, ping_times):
            ping_cmds += "ping %s -c 1 | tee -a /var/log/pingtest.log\n" % target_ip

        if openvpn_connect:
            # openvpn_cmd1 = "echo password | sudo -S openvpn --mktun --dev tun0\n"
            openvpn_cmd2 = "echo password | sudo -S openvpn --config %s --auth-user-pass %s " \
                           "--log /var/log/openvpn.log --daemon &\n" % (openvpn_config, openvpn_auth)

            logger.debug("Start to launch OpenVPN Client")
            # openvpn_cmds = openvpn_cmd1 + openvpn_cmd2

            # Launch OpenVPN client
            # stdin.write(openvpn_cmds)
            stdin.write(openvpn_cmd2)
            time.sleep(4)

        logger.info("Start the ping tests for %s time(s)", str(retries))
        while retries:
            # Start to ping the aws user instance for 10 times
            logger.info("Start to ping %s", target_ip)
            stdin.write(ping_cmds)

            while True:
                part = channel.recv(1024)
                data = part.decode("utf-8")
                if "ping statistics" in data:
                    ping_times -= 1
                if ping_times == 0:
                    logger.debug("Pings finished. Exit")
                    break
                sys.stdout.write(part.decode("utf-8"))
                sys.stdout.flush()

            retries -= 1
            ping_times = 10

        # Kill running openvpn process after pings
        logger.debug("Kill running openvpn process after pings")
        stdin.write('''
            echo password | sudo -S killall openvpn\n
        '''
                    )

        if openvpn_disconnect:
            logger.info("Start to close SSH client")
            close_ssh_client(logger, ssh)

        return True
    else:
        logger.error("VPC ID %s isn't found in Dashboard. Fails" % vpc_id)
        return False


# Download OpenVPN log file and ping test result file from the Linux
# instance connected to the cloudn-test
def sftp_download(logger, instance_ip="", keyLoc=""):
    from tests.main import variables as _variables
    if not instance_ip:
        instance_ip = _variables["cloudn_instance_ip"]

    try:
        transport = paramiko.Transport(instance_ip, 22)
        if not keyLoc:
            transport.connect(username=_variables["cloudn_instance_username"],
                              password=_variables["cloudn_instance_password"])
        else:
            keyLocation = open(keyLoc, 'r')
            key = keyLocation.read()
            keyfile = io.StringIO(key)
            mykey = paramiko.RSAKey.from_private_key(keyfile)
            transport.connect(username=_variables["cloudn_instance_username"],
                              pkey=mykey)

        sftp = paramiko.SFTPClient.from_transport(transport)
        openvpn_log = r'/var/log/openvpn.log'
        ping_log = r'/var/log/pingtest.log'
        local_path = os.path.dirname(os.path.abspath(__file__)) + "\\archives\\temp"
        openvpn_local = local_path + "\\openvpn.log"
        ping_local = local_path + "\\pingtest.log"
        logger.info("Downloading %s from %s to %s" % (openvpn_log, instance_ip, openvpn_local))
        sftp.get(openvpn_log, openvpn_local)
        logger.info("Downloading %s from %s to %s" % (ping_log, instance_ip, ping_local))
        sftp.get(ping_log, ping_local)
    except Exception as e:
        logger.exception("Fail to sftp download etc from %s with exception: %s" % (instance_ip, str(e)))
    finally:
        logger.info("Close sftp download connection to %s" % instance_ip)
        sftp.close()
        transport.close()


# Upload OpenVPN configuration file to the Linux instance connected to the cloudn-test
def sftp_upload(logger, file_name, instance_ip="", keyLoc=""):
    from tests.main import variables as _variables
    if not instance_ip:
        instance_ip = _variables["cloudn_instance_ip"]
    logger.info("sftp upload %s to %s" % (file_name, instance_ip))

    transport = paramiko.Transport(instance_ip, 22)
    try:
        if not keyLoc:
            transport.connect(username=_variables["cloudn_instance_username"],
                              password=_variables["cloudn_instance_password"])
        else:
            keyLocation = open(keyLoc, 'r')
            key = keyLocation.read()
            keyfile = io.StringIO(key)
            mykey = paramiko.RSAKey.from_private_key(keyfile)
            transport.connect(username=_variables["cloudn_instance_username"],
                              pkey=mykey)
    except SSHException as e:
        logger.exception("SFTP upload transport connection exception " + str(e))
        return False
    sftp = paramiko.SFTPClient.from_transport(transport)
    local_path = os.path.dirname(os.path.abspath(__file__)) + "\\attachments"
    openvpn_local = local_path + "\\" + file_name
    openvpn_remote_dir = r'/home/' + _variables["cloudn_instance_username"] + r'/'
    openvpn_remote_file = openvpn_remote_dir + file_name

    try:
        files = sftp.listdir(path=openvpn_remote_dir)
        if file_name in files:
            logger.debug("Deleting %s if already exists" % openvpn_remote_file)
            sftp.remove(openvpn_remote_file)
        logger.info("Uploading %s to %s at %s" % (openvpn_local, openvpn_remote_file, instance_ip))
        sftp.put(openvpn_local, openvpn_remote_file)
        return True
    except Exception as e:
        logger.exception("Fail to sftp upload etc to %s with exception: %s" % (instance_ip, str(e)))
        return False
    finally:
        logger.info("Close sftp upload connection to %s" % instance_ip)
        sftp.close()
        transport.close()


# launch cloudn-test VPN and ping an instance in cloudn-test VPC
def vpn_ping_cloudn_vpc(driver, logger, vpc_name, ssh_ip, ssh_username, ssh_pwd, instance_ip="", vpc_id=""):
    from tests.main import variables as _variables
    ec2_conn = boto.ec2.connect_to_region(_variables["aws_region"])

    # find the VPC ID associated with the VPC name, such as VPC31, from the dashboard
    if not vpc_id:
        vpc_id = GUI.v1.dashboard.DashBoard(driver).find_vpc_id(vpc_name)

    ping_result = False
    if vpc_id:
        # use boto to find out the AWS user instance's IP address
        if not instance_ip:
            instance_ip = find_user_instance_ip_by_vpc_id(ec2_conn, vpc_id)

        if instance_ip:
            # ssh into the instance connected to local cloudn-test
            ssh = launch_ssh_client(logger, ssh_ip, ssh_username, ssh_password=ssh_pwd)

            # ping AWS user instance
            if ssh:
                ping_result = ping_aws_user_instance(logger, ssh, instance_ip, vpc_name)
                # Shut down SSH client
                close_ssh_client(logger, ssh)
            else:
                logger.error("Failed to ssh into the instance connected to local cloudn-test")
        else:
            logger.error("Can't find an user instance in VPC %s", vpc_name)
    else:
        logger.error("VPC %s is not found in DashBoard", vpc_name)

    return ping_result


# launch vpn and ping an user instance in legacy VPC
def vpn_ping_legacy_vpc(logger, vpc_id, user_inst_id):
    from tests.main import variables as _variables
    ec2_conn = boto.ec2.connect_to_region(_variables["aws_region"])

    instance_ip = find_user_instance_ip_by_instance_id(ec2_conn, user_inst_id)
    logger.info("IP address of the user instance in VPC %s is %s" % (vpc_id, instance_ip))

    if instance_ip:
        # ssh into the instance connected to local cloudn-test
        ssh = launch_ssh_client(logger,
                                _variables["cloudn_instance_ip"],
                                _variables["cloudn_instance_username"],
                                ssh_password=_variables["cloudn_instance_password"])

        if not ssh:
            return None

        # ping AWS user instance
        ping_result = ping_aws_user_instance(logger, ssh, instance_ip, vpc_id)

        # Shut down SSH client
        close_ssh_client(logger, ssh)
    else:
        logger.error("Can't find an user instance in VPC %s", vpc_id)

    return ping_result


# delete an user instance
def delete_user_instance(driver, logger, vpc_name):
    from tests.main import variables as _variables
    vpc_conn = vpc.connect_to_region(_variables["aws_region"])
    ec2_conn = boto.ec2.connect_to_region(_variables["aws_region"])

    # Delete the user instance in VPC
    vpc_id = GUI.v1.dashboard.DashBoard(driver).find_vpc_id(vpc_name)
    if vpc_id:
        user_instance_id = find_user_instance_id(vpc_conn, vpc_id, _variables["aws_ami_id"])
        if user_instance_id:
            vpc_conn.terminate_instances(user_instance_id)
            wait_for_instance_to_be_ready(ec2_conn, logger, user_instance_id, "terminated")
            logger.debug("User instance %s is deleted for VPC %s" % (user_instance_id, vpc_name))
            result_writer(vpc_name, "Instance_Deletion", "Passed")
            time.sleep(30)
            return True
        else:
            return False
    else:
        logger.error("User instance in VPC %s can't be deleted", vpc_name)
        result_writer(vpc_name, "Instance_Deletion", "Failed")
        return False


def delete_user_instance_by_id(logger, cloud_region, user_instance_id):
    vpc_conn = vpc.connect_to_region(cloud_region)
    ec2_conn = boto.ec2.connect_to_region(cloud_region)

    # Delete the user instance in VPC
    vpc_conn.terminate_instances(user_instance_id)
    wait_for_instance_to_be_ready(ec2_conn, logger, user_instance_id, "terminated")
    logger.debug("User instance %s is deleted", user_instance_id)
    time.sleep(30)
    return True


def delete_security_group(logger, cloud_region, sec_grp_id):
    ec2_conn = boto.ec2.connect_to_region(cloud_region)
    while 1:
        try:
            ec2_conn.delete_security_group(group_id=sec_grp_id)
            logger.info("Delete security group " + sec_grp_id + "...done")
            break
        except boto.exception.EC2ResponseError:
            logger.info("Trying to delete security group " + sec_grp_id + "...please wait")
            time.sleep(5)


# create a legacy vpc with an user instance
def create_legacy_vpc(logger, vpc_name, cidr, public, private, region=""):
    from tests.main import variables as _variables
    if not region:
        region = _variables['aws_region']
    conn = connect_aws_vpc(logger, region)
    ec2_conn = boto.ec2.connect_to_region(region)

    # Create a VPC
    if not conn:
        logger.error("Failed to connect to AWS VPC. Abort")
        return None

    vpc = conn.create_vpc(cidr)
    if vpc.state != "available":
        time.sleep(3)

    vpc.add_tag("Name", vpc_name)
    logger.info("VPC %s is created", vpc.id)

    # Configure the VPC to support DNS resolution and hostname assignment
    conn.modify_vpc_attribute(vpc.id, enable_dns_support=True)
    conn.modify_vpc_attribute(vpc.id, enable_dns_hostnames=True)

    # Create an Internet gateway
    igw = conn.create_internet_gateway()
    logger.info("Internet gateway %s is created", igw.id)

    # Create a new VPC security group
    sg_id = create_default_security_group(conn, logger, vpc.id)
    logger.info("Security group %s is created", sg_id)

    # Create a VPN gateway
    vgw = conn.create_vpn_gateway('ipsec.1')
    vgw.attach(vpc.id)
    logger.info("Virtual private gateway %s is created", vgw.id)

    # Attach the Internet gateway to our VPC
    conn.attach_internet_gateway(igw.id, vpc.id)
    logger.info("Internet gateway %s is attached to VPC %s" % (igw.id, vpc.id))

    # Create two Route Tables for the two subnets to be created
    public_route_table = conn.create_route_table(vpc.id)
    private_route_table = conn.create_route_table(vpc.id)
    logger.info("Public routing table %s is created", public_route_table.id)
    logger.info("Private routing table %s is created", private_route_table.id)

    # Create two size /24 subnets
    public_subnet = conn.create_subnet(vpc.id, public)
    private_subnet = conn.create_subnet(vpc.id, private)
    logger.info("Public subnet %s is created", public_subnet.id)
    logger.info("Private subnet %s is created", private_subnet.id)
    public_subnet_tag = {'Name': 'public subnet'}
    private_subnet_tag = {'Name': 'private_subnet'}
    ec2_conn.create_tags([public_subnet.id], public_subnet_tag)
    ec2_conn.create_tags([private_subnet.id], private_subnet_tag)
    logger.info("Public subnet %s is tagged by 'public subnet'", public_subnet.id)
    logger.info("Private subnet %s is tagged by 'private subnet'", private_subnet.id)

    # Associate Route Tables with our subnets
    conn.associate_route_table(public_route_table.id, public_subnet.id)
    conn.associate_route_table(private_route_table.id, private_subnet.id)
    logger.info("Associate route tables with our subnets")

    # Create a default route pointing to IGW for public subnet
    conn.create_route(public_route_table.id, '0.0.0.0/0', igw.id)

    # Create a default route pointing to VGW for private subnet
    while 1:
        try:
            conn.create_route(private_route_table.id, '0.0.0.0/0', vgw.id)
            break
        except boto.exception.EC2ResponseError:
            logger.info("please wait until VGW is ready")
#            logger.exception(boto.exception.EC2ResponseError)
            time.sleep(10)

    logger.info("VPC %s with id %s is UP!" % (vpc_name, vpc.id))

    vpc_info = {'vpc_id': vpc.id, 'vgw_id': vgw.id, 'igw_id': igw.id, 'sec_group_id': sg_id,
                'public_subnet_id': public_subnet.id, 'private_subnet_id': private_subnet.id}

    return vpc_info


# delete a legacy VPC
def delete_legacy_vpc(logger, vpc_info, region=""):
    from tests.main import variables as _variables
    if not region:
        region = _variables["aws_region"]
    vpc_conn = vpc.connect_to_region(_variables["aws_region"])
    ec2_conn = boto.ec2.connect_to_region(_variables["aws_region"])

    # Delete the security group
    while 1:
        try:
            ec2_conn.delete_security_group(group_id=vpc_info['sec_group_id'])
            logger.info("Delete security group " + vpc_info['sec_group_id'] + "...done")
            break
        except boto.exception.EC2ResponseError:
            logger.info("Trying to delete security group " + vpc_info['sec_group_id'] + "...please wait")
            time.sleep(5)

    # Detach Virtual Private gateway in this VPC
    while 1:
        try:
            detach_vgw = vpc_conn.detach_vpn_gateway(vpc_info['vgw_id'], vpc_info['vpc_id'])
            logger.info("detach vpn gateway %s from VPC %s" % (vpc_info['vgw_id'], vpc_info['vpc_id']))
            if detach_vgw:
                break
            else:
                time.sleep(5)
        except boto.exception.EC2ResponseError:
            logger.debug("detach vpn gateway " + vpc_info['vgw_id'] + " fails")
            logger.exception(boto.exception.EC2ResponseError)
            return False
    time.sleep(300)

    # Detach Internet gateway in this VPC
    while 1:
        try:
            detach_igw = vpc_conn.detach_internet_gateway(vpc_info['igw_id'], vpc_info['vpc_id'])
            logger.info("detach internet gateway %s from VPC %s" % (vpc_info['igw_id'], vpc_info['vpc_id']))
            if detach_igw:
                break
            else:
                time.sleep(5)
        except boto.exception.EC2ResponseError:
            logger.debug("detach internet gateway " + vpc_info['igw_id'] + " fails")
            logger.exception(boto.exception.EC2ResponseError)
            return False
    time.sleep(300)

    # Delete Virtual Private gateway in VPC
    while 1:
        try:
            delete_vgw = vpc_conn.delete_vpn_gateway(vpc_info['vgw_id'])
            logger.info("Virtual private gateway %s is deleted", vpc_info['vgw_id'])
            if delete_vgw:
                break
            else:
                time.sleep(5)
        except boto.exception.EC2ResponseError:
            logger.debug("delete vpn gateway " + vpc_info['vgw_id'] + "fails")
            logger.exception(boto.exception.EC2ResponseError)
            return False

    # Delete Internet gateway in VPC
    while 1:
        try:
            delete_igw = vpc_conn.delete_internet_gateway(vpc_info['igw_id'])
            logger.info("Internet gateway %s is deleted", vpc_info['igw_id'])
            if delete_igw:
                break
            else:
                time.sleep(5)
        except boto.exception.EC2ResponseError:
            logger.debug("delete internet gateway " + vpc_info['igw_id'] + "fails")
            logger.exception(boto.exception.EC2ResponseError)
            return False

    # Delete subnets
    for subnet in vpc_conn.get_all_subnets(filters={'vpc-id': vpc_info['vpc_id']}):
        vpc_conn.delete_subnet(subnet.id)
        logger.info("Delete subnet %s for VPC %s" % (subnet.id, vpc_info['vpc_id']))

    # Delete attached routing tables
    for rtbl in vpc_conn.get_all_route_tables(filters={'vpc-id': vpc_info['vpc_id']}):
        if rtbl.associations == []:
            vpc_conn.delete_route_table(rtbl.id)
            logger.info("Delete route table %s for VPC %s" % (rtbl.id, vpc_info['vpc_id']))

    # Delete the VPC
    logger.info("Delete VPC " + vpc_info['vpc_id'])
    return vpc_conn.delete_vpc(vpc_info['vpc_id'])

"""
# create a legacy vpc with an user instance
def create_legacy_vpc(logger, vpc_name, instance_name=""):
    from tests.main import variables as _variables
    conn = connect_aws_vpc(logger)

    # Create a VPC
    vpc = conn.create_vpc('10.0.0.0/16')
    if vpc.state != "available":
        time.sleep(3)

    vpc.add_tag("Name", vpc_name)
    logger.info("VPC %s is created", vpc.id)

    # Configure the VPC to support DNS resolution and hostname assignment
    conn.modify_vpc_attribute(vpc.id, enable_dns_support=True)
    conn.modify_vpc_attribute(vpc.id, enable_dns_hostnames=True)

    # Create an Internet gateway
    igw = conn.create_internet_gateway()
    logger.info("Internet gateway %s is created", igw.id)

    # Create a new VPC security group
    sg_id = create_default_security_group(conn, logger, vpc.id)
    logger.info("Security group %s is created", sg_id)

    # Create a VPN gateway
    vgw = conn.create_vpn_gateway('ipsec.1')
    vgw.attach(vpc.id)
    logger.info("Virtual private gateway %s is created", vgw.id)

    # Attach the Internet gateway to our VPC
    conn.attach_internet_gateway(igw.id, vpc.id)
    logger.info("Internet gateway %s is attached to VPC %s" % (igw.id, vpc.id))

    # Create two Route Tables for the two subnets to be created
    public_route_table = conn.create_route_table(vpc.id)
    private_route_table = conn.create_route_table(vpc.id)
    logger.info("Public routing table %s is created", public_route_table.id)
    logger.info("Private routing table %s is created", private_route_table.id)

    # Create two size /24 subnets
    public_subnet = conn.create_subnet(vpc.id, '10.0.0.0/24')
    private_subnet = conn.create_subnet(vpc.id, '10.0.1.0/24')
    logger.info("Public subnet %s is created", public_subnet.id)
    logger.info("Private subnet %s is created", private_subnet.id)

    # Associate Route Tables with our subnets
    conn.associate_route_table(public_route_table.id, public_subnet.id)
    conn.associate_route_table(private_route_table.id, private_subnet.id)
    logger.info("Associate route tables with our subnets")

    # Create a default route pointing to IGW for public subnet
    conn.create_route(public_route_table.id, '0.0.0.0/0', igw.id)

    # Create a default route pointing to VGW for private subnet
    while 1:
        try:
            conn.create_route(private_route_table.id, '0.0.0.0/0', vgw.id)
            break
        except boto.exception.EC2ResponseError:
            logger.info("please wait until VGW is ready")
#            logger.exception(boto.exception.EC2ResponseError)
            time.sleep(10)

    logger.info("VPC %s with id %s is UP!" % (vpc_name, vpc.id))

    if instance_name:
        logger.info("Start to create the user instance inside of the VPC...")
        # Create an user instance
        reservation = conn.run_instances(_variables["aws_ami_id"],
                                         key_name="latest1",
                                         security_group_ids=[sg_id],
                                         instance_type=_variables["aws_instance_type"],
                                         subnet_id=private_subnet.id)

        instance = reservation.instances[0]

        # Wait for the instance to be running and have an public DNS name
        wait_for_instance_to_be_ready(conn, logger, instance.id, 'running')

        logger.info("User instance %s with private IP address %s is up" % (instance.id, instance.private_ip_address))

        instance.add_tag("Name", instance_name)

        vpc_info = {'vpc_id': vpc.id, 'instance_id': instance.id, 'vgw_id': vgw.id,
                    'igw_id': igw.id, 'sec_group_id': sg_id, 'instance_ip': instance.private_ip_address}
    else:
        logger.info("No need to create a user instance inside of the VPC")
        vpc_info = {'vpc_id': vpc.id, 'instance_id': '', 'vgw_id': vgw.id,
                    'igw_id': igw.id, 'sec_group_id': sg_id, 'instance_ip': ''}

    return vpc_info


# delete a legacy VPC
def delete_legacy_vpc(logger, vpc_info):
    from tests.main import variables as _variables
    vpc_conn = vpc.connect_to_region(_variables["aws_region"])
    ec2_conn = boto.ec2.connect_to_region(_variables["aws_region"])

    # Delete the user instance
    if vpc_info['instance_id']:
        logger.info("Start to delete the user instance inside of the VPC")
        vpc_conn.terminate_instances(vpc_info['instance_id'])
        wait_for_instance_to_be_ready(ec2_conn, logger, vpc_info['instance_id'], "terminated")
        logger.info("User instance %s is deleted for VPC %s" % (vpc_info['instance_id'],
                                                                vpc_info['vpc_id']))
    else:
        logger.info("No need to delete the user instance inside of the VPC")

    # Delete the security group
    while 1:
        try:
            ec2_conn.delete_security_group(group_id=vpc_info['sec_group_id'])
            logger.info("Delete security group " + vpc_info['sec_group_id'] + "...done")
            break
        except boto.exception.EC2ResponseError:
            logger.info("Trying to delete security group " + vpc_info['sec_group_id'] + "...please wait")
            time.sleep(5)

    # Detach Virtual Private gateway in this VPC
    while 1:
        try:
            detach_vgw = vpc_conn.detach_vpn_gateway(vpc_info['vgw_id'], vpc_info['vpc_id'])
            logger.info("detach vpn gateway %s from VPC %s" % (vpc_info['vgw_id'], vpc_info['vpc_id']))
            if detach_vgw:
                break
            else:
                time.sleep(5)
        except boto.exception.EC2ResponseError:
            logger.debug("detach vpn gateway " + vpc_info['vgw_id'] + " fails")
            logger.exception(boto.exception.EC2ResponseError)
            return False
    time.sleep(300)

    # Detach Internet gateway in this VPC
    while 1:
        try:
            detach_igw = vpc_conn.detach_internet_gateway(vpc_info['igw_id'], vpc_info['vpc_id'])
            logger.info("detach internet gateway %s from VPC %s" % (vpc_info['igw_id'], vpc_info['vpc_id']))
            if detach_igw:
                break
            else:
                time.sleep(5)
        except boto.exception.EC2ResponseError:
            logger.debug("detach internet gateway " + vpc_info['igw_id'] + " fails")
            logger.exception(boto.exception.EC2ResponseError)
            return False
    time.sleep(300)

    # Delete Virtual Private gateway in VPC
    while 1:
        try:
            delete_vgw = vpc_conn.delete_vpn_gateway(vpc_info['vgw_id'])
            logger.info("Virtual private gateway %s is deleted", vpc_info['vgw_id'])
            if delete_vgw:
                break
            else:
                time.sleep(5)
        except boto.exception.EC2ResponseError:
            logger.debug("delete vpn gateway " + vpc_info['vgw_id'] + "fails")
            logger.exception(boto.exception.EC2ResponseError)
            return False

    # Delete Internet gateway in VPC
    while 1:
        try:
            delete_igw = vpc_conn.delete_internet_gateway(vpc_info['igw_id'])
            logger.info("Internet gateway %s is deleted", vpc_info['igw_id'])
            if delete_igw:
                break
            else:
                time.sleep(5)
        except boto.exception.EC2ResponseError:
            logger.debug("delete internet gateway " + vpc_info['igw_id'] + "fails")
            logger.exception(boto.exception.EC2ResponseError)
            return False

    # Delete subnets
    for subnet in vpc_conn.get_all_subnets(filters={'vpc-id': vpc_info['vpc_id']}):
        vpc_conn.delete_subnet(subnet.id)
        logger.info("Delete subnet %s for VPC %s" % (subnet.id, vpc_info['vpc_id']))

    # Delete attached routing tables
    for rtbl in vpc_conn.get_all_route_tables(filters={'vpc-id': vpc_info['vpc_id']}):
        if rtbl.associations == []:
            vpc_conn.delete_route_table(rtbl.id)
            logger.info("Delete route table %s for VPC %s" % (rtbl.id, vpc_info['vpc_id']))

    # Delete the VPC
    logger.info("Delete VPC " + vpc_info['vpc_id'])
    return vpc_conn.delete_vpc(vpc_info['vpc_id'])
"""


def wait_for_vgw_attached(logger, vpc_info):
    vgw_attached = False
    count = 0
    vgw_id = vpc_info['vgw_id']
    vpc_id = vpc_info['vpc_id']

    from tests.main import variables as _variables
    conn = vpc.connect_to_region(_variables["aws_region"])

    while count < 50:
        count += 1
        for vgw in conn.get_all_vpn_gateways(filters={'attachment.vpc-id':vpc_id}):
            if vgw.id == vgw_id:
                vgw_attached = True
                logger.info("VGW %s is restored to attached state for VPC %s", vgw_id, vpc_id)
                break
        if vgw_attached == True:
            break
        else:
            logger.info("Continue to wait for VGW %s to restore to attached state ...", vgw_id)
            time.sleep(6)

    if vgw_attached == False:
        logger.error("VGW %s can't be restored to attached state for VPC %s", vgw_id, vpc_id)

    return vgw_attached


# make ssh connection to an EC2 instance
def ssh_from_instance(logger, cloud_region, instance_id, instance_ip, ssh_key, host_key, username):
    from boto.manage.cmdshell import sshclient_from_instance

    conn = boto.ec2.connect_to_region(cloud_region)
    reservations = conn.get_all_instances(instance_ids=[instance_id])

    instance = reservations[0].instances[0]

    if test_ssh_port(instance_ip):
        logger.debug("%s port 22 is reachable", instance_ip)
    else:
        logger.error("%s port 22 is unreachable. Abort", instance_ip)
        return None

    ssh_client = sshclient_from_instance(instance, ssh_key_file=ssh_key, host_key_file=host_key, user_name=username)

    return ssh_client


# execute command on an EC2 instance after ssh connection is established
def execute_cmd_on_instance(logger, ssh_client, cmd, debug = False):
    status, stdout, stderr = ssh_client.run(cmd)
    _stdout = stdout.decode('utf-8')
    _stderr = stderr.decode('utf-8')
    if debug:
        logger.debug("execute_cmd_on_instance stdout for command %s", cmd)
        logger.debug(_stdout)
        logger.debug("execute_cmd_on_instance stderr for command %s", cmd)
        logger.debug(_stderr)
    ssh_result = {'ssh_status': status, 'ssh_stdout': _stdout, 'ssh_stderr': _stderr}
    return ssh_result


# Modify OpenVPN config file for linux to accept pushed DNS server
def modify_openvpn_config(logger, config_file):
    import fileinput
    logger.info("Modify OpenVPN config file %s for Linux client to accept pushed DNS server", config_file)
    if not os.path.exists(config_file):
        logger.error("%s doesn't exist. abort")
        return False
    if not os.path.isfile(config_file):
        logger.error("%s is not a file. abort")
        return False
    for line in fileinput.input(config_file, inplace=1):
        print(line, end="")
        if fileinput.isfirstline():
            logger.debug("Three lines added to %s", config_file)
            print('script-security 2')
            print('up /etc/openvpn/update-resolv-conf')
            print('down /etc/openvpn/update-resolv-conf')
    return True


# Delete ELB
def delete_elb(logger, elb_name, region=""):
    from tests.main import variables as _variables
    if not region:
        region = _variables["aws_region"]

    conn = boto.ec2.elb.connect_to_region(region)
    # get ELB by filtering its name
    elb = conn.get_all_load_balancers(load_balancer_names=[elb_name])
    logger.info("Delete ELB %s", elb_name)
    elb[0].delete()