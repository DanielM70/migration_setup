import boto3
import sys
import datetime
import json
from json import JSONEncoder

## Various functions to manage add/remove and getting of parameters from SSM parameter store

def putParameter(key, value, secure):

    if secure == True:
        typestring = 'SecureString'
    else:
        typestring = 'String'

    client = boto3.client('ssm')

    response = client.put_parameter(
        Name = '/migrationFactory/' + key,
        Description = 'Migration Factory Setting',
        Value = value,
        Type=typestring,
        #Overwrite=True,
        Tags=[
            {
                'Key': 'Purpose',
                'Value': 'Migration Factory Setting'
            },
        ],
        Tier='Standard',
    )

def removeParameter(key):
    
    client = boto3.client('ssm')

    client.delete_parameter(
    Name = '/migrationFactory/' + key,  
   )

def removeParameters():

    client = boto3.client('ssm')
    parameters = client.describe_parameters()['Parameters']
    
    try:
        toDelete=""
        for parameter in parameters:
                toDelete=parameter['Name']

                client.delete_parameters(
                    Names=[
                        toDelete,
                        ]
                    )
    except:
        print('Failed to delete Parameters')

    print('Parameters Deleted')


def getParameter(key):
    
    client = boto3.client('ssm')

    response=client.get_parameter(
        Name = str('/migrationFactory/'+key),
    )

    value=response['Parameter']['Value']
    return(value)


