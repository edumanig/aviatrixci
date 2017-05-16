__author__ = 'lmxiang'

import argparse
import logging
import json
import os
import re
import tests.exceptions

from tests.test_utils import run_os_cmd
from tests.vnet_utils import cidrstring_to_ipint, int_to_ipstring


def check_ping_results():
    logger = logging.getLogger('cloudx')

    output_file = "archives\\temp\\cmd_output_file"
    output_file_abs = os.path.abspath(output_file)

    transmitted = 0
    received = 0
    ping_pass_rate = 0.8

    with open(output_file_abs) as f:
        content = f.readlines()
    for line in content:
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
            for line in content:
                logger.debug(line)
            logger.error("ping test FAILED: success rate is %f" % success_rate)
            return False
    else:
        logger.info("No ping packet as transmitted. Failed")
        return False


def create_instance(inst_name, subnet_name, cidr):
    logger = logging.getLogger('cloudx')
    machine_type = 'n1-standard-1'
    private_ip = '10'
    private_network_ip = int_to_ipstring(cidrstring_to_ipint(cidr, private_ip))
    print('private_network_ip: ', private_network_ip)
    metadata = 'google-cloud-marketplace-solution-key=ubuntu-os-cloud:ubuntu-trusty'
    image = '/ubuntu-os-cloud/ubuntu-1404-trusty-v20160610'
    maintenance_policy = 'MIGRATE'
    scopes = 'default="https://www.googleapis.com/auth/cloud-platform"'
    tags = 'aviatrix-user-instance'
    boot_disk_size = '10'
    boot_disk_type = 'pd-standard'
    boot_disk_device_name = 'ubuntu-trusty-1'

    cmd = 'gcloud compute instances create {} --machine-type {} --subnet {} --private-network-ip {} ' \
          '--metadata {} --maintenance-policy {} --scopes {} --tags {} --image {} --boot-disk-size {} ' \
          '--boot-disk-type {} --boot-disk-device-name {} --format json --verbosity error'
    cmd = cmd.format(inst_name, machine_type, subnet_name, private_network_ip, metadata, maintenance_policy,
                     scopes, tags, image, boot_disk_size, boot_disk_type, boot_disk_device_name)
    print(cmd)
    logger.info('##### cmd - %s', cmd)

    try:
        result = run_os_cmd(cmd)
        logger.info('cmd done successfully - %s', result)
    except tests.exceptions.RunOsCommandsErr as err:
        logger.error(err)

    try:
        if result:
             with open(result, "r") as fin:
                json_data = fin.read()
                inst_info = json.loads(json_data)
                if inst_info[0]['status'] == "RUNNING":
                    logger.info("User instance is in running state")
                else:
                    logger.error("User instance fails to come up")
    except ValueError:
        logger.error("JSON loads error while creating user instance")


def delete_instance(inst_name):
    logger = logging.getLogger('cloudx')
    cmd = 'gcloud compute instances delete {} --zone {} --quiet --format json'
    cmd = cmd.format(inst_name, 'us-central1-b')
    print(cmd)
    logger.info('##### cmd - %s', cmd)

    try:
        result = run_os_cmd(cmd)
        logger.info('cmd done successfully - %s', result)
    except tests.exceptions.RunOsCommandsErr as err:
        logger.error(err)


def ssh_instance(inst_name, ssh_cmd):
    logger = logging.getLogger('cloudx')
    cmd = 'gcloud compute ssh ubuntu@{} --format json --quiet --command {}'
    cmd = cmd.format(inst_name, ssh_cmd)
    print(cmd)
    logger.info('##### cmd - %s', cmd)

    try:
        result = run_os_cmd(cmd, trim=False)
        logger.info('cmd done successfully - %s', result)
    except tests.exceptions.RunOsCommandsErr as err:
        logger.error(err)


def get_project_info():
    logger = logging.getLogger('cloudx')
    command = 'gcloud compute project-info describe --format json'
    try:
        result = run_os_cmd(command)
    except tests.exceptions.RunOsCommandsErr as err:
        logger.error(err)
        return []


