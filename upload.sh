#!/bin/bash


Account_ID=`aws sts get-caller-identity --query Account --output text`
rootPath='/Users/daniel.mulrooney/workspaces/migration_setup'
solutionName='migrationFactory'       ## Replace with customer 3 letter acronym
version='2.02'                        ## should be incremented by platform only
region=`aws configure get region`
cd $rootPath/$solutionName/deployment/

echo "Upload global files"
aws s3 cp global-s3-assets/ s3://$Account_ID-migration-$region/$solutionName/$version/ --acl public-read --recursive

echo "Upload regional files"
aws s3 cp regional-s3-assets/ s3://$Account_ID-migration-$region/$solutionName/$version/ --acl public-read --recursive