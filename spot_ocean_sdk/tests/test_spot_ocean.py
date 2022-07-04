from spot_ocean_sdk import spot_ocean
from mock import Mock, patch
from spotinst_sdk2.models.ocean import aws

RESOURCE_CONFIG = {
	'InstanceTypes': 't3.medium',
    'OceanClusterName': None,
    'ClusterID': None,
    'Region':  None,
    'SecurityGroupIDs': None,
    'ImageID': None,
    'KeyPair': None,
    'SubnetIDs': None,
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
    # spot_ocean_aws.InstanceTypes = Mock()
    spot_ocean_aws.InstanceTypes = aws.InstanceTypes(whitelist=[
        RESOURCE_CONFIG.get('InstanceTypes')])
    print(spot_ocean_aws.InstanceTypes)
    # spot_ocean_aws.InstanceTypes.client = Mock()
    instance_types = spot_ocean.get_instance_types_object(RESOURCE_CONFIG.get(
        'InstanceTypes'))
    print(instance_types)
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


