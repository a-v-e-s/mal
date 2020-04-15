#!/bin/bash

CPUS_TO_USE=$((`nproc` - 1))

echo "Enter the filename with video titles:"
read INPUT_FILE
echo "Enter the email address associated with the account:"
read EMAIL
echo "Please enter your password:"
read PASSWORD

while read title; do
	while true; do
		if [[ `jobs -r | wc -l` -ge $CPUS_TO_USE ]]; then
			sleep 1 && continue
		fi
		url="https://gaia.com/video/$title?fullplayer=feature"
		python3 -m youtube_dl --username $EMAIL --password $PASSWORD $url &
		break
	done
done < "$INPUT_FILE"

