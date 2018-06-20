# =============================================================================
# use pearson correlation coefficient values between pairs of tickers to calculate dendrogram
# =============================================================================
import numpy as np
import networkx as nx
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

def graph_dendrogram(f_from, f_to):
    np.set_printoptions(precision=4, suppress=True)
    plt.figure(figsize=(10,3))
    plt.style.use('seaborn-whitegrid')
    
    f = open(f_from, 'r')
    spl = f.readlines()
    
    edge_weight = []
    
    for i in range(len(spl)):
        (src, dst, correl) = (spl[i].rstrip()).split('\t')
        correl_float = float(correl)
        edge_weight.append((src, dst, float("{0:.4f}".format(correl_float))))
    
    
    wg = nx.Graph()
    wg.add_weighted_edges_from(edge_weight)
    
    tcsr = nx.to_scipy_sparse_matrix(wg)
    
    arr = tcsr.toarray().astype(float)
    mat = np.array(arr)
    
    mat_absolute = np.absolute(mat)
    
    methods = ['average', 'ward', 'complete']
    for mtd in methods:
        linkage_matrix = linkage(mat_absolute, mtd)
            
        labelsize=15
        ticksize=8
        fig, ax = plt.subplots(figsize=(10, 15)) # set size
        dendrogram(linkage_matrix, orientation="right", labels=list(wg.nodes()), leaf_font_size=ticksize)
        
        plt.title('Investment Products Hierarchical Clustering Tree (' + mtd + ')', fontsize=labelsize)
        plt.xlabel('distance', fontsize=labelsize)
        plt.ylabel('stock', fontsize=labelsize)
        plt.tick_params(\
            axis= 'x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='on')
        
        ax.axvline(2.5, color="black", linestyle="--")
        
        plt.tight_layout() #show plot with tight layout
        
        plt.savefig(f_to + mtd +'.png', dpi=200) #save figure 
    
    
