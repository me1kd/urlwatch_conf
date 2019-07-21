#!/bin/bash
while :
do
	now=$(date +"%T")
        echo "Current time : $now"
	python3 $1 >> ./logs.txt
        sleep $2
done
