#!/usr/bin/bash

gittag="jbosstools-4.4.3.AM1"

MODULES="jbosstools-base \
         jbosstools-build"

mkdir $gittag
pushd $gittag

# JBoss Tools is split across many repositories
for module in $MODULES; do
  wget https://github.com/jbosstools/$module/archive/$gittag.tar.gz
  mkdir $module
  tar --strip-components=1 --directory=$module -xf $gittag.tar.gz
  rm $gittag.tar.gz
done

# Delete pre-built artifacts
for ext in jar war zip class; do
  find -type f -name *.$ext -delete
done

# Delete modules we are not currently interested in building
for m in jbosstools-base/{site,tests,common,stacks,runtime} ; do
  rm -rf $m && sed -i -e "/<module>$(basename $m)/d" $(dirname $m)/pom.xml
done

popd
tar cJf $gittag.tar.xz $gittag/
rm -r $gittag/

