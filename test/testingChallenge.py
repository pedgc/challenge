from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from colorama import Fore, Back, init #,Style
import json
import random
from threading import Thread
import time

#= = = = = = GLOBAL VARIABLES = = = = = =
POLL_INTERVAL = 2
CONTRACT_ADDR = '0x9EB38d11Cdf7ddddba6F225CA685B95614AdC106'
ABI_JSON = '../build/contracts/Challenge.json'
NODE_HTTP = 'http://127.0.0.1:7545'

#- - - - Pretty Print variables - - - -
TITLE = Back.BLACK + Fore.RED
BLUE = Fore.BLUE
EVENT = Fore.YELLOW

#- - - - - Connection to Blockchain & Contract - - - - -
with open(ABI_JSON) as json_file:
    info_json = json.load(json_file)
abi = info_json["abi"]
w3 = Web3(Web3.HTTPProvider(NODE_HTTP))
contract = w3.eth.contract(address=CONTRACT_ADDR, abi=abi)

# = = = = EVENTS = = = =
WINNER_EVENT = contract.events.Winner()   # Needs to be instanciated due to Web3py limitations
WINNER1_EVENT = contract.events.Winner1() # Needs to be instanciated due to Web3py limitations
WINNER2_EVENT = contract.events.Winner2() # Needs to be instanciated due to Web3py limitations

def handle_event(event):
    receipt = w3.eth.wait_for_transaction_receipt(event['transactionHash'])
    result = WINNER_EVENT.processReceipt(receipt, errors=STRICT)
    print("Event: "+ EVENT +str(result[0]['args']))

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)

def main():
    # - - - Pretty Print - - -
    init(autoreset=True)
    print(Back.GREEN +"\n")

    # = = = = = = CONTRACT & EVENTS = = = = = = = =

    #- - - - - Listen to Events in Thread - - - -
    block_filter = w3.eth.filter({'fromBlock':'latest', "address": CONTRACT_ADDR})
    event_filter = WINNER_EVENT.createFilter(fromBlock='latest')
    # worker = Thread(target=log_loop, args=(block_filter, POLL_INTERVAL), daemon=True)
    worker = Thread(target=log_loop, args=(event_filter, POLL_INTERVAL), daemon=True)
    worker.start()

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
    time.sleep(POLL_INTERVAL + 1)


    # = = = = = = = = = = = LEV DISTANCE = = = = = = = = = =
    # str1 = "asd"
    # str2 = "asd"
    # str3 = "222"
    # str4 = "asdd"
    # str5 = "123"
    # str6 = "223"

    #- - - - Player Transactions - - - - -
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
    resul = "Skullcandy";
    player1_resul = "Skulcandy";
    player2_resul = "Skulcandi";
    winner = contract.functions.gameLev(player1, player2, bet, player1_resul, player2_resul, resul).transact(adminVoidTx)
    pl1_balance = contract.functions.getBalance(player1).call()
    pl2_balance = contract.functions.getBalance(player2).call()
    contractBalance = contract.functions.getBalanceContract().call()

    #- - - - - - Printing - - - - - -
    print(TITLE + "\n\t\tLEV DISTANCE")
    # print("asd & asd: "+ BLUE +str(contract.functions.levDistance(str1, str2).call()))
    # print("asd & asdd: "+ BLUE +str(contract.functions.levDistance(str1, str4).call()))
    # print("asd & 222: "+ BLUE +str(contract.functions.levDistance(str1, str3).call()))
    # print("123 & 222: "+ BLUE +str(contract.functions.levDistance(str5, str3).call()))
    # print("223 & 222: "+ BLUE +str(contract.functions.levDistance(str6, str3).call()))
    print("Game Input:\n\t"+ BLUE +"Bet: "+str(bet)+"\n\tResul: "+str(resul))
    print("Game Output:\n\t"+ BLUE +"Winner: "+str(winner.hex())+"\n\tPlayer 1 Balance: "+str(pl1_balance)+"\n\tPlayer 2 Balance: "+str(pl2_balance))
    print("Contract Balance: "+ BLUE +str(contractBalance))
    time.sleep(POLL_INTERVAL + 1)


if __name__ == '__main__':
    main()
