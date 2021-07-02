#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from tkinter import *
from tkinter import ttk
import sys
sys.path.insert(0, 'App/ContractInteraction')
from ContractInteraction import DogsOrCatsContract, TextImageContract, Notifications
from DogsOrCatsContract import DogsOrCats
from TextImageContract import TextImage
from Notifications import Notification, ErrorNotification


class App():
    def __init__(self, textImage, dogsOrCats):
        self.errorNotif = ErrorNotification()
        # Main Window
        self.root = Tk()
        self.root.geometry('500x400')
        self.root.resizable(width=True,height=True)
        self.root.title('User')

        # = = = = = = Widget Functionality = = = = = = = =
        # Information Field
        self.tinfo = Text(self.root, width=60, height=15)
        self.separator1 = ttk.Separator(self.root, orient=HORIZONTAL)

        # Image Text Contest Buttons
        self.textFrame = ttk.Frame(self.root)
        self.binfo_text = ttk.Button(self.textFrame, text='Info', command=partial(self.info, textImage))
        self.bContest_text = ttk.Button(self.textFrame, text='Send Result', command=partial(self.Contest, textImage))
        self.separator2 = ttk.Separator(self.root, orient=HORIZONTAL)

        # Dog Or Cat Contest Buttons
        self.DoCFrame = ttk.Frame(self.root)
        self.binfo_DoC = ttk.Button(self.DoCFrame, text='Info', command=partial(self.info, dogsOrCats))
        self.bContest_DoC = ttk.Button(self.DoCFrame, text='Send Result', command=partial(self.Contest, dogsOrCats))
        self.separator3 = ttk.Separator(self.root, orient=HORIZONTAL)

        # Exit Button
        self.bExit = ttk.Button(self.root, text='Exit', command=self.root.destroy)

        # = = = = = = Widget Placement = = = = = = = =
        # Information Field
        self.tinfo.pack(side=TOP)
        self.separator1.pack(side=TOP, fill=BOTH, expand=True, padx=2, pady=1)

        # Image Text Contest Buttons
        self.textFrame.pack(side=TOP, fill=BOTH, expand=True)
        self.binfo_text.pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=0)
        self.bContest_text.pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=0)
        self.separator2.pack(side=TOP, fill=BOTH, expand=True, padx=2, pady=1)

        # Dog Or Cat Contest Buttons
        self.DoCFrame.pack(side=TOP, fill=BOTH, expand=True)
        self.binfo_DoC.pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=0)
        self.bContest_DoC.pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=0)
        self.separator3.pack(side=TOP, fill=BOTH, expand=True, padx=2, pady=1)

        # Exit Button
        self.bExit.pack(side=TOP, fill=BOTH, expand=True, padx=2, pady=0)

        # = = = = = = = = = = = = = =
        self.binfo_text.focus_set()
        self.root.mainloop()

    # Set Contest Window
    def Contest(self, contestObject):
        try:
            contestWindow = Toplevel()
            contestWindow.geometry('300x120')
            contestWindow.resizable(width=True,height=True)
            contestWindow.title("Set Contest")
            contestWindow.transient(master=self.root)
            contestWindow.grab_set()


            labelSolution = ttk.Label(contestWindow, text="Solution:")
            valueSolution = ttk.Entry(contestWindow, width=30)
            separ1 = ttk.Separator(contestWindow, orient=HORIZONTAL)

            bSend = ttk.Button(contestWindow, text="Send", command=partial(self.validateAndContest, contestObject, valueSolution) )
            bCancel = ttk.Button(contestWindow, text='Cancel', command=contestWindow.destroy)

            labelSolution.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
            valueSolution.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
            separ1.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
            bSend.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
            bCancel.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
            bCancel.focus_set()

            self.root.wait_window(contestWindow)
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif()
            print("\nERROR:\n\t" + str(e))

    def validateAndContest(self, contestObject, valueSolution):
        paramsAreValid = False

        try:
            if (type(contestObject) is TextImage):
                if (isinstance(valueSolution.get(), str)):
                    print("TextImage Solution: "+str(valueSolution.get()))
                    contestObject.contest(str(valueSolution.get()))
            elif (type(contestObject) is DogsOrCats):
                if (isinstance(valueSolution.get(), str)):
                    print("DogsOrCats Solution: "+str(valueSolution.get()))
                    solution = valueSolution.get().split(',')
                    solution = list(map(int, solution))
                    contestObject.contest(solution)
        except ValueError as v:
            error = "Incorrect Solution Format: "+str(v)
            self.errorNotif.showErrorNotif(error)
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif()
            print("\nERROR:\n\t" + str(e))


    def info(self, contestObject):
        try:
            # Delete info of the textbox
            self.tinfo.delete("1.0", END)

            userInfo = """
= = = = = = = = = = =
= USER INFORMATION  =
= = = = = = = = = = =
"""
            text_info = userInfo
            text_info += "Name: " + str(contestObject.getName()) + "\n"
            text_info += "Status: " + str(contestObject.getStatus()) + "\n"
            text_info += "Prize: " + str(contestObject.getPrize()) + "\n"
            text_info += "Prize Has Been Sent: " + str(contestObject.getPrizeHasBeenSent()) + "\n"
            text_info += "Contesters: " + str(contestObject.getContesters()) + "\n"
            text_info += "Admin: " + str(contestObject.getAdmin()) + "\n"

            # Insert info in the textbox
            self.tinfo.insert("1.0", text_info)
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif()
            print("\nERROR:\n\t" + str(e))
