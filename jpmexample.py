#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 11:09:13 2022

@author: elyheston
"""

import yfinance as yf
import numpy as np
import pandas as pd
from pandas.tseries.offsets import DateOffset

vix_df = yf.download("^VIX")
vix_df["MA"] = vix_df.Close.rolling("30D").mean()
vix_df_filt = vix_df[vix_df.Close > 1.5 * vix_df.MA]
series = pd.Series(vix_df_filt.index).diff() / np.timedelta64(1,"D") >= 30
series[0] = True
signals = vix_df_filt[series.values]

sp_df = yf.download("^GSPC", start="1990-01-01")

test = sp_df[(sp_df.index >= signals.index[0]) & (sp_df.index <= signals.index[0] + DateOffset(months=6))]

(test.Close.pct_change() + 1).cumprod()

returns = []

for i in range(len(signals)):
    subdf = sp_df[(sp_df.index >= signals.index[i]) & (sp_df.index <= signals.index[i] + DateOffset(months=6))]
    returns.append((subdf.Close.pct_change()+1).prod())
    
reggie = pd.Series(returns).mean()
print(reggie)

(pd.Series(returns)-1).plot(kind="bar")