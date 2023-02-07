import sys
import boto3

from cloudify import ctx
from spotinst_sdk2 import SpotinstSession
from cloudify_common_sdk.utils import get_ctx_node
from cloudify.exceptions import NonRecoverableError
from cloudify.utils import exception_to_error_cause
from spotinst_sdk2.client import SpotinstClientException
from cloudify_common_sdk.secure_property_management import get_stored_property

EXPECTED_CLIENT_CONFIG = [
        "spot_ocean_token",
        "account_id"
    ]


def get_resource_config(target=False):
    """Get the cloudify.nodes.terraform.Module resource_config"""
    return get_stored_property(ctx, 'resource_config', target)


def get_client_config(target=False, property_name='client_config'):
    """Get the cloudify.nodes.terraform.Module resource_config"""
    node = get_ctx_node(target=target)
    client_config = node.properties.get(property_name, {})
    return client_config


def get_client(client_config=None):
    client_config = client_config or get_client_config()
    validate_resource(resource=client_config,
                      expected_resources=EXPECTED_CLIENT_CONFIG,
                      operation='client_config')

    session = SpotinstSession(auth_token=client_config.get("spot_ocean_token"),
                              account_id=client_config.get("account_id"))
    spot_client = session.client("ocean_aws")
    try:
        spot_client.get_all_ocean_cluster()
    except SpotinstClientException as ex:
        _, _, tb = sys.exc_info()
        print(str(exception_to_error_cause(ex, tb)))
        if hasattr(ex, 'message'):
            print('The message: {}'.format(ex.message))
        raise NonRecoverableError("Spot Ocean client creation failed",
                                  causes=[exception_to_error_cause(ex, tb)])
    return spot_client


def validate_resource(resource, expected_resources, operation=''):
    if not all(p in resource for p in expected_resources):
        raise NonRecoverableError(
            '{} is missing parameters.\n{} = {}, expected to include {}'.format
            (operation, operation, resource.keys(), expected_resources))
    return True


def get_aws_client(aws_resource):
    aws_cred = get_client_config(property_name='aws_config')
    client = boto3.client(
        aws_resource,
        aws_access_key_id=aws_cred.get('aws_access_key_id'),
        aws_secret_access_key=aws_cred.get('aws_secret_access_key'),
        aws_session_token=aws_cred.get('aws_session_token'),
        region_name=aws_cred.get('region_name')
    )
    return client


def get_image(cluster_id):
    ssm = get_aws_client("ssm")
    cluster_version = get_cluster_version(cluster_id)
    ssm_input = '/aws/service/eks/optimized-ami/' + cluster_version +\
                '/amazon-linux-2/recommended/image_id'
    result = ssm.get_parameters(Names=[ssm_input])
    if not result.get('Parameters'):
        raise NonRecoverableError('No Image AMI was provided and no image '
                                  'was found. Please provide an Image AMI')
    image_id = result['Parameters'][0]['Value']
    return image_id
    # ec2 = get_aws_client("ec2")
    # cluster_version = get_cluster_version(cluster_id)
    # images = ec2.describe_images(
    #     Filters=[
    #         {'Name': 'owner-id', 'Values': ['602401143452']},
    #         {'Name': 'name', 'Values': ['amazon-eks-node-' +
    #                                     cluster_version +
    #                                     '*']}
    #     ]
    # )
    # if not images.get('Images'):
    #     raise NonRecoverableError('No Image AMI was provided and no image
    #     was found. Please provide an Image AMI')
    # oldest_to_newest = sorted(images.get('Images'),
    #                           key=lambda x: x['CreationDate'])
    #
    # most_recent_image_id = oldest_to_newest[-1]['ImageId']
    # return most_recent_image_id


def get_cluster_version(cluster_id):
    # eks = client('eks')
    eks = get_aws_client('eks')
    cluster = eks.describe_cluster(name=cluster_id)
    if 'cluster' not in cluster or 'version' not in cluster['cluster']:
        raise NonRecoverableError(
            'Unable to determine version of EKS cluster {}, '
            'and no ImageId was provided.'.format(cluster_id))
    return cluster['cluster']['version']
