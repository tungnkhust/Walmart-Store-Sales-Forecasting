import pandas as pd
import pickle
from process import *
from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVR
from sklearn.model_selection import train_test_split
from metrics import weighted_mean_absolute_error


def train_linear_regression(X_train, y_train, X_test=None, y_test=None, weight=None):
    # model
    model = LinearRegression()

    print('Num train samples: ', X_train.shape[0])
    print('Num features     : ', X_train.shape[1])
    print('Training------------------------------>')
    model.fit(X=X_train, y=y_train)

    # evaluate on test dataset
    if X_test is not None:
        print('Num train samples: ', X_test.shape[0])
        print('Num features     : ', X_test.shape[1])
        y_pred = model.predict(X=X_test)
        mse = mean_squared_error(y_test, y_pred, sample_weight=weight)
        rmse = np.sqrt(mse)
        wmae = weighted_mean_absolute_error(y_test, y_pred, weight)
        print("WMAE: ", wmae)
        print("RMSE: ", rmse)
    return model


def main():
    data_df = pd.read_csv('data.csv')
    train_df, test_df = train_test_split(data_df, test_size=0.2)

    y_train = train_df['Weekly_Sales'].to_numpy()
    X_train = process_pipeline(train_df.drop(columns=['Weekly_Sales']))

    y_test = test_df['Weekly_Sales'].to_numpy()
    X_test = process_pipeline(test_df.drop(columns=['Weekly_Sales']))

    weight = get_weight(test_df)['weight'].to_numpy()

    # train model
    model = train_linear_regression(X_train, y_train, X_test, y_test, weight)
    filename = 'linear_regression_model.sav'
    pickle.dump(model, open(filename, 'wb'))


if __name__ == '__main__':
    main()