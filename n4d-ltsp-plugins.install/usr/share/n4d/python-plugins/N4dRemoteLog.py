#!/usr/bin/env python

# Libraries
import sys
import time
import os
import lliurex.net
#import subprocess


class N4dRemoteLog:
  
  fd=None
  LOG_PATH="/tmp/"
  LOG_PREFIX="n4dr"
  
  def info(self):
    '''
    Show basic info about this plugin
    '''	
    return {'status':True, 'msg':'[N4dRemoteLog] Manage remote logs'}
  
  #def info

  def __init__(self):
    pass    
  # def __init__
    
  
  def read_n4dr_log(self, log_name, line_start, line_nums):
    '''
    Read logging from server passed as name.
    Starting at the line_start argument to the line_start+line_nums
    If the end of file is foundit returns all file.
    
    If only filename is passed (and None None), the entire file is
    sended
    '''
    log_name_fullpath=N4dRemoteLog.LOG_PATH+N4dRemoteLog.LOG_PREFIX+log_name+".log"
    
    if line_start != None and line_nums != None:
      line_start=int(line_start)
      line_end=int(line_start)+int(line_nums)
      if os.path.exists(log_name_fullpath):
        lines = open(log_name_fullpath, 'r').readlines()[line_start:line_end]
    else:
      if os.path.exists(log_name_fullpath):
        lines = open(log_name_fullpath, 'r').readlines()
        
    print(lines)
    
    return {'status':True, 'file':lines}
  #def read_log_lines_from_server(self, filename, line_start, line_nums)
  
  def write_n4dr_log(self,log_name,log_msg):
    '''
    Write the log_msg to the ip_to_write with the logname
    '''
    if log_msg != None :
        log_name_fullpath=N4dRemoteLog.LOG_PATH+N4dRemoteLog.LOG_PREFIX+log_name+".log"
        print log_name_fullpath
        try:
            f=open(log_name_fullpath,'a')
            f.write(log_msg+"\n")
            f.close()
        except Exception as e:
            return {'status':False, 'msg':str(e)}
    
    return {'status':True, 'file':str(log_name)}
  
if __name__ == '__main__':
  
  n4dLog = N4dRemoteLog()


  

