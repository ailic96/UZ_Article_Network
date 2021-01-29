import networkx as nx           # Network operations
import numpy as np              # Reading .mtx
from scipy.io import mmread     # Reading .mtx
import matplotlib.pyplot as plt        # Basic plotting
import operator                 # Sorting and converting dictionary to a list
import pandas as pd             # Tables and visualization
import collections              # Counting
import community                # Communities

def txt_to_graphi(graph, name):
    """Converts a file to graphi file for further visualization (Just changes file extension).

    Args:
        graph (graph):  graph file
        name (str):     output file name
    """

    with open('visualization/'+ name +'.graphml', 'wb') as output_file:
        nx.write_graphml(graph, output_file)
    
    print(name + '.graphml file generated')
        

def global_layer(graph):

    """Prints basic global graph properties.

    Args:
        graph (graph): .txt loaded as a graph file
    """

    print('Osnovne informacije o grafu: ')
    print('Je li graf usmjeren?', nx.is_directed(graph))
    print('Je li graf tezinski?:', nx.is_weighted(graph))
    
    total_nodes = graph.number_of_nodes()
    print('\nBroj cvorova N u grafu: ' + str(total_nodes))
    total_edges = graph.number_of_edges()
    print('Broj veza K u grafu: ' + str(total_edges))
    print('Broj ulaznih veza: ' + str(len(graph.in_degree())))
    print('Broj izlaznih veza: ' + str(len(graph.out_degree())))
    print('Prosjecan stupanj mreze: ' + str(len(list(nx.average_degree_connectivity(graph)))))
    
    total_weight = graph.size(weight='weight')
    avg_weight = total_weight / total_nodes
    print('Ukupna snaga grafa: ' + str(total_weight))
    print('Prosjecna snaga grafa: ' + str(avg_weight))

    # Creating a graph copy
    G_copy = graph.copy()

    edge_weights = nx.get_edge_attributes(G_copy,'weight')
    G_copy.remove_edges_from((e for e, w in edge_weights.items() if w <= 10))

    largest_comp = graph.subgraph(max(nx.weakly_connected_components(G_copy), key=len)) 

    total_nodes_comp = largest_comp.number_of_nodes()
    print('\nBroj cvorova N u najvecoj komponenti: ' + str(total_nodes_comp))
    total_edges_comp = largest_comp.number_of_edges()
    print('Broj veza K u najvecoj komponenti ' + str(total_edges_comp))

    avg_path = nx.average_shortest_path_length(largest_comp)
    print('Prosjecni najkraci put komponente ' + str(len(largest_comp)) + ' iznosi: ' + str(avg_path))

    diam = nx.diameter(largest_comp.to_undirected())
    print('Dijametar najveće komponente ' + str(len(largest_comp)) + ' iznosi: ' + str(diam)) 
   

    # Broj povezanih komponenti
    conn_comp = nx.number_weakly_connected_components(graph)
    conn_comp_max = len(list(max(nx.weakly_connected_components(graph), key=len)))
    print('Broj povezanih komponenti grafa: ' + str(conn_comp))
    print('Velicina najvece komponente grafa: ' + str(conn_comp_max))

    # Gustoća grafa
    print('Gustoća grafa: ' + str(nx.density(graph)))

    # Koeficijent grupiranja
    avg_clustering = nx.average_clustering(graph)
    print('Globalni koeficijent grupiranja: ' + str(avg_clustering))

    #Koeficijent asortativnosti
    node_assortativity = nx.degree_assortativity_coefficient(graph)
    print('Asortativnost s obzirom na stupanj cvora: ' + str(node_assortativity))
    

    # Histogram distribucije stupnjeva
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color="b")

    plt.title("Histogram distribucije stupnjeva")
    plt.ylabel("Broj")
    plt.xlabel("Stupanj")
    ax.set_xticklabels(deg)
    plt.ylim(0, 3442)
    plt.xlim(0, 5000)



def local_layer(graph):
    """Prints basic global graph properties.

    Args:
        graph (): graph (graph): .txt loaded as a graph file
    """

    degree_cent = nx.degree_centrality(graph)
    sorted_degree = sorted(degree_cent.items(), key=operator.itemgetter(1), reverse=True)  
    degree_df = pd.DataFrame(sorted_degree, columns=['Node','Degree Centrality'])

    print('******************************************')
    print('\nData for graph of length: ', len(graph))
    print('Degree: ')
    print(degree_df.head(n=10))

    curr_flow_clos_cent = nx.eigenvector_centrality(graph)
    sorted_curr_flow_clos_cent = sorted(curr_flow_clos_cent.items(), key=operator.itemgetter(1), reverse=True)  
    sorted_curr_flow_clos_cent_df = pd.DataFrame(sorted_curr_flow_clos_cent, columns=['Node','Eigenvector Centrality'])
    
    print('\nEigenvector centrality: ')
    print(sorted_curr_flow_clos_cent_df.head(n=10))
    

    G_copy = graph.to_undirected()
    comp_list = [ G_copy.subgraph(c) for c in nx.connected_components(G_copy)]
   
    for graph in comp_list:
        
        if len(graph) >= 1000:
            print('Ecentricnost za komponentu s velicinom: ' + str(len(graph)))
        
            eccent = nx.current_flow_closeness_centrality(graph)
            eccent_sorted = sorted(eccent.items(), key=operator.itemgetter(1), reverse=True) 
            eccent_df =  pd.DataFrame(sorted_degree, columns=['Node','Eccentricity Centrality'])

            print('\nEccentricity centrality: ')
            print(degree_df.head(n=10))
           

            
fh=  open('data/portal_article_all_bigrams_counted.txt',        'r',  encoding='utf-8')
fh_1=open("data/portal_article-2020-02-24_bigrams_counted.txt", 'r', encoding='utf-8')
fh_2=open("data/portal_article-2020-03-13_bigrams_counted.txt", 'r', encoding='utf-8')
fh_3=open("data/portal_article-2020-05-11_bigrams_counted.txt", 'r', encoding='utf-8')
fh_4=open("data/portal_article-2020-08-25_bigrams_counted.txt", 'r', encoding='utf-8')

G =nx.read_edgelist(fh,   nodetype=str, data=(('weight',int),), create_using=nx.DiGraph())
G1=nx.read_edgelist(fh_1, nodetype=str, data=(('weight',int),), create_using=nx.DiGraph())
G2=nx.read_edgelist(fh_2, nodetype=str, data=(('weight',int),), create_using=nx.DiGraph())
G3=nx.read_edgelist(fh_3, nodetype=str, data=(('weight',int),), create_using=nx.DiGraph())
G4=nx.read_edgelist(fh_4, nodetype=str, data=(('weight',int),), create_using=nx.DiGraph())

txt_to_graphi(G1, 'G1_2020-02-24')
txt_to_graphi(G2, 'G2_2020-03-13')
txt_to_graphi(G3, 'G3_2020-05-11')
txt_to_graphi(G4, 'G4_2020-08-25')

global_layer(G)
local_layer(G1)
local_layer(G2)
local_layer(G3)
local_layer(G4)
