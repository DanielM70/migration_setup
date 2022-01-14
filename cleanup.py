from boto3.resources.model import Waiter
import botocore
import boto3
import subprocess
import compare
from parameters import removeParameter, getParameter, removeParameters

Account_ID = boto3.client('sts').get_caller_identity()['Account'] 

rootPath = '/Users/daniel.mulrooney/workspaces/migration_setup/'
checkoutFolder = 'migrationFactory'
my_session = boto3.session.Session()
Region = my_session.region_name


users = {
    1: {'name': 'discovery', 'boundary': 'arn:aws:iam::aws:policy/AWSApplicationDiscoveryAgentAccess'}, 
    2: {'name': 'migration', 'boundary': 'arn:aws:iam::aws:policy/AWSApplicationMigrationAgentPolicy'}
}

## Clean up s3 bucket

def cleanUpBucket():

    #
    buckets =  Account_ID+'-migration'+'-'+Region,'cemf-prd-712056642930-access-logs', 'cemf-prd-712056642930-front-end'

    for bucketName in buckets:


        print(bucketName)
        s3_resource = boto3.resource('s3')

        # check to see if bucket exists
        # if bucket exists proceed

        if s3_resource.Bucket(bucketName).creation_date is None: 
            print('Bucket already deleted' + bucketName)
            continue


        try: 
            res = []

            response_list=bucket=s3_resource.Bucket(bucketName)
            for obj_version in bucket.object_versions.all():
                res.append({'Key': obj_version.object_key,
                            'VersionId': obj_version.id})
            #print(res) 
            
            if bool(res):
                try:
                    response_delete=(bucket.delete_objects(Delete={'Objects': res}))
                except:
                    print('Delete error', response_delete)
            else:
                print('List is empty moving on')
        except:
            print('Something went wrong')
            

        # if bucket exists delete
        # otherwise continue lopp 

        try:
            response_delete_bucket=client = boto3.client('s3')
            client.delete_bucket(
                Bucket = bucketName,
            )
        except:
            print('Bucket error', response_delete_bucket)
            continue



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

#            removeParameter(key_id['AccessKeyMetadata'][0]['UserName'] + '/AccessKeyId')
#            removeParameter(key_id['AccessKeyMetadata'][0]['UserName'] + '/SecretAccessKey')

        except botocore.exceptions.ClientError as error:

            if error.response['Error']['Code'] == 'NoSuchEntity':
                print('No such user')
                continue 
        
def cleanupSecurityGroup():

    client = boto3.client('ec2')

    try:

        sg_id = client.describe_security_groups(
            GroupNames=[
            'mfsg',
            ],
        )
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidGroup.NotFound':
            print('No SG exists ')

    else:
        response = client.delete_security_group(GroupId=sg_id['SecurityGroups'][0]['GroupId'])
        print(response)


## Add Remove Functions as needed

print('Deleting migrationFactory folder')
delcmd = 'rm -rf migrationFactory'
subprocess.check_call([delcmd], shell=True, cwd=rootPath)

def cleanupCloudFormation():

    stackName='migrationFactory'+Account_ID

    client = boto3.client('cloudformation')

    response = client.delete_stack(
        StackName=stackName
    )
    print(response)


def cleanupUserPool():

    client = boto3.client('cognito-idp')

    response = client.delete_user_pool(
        UserPoolId=getParameter('UserPoolId')
    )

    print(response)



removeIAMusers()
cleanupSecurityGroup()
cleanUpBucket()
cleanupCloudFormation()
#cleanupUserPool()
removeParameters()
