import csv
from jinja2 import Template

source_file = "master_list.csv"  # csv file
j2_temp_file = 'j2_temp.j2'  # jinja template

with open(j2_temp_file) as f:
    config_temp = Template(f.read())  # open and read jinja template, store contents in config_temp

with open(source_file) as f:  # open and read master list
    reader = csv.DictReader(f)
    for row in reader:
        config = config_temp.render(
            hostname = row['Hostname'],
            lo0_add = row['Loopback0'],
            lo1_add = row['Loopback1'],
            tun0_add = row['VPN Tunnel Address'],
            wan_ip_add = row['Wan IP'],
            as_num = row['AS Number'],
            isp_gw_add = row['Wan Gateway']
            #oob = row['OOB_IP']
        )
        # print(row['Hostname'])
        with open(row['OOB_IP']+'.txt','w') as f:
            f.write(config)

