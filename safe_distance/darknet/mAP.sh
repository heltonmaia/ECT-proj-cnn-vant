#!/bin/sh

if [ $# -ne 3 ]; then
	echo "Missing arguments!\nUsage: sh mAP.sh .data .cfg .weights" 1>&2
  	exit
fi

./darknet detector map $1 $2 $3

