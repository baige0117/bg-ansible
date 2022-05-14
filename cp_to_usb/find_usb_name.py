from netmiko import ConnectHandler
import time
import re

#pattern = re.compile('/\w\w\w/\w\w\w\d')
# ----------------ENTER YOUR PARAMETERS BELOW---------------------
uid = 'baige'
psw = 'admin'
log_dir = '/home/baige/writable/hp_logs/'
ip_add = '192.168.1.166'
usb_mount = '/mnt/usb'
# ----------------------------------------------------------------

txt_log_file = re.compile('^[P|p][R|r][I|i][N|n][T|t][E|e][R|r].*\.log$')
gz_log_file = re.compile('^[P|p][R|r][I|i][N|n][T|t][E|e][R|r].*\.log\.gz$')
find_gz_folder = re.compile('SESSION')
multi_logs = re.compile('\d+|(?:\d+,)+')

linux = {
        'device_type': 'linux',
        'ip': ip_add,
        'username': uid,
        'password': psw,
        'secret': psw
        }

connection = ConnectHandler(**linux)
connection.enable()

def find_usb_from_fdisk():
        pattern = re.compile('/\w\w\w/\w\w\w\d')
        output = connection.send_command_timing('sudo fdisk -l\nadmin')
        usb_list = re.findall(pattern,output)
        usb_name = usb_list[-1]
        return usb_name
#print(find_usb_from_fdisk() + 'from fdisk')


def find_usb_from_dmesg():
    pattern = re.compile('\w\w\w\:\s(\w\w\w\d)')
    output = connection.send_command_timing('dmesg -T | tail')
    #print(output)
    found_usb = re.findall(pattern,output)
    usb_name = '/dev/' + found_usb[0]
    return usb_name
#print(find_usb_from_dmesg() + 'from log')

def compare_two_strings(str_A,str_B):
    if str_A == str_B:
        return str_A
    else:
        print('USB name mismatched. Please exit and check again!')
        pass

if bool(compare_two_strings(find_usb_from_dmesg(),find_usb_from_fdisk())) is True:
    print(compare_two_strings(find_usb_from_dmesg(),find_usb_from_fdisk()))
else:
    print('quit')


connection.disconnect()