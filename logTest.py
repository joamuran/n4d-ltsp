#!/usr/bin/env python

import socket, sys, struct
import logging, logging.handlers

rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.DEBUG)
socketHandler = logging.handlers.SocketHandler('localhost',logging.handlers.DEFAULT_TCP_LOGGING_PORT)
rootLogger.addHandler(socketHandler)

logging.info('LliureX Mirror Info')

logger_remote = logging.getLogger('LliurexMirror')

logger_remote.debug('LliureX Mirror : Debug for if the flies')
logger_remote.info('LliureX Mirror: Info field')
logger_remote.warning('LliureX Mirror: Warning...Atchung!')
logger_remote.error('LliureX Mirror: ERROR - HORROR')

