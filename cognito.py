import botocore
import boto3
import properties
from parameters import getParameter


client = boto3.client('cognito-idp')
#poolId=getParameter('UserPoolId')

def cognitoAddUser(userEmail, userGroup):


    try:

        client.admin_create_user(
            UserPoolId=getParameter('UserPoolId'),
            Username=userEmail,
            #UserAttributes = [
                #{"Name": "first_name", "Value": 'PVTR'},
                #{"Name": "last_name", "Value": 'Admin'},
                #{"Name": "email_verified", "Value": "true" }
            #],
            ForceAliasCreation=False,
            DesiredDeliveryMediums=[
                'EMAIL',
            ],
        )

        client.admin_add_user_to_group(
            UserPoolId=getParameter('UserPoolId'),
            Username=userEmail,
            GroupName=userGroup
        )
    
    except:
        print('User Already added')




