#!/usr/bin/env python
# coding = utf-8

# Import the libraries
from xmlrpclib import *
import sys

# Fix info for user at example
user="user"
password="password"


# Simple mechanism to support given the user and password as a arguments
# this is a not "production mechanism".

try:

  # Get the user
  if (sys.argv[0]): 
    user=sys.argv[0]

  # Get the password
  if (sys.argv[1]):
    password = sys.argv[1]

except Exception as e:
  print("Exception is ocurred, default user password is set")


user_info=(user,password)
print ("[DEBUG] :: " + str(user_info))
server = ServerProxy ("https://localhost:9779") # Conexion con el servidor. Por defecto siempre escucha en el puerto 9779

#print (server.get_lliurex_version_on_chroot(user_info,"LtspChroot","/graveyard/"))

