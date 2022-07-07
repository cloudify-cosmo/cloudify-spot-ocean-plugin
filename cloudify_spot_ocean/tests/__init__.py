from cloudify.state import current_ctx
from cloudify.mocks import MockCloudifyContext, MockNodeInstanceContext


def mock_context(test_name,
                 test_node_id,
                 test_properties,
                 test_runtime_properties):

    ctx = MockCloudifyContext(
        node_id=test_node_id,
        properties=test_properties,
        runtime_properties=None if not test_runtime_properties
        else test_runtime_properties,
        deployment_id=test_name
    )
    ctx._instance = MockNodeInstanceContext(
        ctx._instance.id,
        ctx._instance.runtime_properties,
        ctx._instance.relationships,
        ctx._instance.index
    )
    ctx._instance.type = 'node-instance'
    current_ctx.set(ctx=ctx)
    return ctx
