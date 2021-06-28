#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from colorama import Fore, Back, init #,Style
from threading import Thread
import time
from functools import partial
from LevDistContract import *
from Notifications import *

#- - - - Pretty Print variables - - - -
TITLE = Back.BLACK + Fore.RED
BLUE = Fore.BLUE
EVENT = Fore.YELLOW

class App():
    def __init__(self, levdist):

        self.root = Tk()
        self.root.geometry('600x400')
        self.root.resizable(width=True,height=True)
        self.root.title('Admin')

        self.tinfo = Text(self.root, width=60, height=10)
        self.tinfo.pack(side=TOP)

        self.binfo = ttk.Button(self.root, text='Info', command=partial(self.info, levdist))
        self.binfo.pack(side=LEFT)

        self.bSetContest = ttk.Button(self.root, text='Set Contest', command=partial(self.setContest, levdist))
        self.bSetContest.pack(side=LEFT)

        self.bResetContest = ttk.Button(self.root, text='Reset Contest', command=levdist.resetContest)
        self.bResetContest.pack(side=LEFT)

        self.bExit = ttk.Button(self.root, text='Exit', command=self.root.destroy)
        self.bExit.pack(side=RIGHT)

        self.binfo.focus_set()
        self.root.mainloop()

    def setContest(self, levdist):
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

        bCreate = ttk.Button(setContestWindow, text="Create", command=lambda : levdist.createContest(prize.get(), str(valueSolution.get())))
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



    def info(self, levdist):

        # Borra el contenido que tenga en un momento dado
        # la caja de texto
        self.tinfo.delete("1.0", END)

        # Obtiene información de la ventana 'self.root':
        info1 = str(levdist.getInitStatus())
        info2 = str(levdist.getAdmin())
        info3 = str(levdist.getSolution())
        info4 = str(levdist.getPrize())
        info5 = str(levdist.getWinners())
        info6 = str(levdist.getName())

        # Construye una cadena de texto con toda la
        # información obtenida:
        texto_info = "Status: " + info1 + "\n"
        texto_info += "Admin: " + info2 + "\n"
        texto_info += "Solution: " + info3 + "\n"
        texto_info += "Prize: " + info4 + "\n"
        texto_info += "Winners: " + info5 + "\n"
        texto_info += "Name: " + info6 + "\n"

        # Inserta la información en la caja de texto:
        self.tinfo.insert("1.0", texto_info)

def main():
    # - - - Pretty Print - - -
    init(autoreset=True)
    print(Back.GREEN +"\n")

    # #- - - - - Listen to Events in Thread - - - -
    # block_filter = w3.eth.filter({'fromBlock':'latest', "address": CONTRACT_ADDR})
    # event_filter = WINNER_EVENT.createFilter(fromBlock='latest')
    # worker = Thread(target=log_loop, args=(event_filter, POLL_INTERVAL), daemon=True)
    # worker.start()

    #- - - - - Launch GUI - - - - -
    notif = Notifications()
    levdist = LevDistContract()
    mi_app = App(levdist)
    return 0

if __name__ == '__main__':
    main()
