import os
import shutil


class n4dPXEManager:
   def getImageList(self):
      listimages=[]
      timeout=60

      f=open("/var/lib/tftpboot/ltsp/pxelinux.cfg/default", "r")
      lines=(f.read()).split("\n")
      lastline=""
      
      for line in lines:
         
         if ("TIMEOUT" in line.upper()):
            timeout=line.replace("TIMEOUT ", "")
         
         if ("MENU DEFAULT" in line.upper()):
            default=lastline
            #default=line.replace("LABEL ", "")
         
         if (("LABEL" in line.upper())and not("MENU" in line.upper()) and ("Instal.la LliureX en aquest ordinador") not in line):
            listimages.append(line.replace("LABEL ", ""));
            lastline=line.replace("LABEL ", "")
      
      
      return {'timeout':timeout,'images':listimages, 'default':default}

   def setImageDefaultBoot(self, default, timeout):
      f=open("/var/lib/tftpboot/ltsp/pxelinux.cfg/default", "r")
      
      f2=open("/tmp/default", "w")
      
      lines=(f.read()).split("\n")
      
      for line in lines:
         if ("TIMEOUT " in line.upper()):
            f2.write("TIMEOUT "+timeout+"\n")
            #print "TIMEOUT "+timeout
         else:
            if not("MENU DEFAULT" in line.upper()):
               f2.write(line+"\n")
               #print line
            
            if (("LABEL" in line.upper())and not("MENU" in line.upper()) and ("Instal.la LliureX en aquest ordinador") not in line):
               if (line.replace("LABEL ", "")==default):
                  f2.write("    MENU default\n")
                  #print "    MENU default"
      f.close()
      f2.close()
      shutil.copy("/tmp/default", "/var/lib/tftpboot/ltsp/pxelinux.cfg/default")
         
#myselector=n4dPXEManager()
#mylist=myselector.getImageList()
#
#print mylist
#print "defualt is "+mylist["default"]
#
#myselector.setImageDefaultBoot(mylist["default"], mylist["timeout"])
#print "\n\n\n"
#myselector.setImageDefaultBoot("localboot", "20")
