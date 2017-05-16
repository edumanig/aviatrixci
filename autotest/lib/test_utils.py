from __future__ import print_function

import argparse
import email
import email.mime.application
import imaplib
import json, paramiko
import os
import sys
import re
import shutil
import smtplib
import subprocess
import time
import zipfile
import logging
import autotest.lib.exceptions
import glob

from tabulate import tabulate
from datetime import datetime
from io import StringIO
from selenium.webdriver.remote.remote_connection import LOGGER

def avx_logger():
    LOGGER.setLevel(logging.WARNING)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler which also logs debug messages
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(ch)
    return logger

def run_os_cmd(command, trim=True):
    """
    runs a command via the shell and returns the exit code and the
    output result fro the given cmd. raise exception RunOsCommandsErr
    on non exit status and log the errors. return result of exec on success
    """
    logger = logging.getLogger('cloudx')
    cmd = r'cmd.exe /k ' + command
    logger.info('command executed %s', cmd)
    output_file = "archives\\temp\\cmd_output_file"
    error_file = "archives\\temp\\cmd_error_file"

    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    if not os.path.exists(os.path.dirname(error_file)):
        os.makedirs(os.path.dirname(error_file))

    output_file_abs = os.path.abspath(output_file)
    error_file_abs = os.path.abspath(error_file)

    with open(output_file_abs, "w+") as outfile:
        with open(error_file_abs, "w+") as errorfile:
            p = subprocess.Popen(cmd,
                                 stdin=subprocess.PIPE,
                                 stdout=outfile,
                                 stderr=errorfile,
                                 bufsize=-1)
            result, error = p.communicate()
            returncode = p.returncode

    if returncode == 0:
        if os.path.getsize(error_file_abs) > 0 and 'ERROR' in open(error_file_abs).read():
            f1 = open(error_file_abs, "r+")
            lines = f1.readlines()
            logger.error("Command execution succeeded, but gcloud returns the following errors")
            logger.error(lines)
            return None
        else:
            if trim:
                f = open(output_file_abs, "r+")
                # Trim the empty line and command prompt at the end of the output file
                lines = f.readlines()
                f.seek(0)
                for line in lines:
                    if line.strip() == "":
                        break
                    else:
                        f.write(line)
                f.truncate()
                f.close()
            return output_file_abs
    elif returncode == 1:
        reason = 'Command execution NOT succeeded. Exit code:1. '
    else:
        reason = 'Command error occured. Exit code:{}.'.format(returncode)
        error_msg = 'Command:"{}" FAILed.'.format(cmd)
        err = '{} Reason:{} Error: {} Return:{}'.format(error_msg, reason, error, result)
    raise autotest.lib.exceptions.RunOsCommandsErr(err)

def get_test_data(modname):
    if modname:
        data_dir = 'testdata\\'
        fn_dir = "\\".join(modname.split('.'))
        fn = os.path.abspath(data_dir + fn_dir + ".json")
        try:
            with open(fn) as testdata:
                return json.load(testdata)
        except (IOError,FileNotFoundError):
            print('Failed to open', fn)
            exit()
    else:
        print("Data file name is empty. Abort")
        exit()

class testcases():
    case_data ={}
    expected_result = {}

    def __init__(self,modname):
        self.modname = modname
        self.data = get_test_data(modname)
        self.logger = logging.getLogger(__name__)

    def start_test(self,casenum):
        self.case = self.data[casenum]
        self.logger.info("========================= Start of {}.{} =========================".format(self.modname,casenum))
        self.logger.info(self.case['description'])
        self.logger.info("-----------------------------------------------------------------------------------------------------------------")
        self.case_data = self.case['case_data']
        self.expected_result = self.case['expected_result']

    def end_test(self,casenum):
        self.input = {}
        self.expected_result = {}
        if "test_case" in casenum.lower():
            self.logger.info("Pass")
        else:
            self.logger.info("All set")
        self.logger.info("========================= End of {}.{} ===========================".format(self.modname,casenum))



'''
#gmail API get credential
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Gmail API Python Quickstart'

    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
'''

'''
def ListMessagesMatchingQuery(service, user_id, query=''):
  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError as error:
    print('An error occurred: %s' % error)
'''

'''
def GetAttachments(service, user_id, msg_id, file_type="ovpn", prefix=""):
    """Get and store attachment from Message with given id.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
    prefix: prefix which is added to the attachment filename on saving
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        for part in message['payload']['parts']:
            if file_type in part['filename']:
                if 'data' in part['body']:
                    data=part['body']['data']
                else:
                    att_id=part['body']['attachmentId']
                    att=service.users().messages().attachments().get(userId=user_id, messageId=msg_id,id=att_id).execute()
                    data=att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                path = prefix+part['filename']
                filePath = os.path.dirname(os.path.abspath(__file__)) + "\\attachments\\" + path
                with open(filePath, 'wb') as f:
                    f.write(file_data)
        print('Download successfully!')
        return filePath
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
'''

