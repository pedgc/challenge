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
from Notifications import Notification


class App():
    def __init__(self, levdist, dogsOrCats):

        # Main Window
        self.root = Tk()
        self.root.geometry('600x500')
        self.root.resizable(width=True,height=True)
        self.root.title('Admin')

        # = = = = = = Widget Functionality = = = = = = = =
        # Information Field
        self.tinfo = Text(self.root, width=70, height=20)
        self.separator1 = ttk.Separator(self.root, orient=HORIZONTAL)

        # Image Text Contest Buttons
        self.textFrame = ttk.Frame(self.root)
        self.binfo_text = ttk.Button(self.textFrame, text='Info', command=partial(self.info, levdist))
        self.bSetContest_text = ttk.Button(self.textFrame, text='Set Contest', command=partial(self.setContest, levdist))
        self.bResetContest_text = ttk.Button(self.textFrame, text='Reset Contest', command=levdist.resetContest)
        self.separator2 = ttk.Separator(self.root, orient=HORIZONTAL)

        # Dog Or Cat Contest Buttons
        self.DoCFrame = ttk.Frame(self.root)
        self.binfo_DoC = ttk.Button(self.DoCFrame, text='Info', command=partial(self.info, dogsOrCats))
        self.bSetContest_DoC = ttk.Button(self.DoCFrame, text='Set Contest', command=partial(self.setContest, dogsOrCats))
        self.bResetContest_DoC = ttk.Button(self.DoCFrame, text='Reset Contest', command=dogsOrCats.resetContest)
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
        self.bSetContest_text.pack(side=LEFT, fill=BOTH, expand=True, padx=0, pady=0)
        self.bResetContest_text.pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=0)
        self.separator2.pack(side=TOP, fill=BOTH, expand=True, padx=2, pady=1)

        # Dog Or Cat Contest Buttons
        self.DoCFrame.pack(side=TOP, fill=BOTH, expand=True)
        self.binfo_DoC.pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=0)
        self.bSetContest_DoC.pack(side=LEFT, fill=BOTH, expand=True, padx=0, pady=0)
        self.bResetContest_DoC.pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=0)
        self.separator3.pack(side=TOP, fill=BOTH, expand=True, padx=2, pady=1)

        # Exit Button
        self.bExit.pack(side=TOP, fill=BOTH, expand=True, padx=2, pady=0)

        # = = = = = = = = = = = = = =
        self.binfo_text.focus_set()
        self.root.mainloop()

    def setContest(self, contestObject):
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

        bCreate = ttk.Button(setContestWindow, text="Create", command=partial(self.validateAndCreate, contestObject, prize, valueSolution) )
        bCancel = ttk.Button(setContestWindow, text='Cancel', command=setContestWindow.destroy)

        labelPrize.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        valuePrize.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        labelSolution.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        valueSolution.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        separ1.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        bCreate.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        bCancel.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)
        bCancel.focus_set()

        self.root.wait_window(setContestWindow)

    def validateAndCreate(self, contestObject, prize, valueSolution):
        paramsAreValid = False

        if (isinstance(prize.get(), float)):
            if (isinstance(contestObject, TextImage)):
                if (isinstance(valueSolution.get(), str)):
                    contestObject.createContest(prize.get(), str(valueSolution.get()))
            elif (isinstance(contestObject, DogsOrCats)):
                if (isinstance(valueSolution.get(), str)):
                    solution = valueSolution.get().split(',')
                    solution = list(map(int, solution))
                    contestObject.createContest(prize.get(), solution)
                # PENDING TASK


    def info(self, contestObject):

        # Delete info of the textbox
        self.tinfo.delete("1.0", END)

        adminInfo = """
= = = = = = = = = = =
= ADMIN INFORMATION =
= = = = = = = = = = =
"""
        userInfo = """
= = = = = = = = = = =
= USER INFORMATION  =
= = = = = = = = = = =
"""

        text_info = adminInfo
        text_info += "Solution: " + str(contestObject.getSolution()) + "\n"
        text_info += "Winners: " + str(contestObject.getWinners()) + "\n"
        text_info += userInfo
        text_info += "Name: " + str(contestObject.getName()) + "\n"
        text_info += "Status: " + str(contestObject.getStatus()) + "\n"
        text_info += "Prize: " + str(contestObject.getPrize()) + "\n"
        text_info += "Prize Has Been Sent: " + str(contestObject.getPrizeHasBeenSent()) + "\n"
        text_info += "Contesters: " + str(contestObject.getContesters()) + "\n"
        text_info += "Admin: " + str(contestObject.getAdmin()) + "\n"

        # Insert info in the textbox
        self.tinfo.insert("1.0", text_info)
