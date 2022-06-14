#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 09:26:58 2022
Script for loop to find best sma
@author: ericberner
"""

import pandas as pd
import bt

def above_sma(tickers, sma_per=50, start='2015-01-01', name='above_sma'):
   
    data = bt.get(tickers, start=start)
   
    sma = data.rolling(sma_per).mean()
    
    s = bt.Strategy(name, [bt.algos.SelectWhere(data > sma),
                           bt.algos.WeighEqually(),
                           bt.algos.Rebalance()])
   
    return bt.Backtest(s, data)

result_df = pd.DataFrame(columns = ['SMA','CAGR','daily_sharpe'])

tickers = 'goog,AAPL,msft'

for SMA_number in range(10,20): 

    SMA_name='sma'+ str(SMA_number)

    result = bt.run(above_sma(tickers, sma_per=SMA_number, name= SMA_name))

    result_df = result_df.append({'SMA':SMA_number,'CAGR':result.stats.at['cagr',SMA_name], 
                                  'daily_sharpe': 
result.stats.at['daily_sharpe',SMA_name]},ignore_index=True)
   
result_df.set_index('SMA',inplace=True, drop=True)
