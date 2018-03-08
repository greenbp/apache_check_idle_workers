#!/usr/bin/python
import subprocess
import time
import commands

logFile = open('/var/log/check_apache.log','a')
logFile.flush()

while True:

  idle = commands.getoutput('/etc/init.d/httpd fullstatus | grep "idle workers" | cut -d " " -f 9')
  t = time.strftime("%Y-%m-%d %H:%M:%S")

  def check_idle(response):
      if response == "0":
          logFile.write('%s - %s workers, restarting\n' % (t, idle))
          subprocess.call(["service httpd restart"], shell=True)
          time.sleep(1)
          status = commands.getoutput('service httpd status | cut -d " " -f 6')
          if status == "running...":
            logFile.write('%s Restarted, status: %s\n' % (t, status))
          else:
             logFile.write('%s Could not restart apache\n' % t)    
      elif response.isdigit() and response != "0":
          #logFile.write('%s - %s workers, OK\n' % (t, idle))
          print('%s - %s workers, OK' % (t, idle))
      elif not response.isdigit():
          logFile.write('%s - Apache dead: %s\n' % (t, idle))
          subprocess.call(["killall -9 httpd"], shell=True)
          subprocess.call(["service httpd restart"], shell=True)
          time.sleep(1)
          status = commands.getoutput('service httpd status | cut -d " " -f 6')
          print('%s' % status)
          if status == "running...":
            logFile.write('%s Restarted, status: %s\n' % (t, status))
          else:
             logFile.write('%s Could not restart apache\n' % t)
  
  check_idle(idle)
  logFile.flush()
  time.sleep(1)
