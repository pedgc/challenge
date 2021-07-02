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
CONTRACT_ADDR = '0x28E6D305cf6392Ae898F56383290367662E2E732'
ABI_JSON = '../build/contracts/DogsOrCats.json'
NODE_HTTP = 'http://127.0.0.1:7545'
GAS = 300000000
GAS_PRICE = 21000


class DogsOrCats(TextImage):
    def __init__(self):
        # = = = = = = = CONNECTION TO CONTRACT = = = = = = = = =
        with open(ABI_JSON) as json_file:
            info_json = json.load(json_file)
        abi = info_json["abi"]
        self.w3 = Web3(Web3.HTTPProvider(NODE_HTTP))
        self.contract = self.w3.eth.contract(address=CONTRACT_ADDR, abi=abi)
        self.accounts = self.w3.eth.accounts
        self.myAccount = self.accounts[0]
        self.errorNotif = ErrorNotification()

    # # - - - - - - Getters & Setters - - - - - - -
    #
    # def getSolution(self):
    #     return self.contract.functions.getSolution().call()
    # def getWinners(self):
    #     return self.contract.functions.getWinners().call()
    #
    # # Users
    # def getStatus(self):
    #     return self.contract.functions.getStatus().call()
    # def getAdmin(self):
    #     return self.contract.functions.getAdmin().call()
    # def getPrize(self):
    #     return self.contract.functions.getPrize().call()
    # def getName(self):
    #     return self.contract.functions.getName().call()
    # def getContesters(self):
    #     return self.contract.functions.getContesters().call()
    # def getPrizeHasBeenSent(self):
    #     return self.contract.functions.getPrizeHasBeenSent().call()
    #
    # # - - - - - - - - Methods - - - - - - - -
    # def createTx(self, _from, _value):
    #     tx = {
    #         'gas': GAS,
    #         'gasPrice': GAS_PRICE,
    #         'from': _from,
    #         'value': self.w3.toWei(_value, 'ether')
    #     }
    #     return tx
    #
    # def createContest(self, prize, solution):
    #     self.contract.functions.createContest(solution).transact(self.createTx(self.myAccount, prize))
    #
    # def resetContest(self):
    #     self.contract.functions.resetContest().transact(self.createTx(self.myAccount, 0))
    #
    # def setAdmin(self, newAdminAddr):
    #     self.contract.functions.setAdmin(newAdminAddr).transact(self.createTx(self.myAccount, 0))
    #
    # def setName(self, newName):
    #     self.contract.functions.setName(newName).transact(self.createTx(self.myAccount, 0))
    #
    # def contest(self, solution):
    #     self.contract.functions.contest(solution).transact(self.createTx(self.myAccount, 0))
