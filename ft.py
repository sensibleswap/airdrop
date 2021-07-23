# pip3 install requests
# usage:
# python3 sync_tx.py

import time
import os
import requests
import json


# 9757197ec84183cd39e2239e56c8cc04fce9f9cd mc
# d486f42fd4930c964f6840a2997b0ef9b3abc38d tmc4
# f40f1b388e3265e0c9948f558615123f6996dbfa bsv/mc

# 15dd17380b87af419c3249e6631cd979ab4054a1 boex


# mc owners
# https://api.sensiblequery.com/ft/owners/514776383faa66e4a65808904d4d6724e4774fbe/9757197ec84183cd39e2239e56c8cc04fce9f9cd

# mc utxo by address
# https://api.sensiblequery.com/ft/utxo/514776383faa66e4a65808904d4d6724e4774fbe/9757197ec84183cd39e2239e56c8cc04fce9f9cd/16CWPf4v9dBoPvfyibruJf784DNFiKqYkM

# mc swap pool address: 16CWPf4v9dBoPvfyibruJf784DNFiKqYkM

NULL_ADDRESS = '1111111111111111111114oLvT2'

# token hash
# 6.0
#codehash = "514776383faa66e4a65808904d4d6724e4774fbe"
codehash = '777e4dd291059c9f7a0fd563f7204576dcceb791'
# bsv/mc
genesis_data = {
    'bsv-mc': "f40f1b388e3265e0c9948f558615123f6996dbfa",
    'boex': '15dd17380b87af419c3249e6631cd979ab4054a1',
    'mc': '54256eb1b9c815a37c4af1b82791ec6bdf5b3fa3', #7.1.0
} 
# bsv/boex
#genesis = "a448a5703c9381e427d7e41e17dde098d3f9be70"

def getBalance(address):

    size = 10
    while True:
        r = requests.get("https://api.sensible.satoplay.cn/ft/utxo/%s/%s/%s?cursor=0&size=%d" % (codehash, genesis, address, size))
        resp = r.json()
        if resp["code"] != 0:
            print (resp["msg"])
            os.exit(1)
        if len(resp["data"]) == size:
            size *= 2
            continue

        print ("get utxo for:", address, "size:", len(resp["data"]))

        balance = 0
        for utxo in resp["data"]:
            balance += int(utxo["tokenAmount"])

        return balance

def get_token(symbol, detail=False):
    genesis = genesis_data[symbol]
    r = requests.get("https://api.sensible.satoplay.cn/ft/owners/%s/%s?cursor=0&size=5000" % (codehash, genesis))
    resp = r.json()

    if resp["code"] != 0:
        print (resp["msg"])
        os.exit(1)

    balance = 0
    pending_balance = 0
    userData = {}
    print ("address count:", len(resp["data"]))
    for data in resp["data"]:
        if detail:
            finalBalance = getBalance(data["address"])
        else:
            finalBalance = data["pendingBalance"] + data["balance"]
        print (data['address'], finalBalance)
        if data['address'] == '1111111111111111111114oLvT2':
            continue
        userData[data['address']] = finalBalance

        if finalBalance != (data["pendingBalance"] + data["balance"]):
            print (data["address"], "utxo balanc not match:", data, finalBalance)

            balance += finalBalance
        else:
            balance += data["balance"]
            pending_balance += data["pendingBalance"]

        # print (data)

    userData['sum'] = balance + pending_balance
    with open(symbol + '_balance.json', 'w') as f:
        json.dump(userData, f, indent=4)

    print("total supply:", balance, pending_balance, balance + pending_balance)

def count_token(sum_token):
    symbol = 'bsv-mc'
    with open(symbol + '_balance.json', 'r') as f:
        lp_balance = json.load(f)

    sum_lp = lp_balance['sum']
    token_balance = {}
    count_token = 0
    for addr, balance in lp_balance.items():
        if addr != 'sum':
            token_balance[addr] = balance * sum_token // sum_lp
            count_token += token_balance[addr]
            print (addr, token_balance[addr])

    print ('sum:', count_token, sum_token)
    with open('mc_count_balance.json', 'w') as f:
        json.dump(token_balance, f, indent=4)

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'gettoken':
        get_token(sys.argv[2])
    elif sys.argv[1] == 'counttoken':
        count_token(int(sys.argv[2]))
