__author__ = 'lmxiang'

import logging
import azure

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource.resources.models import ResourceGroup
from azure.mgmt.network.models import AddressSpace, Subnet, VirtualNetwork, \
    IPAllocationMethod, NetworkInterface, NetworkInterfaceIPConfiguration, PublicIPAddress, \
    NetworkSecurityGroup
from azure.mgmt.storage.models import StorageAccountCreateParameters, Sku, Kind, SkuName
from azure.mgmt.compute.models import VirtualMachine, OSProfile, HardwareProfile, \
    StorageProfile, OSDisk, CachingTypes, DiskCreateOptionTypes, VirtualHardDisk, \
    ImageReference, VirtualMachineSizeTypes, NetworkProfile, NetworkInterfaceReference, Plan
#from tests.utils.test_utils import avx_logger

logger = logging.getLogger(__name__)

def get_ad_sp_credential(tenant_id, client_id, client_secret):
    #logger = logging.getLogger('cloudx')
    #info = 'subscription_id: ' + subscription_id
    #logger.info(info)
    try:
        credentials = ServicePrincipalCredentials(client_id=client_id, secret=client_secret, tenant=tenant_id)
    except Exception as e:
        logger.error(str(e))
        return None
    logger.info('get_ad_sp_credential successful.')
    return credentials


def _check_cred_id(subscription_id, credentials):
    logger = logging.getLogger('cloudx')
    if credentials is None or subscription_id == '':
        reason = 'Azure RM credential not available. Please check Azure RM credential.'
        logger.error(reason)
        return False
    else:
        return True


def find_vnet(subscription_id, credentials, vnet_name):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    network_client = NetworkManagementClient(credentials, subscription_id)

    vnet_iter = network_client.virtual_networks.list_all()
    vnets = list(vnet_iter)

    for vnet in vnets:
        info = 'vnet_name: ' + vnet.name + \
               ' vnet_cidr: ' + vnet.address_space.address_prefixes[0]
        logger.info(info)
        if vnet.name == vnet_name:
            vnet_cidr = vnet.address_space.address_prefixes[0]
            resource_id = vnet.id
            vnet_rg = vnet_rg = resource_id.split('/')[4]
            info = 'vnet ' + vnet_name + ' found. vnet_rg: ' \
                   + vnet_rg + ' vnet_cidr: ' + vnet_cidr
            logger.info(info)
            return (vnet, vnet_rg)
    return False


def create_resource_group(subscription_id, credentials, region, group_name):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    resource_client = ResourceManagementClient(credentials, subscription_id)

    resource_group_params = ResourceGroup(
        location=region,
        tags={
            'RGID': subscription_id + group_name
        },
    )

    result_create = resource_client.resource_groups.create_or_update(
        group_name,
        resource_group_params,
    )

    logger.info('Resource group {} is create'.format(result_create.name))


def find_resource_group(subscription_id, credentials, group_name):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    resource_client = ResourceManagementClient(credentials, subscription_id)

    try:
        result = resource_client.resource_groups.get(group_name)
    except:
        logger.error("Resource group %s not found", group_name)
        return False

    if result:
        logger.info("Resource group %s found", group_name)
        return True
    else:
        logger.error("Resource group %s not found", group_name)
        return False


def delete_resource_group(subscription_id, credentials, group_name):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    resource_client = ResourceManagementClient(credentials, subscription_id)

    result_delete = resource_client.resource_groups.delete(
        group_name,
    ).result()


def create_storage_account(subscription_id, credentials, region, group_name, storage_name):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    storage_client = StorageManagementClient(credentials, subscription_id)

    resource_client = ResourceManagementClient(credentials, subscription_id)
    resource_client.providers.register('Microsoft.Storage')

    result = storage_client.storage_accounts.create(
        group_name,
        storage_name,
        StorageAccountCreateParameters(
            location = region,
            sku = Sku(name=SkuName.standard_lrs),
            kind = Kind.storage,
        ),
    ).result()


def find_storage_account(subscription_id, credentials, group_name, storage_name):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    storage_client = StorageManagementClient(credentials, subscription_id)

    storage_accounts = storage_client.storage_accounts.list_by_resource_group(group_name)

    for storage_account in storage_accounts:
        if storage_account.name == storage_name:
            logger.info("Storage account %s found", storage_name)
            return True

    logger.info("Storage account %s not found", storage_name)
    return False


