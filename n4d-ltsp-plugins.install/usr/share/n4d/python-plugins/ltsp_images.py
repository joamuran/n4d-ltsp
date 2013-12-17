#!/usr/bin/python
# This script is licensed under GPL v3 or higher
#
# Authors: Angel Berlanas Vicente 
#          <angel.berlanas@gmail.com>
#	   Jose Alfredo Murcia Andres
#	   <joamuran@gmail.com>
#

# Libraries
import sys
import subprocess



class LtspImage:
	
	llx_ltsp_status="available"
	llx_ltsp_status_msg=""
	
	def __init__(self):
		'''
		A simple init method
		'''
		print "[LTSPImage] Setting LTSP Status: Available"
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
		return {'status':True, 'msg':'[LtspImage] Info'}
	#def info 
	
	def create_desktop(self):
		'''
		Create a Desktop image for LTSP system
		'''
		try:
			self.llx_ltsp_status_msg=subprocess.check_output(["lliurex-ltsp-create-client","desktop"])
			return {'status': True, 'msg':'[LtspImage] Desktop is created'}
		except Exception as e:
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
		
	#def create_desktop
	
	def create_client(self):
		'''
		Create a Client image for LTSP system
		'''
		try:
			self.llx_ltsp_status_msg=subprocess.check_output(["lliurex-ltsp-create-client","client"])
			return {'status': True, 'msg':'[LtspImage] Client is created'}
		except Exception as e:
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
		
	#def create_desktop
	
	def create_infantil(self):
		'''
		Create a Infantile image for LTSP system
		'''
		try:
			self.llx_ltsp_status_msg=subprocess.check_output(["lliurex-ltsp-create-client","infantil"])
			return {'status': True, 'msg':'[LtspImage] Infantile is created'}
		except Exception as e:
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
		
	#def create_desktop
	
	
	def create_musica(self):
		'''
		Create a Music  image for LTSP system
		'''
		try:
			self.llx_ltsp_status_msg=subprocess.check_output(["lliurex-ltsp-create-client","musica"])
			return {'status': True, 'msg':'[LtspImage] Music is created'}
		except Exception as e:
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
		
	#def create_desktop
	
	def create_pime(self):
		'''
		Create a Pime image for LTSP system
		'''
		try:
			self.llx_ltsp_status_msg=subprocess.check_output(["lliurex-ltsp-create-client","pime"])
			return {'status': True, 'msg':'[LtspImage] PIME is created'}
		except Exception as e:
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
		
	#def create_desktop
	
	def run_Image_Command(self, command, XServerIP, display, XephyPID):
		'''
		runs command in server to work with images
		'''
		#import time
		print "Performing command: "+command
		print "Status: "+self.llx_ltsp_status
		

		try:
			# Cleaning apt cache from chroot
			command_orig=command.split(" ")[0]
			command_param=command.split(" ")[1]
			if (command_orig=="ltsp-update-image"):
				output=subprocess.check_output(["chroot", command_param, "apt-get", "clean"])

				
			# Now prepare the appropiate scripts in server
			xscript="/tmp/image_script.sh"
			print "Building file: "+xscript
			f = open(xscript, 'w')
			f.write("#/bin/bash\n\n")
			f.write("export HOME=/root\n")	
			f.write("export DISPLAY="+XServerIP+display+"\n")
			#eval "xterm -geometry 79x27+10+15 -hold -fa 'default' -e 'apt-get update; \
			#apt-get install lliurex-ltsp-client; \
			#echo;echo;echo;echo Hem finalitzat.Taqueu la finestra per continuar. ;echo;echo;exit 0'"
			#f.write("dbus-launch --exit-with-session gnome-terminal -x sh -c \" "+command+"; \
			#	zenity --info --text 'Operation Finished. Click to close.'; \
			#	 n4d-client -h "+XServerIP+" -c ltspClientXServer -m killXephyr -a "+XephyPID+"\"\n")
			#f.write("echo 7\n")
			f.write("dbus-launch --exit-with-session xterm -geometry 79x27+10+15 -hold -fa 'default' -e \" "+command+"; \
				zenity --info --text 'Operation Finished. Click to close.'; \
				 n4d-client -h "+XServerIP+" -c ltspClientXServer -m killXephyr -a "+XephyPID+"\"\n")
			
			f.write("exit 0\n ")
			
			f.close()
		
			subprocess.Popen(["chmod","+x", xscript])
			output=subprocess.check_output(["bash", "/tmp/image_script.sh"])
		
				
		
		
			
						
			return {'status': True, 'msg':'[LtspImage] img updated'}
		except Exception as e:
			self.llx_ltsp_status="available"
			f.close()
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
	
	
	def regenerate_img(self, imgchroot):
		'''
		Regenerates img file for chroot
		'''
		import time
		print "Regenerating image from "+imgchroot
		print "Status: "+self.llx_ltsp_status
	
		try:
			dirs=imgchroot.split("/")
			print "*"+imgchroot+"*"
			print str(dirs)
			img_name=dirs[len(dirs)-1]
			if (img_name==''):
				img_name=dirs[len(dirs)-2]
						
			self.llx_ltsp_status="working"
			f = open('/tmp/n4drlstpimages.log', 'w')
			
			# Regenerate image
			f.write("[llxptspmsg] Regenerating image\n")
			f.flush()
			#self.llx_ltsp_status_msg=subprocess.check_call(["ls","-l"],stdout=f) # to modify
			#self.llx_ltsp_status_msg=subprocess.check_call(["echoprogress"],stdout=f) # to modify
			#self.llx_ltsp_status_msg=subprocess.check_call(["ls","-l"],stdout=f) # to modify
			#self.llx_ltsp_status_msg=subprocess.check_call(["echoprogress"],stdout=f) # to modify
			
			#self.llx_ltsp_status_msg=subprocess.check_call(["cat","/tmp/tralari.log"],stdout=f) # to modify

			self.llx_ltsp_status_msg=subprocess.check_call(["ltsp-update-image",img_name],stdout=f) # to modify
			
			#f.write(ret)
			self.llx_ltsp_status="available"
			f.close()
						
			return {'status': True, 'msg':'[LtspImage] img updated'}
		except Exception as e:
			self.llx_ltsp_status="available"
			f.close()
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
	
	#def regenerate_img
		
	####################
	####################
	# BEGGINING PARTY
	####################
	
	def n4d_create_client(self, clientid, imgchroot):
		'''
		Regenerates img file for chroot
		'''
		
		print ("Create image "+ clientid +" image from "+imgchroot)
		print ("Status: "+self.llx_ltsp_status)
		
		try:
			self.llx_ltsp_status="working"
			f = open('/tmp/n4drlstpimages.log', 'w')
			
			self.llx_ltsp_status_msg=subprocess.check_call(["lliurex-ltsp-create-client", clientid],stdout=f) # to modify
			
			
			self.llx_ltsp_status="available"
			f.close()
						
			return {'status': True, 'msg':'[LtspImage] Desktop is created'}
		except Exception as e:
			# Close file and set status available
			self.llx_ltsp_status="available"
			f.close()
			
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
	
	#def regenerate_img
	
	
	def is_enough_space_in_disk(self, imgchroot):
		import os
		return {'status':True, 'free':'12300', 'used': '100'}
		'''
		# Calculate chroot size
		total_size = 0
		start_path=imgchroot
		for dirpath, dirnames, filenames in os.walk(start_path):
			for f in filenames:
				fp = os.path.join(dirpath, f)
				if os.path.exists(fp):
					total_size += os.stat(fp).st_size
		
		# Calculate free space... in opt and /
		
		stat=os.statvfs("/opt/ltsp")
		free=stat.f_bsize*stat.f_bavail
		
		if(free<total_size):
			return {'status':False, 'free':str(free), 'used': str(total_size)}
		else:
			return {'status':True, 'free':str(free), 'used': str(total_size)}
		'''	
	
	def n4d_update_client(self, clientid, imgchroot, username, password):
		'''
		Regenerates img file for chroot
		'''
		
		# Prepare for chroot first
		### ... prepare_chroot_for_run(imgchroot) -> En Classe ltsp chroot!!
		# o ho pose aci, o me cree altra instancia de ltspchroot, o va a la
		# llibreria o directament la utilitze per n4d!!!!!!<---

		connection_user=(username, password)
		
		print "Updating image "+clientid+" from "+imgchroot
		print "Status: "+self.llx_ltsp_status
		
		try:
			self.llx_ltsp_status="working"
			f = open('/tmp/n4drlstpimages.log', 'w')
			f.write("[llxptspmsg] Stage 1 of 2. Updating client\n")
			f.flush()
			
			# Prepare for operate into chroot via n4d
			server = ServerProxy("https://127.0.0.1:9779")
			print str(connection_user)+str()
						
			print str(imgchroot)
			
			server.prepare_chroot_for_run(connection_user,"LtspChroot", imgchroot)
			# Update chroot			
			self.llx_ltsp_status_msg=subprocess.check_call(["chroot",imgchroot,"lliurex-upgrade"],stdout=f) # to modify
			
			# Umount chroot
			server.umount_chroot(connection_user,"LtspChroot", imgchroot)
			
			# Regenerate image
			f.write("[llxptspmsg] Stage 2 of 2. Regenerating image\n")
			f.flush()
			self.llx_ltsp_status_msg=subprocess.check_call(["ltsp-update-image",clientid],stdout=f) # to modify
			
			#f.write(ret)
			self.llx_ltsp_status="available"
			f.close()
						
			return {'status': True, 'msg':'[LtspImage] img updated'}
		except Exception as e:
			self.llx_ltsp_status="available"
			f.close()
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
	
	#def n4d_update_client
	
	def n4d_delete_client(self, clientid, imgchroot, img_file, connection_user):
		'''
		Remove an LTSP image and its chroot
		'''
		import os
		import shutil
		
		print ("Delete Client "+clientid+" from "+imgchroot+" and "+img_file)
		
		print ("Status: "+self.llx_ltsp_status)
		
		try:
			self.llx_ltsp_status="working"
			#f = open('/tmp/n4drlstpimages.log', 'w')
			#f.write('tralari')
			
			#f.write("Deleting "+img_file+"...\n")
			#f.flush()
			if (os.path.isfile(img_file)):
				os.remove(img_file)
			#	f.write("Deleted "+img_file+"...\n")
			#else:
			#	f.write(img_file+" did not exists...\n")
			#f.flush()
				
			#f.write("Deleting "+imgchroot+"...\n")
			#f.flush()
			
			if (os.path.isdir(imgchroot)):
				# umount chroot
				server = ServerProxy("https://127.0.0.1:9779")
			#	f.write("Umounting devices...\n")
				server.force_umount_chroot(connection_user,"LtspChroot", imgchroot)
				#server.umount_chroot(connection_user,"LtspChroot", imgchroot)
				# Now delete...
			#	f.write("Deleting...\n")
				shutil.rmtree(imgchroot)
			#	f.write("Deleted "+imgchroot+"...\n")
			#else:
			#	f.write(imgchroot+" did not exists...\n")
			
			#f.write("chroot doens't exists yet...\n")
			
			tftpdir='/var/lib/tftpboot/ltsp/'+imgchroot.split("/")[3]
			
			#f.write("Deleting tftpdir:"+tftpdir+"...\n")
			#f.flush();	 			
		
		
			if(os.path.isdir(tftpdir)):
				shutil.rmtree(tftpdir)
			#	f.write("Deleted "+tftpdir+"...\n")
			#else:
			#	f.write(tftpdir+"did not exists...\n")
		
			#f.write("Regenerate menus... \n")
			#f.flush()
			self.llx_ltsp_status_msg=subprocess.check_call(["/usr/share/lliurex-ltsp/llx-create-pxelinux.sh"],stdout=None) # to modify
			
			#f.write("Finished !\n")
			#f.flush()
			
			self.llx_ltsp_status="available"
			#f.close()
						
			return {'status': True, 'msg':'[LtspImage] img updated'}
		except Exception as e:
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
	
	#def regenerate_img
	
	
	def n4d_install_xfce(self, clientid, imgchroot, connection_user):
		'''
		Installs XFCE into client
		'''
		
		print "Installing XFCE for "+clientid+" into "+imgchroot
		print "Status: "+self.llx_ltsp_status
		
		try:
			
			self.llx_ltsp_status="working"
			f = open('/tmp/n4drlstpimages.log', 'w')
			
			# Prepare for operate into chroot via n4d
			server = ServerProxy("https://127.0.0.1:9779")
			server.prepare_chroot_for_run(connection_user,"LtspChroot", imgchroot)
		
			# Install XFCE
			self.llx_ltsp_status_msg=subprocess.check_call(["apt-get","install","lliurex-cdd-xdesktop"],stdout=f) # to modify
			#f.write(ret)
			self.llx_ltsp_status="available"
			
			# Umount chroot
			server.umount_chroot(connection_user,"LtspChroot", imgchroot)
			
			f.close()
						
			return {'status': True, 'msg':'[LtspInstallXFCE] xfce installed'}
		except Exception as e:
			return {'status': False, 'msg':'[LtspInstallXFCE] Error'+str(e)}
	
	#def n4d_install_xfce
		
	
	####################
	####################
	# END PARTY
	####################
	
	
	
	
	
	# N4D Remote Logging Methods
	def prepare_log(self):
		import os
		
		if (os.path.isfile('/tmp/n4drlstpimages.log')):
			print 'Deleting File /tmp/n4drlstpimages.log'
			os.remove('/tmp/n4drlstpimages.log')
			return 'True'
		# Clean log file
		return 'False'
		
		#[ ! -e /tmp/n4drmirror.log ] || rm  -f /tmp/n4drmirror.log
	# def  prepare_log()
	
	def exist_log_file(self):
		if (os.path.isfile('/tmp/n4drlstpimages.log')):
			return 'True'
		else:
			return 'False'
		#if [ -e /tmp/n4drmirror.log ] ; then
		#	echo "True"
		#else
		#	echo "False"
		#fi
	# def exist_log_file

	def get_status(self):
		if (self.llx_ltsp_status=="available"):
			return "{'status':'available','msg':'Ltsp Images is ready'}"
		else:
			return "{'status':'busy','msg':'LTSP Images is busy'}"
		pass
	


	# TODO 
	
	
	
#class LtspImage:
