import sys
import random
import time
import threading

def loadingHack(thread_):
    chaine = "[*] Performing database operations..."
    chars = "$*.X^%_/\\#~!?;"
    chars_len = len(chars)

    while thread_.is_alive():
        chainehack = ""
        for c in chaine:
            chainehack += c
            r = random.choice(chars) + random.choice(chars) + random.choice(chars)
            sys.stdout.write('\r' + chainehack + r)
            sys.stdout.flush()
            time.sleep(0.06)

        if len(chainehack) == len(chaine):
            sys.stdout.write('\n')
            sys.stdout.flush()
            break


def loadingUpper(thread_):
    string = "Performing database operations"
    string = list(string)
    nb = len(string)

    while thread_.is_alive():
        x = 0
        while x < nb:
            c = string[x]
            c = c.upper()
            string[x] = c
            sys.stdout.write("\r[*] " + ''.join(string) + '...')
            sys.stdout.flush()
            time.sleep(0.1)
            c = string[x]
            c = c.lower()
            string[x] = c
            x += 1

    print()

def loadingTextPrint(thread_):
    string = "Performing database operations..."

    while thread_.is_alive():
        space = " " * 100
        sys.stdout.write("\r"+space)

        x = 1

        while x <= len(string):
            times = "0."
            times += str(random.choice(range(1, 3)))
            sys.stdout.write("\rroot@littlebrother:~$ "+string[:x]+"|")
            time.sleep(float(times))
        x += 1

    print()
