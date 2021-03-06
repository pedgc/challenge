from web3 import Web3
from web3.exceptions import ContractLogicError
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from ContractInteraction import Notifications
from Notifications import ErrorNotification, Notification
from colorama import Fore
import time
import json
import os
from ast import literal_eval

#- - - - Pretty Print variables - - - -
BLUE = Fore.BLUE

#= = = = = = GLOBAL VARIABLES = = = = = =
POLL_INTERVAL = 2
CONTRACT_ADDR = '0x9f5fBF4f53AD9c0bf46C56415E1FA9895b4BDf5C'
ABI_JSON = '../build/contracts/TextImage.json'
# NODE_HTTP = 'http://127.0.0.1:7545' #Ganache
NODE_HTTP = 'https://ropsten.infura.io/v3/2f93f099906e46a58e16e7d93fa4d2de' #Ropsten HTTP
NODE_WSS = 'wss://ropsten.infura.io/ws/v3/2f93f099906e46a58e16e7d93fa4d2de' #Ropsten websocket
GAS = 2000000    #Wei
# GAS_PRICE = 100 #GWei


class TextImage():
    def __init__(self, private_key):
        # = = = = = = = CONNECTION TO CONTRACT = = = = = = = = =
        with open(ABI_JSON) as json_file:
            info_json = json.load(json_file)
        self.abi = info_json["abi"]
        # self.w3 = Web3(Web3.HTTPProvider(NODE_HTTP))
        self.w3 = Web3(Web3.WebsocketProvider(NODE_WSS))
        self.contract = self.w3.eth.contract(address=CONTRACT_ADDR, abi=self.abi)
        self.private_key = private_key
        self.myAccount = self.w3.eth.account.from_key(private_key).address
        # self.node_http = NODE_HTTP
        self.contract_addr = CONTRACT_ADDR
        self.errorNotif = ErrorNotification()
        self.Notif = Notification(self)
        self.GAS_PRICE = self.w3.eth.gas_price
        print(BLUE + "Using:\n\t- Web3 Version: "+str(self.w3.api) + "\n\t- Client Version: "+str(self.w3.clientVersion))
        print(BLUE + "My Address: https://ropsten.etherscan.io/address/"+str(self.myAccount))

    # - - - - - - Getters & Setters - - - - - - - -
    def getSolution(self):
        try:
            return self.contract.functions.getSolution().call({'from': self.myAccount})
        except ContractLogicError as e:
            msg = str(e) + " [getSolution]"
            self.errorNotif.showErrorNotif(msg, "getSolution")
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "getSolution")

    def getWinners(self):
        try:
            return self.contract.functions.getWinners().call()
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "getWinners")

    def setAdmin(self, newAdminAddr):
        try:
            tx = self.contract.functions.setAdmin(newAdminAddr).buildTransaction(self.createTx(0))
            self.signTxAndWaitNotif(tx)
        except ValueError as v:
            dict = literal_eval(str(v))
            self.errorNotif.showErrorNotif(str(dict['message']), "setAdmin")
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "setAdmin")

    # Users
    def getStatus(self):
        try:
            return self.contract.functions.getStatus().call()
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "getStatus")

    def getAdmin(self):
        try:
            return self.contract.functions.getAdmin().call()
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "getAdmin")

    def getPrize(self):
        try:
            prize = self.contract.functions.getPrize().call()
            prize = self.w3.fromWei(prize, 'ether')
            return prize
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "getPrize")

    def getName(self):
        try:
            return self.contract.functions.getName().call()
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "getName")

    def getContesters(self):
        try:
            return self.contract.functions.getContesters().call()
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "getContesters")

    def getPrizeHasBeenSent(self):
        try:
            return self.contract.functions.getPrizeHasBeenSent().call()
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "getPrizeHasBeenSent")

    # - - - - - - - - Methods - - - - - - - -
    def createTx(self, _value):
        GAS_PRICE = self.w3.eth.gas_price
        print(BLUE + "Current Gas Price: "+str(self.w3.fromWei(GAS_PRICE, 'GWei')) + " GWei")
        GAS_PRICE = round(GAS_PRICE*1.15)
        print(BLUE + "Using Gas Price: "+str(self.w3.fromWei(GAS_PRICE, 'GWei')) + " GWei")

        tx = {
            'gas': self.w3.toWei(GAS, 'Wei'),
            'gasPrice': GAS_PRICE,
            'nonce': self.w3.eth.getTransactionCount(self.myAccount),
            'from': str(self.myAccount),
            'value': self.w3.toWei(_value, 'ether')
        }
        return tx

    def createContest(self, prize, solution):
        try:
            tx = self.contract.functions.createContest(solution).buildTransaction(self.createTx(prize))
            self.signTxAndWaitNotif(tx)
        except ValueError as v:
            dict = literal_eval(str(v))
            self.errorNotif.showErrorNotif(str(dict['message']), "createContest")
        except ContractLogicError as v:
            print("\tERROR - TextImageContract/createContest: \n"+str(v))
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "createContest")

    def resetContest(self):
        try:
            tx = self.contract.functions.resetContest().buildTransaction(self.createTx(0))
            self.signTxAndWaitNotif(tx)
        except ValueError as v:
            dict = literal_eval(str(v))
            self.errorNotif.showErrorNotif(str(dict['message']), "resetContest")
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "resetContest")

    def calculateWinners(self):
        try:
            tx = self.contract.functions.calculateWinners().buildTransaction(self.createTx(0))
            self.signTxAndWaitNotif(tx)
        except ValueError as v:
            dict = literal_eval(str(v))
            self.errorNotif.showErrorNotif(str(dict['message']), "calculateWinners")
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "calculateWinners")

    def sendPrizeToWinners(self):
        try:
            tx = self.contract.functions.sendPrizeToWinners().buildTransaction(self.createTx(0))
            self.signTxAndWaitNotif(tx)
        except ValueError as v:
            dict = literal_eval(str(v))
            self.errorNotif.showErrorNotif(str(dict['message']), "sendPrizeToWinners")
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "sendPrizeToWinners")

    def contest(self, solution):
        try:
            tx = self.contract.functions.contest(solution).buildTransaction(self.createTx(0))
            self.signTxAndWaitNotif(tx)
        except ValueError as v:
            dict = literal_eval(str(v))
            self.errorNotif.showErrorNotif(str(dict['message']), "contest")
            self.errorNotif.showUnexpErrorNotif(v, "contest")
        except ContractLogicError as v:
            print("\tERROR - TextImageContract/contest: \n"+str(v))
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "contest")

    def signTxAndWaitNotif(self, tx):
        signed_tx = self.w3.eth.account.signTransaction(tx, private_key=self.private_key)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        self.Notif.event(tx_hash)
