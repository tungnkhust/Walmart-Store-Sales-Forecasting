from process_data import *
from utils import load_model
import os


def predict_submission(model_path, submission_path, test_path, feature_path, store_path):
    test_df = pd.read_csv(test_path)
    feature_df = pd.read_csv(feature_path)
    store_df = pd.read_csv(store_path)
    test_df = test_df.merge(feature_df, how='inner', on=['Store', 'Date', 'IsHoliday'])
    test_df = test_df.merge(store_df, how='inner', on='Store')
    test_df.to_csv('test_pro.csv', index=False)
    X_test = process_pipeline(test_df)

    model = load_model(model_path)
    print('predict submission')
    model.predict(X_test)

    ids = []
    for _, row in test_df.iterrows():
        store = row['Store']
        dept = row['Dept']
        date = row['Date']
        id = f'{store}_{dept}_{date}'
        ids.append(id)
    y_preds = model.predict(X_test).tolist()
    submission_df = pd.DataFrame({'ID': ids, 'Weekly_Sales': y_preds})
    submission_df.to_csv(submission_path, index=False)
    print('done')


def main():
    model_path = 'random_forest_model.sav'
    submission_path = 'submission/submission.csv'
    test_path = 'data/test.csv'
    feature_path = 'data/features.csv'
    store_path = 'data/stores.csv'

    if os.path.exists('submission') is False:
        os.mkdir('submission')
    predict_submission(
        model_path=model_path,
        submission_path=submission_path,
        test_path=test_path,
        feature_path=feature_path,
        store_path=store_path
    )


if __name__ == '__main__':
    main()