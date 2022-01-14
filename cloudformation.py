from copy import Error
import botocore
import boto3
import properties
from utility import createSecurityGroup, getSubnetId
from parameters import putParameter, getParameter



## Deploy CloudFormation

def deployMigrationFactoryCore(Account_ID, bucketName):

    # Check Region

   #Region=getParameter('Region')

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
        StackName=properties.solutionName + Account_ID,
        TemplateURL='https://' + bucketName + '-' + getParameter('Region') + '.s3.amazonaws.com/' + properties.solutionName + '/' + properties.version + '/aws-cloudendure-migration-factory-solution.template',
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
                'ParameterValue': properties.serviceAccountEmail,
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

    waiter = client.get_waiter('stack_create_complete')
    print("...waiting for stack to be ready...")
    waiter.wait(StackName=properties.solutionName + Account_ID)

    return stack_id['StackId']

#    except:
#        print(Error)



## This will be used when deploying to a separate account than where Migration Factory exists 
## possible we deploy Migration Factory to lower env, and need to deploy this to higher env  
    
def deployMGN(Account_ID, bucketName):

    client = boto3.client('cloudformation')
    stack_id = client.create_stack(
        StackName='MGN' + properties.solutionName + Account_ID,
        TemplateURL='https://' + bucketName + '-' + getParameter('Region') +  '.s3.amazonaws.com/' + properties.solutionName + '/' + properties.version + '/aws-cloudendure-migration-factory-solution-mgn-target-account.template',
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


## Push all CloudFormation Outputs to Parameter store

def pushOutputs(stackId):
    client = boto3.client('cloudformation')
    outputs = client.describe_stacks(
        StackName = stackId
    )

    # To Do: Figure out how to generate this 
    keyNames = ['MigrationFactoryURL', 'UserPoolId', 'ExecutionServerIAMRole', 'ExecutionServerIAMPolicy', 'ToolsAPI', 'LoginAPI', 'LoginAPI URL', 'AdminAPI']

    outputKeys=outputs['Stacks'][0]['Outputs']

    for keyName in keyNames: 
        for outputkey in outputKeys:
            listKeyName=outputkey['OutputKey']
            if listKeyName == keyName:
                print(keyName + '=' + outputkey['OutputValue'])
                putParameter(keyName, outputkey['OutputValue'], 'false')