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
		into a chroot -> This functionanlity has moved to client part (Xephyr will run on Client Administrator App, not on Server)
		'''
		
		'''
		try:
			# Display on :42, the answer to the Universe, the Existence and all other things  (i.e. Xephire Display)
			
			subprocess.Popen(["Xephyr","-ac","-screen","800x600",":42"])
			subprocess.Popen(["metacity", "--display",":42"])
			#subprocess.Popen(["xfwm4", "--display",":42"])
		except Exception as e:
			return {'status': False, 'msg':'[N4dChroot] '+str(e)}

	'''
	#def prepare_X11_applications(self,chroot_dir)
	'''
	def run_command_on_chroot(self,chroot_dir,command,XServerIP,display):
		'' '
		Possible commands:
			* x-editor
			* synaptic
			* terminal
		'' ' 
		#import os
	
		output=""
		if not self.test_chroot(chroot_dir)["status"] :
		# If not a directory...you can't do nothing more.
			return {'status': False, 'msg':'[N4dChroot] Directory not existent'}
		
		else: 
			# First prepare chroot
			self.prepare_chroot_for_run(chroot_dir)
			
			# Then Prepare to run X applications
			self.prepare_X11_applications(chroot_dir)
			
			try:
				import time
				# Now prepare the appropiate scripts in chroot
				xscript=chroot_dir+"/tmp/xscript.sh"
				print "Building file: "+xscript
				f = open(xscript, 'w')
				f.write("#/bin/bash\n\n")
				#f.write("shopt -s expand_aliases\n")
				f.write("export DISPLAY="+XServerIP+display+"\n")
				#f.write("metacity &\n")
				f.write("setxkbmap es\n")
				f.write("metacity --display "+XServerIP+display+" &\n")
				# Avoid shuddown
				f.write("cp /etc/skel/.bashrc /root/.bashrc\n")
				f.write("echo \"alias shutdown='echo Bad luck, guy!'\" >> /root/.bashrc \n")
				f.write("echo \"alias halt='echo Bad luck, guy!'\" >> /root/.bashrc \n")
				f.write("echo \"alias init='echo Bad luck, guy!'\" >> /root/.bashrc \n")
				f.write("echo \"alias telinit='echo Bad luck, guy!'\" >> /root/.bashrc \n")
				f.write("echo \"alias zic='echo Bad luck, guy!'\" >> /root/.bashrc \n")

			
				if (command=="x-editor"):
					print "Loading x-editor, display will be: "+XServerIP+display
					f.write("dbus-launch --exit-with-session scite\n")
					#subprocess.check_output(["chroot",chroot_dir, "/usr/share/lliurex-ltsp-client/Xeditor.sh"])
				elif (command=="synaptic"):
					print "Loading synaptic, display will be: "+XServerIP+display
					f.write("dbus-launch --exit-with-session synaptic\n")
					#subprocess.check_output(["chroot",chroot_dir, "/usr/share/lliurex-ltsp-client/Xsynaptic.sh"])
				elif (command=="terminal"):
					print "Loading terminal, display will be: "+XServerIP+display
					f.write("dbus-launch --exit-with-session xterm\n")
					#subprocess.check_output(["chroot",chroot_dir, "/usr/share/lliurex-ltsp-client/Xterminal.sh"])
				
				elif (command=="start_session"):
					print "Starting session, display will be: "+XServerIP+display
					#f.write("gnome-session --session gnome-fallback\n")
					f.write("dbus-launch --exit-with-session gnome-session --session=gnome-fallback")
					#subprocess.check_output(["chroot",chroot_dir, "/usr/share/lliurex-ltsp-client/Xterminal.sh"])
				
				else:
					print "Running user command: "+command
					f.write(command)

				f.write("exit 0")
				f.close()
				
				#Once scripts will be prepared, let's run it				
				subprocess.Popen(["sudo", "chmod","+x", xscript])
				#output=subprocess.check_output(["chroot",chroot_dir, "/tmp/xscript.sh"])
				
				# yes... dirty code, but runs...
				repeat=True
				retries=0
				output=None
				while (repeat==True):
					try:
						output=subprocess.check_output(["chroot",chroot_dir, "/tmp/xscript.sh"])
						repeat=False
					except Exception as e:
						retries=retries+1
						if(retries>10):
							return {'status': False, 'msg':'Max retries exceed'}
				
				
				# if command was session, we have to unlink /home and /etc
				if (command=="start_session"):
					subprocess.check_output(["umount","-l",chroot_dir+"/home"])
				

			
			except Exception as e:
				self.umount_chroot(chroot_dir)
				if(e.__class__==subprocess.CalledProcessError):
					#return {'status': False, 'msg':str(e).split(' ')[:-1]}
					return {'status': False, 'msg':' '.join(str(e).split(' ')[-1:])}
				else:
					
					return {'status': False, 'msg':'[N4dChroot] '+str(e)+" EXCEPTION CLASS: "+str(e.__class__)}
			
			# At last leave chroot gracefully
			
			
			self.umount_chroot(chroot_dir)
			return {'status': True, 'msg':'[N4dChroot] Finished with Output: '+str(output)}
		
	#def run_command_on_chroot(self,chroot_dir,command)
	
	'''
	
	def run_command_on_chroot(self,chroot_dir,command,XServerIP,display):
		'''
		Possible commands:
			* x-editor
			* synaptic
			* terminal
		'''
		#import os
	
		output=""
		if not self.test_chroot(chroot_dir)["status"] :
		# If not a directory...you can't do nothing more.
			return {'status': False, 'msg':'[N4dChroot] Directory not existent'}
		
		else: 
			# First prepare chroot
			self.prepare_chroot_for_run(chroot_dir)
			
			# Then Prepare to run X applications
			self.prepare_X11_applications(chroot_dir)
			
			try:
				import time
				# Now prepare the appropiate scripts in chroot
				xscript=chroot_dir+"tmp/xscript.sh"
				print "Building file: "+xscript
				f = open(xscript, 'w')
				f.write("#/bin/bash\n\n")
				
				f.write("export DISPLAY="+XServerIP+display+"\n")
				
				f.write("setxkbmap es\n")
				f.write("export HOME=/root\n")
				
				if (not (command=="start_session")): # unallow metacity in session
					f.write("metacity --display "+XServerIP+display+" &\n")

				# Avoid shuddown
				f.write("cp /etc/skel/.bashrc /root/.bashrc\n")
				
				f.write("echo \"alias shutdown='echo Bad luck, guy!'\" >> /root/.bashrc \n")
				f.write("echo \"alias halt='echo Bad luck, guy!'\" >> /root/.bashrc \n")
				f.write("echo \"alias init='echo Bad luck, guy!'\" >> /root/.bashrc \n")
				f.write("echo \"alias telinit='echo Bad luck, guy!'\" >> /root/.bashrc \n")
				f.write("echo \"alias zic='echo Bad luck, guy!'\" >> /root/.bashrc \n")

				if (command=="x-editor"):
					print "Loading x-editor, display will be: "+XServerIP+display
					f.write("dbus-launch --exit-with-session scite\n")
					#subprocess.check_output(["chroot",chroot_dir, "/usr/share/lliurex-ltsp-client/Xeditor.sh"])
				elif (command=="synaptic"):
					print "Loading synaptic, display will be: "+XServerIP+display
					f.write("dbus-launch --exit-with-session synaptic\n")
					#subprocess.check_output(["chroot",chroot_dir, "/usr/share/lliurex-ltsp-client/Xsynaptic.sh"])
				elif (command=="terminal"):
					print "Loading terminal, display will be: "+XServerIP+display
					f.write("dbus-launch --exit-with-session xterm\n")
				
				elif (command=="start_session"):
					print "Starting session, display will be: "+XServerIP+display
					f.write("dbus-launch --exit-with-session gnome-session --session=gnome-fallback\n")
				
					
				else:
					print "Running user command: "+command
					f.write(command)

				f.close()
				
				#Once scripts will be prepared, let's run it				
				subprocess.Popen(["sudo", "chmod","+x", xscript])

				
				# yes... dirty code, but runs...
				
				# if command was session, we have to unlink /home and /etc
				if (command=="start_session"):
					output=subprocess.check_output(["chroot",chroot_dir, "/tmp/xscript.sh"])
					subprocess.check_output(["umount","-l",chroot_dir+"/home"])
					
				
				else:  # if not start session, we can allow retries
				
					repeat=True
					retries=0
					output=None
					while (repeat==True):
						try:
							output=subprocess.check_output(["chroot",chroot_dir, "/tmp/xscript.sh"])
							repeat=False
						except Exception as e:
							retries=retries+1
							if(retries>10):
								return {'status': False, 'msg':'Max retries exceed'}
				

			except Exception as e:
				self.umount_chroot(chroot_dir)
				
				output=subprocess.check_output(["echo",str(e), ">>","/tmp/myerr"])
				
				if(e.__class__==subprocess.CalledProcessError):
					return {'status': False, 'msg':' '.join(str(e).split(' ')[-1:])}
				else:
					
					return {'status': False, 'msg':'[N4dChroot] '+str(e)+" EXCEPTION CLASS: "+str(e.__class__)}
			
			# At last leave chroot gracefully
			
			
			self.umount_chroot(chroot_dir)
			return {'status': True, 'msg':'[N4dChroot] Finished with Output: '+str(output)}
		
	#def run_command_on_chroot(self,chroot_dir,command)

	
	##################
	def prepare_chroot_for_session(self, chroot_dir):
		'''
		Prepare chroot to start session
		mounting some directories:
			* /var/run
			* ...
		'''
		try:

			# Mounting /home on chroot
			print "Let's mount home"
			ret=subprocess.check_output(["mount","--bind","/home/",chroot_dir+"/home/"])
			print "Check it!"
			#ret=subprocess.check_output(["mount","-o","bind","/home",chroot_dir+"/home"])

			#print "stage 1:"+str(ret)
			# God takes we confessed
					
			# linking /var/run/dbus
			#ret=subprocess.check_output(["cp", "-r",chroot_dir+"/var/run/dbus", chroot_dir+"/var/run/dbus.bak"])
			#ret=subprocess.check_output(["rm", "-rf", chroot_dir+"/var/run/dbus"])
			#ret=subprocess.check_output(["mkdir", chroot_dir+"/var/run/dbus"])
			#ret=subprocess.check_output(["ln", "-s", "/var/run/dbus", chroot_dir+"/var/run/dbus"])
			
			# link /var/lib/dbus/machine-id
			###ret=subprocess.check_output(["cp", "-r", chroot_dir+"/var/lib/dbus/machine-id", chroot_dir+"/var/lib/dbus/machine-id.bak"])
			###ret=subprocess.check_output(["rm", "-rf", chroot_dir+"/var/lib/dbus/machine-id"])
			###ret=subprocess.check_output(["cp", "/var/lib/dbus/machine-id", chroot_dir+"/var/lib/dbus/machine-id"])
			
			return ret
			
		except Exception as e:
			print("LtspSessionCommands: Not mounted " + str(chroot_dir))
			return e		
	#def prepare_chroot_for_run(self,chroot)
		
	
	def remove_session(self, chroot_dir):
		'''
		Umount system directories
		now with -lazy, 
		TODO:
			test if it is mounted already
		'''
		if not self.test_chroot(chroot_dir)["status"] :
			# If not a directory...you can't do nothing more.
			return False
		else:
			ret=subprocess.check_output(["umount","-l",chroot_dir+"/home/"])
					
			# unlinking /var/run/dbus
			#ret=subprocess.check_output(["rm", "-rf", chroot_dir+"/var/run/dbus"])
			#ret=subprocess.check_output(["mv", chroot_dir+"/var/run/dbus.bak", chroot_dir+"/var/run/dbus"])
			
			# unlink /var/lib/dbus/machine-id
			###ret=subprocess.check_output(["rm", "-rf", chroot_dir+"/var/lib/dbus/machine-id"])
			###ret=subprocess.check_output(["mv", chroot_dir+"/var/lib/dbus/machine-id.bak", chroot_dir+"/var/lib/dbus/machine-id"])
			
			
			return True
	#def remove_session
		
	
	##################

	# N4D Remote Logging Methods
	def prepare_log(self):
		import os
		
		if (os.path.isfile('/tmp/n4d_lstp_chroot.log')):
			print 'Deleting File /tmp/n4d_lstp_chroot.log'
			os.remove('/tmp/n4d_lstp_chroot.log')
			return 'True'
		# Clean log file
		return 'False'
		
		#[ ! -e /tmp/n4drmirror.log ] || rm  -f /tmp/n4drmirror.log
	# def  _prepare_log()
	
	def exist_log_file(self):
		if (os.path.isfile('/tmp/n4d_lstp_chroot.log')):
			return 'True'
		else:
			return 'False'
		#if [ -e /tmp/n4drmirror.log ] ; then
		#	echo "True"
		#else
		#	echo "False"
		#fi
	# def _exist_log_file


	# TODO 
	
	def get_json_images(self):
		import os
		import os.path
		import subprocess
		'''
		Return images installed on system.
		'''
		
		'''
		static values contains description of images and the place of img and chroot dirs.
		In further developts, and to enhace flexibility to manage multiple clients from
		same image, it can be placed in a config file, manageable by the user.
		'''
		static_values={"client":{"desc":"LliureX School Model appends traditional classroom model. In the classroom model, the IT classrooms form an independent network with a server to wich can connect workstation as well as thin clients. The new School Model, in addition, allows the interconnection of a variety of classrooms with the school server	.",
					 "name":"Classroom Client",
					 "img": "lliurex-client.png",
					 "image_file":"/opt/ltsp/images/llx-client.img",
					 "squashfs_dir":"/opt/ltsp/llx-client/"},
				"desktop":{"desc":"LliureX Desktop is the adaptation of the generic distribution LliureX designed for personal computers, the hall of teachers, secretaries, etc.. That is, is intended to be installed on computers that do not rely on a server (not found in the computer lab or in the library ...).",
					 "name":"LliureX Desktop",
					 "img": "lliurex-escriptori.png",
					 "image_file":"/opt/ltsp/images/llx-desktop.img",
					 "squashfs_dir":"/opt/ltsp/llx-desktop/"},
				"infantil":{"desc":"LliureX Infantil is the LliureX adaptation for First and Primary School.",
					 "name":"LliureX Infantil",
					 "img": "lliurex-infantil.png",
					 "image_file":"/opt/ltsp/images/llx-infantil.img",
					 "squashfs_dir":"/opt/ltsp/llx-infantil/"},
				"musica":{"desc":"LliureX Music the adaptation for multimedia computers with specific software needs for audio, video and multimedia.",
					 "name":"LliureX Music",
					 "img": "lliurex-musica.png",
					 "image_file":"/opt/ltsp/images/llx-musica.img",
					 "squashfs_dir":"/opt/ltsp/llx-musica/"},
				"pime":{"desc":"LliureX Pime is an adaptation that has been developed for use in vocational training families of Commerce Administration and Management and Marketing. Includes a selection of applications tailored to the business-oriented programs, without educational applications for Primary and Secondary Schools, as well as applications to support teaching. For this reasons, LliureX Pime is a good candidate for those SMEs (Small and Medium Enterprises) who want to introduces in the free software, especially for the Valencian Community, as the environment is translated into Catalan and Spanish, as in other adaptations LliureX.",
					 "name":"LliureX Pime",
					 "img": "lliurex-pime.png",
					 "image_file":"/opt/ltsp/images/llx-pime.img",
					 "squashfs_dir":"/opt/ltsp/llx-pime/"}
					}
		
		ret=[]
		'''img={"id": "tralari", "name": "tralari", "desc":"tralara",
			   "img": "wwwww", "image_file": "aaaaaaa", "squashfs_dir":"wwwwwwww",
			   "installed":22222.33333, "lliurex_version":"w2",
			   "errorcode":"qwqqq", "errormsg":"eeeeee"}
		
		ret.append(img)
		ret.append(img)'''
		
		for i in ["client", "desktop", "infantil", "musica", "pime"]:
			img_id=i
			img_name=static_values[i]["name"]
			img_desc=static_values[i]["desc"]
			img_img=static_values[i]["img"]
			img_file=static_values[i]["image_file"]
			img_squash=static_values[i]["squashfs_dir"]
			
			print "squash: "+img_squash;
			
			# Check if exists img file and gets the date
			if os.path.exists(img_file):
				img_installed=os.stat(img_file).st_mtime
				# Let's check if there is also directory and its lliurex-version
				if (os.path.isdir(img_squash)):
					print "is dir"
					try:
						# Direcroty exists, check chroot
						if (os.path.isfile('/tmp/llx-version-chroot.info')):
							os.remove('/tmp/llx-version-chroot.info')
						f = open('/tmp/llx-version-chroot.info', 'w')
						subprocess.check_call(["chroot",img_squash, "lliurex-version"],stdout=f) # to modify
						f.close()
						f = open('/tmp/llx-version-chroot.info', 'r')
						img_lliurex_version=f.readline();
						img_errorcode=None
						img_errormsg=None
						img_errortype=None
						
					except Exception as e:
						img_lliurex_version="unknown"
						img_errorcode="NO_LLIUREX_VERSION_IN_CHROOT"
						img_installed=None
						img_errormsg="Chroot image "+img_squash+" seems that has no a valid LliureX System installed. Could not get lliurex-version."
						img_errortype="ERROR"
						pass
					
				else: # img_sqash does not exists-> Error
					print ("is no dir")
					img_lliurex_version="unexistent";
					img_errorcode="NO_CHROOT_FOR_IMAGE"
					img_installed=None
					img_errormsg="Chroot folder "+img_squash+" does not exists. Maybe it's lost or corrupt."
					img_errortype="ERROR"
									
				
			else:
				# Check now it there was an chroot dir, but no img, so, there is an error
				if (os.path.isdir(img_squash)):
					print ("[N4d_LTSP_CHROOT] Chroot folder exists, but not image file. Crashed on installation. ")
					# Chech lliruex-version
					try:
						if (os.path.isfile('/tmp/llx-version-chroot.info')):
							os.remove('/tmp/llx-version-chroot.info')
						f = open('/tmp/llx-version-chroot.info', 'w')
						subprocess.check_call(["chroot",img_squash, "lliurex-version"],stdout=f) # to modify
						f.close()
						f = open('/tmp/llx-version-chroot.info', 'r')
						img_lliurex_version=f.readline();
						
						if(img_lliurex_version!=""):
							img_installed=None
							img_errorcode="NO_IMAGE_FOR_CHROOT_WITH_VERSION"
							img_errormsg="Client image "+img_file+" for chroot folder "+img_squash+" does not exists. It is hardly due to a failure in the packages installation. You can try to update system or regenerate image to solve it."
							img_errortype="WARNING"
						else:										
							img_lliurex_version="unexistent";
							img_installed=None
							img_errorcode="NO_IMAGE_FOR_CHROOT"
							img_errormsg="Client image "+img_file+" for chroot folder "+img_squash+" does not exists and there is not a valid LliureX Version in the folder. It is hardly due to a failure in the packages installation. Update mirror before install an image, please."
							img_errortype="ERROR"
					except Exception:
						img_lliurex_version="unexistent";
						img_installed=None
						img_errorcode="NO_IMAGE_FOR_CHROOT"
						img_errormsg="Client image "+img_file+" for chroot folder "+img_squash+" does not exists and there is not a valid LliureX Version in the folder. It is hardly due to a failure in the packages installation. Update mirror before install an image, please."
						img_errortype="ERROR"
						pass
					
				else:
					#print ("does not exists")
					img_installed=None
					img_lliurex_version=None
					img_errorcode=None
					img_errormsg=None
					img_errortype=None
			
			img={"id": img_id, "name": img_name, "desc":img_desc,
			   "img": img_img, "image_file": img_file, "squashfs_dir":img_squash,
			   "installed":img_installed, "lliurex_version":img_lliurex_version,
			   "errorcode":img_errorcode, "errortype":img_errortype, "errormsg":img_errormsg}

			ret.append(img)
		
		return {"images": ret}
		

#class LtspChroot

