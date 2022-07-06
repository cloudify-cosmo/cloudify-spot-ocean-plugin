from spot_ocean_sdk import spot_ocean
from mock import patch

from cloudify.exceptions import NonRecoverableError

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

    class MockCap(object):
        def __init__(self,
                     minimum,
                     maximum,
                     target):
            self.minimum = minimum
            self.maximum = maximum
            self.target = target
    spot_ocean_aws.Capacity = MockCap

    capacity = spot_ocean.get_capacity_object(
        minimum=RESOURCE_CONFIG.get('MinCapacity'),
        maximum=RESOURCE_CONFIG.get('MaxCapacity'),
        target=RESOURCE_CONFIG.get('TargetCapacity'))
    assert capacity.minimum == RESOURCE_CONFIG.get('MinCapacity')
    assert capacity.maximum == RESOURCE_CONFIG.get('MaxCapacity')
    assert capacity.target == RESOURCE_CONFIG.get('TargetCapacity')
    try:
        spot_ocean.get_capacity_object(33, 33, "t")
    except NonRecoverableError:
        pass
    try:
        spot_ocean.get_capacity_object(33, "t", 33)
    except NonRecoverableError:
        pass
    try:
        spot_ocean.get_capacity_object("t", 33, 33)
    except NonRecoverableError:
        pass


@patch('spot_ocean_sdk.spot_ocean.aws')
def test_get_instance_types_object(spot_ocean_aws, *_, **__):
    class MockIT(object):
        def __init__(self, whitelist):
            self.whitelist = whitelist

    spot_ocean_aws.InstanceTypes = MockIT
    instance_types = spot_ocean.get_instance_types_object(RESOURCE_CONFIG.get(
        'InstanceTypes'))
    assert instance_types.whitelist == [RESOURCE_CONFIG.get('InstanceTypes')]
    try:
        spot_ocean.get_instance_types_object(33)
    except NonRecoverableError:
        pass


@patch('spot_ocean_sdk.spot_ocean.aws')
def test_get_strategy_object(spot_ocean_aws, *_, **__):
    class MockS(object):
        def __init__(self,
                     utilize_reserved_instances,
                     fallback_to_od,
                     spot_percentage):
            self.utilize_reserved_instances = utilize_reserved_instances
            self.fallback_to_od = fallback_to_od
            self.spot_percentage = spot_percentage

    spot_ocean_aws.Strategy = MockS

    strategy = spot_ocean.get_strategy_object()

    assert not strategy.utilize_reserved_instances  # value is set to False
    assert strategy.fallback_to_od  # value is set to True
    assert strategy.spot_percentage == 100  # value is set to 100%


@patch('spot_ocean_sdk.spot_ocean.aws')
def test_get_launch_specification_object(spot_ocean_aws, *_, **__):
    class MockLS(object):
        def __init__(self, security_group_ids, image_id, key_pair):
            self.security_group_ids = security_group_ids
            self.image_id = image_id
            self.key_pair = key_pair

    spot_ocean_aws.LaunchSpecifications = MockLS

    launch_specification = spot_ocean.get_launch_specification_object(
        security_group_ids=RESOURCE_CONFIG.get('SecurityGroupIDs'),
        image_id=RESOURCE_CONFIG.get('ImageID'),
        key_pair=RESOURCE_CONFIG.get('KeyPair'))
    assert launch_specification.security_group_ids == \
           RESOURCE_CONFIG.get('SecurityGroupIDs')
    assert launch_specification.image_id == RESOURCE_CONFIG.get('ImageID')
    assert launch_specification.key_pair == RESOURCE_CONFIG.get('KeyPair')
    try:
        spot_ocean.get_launch_specification_object(33, "foo", "bar")
    except NonRecoverableError:
        pass
    try:
        spot_ocean.get_launch_specification_object([], 33, "bar")
    except NonRecoverableError:
        pass
    try:
        spot_ocean.get_launch_specification_object([], "foo", 33)
    except NonRecoverableError:
        pass


@patch('spot_ocean_sdk.spot_ocean.aws')
def test_get_compute_object(spot_ocean_aws, *_, **__):
    class MockComp(object):
        def __init__(self, instance_types, subnet_ids, launch_specification):
            self.instance_types = instance_types
            self.subnet_ids = subnet_ids
            self.launch_specification = launch_specification

    spot_ocean_aws.Compute = MockComp
    compute = spot_ocean.get_compute_object(
        instance_types=spot_ocean_aws.InstanceTypes,
        subnet_ids=RESOURCE_CONFIG.get('SubnetIDs'),
        launch_specification=spot_ocean_aws.LaunchSpecifications)
    assert compute.subnet_ids == RESOURCE_CONFIG.get('SubnetIDs')
    try:
        spot_ocean.get_compute_object("foo", [], "bar")
    except NonRecoverableError:
        pass


@patch('spot_ocean_sdk.spot_ocean.aws')
def test_get_ocean_object(spot_ocean_aws, *_, **__):
    class MockO(object):
        def __init__(self,
                     name,
                     controller_cluster_id,
                     region,
                     capacity,
                     strategy,
                     compute):
            self.name = name
            self.controller_cluster_id = controller_cluster_id
            self.region = region
            self.capacity = capacity
            self.strategy = strategy
            self.compute = compute

    spot_ocean_aws.Ocean = MockO
    ocean = spot_ocean.get_ocean_object(
        name=RESOURCE_CONFIG.get('OceanClusterName'),
        cluster_id=RESOURCE_CONFIG.get('ClusterID'),
        region=RESOURCE_CONFIG.get('Region'),
        capacity=spot_ocean_aws.Capacity,
        strategy=spot_ocean_aws.Strategy,
        compute=spot_ocean_aws.Compute)
    assert ocean.name == RESOURCE_CONFIG.get('OceanClusterName')
    assert ocean.controller_cluster_id == RESOURCE_CONFIG.get('ClusterID')
    assert ocean.region == RESOURCE_CONFIG.get('Region')
    try:
        spot_ocean.get_ocean_object(
            name=1,
            cluster_id=RESOURCE_CONFIG.get('ClusterID'),
            region=RESOURCE_CONFIG.get('Region'),
            capacity=spot_ocean_aws.Capacity,
            strategy=spot_ocean_aws.Strategy,
            compute=spot_ocean_aws.Compute)
    except NonRecoverableError:
        pass
    try:
        spot_ocean.get_ocean_object(
            name=RESOURCE_CONFIG.get('OceanClusterName'),
            cluster_id=2,
            region=RESOURCE_CONFIG.get('Region'),
            capacity=spot_ocean_aws.Capacity,
            strategy=spot_ocean_aws.Strategy,
            compute=spot_ocean_aws.Compute)
    except NonRecoverableError:
        pass
    try:
        spot_ocean.get_ocean_object(
            name=RESOURCE_CONFIG.get('OceanClusterName'),
            cluster_id=RESOURCE_CONFIG.get('ClusterID'),
            region=3,
            capacity=spot_ocean_aws.Capacity,
            strategy=spot_ocean_aws.Strategy,
            compute=spot_ocean_aws.Compute)
    except NonRecoverableError:
        pass
