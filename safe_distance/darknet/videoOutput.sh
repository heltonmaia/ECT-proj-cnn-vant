#!/bin/sh

if [ $# -ne 5 ]; then
	echo "Missing arguments!\nUsage: sh video.sh .data .cfg .weights video output" 1>&2
  	exit
fi

./darknet detector demo $1 $2 $3 $4 -out_filename $5
