import boto3
import sys

def putParameter(Account_ID, key, value, secure ):

    if secure == True:
        typestring = 'SecureString'
    else:
        typestring = 'String'

    client = boto3.client('ssm')

    response = client.put_parameter(
        Name = '/' + Account_ID + '/MigrationFactory/' + key,
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

    Name2 = '/' + Account_ID + '/MigrationFactory/' + key
    print(Name2)

    client.delete_parameter(
    Name = '/' + Account_ID + '/MigrationFactory/' + key,  
   )


