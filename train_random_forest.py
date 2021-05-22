import pandas as pd
import pickle
from process_data import *
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.svm import LinearSVR
from sklearn.model_selection import train_test_split
from metrics import weighted_mean_absolute_error


def gridsearch_train(X_train, y_train, X_test=None, y_test=None, weight=None):
    parameters = {
            'n_estimators': [56, 58, 60],
            'max_depth': [25, 27],
            'min_samples_split': [2, 3],
            'min_samples_leaf': [1, 2, 3],
            'max_features': [4, 5, 6]
        }

    model = RandomForestRegressor()
    
    model = GridSearchCV(model, parameters, n_jobs=7)
    print('----------------training----------------')

    model.fit(X=X_train, y=y_train)
    print('----------------train-done----------------')

    # evaluate
    y_pred = model.predict(X=X_test)
    mse = mean_squared_error(y_test, y_pred, sample_weight=weight)
    rmse = np.sqrt(mse)
    wmae = weighted_mean_absolute_error(y_test, y_pred, weight)
    print("WMAE: ", wmae)
    print("RMSE: ", rmse)

    print(model.best_params_)
    return model


def train(X_train, y_train, X_test=None, y_test=None, weight=None):
    # model
    model = RandomForestRegressor(
        n_estimators=58,
        max_depth=27,
        max_features=6,
        min_samples_split=3,
        min_samples_leaf=1
    )
    print('Training------------------------------>')

    print(X_train.shape)
    model.fit(X=X_train, y=y_train)


    # evaluate
    y_pred = model.predict(X=X_test)
    mse = mean_squared_error(y_test, y_pred, sample_weight=weight)
    rmse = np.sqrt(mse)
    wmae = weighted_mean_absolute_error(y_test, y_pred, weight)
    print("WMAE: ", wmae)
    print("RMSE: ", rmse)
    return model


def main():
    data_df = pd.read_csv('data/data.csv')
    train_df, test_df = train_test_split(data_df, test_size=0.2)

    y_train = train_df['Weekly_Sales'].to_numpy()
    X_train = process_pipeline(train_df.drop(columns=['Weekly_Sales']))

    y_test = test_df['Weekly_Sales'].to_numpy()
    X_test = process_pipeline(test_df.drop(columns=['Weekly_Sales']))

    weight = get_weight(test_df)['weight'].to_numpy()
    model = train(X_train, y_train, X_test, y_test, weight)
    filename = 'models/random_forest_model.sav'
    pickle.dump(model, open(filename, 'wb'))


if __name__ == '__main__':
    main()