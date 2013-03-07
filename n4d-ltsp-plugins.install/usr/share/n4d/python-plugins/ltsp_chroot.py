#!/usr/bin/python
# This script is licensed under GPL v3 or higher
#
# Author: Angel Berlanas Vicente 
#         <angel.berlanas@gmail.com>
#
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
    if not os.path.isdir(chroot_dir):
      return {'status': True, 'msg':'[N4dChroot] Directory not existent'}

  #def test_chroot(self, chroot_dir)
 
  def get_lliurex_version_on_chroot(self, chroot_dir):
    '''
    get the LliureX Version of chroot given.
    '''
    if not self.test_chroot(chroot_dir)["status"] :
      # If not a directory...you can't do nothing more.
      return {'status': False, 'msg':'[N4dChroot] Directory not existent'}

    else :
      # Ok, this is a directory. 
      lliurex_version=subprocess.check_output(["chroot",chroot_dir,"lliurex-version"])
      return {'status': True, 'msg':'[N4dChroot] '+lliurex_version }     
	
  #def get_lliurex_version_on_chroot(self, chroot_dir):

#class LtspChroot

