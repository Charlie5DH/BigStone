#!/bin/bash

while true ; do
	IP=$(ifconfig wlan0 | grep inet | grep -v inet6 | awk '{ print $2 }')
	if [ "$IP" != "" ] ; then
		break
	fi
	sleep 1
done
echo "Network done! IP: $IP"

AWS="ubuntu@ec2-54-207-127-233.sa-east-1.compute.amazonaws.com"

ssh -f -i ~/.ssh/aws_cantina.pem -N -R 4445:localhost:22 $AWS

if [[ $? -eq 0 ]]; then
   echo "Tunnel to host created successfully"
else
   echo "An error occurred creating a tunnel to host. RC was $?"
fi
