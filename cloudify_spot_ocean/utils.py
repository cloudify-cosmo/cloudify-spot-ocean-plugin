from boto3 import client

from cloudify import ctx
from cloudify_common_sdk.utils import (
    get_ctx_node,
    get_ctx_instance,
)
from cloudify.exceptions import NonRecoverableError

from spotinst_sdk2 import SpotinstSession


def get_resource_config(target=False):
    """Get the cloudify.nodes.terraform.Module resource_config"""
    instance = get_ctx_instance(target=target)
    resource_config = instance.runtime_properties.get('resource_config')
    if not resource_config or ctx.workflow_id == 'install':
        node = get_ctx_node(target=target)
        resource_config = node.properties.get('resource_config', {})
    return resource_config


def get_client_config(target=False):
    """Get the cloudify.nodes.terraform.Module resource_config"""
    instance = get_ctx_instance(target=target)
    client_config = instance.runtime_properties.get('client_config')
    if not client_config or ctx.workflow_id == 'install':
        node = get_ctx_node(target=target)
        client_config = node.properties.get('client_config', {})
    return client_config


def get_client(client_config=None):
    if not client_config:
        client_config = get_client_config()
    session = SpotinstSession(auth_token=client_config.get("spot_ocean_token"),
                              account_id=client_config.get("account_id"))
    ocean_client = session.client("ocean_aws")

    return ocean_client


def validate_resource_config(resource_config, expected_resource_config):
    return all(p in resource_config for p in expected_resource_config)


def get_image(cluster_id):
    ec2 = client('ec2')
    cluster_version = get_cluster_version(cluster_id)
    images = ec2.describe_images(
        Filters=[
            {'Name': 'owner-id', 'Values': ['602401143452']},
            {'Name': 'name', 'Values': ['amazon-eks-node-' +
                                        cluster_version +
                                        '*']}
        ]
    )

    oldest_to_newest = sorted(images['Images'],
                              key=lambda x: x['CreationDate'])

    most_recent_image_id = oldest_to_newest[-1]['ImageId']
    return most_recent_image_id


def get_cluster_version(cluster_id):
    eks = client('eks')
    cluster = eks.describe_cluster(cluster_id)
    if 'cluster' not in cluster or 'version' not in cluster['cluster']:
        raise NonRecoverableError(
            'Unable to determine version of EKS cluster {}, '
            'and no ImageId was provided.'.format(cluster_id))
    return cluster['cluster']['version']
