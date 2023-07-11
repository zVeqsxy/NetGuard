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
from lib.loading import loadingHack, loadingUpper, loadingTextPrint
from lib.menu import clear_prompt, header, say_good_bye, input_txt, mainOptions, toolsOptions, usersOptions
from lib.help import mainHelp, toolsHelp, usersHelp

scanner = IPScanner()
mysql = MySqlCommands()

def startloading():
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
    all_mac_addr = mysql.getAllMacAddress()

    active_addr = scanner.startPing()
    active_mac = []
    active_ip = []

    for addr in active_addr:
        ip, mac = addr.split("|")
        active_ip.append(ip)
        active_mac.append(mac)

    for i in range(len(active_mac)):
        if active_mac[i] not in all_mac_addr:
            mysql.insertUser(IP_address=active_ip[i], Mac_address=active_mac[i])

def sniffing():
    print("\n [1] Sniff all packets on the network \n [2] Sniff packets for a specific user")
    location_choice = int(input(" Enter your choice: "))

    print("\n [1] All interfaces \n [2] Specific interface \n")
    interface_choice = int(input(" Enter your choice: "))

    interfaces = scanner.scanInterfaces()

    if interface_choice == 1:
        if location_choice == 1:
            packets = sniff(filter="", count=10, iface=interfaces)

        elif location_choice == 2:
            _, users_ID = displayAllUsers()
            try: 
                id = int(input(" Enter the ID of your desired user: "))
                if id not in users_ID:
                    print(" This ID does not exist.")
                    return

                packets = sniff(filter="host " + ip, count=10, iface=interfaces)

            except:
                print(" Invalid input.")
                return

# packets = sniff(filter="", count=10, iface=interfaces)
# packets = sniff(filter="host " + ip, count=10, iface=interfaces)
# packets = sniff(filter="ether host " + mac, count=10, iface=interfaces)


    elif interface_choice == 2:
        for i, interface in enumerate(interfaces):
            print(f"{i}. {interface}")

        try:
            choice3 = int(input("\n Enter your choice: "))
            interface = interfaces[choice3 - 1]
        except:
            print("Invalid choice")
            return

        if location_choice == 1:
            packets = sniff(filter="", count=10, iface=interface)
        elif location_choice == 2:
            ip = input("Enter IP address: ")
            packets = sniff(filter="host " + ip, count=10, iface=interface)
        elif location_choice == 3:
            mac = input("Enter MAC address: ")
            packets = sniff(filter="ether host " + mac, count=10, iface=interface)

    else:
        print("Invalid choice")
        return

    if packets:
        return packets
    
    else:
        print("No packets found")
        return


################################################################################################################################################################
################################################################################################################################################################

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
    mysql.updateUser(column=column, new_value=new_value, ID_=user_pick)

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

def main():
    try:
        header()
        print(mainOptions)
        while True:
            choice = input_txt("~")

            # TOOLS
            if choice == "1":
                header()
                print(toolsOptions)

                while True:
                    choice = input_txt("Tools")
                    if choice == "1":              
                        header()
                        scan()
                        scanner.displayActiveAddress()
                        print(toolsOptions)

                    elif choice == "2":            
                        print("\n Coming soon..")

                    elif choice == "3":            
                        print("\n Coming soon..")

                    elif choice == "b":
                        header()
                        print(mainOptions)
                        break
                    
                    elif choice == "h":
                        print(toolsHelp)
                    
                    elif choice == "c":
                        header()
                        print(toolsOptions)

                    elif choice == "e":
                        say_good_bye()
                        sys.exit(1)

            # USERS
            elif choice == "2":
                header()
                print(usersOptions)

                while True:
                    choice = input_txt("Users")
                    if choice == "1":                   
                        header()
                        displayAllUsers()
                        print(usersOptions)

                    elif choice == "2":                 
                        addUser()

                    elif choice == "3":                
                        header()
                        editUser()

                    elif choice == "4":                 
                        header()
                        deleteUser()

                    elif choice == "b":
                        header()
                        print(mainOptions)
                        break
                    
                    elif choice == "h":
                        print(usersHelp)
                    
                    elif choice == "c":
                        header()
                        print(usersOptions)

                    elif choice == "e":
                        say_good_bye()
                        sys.exit(1)

            elif choice == "h":
                print(mainHelp)

            elif choice == "c":
                header()
                print(mainOptions)

            elif choice == "e":
                say_good_bye()
                break

            else:
                return main()

    except Exception as e:
        print(e)

main()