def find_image(subscription_id, credentials, region, publisher_name, offer_name, sku_name):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    compute_client = ComputeManagementClient(credentials, subscription_id)

    result_list_pub = compute_client.virtual_machine_images.list_publishers(
        region,
    )

    version_list = []
    for publisher in result_list_pub:
        if publisher.name == publisher_name:
            result_list_offers = compute_client.virtual_machine_images.list_offers(
                region,
                publisher.name,
            )

            for offer in result_list_offers:
                if offer.name == offer_name:
                    result_list_skus = compute_client.virtual_machine_images.list_skus(
                        region,
                        publisher.name,
                        offer.name,
                    )

                    for sku in result_list_skus:
                        if sku.name == sku_name:
                            result_list = compute_client.virtual_machine_images.list(
                                region,
                                publisher.name,
                                offer.name,
                                sku.name,
                            )

                            for version in result_list:
                                result_get = compute_client.virtual_machine_images.get(
                                    region,
                                    publisher.name,
                                    offer.name,
                                    sku.name,
                                    version.name,
                                )

                            version_list.append(version)

    version = version_list[-1].name

    logger.info("The latest %s %s version: %s", (offer_name, sku_name, version))

    return version


def create_virtual_network(subscription_id, credentials, region, group_name, vnet_name, subnet_name,
                           vnet_cidr, subnet_cidr):
    #logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    resource_client = ResourceManagementClient(credentials, subscription_id)
    resource_client.providers.register('Microsoft.Network')
    network_client = NetworkManagementClient(credentials, subscription_id)

    address_spaces= AddressSpace(address_prefixes=[vnet_cidr])
    subnets = [Subnet(name=subnet_name, address_prefix=subnet_cidr)]
    network_parameters = VirtualNetwork(location=region, address_space=address_spaces, subnets=subnets)

    result_create = network_client.virtual_networks.create_or_update(group_name,vnet_name,
                                                                     network_parameters).result()


def get_virtual_subnet(subscription_id, credentials, group_name, network_name, subnet_name):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    network_client = NetworkManagementClient(credentials, subscription_id)

    subnet = network_client.subnets.get(group_name, network_name, subnet_name)

    return subnet


def create_public_ip(subscription_id, credentials, region, group_name, ip_name):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    network_client = NetworkManagementClient(credentials, subscription_id)

    result_create = network_client.public_ip_addresses.create_or_update(
        group_name,
        ip_name,
        PublicIPAddress(
            location=region,
            public_ip_allocation_method=IPAllocationMethod.static,
            idle_timeout_in_minutes=4
        )
    ).result()


def get_public_ip(subscription_id, credentials, group_name, ip_name):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    network_client = NetworkManagementClient(credentials, subscription_id)

    public_ip_address = network_client.public_ip_addresses.get(group_name, ip_name)

    allocated_ip = public_ip_address.ip_address

    logger.info('Public IP allocated {}'.format(allocated_ip))

    return allocated_ip

def create_network_interface(subscription_id, credentials, region, group_name, interface_name,
                             network_name, subnet_name, ip_name, security_group):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    network_client = NetworkManagementClient(credentials, subscription_id)
    subnet = get_virtual_subnet(subscription_id, credentials, group_name, network_name, subnet_name)

    public_ip_address = network_client.public_ip_addresses.get(group_name, ip_name)
    public_ip_id = public_ip_address.id
    logger.info("public_ip_id " + public_ip_id)

    result = network_client.network_interfaces.create_or_update(
        group_name,
        interface_name,
        azure.mgmt.network.models.NetworkInterface(
            location=region,
            network_security_group=security_group,
            ip_configurations=[
                azure.mgmt.network.models.NetworkInterfaceIPConfiguration(
                    name='default',
                    private_ip_allocation_method=azure.mgmt.network.models.IPAllocationMethod.dynamic,
                    subnet=subnet,
                    public_ip_address=azure.mgmt.network.models.PublicIPAddress(
                        id=public_ip_id,
                    ),
                ),
            ],
        ),
    ).result()


def get_network_interface(subscription_id, credentials, group_name, interface_name):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    network_client = NetworkManagementClient(credentials, subscription_id)

    network_interface = network_client.network_interfaces.get(
        group_name,
        interface_name,
    )
    return network_interface.id

def get_private_ip_address(subscription_id, credentials, group_name, interface_name):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    network_client = NetworkManagementClient(credentials, subscription_id)

    network_interface = network_client.network_interfaces.get(
        group_name,
        interface_name,
    )

    private_ip = network_interface.ip_configurations[0].private_ip_address

    logger.info('Private IP allocated {}'.format(private_ip))

    return private_ip

def create_security_group(subscription_id, credentials, region, resource_group, sg_name):
    params_create = azure.mgmt.network.models.NetworkSecurityGroup(
        location=region,
        security_rules=[
            azure.mgmt.network.models.SecurityRule(
                name=sg_name,
                access=azure.mgmt.network.models.SecurityRuleAccess.allow,
                description='Aviatrix security rule',
                destination_address_prefix='*',
                destination_port_range='*',
                direction=azure.mgmt.network.models.SecurityRuleDirection.inbound,
                priority=500,
                protocol=azure.mgmt.network.models.SecurityRuleProtocol.tcp,
                source_address_prefix='*',
                source_port_range='*',
            ),
        ],
    )
    network_client = NetworkManagementClient(credentials, subscription_id)
    result_create = network_client.network_security_groups.create_or_update(resource_group, sg_name,
                                                                            params_create)
    result_create.wait()

