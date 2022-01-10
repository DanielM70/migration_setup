import boto3
import sys

def putParameter(Account_ID, key, value, secure):

    if secure == True:
        typestring = 'SecureString'
    else:
        typestring = 'String'

    client = boto3.client('ssm')

    response = client.put_parameter(
        Name = '/' + Account_ID + '/migrationFactory/' + key,
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

def removeParameter(Account_ID, key):
    
    client = boto3.client('ssm')

    client.delete_parameter(
    Name = '/' + Account_ID + '/migrationFactory/' + key,  
   )

def getParameter(Account_ID, key):
    
    client = boto3.client('ssm')

    response=client.get_parameter(
        Name = '/'+Account_ID+'/migrationFactory/'+key,
    )

    value=response['Parameter']['Value']
    print(value)


