#!/bin/sh

if [ $# -ne 4 ]; then
	echo "Missing arguments!\nUsage: sh image.sh .data .cfg .weights image" 1>&2
  	exit
fi

./darknet detector test $1 $2 $3 $4 -i 0 -thresh 0.25
