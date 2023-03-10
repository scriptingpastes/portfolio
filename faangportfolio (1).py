# -*- coding: utf-8 -*-
"""faangportfolio.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gUrkS9bEAMBcAXUJdz66wDvzVxKFDmAU
"""

import matplotlib.pyplot as plt
import pandas_datareader.data as web
import numpy as np
import pandas as pd
!pip install yfinance
import yfinance as yf
import datetime as dt

meta_hist_list = [0, 1.053, .4277, .3415, .093, .5338, -.2571, .5657, .3309, .2313]
apple_hist_list = [ .3259, .0806, .4062, -.0302, .1248, .4848, -.0539, .8897, .8231, .3465]
amzn_hist_list = [ .4493, .5896, -.2218, 1.1778, .1095, .5596, .2843, .2303, .7626, .0238]
nflx_hist_list = [.3363, 2.9764, -.0721, 1.3438, .0824, .5506, .3944, .2089, .6711, .1141]
goog_hist_list = [.0952, .5843, -.0559, .4661, .0186, .3293, -.008, .2818, .3085, .6530]

portval = 10000
port_list = []
idx = 0
port_list.append(((0.2 * portval) * (meta_hist_list[idx]+1)) + ((0.2 * portval) * (apple_hist_list[idx]+1)) + ((0.2 * portval) * (amzn_hist_list[idx]+1)) + ((0.2 * portval) * (nflx_hist_list[idx]+1)) + ((0.2 * portval) * (goog_hist_list[idx]+1)))
meta1 = ((0.2 * portval) * (meta_hist_list[idx]+1))
apple1 = ((0.2 * portval) * (apple_hist_list[idx]+1))
amzn1 = ((0.2 * portval) * (amzn_hist_list[idx]+1))
nflx1 = ((0.2 * portval) * (nflx_hist_list[idx]+1))
goog1 = ((0.2 * portval) * (goog_hist_list[idx]+1))

print(port_list[idx])

print(len(meta_hist_list), len(apple_hist_list), len(amzn_hist_list), len(nflx_hist_list), len(goog_hist_list))

pct_list = []
prev_portal_val = portval
portal_val_cur = port_list[0]
print (prev_portal_val, portal_val_cur)
pct_list.append((portal_val_cur- prev_portal_val)/prev_portal_val)
prev_portal_val = portal_val_cur

print(idx, ":", portal_val_cur, ":", pct_list[idx])

for index in range(1, len(apple_hist_list)):
   port_list.append(((apple1) * (apple_hist_list[index]+1)) + ((amzn1) * (amzn_hist_list[index]+1)) + ((goog1) * (goog_hist_list[index]+1)) + ((nflx1) * (nflx_hist_list[index]+1)) + ((meta1)) * (meta_hist_list[index]+1))
   apple1 = ((apple1) * (apple_hist_list[index]+1))
   amzn1 = ((amzn1) * (amzn_hist_list[index]+1))
   meta1 = ((meta1) * (meta_hist_list[index]+1))
   goog1 = ((goog1) * (goog_hist_list[index]+1))
   nflx1 = ((nflx1) * (nflx_hist_list[index]+1))

   portal_val_cur = port_list[index]
   pct_list.append((portal_val_cur- prev_portal_val)/prev_portal_val)
   prev_portal_val = portal_val_cur

   print(index, ":" ,  port_list[index], ":", pct_list[index])

# Commented out IPython magic to ensure Python compatibility.
begin_time = dt.datetime(2012,12,31)
end_time = dt.datetime(2015,12,31)


stocks = ['AAPL','AMZN','META','NFLX', 'GOOG']
num_of_stock_picks = len(stocks)
print(num_of_stock_picks)
 
data = yf.download(stocks,start= begin_time, end= end_time)['Adj Close']

stockreturns = data.pct_change()

mean_returns = stockreturns.mean()
cov_matrix = stockreturns.cov()

mc_sims = 20000
num_of_intermid_vars = 3 
results = np.zeros((num_of_intermid_vars+num_of_stock_picks, mc_sims))
print (results.shape) 

trading_days_in_a_year = 252 

