import random
from random import randint
import os
import csv
import math
from datetime import datetime

infinity = 1000

class Block:
    def __init__(self, blockID, PoW, list_tx):
        self.blockID, self.PoW, self.list_tx = blockID, PoW, list_tx

    def __str__(self):
        plain_list_tx = []
        for tx in self.list_tx:
            strtx = getTxStr(tx)
            plain_list_tx.append(strtx)
        return f"block {self.blockID}, PoW {self.PoW}, Tx:{plain_list_tx}"


class Tx():
    def __init__(self,payeur,destinataire,amount,fee):
        self.payeur, self.destinataire, self.amount, self.fee = payeur,destinataire,amount,fee

    def __str__(self):
        return f"Tx: from {self.payeur}, to {self.destinataire}, amount {self.amount}, fee {self.fee}"

    def tx_str(self):
        strtx = ""
        strtx += str(self.payeur)
        strtx += str(self.destinataire)
        if self.amount < 10:
            strtx += "0" + str(self.amount)
        else:
            strtx += str(self.amount)
        strtx += str(self.fee)

        return strtx

def strToRealTx(tx):
    payeur = int(tx[0])
    destinataire = int(tx[1])
    montant = int(tx[2:4])
    frais = int(tx[4])
    realTx = Tx(payeur,destinataire,montant,frais)

    return realTx


def getTxStr(tx):
    tx_str = ""
    tx_str += str(tx.payeur)
    tx_str += str(tx.destinataire)
    if tx.amount < 10:
        tx_str += "0" + str(tx.amount)
    else:
        tx_str += str(tx.amount)
    tx_str += str(tx.fee)

    return tx_str



class Reward(Tx):
    def __init__(self,destinataire):
        self.payeur, self.destinataire, self.amount, self.fee = 0,destinataire,10,0

def findBlockIDs(list_blocks):
    list_blockIDs = []

    for block in list_blocks:
        blockID = block.blockID
        list_blockIDs.append(blockID)

    return(list_blockIDs)

def findAncestorIDs(newblockID):
    list_ancestorsIDs = []

    for n in range(len(str(newblockID))):
        list_ancestorsIDs.append(int(newblockID[n:]))

    print('in fct findAncestorIDs, ancestors of',newblockID,'are',list_ancestorsIDs)
    return(list_ancestorsIDs)

def findAncestors(list_ancestorIDs,list_blocks):
    list_ancestors = []

    for block in list_blocks:
        for id in list_ancestorIDs:
            if int(block.blockID) == id:
                list_ancestors.append(block)
                print('in fct findAncestors',block)

    return(list_ancestors)

def createMempool(list_nodes,nb_tx,max_amount):
    mempool = []

    for i in range(nb_tx):
        payeur = random.choice(list_nodes)
        max_fee = max_amount // 5
        fee = randint(0,max_fee)
        max_amount -= fee
        amount = randint(1,max_amount)

        # choisir un destinataire au hasard parmi tous les noeuds, sauf le payeur
        list_destinataires = list_nodes.copy()
        list_destinataires.remove(payeur)
        destinataire = random.choice(list_destinataires)

        tx = Tx(payeur, destinataire, amount, fee)
        mempool.append(tx)

#    for tx in mempool:
#        print(getTxStr(tx))
    return mempool


def checkBalance(list_nodes,new_blockID,list_blocks):
    print('$$ checkBalance $$')
    dict_balance = {}
    for node in list_nodes:
        dict_balance[node] = 0

    list_ancestorIDs = findAncestorIDs(new_blockID)
    list_ancestors = findAncestors(list_ancestorIDs,list_blocks)

    for block in list_ancestors:
        miner = int(str(block.blockID)[0])
        list_tx = block.list_tx
        for tx in list_tx:
            dict_balance[miner] += tx.fee
            if tx.payeur != 0:
                dict_balance[tx.payeur] -= (tx.amount + tx.fee)
            dict_balance[tx.destinataire] += tx.amount
        print("$$",block.blockID,dict_balance)

#    print('in fct checkBalance, end balance:',dict_balance)
    return dict_balance

def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

def readBlocksFromCSVFile():
    list_blocks = []
    newest_csv_file = newest('interac_bchains/')