def get_security_group(subscription_id, credentials, resource_group, sg_name):
    network_client = NetworkManagementClient(credentials, subscription_id)
    security_group = network_client.network_security_groups.get(resource_group, sg_name)

    return security_group

def create_vm(subscription_id, credentials, region, group_name, ip_name, network_name, subnet_name,
              interface_name, storage_name, vm_name, vnet_cidr, subnet_cidr, security_group, vm_data,
              vm_property, marketplace=False):
    vm_info = {}
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    IMAGE_PUBLISHER = vm_data['IMAGE_PUBLISHER']
    IMAGE_OFFER = vm_data['IMAGE_OFFER']
    IMAGE_SKU = vm_data['IMAGE_SKU']
    IMAGE_VERSION = vm_data['IMAGE_VERSION']

    osdisk_name = vm_property['osdisk_name']
    vm_username = vm_property['vm_username']
    vm_password = vm_property['vm_password']
    vm_computer_name = vm_property['vm_computer_name']

    compute_client = ComputeManagementClient(credentials, subscription_id)

    resource_client = ResourceManagementClient(credentials, subscription_id)
    resource_client.providers.register('Microsoft.Compute')
    resource_client.providers.register('Microsoft.Network')
    resource_client.providers.register('Microsoft.Storage')

    if find_resource_group(subscription_id, credentials, group_name):
        logger.info("Resource group already exists. Delete it now")
        delete_resource_group(subscription_id, credentials, group_name)
    logger.info("Create Resource Group")
    create_resource_group(subscription_id, credentials, region, group_name)
    if not find_resource_group(subscription_id, credentials, group_name):
        logger.error("Failed to create resource group %s for vm %s", (group_name, vm_name))
        return False

    logger.info("Allocate Public IP")
    create_public_ip(subscription_id, credentials, region, group_name, ip_name)
    public_ip = get_public_ip(subscription_id, credentials, group_name, ip_name)
    if not public_ip:
        logger.error("Failed to allocate public IP for vm %s", vm_name)
        return False
    logger.info("Public ip allocated successfully " + public_ip)
    vm_info.update({'public_ip': public_ip})

    logger.info("Create Virtual Network and its Subnets")
    create_virtual_network(subscription_id, credentials, region, group_name, network_name,
                           subnet_name, vnet_cidr, subnet_cidr)
    subnet = get_virtual_subnet(subscription_id, credentials, group_name, network_name, subnet_name)
    if not subnet:
        logger.error("Failed to create VNet for vm %s", vm_name)
        return False
    logger.info("VNet created successfully")

    logger.info("Create Network Security Group")
    create_security_group(subscription_id, credentials, region, group_name, security_group)
    security_group = get_security_group(subscription_id, credentials, group_name, security_group)

    logger.info("Create Network Interface")
    create_network_interface(subscription_id, credentials, region, group_name, interface_name,
                             network_name, subnet_name, ip_name, security_group)
    nic_id = get_network_interface(subscription_id, credentials, group_name, interface_name)
    if not nic_id:
        logger.error("Failed to create network interface for vm %s", vm_name)
        return False
    logger.info("Network interface %s created successfully" + nic_id)

    private_ip = get_private_ip_address(subscription_id, credentials, group_name, interface_name)
    if not private_ip:
        logger.error("Failed to allocate private IP for vm %s", vm_name)
        return False
    logger.info("Private ip allocated successfully" + private_ip)
    vm_info.update({'private_ip': private_ip})

    logger.info("Create Storage Account")
    create_storage_account(subscription_id, credentials, region, group_name, storage_name)
    if not find_storage_account(subscription_id, credentials, group_name, storage_name):
        logger.error("Failed to find storage account for vm %s", vm_name)
        return False
    logger.info("Storage account %s created successfully" + storage_name)

    logger.info("Create Virtual Machine")
    if not marketplace:
        result_vm = compute_client.virtual_machines.create_or_update(
            group_name,
            vm_name,
            VirtualMachine(
                location=region,
                os_profile=OSProfile(
                    admin_username=vm_username,
                    admin_password=vm_password,
                    computer_name=vm_computer_name,
                ),
                hardware_profile=HardwareProfile(
                    vm_size=VirtualMachineSizeTypes.standard_a1
                ),
                network_profile=NetworkProfile(
                    network_interfaces=[
                        NetworkInterfaceReference(
                            id=nic_id,
                        ),
                    ],
                ),
                storage_profile=StorageProfile(
                    os_disk=OSDisk(
                        caching=CachingTypes.none,
                        create_option=DiskCreateOptionTypes.from_image,
                        name=osdisk_name,
                        vhd=VirtualHardDisk(
                            uri='https://{0}.blob.core.windows.net/vhds/{1}.vhd'.format(
                                storage_name,
                                osdisk_name,
                            ),
                        ),
                    ),
                    image_reference=ImageReference(
                        publisher=IMAGE_PUBLISHER,
                        offer=IMAGE_OFFER,
                        sku=IMAGE_SKU,
                        version=IMAGE_VERSION,
                    ),
                ),
            ),
        )
    else:
        result_vm = compute_client.virtual_machines.create_or_update(
            group_name,
            vm_name,
            VirtualMachine(
                location=region,
                plan=Plan(
                    name=IMAGE_SKU,
                    product=IMAGE_OFFER,
                    publisher=IMAGE_PUBLISHER
                ),
                os_profile=OSProfile(
                    admin_username=vm_username,
                    admin_password=vm_password,
                    computer_name=vm_computer_name,
                ),
                hardware_profile=HardwareProfile(
                    vm_size=VirtualMachineSizeTypes.standard_ds2
                ),
                network_profile=NetworkProfile(
                    network_interfaces=[
                        NetworkInterfaceReference(
                            id=nic_id,
                        ),
                    ],
                ),
                storage_profile=StorageProfile(
                    os_disk=OSDisk(
                        caching=CachingTypes.none,
                        create_option=DiskCreateOptionTypes.from_image,
                        name=osdisk_name,
                        vhd=VirtualHardDisk(
                            uri='https://{0}.blob.core.windows.net/vhds/{1}.vhd'.format(
                                storage_name,
                                osdisk_name,
                            ),
                        ),
                    ),
                    image_reference=ImageReference(
                        publisher=IMAGE_PUBLISHER,
                        offer=IMAGE_OFFER,
                        sku=IMAGE_SKU,
                        version=IMAGE_VERSION,
                    ),
                ),
            ),
        )
    result_vm.wait()
    return vm_info

