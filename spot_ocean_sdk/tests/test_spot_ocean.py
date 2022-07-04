from spot_ocean_sdk import spot_ocean
from mock import Mock, patch
from spotinst_sdk2.models.ocean import aws

RESOURCE_CONFIG = {
    'InstanceTypes': 't3.medium',
    'OceanClusterName': 'eks-name',
    'ClusterID': 'cluster-1111',
    'Region': 'us-west-1',
    'SecurityGroupIDs': ['sg-1'],
    'ImageID': 'ami-1',
    'KeyPair': 'keypair',
    'SubnetIDs': ['subnet-1'],
    'MinCapacity': 1,
    'MaxCapacity': 1,
    'TargetCapacity': 1
}


@patch('spot_ocean_sdk.spot_ocean.aws')
def test_get_capacity_object(spot_ocean_aws, *_, **__):
    min = RESOURCE_CONFIG.get('MinCapacity')
    max = RESOURCE_CONFIG.get('MaxCapacity')
    target = RESOURCE_CONFIG.get('TargetCapacity')
    spot_ocean_aws.Capacity = aws.Capacity(minimum=min,
                                           maximum=max,
                                           target=target)

    capacity = spot_ocean.get_capacity_object(minimum=min,
                                              maximum=max,
                                              target=target)
    assert capacity.minimum == spot_ocean_aws.Capacity.minimum
    assert capacity.maximum == spot_ocean_aws.Capacity.maximum
    assert capacity.target == spot_ocean_aws.Capacity.target


@patch('spot_ocean_sdk.spot_ocean.aws')
def test_get_instance_types_object(spot_ocean_aws, *_, **__):
    spot_ocean_aws.InstanceTypes = aws.InstanceTypes(whitelist=[
        RESOURCE_CONFIG.get('InstanceTypes')])
    instance_types = spot_ocean.get_instance_types_object(RESOURCE_CONFIG.get(
        'InstanceTypes'))
    assert instance_types.whitelist == spot_ocean_aws.InstanceTypes.whitelist
    assert instance_types.blacklist == spot_ocean_aws.InstanceTypes.blacklist


@patch('spot_ocean_sdk.spot_ocean.aws')
def test_get_strategy_object(spot_ocean_aws, *_, **__):
    spot_ocean_aws.Strategy = aws.Strategy(
        utilize_reserved_instances=False,
        fallback_to_od=True,
        spot_percentage=100)
    print(spot_ocean_aws.Strategy)

    strategy = spot_ocean.get_strategy_object()
    print(strategy)
    assert strategy.utilize_reserved_instances == \
           spot_ocean_aws.Strategy.utilize_reserved_instances
    assert strategy.fallback_to_od == spot_ocean_aws.Strategy.fallback_to_od
    assert strategy.spot_percentage == spot_ocean_aws.Strategy.spot_percentage


@patch('spot_ocean_sdk.spot_ocean.aws')
def test_get_launch_specification_object(spot_ocean_aws, *_, **__):
    spot_ocean_aws.LaunchSpecifications = aws.LaunchSpecifications(
        security_group_ids=RESOURCE_CONFIG.get('SecurityGroupIDs'),
        image_id=RESOURCE_CONFIG.get('ImageID'),
        key_pair=RESOURCE_CONFIG.get('KeyPair'))
    launch_specification = spot_ocean.get_launch_specification_object(
        security_group_ids=RESOURCE_CONFIG.get('SecurityGroupIDs'),
        image_id=RESOURCE_CONFIG.get('ImageID'),
        key_pair=RESOURCE_CONFIG.get('KeyPair'))
    assert launch_specification.security_group_ids == \
           spot_ocean_aws.LaunchSpecifications.security_group_ids
    assert launch_specification.image_id == \
           spot_ocean_aws.LaunchSpecifications.image_id
    assert launch_specification.key_pair == \
           spot_ocean_aws.LaunchSpecifications.key_pair


def test_get_compute_object(spot_ocean_aws, *_, **__):
    spot_ocean_aws.Compute = aws.Compute(
        instance_types=spot_ocean_aws.InstanceTypes,
        subnet_ids=RESOURCE_CONFIG.get('SubnetIDs'),
        launch_specification=spot_ocean_aws.LaunchSpecifications)
    compute = spot_ocean.get_compute_object(
        instance_types=spot_ocean_aws.InstanceTypes,
        subnet_ids=RESOURCE_CONFIG.get('SubnetIDs'),
        launch_specification=spot_ocean_aws.LaunchSpecifications)
    assert compute.subnet_ids == spot_ocean_aws.Compute.subnet_ids


def test_get_ocean_object(spot_ocean_aws, *_, **__):
    spot_ocean_aws.Ocean = aws.Ocean(
        name=RESOURCE_CONFIG.get('OceanClusterName'),
        controller_cluster_id=RESOURCE_CONFIG.get('ClusterID'),
        region=RESOURCE_CONFIG.get('Region'),
        capacity=spot_ocean_aws.Capacity,
        strategy=spot_ocean_aws.Strategy,
        compute=spot_ocean_aws.Compute)
    ocean = spot_ocean.get_ocean_object(
        name=RESOURCE_CONFIG.get('OceanClusterName'),
        controller_cluster_id=RESOURCE_CONFIG.get('ClusterID'),
        region=RESOURCE_CONFIG.get('Region'),
        capacity=spot_ocean_aws.Capacity,
        strategy=spot_ocean_aws.Strategy,
        compute=spot_ocean_aws.Compute)
    assert ocean.name == spot_ocean_aws.Ocean.name
    assert ocean.controller_cluster_id == \
           spot_ocean_aws.Ocean.controller_cluster_id
    assert ocean.region == spot_ocean_aws.Ocean.region

