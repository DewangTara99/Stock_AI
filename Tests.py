from datetime import datetime
from MultRegression import prediction
import pandas as pd


def CSV_to_DF(ticker):
        # Importing the datasets
        file = str(ticker) + '_updated.csv'
        datasets = pd.read_csv(file)
        return datasets

def Diff(n, a):
        ticker = 'NVDA'
        dataset = CSV_to_DF(ticker)
        inputs = dataset.iloc[a, 2:].values
        out1 = dataset.iloc[a + n, 1]
        # input ticker, today's parameters, and the future Open price after 'n' days
        out2 = prediction(ticker, inputs, n)
        out = (out2 - out1) 
        return out

