import sys

from functools import wraps
from cloudify.utils import exception_to_error_cause
from cloudify.exceptions import NonRecoverableError
from spotinst_sdk2.client import SpotinstClientException

from . import utils


def with_spot_ocean(func):
    @wraps(func)
    def f(*args, **kwargs):
        ctx = kwargs['ctx']
        client_config = utils.get_client_config()
        resource_config = utils.get_resource_config()
        ocean_client = utils.get_client(client_config)
        kwargs['ocean_client'] = ocean_client
        kwargs['client_config'] = client_config
        kwargs['resource_config'] = resource_config
        try:
            return func(*args, **kwargs)
        except SpotinstClientException as ex:
            _, _, tb = sys.exc_info()
            ctx.logger.error(str(exception_to_error_cause(ex, tb)))
            if hasattr(ex, 'message'):
                ctx.logger.error('The message: {}'.format(ex.message))
            raise NonRecoverableError(
                "Spot Ocean operation failed",
                causes=[exception_to_error_cause(ex, tb)])
    return f
