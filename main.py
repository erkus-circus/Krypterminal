"""
Kyrpterminal
Eric Diskin
Started: 10/8/2018
""" """
Some pkgs created by Ashten Spector
"""

import json
import os
import platform as pltfrm
import shutil
import sys
import time

import requests as req

VERSION = '1.0.0.0'

startup = []

# NOTE: Add ALL changes to the below string.
whatsNew = """

Changes in """+VERSION+""":
~ Sent all files into one file
~ Allowed for multiple people to use this than just one without lots of bugs.
~ Improved the pkg download and install proccess.
~ Improved reset functionality
~ Fixed pkgs automatically abandoning even there is no error.

~ Commands
    ~ Added restart
        ~ restarts system
        ~ Added future
            ~ learn what is coming in future updates.
    ~ devMode
        ~ turns on dev commands such as python restarts
    ~ added sleep
        ~ sleep the terminal for a certain amt of time
        ~ after sleep add another cmd for after cmd (optional)
    ~ Added path
        ~ path -l lists osys.paths
        ~ path -a adds a path to osys.paths
        ~ path -r removes a path to osys.paths
        ~ For scanning more directories for pkgs.
        ~ Externally installed pkgs
        ~ User created pkgs.
    ~ Added setname
    ~ Added name
    ~ Added input
        ~ Changes from showing osys.path to whatever you want
        ~ Equivelent to WIN10 'prompt' command
    ~ Added tree
        ~ shows a tree of the current directory and all subdirectories with files 
    ~ Added ispkg
        ~ checks if a package is installed in the paths.
    ~ Changed reset-pkgs to reset
    ~ Added open
        ~ Opens a file in directory
    ~ seperate commands with ;
    ~ Added pkgs
        ~ Lists all the pkgs in the global path (osys.paths or path file in BP)
        ~ Turn pkgs on or off 
    ~ Added stopAtError
        ~ Stops at errors instead of restarting.
    ~ Moved the clear command execution to com module.
~ No longer asks for users name when starting terminal.
~ startup cmds added. edit startup list to change startup cmds.
~ Many, many bug fixes!
""".replace('\n','\n\n')

"""
If you are reading this and have no idea what pkgs are,
go to https://github.com/erkus-circus/cmds/
"""

future = """
For future version (1.1.0.0):
    ~ Begin work on a front-end version
"""

BASE_PATH = os.getcwd()
BP = BASE_PATH
ONOFF = ('off', 'on')
DEFAULT = ('13DEFAULT-COMMAND13','erk_wuz_here')

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

def leng(tlen, length):
    if len(tlen) >= length:
        return True
    return False

def py(IO):
    try:
        exec(IO.read())
    except:
        return

