

## Add any IAM users and policies required
## Copy line 1, add info, make sure to close with a comma

iamUsers={
    1: {'name': 'discovery', 'boundary': 'arn:aws:iam::aws:policy/AWSApplicationDiscoveryAgentAccess'}, 
    2: {'name': 'migration', 'boundary': 'arn:aws:iam::aws:policy/AWSApplicationMigrationAgentPolicy'}
}

## Add Application users and Role
## Copy line 1, add info, make sure to close with a comma

cognitoUsers={
    1: {'name': 'daniel.mulrooney+1@pivotree.com', 'role': 'admin'},
    2: {'name': 'daniel.mulrooney+2@pivotree.com', 'role': 'admin'},
    3: {'name': 'daniel.mulrooney+3@pivotree.com', 'role': 'admin'},
}


## Migration Factory repo
## Currently pointed to AWS (may change to PVTR managed)

repoName='git@github.com:awslabs/aws-cloudendure-migration-factory-solution.git'

## Path where you've checked out this code

rootPath='/Users/daniel.mulrooney/workspaces/migration_setup/'
checkoutFolder='migrationFactory'

## Used by CloudFormation
## sed will update these values in various places in migrationFactory code

solutionName='migrationFactory'                         ## Replace with customer 3 letter acronym
version='2.02'                                          ## should be incremented by platform only
serviceAccountEmail='daniel.mulrooney@pivotree.com'     ## Service Account Email


