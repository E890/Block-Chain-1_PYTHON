#import libraries
import hashlib
import random
import string
import json
import binascii
import numpy as np 
import pandas as pd 
import pylab as pl 
import logging
import datetime
import collections

#required for PKI
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

#CLIENT CLASS
'''
  The Client class generates the private and public 
  keys by using the built-in Python RSA algorithm. 
  The interested reader may refer to this tutorial for 
  the implementation of RSA. During the object initialization, 
  we create private and public keys and store their values in the instance variable.
'''

'''
  Note that you should never lose your private key. 
  For record keeping, the generated private key may 
  be copied on a secured external storage or you may 
  simply write down the ASCII representation of it on 
  a piece of paper.
'''

#The generated public key will be used as the client’s 
# identity. For this, we define a property called identity 
# that returns the HEX representation of the public key.

'''
    The identity is unique to each client and can be
    made publicly available. Anybody would be able to 
    send virtual currency to you using this identity 
    and it will get added to your wallet.
'''

class Client:
    
    def __init__(self):
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)
        
    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
    
  

class Transaction:

    def __init__(self,sender,recipient,value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()

    def to_dict(self):
        if self.sender == 'Genesis':
            identity = 'Genensis'
        else:
            identity = self.sender.identity

        return collections.OrderedDict({
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time':self.time
        })

    #sign the dict using private key of sender
    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h =  SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')


#testing the client   
Eliud = Client()
Luda = Client()

#create transaction.
t = Transaction(
    Eliud,
    Luda.identity,
    5.0
)

#print('\t\t Eliud Private key >> \n',Eliud.identity)
#print('\t\t Luda Private Key >> \n',Luda.identity)

Signature = t.sign_transaction()
#print('\t Signature >> \n',Signature)

'''
    In this chapter, let us create a Transaction class 
    so that a client will be able to send money to somebody. 
    Note that a client can be both a sender or a recipient 
    of the money. When you want to receive money, some other 
    sender will create a transaction and specify your public 
    address in it. We define the initialization of a transaction class as follows:
'''
#Adding transactions

#dispaly transactions
def dispaly_transactions(Transaction):
    #for every transaction in transaction 
    dict = Transaction.to_dict()
    print("sender: " + dict['sender'])
    print("------")
    print("recipient: " + dict['recipient'])
    print("------")
    print("value: " + str(dict['value']))
    print("------")
    print("time: " + str(dict['time']))
    print("------")


#create a global transaction queu forn storing transaction objects
transactions_queu = []

#create multiple clients.
jane = Client()
roon = Client()
paul = Client()
rivaer = Client()

#intiate 1st transaction
t1 = Transaction(
    jane,
    roon.identity,
    12.3
)

'''
    We will sign this transaction using Dinesh’s 
    private key and add it to the transaction queue 
    as follows: 
'''

t1.sign_transaction()
transactions_queu.append(t1)

# more transactions.
t2 = Transaction(
    roon,
    paul.identity,
    2.3
)

t2.sign_transaction()
transactions_queu.append(t2)

t3 =Transaction(
    paul,
    rivaer.identity,
    5.3
)

t3.sign_transaction()
transactions_queu.append(t3)

t4 = Transaction(
    paul,
    roon.identity,
    3.4
)

t4.sign_transaction()
transactions_queu.append(t4)


t5 = Transaction(
    rivaer,
    jane.identity,
    4.6
)

t5.sign_transaction()
transactions_queu.append(t5)

# print('pauls identity : >> ', paul.identity)
# print('roons identity : >> ', roon.identity)
# print('jane identity : >> ', jane.identity)

#DUMPING TRANSACTIONS
for trans in transactions_queu:
    dispaly_transactions(trans)
    print('----------------///----------------')

#blocks 

class Block:

    def __init__(self):
        self.verified_transactions = []
        self.previous_block_hash = ""
        self.Nonce = ""

last_block_hash = ""

#create genesis  block
Munyala = Client()

t0 = Transaction(
    'Genesis',
    Munyala.identity,
    500.0
)

block0 = Block()
block0.previous_block_hash =None
Nonce = None
block0.verified_transactions.append(t0)

digest = hash(block0)
last_block_hash = digest

TPCoins = []

def dump_blockain (self):
    print("Number of blocks in the chain: " + str(len(self)))


    for x in range(len(TPCoins)):
        block_temp = TPCoins[x]
        print("Block # " + str(x))
        
    for transactions_queu in block_temp.verified_transactions:
        dispaly_transactions(transactions_queu)
        print('-----------')
    print('===============================')


TPCoins.append(block0)
dump_blockain(TPCoins)

#creating miners
def sha256(message):
    return hashlib.sha256(message.encode("ascii")).hexdigest()

#mine function
def mine(message, defficulty = 1):
    assert defficulty >= 1
    prefix = '1' * defficulty

    for i in range(1000):
        digest = sha256(str(hash(message)) + str(i))
        if digest.startswith(prefix):
            print('after ' + str(i) + " iterations found nonce: " + digest)

    return digest

mine("test message", 2)
