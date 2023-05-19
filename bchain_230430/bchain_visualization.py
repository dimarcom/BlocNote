import csv
import os
import matplotlib.pyplot as plt
import networkx as nx
G = nx.Graph()

def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

list_blocs = []
list_nodes = []
#newest_csv_file = newest('bchains_sim/')
newest_csv_file = newest('interac_bchains/')
with open(newest_csv_file, newline='') as open_file:
#with open('bchains/bchain_sim20221026_193342.csv', newline='') as open_file:
    csv_reader = csv.reader(open_file, delimiter=',')
    for row in csv_reader:
        # row = row = [bloc.blocID,bloc.PoW,bloc.Tx]
        bloc = (row[0],row[1],row[2],row[3],row[4])
        list_blocs.append(bloc)
        list_nodes.append(row[0])
print(list_blocs)

G.add_nodes_from(list_nodes)
print(list(G.nodes))

list_edges = []
for bloc in list_blocs:
    if bloc[0] != '0':
        parent=bloc[0][1:]
        list_edges.append((bloc[0],parent))

G.add_edges_from(list_edges)
print(list(G.edges))

dict_labels = {}
nb_blocs = len(list_blocs)
#keys = range(nb_blocs)
for node in G.nodes:
    for bloc in list_blocs:
        if node == bloc[0]:
            PoW = bloc[1]
            tx = '0'+bloc[2]+"\n"+bloc[3]+"\n"+bloc[4]
            dict_labels[node] = node+'\n'+PoW + '\n'+tx
            #dict_labels[node] = node + '\n' + PoW
#            dict_labels[node] = node+'\n'+PoW+'\n'+tx+'\n'+bloc[5]
#            dict_labels[node] = node + '\n' + PoW + '\n' + bloc[5]
print("dict",dict_labels)

pos = nx.spring_layout(G)
# nx.draw(G, with_labels=True, font_weight='bold')
nx.draw(G,pos=pos,with_labels=False)
#nx.draw_networkx(G,pos=pos,labels=dict_labels)

nodenames = {}
for n in G.nodes():
    nodenames[n] = 'firstline \n secondline \n thirdline'
#nodenames = {n:'firstline \n secondline \n thirdline' for n in G.nodes()}
#nx.draw_networkx_labels(G, pos=pos, labels=nodenames)

nx.draw_networkx_labels(G, pos=pos, labels=dict_labels)

nx.draw_networkx(G, pos = pos, labels = dict_labels,
                 node_shape = "s", node_size = 1500,
                 node_color = "lightblue",
                 edge_color = "blue",  #color of the edges
                 edgecolors = "gray")     #edges of the box of node


plt.show()
