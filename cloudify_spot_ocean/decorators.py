from functools import wraps
from . import utils


def with_spot_ocean(func):
    @wraps(func)
    def f(*args, **kwargs):
        client_config = utils.get_client_config()
        resource_config = utils.get_resource_config()
        ocean_client = utils.get_client(client_config)
        kwargs['ocean_client'] = ocean_client
        kwargs['client_config'] = client_config
        kwargs['resource_config'] = resource_config
        return func(*args,
                    **kwargs)
    return f
