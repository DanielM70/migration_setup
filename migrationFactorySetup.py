import boto3
import os
import subprocess
import git
from parameters import getParameter, putParameter
from utility import createSecurityGroup, getSubnetId
from cloudformation import deployMigrationFactoryCore, deployMGN

Account_ID = boto3.client('sts').get_caller_identity()['Account'] 


## Customizable if wanted
bucketName = Account_ID + '-migration'
solutionName = 'migrationFactory'       ## Replace with customer 3 letter acronym
version = '0.01'                        ## should be incremented by platform only



## Migration Factory repo
## Currently pointed to AWS (may change to PVTR managed)
repoName = 'git@github.com:awslabs/aws-cloudendure-migration-factory-solution.git'

## Path where you've checked out this code
rootPath = '/Users/daniel.mulrooney/workspaces/migration_setup/'
checkoutFolder = 'migrationFactory'

### Main Body of Scipt

## Check out migration factory code from AWS
git.Repo.clone_from(repoName, checkoutFolder)
print('Repo cloned')

## Update build-s3-dist.sh script from AWS to address issue with template path and set root path
## We may start cloning AWS repo and upload to our own, if that's the case we can fix this stuff
## then and remove this. Each version will need to be tested for any errors.
fixcmd = './fixScript.sh' + ' ' + rootPath + checkoutFolder
subprocess.call(['chmod', '0755', '/Users/daniel.mulrooney/workspaces/migration_setup/fixScript.sh'])
subprocess.check_call([fixcmd], shell=True, cwd='/Users/daniel.mulrooney/workspaces/migration_setup/')

## Execute the build-s3-dist.sh script with required arguments
#buildcmd = './build-s3-dist.sh' + ' ' + bucketName + ' ' + solutionName + ' ' + version

buildcmd = './build-s3-dist.sh' + ' ' + bucketName + ' ' + solutionName + ' ' + version
subprocess.call(['chmod', '0755', rootPath + checkoutFolder + '/deployment/build-s3-dist.sh'])
subprocess.check_call([buildcmd], shell=True, cwd=rootPath + checkoutFolder + '/deployment/')

## Once all the lamda is built and templates updated upload to required S3 buckets
print('Upload content')
uploadcmd = './upload.sh'
subprocess.call(['chmod', '0755', 'upload.sh'])
subprocess.check_call([uploadcmd], shell=True, cwd=rootPath)


## Start building the environment using provided AWS cloud formation templates

print('Executing Migration Factory core cloudformation')
stack_id_transient_core = deployMigrationFactoryCore(Account_ID,bucketName)

print(stack_id_transient_core)

print('Executing Migration Factory MGN cloudformation')
stack_id_transient_mgn = deployMGN(Account_ID,bucketName)

print(stack_id_transient_mgn)