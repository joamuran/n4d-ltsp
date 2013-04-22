#!/usr/bin/env python

# Libraries
import sys
import urllib
import logging
import logging.config
import time
import os

#import subprocess

class N4dRemoteLog:
  
  fd=None
  
  def info(self):
    '''
    Show basic info about this plugin
    '''	
    return {'status':True, 'msg':'[N4dRemoteLog] Manage remote logs'}
  
  #def info
  
  
  
  def __init__(self):
    pass    
  
  def create_logging_server(self, log_server, port=9999 ):
    '''
    Create the loggin server on the custom port
    '''
    t = logging.config.listen(port)
    t.start()
    
    logger = logging.getLogger(log_server)
    
    try:
      # Loop while true
      while True:
        logger.debug('debug message')
        logger.info('info message')
        logger.warn('warn message')
        logger.error('error message')
        logger.critical('critical message')
        time.sleep(5)
    
    except Exception:
      logging.config.stopListening()
      t.join()

  
  
  def write_log(self, text):
    '''
    Write the text to the log and publish it at Loggin System
    '''
    
    pass

  
  def read_log(self, line):
    pass
  

  


  


