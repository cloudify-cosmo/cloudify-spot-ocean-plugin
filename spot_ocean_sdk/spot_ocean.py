from spotinst_sdk2.models.ocean import aws


def get_launch_specification_object(security_group_ids, image_id, key_pair):
    launch_specification = aws.LaunchSpecifications(
        security_group_ids=security_group_ids,
        image_id=image_id,
        key_pair=key_pair)

    return launch_specification


def get_instance_types_object(instance_types):
    instance_types = aws.InstanceTypes(whitelist=[instance_types])

    return instance_types


def get_compute_object(instance_types, subnet_ids, launch_specification):
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
    capacity = aws.Capacity(minimum=minimum, maximum=maximum, target=target)

    return capacity


def get_ocean_object(name, cluster_id, region, capacity, strategy, compute):
    ocean = aws.Ocean(name=name,
                      controller_cluster_id=cluster_id,
                      region=region,
                      capacity=capacity,
                      strategy=strategy,
                      compute=compute)
    return ocean
