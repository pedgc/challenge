#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from tkinter import *
from tkinter import ttk
from ContractInteraction import Notifications
from Notifications import Notification, ErrorNotification, InvalidLengthError


class Authentication():
    def __init__(self):
        self.errorNotif = ErrorNotification()

    def obtainPrivateKey(self):
        try:
            # Main Window
            self.root = Tk()
            self.root.geometry('400x110')
            self.root.resizable(width=True,height=True)
            self.root.title('Authentication')

            # = = = = = = Widget Functionality = = = = = = = =
            privateKey = StringVar()
            self.labelPrivKey = ttk.Label(self.root, text="Private Key:")
            self.valuePrivKey = ttk.Entry(self.root, textvariable=privateKey, width=30)
            self.separ1 = ttk.Separator(self.root, orient=HORIZONTAL)

            self.bOK = ttk.Button(self.root, text="Use this Private Key", command=partial(self.validate, self.valuePrivKey) )

            self.labelPrivKey.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
            self.valuePrivKey.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
            self.separ1.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
            self.bOK.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

            self.root.mainloop()

            resul = hex(int("0x"+privateKey.get(), 16))
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "obtainPrivateKey")

        return resul

    def validate(self, valuePrivKey):
        try:
            if(len(valuePrivKey.get()) == 64):
                int(valuePrivKey.get(), 16)
                self.root.destroy()
            else:
                raise InvalidLengthError()
        except ValueError as v:
            error = "No hexadecimal format: "+str(v)
            self.errorNotif.showErrorNotif(error)
        except InvalidLengthError as v:
            error = "Invalid Lenght Error: The length must be 64 characters"
            self.errorNotif.showErrorNotif(error)
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "validate")
