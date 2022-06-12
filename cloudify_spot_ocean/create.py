from spotinst_sdk2 import SpotinstSession
from spotinst_sdk2.models.ocean import aws

# Cloudify
from cloudify import ctx


def create():

    session = \
        SpotinstSession(auth_token=ctx.instance.runtime_properties[
            "SpotOceanToken"],
                        account_id=ctx.instance.runtime_properties[
            "AccountID"])
    client = session.client("ocean_aws")

    ################ Compute ################
    launch_specification = aws.LaunchSpecifications(
        security_group_ids=ctx.instance.runtime_properties[
            "security_group_ids"],
        image_id=ctx.instance.runtime_properties["image_id"],
        key_pair=ctx.instance.runtime_properties["key_pair"])

    instance_types = aws.InstanceTypes(whitelist=[
        ctx.instance.runtime_properties["instance_types"]])

    compute = aws.Compute(instance_types=instance_types,
                          subnet_ids=ctx.instance.runtime_properties[
                              "subnet_ids"],
                          launch_specification=launch_specification)

    ################ Strategy ################

    strategy = aws.Strategy(utilize_reserved_instances=False,
                            fallback_to_od=True,
                            spot_percentage=100)

    ################ Capacity ################

    capacity = aws.Capacity(minimum=1, maximum=4, target=1)

    ################# Ocean #################

    ocean = aws.Ocean(name="Ocean SDK Test",
                      controller_cluster_id=ctx.instance.runtime_properties[
                          "ocean_cluster_name"],
                      region="us-east-1",
                      capacity=capacity,
                      strategy=strategy,
                      compute=compute)

    create_response = client.create_ocean_cluster(ocean=ocean)
    instance_id = create_response["id"]
    ctx.instance.runtime_properties["create_response"] = create_response
    ctx.instance.runtime_properties["instance_id"] = instance_id


if __name__ == '__main__':
  create(token=token, account=account, args=args)




##############
#{'id': 'o-aad830c0', 'name': 'Ocean SDK Test', 'controller_cluster_id': 'ocean-first', 'region': 'us-east-1', 'capacity': {'minimum': 1, 'maximum': 10, 'target': 3}, 'strategy': {'utilize_reserved_instances': False, 'fallback_to_od': True, 'spot_percentage': 100}, 'compute': {'subnet_ids': ['subnet-0caada3ee8345a85d', 'subnet-06e1e5beb06deae56', 'subnet-0ab4fd9c07de827c0', 'subnet-09c623b7fea384277'], 'instance_types': {'whitelist': ['t3.medium']}, 'launch_specification': {'security_group_ids': ['sg-09e787ee93e8494e2'], 'key_pair': 'eks_keyocean-first', 'image_id': 'ami-0319c884da18af515', 'user_data': '__hidden__'}}, 'created_at': '2022-04-18T11:28:44.013Z', 'updated_at': '2022-04-18T11:28:44.013Z'}
##################
