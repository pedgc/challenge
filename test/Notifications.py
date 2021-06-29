from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from plyer.utils import platform
from plyer import notification
from threading import Thread
import time

POLL_INTERVAL = 1


class Notifications():
    def __init__(self, obj):
        self.w3 = obj.w3
        self.NOTIF_EVENT = obj.contract.events.Notification()   # Needs to be instanciated due to Web3py limitations
        self.event_filter = self.NOTIF_EVENT.createFilter(fromBlock='latest')
        self.launchThread()

    def handle_event(self, event):
        receipt = self.w3.eth.wait_for_transaction_receipt(event['transactionHash'])
        result = self.NOTIF_EVENT.processReceipt(receipt, errors=STRICT)
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
