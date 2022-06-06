from spotinst_sdk2 import SpotinstSession
from spotinst_sdk2.models.ocean import aws


def create(token=None, account=None, **args):
  session = SpotinstSession(auth_token=token, account_id=account)
  client = session.client("ocean_aws")
  
  args = args["args"]

  ################ Compute ################
  launch_specification = aws.LaunchSpecifications(
    security_group_ids=args["security_group_ids"],
    image_id=args["image_id"], 
    key_pair=args["key_pair"])

  instance_types = aws.InstanceTypes(whitelist=[args["instance_types"]])

  compute = aws.Compute(instance_types=instance_types, 
                        subnet_ids=args["subnet_ids"], 
                        launch_specification=launch_specification)

  ################ Strategy ################

  strategy = aws.Strategy(utilize_reserved_instances=False, 
                          fallback_to_od=True, 
                          spot_percentage=100)

  ################ Capacity ################

  capacity = aws.Capacity(minimum=1, maximum=10, target=3)

  ################# Ocean #################

  ocean = aws.Ocean(name="Ocean SDK Test", 
                    controller_cluster_id=args["ocean_cluster_name"], 
                    region="us-east-1", 
                    capacity=capacity, 
                    strategy=strategy, 
                    compute=compute)



  return client.create_ocean_cluster(ocean=ocean)

if __name__ == '__main__':
  create(token=token,account=account,args=args)




##############
#{'id': 'o-aad830c0', 'name': 'Ocean SDK Test', 'controller_cluster_id': 'ocean-first', 'region': 'us-east-1', 'capacity': {'minimum': 1, 'maximum': 10, 'target': 3}, 'strategy': {'utilize_reserved_instances': False, 'fallback_to_od': True, 'spot_percentage': 100}, 'compute': {'subnet_ids': ['subnet-0caada3ee8345a85d', 'subnet-06e1e5beb06deae56', 'subnet-0ab4fd9c07de827c0', 'subnet-09c623b7fea384277'], 'instance_types': {'whitelist': ['t3.medium']}, 'launch_specification': {'security_group_ids': ['sg-09e787ee93e8494e2'], 'key_pair': 'eks_keyocean-first', 'image_id': 'ami-0319c884da18af515', 'user_data': '__hidden__'}}, 'created_at': '2022-04-18T11:28:44.013Z', 'updated_at': '2022-04-18T11:28:44.013Z'}
##################
