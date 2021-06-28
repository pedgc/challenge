from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
import json
import random
import binascii
from plyer.utils import platform
from plyer import notification
from threading import Thread
import time

#= = = = = = GLOBAL VARIABLES = = = = = =
POLL_INTERVAL = 2
CONTRACT_ADDR = '0x9797Ab86AaEd7Fc185Bf69039a4C7d2110fEA74c'
ABI_JSON = '../build/contracts/LevDistance.json'
NODE_HTTP = 'http://127.0.0.1:7545'
GAS = 300000000
GAS_PRICE = 21000
POLL_INTERVAL = 1


class Notifications():
    def __init__(self):
        # = = = = = = = CONNECTION TO CONTRACT = = = = = = = = =
        with open(ABI_JSON) as json_file:
            info_json = json.load(json_file)
        abi = info_json["abi"]
        self.w3 = Web3(Web3.HTTPProvider(NODE_HTTP))
        self.contract = self.w3.eth.contract(address=CONTRACT_ADDR, abi=abi)
        # = = = = EVENTS = = = =
        self.NOTIF_EVENT = self.contract.events.Notification()   # Needs to be instanciated due to Web3py limitations

        #- - - - - Listen to Events in Thread - - - -
        self.block_filter = self.w3.eth.filter({'fromBlock':'latest', "address": CONTRACT_ADDR})
        self.event_filter = self.NOTIF_EVENT.createFilter(fromBlock='latest')

        self.launchThread()

    def handle_event(self, event):
        receipt = self.w3.eth.wait_for_transaction_receipt(event['transactionHash'])
        result = self.NOTIF_EVENT.processReceipt(receipt, errors=STRICT)
        notification.notify(title='Notification', message=str(result[0]['args']['_notif']), app_name='Text Challenge', app_icon='path/to/the/icon.png')
        print("Event: "+str(result[0]['args']))

    def log_loop(self, event_filter, poll_interval):
        while True:
            for event in event_filter.get_new_entries():
                self.handle_event(event)
            time.sleep(poll_interval)

    def launchThread(self):
        worker = Thread(target=self.log_loop, args=(self.event_filter, POLL_INTERVAL), daemon=True)
        worker.start()
