from _00_GetTickerProfile import get_ticker_profile
from _01_DataRetrievalYahoo import retrieve_closing_price
from _02_DataProcessing import process_data
from _03_GraphProcessingEdgeReduction import graph_reduction
from _04_GraphProcessingMST import graph_mst   
from _05_GraphDendrogram import graph_dendrogram   


f_tickers = './data/tickers.csv'
f_tickers_prof = './data/tickers_prof.tsv'
f_close_price = './data/close_price.tsv'
f_close_price_graph = './data/close_price_distance.graph'
f_cluster = './data/cluster.json'
f_mst = './data/mst.json'
f_centrality = './data/centrality.csv'
f_close_price_change = './data/close_price_change.tsv'
f_dendrogram = './data/'
f_to_centrality = './centrality/mst_centrality.json'
f_to_top5 = './data/top5influencing.txt'


start_date = '2015-01-01'
end_date = '2017-12-31'


get_ticker_profile(f_from=f_tickers, f_to=f_tickers_prof)
retrieve_closing_price(f_from=f_tickers, f_to=f_close_price, d_from=start_date, d_to=end_date)
process_data(f_from=f_close_price, f_to=f_close_price_graph)
graph_reduction(f_from=f_close_price_graph, f_to=f_cluster)
graph_mst(f_from=f_close_price_graph, f_to_mst=f_mst, f_to_centrality=f_centrality, f_to_top5=f_to_top5)
graph_dendrogram(f_from=f_close_price_graph, f_to=f_dendrogram)



