from mock import patch
from .. import decorators
from . import mock_context


@decorators.with_spot_ocean
def fake_function(*args, **kwargs):
    return args, kwargs


@patch('cloudify_spot_ocean.utils.get_resource_config',
       return_value='mock_get_resource_config')
@patch('cloudify_spot_ocean.utils.get_client_config',
       return_value='mock_get_client_config')
@patch('cloudify_spot_ocean.utils.get_client', return_value='mock_get_client')
def test_decorator_stores_kwargs(*_):
    args = []
    kwargs = {
        'ctx': mock_context(test_name="test_decorator_stores_kwargs",
                            test_node_id="test_decorator_stores_kwargs",
                            test_properties={
                                'client_config': {'spot_ocean_token': 'tok-1',
                                                  'account_id': 'act-1'},
                                'resource_config':
                                    {'resource_config': 'resource_config'}},
                            test_runtime_properties={})
    }

    _, response = fake_function(*args, **kwargs)
    print("response = {}".format(response))
    print(response['ocean_client'])
    assert response['resource_config'] == 'mock_get_resource_config'
    assert response['client_config'] == 'mock_get_client_config'
    assert response['ocean_client'] == 'mock_get_client'
