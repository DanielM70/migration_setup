import botocore
import boto3
from parameters import removeParameter


users = {
    1: {'name': 'discovery', 'boundary': 'arn:aws:iam::aws:policy/AWSApplicationDiscoveryAgentAccess'}, 
    2: {'name': 'migration', 'boundary': 'arn:aws:iam::aws:policy/AWSApplicationMigrationAgentPolicy'}
}

Account_ID = boto3.client('sts').get_caller_identity()['Account'] 

## Clean up s3 bucket

def cleanUpBucket():

    client = boto3.client('s3')

    client.delete_bucket(
        Bucket = Account_ID + '-migrationfactory',
    )



## Clean up User Keys, then Users

def removeIAMusers():

    for id, info in users.items():
        
        print("\nUser_ID:", id)

        client = boto3.client('iam')
        
        ## Query for access key ID

        try:
            
            client.get_user(UserName = users[id]['name'])

            key_id = client.list_access_keys(
            UserName = users[id]['name']
            )

            print(key_id['AccessKeyMetadata'][0]['UserName'])
            print(key_id['AccessKeyMetadata'][0]['AccessKeyId'])

            
            ## Delete Access key
            
            client.delete_access_key(
                UserName = key_id['AccessKeyMetadata'][0]['UserName'], 
                AccessKeyId = key_id['AccessKeyMetadata'][0]['AccessKeyId']
            )

            ## Delete User

            client.delete_user(
                UserName = key_id['AccessKeyMetadata'][0]['UserName']
            )

            removeParameter( Account_ID, key_id['AccessKeyMetadata'][0]['UserName'] + '/AccessKeyId')
            removeParameter( Account_ID, key_id['AccessKeyMetadata'][0]['UserName'] + '/SecretAccessKey')

        except botocore.exceptions.ClientError as error:

            if error.response['Error']['Code'] == 'NoSuchEntity':
                print('No such user')
                continue 
        #continue
        



## Add Remove Functions as needed

cleanUpBucket()
removeIAMusers()