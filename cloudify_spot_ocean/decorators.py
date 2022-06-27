from functools import wraps
from . import utils


def with_spot_ocean(func):
    @wraps(func)
    def f(*args, **kwargs):
        ctx = kwargs.get('ctx')
        client_config = utils.get_client_config()
        resource_config = utils.get_resource_config()
        kwargs['client_config'] = client_config
        kwargs['resource_config'] = resource_config
        client = utils.get_client(client_config)
        return func(*args,
                    **kwargs,
                    client=client,
                    ctx=ctx,
                    resource_config=resource_config)
    return f
