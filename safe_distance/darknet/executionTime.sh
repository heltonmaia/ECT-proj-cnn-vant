#!/bin/sh

if [ $# -ne 5 ]; then
	echo "Missing arguments!\nUsage: sh executionTime.sh .data .cfg .weights files output" 1>&2
  	exit
fi

./darknet detector test $1 $2 $3 -dont_show  < $4 | awk '/seconds/ {print $7","}' >> $5

