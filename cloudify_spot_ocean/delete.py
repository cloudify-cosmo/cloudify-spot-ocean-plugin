from spotinst_sdk2 import SpotinstSession
from spotinst_sdk2.models.ocean import aws

def delete(token=None, account=None, ocean_cluster_id=None):
	session = \
		SpotinstSession(auth_token=ctx.instance.runtime_properties[
			"SpotOceanToken"],
						account_id=ctx.instance.runtime_properties[
							"AccountID"])
	client = session.client("ocean_aws")
	
	return client.delete_ocean_cluster(ocean_cluster_id)