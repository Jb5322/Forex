#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 10:14:07 2022

@author: ericberner
"""

import bt
# fetch some data
data = bt.get('spy,agg,eem,db,gs', start='2010-01-01')
# create the momentum strategy - we will specify the children (3rd argument)
# to limit the universe the strategy can choose from
mom_s = bt.Strategy('mom_s', [bt.algos.RunMonthly(),
                              bt.algos.SelectAll(),
                              bt.algos.SelectMomentum(1),
                              bt.algos.WeighEqually(),
                              bt.algos.Rebalance()],
                    ['spy', 'eem'])
extra_strategy = bt.Strategy('extra_strategy', [bt.algos.RunMonthly(),
                              bt.algos.SelectAll(),
                              bt.algos.SelectMomentum(1),
                              bt.algos.WeighEqually(),
                              bt.algos.Rebalance()],
                    ['db', 'gs'])
# create the master strategy - this is the top-most node in the tree
# Once again, we are also specifying  the children. In this case, one of the
# children is a Security and the other other 2 are Strategies.
master = bt.Strategy('master', [bt.algos.RunMonthly(),
                                bt.algos.SelectAll(),
                                bt.algos.WeighEqually(),
                                bt.algos.Rebalance()],
                    [mom_s, extra_strategy, 'agg'])
# create the backtest and run it
test = bt.Backtest(master, data)
# create results so we can display and plot
results = bt.run(test)
results.plot()
results.display()
results.plot_security_weights()