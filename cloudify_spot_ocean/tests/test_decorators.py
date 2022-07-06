from mock import patch
from .. import utils
from .. import decorators


@decorators.with_spot_ocean
def fake_function(*args, **kwargs):
    return args, kwargs


@patch(utils.get_resource_config())
@patch(utils.get_client_config())
@patch(utils.get_client())
def test_decorator_stores_kwargs():
    args = []
    kwargs = {
        'ctx': 'ctx',
        'client_config': 'client_config',
        'resource_config': 'client_config'
    }

    def mock_get_resource_config():
        return "mock_get_resource_config"

    def mock_get_client_config():
        return "mock_get_client_config"

    def mock_get_client(client_config):
        return "mock_get_client"

    utils.resource_config = mock_get_resource_config
    utils.get_client_config = mock_get_client_config
    utils.get_client = mock_get_client

    response = fake_function(*args, **kwargs)
    assert response['resource_config'] == 'mock_get_resource_config'
    assert response['client_config'] == 'mock_get_client_config'
    assert response['ocean_client'] == 'mock_get_client'
