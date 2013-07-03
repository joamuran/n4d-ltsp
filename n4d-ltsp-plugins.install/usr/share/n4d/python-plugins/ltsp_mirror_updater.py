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

	def launchLliurexMirrorGui(self,XServerIP,display):
		try:
			import time
			# Now prepare the appropiate scripts in chroot

			xscript="/tmp/xscript.sh"
			print "Building file: "+xscript
			f = open(xscript, 'w')
			f.write("#/bin/bash\n\n")
			#f.write("shopt -s expand_aliases\n")
			f.write("export DISPLAY="+XServerIP+display+"\n")
			f.write("setxkbmap es\n")
			f.write("dbus-launch --exit-with-session lliurex-mirror-gui\n")
			f.close()
			subprocess.Popen(["sudo", "chmod","+x", xscript])
			output=subprocess.check_output(["/tmp/xscript.sh"])
			return {'status': True, 'msg':'[remote lliurex-mirror-gui] Finished with Output: '+str(output)}

		except Exception:
			return {'status': False, 'msg':'remote lliurex-mirror-gui'.join(str(e).split(' ')[-1:])}
	
#class LtspMirrorUpdater

