from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
import json
# import random
# import binascii
from ContractInteraction import TextImageContract, Notifications
from TextImageContract import TextImage
from Notifications import ErrorNotification

#= = = = = = GLOBAL VARIABLES = = = = = =
POLL_INTERVAL = 2
CONTRACT_ADDR = '0x56bD5eB1d8768124172D07b7fa361470870cBc91'
ABI_JSON = '../build/contracts/DogsOrCats.json'
NODE_HTTP = 'http://127.0.0.1:7545'
GAS = 300000000
GAS_PRICE = 21000


class DogsOrCats(TextImage):
    def __init__(self, private_key):
        # = = = = = = = CONNECTION TO CONTRACT = = = = = = = = =
        with open(ABI_JSON) as json_file:
            info_json = json.load(json_file)
        abi = info_json["abi"]
        self.w3 = Web3(Web3.HTTPProvider(NODE_HTTP))
        self.contract = self.w3.eth.contract(address=CONTRACT_ADDR, abi=abi)
        self.myAccount = self.w3.eth.account.from_key(private_key).address
        self.errorNotif = ErrorNotification()
        print("myAccount:\n\t" + str(self.myAccount) +"\n\t"+ str(type(self.myAccount)))
        self.private_key = 0x0