'''
def download_email_attachment(logger, email_subject):
    user_id = 'me'

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    msg_ids = ListMessagesMatchingQuery(service, user_id, query=email_subject)
    for msg_id in msg_ids:
        logger.info('msg_id: ', msg_id)

    if msg_ids:
        attachment = GetAttachments(service, user_id, msg_ids[0]['id'])
        return attachment
'''

def _result_creator(file_name, result, time_start, time_stop):
    output = StringIO()
    print("", file=output)
    print("", file=output)
    #print("Archive File: " + file_name, file=output)
    #print("")
    print("Test Start Time: " + time_start, file=output)
    print("")
    print("---- START OF TEST RESULTS ----", file=output)
    print(result, file=output)
    print("", file=output)
    print("result::errors", file=output)
    for error in result.errors:
        print(error, file=output)
        print("", file=output)
    print("", file=output)
    print("result::failures", file=output)
    for failure in result.failures:
        print(failure, file=output)
        print("", file=output)
    print("", file=output)
    print("result::skipped", file=output)
    for skip in result.skipped:
        print(skip, file=output)
        print("", file=output)
    print("", file=output)
    print("result::successful", file=output)
    print(result.wasSuccessful(), file=output)
    print("", file=output)
    print("result::test-run", file=output)
    print(result.testsRun, file=output)
    print("---- END OF TEST RESULTS ----", file=output)
    print("")
    print("Test Stop Time: " + time_stop, file=output)
    print("", file=output)
    contents = output.getvalue()
    output.close()
    return contents

def directory_clearer(path):
    if os.listdir(path) != []:
        shutil.rmtree(path, ignore_errors=True)
    if not os.path.exists(path):
        os.mkdir(path)

def find_files_in_directory(path, file_pattern):
    cur_dir = os.getcwd()
    os.chdir(path)
    files = glob.glob(file_pattern)
    os.chdir(cur_dir)
    return files

def delete_files_in_directory(path):
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def zip_creator(zip_file_name, report_dir):
    with zipfile.ZipFile(zip_file_name, "w") as myzip:
        for root, dirs, files in os.walk(report_dir):
            for file in files:
                myfile = os.path.join(root, file)
                if os.path.isfile(myfile):
                    myzip.write(myfile, os.path.basename(myfile))


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-cf', action="store",
                        dest="config",
                        #type=argparse.FileType('r'),
                        help='Specify variable config file')
    parser.add_argument('-ct', action="store",
                        dest="cloud_type",
                        help='Specify cloud type under test')
    parser.add_argument('-uid', action="store",
                        dest="userID",
                        help='Specify user ID for archive and email')
    parser.add_argument('-logging', action="store",
                        dest="logging",
                        default="ERROR",
                        help='Specify the logging level with options')
    return parser.parse_args()


def config_parser(file_name, variables):
    with open(file_name, 'r') as fh:
        data = fh.readlines()
        for line in data:
            key, value = line.split("=")
            variables[key.strip()] = value.strip()


def report_writer(file_name, result, time_start, time_stop):
    contents = _result_creator(file_name, result, time_start, time_stop)

    with open(file_name, 'a') as fh:
        print(contents, file=fh)
        fh.flush()


# check gmail and download the openvpn config file attached
def download_email_attachment(logger, userName, passwd):
    from autotest.run_autotest import config
    #detach_dir = '.'
    download_dir = config['download']['attachment_download']
    fileName = ""

    if "attachments" not in os.listdir(download_dir):
        logger.info("Create the directory for attachments ")
        os.mkdir(download_dir+"\\attachments")

    try:
        imapSession = imaplib.IMAP4_SSL("imap.gmail.com")
        typ, accountDetails = imapSession.login(userName, passwd)
        if typ != "OK":
            logger.error("Not able to sign into %s!" % userName)
            return False

        imapSession.select('Inbox')
        typ, data = imapSession.search(None, '(SUBJECT "OpenVPN client configuration file")')
        if typ != "OK":
            logger.error("Error searching Inbox of %s." % userName)
            return False

        # Get the msgId of the latest email with OpenVPN config file
        msgId = data[0].split()[-1]
        typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
        if typ != "OK":
            logger.error("Error fetching mail from account of %s." % userName)
            return False

        emailBody = messageParts[0][1]
        mail = email.message_from_bytes(emailBody)
        for part in mail.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition") is None:
                continue
            fileName = part.get_filename()

            if bool(fileName) and fileName.split(".")[1] == "ovpn":
                filePath = os.path.abspath(download_dir) + "\\attachments\\" + fileName
                logger.debug("Email attachment file name is %s" % fileName)
                logger.debug("Download the email attachment to %s" % filePath)
                with open(filePath, 'wb+') as fp:
                    logger.debug("Create the email attachment at %s" % filePath)
                    fp.write(part.get_payload(decode=True))
        imapSession.close()
        imapSession.logout()
    except Exception as e:
        logger.exception("Not able to download attachment from account %s with exception: %s" % (userName, str(e)))
        return False
    except imaplib.IMAP4.error as e:
        logger.exception("IMAP login failure with exception %s" % e)
        return False
    finally:
        if bool(fileName):
            return filePath
        else:
            return ""

