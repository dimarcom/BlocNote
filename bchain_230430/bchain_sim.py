from bchain_rousseau import *

if __name__ == "__main__":

    list_nodes = [4,5,8,9]
    nb_blocks = 10
    list_blocks = [Block(0,0,[])]

    while len(list_blocks) < nb_blocks:
        list_blocks.append(createNewBlock(list_nodes,list_blocks))

    for block in list_blocks:
        print(block)

    list_rows = writeCSVRows(list_blocks)
#   list_rows = writeCSVRowsWithBalance(list_nodes,list_blocks)
    writeToFile(list_rows)