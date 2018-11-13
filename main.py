"""
Kyrpterminal
Eric Diskin
Started: 10/8/2018
"""

import json
import os
import platform as pltfrm
import shutil
import sys
import commands
import time
from threading import Thread
import requests as req

VERSION = '2.0.0 Beta 3'

RESTART = 'RESTART'
NOIO = 'NOIO'
NOCMD = 'NOCMD'
NAN = 'NAN'
CRASH = 'CRASH'
EOF = 'EOF'
UNEX = 'UNEX'
RUNAPP = 'RUNAPP'

#COMMANDS
cm = commands

# NOTE: Add ALL changes to the below string.
whatsNew = """
    ~ No longer in a big loop! commands can now be called from a function
    ~ added commands module so all commands are stored with use, syntax and name
    ~ Commented more, so other people can read
    ~ Threads are used to run apps
""".replace('\n','\n\n')

"""
If you are reading this and have no idea what apps are,
go to https://github.com/erkus-circus/cmds/
"""

future = """
For future version (2.0.0):
    ~ Front End!
    ~ Improved performance and usable from other things
"""

BASE_PATH = os.getcwd()# BP and BASE_PATH are the base path (for my computer it is C:\code\Colab\Python\OS)
BP = BASE_PATH

threads = {}

FT = (False, True)
DEFAULT = ('13DEFAULT7-7COMMAND13','erk_wuz_here','placeholders are great','lol','lol')

# change working directory to user home foler
os.chdir(os.path.expanduser('~'))
# C:\Users\<name>\

def cmd(command):
    """Execute a system command in the terminal.
    command is the command to execute in the terminal."""
    """Example:
    cmd('clear')
    cmd('cls')
    cmd('exit')"""
    os.system(command)

def runApp(script, path, argv, opts={}):
    sys.argv = argv
    if 'use_main' in opts:
        if opts['use_main']:
            exec(compile(script, path, 'exec'), {'__file__': path})
            return

    t = Thread(name=path, target=lambda script, path: exec(
        compile(script, path, 'exec'), {'__file__': path}), args=(script, path))
    t.start()


def leng(tlen, length):
    """if the length of tlen (iterable) is greater or equal to length, return true, otherwise return false."""
    if len(tlen) >= length:
        return True
    return False

def py(IO):
    # Execute an I/O
    try:
        exec(IO.read())
    except:
        return

def download(URL, LOC=None):
    """
    Download something from the internet
    """
    if LOC == None:
        LOC = URL.split('/')[-1]

    r = req.get(URL, allow_redirects=True)

    with open(LOC, 'w') as file:
        file.write(bytes.decode(r.content, 'utf8'))

def get(URL):
    """
    Return the content of a request to a website
    """
    return req.get(URL, allow_redirects=True).content

def plfrm():
    """The plfrm function returns the platform of the host OS.
    if the system is Windows, it returns wind.
    if the system is Linux then it returns linx.
    if the system is Java it returns jav.
    """

    if pltfrm.system() == 'Windows':
        return 'wind'

    elif pltfrm.system() == 'Java':
        return 'jav'

    else:
        return 'linx'

def clear():
    if plfrm() == 'wind':
        cmd('cls')
    else:
        cmd('clear')

def readFile(path, prefix=''):
    """return a read file"""
    with open(prefix + path) as file:
        ret = file.read()
    return ret

def deldir(path):
    """remove a directory"""
    shutil.rmtree(path)

def join(arr, **kwargs):
    """join an iterable
    kwargs:
        sep=iter seperator (default: SPACE)"""
    sep = ' '
    if 'sep' in kwargs:
        sep = kwargs['sep']

    return sep.join(arr)

def tree(direct, tabs=0, files=True, dirs=True):#TODO FIXME: not ment to print, just return array/obj of folders and paths
    """
    Print a tree of a directory
    (uses print function)
    """
    try:
        for d in os.listdir(direct):
            if os.path.isfile(direct + '/' + d) and files:
                print((' ' * (tabs)) + ' |- ' + d)

            elif os.path.isdir(direct + '/' + d) and dirs:

                print((' ' * (tabs)) + ' \\ ' + d)
                tabs += 1
                tabs = tree(direct + '/' + d, tabs)
                tabs -= 1

        print((' ' * (tabs)) + '/')
    except:
        print((' ' * tabs) + '/ ~ A restricted directory was found. skipping.')

    return tabs

