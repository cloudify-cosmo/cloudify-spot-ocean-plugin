import decorators
from cloudify.exceptions import NonRecoverableError
from ..spot_ocean_sdk import spot_ocean
from .utils import validate_resource_config


@decorators.with_spot_ocean
def create(client, ctx, resource_config):
    expected_resource_config = [
        "SecurityGroupIDs",
        "KeyPair",
        "InstanceTypes",
        "SubnetIDs",
        "MinCapacity",
        "MaxCapacity",
        "TargetCapacity",
        "OceanClusterName",
        "ClusterID",
        "Region"
    ]
    if not validate_resource_config(resource_config, expected_resource_config):
        raise NonRecoverableError(
            'resource_config is missing parameters.\n '
            'resource config = {}, expected to include {}'.format(
                resource_config.keys(), expected_resource_config)
        )

    launch_specification = spot_ocean.get_launch_specification_object(
        security_group_ids=resource_config.get("SecurityGroupIDs"),
        image_id=resource_config.get("ImageID"),
        key_pair=resource_config.get("KeyPair"))

    instance_types = spot_ocean.get_instance_types_object(
        instance_types=resource_config.get("InstanceTypes"))

    compute = spot_ocean.get_compute_object(
        instance_types=instance_types,
        launch_specification=launch_specification,
        subnet_ids=resource_config.get("SubnetIDs"))

    strategy = spot_ocean.get_strategy_object()
    capacity = spot_ocean.get_capacity_object(
        minimum=resource_config.get("MinCapacity"),
        maximum=resource_config.get("MaxCapacity"),
        target=resource_config.get("TargetCapacity"))

    ocean = spot_ocean.get_ocean_object(
        name=resource_config.get("OceanClusterName"),
        cluster_id=resource_config.get("ClusterID"),
        region=resource_config.get("Region"),
        capacity=capacity,
        strategy=strategy,
        compute=compute)
    create_response = client.create_ocean_cluster(ocean=ocean)
    instance_id = create_response.get("id", None)
    if not instance_id:
        raise NonRecoverableError(
            'cluster not added successfully to spot ocean')
    ctx.instance.runtime_properties["create_response"] = create_response
    ctx.instance.runtime_properties["instance_id"] = instance_id


@decorators.with_spot_ocean
def delete(client, ctx, resource_config):
    return client.delete_ocean_cluster(
        ctx.instance.runtime_properties.get("instance_id"))


@decorators.with_spot_ocean
def describe_all(client, ctx, resource_config):
    return client.get_all_ocean_cluster()


@decorators.with_spot_ocean
def describe_all(client, ctx, resource_config):
    return client.get_ocean_cluster(
        ctx.instance.runtime_properties.get("instance_id"))