def download(URL='http://google.com/favicon.ico', LOC=None):
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
    if the system is Java it returns java.
    """

    if pltfrm.system() == 'Windows':
        return 'wind'

    elif pltfrm.system() == 'Java':
        return 'java'

    else:
        return 'linx'

def fExists(path):
    """check if a file exits"""
    if os.path.isfile(path):
        return True
    return False

def clear():
    if plfrm() == 'wind':
        cmd('cls')
    else:
        cmd('clear')

def dirExists(direct):
    """check if a directory exits"""
    if os.path.isdir(direct):
        return True
    return False

def readFile(path, prefix=''):
    with open(prefix + path) as file:
        ret = file.read()
    return ret

def deldir(path):
    shutil.rmtree(path)

def join(arr, **kwargs):
    """join an iterable
    kwargs:
        sep=iter seperator (default: SPACE)"""
    sep = ' '
    if 'sep' in kwargs:
        sep = kwargs['sep']

    return sep.join(arr)

def rdir(dir):
    shutil.rmtree(dir)

def tree(direct, tabs=0):
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
    return tabs

try:
    class osys:
        username = 'Guest'
        restart = False  # if resart happens when the main loop breaks.
        paths = json.load(open(BP + '/path'))  # the place to scan pkgs
        path = os.getcwd()  # the path
        devMode = False # for dev cmds
        prompt = DEFAULT
        pkgs = True
        ncom = None  # the next command to execute
        stopAtError = True  # Show errors that occur in pkgs
    
    if osys.paths == []:
        with open(BP + '/path','w') as f:
            json.dump([BP + '/pkgs'], f)
            osys.paths = [BP + '/pkgs']
    
except:
    sys.exit('An error occured. could not begin. exiting...')


def sendCom(comm):
    osys.ncom = comm

def mainOs():
    global startup
    clear()
    print('Krypterminal [Version %s]' %  (VERSION))
    print('Eric Diskin\n')

    if osys.restart:
        osys.restart = False
    
    try:
        os.makedirs(BP + '/pkgs')
    except OSError as e:
        pass

    try:
        while True:
            if startup != []:
                # the startup system. change startup var to exec different cmds at start.
                osys.ncom = startup.pop(0)

                
            def ecmd(cmd):
                osys.ncom = cmd

            if osys.ncom == None:
                osys.path = os.getcwd()
                if osys.prompt == DEFAULT:
                    command = input(osys.path + ':> ')
                else:
                    command = input(osys.prompt)

            else:
                # if there is a next command
                command = osys.ncom
                osys.ncom = None

            if len(command) < 1:
                continue
            
            if ';' in command:
                startup = command.split(';')
                continue

            words = command.split()
            cmd1 = words[0]

            make = False
            
            if osys.pkgs:
                for p in osys.paths:
                    for direct in os.listdir(p):
                        if cmd1 == direct:
                            path = p +'\\'+ direct + '\\'
                            if not fExists(path + 'setup.json'):
                                continue

                            with open(path + 'setup.json') as js:
                                    js = json.load(js)
                            if not osys.stopAtError:
                                try:
                                    exec(readFile(path + js['run']), {'command':command, 'cmdexec':ecmd})

                                except Exception as e:
                                    if osys.stopAtError:
                                        print(e)
                                    else:
                                        print('Something went wrong. abandoning script.')
                            else:
                                exec(readFile(path + js['run']), {'command': command, 'cmdexec': ecmd, 'PATH': BP + '/pkgs/%s/' % direct})

                            make = True
                            break

                        if make:
                            break

                if make:
                    continue

            if osys.devMode:
                if words[0] == 'python' or words[0] == 'py':
                    cmd1 = 'exit'

            if cmd1 == 'restart':
                print('Restaring')

            elif cmd1 == 'exit':
                # end the loop and exit the OS
                print('Wrapping up..')
                time.sleep(1)
                print('Bye %s' % (osys.username))
                sys.exit()
                break
            
            elif cmd1 == 'sleep':
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
                for i in whatsNew.split('\n'):
                    print(i)
                    time.sleep(.05)

            elif cmd1 == 'future':
                for i in future.split('\n'):
                    print(i)
                    time.sleep(.05)

            elif cmd1 == 'tree':
                tree(osys.path)
            
            elif cmd1 == 'prompt':
                if leng(words,2):
                    osys.prompt = ' '.join(words[1:])
                else:
                    print('prompt changed to DEFAULT.')
                    osys.prompt = DEFAULT

            elif cmd1 == 'path':
                if '-a' in words and '-r' in words:
                    print('Unable to add and remove path from the global path.')
                    continue
                    
                if leng(words,2):
                        word = words[1]
                        if word == '-l':
                            for path in osys.paths:
                                print(path)

                        elif word == '-r':
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
                            if leng(words, 3):
                                if ' '.join(words[2:]) in osys.paths:
                                    print('Unable to add an already existing path to global path.')

                                else:
                                    if dirExists(' '.join(words[2:])):
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
                URL: https://github.com/erkus-circus/cmds.git"""
                if leng(words, 2):
                    install(words[1])
                else:
                    print('Could not download empty package.')
                    continue

            elif cmd1 == 'setname':
                if leng(words, 2):
                    osys.username = ' '.join(words[1:])
                else:
                    print('Usage: setname <your-name>')
            
            elif cmd1 == 'name':
                    print(osys.username)
            
            elif cmd1 == 'ispkg':
                if not leng(words, 2):
                    print('Usage: ispkg <pkg>\nreturns \'Installed\' if installed.\nif not returns \'\'')
                else:
                    if dirExists(BP + '/pkgs/' + ' '.join(words[1:])):
                        print("'Installed'")
                    else:
                        print("''")

            elif cmd1 == 'pkgs':
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
                if leng(words, 2):
                    if fExists(' '.join(words[1:])):
                        cmd(' '.join(words[1:]))
                    else:
                        print('Invalid file name or file path.')
                
                else:
                    print('Usage: open <path to file>')

            elif cmd1 == 'reset':
                print('Reseting..')
                deldir(BP + '/pkgs/')
                os.makedirs(BP + '/pkgs/')
                with bpopen('path','w') as f:
                    json.dump([BP + '\\pkgs'], f)
                print('Reset complete. restarting...')
                clear()
                osys.restart = True
                break

            elif cmd1 == 'uninstall':
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

                if dirExists(join(words[1:])):
                    os.chdir(join(words[1:]))
                    osys.path = os.getcwd()

                else:
                    print('Invalid directory')
                    continue

            elif cmd1 == 'dir':
                for i in os.listdir():
                    print(i)

            elif cmd1 == 'mirror':
                print(' '.join(words[1:]))

            elif cmd1 == 'uninstall':
                """Uninstall an installed pkg (via install command)"""
                rdir(BP + '/pkgs/%s/' % words[1])

            elif cmd1 == 'clr':
                clear() # clear terminal

            else:
                print('Invalid command \'%s\'.\nTry typing \'pkgs on\'' % (cmd1))

    except Exception as e:
        if not osys.stopAtError:
            osys.restart = True
            clear()
            print('A crash occured. restarting...\n\n')

        else:
            print(e)

    if osys.restart:
        mainOs()
        sys.exit()

def bpopen(*args):
    return open(BASE_PATH + '/' + args[0], *args[1:])

def install(name):
    """Download a package"""
    path = BP + '/pkgs/%s/' % name
    try:
        print('Downloading setup file...')
        js = json.loads(bytes.decode(get(
            'https://raw.githubusercontent.com/erkus-circus/cmds/master/%s/setup.json' % name), 'utf8'))


        if dirExists(path):
            print('Package already installed. reinstalling...')
            rdir(path)
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
        print('Unable to download pkg. cleaning up...\n')
        if dirExists(path):
            rdir(path)

mainOs()
