#!/bin/bash
while :
do
idle=$(/etc/init.d/httpd fullstatus | grep "idle workers" | cut -d " " -f 9)
date=$(date)
echo $idle
if [[ $idle == 0 ]]; then
   echo $date "-" $idle "workers, restarting httpd" >> /var/log/check_apache.log
   service httpd restart >> /var/log/check_apache.log
   sleep 5
elif [[ $idle == " " ]]; then
   echo $date "-" $idle", attempting to kill and restart"
   killall httpd
   service httpd start
   sleep 5
else
#   echo $date "-" $idle "idle workers" # >> /var/log/check_apache.log
   sleep 1
fi
done
