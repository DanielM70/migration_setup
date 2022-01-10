import boto3
## Add various functions here

def createSecurityGroup():

    client = boto3.client('ec2')
    res = client.describe_vpcs(Filters=[{'Name':'isDefault','Values': ['true']},]) 
    vpc_id = res['Vpcs'][0]['VpcId']

    ec2 = boto3.resource('ec2')
    vpc = ec2.Vpc(vpc_id)

    security_group = vpc.create_security_group(
        Description='Migration Factory Security Group',
        GroupName='mfsg',
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'MigrationFactory'
                    },
                ]
            },
        ],
    )

    # ec2.SecurityGroup(id='sg-0489ff5914efb4871')

    return(security_group)

def getSubnetId():

    client = boto3.client('ec2')
    res = client.describe_vpcs(Filters=[{'Name':'isDefault','Values': ['true']},]) 
    vpc_id = res['Vpcs'][0]['VpcId']

    subnet_id = client.describe_subnets(
        Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_id,
                    ]
                },
            ],
        )

    sub_id = subnet_id['Subnets'][1]['SubnetId']
    return sub_id


## The following function does not work, was replaced with upload.sh
## to do: need to figure out how to apply ACL
## to do: fix path to upload to version and remove global/regional-s3-assets folder name

def uploadFiles():
    path = ["migrationFactory/deployment/global-s3-assets", "migrationFactory/deployment/regional-s3-assets"] 

    for p in path:

        for root,dirs,files in os.walk(p):
            
            for file in files:

                client = boto3.client('s3')

                p1=p.split('/')[2]

                client.upload_file(os.path.join(root, file), bucketName , solutionName+'/'+version+'/'+p1+'/'+file)

                print(p1+'/'+file, 'uploaded')