def list_gce_network(project):
    logger = logging.getLogger('cloudx')
    command = r'gcloud compute networks list --project %s  --format json' % project
    try:
        result = run_os_cmd(command)
        with open(result, "r") as fin:
            json_data = fin.read()
            vpcs = json.loads(json_data)
            logger.info('Done command %s', command)
    except tests.exceptions.RunOsCommandsErr as err:
        logger.error(err)
        return []

    vpc_array = []
    for vpc in vpcs:
        vpc_item = {}
        if vpc:
            if vpc['x_gcloud_mode'] == 'legacy':
                continue
            vpc_item['project'] = project
            vpc_item['name'] = vpc['name']
            vpc_item['x_gcloud_mode'] = vpc['x_gcloud_mode']
            vpc_array.append(vpc_item)
    logger.info('vpc_array is %s', str(vpc_array))
    print(str(vpc_array))
    return vpc_array


def create_gce_network(network_name, subnet_name, cidr):
    logger = logging.getLogger('cloudx')
    # Create network with mode custom
    command1 = r'gcloud compute networks create %s --mode custom --format json' % network_name
    # Add subnet into this network
    command2 = r'gcloud compute networks subnets create subnet-us-central --network %s ' \
               r'--region us-central1 --range %s --format json' % (subnet_name, cidr)
    # Add firewall rule to allow all intra-network traffic
    command3 = r'gcloud compute firewall-rules create allow-internal --network %s ' \
               r'--allow tcp,udp,icmp --source-range %s' % (network_name, cidr)
    # Add firewall rule to allow all external traffic
    command4 = r'gcloud compute firewall-rules create allow-external --network %s ' \
               r'--allow tcp:22,tcp:3389,icmp' % network_name

    for command in [command1, command2, command3, command4]:
        try:
            result = run_os_cmd(command)
            logger.info('Done command %s', command)
        except tests.exceptions.RunOsCommandsErr as err:
            logger.error(err)


def delete_gce_network(name):
    logger = logging.getLogger('cloudx')
    command1 = r'gcloud compute firewall-rules delete allow-internal --quiet'
    command2 = r'gcloud compute networks subnets delete subnet-us-central --quiet'
    command3 = r'gcloud compute networks delete %s --quiet' % name

    for command in [command1, command2, command3]:
        try:
            result = run_os_cmd(command)
            logger.info('Done command %s', command)
        except tests.exceptions.RunOsCommandsErr as err:
            logger.error(err)


def main(project, zone, instance_name, wait=True):
    '''
    credentials = GoogleCredentials.get_application_default()
    compute = discovery.build('compute', 'v1', credentials=credentials)

    print('Creating instance.')

    operation = create_instance(compute, project, zone, instance_name)
    wait_for_operation(compute, project, zone, operation['name'])

    instances = list_instances(compute, project, zone)

    print('Instances in project %s and zone %s:' % (project, zone))
    for instance in instances:
        print(' - ' + instance['name'])

    print("""
            Instance created.
            It will take a minute or two for the instance to complete work.
            Once the image is uploaded press enter to delete the instance.
        """)

    if wait:
        input()

    print('Deleting instance.')

    operation = delete_instance(compute, project, zone, instance_name)
    wait_for_operation(compute, project, zone, operation['name'])
    '''

    # get_project_info()

    # list_gce_network(project)

    # create_gce_network("newnetwork", "subnet-us-central", "192.168.1.0/24")

    # create_instance("newinstance", "subnet-us-central", "192.168.1.0/24")

    ssh_instance("newinstance", '"ping 127.0.0.1 -c 5"')
    check_ping_results()

    # delete_instance("newinstance")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument(
        '--zone',
        default='us-central1-f',
        help='Compute Engine zone to deploy to.')
    parser.add_argument(
        '--name', default='demo-instance', help='New instance name.')

    args = parser.parse_args()

    main(args.project_id, args.zone, args.name)