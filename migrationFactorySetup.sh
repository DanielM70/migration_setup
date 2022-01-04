import boto3

## List of IAM users to create
## This will create user, assign associated policy, create a secret/key

users = {
    1: {'name': 'discovery', 'boundary': 'arn:aws:iam::aws:policy/AWSApplicationDiscoveryAgentAccess'}, 
    2: {'name': 'migration', 'boundary': 'arn:aws:iam::aws:policy/AWSApplicationMigrationAgentPolicy'}
}


for id, info in users.items():
    
    print("\nUser_ID:", id, info)

    client = boto3.client('iam')
    
    client.create_user(
        UserName = users[id]['name'],
        PermissionsBoundary = users[id]['boundary'],
        Tags=[
            {
                'Key': 'Purpose',
                'Value': 'MigrationProcess'
            }
        ]
    )
    

    data = client.create_access_key(
    UserName=users[id]['name']
    )

    print('++++++++++++++++++')
    print(users[id]['name'], 'created')
    print(data['AccessKey']['UserName'])
    print(data['AccessKey']['AccessKeyId'])
    print(data['AccessKey']['SecretAccessKey'])

    ## Create S3 bucket 