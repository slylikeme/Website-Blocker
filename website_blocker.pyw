import time
from datetime import datetime as dt
import gc

gc.enable()

hosts_temp = 'hosts'
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect='127.0.0.1'
website_list = ['www.reddit.com', 'reddit.com', 'www.politico.com',
                'politico.com', 'www.cnn.com', 'cnn.com', 'www.npr.org',
                'npr.org', 'www.pbs.org', 'pbs.org']

# main loop that runs throughout the day
while True:
    if dt(dt.now().year, dt.now().month, dt.now().day, 12) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, 16):
        # print('Working hours...')
        # open hosts file
        with open(hosts_path, 'r+') as myfile:
            content = myfile.read()
            for website in website_list:
                if website in content:  # if already there do nothing
                    pass
                else:   # append website_list to hosts file if not there
                    myfile.write(redirect + '\t' + website + '\n')

    else:
        # print('Fun hours...')
        # open hosts
        with open(hosts_path, 'r+') as myfile:
            content = myfile.readlines()
            myfile.seek(0)
            for line in content:    # remove website_list from hosts file
                if not any(website in line for website in website_list):
                    myfile.write(line)
            myfile.truncate()
    time.sleep(30)
