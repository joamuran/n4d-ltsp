#!/usr/bin/python

# Libraries
import sys
import re
#import subprocess

class Client:
  def __init__(self, mac):
    self.mac=mac
    self.type="fat"
    self.desc=""
    self.name=""
    self.session="gnome"
    self.monitor="auto" # Deprecated
    self.autologin="unchecked"
    self.username=""
    self.userpass=""
  def set_type(self, clienttype):
    self.type=clienttype
  def set_name(self, name):
    self.name=name
  def set_desc(self, desc):
    self.desc=desc
  def set_session(self, session):
    self.session=session
  def set_monitor(self, monitor):
    self.monitor=monitor
  def set_autologin(self, autologin):
    self.autologin=autologin
  def set_username(self, username):
    self.username=username
  def set_usernpass(self, userpass):
    self.userpass=userpass
  def get_client(self):
    client='{'
    client=client + '"mac":"'+self.mac+'"'
    client=client + ',"type":"'+self.type+'"'
    client=client + ',"name":"'+self.name+'"'
    client=client + ',"desc":"'+self.desc+'"'
    client=client + ',"session":"'+self.session+'"'
    client=client + ',"monitor":"'+self.monitor+'"'
    client=client + ',"autologin":"'+self.autologin+'"'
    client=client + ',"username":"'+self.username+'"'
    client=client + ',"userpass":"'+self.userpass+'"}'
    return client



class LtspClientConfig:
    
  def __init__(self):
    '''
    A simple init method
    '''
    self.conf_file="/var/lib/tftpboot/ltsp/lts.conf"
    self.client_list=[]
    
    pass    
  #def init

  def get_ltsp_conf(self):
    '''
    Returns parsed lts.conf config file
    This file is usually /var/lib/tftpboot/ltsp/lts.conf
    '''
    self.current_section=""
    self.current_client=None

    lines=open(self.conf_file, 'r').readlines();
    for line in lines:
      line=line.strip()
      #First, let's see if is not a comment
      if len(line)>0 and line[0]!="#":
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
              self.current_client.set_type=line[15:]
              #print "FatClient: "+line[15:]
            if line[:8]=="HOSTNAME":
              self.current_client.set_name=line[10:]
              #print "host: "+line[10:]
            if line[:8]=="LDM_SESS":
              self.current_client.set_session=line[12:]
              #print "session: "+line[12:]
            if line[:8]=="LDM_AUTO":
              self.current_client.set_autologin=line[14:]
              #print "Autologin: "+line[14:]
            if line[:8]=="LDM_USER":
              self.current_client.set_username=line[13:]
              #print "username: "+line[13:]
            if line[:8]=="LDM_PASS":
              self.current_client.set_userpass=line[13:]
              #print "password: "+line[13:]
            
            #print line[:7]
           #print self.current_section+"> "+line
    # END for line in lines:
    if self.current_client is not None:
      # Write the last client
      self.client_list.append(self.current_client)
  
    config='{"clients":['
    index=0
    for cl in self.client_list:
      myclient=cl.get_client()
      config=config+myclient
      # Adding "," if there are more elements
      index=index+1
      if index<len(self.client_list):
        config=config+','
    config=config+']'
     
    return config 
    
  
  def set_ltsp_conf(self, config):
    pass
  
client=LtspClientConfig()
conf=client.get_ltsp_conf()
print conf