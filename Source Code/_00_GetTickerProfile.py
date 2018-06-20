# =============================================================================
# find each ticker's name, industry and save into file
# =============================================================================
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_ticker_profile(f_from, f_to):
    tickers_prof = pd.DataFrame(data={'ticker':[], 'name':[], 'industry':[]})
    tickers = [line.rstrip() for line in open(f_from)]
    count = 0
    
    for tik in tickers:
        time.sleep(1)
        count += 1
        print('https://finance.yahoo.com/quote/'+tik+'/profile?p='+tik)
        req = requests.get('https://finance.yahoo.com/quote/'+tik+'/profile?p='+tik, allow_redirects=False)
        soup = BeautifulSoup(req.content, 'html.parser')
        
        ticker_name = ''
        ticker_industry = ''
        
        if soup.find('h3', {'data-reactid':'6'}):
            ticker_name = [soup.find('h3', {'data-reactid':'6'})][0].string
        elif soup.find('h3', {'class':'Mb(5px) Mend(40px)'}):
            ticker_name = [soup.find('h3', {'class':'Mb(5px) Mend(40px)'})][0].string
        elif soup.find('span', {'data-reactid':'5'}):
            ticker_name = [soup.find('span', {'data-reactid':'5'})][0].string
        
        if soup.find('strong', {'data-reactid':'21'}):
            ticker_industry = [soup.find('strong', {'data-reactid':'21'})][0].string
        elif soup.find('span', {'class':'Fl(end)'}):
            ticker_industry = [soup.find('span', {'class':'Fl(end)'})][0].string
#                                'industry':str([soup.find('span', {'class':'Fl(end)'})][0].string+'-'+[soup.find('span', {'class':'Fl(end)', 'data-reactid':'29'})][0].string)},
        else:
            ticker_industry = ticker_name
            
        tickers_prof = tickers_prof.append({'ticker':tik, 
                            'name':ticker_name, 
                            'industry':ticker_industry},
                            ignore_index=True)
        
    tickers_prof.to_csv(f_to)
