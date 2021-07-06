from web3 import Web3
from web3.exceptions import ContractLogicError, TransactionNotFound
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from plyer.utils import platform
from plyer import notification
from threading import Thread
from datetime import datetime
import time
import asyncio
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

        # # self.w3 = Web3(Web3.HTTPProvider(NODE_HTTP))
        # self.w3 = Web3(Web3.AsyncHTTPProvider(obj.node_http))
        # self.contract = self.w3.eth.contract(address=obj.contract_addr, abi=obj.abi)
        self.contract = obj.contract
        self.NOTIF_EVENT = obj.contract.events.Notification()   # Needs to be instanciated due to Web3py limitations
        # self.event_filter = self.NOTIF_EVENT.createFilter(fromBlock='latest')
        self.event_filter = self.NOTIF_EVENT.createFilter(fromBlock='latest')
        # self.tx_filter = self.NOTIF_EVENT.createFilter(fromBlock='pending')
        self.myAccount = obj.myAccount
        # self.launchThread()
        # self.start()

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
        print("EVENT RECEIVED: "+str(result[0]['args']['_notif']))

    def log_loop(self, event_filter, poll_interval):
        while True:
            for event in event_filter.get_new_entries():
                self.handle_event(event)
            time.sleep(poll_interval)
    # async def log_loop(self, event_filter, poll_interval):
    #     while True:
    #         try:
    #             for event in event_filter.get_new_entries():
    #                 self.handle_event(event)
    #             await asyncio.sleep(poll_interval)
    #         except ValueError as v:
    #             dict = literal_eval(str(v))
    #             self.errorNotif.showErrorNotif(str(dict['message']))
    #         except ContractLogicError as v:
    #             print("\tERROR - AppUser/validateAndContest: \n"+str(v))

    def launchThread(self):
        worker = Thread(target=self.log_loop, args=(self.event_filter, POLL_INTERVAL), daemon=True)
        worker.start()
    # def launchThread(self):
    #     worker = Thread(target=self.start2, args=(), daemon=True)
    #     worker.start()
    #
    # def start2(self):
    #     asyncio.set_event_loop(asyncio.new_event_loop())
    #     loop = asyncio.get_event_loop()
    #
    #     try:
    #         loop.run_until_complete(
    #             asyncio.gather(
    #                 self.log_loop(self.event_filter, POLL_INTERVAL)))
    #     finally:
    #         loop.close()

    def event(self, tx_hash):
        worker = Thread(target=self.handle_it, args=(tx_hash, 5), daemon=True)
        worker.start()

    # def event2(self, tx_hash):
    #     asyncio.set_event_loop(asyncio.new_event_loop())
    #     loop = asyncio.get_event_loop()
    #     try:
    #         loop.run_until_complete(
    #             asyncio.gather(
    #                 self.handle_it2(self.event_filter, POLL_INTERVAL)))
    #     finally:
    #         loop.close()
    # async def event2(self, tx_hash):
    #     asyncio.run(self.handle_it2(self.event_filter, POLL_INTERVAL))
    #     await asyncio.gather(self.handle_it2(self.event_filter, POLL_INTERVAL))
    # def event2(self, tx_hash):
    #     # asyncio.set_event_loop(asyncio.new_event_loop())
    #     try:
    #         self.loop.run_until_complete(self.handle_it2(tx_hash, POLL_INTERVAL))
    #     finally:
    #         loop.close()

    def handle_it(self, tx_hash, poll_interval):
        notification.notify(
            title='Notification',
            message="Waiting for the transaction to be mined. Please read cmd to obtain more info",
            app_name='Text Challenge',
            app_icon='path/to/the/icon.png'
        )
        event_received = False
        i = 0
        while event_received == False:
            try:
                print("Waiting for the transaction to be mined ["+str(i*5)+"s]")
                i += 1
                tx_receipt = self.w3.eth.get_transaction_receipt(tx_hash)
                event = self.contract.events.Notification().processReceipt(tx_receipt)
                if (event):
                    print("EVENT RECEIVED (contest): "+str(event[0]['args']))
                    event_received = True
                    notification.notify(
                        title='Notification',
                        message=str(event[0]['args']['_notif']),
                        app_name='Text Challenge',
                        app_icon='path/to/the/icon.png'
                    )
            except TransactionNotFound as t:
                print("Not mined yet!")
                time.sleep(5)
    # async def handle_it3(self, tx_hash):
    #     try:
    #         notification.notify(
    #             title='Notification',
    #             message="Waiting for the transaction to be mined. Please read cmd to obtain more info",
    #             app_name='Text Challenge',
    #             app_icon='path/to/the/icon.png'
    #         )
    #         print("Waiting for the transaction to be mined ["+str(i*5)+"s]")
    #         tx_receipt = self.w3.eth.get_transaction_receipt(tx_hash)
    #         rich_logs = await self.contract.events.Notification().processReceipt(tx_receipt)
    #         if (rich_logs):
    #             print("EVENT RECEIVED (contest): "+str(rich_logs[0]['args']))
    #             event_received = True
    #             notification.notify(
    #                 title='Notification',
    #                 message=str(result[0]['args']['_notif']),
    #                 app_name='Text Challenge',
    #                 app_icon='path/to/the/icon.png'
    #             )
    #     except Exception as e:
    #         print("ERROR:\n\t"+str(e))

    async def handle_it2(self, tx_hash, poll_interval):
        event_received = False
        i = 0
        while event_received == False:
            try:
                notification.notify(
                    title='Notification',
                    message="Waiting for the transaction to be mined. Please read cmd to obtain more info",
                    app_name='Text Challenge',
                    app_icon='path/to/the/icon.png'
                )
                print("Waiting for the transaction to be mined ["+str(i*5)+"s]")
                await asyncio.sleep(poll_interval)
                i += 1
                tx_receipt = self.w3.eth.get_transaction_receipt(tx_hash)
                rich_logs = self.contract.events.Notification().processReceipt(tx_receipt)
                if (rich_logs):
                    print("EVENT RECEIVED (contest): "+str(rich_logs[0]['args']))
                    event_received = True
                    notification.notify(
                        title='Notification',
                        message=str(result[0]['args']['_notif']),
                        app_name='Text Challenge',
                        app_icon='path/to/the/icon.png'
                    )
            except TypeError as e:
                print("Not mined yet!")
            except Exception as e:
                print("Not mined yet!:\n\t"+str(e))

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
