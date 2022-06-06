from spotinst_sdk2 import SpotinstSession
from spotinst_sdk2.models.ocean import aws

def describe_all(token=None, account=None):
	session = SpotinstSession(auth_token=token, account_id=account)
	client = session.client("ocean_aws")

	return client.get_all_ocean_cluster()