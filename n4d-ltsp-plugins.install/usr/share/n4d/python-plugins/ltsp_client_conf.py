#!/usr/bin/python

# Libraries
import sys
import re
import json
import urllib

#import subprocess

class Client:
  def __init__(self, mac):
    self.mac=mac
    self.fat="true"
    self.desc=""
    self.name=""
    self.session="gnome"
    self.monitor="auto" # Deprecated
    self.autologin="unchecked"
    self.username=""
    self.userpass=""
    
  def set_type(self, param):
    self.fat=param  
  def set_name(self, param):
    self.name=param
  def set_desc(self, param):
    self.desc=param
  def set_session(self, param):
    self.session=param
  def set_monitor(self, param):
    self.monitor=param
  def set_autologin(self, param):
    self.autologin=param
  def set_username(self, param):
    self.username=param
  def set_userpass(self, param):
    self.userpass=param
  def get_client(self):
    client='{'
    client=client + '"mac":"'+self.mac+'"'
    client=client + ',"fat":"'+self.fat+'"'
    client=client + ',"name":"'+self.name+'"'
    client=client + ',"desc":"'+self.desc+'"'
    client=client + ',"session":"'+self.session+'"'
    client=client + ',"monitor":"'+self.monitor+'"'
    client=client + ',"autologin":"'+self.autologin+'"'
    client=client + ',"username":"'+self.username+'"'
    client=client + ',"userpass":"'+self.userpass+'"}'
    #print "*"
    #print client
    #print "!"
    return client



