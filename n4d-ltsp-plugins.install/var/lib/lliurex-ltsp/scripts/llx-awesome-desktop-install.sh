#!/bin/bash

clientIp=$1
display=$2


export DISPLAY=$clientIp$display
eval "xterm -geometry 79x27+10+15 -hold -fa 'default' -e 'apt-get update; \
apt-get install lliurex-ltsp-client; \
echo;echo;echo;echo Hem finalitzat.Taqueu la finestra per continuar. ;echo;echo;exit 0'"

exit 0