try:
    # the class that has all important variables
    class osys:
        username = 'Guest' # username
        restart = False  # resart happens when the main loop breaks.
        paths = json.load(open(BP + '/path'))  # the place to scan apps
        path = os.getcwd()  # the path
        devMode = False # for dev cmds
        ncoms = []
        prompt = DEFAULT # the prompt to use in terminal
        apps = True # enable or disable apps
        ncom = None  # the next command to execute
        stopAtError = True  # stop and show an error when it occurs instead of restarting
    
    if osys.paths == []:
        # if there is no place to scan for apps, create one
        with open(BP + '/path','w') as f:
            json.dump([BP + '/apps'], f)
            osys.paths = [BP + '/apps']
    
except:
    sys.exit('An error occured. could not begin. exiting...')


def sendCom(comm):
    """Set the next command to execute"""
    osys.ncom = comm


def bpopen(*args):
    """Open a a path from BP"""
    return open(BASE_PATH + '/' + args[0], *args[1:])

def install(name):
    """Download a package"""
    path = BP + '/apps/%s/' % name
    try:
        js = json.loads(bytes.decode(get(
            'https://raw.githubusercontent.com/erkus-circus/cmds/master/%s/setup.json' % name), 'utf8'))

        if os.path.isdir(path):
            deldir(path)
        
        os.makedirs(path)

        for file in js['files']:
            f = bytes.decode(get(
                'https://raw.githubusercontent.com/erkus-circus/cmds/master/%s/%s' % (name, file)), 'utf8')

            with open(path + file, 'w') as FWRITE:
                FWRITE.write(f)
                
        with open(path + 'setup.json', 'w') as setup:
            json.dump(js, setup)

        return

    except:
        #The pkg is not able to download, delete any remanants to
        if os.path.isdir(path):
            deldir(path)