def find_vm(subscription_id, credentials, group_name, vm_name):
    logger = logging.getLogger('cloudx')
    if not _check_cred_id(subscription_id, credentials):
        return None

    compute_client = ComputeManagementClient(credentials, subscription_id)

    result_vms = compute_client.virtual_machines.list(group_name)

    for vm in result_vms:
        if vm.name == vm_name:
            logger.info("%s found", vm_name)
            return True

    logger.error("%s not found", vm_name)
    return False

def main():
    """
    subscription_id = 'b8b6202f-4cd1-4101-a016-00a84c4128c2'
    arm_tenant_id = '14ccb0a2-ca16-446f-8711-795cc4125fa5'
    arm_client_id = 'df29d4f8-fc1d-4ae5-9956-fbf02f037881'
    arm_client_secret = 'ntypHQrFvirImv4IzbBhVUEO/94ChHbYq9X6PLePayw='

    vm1 = {"IMAGE_PUBLISHER": "aviatrix-systems",
           "IMAGE_OFFER": "aviatrix-cloud-services-preview",
           "IMAGE_SKU": "av-csg-byol",
           "IMAGE_VERSION": "latest"
           }

    vm2 = {"IMAGE_PUBLISHER": "aviatrix-systems",
           "IMAGE_OFFER": "aviatrix-cloud-services-preview",
           "IMAGE_SKU": "av-csg-10-tunnels",
           "IMAGE_VERSION": "latest"
           }

    vm_list = [vm1, vm2]

    vm_property = {"osdisk_name": "aviatrixosdisk123",
                   "vm_username": "administrator",
                   "vm_password": "Aviatrix123#",
                   "vm_computer_name": "avx-controller"
                   }

    vm_index = 1
    credential = get_ad_sp_credential(subscription_id, arm_tenant_id, arm_client_id, arm_client_secret)
    for vm_data in vm_list:
        logger.info("Create VM %s", str(vm_index))
        create_vm(subscription_id, credential, "eastus2", "avxreggrp", "avxregip", "avxregnet", "avxregsub",
                  "avxregitf", "avxregstorage", "avxregvm", "192.168.0.0/16", "192.168.1.0/24",
                  "avxregsg", vm_data, vm_property, marketplace=True)
        find_vm(subscription_id, credential, "avxreggrp", "avxregvm")
        delete_resource_group(subscription_id, credential, "avxreggrp")
        vm_index = vm_index + 1
    """

if __name__ == '__main__':
    logger = logging.getLogger("cloudn-test")
    #ch = logging.StreamHandler()
    #ch.setLevel(logging.DEBUG)

    main()
