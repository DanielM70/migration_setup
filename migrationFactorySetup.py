import boto3
import os
import subprocess
import git
import properties
from cognito import cognitoAddUser
from parameters import getParameter, putParameter
from cloudformation import deployMigrationFactoryCore, pushOutputs

#Account_ID = boto3.client('sts').get_caller_identity()['Account'] 


# Used to update CloudFormation templates 
# DO NOT add region, that is appended in the CFN template

bldbucketName = getParameter('Account_ID') + '-migration'

### Main Body of Scipt

## Check out migration factory code from AWS
git.Repo.clone_from(properties.repoName, properties.checkoutFolder)
print('Repo cloned')

## Update build-s3-dist.sh script from AWS to address issue with template path and set root path
## We may start cloning AWS repo and upload to our own, if that's the case we can fix this stuff
## then and remove this. Each version will need to be tested for any errors.
fixcmd = './fixScript.sh' + ' ' + properties.rootPath + properties.checkoutFolder
subprocess.call(['chmod', '0755', '/Users/daniel.mulrooney/workspaces/migration_setup/fixScript.sh'])
subprocess.check_call([fixcmd], shell=True, cwd='/Users/daniel.mulrooney/workspaces/migration_setup/')

## Execute the build-s3-dist.sh script with required arguments
#buildcmd = './build-s3-dist.sh' + ' ' + bucketName + ' ' + solutionName + ' ' + version

buildcmd = './build-s3-dist.sh' + ' ' + bldbucketName + ' ' + properties.solutionName + ' ' + properties.version
subprocess.call(['chmod', '0755', properties.rootPath + properties.checkoutFolder + '/deployment/build-s3-dist.sh'])
subprocess.check_call([buildcmd], shell=True, cwd=properties.rootPath + properties.checkoutFolder + '/deployment/')

## Once all the lamda is built and templates updated upload to required S3 buckets
print('Upload content')
uploadcmd = './upload.sh'
subprocess.call(['chmod', '0755', 'upload.sh'])
subprocess.check_call([uploadcmd], shell=True, cwd=properties.rootPath)


## Start building the environment using provided AWS cloud formation templates

print('Executing Migration Factory core cloudformation')
stack_id = deployMigrationFactoryCore(getParameter('Account_ID'),bldbucketName)
response=pushOutputs(stack_id)

print(response)

## Add users to Cognito

for id, info in properties.cognitoUsers.items():
    
    print('Adding user to Cognito')
    cognitoAddUser(properties.cognitoUsers[id]['name'], properties.cognitoUsers[id]['role'])
