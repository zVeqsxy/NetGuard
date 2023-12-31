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

def inputTxt(location):
	text = " NetGuard(" + Fore.BLUE + location + Fore.RESET +")$ "
	x = input(text)
	return x


def sayGoodBye():
	print("\n[" + Fore.BLUE + "I" + Fore.RESET + "] Bye ! :)")


active_addresses_label = """     _    ____ _____ _____     _______      _    ____  ____  ____  _____ ____ ____  _____ ____
    / \  / ___|_   _|_ _\ \   / / ____|    / \  |  _ \|  _ \|  _ \| ____/ ___/ ___|| ____/ ___|
   / _ \| |     | |  | | \ \ / /|  _|     / _ \ | | | | | | | |_) |  _| \___ \___ \|  _| \___ \\
  / ___ \ |___  | |  | |  \ V / | |___   / ___ \| |_| | |_| |  _ <| |___ ___) |__) | |___ ___) |
 /_/   \_\____| |_| |___|  \_/  |_____| /_/   \_\____/|____/|_| \_\_____|____/____/|_____|____/
																								"""

#############################################################################

main_options = """
 [1] Tools
 [2] Users

 [h] Help message    [c] Clear screen    [e] Exit
"""

# ----------------------------------------------------------------------------

tools_options = """
 [1] Scan
 [2] Capture packets
 [3] Blocking websites

 [b] Back to main menu    [h] Help message    [c] Clear screen    [e] Exit
"""

#----------------------------------------------------------------------------


users_options = """
 [1] Display users
 [2] Add users
 [3] Edit users
 [4] Delete users

 [b] Back to main menu    [h] Help message    [c] Clear screen    [e] Exit
"""

#############################################################################
