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

class LtspChroot:

	def __init__(self):
		'''
		A simple init method
		'''
		pass    
	#def init

	def startup(self,options):
		'''
		Startup functions
		'''
		pass
	#def startup

	def apt(self):
		'''
		Apt functions
		'''
		pass
	#def apt(self)

	def info(self):
		'''
		Show basic info about this plugin.
		'''
		return {'status':True, 'msg':'[N4dChroot] Info'}
	#def info 

	def test_chroot(self, chroot_dir):
		'''
		test_chroot test if the given directory is a real chroot or 
		besides, it seems like a chroot.
		'''
		if os.path.isdir(chroot_dir):
			return {'status': True, 'msg':'[N4dChroot] Directory existent'}
		else:
			return {'status': False, 'msg':'[N4dChroot] Directory not existent'}

	  #def test_chroot(self, chroot_dir)

	def get_lliurex_version_on_chroot(self, chroot_dir):
		'''
		get the LliureX Version of chroot given.
		'''
		try:
			if not self.test_chroot(chroot_dir)["status"] :
				# If not a directory...you can't do nothing more.
				return {'status': False, 'msg':'[N4dChroot] Directory not existent'}

			else :
				# Ok, this is a directory. 
				lliurex_version=subprocess.check_output(["chroot",chroot_dir,"lliurex-version"])
				return {'status': True, 'msg':'[N4dChroot] '+lliurex_version }     
				
		except Exception as e:
			print(str(e))
		#def get_lliurex_version_on_chroot(self, chroot_dir):

	def prepare_chroot_for_run(self,chroot_dir):
		'''
		Prepare chroot to run commands
		mounting some directories:
			* /proc/
			* /sys/
			* 
		'''
		if not self.test_chroot(chroot_dir)["status"] :
			# If not a directory...you can't do nothing more.
			return {'status': False, 'msg':'[N4dChroot] Directory not existent'}
		
		else:
			# Mount /proc
			ret=subprocess.check_output(["mount","-o","bind","/proc",chroot_dir+"/proc"])
			# Mount /sys
			ret=subprocess.check_output(["mount","-o","bind","/sys",chroot_dir+"/sys"])
			# Mount /dev
			ret=subprocess.check_output(["mount","-o","bind","/dev",chroot_dir+"/dev"])
			# Mount /dev/pts
			ret=subprocess.check_output(["mount","-o","bind","/dev/pts",chroot_dir+"/dev/pts"])
			
			
			return {'status': True, 'msg':'[N4dChroot] All is mounted'}
			
	#def prepare_chroot_for_run(self,chroot)
		
	def umount_chroot(self,chroot_dir):
		'''
		Umount system directories
		now with -lazy, 
		TODO:
			test if it is mounted already
		'''
		if not self.test_chroot(chroot_dir)["status"] :
			# If not a directory...you can't do nothing more.
			return {'status': False, 'msg':'[N4dChroot] Directory not existent'}
			
		else:
			# Mount /proc
			ret=subprocess.check_output(["umount","-l",chroot_dir+"/proc"])
			# Mount /sys
			ret=subprocess.check_output(["umount","-l",chroot_dir+"/sys"])
			# Mount /dev/pts
			ret=subprocess.check_output(["umount","-l",chroot_dir+"/dev/pts"])
			# Mount /dev
			ret=subprocess.check_output(["umount","-l",chroot_dir+"/dev"])
			
			return {'status': True, 'msg':'[N4dChroot] All is umounted'}
	#def umount_chroot(self,chroot_dir)

	def prepare_X11_applications(self,chroot_dir):
		'''
		Prepare a X11 environment to run graphical apps 
		into a chroot
		'''
		try:
			#subprocess.check_output(["xhost",])
			#subprocess.check_output["Xephyr","-ac","-screen","1024x768",":1","&"]
			#subprocess.Popen(["Xephyr","-ac -screen 800x600 :1"])
			#subprocess.Popen(["Xephyr","-ac","-keybd","-screen","800x600",":1"])
			subprocess.Popen(["Xephyr","-ac","-screen","800x600",":1"])
			#subprocess.check_output(["chroot",chroot_dir, "sh","-c","export DISPLAY=:1"])
			#subprocess.check_output["chroot",chroot_dir, "export","DISPLAY=:1"]
			
		except Exception as e:
			return {'status': False, 'msg':'[N4dChroot] '+str(e)}
	
	#def prepare_X11_applications(self,chroot_dir)

	def run_command_on_chroot(self,chroot_dir,command,XServerIP):
		'''
		Possible commands:
			* x-editor
			* synaptic
			* terminal
		'''
		import os
		
		if not self.test_chroot(chroot_dir)["status"] :
		# If not a directory...you can't do nothing more.
			return {'status': False, 'msg':'[N4dChroot] Directory not existent'}
		
		else: 
			
			# First prepare chroot
			self.prepare_chroot_for_run(chroot_dir)
			
			# Then Prepare to run X applications
			self.prepare_X11_applications(chroot_dir)
			
			try:
				
				# Now prepare the appropiate scripts in chroot
				xscript=chroot_dir+"/tmp/xscript.sh"
				f = open(xscript, 'w')
				f.write("#/bin/sh\n\n")
				f.write("export DISPLAY="+XServerIP+":1\n")
							
				if (command=="x-editor"):
					print "Loading x-editor, display will be: "+XServerIP+":1"
					f.write("scite\n")
					#subprocess.check_output(["chroot",chroot_dir, "/usr/share/lliurex-ltsp-client/Xeditor.sh"])
				elif (command=="synaptic"):
					print "Loading synaptic, display will be: "+XServerIP+":1"
					f.write("synaptic\n")
					#subprocess.check_output(["chroot",chroot_dir, "/usr/share/lliurex-ltsp-client/Xsynaptic.sh"])
				elif (command=="terminal"):
					print "Loading terminal, display will be: "+XServerIP+":1"
					f.write("xterm\n")
					#subprocess.check_output(["chroot",chroot_dir, "/usr/share/lliurex-ltsp-client/Xterminal.sh"])
				else:
					print "Unknown: "+command
					f.write(command)

				#Once scripts will be prepared, let's run it
				f.close()
				subprocess.Popen(["sudo", "chmod","+x", xscript])
				subprocess.check_output(["chroot",chroot_dir, "/tmp/xscript.sh"])
				print "3"
				os.remove(xscript)

			
			except Exception as e:
				return {'status': False, 'msg':'[N4dChroot] '+str(e)}
			
			# At last leave chroot gracefully
			self.umount_chroot(chroot_dir)
	
		
	#def run_command_on_chroot(self,chroot_dir,command)



	# TODO 
	

#class LtspChroot

