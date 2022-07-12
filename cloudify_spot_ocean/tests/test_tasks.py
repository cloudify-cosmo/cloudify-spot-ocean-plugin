import unittest
from mock import patch
from . import mock_context
from .. import tasks

CREATE_RESPONSE = {'id': 'o-35d60931',
                   'name': 'yk1',
                   'controller_cluster_id': 'yk2',
                   'region': 'eu-west-1',
                   'capacity': {'minimum': 1, 'maximum': 1, 'target': 1},
                   'strategy': {'utilize_reserved_instances': False,
                                'fallback_to_od': True,
                                'spot_percentage': 100},
                   'compute': {'subnet_ids': ['subnet-0b0d6c38f4d2ff972',
                                              'subnet-0441be5f6161319f3',
                                              'subnet-0f3faf2a3ce910365',
                                              'subnet-08d5006293c6c030c'],
                               'instance_types': {'whitelist': ['t3.medium']},
                               'launch_specification': {
                                   'security_group_ids': [
                                       'sg-0272674406732d957'],
                                   'key_pair': 'eks_keyyk2'}},
                   'created_at': '2022-07-10T14:44:52.000Z',
                   'updated_at': '2022-07-10T14:44:52.000Z'}

DESCRIBE_RESPONSE = [CREATE_RESPONSE]


class TestTasks(unittest.TestCase):
    def test_create(self, *_, **__):
        ctx = mock_context(test_name="test_decorator_stores_kwargs",
                           test_node_id="test_decorator_stores_kwargs",
                           test_properties={
                               'client_config': {'spot_ocean_token': 'tok-1',
                                                 'account_id': 'act-1'},
                               'resource_config':
                                   {"resource_config": "resource_config",
                                    "SecurityGroupIds": ["sg-1"],
                                    "ImageId": "ami-3",
                                    "KeyPair": "key-p",
                                    "InstanceTypes": "t3.m",
                                    "SubnetIds": ["sub"],
                                    "MinCapacity": 1,
                                    "MaxCapacity": 1,
                                    "TargetCapacity": 1,
                                    "OceanClusterName": "yk1",
                                    "ClusterId": "yk2",
                                    "Region": "us-west-east-72"}},
                           test_runtime_properties={})

        resource_config = {"resource_config": "resource_config",
                           "SecurityGroupIds": ["sg-1"],
                           "ImageId": "ami-3",
                           "KeyPair": "key-p",
                           "InstanceTypes": "t3.m",
                           "SubnetIds": ["sub"],
                           "MinCapacity": 1,
                           "MaxCapacity": 1,
                           "TargetCapacity": 1,
                           "OceanClusterName": "OceanClusterName",
                           "ClusterId": "ClusterId",
                           "Region": "us-west-east-72"}

        with patch('cloudify_spot_ocean.utils.get_client') as ocean_client:
            ocean_client().create_ocean_cluster.return_value = CREATE_RESPONSE
            ocean_client().get_all_ocean_cluster.return_value = \
                DESCRIBE_RESPONSE

            create_response = tasks.create(
                ctx=ctx, resource_config=resource_config)
            assert create_response == CREATE_RESPONSE

    def test_delete(self, *_, **__):
        ctx = mock_context(test_name="test_decorator_stores_kwargs",
                           test_node_id="test_decorator_stores_kwargs",
                           test_properties={},
                           test_runtime_properties={
                               'instance_id': 'o-35d60931'})
        with patch('cloudify_spot_ocean.utils.get_client') as ocean_client:
            ocean_client().create_ocean_cluster.return_value = None
            ocean_client().get_ocean_cluster.side_effect = [True, None]
            assert not tasks.delete(ctx=ctx, ocean_client=ocean_client)

    def test_describe(self, *_, **__):
        ctx = mock_context(test_name="test_decorator_stores_kwargs",
                           test_node_id="test_decorator_stores_kwargs",
                           test_properties={},
                           test_runtime_properties={
                               'instance_id': 'o-35d60931'})
        with patch('cloudify_spot_ocean.utils.get_client') as ocean_client:
            ocean_client.get_ocean_cluster.return_value = CREATE_RESPONSE
            response = tasks.describe(ocean_client=ocean_client, ctx=ctx)
            assert response == CREATE_RESPONSE

    def test_describe_all(self, *_, **__):
        with patch('cloudify_spot_ocean.utils.get_client') as ocean_client:
            ocean_client.get_all_ocean_cluster.return_value = \
                DESCRIBE_RESPONSE
            response = tasks.describe_all(ocean_client=ocean_client)
            assert response == DESCRIBE_RESPONSE
