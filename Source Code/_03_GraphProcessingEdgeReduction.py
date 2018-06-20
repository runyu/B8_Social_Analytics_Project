# =============================================================================
# discretise nodes distance
# create cluster graph
#    https://bl.ocks.org/mbostock/950642
#    https://gist.github.com/fancellu/2c782394602a93921faff74e594d1bb1
# =============================================================================
import numpy as np
import networkx as nx
import pandas as pd

#from networkx.readwrite import json_graph
import json as json


step = 0.2
limit = 0.7

def graph_reduction(f_from, f_to):
    # read all nodes and edges
    f = open(f_from, 'r')
    spl = f.readlines()
    
    edge_weight = []
    u = []
    v = []
    
    # only take corr < 0.7
    for i in range(len(spl)):
        (src, dst, correl) = (spl[i].rstrip()).split('\t')
        if float(correl) < limit:
            band = int(float(correl)/step + 1)
            edge_weight.append((src, dst, str(band)))
        if src not in u: u.append(src)
        if dst not in v: v.append(dst)
    
    wg = nx.Graph()
    wg.add_weighted_edges_from(edge_weight)
 
    edges = wg.edges(data='weight')
    
    nodes_list = pd.DataFrame({'id':[], 'group':[]})
    
    for source, target, weight in edges:
        if source not in nodes_list['id'].values:
            nodes_list = nodes_list.append({'id':source, 'group':weight}, ignore_index=True)
        if target not in nodes_list['id'].values:
            nodes_list = nodes_list.append({'id':target, 'group':weight}, ignore_index=True)
    
    """ create cluster.json """
    nodes_str = ""
    count = 0
    for i, r in nodes_list.iterrows():
        nodes_str = nodes_str + "{\"id\":\"" + r['id'] + "\", \"score\":" + r['group'] + "},"
        count += 1
    nodes_str = nodes_str.rstrip(',')
    
    links_str = ""
    for i, j, k in edges:
        source_index = np.where(nodes_list['id']==i)
        target_index = np.where(nodes_list['id']==j)
        links_str = links_str + "{\"source\":" + str(source_index[0][0]) + ", \"target\":" + str(target_index[0][0]) + "},"
    links_str = links_str.rstrip(',')
    
    json_str = "{\"nodes\":[" + nodes_str + "], \"links\":[" + links_str + "]}"
    parsed = json.loads(json_str)        
    json.dump(parsed, open(f_to,'w'), indent=4)
    
  
    
    
    dg = nx.degree_centrality(wg)
    degree_centrality = pd.from_dict(dg, orient='columns')

    #http://bl.ocks.org/AMDS/4a61497182b8fcb05906
    f_ticker_profile = '../data/tickers_prof.tsv'
    tickers_prof = pd.read_csv(f_ticker_profile, sep='\t', index_col=0)
    
    
    for key in degree_centrality:
        tickers_prof['degree'] = np.where(tickers_prof['ticker']==key, degree_centrality[key])