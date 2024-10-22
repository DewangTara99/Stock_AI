from csv import reader
import numpy as np
import pandas as pd
import math
import pandas_datareader as web
import datetime
import os
import requests
from bs4 import BeautifulSoup as bs
from Insider import InsiderTrading
from Initial_Parameters import Initial_Parameters
import yfinance as yf


# define moving average function
def moving_avg(x, n):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[n:] - cumsum[:-n]) / float(n)

# make a list of zeroes as placeholder list
def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros

# change string list to float list
def string_to_float(lst):
    lst_updated = [float(i) for i in lst]
    return lst_updated

def Parameters(Stock, URL):
    #Get initial parameter array for latter calculations
    Initial = Initial_Parameters(Stock)
    Date = Initial[0]
    Open = string_to_float(Initial[1])
    High = string_to_float(Initial[2])
    Low = string_to_float(Initial[3])
    Close = string_to_float(Initial[4])
    Adj_Close = string_to_float(Initial[5])
    Volume = string_to_float(Initial[6])

    # Daily Average
    counter = len(Open)
    Daily_Average = zerolistmaker(counter)
    index = 0

    while counter > 1:
        Daily_Average[index] = (float(Open[index]) + float(Close[index])) / 2
        index += 1
        counter -= 1
    Daily_Average[-1] = (float(Open[-1]) + float(Close[-1])) / 2

    # Bollinger Bands
    close = pd.DataFrame(Close)
    SMA = close.rolling(window=20).mean()   # 20-day Simple Moving Average
    STDEV = close.rolling(window=20).std()  # 20-day Rolling Standard Deviation

    Upper_Band = SMA + STDEV
    Lower_Band = SMA - STDEV

    # Price Channels
    Upper_Channel = close.rolling(20).max()   # 20-day High
    Lower_Channel = close.rolling(20).min()   #20-day Low
    
    # Relative Strength Index
    def computeRSI (data, time_window):
        diff = data.diff(1).dropna()        # diff in one field(one day)

        #this preservers dimensions off diff values
        up_chg = 0 * diff
        down_chg = 0 * diff
    
        # up change is equal to the positive difference, otherwise equal to zero
        up_chg[diff > 0] = diff[ diff>0 ]
    
        # down change is equal to negative deifference, otherwise equal to zero
        down_chg[diff < 0] = diff[ diff < 0 ]
    
        up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
        down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    
        rs = abs(up_chg_avg/down_chg_avg)
        rsi = 100 - 100/(1+rs)
        return rsi
    
    RSI = computeRSI(close, 14)

    # Moving Average Convergence Divergence

    EMA_12 = close.ewm(span=12, adjust=False).mean()
    EMA_26 = close.ewm(span=26, adjust=False).mean()
    
    MCAD = EMA_12 - EMA_26

    # Williams %R
    high = close.rolling(14).max()
    low = close.rolling(14).min()

    WilliamsR = (high - close) / (high - low)

    # Volatility
    Logarithmic_Returns = np.log(close/close.shift(1))
    Volatility = Logarithmic_Returns.rolling(window=252).std() * np.sqrt(252)

    # True Range
    L1 = high - low 
    L2 = abs(high - close.shift(1).dropna())
    L3 = abs(low - close.shift(1).dropna())
    List_L = pd.concat([L1, L2, L3], axis = 1)

    TR = List_L.max(axis = 1)

    SIZE = len(Open) - 253
    
    # Date to dataframe
    df_Date = pd.DataFrame(Date)

    # Insider Trading
    insider = InsiderTrading(URL)

    # S&P Index
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime.now()
    SP = yf.download('^GSPC', start, end)

    # Testing Parameter Array
    Parameters = [df_Date.tail(SIZE).to_numpy(),
                  pd.DataFrame(Open).tail(SIZE).to_numpy(),
                  pd.DataFrame(High).tail(SIZE).to_numpy(), 
                  pd.DataFrame(Low).tail(SIZE).to_numpy(), 
                  pd.DataFrame(Close).tail(SIZE).to_numpy(), 
                  pd.DataFrame(Adj_Close).tail(SIZE).to_numpy(), 
                  pd.DataFrame(Volume).tail(SIZE).to_numpy(), 
                  pd.DataFrame(Daily_Average).tail(SIZE).to_numpy(), 
                  SMA.tail(SIZE).to_numpy(), 
                  STDEV.tail(SIZE).to_numpy(), 
                  Upper_Band.tail(SIZE).to_numpy(), 
                  Lower_Band.tail(SIZE).to_numpy(),
                  Upper_Channel.tail(SIZE).to_numpy(),
                  Lower_Channel.tail(SIZE).to_numpy(),
                  RSI.tail(SIZE).to_numpy(),
                  MCAD.tail(SIZE).to_numpy(),
                  WilliamsR.tail(SIZE).to_numpy(),
                  Volatility.tail(SIZE).to_numpy(),
                  TR.tail(SIZE).to_numpy(),
                  pd.DataFrame(SP['Open'].to_list()).tail(SIZE).to_numpy(),
                  pd.DataFrame(SP['Volume'].to_list()).tail(SIZE).to_numpy(),
                  pd.DataFrame(insider).tail(SIZE).to_numpy()]

    # Parameters: {'Date', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume', 'Daily_Average', 'SMA', 'STDEV', 'Upper Band', 'Lower Band', 'Upper Channel', 'Lower Channel', 'RSI', 'MCAD', 'WilliamsR', 'Volatility', 'True Range', 'SP Open', 'SP Volume', 'Insider Trading'}
    return Parameters

# P = Parameters('NVDA', 1045810)
