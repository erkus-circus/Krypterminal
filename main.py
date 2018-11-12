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
import time
from threading import Thread
import requests as req

VERSION = '1.2.0'

startup = []

# NOTE: Add ALL changes to the below string.
whatsNew = """
    ~ Commented more, so other people can read
    ~ Threads are used to run pkgs
""".replace('\n','\n\n')

"""
If you are reading this and have no idea what pkgs are,
go to https://github.com/erkus-circus/cmds/
"""

future = """
For future version (1.3.0):
    ~ Nothing at the moment
"""

BASE_PATH = os.getcwd()# BP and BASE_PATH are the base path (for my computer it is C:\code\Colab\Python\OS)
BP = BASE_PATH

threads = {}

ONOFF = ('off', 'on')
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
    print(opts)
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

def tree(direct, tabs=0):
    """
    Print a tree of a directory
    """
    try:
        for d in os.listdir(direct):
            if os.path.isfile(direct + '/' + d):
                print((' ' * (tabs)) + '|- ' + d)

            elif os.path.isdir(direct + '/' + d):

                print((' ' * (tabs)) + ' \\ ' + d)
                tabs += 1
                tabs = tree(direct + '/' + d, tabs)
                tabs -= 1

            else:
                print('neither dir nor file')

        print((' ' * (tabs)) + '/')
    except WindowsError as e:
        print((' ' * tabs) + '/ ~ A restricted directory was found. skipping.')
    return tabs

try:
    # the class that has all important variables
    class osys:
        username = 'Guest' # username
        restart = False  # if resart happens when the main loop breaks.
        paths = json.load(open(BP + '/path'))  # the place to scan pkgs
        path = os.getcwd()  # the path
        devMode = False # for dev cmds
        prompt = DEFAULT # the prompt to use in terminal
        pkgs = True # enable or disable pkgs
        ncom = None  # the next command to execute
        stopAtError = True  # stop and show an error when it occurs instead of restarting
    
    if osys.paths == []:
        # if there is no place to scan for pkgs, create one
        with open(BP + '/path','w') as f:
            json.dump([BP + '/pkgs'], f)
            osys.paths = [BP + '/pkgs']
    
except:
    sys.exit('An error occured. could not begin. exiting...')


def sendCom(comm):
    """Set the next command to execute"""
    osys.ncom = comm

