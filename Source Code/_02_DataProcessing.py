# =============================================================================
# 1. calculate Pearson correlation coefficient and p-value between pairs of stocks 
# 2. convert Pearson correlation coefficient into distance: d(i,j) = sqrt(2*(1-correl)): 
#      the stronger correlation coefficient between 2 tickers the shorter distance they have
# 3. save distance into file
# =============================================================================
import pandas as pd
import itertools
from scipy.stats.stats import pearsonr
import numpy as np
import math

def process_data(f_from, f_to):
    close = pd.read_csv(f_from, sep ='\t', index_col=0)
    close_log = np.log(1 + close.pct_change())
    
    # clean rows which all elementsa are nan
    close_log_clean_r = close_log.dropna(axis=0, how='all')
    # clean cols which any of elements are nan
    close_log_clean_rc = close_log_clean_r.dropna(axis=1, how='any')
    
    
    correlations = {}
    columns = close_log_clean_rc.columns.tolist()
    
    for col_a, col_b in itertools.combinations(columns, 2):
        correlations[col_a + '__' + col_b] = pearsonr(close_log_clean_rc.loc[:, col_a], close_log_clean_rc.loc[:, col_b])
    
    result = pd.DataFrame.from_dict(correlations, orient='index')
    result.columns = ['corr', 'p-value']
    
    result_corr = result[result.columns[0:1]]
    
    print(result_corr.sort_index())
    
    correlations_string=''
    for k, v in correlations.items():
        assetA = k.split('__')[0]
        assetB = k.split('__')[1]
        
        # compute distance
        distance = math.sqrt(2*(1- v[0]))
        corr = str(distance)
        keyAndValue = (assetA, assetB, corr)

        correlations_string = correlations_string + '\t'.join(keyAndValue) + '\n'
    
    file =open(f_to, 'w', encoding='utf-8')
    file.write(correlations_string)
    file.close()