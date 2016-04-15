#!/usr/bin/python
# -*- coding: utf-8 -*- 
import sys
import signal
from lcd import LCD
from subprocess import *
import time
import datetime
import atexit
import psutil


cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
lcd = LCD()

signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))
def run_cmd(cmd):
	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	return output

def exit_handler():
        lcd.clear()
atexit.register(exit_handler)


def screen0():
	ipaddr = run_cmd(cmd)
	lcd.write_line1(datetime.datetime.now().strftime('%b %d  %H:%M:%S'), 2)
	lcd.write_line2('IP %s' % (ipaddr), 2)

def screen1():
	cpu_load = str(psutil.cpu_percent(interval=1))
	mem = psutil.virtual_memory()	
	lcd.write_line1('CPU: '+ cpu_load +'%', 2);
	lcd.write_line2('Memory: '+ str(mem.percent) +'%', 2);

def screen2():
	disk = psutil.disk_usage('/')
	uptime, idletime = [float(field) for field in open("/proc/uptime").read().split()]
	m, s = divmod(uptime, 60)
	h, m = divmod(m, 60)
	lcd.write_line1('Disk '+ str(disk.percent) +'% used', 2);
	lcd.write_line2("Uptime %d:%02d:%02d" % (h, m, s), 2);

def main():
	lcd.clear()
	time.sleep(1)
	last_screen_changed = time.time()
	screen_index = 0

	lcd.set_line2()
	#lcd.type_string('................', 0.3);
	while 1:
		ts = time.time()
		diff = ts - last_screen_changed
		if diff > 10:
		    try:
                      new_index = screen_index+1
  		      if globals()['screen'+ str(new_index) ]:
		        screen_index += 1
                      else:	
 		       screen_index = 0
		    except KeyError:
		     screen_index = 0
                    last_screen_changed = ts
	
                globals()['screen'+ str(screen_index) ]() 
                time.sleep(0.5)	
		
main();

