#!/bin/bash

path=$1
fixpath=$path/deployment
echo "Inside fixScript"
echo $fixpath
dos2unix $fixpath/build-s3-dist.sh
ls -l $fixpath/build-s3-dist.sh
sed -i '' 's/CFN-templates\///g' $fixpath/build-s3-dist.sh
sed -i '' "s|\$PWD|$fixpath|" $fixpath/build-s3-dist.sh

