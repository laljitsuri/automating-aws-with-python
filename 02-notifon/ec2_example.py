import boto3

session = boto3.Session(profile_name='pythonAutomation')
ec2=session.resource('ec2')

img = ec2.Image('ami-020d764f9372da231')

img_name = img.name

ami_name = 'amzn-ami-hvm-2018.03.0.20200602.1-x86_64-gp2'

filters = [{'Name': 'name', 'Values': [ami_name]}]

list(ec2.images.filter(Owners=['amazon'], Filters=filters))

ec2_client = session.client('ec2')
key_pairs=ec2_client.describe_key_pairs()
key_pairs_list=key_pairs.get('KeyPairs')
key_rsa=None
for k in key_pairs_list:
    if k.get('KeyName') == 'id_rsa':
        key_rsa = k

instances = ec2.create_instances(ImageId=img.id,
                                MinCount=1,
                                MaxCount=1,
                                InstanceType='t2.micro',
                                KeyName='id_rsa'
                            )
inst = instances[0]
inst.wait_until_running()
inst.reload()
inst.public_dns_name
inst.security_groups

sg = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])
sg.authorize_ingress(IpPermissions=[{'FromPort':22,
                                    'ToPort':22,
                                    'IpProtocol':'TCP',
                                    'IpRanges':[{'CidrIp':'141.168.87.232/32'}]
                                }]
                    )

sg.authorize_ingress(IpPermissions=[{'FromPort':80,
                                    'ToPort':80,
                                    'IpProtocol':'TCP',
                                    'IpRanges':[{'CidrIp':'0.0.0.0/0'}]
                                }]
                    )

ssh ec2-user@ec2-13-211-159-125.ap-southeast-2.compute.amazonaws.com
sudo yum -y update
sudo yum -y install httpd
sudo chkconfig httpd on
sudo service httpd start
control-D

# Autoscaling commands
session = boto3.Session(profile_name='pythonAutomation')
as_client = session.client('autoscaling')
as_client.describe_auto_scaling_groups
as_client.describe_policies()
as_client.execute_policy(AutoScalingGroupName='Notifon Example Group', PolicyName='Scale Down')
as_client.execute_policy(AutoScalingGroupName='Notifon Example Group', PolicyName='Scale Up')
