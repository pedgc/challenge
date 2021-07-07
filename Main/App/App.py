#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style
from ContractInteraction import DogsOrCatsContract, TextImageContract, Notifications
from DogsOrCatsContract import DogsOrCats
from TextImageContract import TextImage
from Notifications import Notification, ErrorNotification


class App():
    def __init__(self, textImage, dogsOrCats):
        self.errorNotif = ErrorNotification()

        # Main Window
        style = Style(theme="flatly")
        self.root = style.master
        self.root.geometry('570x590')
        self.root.resizable(width=True,height=True)
        self.root.title('Admin')

        # = = = = = = Widget Functionality = = = = = = = =
        # Information Field
        self.tinfo = Text(self.root, width=75, height=20)

        # Image Text Contest Buttons
        self.textFrame = ttk.LabelFrame(self.root, text=' Text from Image ')
        self.innerFrame1_text = ttk.Frame(self.textFrame)
        self.binfo_text = ttk.Button(self.innerFrame1_text, text='Info', style="info.Outline.TButton", command=partial(self.info, textImage))
        self.bSetContest_text = ttk.Button(self.innerFrame1_text, text='Set Contest', command=partial(self.setContest, textImage))
        self.bResetContest_text = ttk.Button(self.innerFrame1_text, text='Reset Contest', style="primary.TButton", command=textImage.resetContest)
        self.bSetAdmin_text = ttk.Button(self.innerFrame1_text, text='Set Contract Admin', command=partial(self.setAddress, textImage))
        self.bCalculateWinners_text = ttk.Button(self.innerFrame1_text, text='Calculate Winner/s', command=textImage.calculateWinners)
        self.bSendPrize_text = ttk.Button(self.innerFrame1_text, text='Send Prize', style="primary.TButton", command=textImage.sendPrizeToWinners)
        self.innerFrame2_text = ttk.Frame(self.textFrame)
        self.bExpelWinner_text = ttk.Button(self.innerFrame2_text, text='Expel Winner', style="warning.TButton", command=textImage.sendPrizeToWinners)
        self.bSetAdmin_text = ttk.Button(self.innerFrame2_text, text='Set New Admin', style="danger.TButton", command=textImage.sendPrizeToWinners)

        # Dog Or Cat Contest Buttons
        self.DoCFrame = ttk.LabelFrame(self.root, text=' Dog or Cat ')
        self.innerFrame1_DoC = ttk.Frame(self.DoCFrame)
        self.binfo_DoC = ttk.Button(self.innerFrame1_DoC, text='Info', style="info.Outline.TButton", command=partial(self.info, dogsOrCats))
        self.bSetContest_DoC = ttk.Button(self.innerFrame1_DoC, text='Set Contest', command=partial(self.setContest, dogsOrCats))
        self.bResetContest_DoC = ttk.Button(self.innerFrame1_DoC, text='Reset Contest', command=dogsOrCats.resetContest)
        self.bSetAdmin_DoC = ttk.Button(self.innerFrame1_DoC, text='Set Contract Admin', command=partial(self.setAddress, dogsOrCats))
        self.bCalculateWinners_DoC = ttk.Button(self.innerFrame1_DoC, text='Calculate Winner/s', command=dogsOrCats.calculateWinners)
        self.bSendPrize_DoC = ttk.Button(self.innerFrame1_DoC, text='Send Prize', command=dogsOrCats.sendPrizeToWinners)
        self.innerFrame2_DoC = ttk.Frame(self.DoCFrame)
        self.separator3 = ttk.Separator(self.root, orient=HORIZONTAL)
        self.bExpelWinner_DoC = ttk.Button(self.innerFrame2_DoC, text='Expel Winner', style="warning.TButton", command=dogsOrCats.sendPrizeToWinners)
        self.bSetAdmin_DoC = ttk.Button(self.innerFrame2_DoC, text='Set New Admin', style="danger.TButton", command=dogsOrCats.sendPrizeToWinners)

        # Exit Button
        self.bExit = ttk.Button(self.root, text='Exit', style="secondary.TButton", command=self.root.destroy)

        # = = = = = = Widget Placement = = = = = = = =
        # Information Field
        self.tinfo.pack(side=TOP, pady=4)

        # Image Text Contest Buttons
        self.textFrame.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=8)
        self.innerFrame1_text.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=1)
        self.binfo_text.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)
        self.bSetContest_text.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)
        self.bResetContest_text.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)
        self.bCalculateWinners_text.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)
        self.bSendPrize_text.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)
        self.innerFrame2_text.pack(side=BOTTOM, fill=BOTH, expand=True, padx=0, pady=1)
        self.bExpelWinner_text.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)
        self.bSetAdmin_text.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)

        # Dog Or Cat Contest Buttons
        self.DoCFrame.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=8)
        self.innerFrame1_DoC.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=1)
        self.binfo_DoC.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)
        self.bSetContest_DoC.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)
        self.bResetContest_DoC.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)
        self.bCalculateWinners_DoC.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)
        self.bSendPrize_DoC.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)
        self.innerFrame2_DoC.pack(side=BOTTOM, fill=BOTH, expand=True, padx=1, pady=1)
        self.bExpelWinner_DoC.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)
        self.bSetAdmin_DoC.pack(side=LEFT, fill=BOTH, expand=True, padx=1, pady=0)
        self.separator3.pack(side=TOP, fill=BOTH, expand=True, padx=2, pady=1)

        # Exit Button
        self.bExit.pack(side=TOP, fill=BOTH, expand=True, padx=2, pady=2)

        # = = = = = = = = = = = = = =
        self.binfo_text.focus_set()
        self.root.mainloop()

    # Set Contest Window
    def setContest(self, contestObject):
        try:
            setContestWindow = Toplevel()
            setContestWindow.geometry('300x200')
            setContestWindow.resizable(width=True,height=True)
            setContestWindow.title("Set Contest")
            setContestWindow.transient(master=self.root)
            setContestWindow.grab_set()

            prize = DoubleVar()
            labelPrize = ttk.Label(setContestWindow, text="Prize [ETH]:")
            labelSolution = ttk.Label(setContestWindow, text="Solution:")
            valuePrize = ttk.Entry(setContestWindow, textvariable=prize, width=10)
            valueSolution = ttk.Entry(setContestWindow, width=30)
            separ1 = ttk.Separator(setContestWindow, orient=HORIZONTAL)

            bCreate = ttk.Button(setContestWindow, text="Create", style="success.TButton", command=partial(self.validateAndCreate, contestObject, prize, valueSolution) )
            bCancel = ttk.Button(setContestWindow, text='Cancel', style="secondary.TButton", command=setContestWindow.destroy)

            labelPrize.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
            valuePrize.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
            labelSolution.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
            valueSolution.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
            separ1.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
            bCreate.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
            bCancel.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
            bCancel.focus_set()

            self.root.wait_window(setContestWindow)
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "setContest")

    # Set Contract Admin Address Window
    def setAddress(self, contestObject):
        try:
            setAddressWindow = Toplevel()
            setAddressWindow.geometry('300x120')
            setAddressWindow.resizable(width=True,height=True)
            setAddressWindow.title("Set Contest Name")
            setAddressWindow.transient(master=self.root)
            setAddressWindow.grab_set()

            Address = StringVar()
            labelAddress = ttk.Label(setAddressWindow, text="New Admin Address:")
            valueAddress = ttk.Entry(setAddressWindow, width=30)
            separ1 = ttk.Separator(setAddressWindow, orient=HORIZONTAL)

            bChange = ttk.Button(setAddressWindow, text="Change Address", command=lambda : contestObject.setAdmin(valueAddress.get()))
            bCancel = ttk.Button(setAddressWindow, text='Cancel', command=setAddressWindow.destroy)

            labelAddress.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
            valueAddress.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
            separ1.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
            bChange.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
            bCancel.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
            bCancel.focus_set()

            self.root.wait_window(setAddressWindow)
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "setAddress")

    def validateAndCreate(self, contestObject, prize, valueSolution):
        try:
            if (isinstance(prize.get(), float)):
                if (isinstance(contestObject, TextImage)):
                    if (isinstance(valueSolution.get(), str)):
                        contestObject.createContest(prize.get(), str(valueSolution.get()))
                elif (isinstance(contestObject, DogsOrCats)):
                    if (isinstance(valueSolution.get(), str)):
                        solution = valueSolution.get().split(',')
                        solution = list(map(int, solution))
                        contestObject.createContest(prize.get(), solution)
        except ValueError as v:
            error = "Incorrect Solution Format: "+str(v)
            self.errorNotif.showErrorNotif(error)
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "validateAndCreate")


    def info(self, contestObject):
        try:
            # Delete info of the textbox
            self.tinfo.delete("1.0", END)

            adminInfo = """
\t\t   ADMIN INFORMATION
\t\t-----------------------------------------
"""
            userInfo = """
\t\t   USER INFORMATION
\t\t----------------------------------------
"""

            text_info = adminInfo
            text_info += "Solution: " + str(contestObject.getSolution()) + "\n"
            text_info += userInfo
            text_info += self.info_getName(contestObject)
            text_info += self.info_getStatus(contestObject)
            text_info += self.info_getPrize(contestObject)
            text_info += self.info_getContesters(contestObject)
            text_info += self.info_getWinners(contestObject)
            text_info += self.info_getPrizeHasBeenSent(contestObject)
            text_info += self.info_getAdmin(contestObject)

            # Insert info in the textbox
            self.tinfo.insert("1.0", text_info)
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "info")


    def info_getName(self, contestObject):
        resul = ""
        try:
            resul = "\t"+str(contestObject.getName())+"\n"
            resul = resul.upper()
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "info_getName")
        return resul

    def info_getStatus(self, contestObject):
        resul = "The contest is NOT active\n"
        try:
            if (contestObject.getStatus()):
                resul = "The contest is ACTIVE\n"
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "info_getStatus")
        return resul

    def info_getPrize(self, contestObject):
        resul = ""
        try:
            resul = "Prize: "+str(contestObject.getPrize())+" ETH\n"
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "info_getPrize")
        return resul

    def info_getContesters(self, contestObject):
        resul = "There are no contesters yet\n"
        try:
            contesters = contestObject.getContesters()
            if(contesters):
                i = 1
                resul = "Contesters ["+str(len(contesters))+"]\n"
                for contester in contesters:
                    resul += "\t"+str(i)+". "+str(contester)+"\n"
                    i += 1
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "info_getContesters")
        return resul

    def info_getWinners(self, contestObject):
        resul = "Winners have not been selected yet\n"
        try:
            winners = contestObject.getWinners()
            if(winners):
                i = 1
                resul = "Winners ["+str(len(winners))+"]\n"
                for winner in winners:
                    resul += "\t"+str(i)+". "+str(winner)+"\n"
                    i += 1
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "info_getWinners")
        return resul

    def info_getPrizeHasBeenSent(self, contestObject):
        resul = "Prize has NOT been sent yet\n"
        try:
            winners = contestObject.getWinners()
            if(contestObject.getPrizeHasBeenSent()):
                resul = "Prize has been sent\n"
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "info_getPrizeHasBeenSent")
        return resul

    def info_getAdmin(self, contestObject):
        resul = ""
        try:
            resul = "Admin: "+str(contestObject.getAdmin())+"\n"
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "info_getAdmin")
        return resul
