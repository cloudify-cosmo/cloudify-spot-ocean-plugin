from cloudify.exceptions import NonRecoverableError
import unittest
from . import mock_context
from .. import utils


def test_get_resource_config():
    mock_context(test_name="test_decorator_stores_kwargs",
                 test_node_id="test_decorator_stores_kwargs",
                 test_properties={
                     'client_config': {'spot_ocean_token': 'tok-1',
                                       'account_id': 'act-1'},
                     'resource_config':
                         {'resource_config': 'resource_config'}},
                 test_runtime_properties={})
    resource_config = utils.get_resource_config()
    assert resource_config == {'resource_config': 'resource_config'}


def test_get_client_config():
    mock_context(test_name="test_decorator_stores_kwargs",
                 test_node_id="test_decorator_stores_kwargs",
                 test_properties={
                     'client_config': {'spot_ocean_token': 'tok-1',
                                       'account_id': 'act-1'},
                     'resource_config':
                         {'resource_config': 'resource_config'}},
                 test_runtime_properties={})
    client_config = utils.get_client_config()
    assert client_config == {'spot_ocean_token': 'tok-1',
                             'account_id': 'act-1'}


class MyTestCase(unittest.TestCase):
    def test_validate_resource_config(self):
        a = {'foo': "bar", 'gpp': 'nar', 'buz': 'zun'}
        b = {'foo': "bar", 'gpp': 'nar', 'buz': 'zun'}
        c = {'foo': "bar", 'buz': 'zun'}

        assert utils.validate_resource(a, b, 'test')
        assert utils.validate_resource(b, c, 'test')
        with self.assertRaises(NonRecoverableError):
            utils.validate_resource(c, b, 'test')
