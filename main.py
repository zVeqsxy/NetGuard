from scapy.all import *
from tabulate import tabulate
from colorama import Fore
from netaddr import EUI
from netaddr.core import AddrFormatError
import threading
import ipaddress
import random
import sys
import time
import os
import re

from classes.MySQL import MySqlCommands
from classes.IPScan import IPScanner
from classes.PacketSniffing import PacketSniffing
from lib.loading import loadingHack, loadingUpper, loadingTextPrint
from lib.menu import clear_prompt, header, sayGoodBye, inputTxt, main_options, tools_options, users_options
from lib.help import main_help, tools_help, users_help

scanner = IPScanner()
mysql = MySqlCommands()
sniffer = PacketSniffing()

# start the loading animation until the scan for the connected devices is done
def startLoading():
    num = random.choice([1, 2, 3])

    setup_thread = threading.Thread(target=scan)
    setup_thread.start()

    if num == 1:
        load = threading.Thread(target=loadingHack, args=(setup_thread,))
    elif num == 2:
        load = threading.Thread(target=loadingUpper, args=(setup_thread,))
    elif num == 3:
        load = threading.Thread(target=loadingTextPrint, args=(setup_thread,))

    load.start()
    setup_thread.join()
    load.join()

# ping and temporarly save every active ip, if not in database = insert into database
def scan():
    all_stored_mac_addr = mysql.getAllMacAddress()

    active_addr = scanner.startPing()
    active_mac = []
    active_ip = []

    for addr in active_addr:
        ip, mac = addr.split("|")
        if mac not in all_stored_mac_addr:
            active_ip.append(ip)
            active_mac.append(mac)

    for ip, mac in zip(active_ip, active_mac):
        mysql.insertUser(IP_address=ip, Mac_address=mac)
        print(" New user inserted: ", ip, mac)

def sniffing():
    print("\n [1] Sniff all packets on the network \n [2] Sniff packets for a specific user")
    choice = input(" Enter your choice: ")

    if choice == "1":
        filter = ""
    elif choice == "2":
        users, users_ID = displayAllUsers()
        user_pick = int(input(" Enter the ID of your desired user: "))

        if user_pick not in users_ID:
            print(" This ID does not exist.")
            return

        found_user = None
        for user in users:
            if user_pick == user[0]:
                found_user = user
                break

        if found_user:
            filter = "host " + found_user[5]
        else:
            print(" No user found.")
            return
    else:
        print(" Invalid choice.")
        return
    
    print("\n [1] Sniff on all interfaces \n [2] Sniff on a specific interface \n")
    interface_choice = input(" Enter your choice: ")

    interfaces = scanner.scanInterfaces()

    if len(interfaces) == 0:
        print(" No interfaces found.")
        return
    elif len(interfaces) == 1:
        print(f" Only one interface found: {''.join(interfaces)}. Sniffing on that interface..")
    else:
        if interface_choice == "2":
            print(f" Available interfaces: {interfaces}")
            interface = [input(" Enter your desired interface: ")]
            if interface not in interfaces:
                print(" Invalid interface.")
                return
        elif interface_choice != "1":
            print(" Invalid choice.")
            return

    print(" Starting to capture packets..")
    packets = sniffer.capturePackets(interfaces, filter)
    print(" Captured packets: ")
    print(packets)

def isValidIP(address):
    try:
        ipaddress.IPv4Address(address)
        return True
    except ipaddress.AddressValueError:
        return False

def getValidIP():
    while True:
        ip = input(" Enter IP: ")
        if isValidIP(ip):
            return ip
        print(" Invalid IP. Try again.\n")

def isValidMac(mac):
    try:
        EUI(mac)
        return True
    except (ValueError, AddrFormatError):
        return False

def getValidMac():
    while True:
        mac = input(" Enter MAC: ")
        if isValidMac(mac):
            return mac
        print(" Invalid MAC. Try again.\n")

def displayAllUsers():
    users = mysql.getAllInfo()
    data = [list(item) for item in users]
    users_ID = [item[0] for item in users]

    headers = ["ID", "Unique ID", "First Name", "Last Name", "Description", "IP-address", "MAC-address", "Blocked websites"]
    table = tabulate(data, headers=headers, tablefmt="fancy_grid", showindex="never")
    print(table)
    return users, users_ID

def addUser():
    print(" If there's something you dont know, just press Enter.")
    fname = input(" Enter First Name: ")
    lname = input(" Enter Last Name: ")
    description = input(" Enter Description: ")
    ip = getValidIP()
    mac = getValidMac()
    websites = input(" Enter Website to block (e.g. google). If multiple = (google, bing, youtube): ")

    mysql.insertUser(Fname=fname, Lname=lname, Description=description, IP_address=ip, Mac_address=mac, Blocked_websites=websites)

def editUser():
    users, users_ID = displayAllUsers()

    user_pick = int(input(" Enter the ID of your desired user: "))

    if user_pick not in users_ID:
        print(" This ID does not exist.")
        return

    found_user = None
    for user in users:
        if user_pick == user[0]:
            found_user = user
            break

    if found_user:
        headers = ["ID", "Unique ID", "First Name", "Last Name", "Description", "IP-address", "MAC-address", "Blocked websites"]
        data = [found_user]
        table = tabulate(data, headers=headers, tablefmt="psql")
        clear_prompt()
        print(table)
    else:
        print(" No user found.")
        return

    elements = {
        1: "Fname",
        2: "Lname",
        3: "Description",
        4: "Blocked_websites"
    } 

    choice = int(input("\n [1] Fname \n [2] Lname \n [3] Description \n [4] Blocked websites \n\n Pick something to edit: "))
    column = elements[choice]
    new_value = input(f"Enter new {column}: ")
    mysql.updateUser(column=column, new_value=new_value, ID=user_pick)

def deleteUser():
    users, users_ID = displayAllUsers()

    user_pick = int(input(" Enter the ID of your desired user: "))

    if user_pick not in users_ID:
        print(" This ID does not exist.")
        return

    found_user = None
    for user in users:
        if user_pick == user[0]:
            found_user = user
            break

    if found_user:
        mysql.deleteUser(user_pick)
    else:
        print(" No user found.")
        return
    
############################################################

def tools():
    header()
    print(tools_options)

    while True:
        choice = inputTxt("Tools")
        match choice:
            case "1":
                header()
                scan()
                scanner.displayActiveAddress()
                print(tools_options)

            # TODO: make the function to capture packets
            case "2":
                sniffing()

            # TODO: make the function to block websites
            case "3":
                print("\n Coming soon..")

            case "b":
                header()
                print(main_options)
                break

            case "h":
                print(tools_help)

            case "c":
                header()
                print(tools_options)

            case "e":
                menu["e"]()

def users():
    header()
    print(users_options)

    while True:
        choice = inputTxt("Users")
        
        match choice:
            case "1":
                header()
                displayAllUsers()
                print(users_options)
            
            case "2":
                addUser()

            case "3":
                header()
                editUser()

            case "4":
                header()
                deleteUser()

            case "b":
                header()
                print(main_options)
                break

            case "h":
                print(users_help)

            case "c":
                header()
                print(users_options)

            case "e":
                menu["e"]()
                
menu = {
    "1": tools,
    "2": users,
    "h": lambda: print(main_help),
    "c": lambda: (header(), print(main_options)),
    "e": lambda: sayGoodBye(sayGoodBye(), sys.exit(1))
}

def main():
    header()
    print(main_options)
    while True:
        choice = inputTxt("~")

        if choice in menu:
            menu[choice]()

if __name__ == "__main__":
    try:
        # startLoading()
        main()
    except Exception as e:
        print(e)
