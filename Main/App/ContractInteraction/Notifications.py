from web3 import Web3
from web3.exceptions import ContractLogicError, TransactionNotFound, SolidityError
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from plyer.utils import platform
from plyer import notification
from threading import Thread
from datetime import datetime
import time
# import asyncio
from colorama import Fore, Back, init

POLL_INTERVAL = 5
#- - - - Pretty Print - - - -
ERROR = Back.BLACK + Fore.RED
TSTAMP = Fore.BLACK
FNAME = Fore.YELLOW
EXCEPTION = Fore.BLUE
OK = Fore.GREEN


class Notification():
    def __init__(self, obj):
        self.w3 = obj.w3
        self.contract = obj.contract
        self.NOTIF_EVENT = obj.contract.events.Notification()   # Needs to be instanciated due to Web3py limitations
        self.myAccount = obj.myAccount

    def event(self, tx_hash):
        worker = Thread(target=self.handle_event, args=(tx_hash, POLL_INTERVAL), daemon=True)
        worker.start()

    def handle_event(self, tx_hash, poll_interval):
        notification.notify(
            title='Notification',
            message="Waiting for the transaction to be mined. Please read cmd to obtain more info",
            app_name='Text Challenge',
            app_icon='path/to/the/icon.png'
        )
        event_received = False
        i = 0
        print(FNAME+"\n- - - - - - - - - - - - - - - - - - - -")
        print(FNAME+"Waiting for the transaction to be mined")
        while event_received == False:
            try:
                tx_receipt = self.w3.eth.get_transaction_receipt(tx_hash)
                event = self.contract.events.Notification().processReceipt(tx_receipt)
                if (event):
                    event_received = True
                    message = str(event[0]['args']['_notif'])
                    notification.notify(
                        title='Notification',
                        message=message,
                        app_name='Text Challenge',
                        app_icon='path/to/the/icon.png'
                    )
                    print(OK+message)
                else:
                    event_received = True
                    url = "https://ropsten.etherscan.io/tx/"+str(tx_receipt['transactionHash'].hex())
                    message = "The transaction was reverted. Check the reason here:\t\n"+url
                    notification.notify(
                        title='Notification',
                        message=message,
                        app_name='Text Challenge',
                        app_icon='path/to/the/icon.png'
                    )
                    print(ERROR+"\nTRANSACTION REVERTED")
                    print(EXCEPTION+message)
            except TransactionNotFound as t:
                print(FNAME+"Not mined yet! ["+str(i*poll_interval)+"s]")
                i += 1
                time.sleep(poll_interval)

class ErrorNotification():
    def __init__(self):
        pass

    def showErrorNotif(self, error):
        if "replacement transaction" in error:
            error = "Please check if you have any pending transactions. If not, wait a few moments and try again.\n"
            url = "https://ropsten.etherscan.io/address/"+str(self.myAccount)
            error = error + url
        notification.notify(
            title='Error',
            message=error,
            app_name='Text Challenge',
            app_icon='path/to/the/icon.png'
        )
        print(ERROR+"\nERROR")
        print(TSTAMP+"<"+str(datetime.now().strftime("%H:%M:%S.%f"))+"> "+FNAME+"["+f_name+"]")
        print(EXCEPTION+str(type(error))+": "+str(error))

    def showUnexpErrorNotif(self, error, f_name):
        notification.notify(
            title='Error',
            message='Unexpected Error: Please read command line to obtain more info',
            app_name='Text Challenge',
            app_icon='path/to/the/icon.png'
        )
        print(ERROR+"\nERROR")
        print(TSTAMP+"<"+str(datetime.now().strftime("%H:%M:%S.%f"))+"> "+FNAME+"["+f_name+"]")
        print(EXCEPTION+str(type(error))+": "+str(error))

class InvalidLengthError(Exception):
    pass