for i in range(mc_sims):
    weights = np.array(np.random.random(num_of_stock_picks))
    weights /= np.sum(weights)

    portfolio_return = np.sum(mean_returns * weights) * trading_days_in_a_year
    portfolio_std_dev = np.sqrt(np.dot(weights.T,np.dot(cov_matrix, weights))) * np.sqrt(trading_days_in_a_year)

    results[0,i] = portfolio_return             # ret
    results[1,i] = portfolio_std_dev            # stdev
    results[2,i] = results[0,i] / results[1,i]  # sharp

    for j in range(num_of_stock_picks) :  #len(weights)):
        results[j+3,i] = weights[j]
 

results_frame = pd.DataFrame(results.T,columns=['ret','stdev','sharpe',stocks[0],stocks[1],stocks[2],stocks[3],stocks[4]])

max_sharpe_port = results_frame.iloc[results_frame['sharpe'].idxmax()]

max_vol_port = results_frame.iloc[results_frame['stdev'].idxmax()]

min_vol_port = results_frame.iloc[results_frame['stdev'].idxmin()]

max_ret_port = results_frame.iloc[results_frame['ret'].idxmax()]
# %matplotlib inline
plt.scatter(results_frame.stdev,results_frame.ret,c=results_frame.sharpe,cmap='RdYlBu',s=1)
plt.xlabel('Volatility')
plt.ylabel('Returns')
plt.colorbar()
plt.scatter(max_sharpe_port[1],max_sharpe_port[0],marker=(5,1,0),color='r',s=100)
plt.scatter(min_vol_port[1],min_vol_port[0],marker=(5,1,0),color='g',s=100)
data.plot()
print (max_sharpe_port)
print (max_vol_port)
print (max_ret_port)
print (min_vol_port)

# Commented out IPython magic to ensure Python compatibility.
begin_time = dt.datetime(2012,12,31)
end_time = dt.datetime(2015,12,31)


stocks = ['AAPL','AMZN','META','NFLX', 'GOOG']
num_of_stock_picks = len(stocks)
print(num_of_stock_picks)
 
data = yf.download(stocks,start= begin_time, end= end_time)['Adj Close']

stockreturns = data.pct_change()

mean_returns = stockreturns.mean()
cov_matrix = stockreturns.cov()

mc_sims = 20000
num_of_intermid_vars = 3 
results = np.zeros((3+num_of_stock_picks, mc_sims))
print (results.shape) 

trading_days_in_a_year = 252 

for i in range(mc_sims):
    weights = np.array(np.random.random(num_of_stock_picks))
    weights /= np.sum(weights)

    portfolio_return = np.sum(mean_returns * weights) * trading_days_in_a_year
    portfolio_std_dev = np.sqrt(np.dot(weights.T,np.dot(cov_matrix, weights))) * np.sqrt(trading_days_in_a_year)

    results[0,i] = portfolio_return             # ret
    results[1,i] = portfolio_std_dev            # stdev
    results[2,i] = results[0,i] / results[1,i]  # sharp

    for j in range(num_of_stock_picks) :  #len(weights)):
        results[j+3,i] = weights[j]
 

results_frame = pd.DataFrame(results.T,columns=['ret','stdev','sharpe',stocks[0],stocks[1],stocks[2],stocks[3],stocks[4]])

max_sharpe_port = results_frame.iloc[results_frame['sharpe'].idxmax()]

max_vol_port = results_frame.iloc[results_frame['stdev'].idxmax()]

min_vol_port = results_frame.iloc[results_frame['stdev'].idxmin()]

max_ret_port = results_frame.iloc[results_frame['ret'].idxmax()]
# %matplotlib inline
plt.scatter(results_frame.stdev,results_frame.ret,c=results_frame.sharpe,cmap='RdYlBu',s=1)
plt.xlabel('Volatility')
plt.ylabel('Returns')
plt.colorbar()
plt.scatter(max_sharpe_port[1],max_sharpe_port[0],marker=(5,1,0),color='r',s=100)
plt.scatter(min_vol_port[1],min_vol_port[0],marker=(5,1,0),color='g',s=100)
data.plot()
print (max_sharpe_port)
print (max_vol_port)
print (max_ret_port)
print (min_vol_port)