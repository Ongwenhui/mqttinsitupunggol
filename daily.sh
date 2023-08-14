#!/bin/sh

# daily maintenance to update docker images
/bin/rm /var/log/sntl.log 1>/dev/null 2>/dev/null

# /bin/systemctl stop watchdog
echo 300 > /dev/shm/.counter

exec 1>>/var/log/sntl.log

daily() {
  /bin/echo -e "Daily system maintenance\n========================"
  /bin/date +-\ %Y%m%d\ %H:%M:%S && /bin/echo "Restarting ecrLogin" && /bin/systemctl restart ecrLogin.service
  /bin/date +-\ %Y%m%d\ %H:%M:%S && /usr/bin/docker pull 465539528376.dkr.ecr.ap-southeast-1.amazonaws.com/msogt/coord:latest && /bin/systemctl restart ws_coord.service
  /bin/date +-\ %Y%m%d\ %H:%M:%S && /usr/bin/docker pull 465539528376.dkr.ecr.ap-southeast-1.amazonaws.com/rpi/dsp:latest && /bin/systemctl restart dsp.service
  /bin/date +-\ %Y%m%d\ %H:%M:%S && /usr/bin/docker pull 465539528376.dkr.ecr.ap-southeast-1.amazonaws.com/rpi/e3372setup:latest && /bin/systemctl restart gsmmodem.service
  /bin/date +-\ %Y%m%d\ %H:%M:%S && /usr/bin/docker pull 465539528376.dkr.ecr.ap-southeast-1.amazonaws.com/rpi/ptz:latest && /bin/systemctl restart ptz_doa.service
  /bin/date +-\ %Y%m%d\ %H:%M:%S && /bin/echo Cleaning docker images... && /usr/bin/docker container prune -f && /usr/bin/docker rmi `/usr/bin/docker images --filter dangling=true --format {{.ID}}` 2> /dev/null
}

# clean up /var/log/watchdog
[ `/usr/bin/stat /var/log/watchdog/test-bin.stdout | /bin/grep -Po 'Size: \K[^ ]+'` -gt 100000 ] && rm /var/log/watchdog/test-bin.stdout 2>/dev/null

echo 300 > /dev/shm/.counter
# /bin/systemctl start watchdog

# pull if there's any patch
# /usr/bin/ssh-agent /bin/bash -c '/usr/bin/ssh-add /root/.ssh/rpi_rsa; /usr/bin/git -C "/root/.setup" pull'

# reboot
/bin/date +-\ %Y%m%d\ %H:%M:%S && /bin/echo Rebooting... && /sbin/reboot
