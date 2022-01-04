import boto3

users = {
    1: {'name': 'discovery', 'boundary': 'arn:aws:iam::aws:policy/AWSApplicationDiscoveryAgentAccess'}, 
    2: {'name': 'migration', 'boundary': 'arn:aws:iam::aws:policy/AWSApplicationMigrationAgentPolicy'}
}

## Clean up User Keys, then Users

def removeIAMusers():

    for id, info in users.items():
        
        print("\nUser_ID:", id)

        client = boto3.client('iam')
        
        ## Query for access key ID

        key_id = client.list_access_keys(
            UserName = users[id]['name']
        )

        print(key_id['AccessKeyMetadata'])
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



removeIAMusers()