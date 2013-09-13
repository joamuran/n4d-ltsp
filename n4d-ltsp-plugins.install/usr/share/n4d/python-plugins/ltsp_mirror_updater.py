#!/usr/bin/python

# This script is licensed under GPL v3 or higher
#
# Authors: Angel Berlanas Vicente 
#         		<angel.berlanas@gmail.com>
#				Jose Alfredo Murcia Andres
#				<joamuran@gmail.com>
#

# Libraries
import sys
import subprocess


class LtspMirrorUpdater:

	def __init__(self):
		'''
		A simple init method
		'''
		pass    
	#def init

	def launchLliurexMirrorGui(self,XServerIP,display,XephyPID):
		try:
			import time
			# Now prepare the appropiate scripts in chroot
			xscript="/tmp/xscript.sh"
			print "Building file: "+xscript
			f = open(xscript, 'w')
			f.write("#/bin/bash\n\n")
			#f.write("shopt -s expand_aliases\n")
			#f.write("sudo su\n")
			f.write("export DISPLAY="+XServerIP+display+"\n")			
			f.write("metacity --display "+display+" &\n")
			f.write("setxkbmap es\n")
			print (XephyPID)
			f.write("sudo dbus-launch --exit-with-session lliurex-mirror-gui; n4d-client -h "+XServerIP+" -c ltspClientXServer -m killXephyr -a "+str(XephyPID)+"\n")
			
			#f.write("sudo dbus-launch --exit-with-session lliurex-mirror-gui; zenity --info --text 'Click to close.'; n4d-client -h "+XServerIP+" -c ltspClientXServer -m killXephyr -a "+str(XephyPID)+"\n")
			#f.write("sudo dbus-launch --exit-with-session lliurex-mirror-gui\n")
			
			f.write("exit 0\n")
			f.close()
			
			# wait for file end writing
			while(not(os.path.exists(xscript))):
				time.sleep(0.2)
	
			subprocess.Popen(["sudo", "chmod","+x", xscript])
			
			output=None
			repeat=True
			retries=0
			
			# yes... dirty code, but runs...
			while (repeat==True):
				try:
					output=subprocess.check_output(["sudo", xscript])
					repeat=False
				except Exception as e:
					retries=retries+1
					if(retries>10):
						return {'status': False, 'msg':'Max retries exceed'}
			
			return {'status': True, 'msg':'[remote lliurex-mirror-gui] Finished with Output: '+str(output)}

		except Exception as e:
			return {'status': False, 'msg':'remote lliurex-mirror-gui'.join(str(e).split(' ')[-1:])}

			
	
#class LtspMirrorUpdater
