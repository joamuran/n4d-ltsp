#!/usr/bin/python
# This script is licensed under GPL v3 or higher
#
# Authors: Angel Berlanas Vicente 
#         		<angel.berlanas@gmail.com>
#	Jose Alfredo Murcia Andres
#			<joamuran@gmail.com>
#

# Libraries
import subprocess
import os.path
import signal

class LTSPX11Environment:
	#PID=None;   
	
	def RemoveXephyrProcess(self, str_display):
		'''
		Removes all instances running on display
		'''
		display=str_display[1:]
		# Check if Xephir is running on :display
		fname='/tmp/.X'+display+'-lock'
		if (os.path.isfile(fname)):
			print ("File "+fname+" exists")
			f = open(fname, 'r')
			for line in f:
				#print "Pid: "+line.strip()
				if (os.path.exists("/proc/"+line.strip())):
					print ("Xephir is running on :"+display)
					os.kill(int(line.strip()), signal.SIGTERM)
				else:
					print("File does not exists")
			os.remove(fname)
			
	#def RemoveXephyrProcess():
	
	
	def prepare_X11_applications_on_chroot(self, display, screen):
		'''
		Prepare a X11 environment to run graphical apps 
		into a chroot -> This functionanlity has moved to client part (Xephyr will run on Client Administrator App, not on Server)
		'''

		try:
			# Check if Xephir is running on :display
			self.RemoveXephyrProcess(display)
			# Display on display
			pid=subprocess.Popen(["Xephyr","-ac","-screen",screen,display])
			subprocess.Popen(["metacity", "--display",display])
			#subprocess.Popen(["openbox", "--display",display])
			
			return pid
		except Exception as e:
			return {'status': False, 'msg':'[N4dChrootAdmin] '+str(e)}

	#def prepare_X11_applications_on_chroot(self,chroot_dir)
	
	#def remove_X11_applications_on_chroot(self, display, metacityPID):
	def remove_X11_applications_on_chroot(self, display):
		'''
		Kill Xephir Process
		'''
		
		import os
		import signal
		
		try:
			# Terminator Solucion 
			#subprocess.Popen(["killall","Xephyr"])
			#print ("Killing: "+XepId)
			# Delete Metacity
			#if (os.path.exists("/proc/"+metacityPID)):
			#	print "Metacity process is running!"
			#	os.kill(int(metacityPID), signal.SIGTERM)
			#else:
			#	print "Metacity process is NOT running!"
			# Delete Xephyr
			self.RemoveXephyrProcess(display)
			#print (type(XepId))
			
		except Exception as e:
			print "Exception killing:"+str(e)
			return {'status': False, 'msg':'[N4dChrootAdmin] '+str(e)}
	#def remove_X11_applications_on_chroot(self,chroot_dir)
	