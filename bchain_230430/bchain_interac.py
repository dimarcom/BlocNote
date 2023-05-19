from bchain_rousseau import *

def createUserBlock():
    flag_erreur = False

    print("Quel est le blocID ?")
    blockID = input()
    if blockID[-1] != "0":
        print("Le blocID n'est pas valide.")
        flag_erreur = True

    print("Quelle est la PoW ?")
    PoW = input()
    if PoW != "0":
        PoW = "0b" + PoW
        target = blockID
        PoW_expected = bin(int(target))
        if PoW != str(PoW_expected):
            print("La PoW n'est pas valide.")
            flag_erreur = True

    print("La transaction de récompense est automatiquement ajoutée.")
    nodeID = int(blockID[0])
    reward = '0'+str(nodeID)+'10'+'0'
    reward = strToRealTx(reward)
    newblock_list_tx = [reward]

    print("Combien de transactions autres que la récompense ?")
    nb_tx = input()
    nb_tx = int(nb_tx)
    if nb_tx == 0:
        print("Pas de transaction autre que la récompense.")
    elif nb_tx > 2:
        print("Il n'est pas possible d'ajouter plus de deux transactions.")
    elif nb_tx >= 1:
        print("Quelle est la première transaction ?")
        tx = input()
        validateTxEntry(tx,list_nodes)
        tx = strToRealTx(tx)
        newblock_list_tx.append(tx)
        if nb_tx == 2:
            print("Quelle est la deuxième transaction ?")
            tx = input()
            validateTxEntry(tx,list_nodes)
            tx = strToRealTx(tx)
            newblock_list_tx.append(tx)

    if flag_erreur:
        print("Le bloc n'est pas valide.")
        user_block = Block(0,0,0)
    else:
        user_block = Block(blockID,PoW,newblock_list_tx)

    print('create userblock',user_block)
    return user_block

def validateTxEntry(tx,list_nodes):
    if len(tx) != 5:
        print("La transaction n'est pas valide.")
        print("""
            Le format d'une transaction est composé de 5 caractères:
            1 = l'adresse du payeur,
            2 = l'adresse du destinataire,
            3 et 4 = le montant de la transaction (entre 01 et 99),
            5 = les frais de transaction (entre 0 et 9).

            Par exemple, si le noeud 5 achète un vélo pour 35 R$ au noeud 7
            et accepte de payer des frais de transaction de 4 R$,
            la transaction est 57354.
            """)

    strtx = str(tx)
    if (strtx[0] or strtx[1]) not in list_nodes:
        print("Transaction invalide")


def updateBchain(list_nodes,user_block,list_blocks):
    user_block_parentID = str(user_block.blockID)[1:]

    miner = user_block.blockID



if __name__ == "__main__":

    list_nodes = [4,5,8,9]

    user_block = createUserBlock()
    print(user_block)
    user_blockID = str(user_block.blockID)
    user_block_parentID = str(user_block.blockID)[1:]

    list_blocks = readBlocksFromCSVFile()
    dict_balance = checkBalance(list_nodes, user_block_parentID, list_blocks)
    print("Solde avant l'ajout du nouveau bloc:",dict_balance)

    list_blockIDs = findBlockIDs(list_blocks)

    if int(user_block_parentID) not in list_blockIDs:
        print("Le nouveau bloc n'a pas de bloc-parent.")
    else:
        list_blocks.append(user_block)
        new_dict_balance = checkBalance(list_nodes, user_blockID, list_blocks)
        print(new_dict_balance)

    flag_newblockisok = True
    for balance in new_dict_balance:
        if new_dict_balance[balance] < 0:
            print("Block not valid !")
            flag_newblockisok = False

    if (flag_newblockisok):
        list_rows = writeCSVRows(list_blocks)
        #   list_rows = writeCSVRowsWithBalance(list_nodes,list_blocks)
        writeToFile(list_rows)
    else:
        print("No new cvs file.")







#   writeToFile(list_blocks)