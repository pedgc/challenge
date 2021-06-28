from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
import json
import random
import binascii

#= = = = = = GLOBAL VARIABLES = = = = = =
POLL_INTERVAL = 2
CONTRACT_ADDR = '0x9797Ab86AaEd7Fc185Bf69039a4C7d2110fEA74c'
ABI_JSON = '../build/contracts/LevDistance.json'
NODE_HTTP = 'http://127.0.0.1:7545'
GAS = 300000000
GAS_PRICE = 21000


class LevDistContract():
    def __init__(self):
        # = = = = = = = CONNECTION TO CONTRACT = = = = = = = = =
        with open(ABI_JSON) as json_file:
            info_json = json.load(json_file)
        abi = info_json["abi"]
        self.w3 = Web3(Web3.HTTPProvider(NODE_HTTP))
        self.contract = self.w3.eth.contract(address=CONTRACT_ADDR, abi=abi)
        self.accounts = self.w3.eth.accounts
        self.adminAccount = self.accounts[0]

    # - - - - - - Getters & Setters - - - - - - - -
    def getInitStatus(self):
        return self.contract.functions.getStatus().call()
    def getAdmin(self):
        return self.contract.functions.getAdmin().call()
    def getSolution(self):
        return self.contract.functions.getSolution().call()
    def getPrize(self):
        return self.contract.functions.getPrize().call()
    def getWinners(self):
        return self.contract.functions.getWinners().call()
    def getName(self):
        return self.contract.functions.getName().call()

    def setInitStatus(self):
        self.contract.functions.setStatus(True).transact(self.createTx(self.adminAccount, 0))

    # - - - - - - - - Methods - - - - - - - -
    def createTx(self, _from, _value):
        tx = {
            'gas': GAS,
            'gasPrice': GAS_PRICE,
            'from': _from,
            'value': self.w3.toWei(_value, 'ether')
        }
        # print("createTx:")
        # print("\tfrom: "+str(_from))
        # print("\tvalue: "+str(_value)+" | "+str(self.w3.toWei(_value, 'ether')))

        return tx

    def createContest(self, prize, solution):
        # print("setContest:")
        # print("\tprize: "+str(prize))
        # print("\tsolution: "+str(solution))
        self.contract.functions.createContest(solution).transact(self.createTx(self.adminAccount, prize))


    def resetContest(self):
        self.contract.functions.resetContest().transact(self.createTx(self.adminAccount, 0))
