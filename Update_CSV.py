from Parameters import Parameters
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.recfunctions import append_fields
import os


def compileParameters(Ticker, URL):
    # Initial Parameter Derivations 
    P = Parameters(Ticker, URL)

    # Insider Trading Indexed by Date
    date = P[0]
    insider = P[21]

    insiderNew = [0] * len(date)
    insiderMut_1 = [k[0] for k in insider]
    insiderMut_2 = [k[1] for k in insider]

    insiderMut = dict(zip(insiderMut_1, insiderMut_2))

    k = 0
    for k in range(len(insiderNew)):
        date_el = date[k][0]
        if date_el in insiderMut_1:
            insiderNew[k] = float(insiderMut[date_el])
        else:
            insiderNew[k] = float(0)

    insiderCoeff = np.array(insiderNew)
    insiderCoeff.resize((len(P[0]),1),refcheck=False)

    # Compile All Parameters
    P[18] = np.array(P[18], copy=False, subok=True, ndmin=2).T
    Parameter = P[1]
    count = 2
    while count < 21:
        Parameter = np.append(Parameter, P[count], 1)
        count += 1
    allParameter = np.append(Parameter, insiderCoeff, 1)
    return allParameter

def updateCSV_Parameters(Ticker, URL):
    csvParameters = compileParameters(Ticker, URL)
    path = r'/Users/Dewangtara/Desktop/Stock_AI'
    CSVstring = str(Ticker) + '_updated' + '.csv'
    pd.DataFrame(csvParameters).to_csv(os.path.join(path, CSVstring))


updateCSV_Parameters('NVDA',1045810)
