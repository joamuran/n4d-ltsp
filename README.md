Python Library Documentation: class LtspChroot in module LtspChroot

## class __LtspChroot__
****************************************

### __methods__
****************************************
#### def __\__init__\__(self):

A simple init method

#### def __apt__(self):

Apt functions

#### def __get_lliurex_version_on_chroot__(self, chroot_dir):

get the LliureX Version of chroot given.

#### def __info__(self):

Show basic info about this plugin.

#### def __prepare_X11_applications__(self, chroot_dir):

Prepare a X11 environment to run graphical apps 
into a chroot

#### def __prepare_chroot_for_run__(self, chroot_dir):

Prepare chroot to run commands
mounting some directories:
* /proc/
* /sys/
* /dev/
* /dev/pts/ 

#### def __run_command_on_chroot__(self, chroot_dir, command):

Possible commands:
        * x-editor
        * synaptic
        * terminal

#### def __startup__(self, options):

Startup functions

#### def __test_chroot__(self, chroot_dir):

test_chroot test if the given directory is a real chroot or 
besides, it seems like a chroot.

#### def __umount_chroot__(self, chroot_dir):

Umount system directories
now with -lazy, 
TODO:
        test if it is mounted already