class LtspClientConfig:
    
  def __init__(self):
    '''
    A simple init method
    '''
    self.conf_file="/var/lib/tftpboot/ltsp/i386/lts.conf"
    self.client_list=[]
    self.default_session="gnome"
    self.default_type="thin"
    self.use_nbd="false"
    self.swap=0
    
    pass    
  #def init

  def get_ltsp_conf(self):
    '''
    Returns parsed lts.conf config file
    This file is usually /var/lib/tftpboot/ltsp/i386/lts.conf
    '''
    self.current_section=""
    self.current_client=None
    self.client_list=[]

    lines=open(self.conf_file, 'r').readlines();
    for line in lines:
      line=line.strip()
      #First, let's see if is not a comment
      if len(line)>0 and line[0]!="#":
        #print "line: "+line
        # Let's see if it's a section definition...
        if line[0]=="[":
          # is default section?
          if line.lower()=="[default]":
            self.current_section="default"
            pass
          # is a MAC?
          elif re.match('^\s*\[([a-fA-F0-9]{2}[:|\-]?){6}\]\s*$',line):
            self.current_section=line[1:-1]
            # Create a client object
            if self.current_client is not None:
              # Add the current client to list
              self.client_list.append(self.current_client)
            # Create a new section with this MAC
            self.current_client=Client(self.current_section)
            
          else: # Otherwise, ignore it
            self.current_section=""
            
        # if it is not a section definition, it's a parameter
        else:
          if self.current_section!="" and self.current_section!="default":
            if line[:8]=="LTSP_FAT":
              self.current_client.set_type(urllib.quote(line[15:]))
              #print "FatClient: "+line[14:]
            if line[:8]=="HOSTNAME":
              self.current_client.set_name(urllib.quote(line[9:]))
              #print "host: "+line[9:]
            if line[:8]=="LDM_SESS":
              #print "SESSION: "+line[13:18].strip()
              if line[13:18]=="gnome":
                self.current_client.set_session("gnome")
              else:
                self.current_client.set_session("xfce")
              #print "session: "+line[12:]
            if line[:8]=="LDM_AUTO":
              #print "Autologin: "+line[14:]
              if line[14:].strip()=="True":
                self.current_client.set_autologin("checked")
              else:
                  self.current_client.set_autologin("unchecked")
              #print "Autologin: "+line[14:]
            if line[:8]=="LDM_USER":
              self.current_client.set_username(urllib.quote(line[13:]))
              #print "username: "+line[13:]
            if line[:8]=="LDM_PASS":
              self.current_client.set_userpass(urllib.quote(line[13:]))
              #print "password: "+line[13:]
            
            #print line[:7]
            #print self.current_section+"> "+line
          elif self.current_section=="default":
            
            # Get Parameters for default section
            
            if line[:8]=="NBD_SWAP":
              self.use_nbd=urllib.quote(line[9:])
              if (self.use_nbd.lower()=="true"):
                # Read /etc/ltsp/nbdswap.conf
                try:
                  nbd_lines=open('/etc/ltsp/nbdswapd.conf', 'r').readlines()
                  nbd_line=(nbd_lines[0]).strip()
                  self.swap=nbd_line[5:]
                  
                except Exception as e:
                  self.swap=0
              else:
                self.swap=0
                
              #print("[LTSP_CLIENT_CONF:GET_LTSP_CONF] use swap: "+self.use_nbd+" amount: *"+str(swap)+"*")
              
            if line[:8]=="LTSP_FAT":
              is_fat=urllib.quote(line[15:])
              #self.default_type=urllib.quote(line[15:])
              #print "||"+self.default_type+"||"
              #print "||"+str(type(self.default_type))+"||"
              #if self.default_type=="true":
               #   print "set default type is true"
              #else:
               #   print "set default type is NOT true"
  
             # if self.default_type=="false":
               #   print "set default type is FALSE"
              #else:
               #   print "set default type is NOT FALSE"
  
              if is_fat=="true":
                  self.default_type="fat"
              else:
                  self.default_type="thin"

            if line[:8]=="LDM_SESS":
              if line[13:18]=="gnome":
                self.default_session="gnome"
              else:
                self.default_session="xfce"
      else: ##if len(line)>0 and line[0]!="#":
        if len(line)>0 and line[:8]=="#LLX-Des":
          self.current_client.set_desc(urllib.quote(line[10:]))

    # END for line in lines:
    if self.current_client is not None:
      # Write the last client
      self.client_list.append(self.current_client)
  
    '{"default_type":"fat", "default_session":"gnome"}'
    config='{"default_type":"'+self.default_type+'", "default_session":"'+self.default_session+'","nbd_swap":"'+self.use_nbd+'", "size":"'+str(self.swap)+'",'
    config=config+'"clients":['
    index=0
    for cl in self.client_list:
      myclient=cl.get_client()
      config=config+myclient
      # Adding "," if there are more elements
      index=index+1
      if index<len(self.client_list):
        config=config+','
    config=config+']}'
     
    return config 
    
  
  def set_ltsp_conf(self, config, class_type, class_session, use_nbd_swap, nbd_swap_size):
    print "Going to save..."+config
    self.new_conf_file="/var/lib/tftpboot/ltsp/i386/lts.conf"
    self.template_file="/var/lib/lliurex-ltsp/templates/lts.conf"
    readlines=open(self.template_file, 'r').readlines();
    writefile=open(self.new_conf_file, 'w');
    for line in readlines:
      writefile.write(line)

    writefile.write("\n# Default Session for classroom")
    if(class_session=="gnome"):
      writefile.write('\nLDM_SESSION="gnome-session-fallback"')
    else:
      writefile.write('\nLDM_SESSION=/usr/bin/xfce4-session')

    writefile.write("\n# Default Classroom type")
    if(class_type=="fat"):
      writefile.write("\nLTSP_FATCLIENT=true")
    else:
      writefile.write("\nLTSP_FATCLIENT=false")
    
    print ("SWAP: "+use_nbd_swap+"-"+nbd_swap_size)
    
    writefile.write("\n# Using NBD swap")
    if(use_nbd_swap=="True"):
      writefile.write("\nNBD_SWAP=True")
      print("111")
      swapfile=open("/etc/ltsp/nbdswapd.conf", 'w')
      print("222")
      swapfile.write("SIZE="+nbd_swap_size)
      print("333")
      swapfile.close()
      
    else:
      writefile.write("\nNBD_SWAP=False")
    


    clientlist=json.loads(config)
    for client in clientlist["clients"]:
      writefile.write("\n\n["+client["mac"]+"]")
      if client["desc"]!="":
        writefile.write("\n#LLX-Desc="+client["desc"])
      if client["name"]!="":
        writefile.write("\nHOSTNAME="+client["name"])
      if client["fat"]!="":
        writefile.write("\nLTSP_FATCLIENT="+client["fat"])
      if client["session"]=="gnome":
        writefile.write('\nLDM_SESSION="gnome-session-fallback"')
      elif client["session"]=="xfce":
        writefile.write('\nLDM_SESSION=/usr/bin/xfce4-session')
      # ignoring monitor
      if client["autologin"]=="checked":
        writefile.write('\nLDM_AUTOLOGIN=True')
      if client["username"]!="":
        writefile.write("\nLDM_USERNAME="+client["username"])
      if client["userpass"]!="":
        writefile.write("\nLDM_PASSWORD="+client["userpass"])


client=LtspClientConfig()
print client.get_ltsp_conf()
#conf=client.set_ltsp_conf('{"clients":[{"mac":"A1:B1:C2:D4:E5:F6","fat":"true","name":"n1","desc":"desc1","session":"gnome","monitor":"auto","autologin":"unchecked","username":"","userpass":""},{"mac":"A1:B1:C2:D4:E5:F6","fat":"true","name":"","desc":"","session":"lxde","monitor":"auto","autologin":"checked","username":"user","userpass":"123"}]}')
#print conf

