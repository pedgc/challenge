from web3 import Web3
from colorama import Fore, Back, init #,Style
import json
import random

#- - - - - - Pretty Print variables - - - - - -
init(autoreset=True)
TITLE = Back.BLACK + Fore.RED
BLUE = Fore.BLUE
print(Back.GREEN +"\n")

# = = = = = = CONNECTION TO CONTRACT = = = = = = =
#- - - - - Variables - - - - -
contractAddress = '0x36d80725537Cc013323b2ED170D7a989e9Ba7191'
with open('../build/contracts/Challenge.json') as json_file:
    info_json = json.load(json_file)
abi = info_json["abi"]

#- - - - - Connection to Blockchain & Contract - - - - -
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
contract = w3.eth.contract(address=contractAddress, abi=abi)

#- - - - - - Printing - - - - - -
print(TITLE + "\n\t\tINITIAL TESTS")
print("Connected to Contract: "+ BLUE +str(w3.isConnected()))
#print("Info of the ABI:\n"+ BLUE +str(abi))

# = = = = = = = = = = = TRANSACTIONS = = = = = = = = = =
#- - - - - Variables - - - - -
accounts = w3.eth.accounts
deposit_trans = {
    'gas': 420000,
    'gasPrice': 21000,
    'from': accounts[4],
    'value': w3.toWei(2, 'ether')
    }
depositAdmin_trans = {
    'gas': 420000,
    'gasPrice': 21000,
    'from': accounts[0],
    'value': w3.toWei(3, 'ether')
    }

withdraw_trans = {
    'gas': 420000,
    'gasPrice': 21000,
    'from': accounts[4],
    }
withdrawAdmin_trans = {
    'gas': 420000,
    'gasPrice': 21000,
    'from': accounts[0],
    }

#- - - - - Deposits - - - - -
tx_hash_deposit = contract.functions.deposit().transact(deposit_trans)
tx_info_deposit = w3.eth.getTransaction(tx_hash_deposit)
tx_hash_depositAdmin = contract.functions.depositAdmin().transact(depositAdmin_trans)
tx_info_depositAdmin = w3.eth.getTransaction(tx_hash_depositAdmin)

#- - - - - Withdraw() - - - - -
tx_hash_withdraw = contract.functions.withdraw(w3.toWei(1, 'ether')).transact(withdraw_trans)
tx_info_withdraw = w3.eth.getTransaction(tx_hash_withdraw)
tx_hash_withdrawAdmin = contract.functions.withdrawAdmin(w3.toWei(1, 'ether')).transact(withdrawAdmin_trans)
tx_info_withdrawAdmin = w3.eth.getTransaction(tx_hash_withdrawAdmin)

#- - - - - getUser() - - - - -
user = contract.functions.getUser(accounts[4]).call()

#- - - - - getBalanceContract() - - - - -
contractBalance = contract.functions.getBalanceContract().call()

#- - - - - - Printing - - - - - -
print(TITLE + "\n\t\tTRANSACTIONS")
print("Info of the user deposit:\n"+ BLUE +str(tx_info_deposit))
print("Info of the user withdraw:\n"+ BLUE +str(tx_info_withdraw))
print("Info of the User: "+ BLUE +str(user))
print("Info of the Admin deposit:\n"+ BLUE +str(tx_info_depositAdmin))
print("Info of the Admin withdraw:\n"+ BLUE +str(tx_info_withdrawAdmin))
print("Contract Balance: "+ BLUE +str(contractBalance))

# = = = = = = = = = = = GAME = = = = = = = = = =
#- - - - Variables - - - - -
player1 = accounts[2]
player2 = accounts[3]
admin = accounts[0]
bet = w3.toWei(1, 'ether')
adminVoidTx = {
    'gas': 420000,
    'gasPrice': 21000,
    'from': admin,
    'value': 0
}

#- - - - Player 1 Deposit - - - -
pl1_deposit_trans = {
    'gas': 420000,
    'gasPrice': 21000,
    'from': player1,
    'value': bet
    }
contract.functions.deposit().transact(pl1_deposit_trans)

#- - - - Player 2 Deposit - - - -
pl2_deposit_trans = {
    'gas': 420000,
    'gasPrice': 21000,
    'from': player2,
    'value': bet
    }
contract.functions.deposit().transact(pl2_deposit_trans)

#- - - - Resul & game() - - - -
resul = random.randint(1, 20)
winner = contract.functions.game(player1, player2, bet, resul).transact(adminVoidTx)
pl1_balance = contract.functions.getBalance(player1).call()
pl2_balance = contract.functions.getBalance(player2).call()
contractBalance = contract.functions.getBalanceContract().call()

#- - - - - - Printing - - - - - -
print(TITLE + "\n\t\tGAME")
print("Game Input:\n\t"+ BLUE +"Bet: "+str(bet)+"\n\tResul: "+str(resul))
print("Game Output:\n\t"+ BLUE +"Winner: "+str(winner.hex())+"\n\tPlayer 1 Balance: "+str(pl1_balance)+"\n\tPlayer 2 Balance: "+str(pl2_balance))
print("Contract Balance: "+ BLUE +str(contractBalance))
