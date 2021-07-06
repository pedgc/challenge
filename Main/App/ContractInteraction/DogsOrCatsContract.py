from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
import json
# import random
# import binascii
from ContractInteraction import TextImageContract, Notifications
from TextImageContract import TextImage
from Notifications import ErrorNotification, Notification

#= = = = = = GLOBAL VARIABLES = = = = = =
POLL_INTERVAL = 2
CONTRACT_ADDR = '0xbe503cF43697bD62d2Ef35cf7876A6aE5f652903'
ABI_JSON = '../build/contracts/DogsOrCats.json'
# NODE_HTTP = 'http://127.0.0.1:7545' #Ganache
NODE_HTTP = 'https://ropsten.infura.io/v3/2f93f099906e46a58e16e7d93fa4d2de' #Ropsten HTTP
NODE_WSS = 'wss://ropsten.infura.io/ws/v3/2f93f099906e46a58e16e7d93fa4d2de' #Ropsten websocket
GAS = 210000   #Wei
GAS_PRICE = 4  #GWei


class DogsOrCats(TextImage):
    def __init__(self, private_key):
        # = = = = = = = CONNECTION TO CONTRACT = = = = = = = = =
        with open(ABI_JSON) as json_file:
            info_json = json.load(json_file)
        self.abi = info_json["abi"]
        # self.w3 = Web3(Web3.HTTPProvider(NODE_HTTP))
        self.w3 = Web3(Web3.WebsocketProvider(NODE_WSS))
        # self.contract = self.w3.eth.contract(address=CONTRACT_ADDR, abi=abi)
        # self.myAccount = self.w3.eth.account.from_key(private_key).address
        # self.errorNotif = ErrorNotification()
        # self.private_key = 0x0
        self.contract = self.w3.eth.contract(address=CONTRACT_ADDR, abi=self.abi)
        self.private_key = private_key
        self.myAccount = self.w3.eth.account.from_key(private_key).address
        self.node_http = NODE_HTTP
        self.contract_addr = CONTRACT_ADDR
        self.errorNotif = ErrorNotification()
        self.Notif = Notification(self) # -> Falta el parametro
        print("My Address: "+str(self.myAccount))
