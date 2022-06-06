from spotinst_sdk2 import SpotinstSession
from spotinst_sdk2.models.ocean import aws

def describe(token=None, account=None, ocean_cluster_id=None):
	session = SpotinstSession(auth_token=token, account_id=account)
	client = session.client("ocean_aws")

	return client.get_ocean_cluster(ocean_cluster_id)