def upload_result(fname):
    if fname:
        try:

            key = paramiko.RSAKey.from_private_key_file("testdata\\keys\\autotest-com.pem")
            sc = paramiko.SSHClient()
            sc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            sc.connect("atavism.avtxautotest.com",username='ubuntu',pkey=key)
            st = sc.open_sftp()

            localpath = fname
            remotepath = "/var/www/test_results/" + os.path.basename(fname)
            st.put(localpath,remotepath)
            st.close()
        except (OSError,IOError):
            print ("Failed to upload the file {}".format(fname))

def notify_user(file_name, result, time_start, time_stop):
    from autotest.run_autotest import config
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication

    msg = MIMEMultipart()

    me = 'master@avtxautotest.com'
    you = config['results']["recipient_email"].split(',')
    msg['Subject'] = 'Automation Test Report'
    msg['From'] = me
    msg['To'] = ', '.join(you)

    fn = os.path.basename(file_name)
    url = u'http://atavism.avtxautotest.com:8012/test_results/' + fn
    # The main body is just another attachment
    text_body = _result_creator(file_name, result, time_start, time_stop)
    result_link = u'========For more details, download the result <a href="'+url+u'">here</a> ========'
    body = MIMEText(text_body)
    rl = MIMEText(result_link,'html')
    msg.attach(rl)
    msg.attach(body)
    """
    # Attach the test report
    fp = open(file_name, 'rb')
    att = MIMEApplication(fp.read(), subtype="text")
    fp.close()
    att.add_header('Content-Disposition','attachment',
                   filename='CloudN_Test_Report.txt')
    msg.attach(att)
    """
#    s = smtplib.SMTP_SSL('mail.carmelosystems.com', 465)
    s = smtplib.SMTP('atavism.avtxautotest.com')
    # print 'use caremloinfo as source'
    #s.login('info@carmelosystems.com', 'Carmelo2013')

    # print('from:' + me + ' to:' + you)
    print('from:' + me + ' to:' + config['results']["recipient_email"])
    s.sendmail(me, you, msg.as_string())
    s.quit()


def screen_capturer(driver, vpc_name, vpc_function):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    screen_file_name = "results\\temp\\" + vpc_name + \
                       vpc_function + "%s.png" % now
    driver.save_screenshot(screen_file_name)
    return screen_file_name


def table_creator(size):
    from autotest.run_autotest import test_results

    for i in range(size):
        test_id = "Test" + str(i+1)
        test_results.update({test_id: [{"VPC_Name": "n/a", "VPC_Creation": "n/a",
                                        "Instance_Creation": "n/a", "Instance_Pings": "n/a",
                                        "Instance_Deletion": "n/a", "VPC_Deletion": "n/a"}]})


def result_writer(vpc_name, key, value):
    from autotest.run_autotest import test_results
    from autotest.run_autotest import config

    start = int(config["starting_vpc_number"])

    # find the index from vpc_name
    if vpc_name.find("vpc-") == -1:
        vpc_number = re.search("vpc(.+)", vpc_name)
        if vpc_number:
            ind = int(vpc_number.group(1))-start
            test_id = "Test" + str(ind+1)
            if key in ["VPC_Name", "VPC_Creation",
                       "Instance_Creation", "Instance_Pings",
                       "Instance_Deletion", "VPC_Deletion"]:
                try:
                    test_results[test_id][0][key] = value
                except IndexError as e:
                    print("result_writer: " + str(e))


def result_dumper(json_file, vpc_data):
    with open(json_file, 'a') as fh:
        json.dump(vpc_data, fh)
        fh.flush()


