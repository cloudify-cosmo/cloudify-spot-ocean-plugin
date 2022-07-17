from spot_ocean_sdk import spot_ocean
from cloudify.exceptions import NonRecoverableError
from spotinst_sdk2.client import SpotinstClientException

from . import decorators
from .utils import validate_resource

EXPECTED_RESOURCE_CONFIG = [
        "SecurityGroupIds",
        "KeyPair",
        "InstanceTypes",
        "SubnetIds",
        "MinCapacity",
        "MaxCapacity",
        "TargetCapacity",
        "OceanClusterName",
        "ClusterId",
        "Region"
    ]


@decorators.with_spot_ocean
def create(ocean_client, ctx, resource_config, **_):
    validate_resource(resource=resource_config,
                      expected_resources=EXPECTED_RESOURCE_CONFIG,
                      operation='resource_config')

    launch_specification = spot_ocean.get_launch_specification_object(
        security_group_ids=resource_config.get("SecurityGroupIds"),
        image_id=resource_config.get("ImageId"),
        key_pair=resource_config.get("KeyPair"),
        cluster_id=resource_config.get("ClusterId")
    )

    instance_types = spot_ocean.get_instance_types_object(
        instance_types=resource_config.get("InstanceTypes"))

    compute = spot_ocean.get_compute_object(
        instance_types=instance_types,
        launch_specification=launch_specification,
        subnet_ids=resource_config.get("SubnetIds"))

    strategy = spot_ocean.get_strategy_object()
    capacity = spot_ocean.get_capacity_object(
        minimum=resource_config.get("MinCapacity"),
        maximum=resource_config.get("MaxCapacity"),
        target=resource_config.get("TargetCapacity"))

    ocean = spot_ocean.get_ocean_object(
        name=resource_config.get("OceanClusterName"),
        cluster_id=resource_config.get("ClusterId"),
        region=resource_config.get("Region"),
        capacity=capacity,
        strategy=strategy,
        compute=compute)
    create_response = ocean_client.create_ocean_cluster(ocean=ocean)
    instance_id = create_response.get("id", None)
    if not instance_id:
        raise NonRecoverableError(
            'EKS cluster not added successfully to spot ocean')
    clusters = describe_all(ocean_client)
    for i in clusters:
        if i['name'] == resource_config.get("OceanClusterName") and\
                i['controller_cluster_id'] == resource_config.get("ClusterId"):
            ctx.instance.runtime_properties["create_response"] = \
                create_response
            ctx.instance.runtime_properties["instance_id"] = instance_id
            return create_response
    raise NonRecoverableError(
        'EKS cluster not added successfully to spot ocean. create response = '
        '{}'.format(create_response))


@decorators.with_spot_ocean
def delete(ocean_client, ctx, instance_id=None, **_):
    instance_id = instance_id or \
                  ctx.instance.runtime_properties.get("instance_id")
    while wait_for_delete(ocean_client, instance_id):
        ocean_client.delete_ocean_cluster(instance_id)


def wait_for_delete(ocean_client, instance_id):
    try:
        val = ocean_client.get_ocean_cluster(instance_id)
        return val
    except SpotinstClientException:
        return None


def describe_all(ocean_client, **_):
    return ocean_client.get_all_ocean_cluster()


def describe(ocean_client, ctx, instance_id=None, **_):
    instance_id = instance_id or \
                  ctx.instance.runtime_properties.get("instance_id")
    return ocean_client.get_ocean_cluster(instance_id)
