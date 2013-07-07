import os
import shutil

class n4dLTSPNetinstall:

   netinstalldir="/var/lib/tftpboot/ltsp/netinstall"
   mainmenufile="/var/lib/tftpboot/ltsp/pxelinux.cfg/default"
   def __init__(self):
      '''
      Simple constructor
      '''
      pass
   
   def is_netinstall_available(self):
      f=open(self.mainmenufile, "r")
      lines=(f.read()).split("\n")
      
      for line in lines:
         if "Netinst" in line:
            return True
         
      return False
   
   def is_netinstall_installed(self):
      if os.path.exists(self.netinstalldir):
         return True
      else:
         return False
      pass
   
   def set_netinstall_installable(self):
      with open(self.mainmenufile, "a") as f:
         f.write("# Netinst: Install Menu \n\
LABEL Instal.la LliureX en aquest ordinador\n\
   MENU LABEL Instal.la LliureX en aquest ordinador\n\
   KERNEL netinstall/ubuntu-installer/i386/boot-screens/vesamenu.c32\n\
   CONFIG netinstall/pxelinux.cfg/default netinstall/\n")

      return True
   
   def unset_netinstall_installable(self):
      try:
      
         file_input = open(self.mainmenufile, 'r').read().split('\n')
         file_output=open("/tmp/default", "w")
         for line in file_input:
            if ("Netinst" in line):
               file_output.close()
               self.copyTempFile()
               return {'status':True, 'msg':'done'}
            
            file_output.write(str(line)+"\n")
            
         file_output.close()
         
         # Not configured, we don't have to save it
         return {'status':True, 'msg':'not configured'} # netinst was not installable
      
      except Exception as e:
         return str(e)
      

   def copyTempFile(self):
      try:
         if(os.path.isfile("/tmp/default")):
            shutil.copyfile("/tmp/default", self.mainmenufile)
         
      except Exception as e:
         return srt(e)
   
   














