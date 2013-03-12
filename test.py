#!/usr/bin/env python
# coding = utf-8

# Import the libraries
from xmlrpclib import *
import sys

# Fix info for user at example
user="user"
password="password"


# Get the user
if (sys.argv[0]): 
  user=sys.argv[0]

# Get the password
if (sys.argv[1]):
  password = sys.argv[1]

user_info=(user,password)

print (user_info)
server = ServerProxy ("https://localhost:9779") # Conexion con el servidor. Por defecto siempre escucha en el puerto 9779

print (server.get_lliurex_version_on_chroot(user_info,"LtspChroot","/graveyard/"))

