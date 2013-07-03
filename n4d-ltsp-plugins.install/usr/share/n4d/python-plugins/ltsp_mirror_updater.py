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
			output=subprocess.check_output(["lliurex-mirror-gui"])
			return {'status': True, 'msg':'[remote lliurex-mirror-gui] Finished with Output: '+str(output)}
		except Exception:
			return {'status': False, 'msg':'remote lliurex-mirror-gui'.join(str(e).split(' ')[-1:])}
	
#class LtspChroot

