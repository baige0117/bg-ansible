import datetime
usb_mount = '/mnt/usb'

def today_datetime():
    today = str(datetime.date.today())
    return today


folder_name = input('You need to create a folder in your USB to store files.\nEnter name of the new folder: ')
usb_path = usb_mount + '/' + folder_name + '-' + today_datetime()
print(usb_path)

