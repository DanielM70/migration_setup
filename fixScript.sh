#!/bin/bash

## Remove CFN-templates as it's not actually used 

path=$1
fixpath=$path/deployment
echo "Inside fixScript"
echo $fixpath
dos2unix $fixpath/build-s3-dist.sh
ls -l $fixpath/build-s3-dist.sh
sed -i '' 's/CFN-templates\///g' $fixpath/build-s3-dist.sh
sed -i '' "s|\$PWD|$fixpath|" $fixpath/build-s3-dist.sh


## This is to fix a bug introduced that prevents the node.js application from building
## just commenting out what appears to be the offending validable, not sure why it's breaking

nodefilepath=$path/source/frontend/src/containers
echo "Fixing node file"
ls -l $nodefilepath/User.js
sed -i '' '259s|var|//var|g' $nodefilepath/User.js

