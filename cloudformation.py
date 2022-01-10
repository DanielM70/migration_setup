from copy import Error
import botocore
import boto3
from utility import createSecurityGroup, getSubnetId


Account_ID = boto3.client('sts').get_caller_identity()['Account'] 
my_session = boto3.session.Session()
Region = my_session.region_name
#bucketName = Account_ID + '-migration'
solutionName = 'migrationFactory'       ## Replace with customer 3 letter acronym
version = '0.01'                        ## should be incremented by platform only
serviceAccountEmail = 'daniel.mulrooney@pivotree.com'

## Deploy CloudFormation

def deployMigrationFactoryCore(Account_ID, bucketName):


    # Grab security group ID

    sg_id = createSecurityGroup()
    sg_id=str(sg_id).split("'")[1]

    # Grab Subnet ID

    subnet_id = getSubnetId()

    ## Results if needed
    print(subnet_id)
    print(sg_id)

    client = boto3.client('cloudformation')
    stack_id = client.create_stack(
        StackName=solutionName + Account_ID,
        TemplateURL='https://' + bucketName + '-' + Region + '.s3.amazonaws.com/' + solutionName + '/' + version + '/aws-cloudendure-migration-factory-solution.template',
        Parameters=[
            {
                'ParameterKey': 'Application',
                'ParameterValue': 'cemf',
                'UsePreviousValue': False,
            },
            {
                'ParameterKey': 'Environment',
                'ParameterValue': 'prd',
                'UsePreviousValue': False,
            },
            {
                'ParameterKey': 'Tracker',
                'ParameterValue': 'false',
                'UsePreviousValue': False,
            },
            {
                'ParameterKey': 'ServiceAccountEmail',
                'ParameterValue': serviceAccountEmail,
                'UsePreviousValue': False,
            },
            {
                'ParameterKey': 'SecurityGroup',
                'ParameterValue': sg_id,
                'UsePreviousValue': False,
            },
            {
                'ParameterKey': 'SubnetId',
                'ParameterValue': subnet_id,
                'UsePreviousValue': False,
            },
        ],
        Capabilities=[
        'CAPABILITY_NAMED_IAM',
        ],
    OnFailure='DO_NOTHING',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'MigrationFactoryCore'
            },
        ],
    EnableTerminationProtection=False
    )

#    waiter = client.get_waiter('stack_create_complete')

#    try:

#        waiter.wait(
#        StackName=solutionName + Account_ID,
#        #NextToken='string',
#        WaiterConfig={
#        'Delay': 30,
#        'MaxAttempts': 120
#            }
#        )

    return stack_id['StackId']

#    except:
#        print(Error)



    
    
def deployMGN(Account_ID, bucketName):

    client = boto3.client('cloudformation')
    stack_id = client.create_stack(
        StackName='MGN' + solutionName + Account_ID,
        TemplateURL='https://' + bucketName + '-' + Region +  '.s3.amazonaws.com/' + solutionName + '/' + version + '/aws-cloudendure-migration-factory-solution-mgn-target-account.template',
        Parameters=[
            {
                'ParameterKey': 'FactoryAWSAccountId',
                'ParameterValue': Account_ID,
                'UsePreviousValue': False,
            },
        ],
        Capabilities=[
        'CAPABILITY_NAMED_IAM',
        ],
    OnFailure='DELETE',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'MGNMigrationFactoryCFN'
            },
        ],
    EnableTerminationProtection=False
    )

    return stack_id['StackId']


