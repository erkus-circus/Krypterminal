"""
Commands for main.py execCmd()
Eric Diskin
2018
"""
CMDS = [
    'cd', # change working directory
    'dir', # list current wokring directory 
    'mirror', # mirror text back
    'install', # install an app from github
    'uninstall', #uninstall an app 
    'reset', # reset to defaults (to ready for sending to github)
    'restart', # restart system (may not work anymore)
    'exit', # call sys.exit
    'sleep', # time.sleep for (float)
    'whatsNew', # get what is new
    'future', # get what will happen in the next update
    'tree', # PRINT(not return) a tree of current dir and all sub with files
    'path', # get the paths variable(where to scan for apps.)
    'setname', # set the osys.username
    'name', # get osys.username
    'isapp', # check if an app is isntalled 
    'apps', # get a list of all apps
    'devMode', # turn devmode on or off
    'stopAtError', # exit the script when an error occurs
    'open', # open a file 
    'clr' # clear terminal (sys.stdout)
]