#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 09:09:07 2022

@author: ericberner
"""

import EconomicCalendar


#run daily beofre market open and filter for currencies with no high impact news
calendar_data = []
calendar_data = EconomicCalendar.news

print(calendar_data)
  



