from colorama import Fore
import os

def clear_prompt():
	os.system("cls")


def header():
	clear_prompt()
	header = """
	███╗░░██╗███████╗████████╗░██████╗░██╗░░░██╗░█████╗░██████╗░██████╗░
	████╗░██║██╔════╝╚══██╔══╝██╔════╝░██║░░░██║██╔══██╗██╔══██╗██╔══██╗
	██╔██╗██║█████╗░░░░░██║░░░██║░░██╗░██║░░░██║███████║██████╔╝██║░░██║
	██║╚████║██╔══╝░░░░░██║░░░██║░░╚██╗██║░░░██║██╔══██║██╔══██╗██║░░██║
	██║░╚███║███████╗░░░██║░░░╚██████╔╝╚██████╔╝██║░░██║██║░░██║██████╔╝
	╚═╝░░╚══╝╚══════╝░░░╚═╝░░░░╚═════╝░░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░

"""
	print(header)


def input_txt(location):
	text = " NetGuard(" + Fore.BLUE + location + Fore.RESET +")$ "
	x = input(text)
	return x


def say_good_bye():
	print("\n[" + Fore.BLUE + "I" + Fore.RESET + "] Bye ! :)")


#############################################################################

mainOptions = """
 [1] Tools
 [2] Users

 [h] Help message    [c] Clear screen    [e] Exit
"""

# ----------------------------------------------------------------------------

toolsOptions = """
 [1] Scan
 [2] Capture packets
 [3] Blocking websites

 [b] Back to main menu    [h] Help message    [c] Clear screen    [e] Exit
"""

#----------------------------------------------------------------------------


usersOptions = """
 [1] Display users
 [2] Add users
 [3] Edit users
 [4] Delete users

 [b] Back to main menu    [h] Help message    [c] Clear screen    [e] Exit
"""

#############################################################################
