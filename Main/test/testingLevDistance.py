from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from colorama import Fore, Back, init #,Style
import json
import random
import binascii
from threading import Thread
import time

#= = = = = = GLOBAL VARIABLES = = = = = =
POLL_INTERVAL = 2
CONTRACT_ADDR = '0xe7d8f720689faa6F6a8c688810d5dc0397C999E5'
ABI_JSON = '../build/contracts/LevDistance.json'
NODE_HTTP = 'http://127.0.0.1:7545'

#- - - - Pretty Print variables - - - -
TITLE = Back.BLACK + Fore.RED
BLUE = Fore.BLUE
EVENT = Fore.YELLOW

# = = = = = = = CONNECTION TO CONTRACT = = = = = = = = =
with open(ABI_JSON) as json_file:
    info_json = json.load(json_file)
abi = info_json["abi"]
w3 = Web3(Web3.HTTPProvider(NODE_HTTP))
contract = w3.eth.contract(address=CONTRACT_ADDR, abi=abi)
accounts = w3.eth.accounts

# = = = = EVENTS = = = =
NOTIF_EVENT = contract.events.Notification()   # Needs to be instanciated due to Web3py limitations

def handle_event(event):
    receipt = w3.eth.wait_for_transaction_receipt(event['transactionHash'])
    result = NOTIF_EVENT.processReceipt(receipt, errors=STRICT)
    print("Event: "+ EVENT +str(result[0]['args']['_notif']))

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)

def main():
    # - - - Pretty Print - - -
    init(autoreset=True)
    print(Back.GREEN +"\n")

    #- - - - - Listen to Events in Thread - - - -
    block_filter = w3.eth.filter({'fromBlock':'latest', "address": CONTRACT_ADDR})
    event_filter = NOTIF_EVENT.createFilter(fromBlock='latest')
    worker = Thread(target=log_loop, args=(event_filter, POLL_INTERVAL), daemon=True)
    worker.start()

    # #- - - - - - Printing Initial Test - - - - - -
    # print(TITLE + "\n\t\tINITIAL TESTS")
    # print("Connected to Contract: "+ BLUE +str(w3.isConnected()))
    # #print("Info of the ABI:\n"+ BLUE +str(abi))
    #
    # = = = = = = = = = = = SETTING CONTEST = = = = = = = = = =
    # Accounts & Transactions
    player1 = accounts[2]
    player2 = accounts[3]
    player3 = accounts[4]
    player4 = accounts[5]
    admin = accounts[0]

    adminPrizeTx = {
        'gas': 300000000,
        'gasPrice': 21000,
        'from': admin,
        'value': w3.toWei(3, 'ether')
    }
    adminVoidTx = {
        'gas': 300000000,
        'gasPrice': 21000,
        'from': admin,
        'value': 0
    }
    pl1_contest_trans = {
        'gas': 420000,
        'gasPrice': 21000,
        'from': player1,
        'value': 0
    }
    pl2_contest_trans = {
        'gas': 420000,
        'gasPrice': 21000,
        'from': player2,
        'value': 0
    }
    pl3_contest_trans = {
        'gas': 420000,
        'gasPrice': 21000,
        'from': player3,
        'value': 0
    }
    pl4_contest_trans = {
        'gas': 420000,
        'gasPrice': 21000,
        'from': player4,
        'value': 0
    }

    # Contest Solutions & Resul
    solution = "Skullcandy"
    pl1_resul = "Skullcandy"
    pl2_resul = "Skulcandy"
    pl3_resul = "Skullcandy"
    pl4_resul = "Skullcandii"

    # Initial Contest Status
    initStatus = contract.functions.getStatus().call()

    # Setting Solution, Prize & Status
    contract.functions.createContest(solution).transact(adminPrizeTx)
    solutionFromContract = contract.functions.getSolution().call()
    prize = contract.functions.getPrize().call()

    # Final Contest Status
    finalStatus = contract.functions.getStatus().call()
    print("Contest has been created")

    # Contesters
    contract.functions.contest(pl1_resul).transact(pl1_contest_trans)
    contract.functions.contest(pl2_resul).transact(pl2_contest_trans)
    contract.functions.contest(pl3_resul).transact(pl3_contest_trans)
    contract.functions.contest(pl4_resul).transact(pl4_contest_trans)
    print("Participants have send their results")

    # Winners
    contract.functions.calculateWinners().transact(adminVoidTx)
    winner = contract.functions.getWinners().call()
    print("Winners have been calculated")

    # Sending Prize to winners
    contract.functions.sendPrizeToWinners().transact(adminVoidTx)
    print("Prize has been sent")

    # Deletting contest
    contract.functions.resetContest().transact(adminVoidTx)
    print("Contest has been reset")

    # = = = = = = = = = PRINTING = = = = = = = = =
    print(TITLE + "\n\t\tCONTEST")
    print("Initial Status: "+ BLUE +str(initStatus))
    print("Final Status: "+ BLUE +str(finalStatus))
    print("- - - - - - - - - - - - - -")
    print("Solution:"+ BLUE +" "+str(solution))
    print("Solution from Contract:"+ BLUE +" "+str(solutionFromContract))
    print("Prize: "+ BLUE +" "+str(prize))
    print("- - - - - - - - - - - - - -")
    print("Player 1: "+ BLUE +str(player1))
    print("Player 2: "+ BLUE +str(player2))
    print("Player 3: "+ BLUE +str(player3))
    print("Player 4: "+ BLUE +str(player4))
    print("- - - - - - - - - - - - - -")
    print("Winners: "+ BLUE +str(winner))

if __name__ == '__main__':
    main()
