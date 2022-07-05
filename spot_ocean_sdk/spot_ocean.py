from spotinst_sdk2.models.ocean import aws

from cloudify.exceptions import NonRecoverableError


def get_launch_specification_object(security_group_ids, image_id, key_pair):
    if not isinstance(security_group_ids, list):
        raise NonRecoverableError(
            'Security group IDs is expected to be a list')
    if not isinstance(image_id, str):
        raise NonRecoverableError('Image ID is expected to be a string')
    if not isinstance(key_pair, str):
        raise NonRecoverableError('Key Pair is expected to be a string')
    launch_specification = aws.LaunchSpecifications(
        security_group_ids=security_group_ids,
        image_id=image_id,
        key_pair=key_pair)

    return launch_specification


def get_instance_types_object(instance_types):
    if not isinstance(instance_types, str):
        raise NonRecoverableError('Instance Types is expected to be a string')
    instance_types = aws.InstanceTypes(whitelist=[instance_types])

    return instance_types


def get_compute_object(instance_types, subnet_ids, launch_specification):
    if not isinstance(subnet_ids, list):
        raise NonRecoverableError('Subnet IDs is expected to be a list')
    compute = aws.Compute(instance_types=instance_types,
                          subnet_ids=subnet_ids,
                          launch_specification=launch_specification)

    return compute


def get_strategy_object():
    strategy = aws.Strategy(utilize_reserved_instances=False,
                            fallback_to_od=True,
                            spot_percentage=100)

    return strategy


def get_capacity_object(minimum, maximum, target):
    if not isinstance(minimum, int):
        raise NonRecoverableError('Minimum is expected to be a integer')
    if not isinstance(maximum, int):
        raise NonRecoverableError('Maximum is expected to be a integer')
    if not isinstance(target, int):
        raise NonRecoverableError('Target is expected to be a integer')

    capacity = aws.Capacity(minimum=minimum, maximum=maximum, target=target)

    return capacity


def get_ocean_object(name, cluster_id, region, capacity, strategy, compute):
    if not isinstance(name, str):
        raise NonRecoverableError('Name is expected to be a string')
    if not isinstance(cluster_id, str):
        raise NonRecoverableError('Cluster ID is expected to be a string')
    if not isinstance(region, str):
        raise NonRecoverableError('Region is expected to be a string')

    ocean = aws.Ocean(name=name,
                      controller_cluster_id=cluster_id,
                      region=region,
                      capacity=capacity,
                      strategy=strategy,
                      compute=compute)
    return ocean