def mainTerminal():
    """The main shell"""
    global startup # startup is the list of commands to execute in order
    clear() # clear terminal

    print('Krypterminal [Version %s]' %  (VERSION)) #Print stuff
    print('Eric Diskin\n')

    if osys.restart:
        # if there was just a restart
        osys.restart = False
        print('A restart occured.')
    
    try:
        os.makedirs(BP + '/pkgs')
        # try to make sure there is a place to scan for pkgs
    except OSError as e:
        pass

    try:
        while True:
            #mainloop

            if startup != []:
                # the startup system. change startup var to exec different cmds at start.
                osys.ncom = startup.pop(0)

            if osys.ncom == None:

                osys.path = os.getcwd()

                if osys.prompt == DEFAULT:
                    # check if prompt is not set to DEFAULT
                    command = input(osys.path + ':> ')
                else:
                    command = input(osys.prompt)

            else:
                # if there is a next command
                command = osys.ncom
                osys.ncom = None

            if len(command) < 1:
                # if there is no input, send another request for it
                continue
            
            if ';' in command:
                # more tan one command in one line
                startup = command.split(';')
                continue

            words = command.split()
            cmd1 = words[0] # the actual command itself

            make = False
            
            if osys.pkgs:
                # if pkgs are enbled

                for p in osys.paths:
                    # for path in the path file (located in BP)
                    if not os.path.isdir(p):
                        # if the dir is not  dir (it as deleted)
                        continue

                    for direct in os.listdir(p):
                        if cmd1 == direct:
                            path = p +'\\'+ direct + '\\'
                            if not os.path.isfile(path + 'setup.json'):
                                # if the folder is not a pkg
                                continue

                            with open(path + 'setup.json') as js:
                                    js = json.load(js)
                            if not osys.stopAtError:
                                try:
                                    runApp(readFile(path + js['run']), path + js['run'], words, js['opts'] if 'opts' in js else {})

                                except Exception as e:
                                    if osys.stopAtError:
                                        print(e)
                                    else:
                                        print('Something went wrong. abandoning script.')
                            else:
                                runApp(
                                    readFile(path + js['run']), path + js['run'], words, js['opts'] if 'opts' in js else {})

                            make = True # the command was a pkg
                            break

                        if make:
                            break

                if make:
                    continue

            if osys.devMode:
                # for testing (makes life 110% easier)
                if words[0] == 'python' or words[0] == 'py':
                    cmd1 = 'exit'

            if cmd1 == 'restart':
                # call mainTerminal again
                print('Restaring..')
                osys.restart = True
                break

            elif cmd1 == 'exit':
                # end the loop and exit the OS
                print('Wrapping up..')
                time.sleep(1)
                print('Bye %s' % (osys.username))
                sys.exit()
                break
            
            elif cmd1 == 'sleep':
                # wait a certain amout of sec before exec next cmd
                try:
                    if leng(words,2):
                        try:
                            time.sleep(float(words[1]))
                            startup = ' '.join(words[2:]).split(';')
                            continue
                        except:
                            print('Could not sleep so long.')
                except ValueError as e:
                    print('Unable to turn %s into a number.' % words[1])

            elif cmd1 == 'whatsNew':
                # print what is new in cur version
                for i in whatsNew.split('\n'):
                    print(i)
                    time.sleep(.05)

            elif cmd1 == 'future':
                # plans fr next version
                for i in future.split('\n'):
                    print(i)
                    time.sleep(.05)

            elif cmd1 == 'tree':
                #print tree of dir
                tree(osys.path)
            
            elif cmd1 == 'prompt':
                # change prompt
                if leng(words,2):
                    osys.prompt = ' '.join(words[1:])
                else:
                    print('prompt changed to DEFAULT.')
                    osys.prompt = DEFAULT

            elif cmd1 == 'path':
                # add dirs to scan for pkgs
                if '-a' in words and '-r' in words:
                    print('Unable to add and remove path from the global path.')
                    continue
                    
                if leng(words,2):
                        word = words[1]
                        if word == '-l':
                            for path in osys.paths:
                                print(path)

                        elif word == '-r':
                            # remove a dir to scan
                            if leng(words,3):
                                try:
                                    osys.paths.remove(' '.join(words[2:]))
                                    with open(BP + '/path', 'w') as pa:
                                            json.dump(osys.paths, pa)
                                except ValueError:
                                    print('Unable to remove path from global path.')
                            else:
                                print('Usage: path -r <directory>')

                        elif word == '-a':
                            # add a dir to scan
                            if leng(words, 3):
                                if ' '.join(words[2:]) in osys.paths:
                                    print('Unable to add an already existing path to global path.')

                                else:
                                    if os.path.isdir(' '.join(words[2:])):
                                        osys.paths.append(' '.join(words[2:]))
                                        with open(BP + '/path','w') as pa:
                                            json.dump(osys.paths,pa)
                                    else:
                                        print('Not a valid directory.')

                            else:
                                print('Usage: path -a <directory>')

                else:
                    print('Usage: path -r(emove path) -a(dd to path) <directory> -l(ist path)')

            elif cmd1 == 'install':
                """Install more commands.
                use Github.
                URL: https://github.com/erkus-circus/cmds/"""
                if leng(words, 2):
                    install(words[1])
                else:
                    print('Usage: install <pkg>')
                    continue

            elif cmd1 == 'setname':
                # set the username
                if leng(words, 2):
                    osys.username = ' '.join(words[1:])
                else:
                    print('Usage: setname <your-name>')
            
            elif cmd1 == 'name':
                #get the username
                    print(osys.username)
            
            elif cmd1 == 'ispkg':
                # is the pkg installed? check
                if not leng(words, 2):
                    print('Usage: ispkg <pkg>\nreturns \'Installed\' if installed.\nif not returns \'\'')
                else:
                    if os.path.isdir(BP + '/pkgs/' + ' '.join(words[1:])):
                        print("'Installed'")
                    else:
                        print("''")

            elif cmd1 == 'pkgs':
                # list pkgs in path
                if not leng(words, 2):
                    for dr in osys.paths:
                        for i in os.listdir(dr):
                            print(i)
                else:
                    if words[1] == '-?':
                        print('Usage: pkgs (lists all the pkgs in global path)')
                        print('Usage: pkgs <on/off> (turns on and off pkgs)')
                    elif words[1] == 'on':
                        osys.pkgs = True
                        print('Pkgs turned on.')
                    elif words[1] == 'off':
                        osys.pkgs = False
                        print('Pkgs turned off.')
                    else:
                        print('Usage: pkgs (lists all the pkgs in global path)')
                        print('Usage: pkgs <on/off> (turns on and off pkgs)')

            elif cmd1 == 'devMode':
                # turn devmode on or off or check if on or off
                if not leng(words, 2):
                    print('devMode is %s.' % ONOFF[osys.devMode])
                else:
                    if words[1] == '-?':
                        print('Usage: devMode (lists all the devMode in global path)')
                        print('Usage: devMode <on/off> (turns on and off devMode)')
                    elif words[1] == 'on':
                        osys.devMode = True
                        print('devMode turned on.')
                    elif words[1] == 'off':
                        osys.devMode = False
                        print('devMode turned off.')

                    else:
                        print('Usage: devMode (lists all the devMode in global path)')
                        print('Usage: devMode <on/off> (turns on and off devMode)')

            elif cmd1 == 'stopAtError':
                # if stop at error
                if leng(words, 2):
                    if words[1] == 'true':
                        osys.stopAtError = True
                    elif words[1] == 'false':
                        osys.stopAtError = False
                    else:
                        print('Usage: stopAtError <true/false>')
                else:
                    print('Usage: stopAtError <true/false>')
            
            elif cmd1 == 'open':
                # open a file
                if leng(words, 2):
                    if os.path.isfile(' '.join(words[1:])):
                        cmd(' '.join(words[1:]))
                    else:
                        print('Invalid file name or file path.')
                
                else:
                    print('Usage: open <path to file>')

            elif cmd1 == 'reset':
                # reset terminal (MUSTDO if sharing)
                print('Reseting..')
                deldir(BP + '/pkgs/')
                os.makedirs(BP + '/pkgs/')
                with bpopen('path','w') as f:
                    f.write('[]')
                clear()
                osys.restart = True
                print('Reset complete. restarting...')
                break

            elif cmd1 == 'uninstall':
                # uninstall pkg
                if leng(words, 2):
                    try:
                        deldir(BP + '/pkgs/' + ' '.join(words[1:]))

                    except:
                        print('Package not found.')
                        continue
                    
                    print('Succesfully deleted %s' + ' '.join(words[1:]))

                else:
                    print('Usage: uninstall <installed pkg>')

            elif cmd1 == 'cd':
                # change directory
                if not leng(words,2):
                    print(os.getcwd())
                    continue

                if os.path.isdir(join(words[1:])):
                    os.chdir(join(words[1:]))
                    osys.path = os.getcwd()

                else:
                    print('Invalid directory')
                    continue

            elif cmd1 == 'dir':
                # list directory
                for i in os.listdir():
                    print(i)

            elif cmd1 == 'mirror':
                # mirror back text
                print(' '.join(words[1:]))

            elif cmd1 == 'uninstall':
                """Uninstall an installed pkg (via install command)"""
                deldir(BP + '/pkgs/%s/' % words[1])

            elif cmd1 == 'clr':
                clear() # clear terminal

            else:
                # cmd1 is not an actual cmd
                print('Invalid command \'%s\'.\nTry typing \'pkgs on\'' % (cmd1))

    except Exception or BaseException as e:
        if not osys.stopAtError:
            # restart
            osys.restart = True
            clear()
            print('A crash occured. restarting...\n\n')

        else:
            print(e)

    if osys.restart:
        mainTerminal()
        sys.exit()

