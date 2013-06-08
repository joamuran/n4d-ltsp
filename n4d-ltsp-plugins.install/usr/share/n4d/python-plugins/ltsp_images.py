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


class LtspImage:
	
	
	llx_ltsp_status="available"
	
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
			ret=subprocess.check_output(["lliurex-ltsp-create-client","desktop"])
			return {'status': True, 'msg':'[LtspImage] Desktop is created'}
		except Exception as e:
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
		
	#def create_desktop
	
	def create_client(self):
		'''
		Create a Client image for LTSP system
		'''
		try:
			ret=subprocess.check_output(["lliurex-ltsp-create-client","client"])
			return {'status': True, 'msg':'[LtspImage] Client is created'}
		except Exception as e:
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
		
	#def create_desktop
	
	def create_infantil(self):
		'''
		Create a Infantile image for LTSP system
		'''
		try:
			ret=subprocess.check_output(["lliurex-ltsp-create-client","infantil"])
			return {'status': True, 'msg':'[LtspImage] Infantile is created'}
		except Exception as e:
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
		
	#def create_desktop
	
	
	def create_musica(self):
		'''
		Create a Music  image for LTSP system
		'''
		try:
			ret=subprocess.check_output(["lliurex-ltsp-create-client","musica"])
			return {'status': True, 'msg':'[LtspImage] Music is created'}
		except Exception as e:
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
		
	#def create_desktop
	
	def create_pime(self):
		'''
		Create a Pime image for LTSP system
		'''
		try:
			ret=subprocess.check_output(["lliurex-ltsp-create-client","pime"])
			return {'status': True, 'msg':'[LtspImage] PIME is created'}
		except Exception as e:
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
		
	#def create_desktop
	
	def regenerate_img(self, imgchroot):
		'''
		Regenerates img file for chroot
		'''
		
		print "Regenerating image from "+imgchroot
		print "Status: "+self.llx_ltsp_status
		
		try:
			self.llx_ltsp_status="working"
			f = open('/tmp/n4drlstpimages.log', 'w')
			f.write('tralari')
			#ret=subprocess.check_output(["ls","/tmp"]) # to modify
			#ret=subprocess.check_output(["ls","/"]) # to modify
			ret=subprocess.call(["apt-get","update"],stdout=f) # to modify
			#f.write(ret)
			self.llx_ltsp_status="available"
			f.close()
						
			return {'status': True, 'msg':'[LtspImage] img updated'}
		except Exception as e:
			return {'status': False, 'msg':'[LtspImage] Error'+str(e)}
	

	#def regenerate_img
		
	
	
	
	
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