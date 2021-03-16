import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def prediction(ticker, inputs, s):
    def CSV_to_DF(ticker):
        # Importing the dataset
        file = str(ticker) + '_updated.csv'
        datasets = pd.read_csv(file)
        return datasets

    # Shifts Open prices down the dataframe column by 's' days
    dataset = CSV_to_DF(str(ticker))
    dataset['0'] = dataset['0'].shift(s)
    SIZE = len(dataset) - s
    dataset = dataset.tail(SIZE)

    def Equation(data):
        # Determine Inputs and Output
        y = data.iloc[:, 1].values
        X = data.iloc[:, 2:].values
        # Splitting the Dataset into the Training Set and Test Set
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)

        from sklearn.linear_model import LinearRegression
        regressor = LinearRegression()
        regressor.fit(X_train, y_train)

        y_pred = regressor.predict(X_test)
        np.set_printoptions(precision=2)

        r = [regressor.coef_, regressor.intercept_]
        return r

    def predict(set, input):
        coeff = Equation(set)[0]
        intercept = Equation(set)[1]
        predicted = 0
        for i in range(len(coeff)):
            predicted += coeff[i] * input[i]
        predicted += intercept
        return predicted

    return predict(dataset, inputs)
