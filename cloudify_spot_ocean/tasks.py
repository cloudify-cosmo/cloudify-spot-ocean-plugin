import decorators
from ..spot_ocean_sdk import spot_ocean


@decorators.with_spot_ocean
def create(client, ctx, resource_config):
    launch_specification = spot_ocean.get_launch_specification_object(
        security_group_ids=resource_config["SecurityGroupIDs"],
        image_id=resource_config["ImageID"],
        key_pair=resource_config["KeyPair"])

    instance_types = spot_ocean.get_instance_types_object(
        instance_types=resource_config["InstanceTypes"])

    compute = spot_ocean.get_compute_object(
        instance_types=instance_types,
        launch_specification=launch_specification,
        subnet_ids=resource_config["SubnetIDs"])

    strategy = spot_ocean.get_strategy_object()
    capacity = spot_ocean.get_capacity_object(
        minimum=resource_config["MinCapacity"],
        maximum=resource_config["MaxCapacity"],
        target=resource_config["TargetCapacity"])

    ocean = spot_ocean.get_ocean_object(
        name=resource_config["OceanClusterName"],
        cluster_id=resource_config["ClusterID"],
        region=resource_config["Region"],
        capacity=capacity,
        strategy=strategy,
        compute=compute)
    create_response = client.create_ocean_cluster(ocean=ocean)
    instance_id = create_response["id"]
    ctx.instance.runtime_properties["create_response"] = create_response
    ctx.instance.runtime_properties["instance_id"] = instance_id


@decorators.with_spot_ocean
def delete(client, ctx, resource_config):
    return client.delete_ocean_cluster(
        ctx.instance.runtime_properties["instance_id"])


@decorators.with_spot_ocean
def describe_all(client, ctx, resource_config):
    return client.get_all_ocean_cluster()


@decorators.with_spot_ocean
def describe_all(client, ctx, resource_config):
    return client.get_ocean_cluster(
        ctx.instance.runtime_properties["instance_id"])
