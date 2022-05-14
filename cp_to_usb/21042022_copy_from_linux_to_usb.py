from netmiko import ConnectHandler
import time
import re
import datetime

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

def today_datetime():
    """Printe date of today"""
    today = str(datetime.date.today())
    return today

def find_usb_from_fdisk():
    """This function is to search usb name from "fdisk -l" output
    the last disk is the most recent inserted device, which is the user's usb"""
    pattern = re.compile('/\w\w\w/\w\w\w\d')
    output = connection.send_command_timing('sudo fdisk -l\nadmin')
    usb_list = re.findall(pattern, output)
    usb_name = usb_list[-1]
    return usb_name

def find_usb_from_dmesg():
    """This function is to search usb name from logs"""
    pattern = re.compile('\w\w\w\:\s(\w\w\w\d)')
    output = connection.send_command_timing('dmesg -T | tail')
    # print(output)
    found_usb = re.findall(pattern, output)
    usb_name = '/dev/' + found_usb[0]
    return usb_name

def display_available_logs(text):
    """Display all available logs for downloading"""
    pattern = re.compile('SESSION\.(\d+)\.LOGS')
    match = re.findall(pattern, text)
    new_list = []
    while match:
        session_id = match.pop()
        new_list.append(int(session_id))
    new_list.sort()
    print('\nBelow listed all historic logs:')
    for i in new_list:
        print('SESSION.' + str(i) + '.LOGS')

def copy_live_logs(file_list):
    """Copy printer.log to USB"""
    txt_log_file = re.compile('^[P|p][R|r][I|i][N|n][T|t][E|e][R|r].*\.log$')
    for file in file_list:
        found_live_log = re.findall(txt_log_file,file)
        if bool(found_live_log) == True:
            connection.send_command_timing(
                'cp ' + log_dir + file + ' ' + usb_path + '/')  # If "printer.log" file was found, copy it to USB
            print('Copying file： "' + file + '" to usb...')
            #print('Completed!')
        else:
            pass
    print('Completed!')

user_prompt = '\n*********  Select Option  *********\n'
user_prompt += '(1). Copy logs from printer to USB\n'
user_prompt += '(2). Quit\n'
user_prompt += '\nEnter your choice: '

input_from_user = ''
while input_from_user != '2':
    msg_from_user = input(user_prompt)
    if msg_from_user == '1':
        print(find_usb_from_dmesg())
        if find_usb_from_dmesg() == find_usb_from_fdisk():
            print('USB drive name: ' + find_usb_from_fdisk() + '\n')
            folder_name = input(
                'You need to create a folder in your USB to store files.\nEnter name of the new folder: ')
            usb_path = usb_mount + '/' + folder_name + '-' + today_datetime()
            print('\nCreating new folder ' + folder_name + '-' + today_datetime() + ' ...')

            connection.send_command_timing(
                'sudo mkdir ' + usb_mount + '\n' + psw + '\nsudo mount ' + find_usb_from_fdisk() + ' ' + usb_mount + '\n' + psw)
            connection.send_command_timing(
                'sudo mkdir ' + usb_path + '\n' + psw + '\n')
            prompt = '\n*********  Select Option  *********\n'
            prompt += '(1). Copy both live and historic logs\n'
            prompt += '(2). Copy live logs only\n'
            prompt += '(3). Back to previous page\n'
            prompt += '\nEnter your choice: '
            user_input = ''

            while user_input != '3':
                message = input(prompt)
                connection.send_command_timing('cd ' + log_dir + '\nls')
                if message == '1':
                    output1 = connection.send_command_timing('ls')
                    files = output1.split()
                    copy_live_logs(files)
                    display_available_logs(output1)
                    # prompt1 = '\nEnter session-id to copy specific historic logs\n'
                    # prompt1 += '(Use "comma" to separate multiply logs, eg: 100,101,102)\n'
                    # prompt1 += 'Enter "all" to copy all historic logs\n'
                    # prompt1 += 'Enter "quit" to exit the program\n'
                    prompt1 = '\n*********  Select Option  *********\n'
                    prompt1 += '(1). Copy all historic logs\n'
                    prompt1 += '(2). Copy specific logs\n'
                    prompt1 += '(3). Back to previous page\n'
                    prompt1 += '\nEnter your choice: '
                    user_input1 = ''
                    while user_input1 != '3':
                        message1 = input(prompt1)
                        if message1 == '3':
                            break

                        elif message1 == '1':
                            output1 = connection.send_command_timing('ls')
                            files = output1.split()
                            for file in files:
                                found_gz_folder = re.findall(find_gz_folder, file)
                                if bool(found_gz_folder) == True:
                                    output2 = connection.send_command_timing(
                                        'cd ' + log_dir + file + '/\nls')  # If "SESSION.XX.LOGS" folder was found, go into this folder
                                    gz_files = output2.split()
                                    for gz_file in gz_files:
                                        found_gz_file = re.findall(gz_log_file,
                                                                   gz_file)  # Check all files under this directory and search "printer.xx.gz" file.
                                        if bool(found_gz_file) == True:
                                            print('Copying "' + gz_file + '" to usb...')
                                            connection.send_command_timing(
                                                'cp ' + log_dir + file + '/' + gz_file + ' ' + usb_path + '/')
                                        else:
                                            pass
                                else:
                                    pass
                            print('Completed!')
                            break
                        elif message1 == '2':
                            prompt2 = '\n*********  User Input Required *********\n'
                            prompt2 += 'Enter log session ID, use "," to separate multiply logs\n'
                            prompt2 += 'Enter "quit" to back to main page\n'
                            prompt2 += 'Enter your choice: '
                            user_input2 = ''
                            while user_input2 != 'quit':
                                message2 = input(prompt2)
                                valid_input = re.findall(multi_logs, message2)
                                if bool(valid_input) == True:
                                    for log_id in valid_input:
                                        # print(log_id)
                                        output2 = connection.send_command_timing(
                                            'cd ' + log_dir + 'SESSION\.' + log_id + '\.LOGS/\nls')
                                        gz_files = output2.split()
                                        for gz_file in gz_files:
                                            found_gz_file = re.findall(gz_log_file,
                                                                       gz_file)  # Check all files under this directory and search "printer.xx.gz" file.
                                            if bool(found_gz_file) == True:
                                                print('Copying "' + gz_file + '" to usb... ...')
                                                connection.send_command_timing(
                                                    'cp ' + log_dir + 'SESSION\.' + log_id + '\.LOGS/' + gz_file + ' ' + usb_path + '/')
                                            else:
                                                pass
                                    break
                                elif message2 == 'quit':
                                    break
                                else:
                                    print('Invalid input. Re-enter your choice!\n')
                            print('Completed!')
                            break
                        else:
                            print('Invalid input. Re-enter your choice!\n')
                    break
                elif message == '2':
                    output1 = connection.send_command_timing('ls')
                    files = output1.split()
                    copy_live_logs(files)
                    break
                elif message == '3':
                    break
                else:
                    print('Invalid input. Re-enter your choice!\n')
        else:
            print('USB name mismatch. Please check and try again!')
            pass
    elif msg_from_user == '2':
        break
    else:
        print('Invalid input. Re-enter your choice!\n')
print('\nUmouting USB from ' + usb_mount)
connection.send_command('sudo umount ' + usb_mount)  # Umount your USB device
connection.disconnect()

