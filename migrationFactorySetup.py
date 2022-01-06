import boto3
import os
import subprocess
import git 


Account_ID = boto3.client('sts').get_caller_identity()['Account']
bucketName = Account_ID + 'migration'
solutionName = 'migrationFactory'
version = '0.01'
args = './build-s3-dist.sh' + ' ' + bucketName + ' ' + solutionName + ' ' + version 

#git.Repo.clone_from('git@github.com:awslabs/aws-cloudendure-migration-factory-solution.git', 'MigrationFactory')
#subprocess.call(['chmod', '0755', '/Users/daniel.mulrooney/workspaces/migration_setup/MigrationFactory/deployment/build-s3-dist.sh'])
#os.system('/Users/daniel.mulrooney/workspaces/migration_setup/MigrationFactory/deployment/build-s3-dist.sh {} {} {}' .format(str(bucketName), str(solutionName), str(version)) )

subprocess.check_call([args], shell=True, cwd='/Users/daniel.mulrooney/workspaces/migration_setup/MigrationFactory/deployment/')