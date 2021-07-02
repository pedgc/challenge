#!/usr/bin/env python
# -*- coding: utf-8 -*-

from colorama import Fore, Back, init
import sys
sys.path.insert(0, 'App')
sys.path.insert(0, 'App/ContractInteraction')
from App import App
from ContractInteraction import DogsOrCatsContract, TextImageContract, Notifications
from DogsOrCatsContract import DogsOrCats
from TextImageContract import TextImage
from Notifications import Notification

#- - - - Pretty Print variables - - - -
TITLE = Back.BLACK + Fore.RED
BLUE = Fore.BLUE
EVENT = Fore.YELLOW

def main():
    # - - - Pretty Print - - -
    init(autoreset=True)
    print(Back.GREEN +"\n")

    #- - - - - Launch GUI - - - - -
    textimage = TextImage()
    dogorcat = DogsOrCats()
    notif_lev = Notification(textimage)
    notif_dog = Notification(dogorcat)
    mi_app = App(textimage, dogorcat)
    return 0

if __name__ == '__main__':
    main()
