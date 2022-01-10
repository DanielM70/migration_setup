import boto3
from parameters import putParameter

## List of IAM users to create
## This will create user, assign associated policy, create a secret/key

users = {
    1: {'name': 'discovery', 'boundary': 'arn:aws:iam::aws:policy/AWSApplicationDiscoveryAgentAccess'}, 
    2: {'name': 'migration', 'boundary': 'arn:aws:iam::aws:policy/AWSApplicationMigrationAgentPolicy'}
}

Account_ID = boto3.client('sts').get_caller_identity()['Account'] 
my_session = boto3.session.Session()
Region = my_session.region_name


def addIAMusers():
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

        #putParameter( Account_ID, 'UserName', data['AccessKey']['UserName'], 'false')
        putParameter(Account_ID, data['AccessKey']['UserName'] + '/AccessKeyId', data['AccessKey']['AccessKeyId'], 'false')
        putParameter(Account_ID, data['AccessKey']['UserName'] + '/SecretAccessKey', data['AccessKey']['SecretAccessKey'], 'True')

        print('++++++++++++++++++')
        print(users[id]['name'], 'created')
        print(data['AccessKey']['UserName'])
        print(data['AccessKey']['AccessKeyId'])
        print(data['AccessKey']['SecretAccessKey'])


## Create S3 bucket 

def createS3bucket():

    client = boto3.client('s3')

    bucket_name = {
        client.create_bucket(
            ACL='public-read',
            Bucket = Account_ID + '-migration' + '-' + Region,
        )
    }
    putParameter(Account_ID, 'Bucket_Name', bucket_name, 'false')


addIAMusers()
createS3bucket()