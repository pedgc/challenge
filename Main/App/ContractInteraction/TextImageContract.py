from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
import json
from ast import literal_eval
from ContractInteraction import Notifications
from Notifications import ErrorNotification
# import random
# import binascii

#= = = = = = GLOBAL VARIABLES = = = = = =
POLL_INTERVAL = 2
CONTRACT_ADDR = '0xeA7180f452026DCCE377153c1ceC52a73510df7B'
ABI_JSON = '../build/contracts/TextImage.json'
NODE_HTTP = 'http://127.0.0.1:7545'
GAS = 300000000
GAS_PRICE = 21000


class TextImage():
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

    # - - - - - - Getters & Setters - - - - - - - -
    def getSolution(self):
        try:
            return self.contract.functions.getSolution().call()
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "getSolution")

    def getWinners(self):
        try:
            return self.contract.functions.getWinners().call()
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "getWinners")

    def setAdmin(self, newAdminAddr):
        try:
            print("SetAdmin\n\tNew Address: " + newAdminAddr)
            self.contract.functions.setAdmin(newAdminAddr).transact(self.createTx(self.myAccount, 0))
        except ValueError as v:
            dict = literal_eval(str(v))
            self.errorNotif.showErrorNotif(str(dict['message']))
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "setAdmin")

    def setName(self, newName):
        try:
            self.contract.functions.setName(newName).transact(self.createTx(self.myAccount, 0))
        except ValueError as v:
            dict = literal_eval(str(v))
            self.errorNotif.showErrorNotif(str(dict['message']))
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "setName")

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
            return self.contract.functions.getPrize().call()
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
    def createTx(self, _from, _value):
        tx = {
            'gas': GAS,
            'gasPrice': GAS_PRICE,
            'from': _from,
            'value': self.w3.toWei(_value, 'ether')
        }
        return tx

    def createContest(self, prize, solution):
        try:
            self.contract.functions.createContest(solution).transact(self.createTx(self.myAccount, prize))
        except ValueError as v:
            dict = literal_eval(str(v))
            self.errorNotif.showErrorNotif(str(dict['message']))
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "createContest")

    def resetContest(self):
        try:
            self.contract.functions.resetContest().transact(self.createTx(self.myAccount, 0))
        except ValueError as v:
            dict = literal_eval(str(v))
            self.errorNotif.showErrorNotif(str(dict['message']))
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "resetContest")

    def calculateWinners(self):
        try:
            self.contract.functions.calculateWinners().transact(self.createTx(self.myAccount, 0))
        except ValueError as v:
            dict = literal_eval(str(v))
            self.errorNotif.showErrorNotif(str(dict['message']))
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "calculateWinners")

    def sendPrizeToWinners(self):
        try:
            self.contract.functions.sendPrizeToWinners().transact(self.createTx(self.myAccount, 0))
        except ValueError as v:
            dict = literal_eval(str(v))
            self.errorNotif.showErrorNotif(str(dict['message']))
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "sendPrizeToWinners")

    def contest(self, solution):
        try:
            self.contract.functions.contest(solution).transact(self.createTx(self.myAccount, 0))
        except ValueError as v:
            dict = literal_eval(str(v))
            self.errorNotif.showErrorNotif(str(dict['message']))
        except Exception as e:
            self.errorNotif.showUnexpErrorNotif(e, "contest")
