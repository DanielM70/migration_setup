import boto3
import os
import subprocess
import git 


Account_ID = boto3.client('sts').get_caller_identity()['Account']

bucketName = Account_ID + 'migration'
solutionName = 'migrationFactory'       ## Replace with customer 3 letter acronym
version = '0.01'                        ## should be incremented by platform only


cmd = './build-s3-dist.sh' + ' ' + bucketName + ' ' + solutionName + ' ' + version 

#git.Repo.clone_from('git@github.com:awslabs/aws-cloudendure-migration-factory-solution.git', 'MigrationFactory')
#subprocess.call(['chmod', '0755', '/Users/daniel.mulrooney/workspaces/migration_setup/MigrationFactory/deployment/build-s3-dist.sh'])
#ubprocess.check_call([cmd], shell=True, cwd='/Users/daniel.mulrooney/workspaces/migration_setup/MigrationFactory/deployment/')
subprocess.call(['chmod', '0755', '/Users/daniel.mulrooney/workspaces/migration_setup/fixScript.sh'])
subprocess.check_call('./fixScript.sh', shell=True, cwd='/Users/daniel.mulrooney/workspaces/migration_setup/')


