#! python3

import gc
import webblockbackend as wbb
import shutil
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


"""
This version is run through a GUI and is toggleable. Websites can be added or
removed through the GUI. It will also make a backup of your hosts file in the
local directory.
"""

gc.enable()

hosts_temp = 'hosts'
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect = '127.0.0.1'
website_list = wbb.get_website_list()

shutil.copy2(r"C:\Windows\System32\drivers\etc\hosts", "./hosts")


# function tied to <<ListboxSelect>> event
def get_selected_row(event):
    try:
        global selected_tuple
        index = blockedList.curselection()[0]
        selected_tuple = blockedList.get(index)
    except IndexError:
        pass


# populates the listbox
def view_command():
    blockedList.delete(0, tk.END)  # clear the box each time
    for row in wbb.view():
        blockedList.insert(tk.END, row)


# toggles blocking on
def block_site():
    with open(hosts_temp, 'r+') as myfile:
        content = myfile.read()
        for website in website_list:
            if website in content:  # if already there do nothing
                pass
            else:   # append website_list to hosts file if not there
                myfile.write(redirect + '\t' + website + '\n')


# toggles blocking off
def unblock_site():
    with open(hosts_temp, 'r+') as myfile:
        content = myfile.readlines()
        myfile.seek(0)
        for line in content:    # remove website_list from hosts file
            if not any(website in line for website in website_list):
                myfile.write(line)
        myfile.truncate()


# adds a site to the list and updates the listbox
def add_command():
    wbb.insert(addEntryValue.get())
    blockedList.delete(0, tk.END)
    for row in wbb.view():
        blockedList.insert(tk.END, row)


# removes a site from the list
def delete_command():
    try:
        global selected_tuple
        wbb.delete(selected_tuple[0])
        blockedList.delete(0, tk.END)
        for row in wbb.view():
            blockedList.insert(tk.END, row)
    except NameError:
        pass


def run_program():
    window.mainloop()


window = tk.Tk()
window.title('Website Blocker')
window['padx'] = 8
window['pady'] = 8
window.resizable(width=False, height=False)

label1 = tk.Label(window, text='Blocking:')
label1.grid(row=0, column=0, sticky='nse')

# radio buttons to toggle blocking
rbValue = tk.IntVar()
rbValue.set(2)
radio1 = tk.Radiobutton(window, text='ON', value=1, variable=rbValue, command=block_site)
radio2 = tk.Radiobutton(window, text='OFF', value=2, variable=rbValue, command=unblock_site)
radio1.grid(row=0, column=1, sticky='nse')
radio2.grid(row=0, column=2, sticky='nse')

# add and remove buttons to add/remove website from website_list
addButton = tk.Button(window, text='Add Website', width=13, command=add_command)
removeButton = tk.Button(window, text='Remove Website', width=13, command=delete_command)
addButton.grid(row=3, column=3)
removeButton.grid(row=5, column=3)

# quit button
quitButton = tk.Button(window, text='Quit', width=13, command=window.destroy)
quitButton.grid(row=6, column=3)

# entry box to add website, linked to add button
addEntryValue = tk.StringVar()
addEntryBox = tk.Entry(window, textvariable=addEntryValue, width=30, relief='sunken')
addEntryBox.grid(row=3, column=0, columnspan=2)

label2 = tk.Label(window, text='Blocked Websites:')
label2.grid(row=4, column=1, sticky='nsw')

# listbox of currently blocked websites
blockedList = tk.Listbox(window, width=30)
blockedList.grid(row=5, column=0, rowspan=4, columnspan=2, sticky='nsew')
blockedList.config(border=1, relief='sunken')
blockedList.bind('<<ListboxSelect>>', get_selected_row)

listScroll = tk.Scrollbar(window, orient=tk.VERTICAL, command=blockedList.yview)
listScroll.grid(row=5, column=2, rowspan=4, sticky='nsw')
blockedList['yscrollcommand'] = listScroll.set

view_command()

if __name__ == '__main__':
    run_program()
