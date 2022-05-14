from netmiko import ConnectHandler
import time
import re

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

usb_info = connection.send_command_timing('fdisk -l')  # Create USB mouting point /media/usb
print(usb_info + '\n')
# Check USB info and mount USB
usb_name = input('Please enter the directory of your usb (eg: /dev/sdb1):\n')  # User must check and input his USB device's directory in the Linux machine.
connection.send_command_timing('sudo mkdir ' + usb_mount +'\n'+ psw + '\nsudo mount '+ usb_name + ' ' + usb_mount + '\n' + psw)  # Create USB mouting point /media/usb

prompt = '\nEnter Session-ID to unzip specific historic logs\n'
prompt += '(Use "comma" to separate multiply logs, eg: 100,101,102)\n'
prompt += 'Enter "all" to unzip all logs\n'
prompt += 'Enter "quit" to exit the program\n'
message = ''
while message != 'quit':
        message = input(prompt)
        output1 = connection.send_command_timing('cd /mnt/usb/\nls')
        usb_files = output1.split()
        valid_input = re.findall(multi_logs, message)
        if message == 'all':
            for usb_file in usb_files:
                #print(usb_file)
                found_gz_file = re.findall(gz_log_file, usb_file)
                if bool(found_gz_file) == True:
                    print('Extracting "' + usb_file + '" ... ...')
                    #time.sleep(0.5)
                    connection.send_command_timing('gzip -dk ' + usb_file + '\ny')
                else:
                    pass
            break
        elif bool(valid_input) == True:
            for log_id in valid_input:
                print('Extracting printer.' + log_id + '.gz ...')
                connection.send_command_timing('gzip -dk printer.' + log_id + '.log.gz' + '\ny')
        elif message == 'quit':
            print('Log(s) Extracting Completed!\n')
            break
        else:
            print('\nInvalid input! Please Enter the Session-ID(s) of the printer.')
connection.send_command('sudo umount ' + usb_mount)  # Umount your USB device
connection.disconnect()