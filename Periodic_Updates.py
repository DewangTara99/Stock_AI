from csv import reader
import numpy as np
import pandas as pd
import math
import pandas_datareader as web
import datetime
import os
from Parameters import Parameters
import csv
import yfinance as yf

# updates stock's csv files
def Update_CSV(ticker):
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime.now()

    #df = web.DataReader(ticker, 'yahoo', start, end)
    df = yf.download(ticker, start, end)

    path = r'/Users/Dewangtara/Desktop/Stock_AI'
    CSVstring = str(ticker) + '.csv'
    df.to_csv(os.path.join(path, CSVstring))

Update_CSV('NVDA')
