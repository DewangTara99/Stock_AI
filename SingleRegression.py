import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def InputPrediction(ticker, date):
    def CSV_to_DF(ticker):
        # Importing the dataset
        file = str(ticker) + '_updated.csv'
        datasets = pd.read_csv(file)
        return datasets

    dataset = CSV_to_DF(str(ticker))

    def Equation(data, n):
        # Determine Inputs and Output
        y = data.iloc[:, n].values
        X = data.iloc[:, 0].values
        # Splitting the Dataset into the Training Set and Test Set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 0)
        X_train= X_train.reshape(-1, 1)
        y_train= y_train.reshape(-1, 1)
        X_test = X_test.reshape(-1, 1)

        regressor = LinearRegression()
        regressor.fit(X_train, y_train)

        y_pred = regressor.predict(X_test)

        r = [regressor.coef_, regressor.intercept_]
        return r

    def predict(set, input):
        predicted = []
        for i in range(2,20):
            coeff = Equation(set, i)[0]
            intercept = Equation(set, i)[1]
            p = coeff * input + intercept
            predicted += [float(p)]
        return predicted

    return predict(dataset, date)



