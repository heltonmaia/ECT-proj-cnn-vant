#!/bin/sh

if [ $# -ne 4 ]; then
	echo "Missing arguments!\nUsage: sh video.sh .data .cfg .weights video" 1>&2
  	exit
fi

./darknet detector demo $1 $2 $3 $4 -i 0 -thresh 0.25
