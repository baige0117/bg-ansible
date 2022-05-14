import pexpect
import os
import re
import time

COMMANDS = []
COMMAND = 'exit'
PATH = os.getcwd()
print(PATH)
os.chdir(PATH)
index1 = 'Are you sure you want to continue connecting'
index2 = 'Password:'
BANNER = "\*\*\*|banner motd|banner login"
username = 'admin'
password = 'admin'
IP_LIST = 'ip_list.txt'
FILES = os.listdir(PATH)

IP_LIST = open(IP_LIST, 'r')
ALL_IP = IP_LIST.readlines()
for IP_ADDRESS in ALL_IP:
    ip = IP_ADDRESS.strip()
    login = pexpect.spawnu('ssh ' + username + '@' + ip)
    login.logfile = open('log', 'a')
    #login.logfile = sys.stdout
    # login.logfile = fout
    #login.logfile = open('log','r')
    index = login.expect([index1, index2, pexpect.EOF, pexpect.TIMEOUT])
    if index == 0:
        print('This is a new device, save SSH key of this device.')
        login.sendline('yes')
        login.expect('Password')
        login.sendline(password)
        login.expect('.*#')
        login.sendline('config t')
        login.expect('.*\)#')
        print(login.before)
        for file in FILES:
            COMPARE_IP_FILENAME = re.match(ip, file)
            MATCHED = bool(COMPARE_IP_FILENAME)
            if MATCHED == True:
                CONFIG_FILE = open(file, 'r')
                COMMANDS = CONFIG_FILE.readlines()
                for UNSTRIPTED_COMMAND in COMMANDS:
                    COMMAND = UNSTRIPTED_COMMAND.strip()
                    if re.match(BANNER, COMMAND) is not None:
                        login.sendline(COMMAND)
                        login.expect('.*')
                    else:
                        # print(COMMAND.strip())
                        login.sendline(COMMAND)
                        login.expect('.*\)#')
                login.sendline('end')
                login.expect('.*#')
                time.sleep(2)
                login.sendline('write mem')
                login.expect('.*#')
                login.sendline('exit')
                print(login.read())
                CONFIG_FILE.close()
                login.close()
            else:
                pass
        # print(login.read())
        # index = login.expect([index1, index2, pexpect.EOF, pexpect.TIMEOUT])
    if index == 1:
        print('Found SSH key of this device, log in and executing commands')
        login.sendline(password)
        login.expect('.*#')
        login.sendline('config t')
        login.expect('.*\)#')
        for file in FILES:
            COMPARE_IP_FILENAME = re.match(ip,file)
            MATCHED = bool(COMPARE_IP_FILENAME)
            if MATCHED == True:
                CONFIG_FILE = open(file,'r')
                COMMANDS = CONFIG_FILE.readlines()
                for UNSTRIPTED_COMMAND in COMMANDS:
                    COMMAND = UNSTRIPTED_COMMAND.strip()
                    # print(COMMAND)
                    if re.match(BANNER,COMMAND) is not None:
                        login.sendline(COMMAND)
                        login.expect('.*')
                    else:
                        #print(COMMAND.strip())
                        login.sendline(COMMAND)
                        login.expect('.*\)#')
                login.sendline('end')
                login.expect('.*#')
                time.sleep(2)
                login.sendline('write mem')
                login.expect('.*#')
                login.sendline('exit')
                print(login.read())
                CONFIG_FILE.close()
                login.close()
            else:
                pass
    elif index == 2:
        print('Target device ' + ip + ' is unreachable!')
        pass
# except Exception:
#     print('IP list is missing!')
# login = pexpect.spawn('home/baige/ssh admin@192.168.2.101')
# print(login.read())
# login.expect('Password:')
# login.sendline('cisco')
# login.expect("R1#")
# print(login.read())
# login.expect(".*#")
# login.sendline("ter len 0")
# login.expect(".*#")
# login.send("show version")
# login.expect(".*#")
# print(login.read())

