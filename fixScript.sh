#!/bin/bash

cd MigrationFactory/deployment/

path=`pwd`

echo $path

dos2unix $path/build-s3-dist.sh
sed -i '' 's/CFN-template\///g' $path/build-s3-dist.sh