def bpopen(*args):
    """Open a a path from BP"""
    return open(BASE_PATH + '/' + args[0], *args[1:])

def install(name):
    """Download a package"""
    path = BP + '/pkgs/%s/' % name
    try:
        print('Downloading setup file...')
        js = json.loads(bytes.decode(get(
            'https://raw.githubusercontent.com/erkus-circus/cmds/master/%s/setup.json' % name), 'utf8'))

        if os.path.isdir(path):
            print('Package already installed. reinstalling...')
            deldir(path)
            print('Package uninstalled. reinstalling...')
        
        os.makedirs(path)
        print('Creating directories.')

        for file in js['files']:
            print('Downloading package file: %s' % file)
            f = bytes.decode(get(
                'https://raw.githubusercontent.com/erkus-circus/cmds/master/%s/%s' % (name, file)), 'utf8')

            print('Writing package file: %s' % file)
            with open(path + file, 'w') as FWRITE:
                FWRITE.write(f)
                
        print('Writing setup file.')
        with open(path + 'setup.json', 'w') as setup:
            json.dump(js, setup)

        print('\n\nSuccecfully installed %s!' % name)
        return

    except:
        #The pkg is not able to download, delete any remanants to
        print('Unable to download pkg. cleaning up...\n')
        if os.path.isdir(path):
            deldir(path)

mainTerminal() # start main loop
