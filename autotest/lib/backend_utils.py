import logging, re, time, socket
import paramiko
from paramiko.ssh_exception import SSHException, AuthenticationException


class SSHCmd:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ssh_client = None

    def ssh_connect(self, hostname, user, passwd, kf=None):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if kf:
                self.ssh_client.connect(hostname, username=user, password=passwd,key_filename=kf)
            else:
                self.ssh_client.connect(hostname, username=user, password=passwd)
            #return ssh
        except AuthenticationException as e:
            self.logger.error("Couldn't SSH into %s due to AuthenticationException %s" % (hostname, str(e)))
            return None
        except SSHException as e:
            self.logger.error("Couldn't SSH into %s due to SSHException %s" % (hostname, str(e)))
            return None
        except socket.error as e:
            self.logger.error("SSH into %s socket error %s" % (hostname, str(e)))
            return None

    def send_command(self, scmd):
        self.logger.info("send the command "+scmd+ " to execute via SSH")
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(scmd+"\n")
            if stdout is not None:
                return stdout.readlines()
            else:
                self.logger.error("Error to execute the command")
                return stderr.readlines()

        except SSHException as e:
            self.logger.exception("Failed to execute the command: SSHException {}".format(e))
            return None

    def upload_file(self, local_file,remote_file):
        self.logger.info("Start to upload file to remote host")
        try:
            sftp = self.ssh_client.open_sftp()
            self.logger.info("Upload the local file {} to remote path {}".format(local_file,remote_file))
            sftp.put(local_file,remote_file)
            return True
        except SSHException:
            self.logger.exception("Could not establish sftp connection")

    def run_openvpn(self,config_file,auth_file):
        self.logger.info("Run openvpn on the client")
        try:
            openvpn_cmd1 = "sudo openvpn --mktun --dev tun0\n"
            openvpn_cmd2 = "sudo openvpn --config {} --auth-user-pass {} --log /var/log/openvpn.log --daemon &\n".format(config_file, auth_file)
            openvpn_cmd = openvpn_cmd1 + openvpn_cmd2

            self.send_command(openvpn_cmd)
            return True
        except SSHException:
            self.logger.exception("Could not establish sftp connection")

    def verify_by_log(self,log_path,message):
        self.logger.info("Verify the result by checking the log message")
        try:
            cmd = "sudo cat "+log_path
            logs = self.send_command(cmd)
            if [message in x for x in logs]:
                self.logger.info("Found {} in {}".format(message,log_path))
                return True
            else:
                self.logger.info("Failed to find the log")
                return False

        except SSHException:
            self.logger.exception("Could not establish sftp connection")

    def ping_private_ip_of_instance(self, private_ip, retry=10):
        ping_passed = 0

        for i in range(retry):
            if ping_passed:
                break
            else:
                stdin, stdout, stderr = self.ssh_client.exec_command("ping " + private_ip + " -c 10\n")
                data = stdout.readlines()

                for line in data:
                    self.logger.debug(line)
                    rate = re.search("(\d+)%", line)
                    if rate:
                        if int(rate.group(1)) < 20:
                            ping_passed = 1
            time.sleep(5)

        if ping_passed:
            self.logger.info("Pings to instance {} passed".format(private_ip))
            return True
        else:
            self.logger.error("Pings to instance {} failed".format(private_ip))
            return False

    def terminate_openvpn(self):
        self.logger.info("Ready to terminate openvpn client on the remote host")
        try:
            cmd = "sudo killall openvpn"
            self.send_command(cmd)
            time.sleep(3)
            check_cmd = "pgrep openvpn"
            result = self.send_command(check_cmd)
            if result == []:
                self.logger.info("All openvpn processes are terminated")
                return True
            return False

        except SSHException:
            self.logger.exception("Failed to execute the command via SSH")

    def ssh_disconnect(self):
        if self.ssh_client.get_transport().is_active():
            self.logger.info("Disconnect SSH Client")
            self.ssh_client.close()