def result_printer(json_file, result_file):
    loaded_list = []
    if os.path.isfile(json_file):
        with open(json_file, 'r') as fh:
            try:
                loaded = json.load(fh)
            except ValueError:
                    return False

        for i in range(len(loaded)):
            test_id = "Test" + str(i+1)
            loaded_list.append([loaded[test_id][0]["VPC_Name"],
                                loaded[test_id][0]["VPC_Creation"],
                                loaded[test_id][0]["Instance_Creation"],
                                loaded[test_id][0]["Instance_Pings"],
                                loaded[test_id][0]["Instance_Deletion"],
                                loaded[test_id][0]["VPC_Deletion"]])

    with open(result_file, 'w') as fh:
        print(tabulate(loaded_list, headers=["VPC Name", "VPC Creation",
                                             "Instance Creation", "Instance Pings",
                                             "Instance Deletion", "VPC Deletion"]), file=fh)


def parse_ping_result(logger, ping_result, target_pass_rate):
    passed = 0
    if ping_result['ssh_status'] == 0:
        #output = ping_result['ssh_stdout'].decode('utf-8')
        for line in ping_result['ssh_stdout'].split('\n'):
            logger.debug(line)
            stats = re.match(r'(.*) packets transmitted, (.*) received', line)
            if stats:
                pass_rate = int(stats.group(2)) / int(stats.group(1)) * 100
                if pass_rate > target_pass_rate:
                    print("Actual ping pass rate is " + str(pass_rate))
                    passed = 1
    else:
        logger.error("ping test failed with errors: " + ping_result['ssh_stderr'].decode('utf-8'))

    if passed == 1:
        return True
    else:
        return False


def get_email_payload_by_msgid(email_accnt, passwd, msgId, delete_it):
    if msgId is None:
        return None
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_accnt, passwd)
    mail.list()
    mail.select('inbox')
    result, messageParts = mail.fetch(msgId, '(RFC822)')
    if result != "OK":
        print("Error fetching mail.")
        return None

    emailBody = messageParts[0][1]
    print(emailBody)
    readable_mail = email.message_from_bytes(emailBody)

    if delete_it:
        print("Delete the message to prevent recheck on the previous notice mail.")
        print("The Delete email still can be tracked in the TRASH folder for 30 days")
        #print(mail.store("1:{0}".format(msgId), '+X-GM-LABELS', '\\Trash'))  # move to trash
        print(mail.store(msgId,'+FLAGS', '\\Deleted'))  # delete
        print("Message deleted!!")


    mail.close()
    mail.logout()
    for part in readable_mail.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=False)
            print("The part.get_payload is: \n", body)

            return body
        else:
            continue

    return None


def get_msgid_by_search_subject(email_accnt, passwd, search_string):
    import imaplib
    search_loop = 0

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    print("email is:", email_accnt)
    print("passwd:", passwd)
    mail.login(email_accnt, passwd)
    mail.list()
    mail.select('inbox')
    result, data = mail.search(None, '(SUBJECT "' + search_string + '")')
    #print("The result is: ", result)
    #print("The data   is: ", data, "Type is:", type(data))
    #print("lalala***********************lalala")

    if result != "OK":
        print("Call searching Inbox Error")
        return None

    while not data[0].split():
        mail.close()
        mail.logout()
        if search_loop < 30:
            search_loop += 1
            print("Search email subject every 2 mins loop: ", search_loop)
            #print("The search_string is: ", search_string)
            time.sleep(120)
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(email_accnt, passwd)
            mail.list()
            mail.select('inbox')
            result, data = mail.search(None, '(SUBJECT "' + search_string + '")')
            #print("data is: ", data)
            #print("data[0] is: ", data[0])
            continue
        else:
            print("Error searching Inbox.")
            mail.close()
            mail.logout()
            return None

    msgId = data[0].split()[-1]

    mail.close()
    mail.logout()
    return msgId


# retrieve the public IP of local machine
def get_public_ip():
    import ipgetter
    IP = ipgetter.myip()
    print("Public IP address is ", IP)
    return IP


"""
runs a command via the shell and returns the exit code and the
output result fro the given cmd. raise exception RunOsCommandsErr
on non exit status and log the errors. return result of exec on sucess
"""
def run_os_command(cmd):
    import subprocess

    p = subprocess.Popen([cmd], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True, bufsize=-1)
    result, error = p.communicate()
    returncode = p.returncode
    if returncode == 0:
        return result
    elif returncode == 1:
        reason = 'Command NOT succeed. Exit code:1. '
    else:
        reason = 'Command error occured. Exit code:{}.'.format(returncode)
    error_msg = 'Command:"{}" FAILed.'.format(cmd)
    err = '{} Reason:{} Error: {} Return:{}'.format(error_msg, reason, error, result)
    raise Exception(err)