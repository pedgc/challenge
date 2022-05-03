#!/usr/bin/env python
# -*- coding: utf-8 -*-

from colorama import Fore, Back, init
import sys
sys.path.insert(0, 'App')
sys.path.insert(0, 'App/ContractInteraction')
from AppAdmin import App
from Auth import Authentication
from ContractInteraction import DogsOrCatsContract, TextImageContract, Notifications
from DogsOrCatsContract import DogsOrCats
from TextImageContract import TextImage
from Notifications import Notification


def main():
    try:
        # - - - Pretty Print - - -
        init(autoreset=True)
        print(Back.GREEN +"\n")
        print(Fore.BLUE + "The program started correctly")

        #- - - - - Launch GUI - - - - -
        try:
            privKey = Authentication().obtainPrivateKey()
        except (UnboundLocalError) as e:
            privKey = 0x0

        if privKey != 0x0:
            textimage = TextImage(privKey)
            dogorcat = DogsOrCats(privKey)
            privKey = 0x0
            notif_lev = Notification(textimage)
            notif_dog = Notification(dogorcat)
            mi_app = App(textimage, dogorcat)
        print("Program was closed")

    except Exception as e:
        self.errorNotif.showUnexpErrorNotif(e, "main()")

    return 0

if __name__ == '__main__':
    main()
