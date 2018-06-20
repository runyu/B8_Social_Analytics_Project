import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from networkx.readwrite import json_graph
import json as json


def graph_mst(f_from, f_to_mst, f_to_centrality, f_to_top5):
    # read all nodes and edges
    f = open(f_from, 'r')
    spl = f.readlines()
    
    edge_weight = []
    
    for i in range(len(spl)):
        (src, dst, correl) = (spl[i].rstrip()).split('\t')
        correl_float = float(correl)
        edge_weight.append((src, dst, float("{0:.4f}".format(correl_float))))
    
    wg = nx.Graph()
    wg.add_weighted_edges_from(edge_weight)
    
    mst = nx.minimum_spanning_tree(wg)
    
    plt.figure(figsize=(20,20))
    nx.draw_networkx(mst, node_size=500, font_size=10)
    
    plt.show()
    
    plt.savefig('./data/mst.png', dpi=200) #save figure 
    
    json_data = json_graph.node_link_data(mst)
    
    with open(f_to_mst, 'w') as f:
        json.dump(json_data, f, indent=2)


    # =============================================================================
    # Centrality and top 5 tickers, the bigger distance, the lower correlation
    # =============================================================================
    eigenvector = nx.eigenvector_centrality_numpy(mst)
    degree = nx.degree_centrality(mst)
    closeness = nx.closeness_centrality(mst)
    betweenness = nx.betweenness_centrality(mst)
    betweenness_edges = nx.edge_betweenness_centrality(mst)
    
    #==============================================================================
    # create centralities for all nodes
    #==============================================================================
    centrality = {}
    index = 0
    for i in json_data['nodes']:
        centrality = {'name':i['id'], 
                    'eigenvector':[value for (key, value) in eigenvector.items() if key == i['id']][0],
                    'degree':[value for (key, value) in degree.items() if key == i['id']][0],
                    'closeness':[value for (key, value) in closeness.items() if key == i['id']][0],
                    'betweenness':[value for (key, value) in betweenness.items() if key == i['id']][0]}
        
        json_data['nodes'][index] = {'id':index, 'centrality':centrality}
        index += 1


    with open(f_to_centrality, 'w') as f:
        json.dump(json_data, f, indent=2)
    
    
    #==============================================================================
    # top 5 tickers
    #==============================================================================
    top5influencing_eigenvector = sorted(eigenvector.items(), key=lambda x: x[1], reverse = True)[:5]
    top5influencing_degree = sorted(degree.items(), key=lambda x: x[1], reverse = True)[:5]
    top5influencing_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse = True)[:5]
    top5influencing_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse = True)[:5]
    top5influencing_betweenness_edges = sorted(betweenness_edges.items(), key=lambda x: x[1], reverse = True)[:5]
    
    with open(f_to_top5, 'w', encoding='utf-8', ) as f:
        f.write('Top 5 Influencing Tickers by Eigenvector Centrality:' + '\n')
        for i in top5influencing_eigenvector:
            f.write(str(i) + '\n')
        f.write('\n')
        
        f.write('Top 5 Influencing Tickers by Degree Centrality:' + '\n')
        for i in top5influencing_degree:
            f.write(str(i) + '\n')
        f.write('\n')
        
        f.write('Top 5 Influencing Tickers by Closeness Centrality:' + '\n')
        for i in top5influencing_closeness:
            f.write(str(i) + '\n')
        f.write('\n')
        
        f.write('Top 5 Influencing Tickers by Betweenness Centrality:' + '\n')
        for i in top5influencing_betweenness:
            f.write(str(i) + '\n')
        f.write('\n')
        
        f.write('Top 5 Influencing Tickers by Edge Betweenness:' + '\n')
        for i in top5influencing_betweenness_edges:
            f.write(str(i) + '\n')
        f.write('\n')
    
