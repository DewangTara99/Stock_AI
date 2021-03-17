from datetime import datetime
from Regression import prediction
import pandas as pd
import matplotlib.pyplot as plt 

# Convert Updated_CSV to Pandas DataFrame
def CSV_to_DF(ticker):
        file = str(ticker) + '_updated.csv'
        datasets = pd.read_csv(file)
        return datasets

# Returns percent error of an algorithm for any given day
def percentError(n, day, ticker):
        dataset = CSV_to_DF(ticker)
        inputs = dataset.iloc[day, 2:].values
        out1 = dataset.iloc[day + n, 1]
        out2 = prediction(ticker, inputs, n)
        out = ((out2 - out1) / (out1)) * 100
        return out

# Returns percent error in prediction over a certain range
def percentErrorOverRange(d1, d2, d, ticker):
        b = 0
        for i in range(d1, d2):
                a = percentError(d, i, ticker)
                b += abs(a)
        returnStr = round(b/(d2 - d1),3)
        return returnStr

def Error(n, ticker):
        return percentErrorOverRange(0,2566-(2*n),n, ticker)


# Setting Coordinates with 'x' as Dates and 'y' as Error
x = range(1,40)
y = []
# Error Test for AMD
for i in range(1,40):
        y.append(Error(i, 'AMD')) 
        
# Graphing Error
plt.plot(x, y) 
plt.xlabel('Days') 
plt.ylabel('Error') 
plt.title('Average Percent Error of Predictions') 
plt.show() 
