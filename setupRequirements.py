import boto3
from parameters import putParameter
import properties




Account_ID = boto3.client('sts').get_caller_identity()['Account'] 
my_session = boto3.session.Session()
Region = my_session.region_name

## Figure out some parameters used throughout the application

putParameter('Account_ID', Account_ID, 'True')
putParameter('Region', Region, 'True')


## List of IAM users to create
## This will create user, assign associated policy, create a secret/key
## List of users is in properties.py file

def addIAMusers():
    for id, info in properties.iamUsers.items():
        
        print("\nUser_ID:", id, info)

        client = boto3.client('iam')
        
        client.create_user(
            UserName = properties.iamUsers[id]['name'],
            PermissionsBoundary = properties.iamUsers[id]['boundary'],
            Tags=[
                {
                    'Key': 'Purpose',
                    'Value': 'MigrationProcess'
                }
            ]
        )
        

        data = client.create_access_key(
        UserName=properties.iamUsers[id]['name']
        )

        #putParameter( Account_ID, 'UserName', data['AccessKey']['UserName'], 'false')
        putParameter(data['AccessKey']['UserName'] + '/AccessKeyId', data['AccessKey']['AccessKeyId'], 'false')
        putParameter(data['AccessKey']['UserName'] + '/SecretAccessKey', data['AccessKey']['SecretAccessKey'], 'True')

        print('++++++++++++++++++')
        print(properties.iamUsers[id]['name'], 'created')
        print(data['AccessKey']['UserName'])
        print(data['AccessKey']['AccessKeyId'])
        print(data['AccessKey']['SecretAccessKey'])


## Create S3 bucket 
## This bucket is where CFN and lambda functions are uploaded for setup process
## Bucket has region code so lamda will work (DO NOT CHANGE it will break stuff)
## Bucket has public ACL due to lambda deploy (DO NOT change it will break stuff)
## Nothing confidential is included in this bucket

def createS3bucket():

    client = boto3.client('s3')

    bucket_name = {
        client.create_bucket(
            ACL='public-read',
            Bucket = Account_ID + '-migration' + '-' + Region,
        )
    }
    print(bucket_name)
    putParameter('Bucket_Name', bucket_name, 'false')


addIAMusers()
createS3bucket()