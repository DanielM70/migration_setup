## Migration Factory Setup


Usage:

# Configuration

Update properties.py with any required information, Do not change scripts or functions unless you know what your doing. 

# Under the hood

setupRequirements.py
    - creates required IAM users, key, secrets and push to parameter store
    - creates required S3 bucket

migrationFactorySetup.py
    - checks out latest code from github
    - updates code to address various bugs or issues with source
    - uploads compiled objects and templates to S3
    - executes cloud formation template that builds the AWS Migration Factory solution
    - creates cognito users as defined and adds to assigned role
    - updates dynamoDB attributes required

properties.py (imported file)
    - includes all variables that are User defined
    - Users emails and Roles
    - additional IAM roles and policies (if required)

cloudformation.py (imported file)
    - executes various cloudformation jobs

parameters.py (imported file)
    - add/remove/get parameters from SSM parameter store

cognito.py (imported file)
    - add users to cognito

fixScript.sh
    - used to fix some issues with checked out code
    - path and compile issue

upload.sh
    - used to upload and set permissions on file in S3
    - have a function but couldn't get permissions to set 

utility.py (imported file)
    - creates security group
    - discovers subnet
    - expect more to be added here or this can be combined with something possibly

clean.py
    - will tear down the environment
        - CFN
        - S3 buckets
        - IAMs
        - SG
        - All SSM parameters
