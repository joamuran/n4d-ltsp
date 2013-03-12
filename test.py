#!/usr/bin/env python
# coding = utf-8
from xmlrpclib import *

user="aberlanas"
password="lliurex"

user_info=(user,password)
server = ServerProxy ("https://localhost:9779") # Conexion con el servidor. Por defecto siempre escucha en el puerto 9779

print (server.get_lliurex_version_on_chroot(user_info,"LtspChroot","/graveyard/"))