def execCmd(c='',args=()):
    global osys
    try:

        if osys.ncoms != []:
            # the ncoms system. change ncoms var to exec different cmds at start.
            osys.ncom = osys.ncoms.pop(0)

        if osys.ncom == None:
            osys.path = os.getcwd()
            command = c + ' '.join(args)

        else:
            # if there is a next command
            command = osys.ncom
            osys.ncom = None

        if len(command) < 1:
            # if there is no input, send another request for it
            return EOF

        words = command.split()
        c = words[0]

        if osys.apps:
            # if apps are enbled

            for p in osys.paths:
                # for path in the path file (located in BP)
                if not os.path.isdir(p):
                    # if the dir is not  dir (it as deleted)
                    execCmd()

                for direct in os.listdir(p):
                    if c == direct:
                        path = p + '\\' + direct + '\\'
                        if not os.path.isfile(path + 'setup.json'):
                            # if the folder is not a pkg
                            continue

                        with open(path + 'setup.json') as js:
                                js = json.load(js)
                        if not osys.stopAtError:
                            try:
                                runApp(readFile(
                                    path + js['run']), path + js['run'], words, js['opts'] if 'opts' in js else {})

                            except Exception as e:
                                if osys.stopAtError:
                                    return(e)
                                else:
                                    return CRASH
                        else:
                            runApp(
                                readFile(path + js['run']), path + js['run'], words, js['opts'] if 'opts' in js else {})

                        # the command was a pkg
                        return OPENAPP

        if osys.devMode:
            # for testing (makes life 110% easier)
            if words[0] == 'python' or words[0] == 'py':
                c = 'exit'

        if c == cm.RESTART:
            # call mainTerminal again
            osys.restart = True
            return RESTART

        elif c == cm.EXIT:
            # end the loop and exit the OS
            sys.exit()
            
        elif c == cm.SLEEP:
            # wait a certain amout of sec before exec next cmd
            try:
                if leng(words, 2):
                    try:
                        time.sleep(float(words[1]))
                    except:
                        return TIMETOLONG
            except ValueError as e:
                return NAN

        elif c == cm.WHATSNEW:
            # return what is new in cur version
            return whatsNew

        elif c == cm.FUTURE:
            # plans fr next version
            return future

        elif c == cm.TREE:
            #return tree of dir
            tree(osys.path)

        elif c == cm.PATH:
            # add dirs to scan for apps
            if '-a' in words and '-r' in words:
                return UNEX

            if leng(words, 2):
                    word = words[1]
                    if word == '-l':
                        return osys.paths

                    elif word == '-r':
                        # remove a dir to scan
                        if leng(words, 3):
                            try:
                                osys.paths.remove(' '.join(words[2:]))
                                with open(BP + '/path', 'w') as pa:
                                        json.dump(osys.paths, pa)
                            except ValueError:
                                pass#TODO
                        else:
                            return('Usage: path -r <directory>')

                    elif word == '-a':
                        # add a dir to scan
                        if leng(words, 3):
                            if ' '.join(words[2:]) in osys.paths:
                                pass#TODO
                            else:
                                if os.path.isdir(' '.join(words[2:])):
                                    osys.paths.append(' '.join(words[2:]))
                                    with open(BP + '/path', 'w') as pa:
                                        json.dump(osys.paths, pa)
                                else:
                                    pass#TODO

                        else:
                            pass  # TODO

            else:
                pass  # TODO
        elif c == cm.INSTALL:
            """Install more commands.
            use Github.
            URL: https://github.com/erkus-circus/cmds/"""
            if leng(words, 2):
                install(words[1])

            else:
                execCmd()

        elif c == cm.SETNAME:
            # set the username
            if leng(words, 2):
                osys.username = ' '.join(words[1:])
            else:
                osys.username = 'Guest'

        elif c == cm.NAME:
            #get the username
            return osys.username

        elif c == cm.ISPKG:
            # is the pkg installed? check
            if not leng(words, 2):
                return False
            else:
                return FT[os.path.isdir(BP + '/apps/' + ' '.join(words[1:]))]

        elif c == cm.APPS:
            # list apps in path
            if not leng(words, 2):
                return os.listdir(BP + "/apps")

            else:
                if words[1] == 'on':
                    osys.apps = True
                elif words[1] == 'off':
                    osys.apps = False

        elif c == cm.DEVMODE:
            # turn devmode on or off or check if on or off
            if not leng(words, 2):
                return FT[osys.devMode]
            else:
                if words[1] == 'on':
                    osys.devMode = True
                    return
                elif words[1] == 'off':
                    osys.devMode = False
                    return

        elif c == cm.STOPATERROR:
            # if stop at error
            if leng(words, 2):
                if words[1] == 'true':
                    osys.stopAtError = True
                elif words[1] == 'false':
                    osys.stopAtError = False
                return
            else:
                return FT[osys.stopAtError]

        elif c == cm.OPEN:
            # open a file
            if leng(words, 2):
                if os.path.isfile(' '.join(words[1:])):
                    cmd(' '.join(words[1:]))
                else:
                    return NOIO

        elif c == cm.RESET:
            # reset terminal (if sharing)
            #TODO add more reset data for frontend
            deldir(BP + '/apps/')
            os.makedirs(BP + '/apps/')
            with bpopen('path', 'w') as f:
                f.write('[]')
            clear()
            osys.restart = True
            return RESTART

        elif c == cm.CD:
            # change directory
            if not leng(words, 2):
                return osys.path

            if os.path.isdir(join(words[1:])):
                os.chdir(join(words[1:]))
                osys.path = os.getcwd()
                return osys.path

            else:
                return NOIO

        elif c == cm.DIR:
            # list directory
            return os.listdir()

        elif c == cm.MIRROR:
            # mirror back text
            return(' '.join(words[1:]))

        elif c == 'uninstall':
            """Uninstall an installed pkg (via install command)"""
            try:
                deldir(BP + '/apps/%s/' % words[1])
                return True
            except:
                return None

        elif c == cm.CLEAR:
            clear()  # clear terminal

        else:
            # cmd1 is not an actual cmd
            return NOCMD

    except Exception as e:
        if not osys.stopAtError:
            # restart
            osys.restart = True
            clear()
            return('A crash occured. restarting...\n\n')

        else:
            return(e)

    if osys.restart:
        mainTerminal()
        sys.exit()

def mainTerminal():
    """The main shell"""
    clear() # clear terminal

    if osys.restart:
        # if there was just a restart
        osys.restart = False
    
    try:
        os.makedirs(BP + '/apps')
        # try to make sure there is a place to scan for apps
    except OSError:
        pass
    
    if __name__ == '__main__':
        while True:
            print(execCmd(input(osys.path + ':>')))


mainTerminal()  # start main loop