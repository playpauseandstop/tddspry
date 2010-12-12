#!/bin/sh
#
# Run ``test`` or any other Makefile target for each bootstrapped environment.
#
# Usage: runtests.sh <target>
#

DIRNAME=`dirname $(readlink -f $0)`
target=$1

if [ -z $target ]
then
    target=test
fi

for dir in $DIRNAME/env*/
do
    if [ ! -d "$dir" ]
    then
        continue
    fi

    source "$dir/bin/activate"
    make $target
done
