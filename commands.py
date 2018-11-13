"""
Commands for main.py execCmd()
Eric Diskin
2018
"""

CD = 'cd' # change working directory
DIR = 'dir' # list current wokring directory 
MIRROR = 'mirror' # mirror text back
INSTALL = 'install' # install an app from github
UNINSTALL = 'uninstall' #uninstall an app 
RESET = 'reset' # reset to defaults (to ready for sending to github)
RESTART = 'restart' # restart system (may not work anymore)
EXIT = 'exit' # call sys.exit
SLEEP = 'sleep' # time.sleep for (float)
WHATSNEW = 'whatsNew' # get what is new
FUTURE = 'future' # get what will happen in the next update
TREE = 'tree' # PRINT(not return) a tree of current dir and all sub with files
PATH = 'path' # get the paths variable(where to scan for apps.)
SETNAME = 'setname' # set the osys.username
NAME = 'name' # get osys.username
ISPKG = 'ispkg' # check if an app is isntalled 
APPS = 'apps' # get a list of all apps
DEVMODE = 'devMode' # turn devmode on or off
STOPATERROR = 'stopAtError' # exit the script when an error occurs
OPEN = 'open' # open a file 
CLEAR = 'clr' # clear terminal (sys.stdout)