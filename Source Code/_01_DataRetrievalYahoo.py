# =============================================================================
# retrieve closing price for each for each tickers
# clean data by removing null values
# =============================================================================
from pandas_datareader import data as pdr
import pandas as pd

import fix_yahoo_finance as yf
yf.pdr_override() 

def retrieve_closing_price(f_from, f_to, d_from, d_to):
    tickers_file = open(f_from, 'r')
    tickers_list = tickers_file.readlines()
    tickers_file.close()
    
    tickers = []
    
    for i in tickers_list:
        tickers.append(i.strip())
    
    # Use pandas_reader.data.DataReader to load the desired data.
    panel_data = pdr.get_data_yahoo(tickers, d_from, d_to)
    
    # Getting just the adjusted closing prices. This will return a Pandas DataFrame
    # The index in this DataFrame is the major index of the panel_data.
    close = panel_data.loc['Close']
    
    # Getting all weekdays between 01/01/2013 and 12/31/2017
    all_weekdays = pd.date_range(start=d_from, end=d_to, freq='B')
    
    # How do we align the existing prices in adj_close with our new set of dates
    # All we need to do is reindex close using all_weekdays as the new index
    close = close.reindex(all_weekdays)
    
    # clean rows which all elements are nan
    close_clean_c = close.dropna(axis=0, how='all')
    
    # clean cols which any elements are nan
    close_clean_rc = close_clean_c.dropna(axis=1, how='any')
    
    close_clean_rc.to_csv(f_to, sep='\t', encoding='utf-8')
