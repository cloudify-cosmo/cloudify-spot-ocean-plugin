from cloudify import ctx

from cloudify_common_sdk.utils import (
    get_ctx_node,
    get_ctx_instance,
)

from spotinst_sdk2 import SpotinstSession


def get_resource_config(target=False):
    """Get the cloudify.nodes.terraform.Module resource_config"""
    instance = get_ctx_instance(target=target)
    resource_config = instance.runtime_properties.get('resource_config')
    ### TODO check if second condtion is needed
    if not resource_config or ctx.workflow_id == 'install':
        node = get_ctx_node(target=target)
        resource_config = node.properties.get('resource_config', {})
    return resource_config


def get_client_config(target=False):
    """Get the cloudify.nodes.terraform.Module resource_config"""
    instance = get_ctx_instance(target=target)
    client_config = instance.runtime_properties.get('client_config')
    ### TODO check if second condtion is needed
    if not client_config or ctx.workflow_id == 'install':
        node = get_ctx_node(target=target)
        client_config = node.properties.get('client_config', {})
    return client_config


def get_client():
    client_config = get_client_config()
    session = SpotinstSession(auth_token=client_config.get("SpotOceanToken"),
                              account_id=client_config.get("AccountID"))
    client = session.client("ocean_aws")

    return client