#    newest_csv_file = 'interac_bchains/bchain_intterac_genese.csv'
#    newest_csv_file = 'interac_bchains/bchain_sim20221218_051429.csv'
    print("Reading bchain from",newest_csv_file)
    with open(newest_csv_file, newline='') as open_file:
        csv_reader = csv.reader(open_file, delimiter=',')
        for row in csv_reader:
            blockID = int(row[0])
            blockPoW = row[1]
            block_listTx = []
            for i in range(2,5):
                if len(row[i]) == 4:
                    row[i] = '0'+row[i]
                if len(row[i]) == 5:
                    tx = strToRealTx(row[i])
                    block_listTx.append(tx)
            block = Block(blockID,blockPoW,block_listTx)

            list_blocks.append(block)

    return list_blocks

def writeCSVRows(list_blocks):
    list_rows = []

    for block in list_blocks:
        list_tx = []
        for tx in block.list_tx:
            list_tx.append(int(getTxStr(tx)))
        for i in range(3):
            if len(list_tx) == 0:
                tx1 = 0
            else:
                tx1 = list_tx[0]
            if len(list_tx) > 1:
                tx2 = list_tx[1]
            else:
                tx2 = 0
            if len(list_tx) == 3:
                tx3 = list_tx[2]
            else:
                tx3 = 0
        row = [block.blockID, block.PoW, tx1, tx2, tx3]
        list_rows.append(row)

    return list_rows

def writeCSVRowsWithBalance(list_nodes,list_blocks):
    list_rows = []

    for block in list_blocks:
        list_tx = []
        for tx in block.list_tx:
            tx = getTxStr(tx)
            if len(tx) == 4:
                tx = '0' + tx
            list_tx.append(int(tx))
        for i in range(3):
            if len(list_tx) == 0:
                tx1 = 0
            else:
                tx1 = list_tx[0]
            if len(list_tx) > 1:
                tx2 = list_tx[1]
            else:
                tx2 = 0
            if len(list_tx) == 3:
                tx3 = list_tx[2]
            else:
                tx3 = 0
        dict_balance = checkBalance(list_nodes,str(block.blockID),list_blocks)
        row = [block.blockID, block.PoW, tx1, tx2, tx3, dict_balance]
        list_rows.append(row)

    return list_rows


def writeToFile(list_rows):
    # ### ------------------------- écriture de la bchain dans un fichier csv
    tstamp = str(datetime.utcnow())
    print('tstamp',tstamp)
    tstamp = tstamp[:-7]
    tstamp = tstamp.replace("-", "")
    tstamp = tstamp.replace(" ", "_")
    tstamp = tstamp.replace(":", "")
    tstamp = tstamp.replace(".", "_")
    print('tstamp',tstamp)
#    filename = 'bchain_sim/bchain_sim' + str(tstamp) + '.csv'
    filename = 'interac_bchains/bchain_interac' + str(tstamp) + '.csv'

    # open the file in the write mode
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        for row in list_rows:
            writer.writerow(row)

def createListBChainBlockIDs(list_blocks):
    list_bchain_blockIDs = []
    for block in list_blocks:
        list_bchain_blockIDs.append(block.blockID)

    return list_bchain_blockIDs

def getFee(tx):
    return tx.fee

def validateTx(mempool,dict_balance):
    list_validTx = []
    print('validateTx',dict_balance)
    for tx in mempool:
        payeur_balance = dict_balance[tx.payeur]
        if payeur_balance > tx.amount + tx.fee:
            list_validTx.append(tx)
            dict_balance[tx.payeur] -= tx.amount + tx.fee

#    for tx in list_validTx:
#        print(tx,tx.fee)

    list_validTx.sort(key=getFee, reverse=True)
    return list_validTx

def createNewBlockID(list_nodes,list_existing_blockIDs):
    minerID = random.choice(list_nodes)
    parentblockID = random.choice(list_existing_blockIDs)

    new_blockID = str(minerID) + str(parentblockID)

    return new_blockID

def createNewBlock(list_nodes,list_blocks):
    list_existing_blockIDs = createListBChainBlockIDs(list_blocks)
    new_blockID = createNewBlockID(list_nodes,list_existing_blockIDs)

    while new_blockID in list_existing_blockIDs:
        new_blockID = createNewBlockID(list_nodes, list_existing_blockIDs)

    minerID = int(new_blockID[0])
    reward = Reward(minerID)
    new_block_list_tx = [reward]
    mempool = createMempool(list_nodes,10,10)

    dict_balance = checkBalance(list_nodes, new_blockID, list_blocks)
    list_validTx = validateTx(mempool,dict_balance)

    if (len(list_validTx)) > 0:
        new_block_list_tx.append(list_validTx[0])
        if (len(list_validTx)) > 1:
            new_block_list_tx.append(list_validTx[1])

    PoW = bin(int(new_blockID))
    new_block = Block(new_blockID,PoW,new_block_list_tx)
    return(new_block)


