from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from plyer.utils import platform
from plyer import notification
from threading import Thread
from datetime import datetime
import time
from colorama import Fore, Back, init

POLL_INTERVAL = 1
#- - - - Pretty Print - - - -
ERROR = Back.BLACK + Fore.RED
TSTAMP = Fore.BLACK
FNAME = Fore.YELLOW
EXCEPTION = Fore.BLUE


class Notification():
    def __init__(self, obj):
        self.w3 = obj.w3
        self.NOTIF_EVENT = obj.contract.events.Notification()   # Needs to be instanciated due to Web3py limitations
        self.event_filter = self.NOTIF_EVENT.createFilter(fromBlock='latest')
        self.myAccount = obj.myAccount
        self.launchThread()

    def handle_event(self, event):
        receipt = self.w3.eth.wait_for_transaction_receipt(event['transactionHash'])
        result = self.NOTIF_EVENT.processReceipt(receipt, errors=STRICT)
        if (self.myAccount == str(result[0]['args']['_sender'])):
            notification.notify(
                title='Notification',
                message=str(result[0]['args']['_notif']),
                app_name='Text Challenge',
                app_icon='path/to/the/icon.png'
            )

    def log_loop(self, event_filter, poll_interval):
        while True:
            for event in event_filter.get_new_entries():
                self.handle_event(event)
            time.sleep(poll_interval)

    def launchThread(self):
        worker = Thread(target=self.log_loop, args=(self.event_filter, POLL_INTERVAL), daemon=True)
        worker.start()

class ErrorNotification():
    def __init__(self):
        a = 1

    def showErrorNotif(self, error):
        notification.notify(
            title='Error',
            message=error,
            app_name='Text Challenge',
            app_icon='path/to/the/icon.png'
        )

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
