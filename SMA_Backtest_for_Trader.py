#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 10:14:42 2022

@author: ericberner
"""
import pandas as pd
import matplotlib.pyplot as plt
import bt
import seaborn as sns


# first let's create a helper function to create a ma cross backtest
def ma_cross(tickers, short_ma=10, long_ma=100, name='ma_cross'):
    # these are all the same steps as above
    
    short_sma = data.rolling(short_ma).mean()
    long_sma  = data.rolling(long_ma).mean()

    # target weights
    
    #include rsi 30 and 70
    tw = long_sma.copy()
    tw[short_sma > long_sma] = 1.0
    tw[short_sma <= long_sma] = -1.0

    # here we specify the children (3rd) arguemnt to make sure the strategy
    # has the proper universe. This is necessary in strategies of strategies
    s = bt.Strategy(name, [bt.algos.WeighTarget(tw), bt.algos.Rebalance()])

    return bt.Backtest(s, data)

tickers = 'usdjpy=x,eurcad=x,euraud=x,eurjpy=x' 

data = bt.get(tickers, start = '2020-1-1', end ='2021-6-1')

result_df = pd.DataFrame(columns = ['SMA_Short','SMA_Long','CAGR','daily_sharpe'])


for SMA_long_number in range(25,275,5):
    
    for SMA_number in range(10,100,2): 

        SMA_name='sma'+ str(SMA_number)

        result = bt.run(ma_cross(tickers, short_ma=SMA_number, long_ma=SMA_long_number, name=SMA_name))

        result_df = result_df.append({'SMA_Short':SMA_number,'SMA_Long':SMA_long_number,'CAGR':result.stats.at['cagr',SMA_name], 
                                      'daily_sharpe': result.stats.at['daily_sharpe',SMA_name]},ignore_index=True)
       
result_df.set_index('SMA_Short',inplace=True, drop=True)


print(result_df)

subset_sharpe_str = result_df.pivot(columns='SMA_Long',values='daily_sharpe')

subset_sharpe = subset_sharpe_str.astype(float)

subset_cagr_str = result_df.pivot(columns='SMA_Long',values='CAGR')

subset_cagr = subset_cagr_str.astype(float)

fig, ax = plt.subplots(figsize=(15, 5))

sns.heatmap(subset_sharpe, cmap='coolwarm').set(title='Daily Sharpe')
plt.show()

fig, ax = plt.subplots(figsize=(15, 5))

sns.heatmap(subset_cagr, cmap='coolwarm').set(title='CAGR')
plt.show()



