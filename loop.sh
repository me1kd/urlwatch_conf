#!/bin/bash
while :
do
	now=$(date +"%T")
        echo "Current time : $now"
	/home/v5dkw/Develop/urlwatch/env/bin/python3 /home/v5dkw/Develop/urlwatch/urlwatch/urlwatch >> /home/v5dkw/Develop/urlwatch/urlwatch/logs.txt 2> /home/v5dkw/Develop/urlwatch/urlwatch/errors.txt
        sleep 30
done
