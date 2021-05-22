import pandas as pd
import os
from process_data import convert_type, convert_date, process_pipeline
from utils import create_id, load_model
from flask import Flask, jsonify, request
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

model = load_model('models/')

test_path = 'data/test.csv'
feature_path = 'data/features.csv'
store_path = 'data/stores.csv'
test_process_path = 'data/test_pro.csv'

if os.path.exists(test_process_path):
    test_df = pd.read_csv(test_process_path)
else:
    test_df = pd.read_csv(test_path)
    feature_df = pd.read_csv(feature_path)
    store_df = pd.read_csv(store_path)
    test_df = test_df.merge(feature_df, how='inner', on=['Store', 'Date', 'IsHoliday'])
    test_df = test_df.merge(store_df, how='inner', on='Store')
    test_df.to_csv('data/test_pro.csv', index=False)

test_df = create_id(test_df)


def get_predict(sample):
    df = test_df.loc[test_df['ID'] == f'{sample["Store"]}_{sample["Dept"]}']
    x = process_pipeline(df)
    y = model.predict(x)
    return {
        "Date": df["Date"],
        "Weekly_Sales": y[0]
    }


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        sample = request.json
        res = get_predict(sample)
        logging.info(f'Res:  {res}')
        return jsonify(res)


if __name__ == '__main__':

    app.run()
    #
    # sample = {
    #     "Store": 1,
    #     "Dept": 1,
    #     "Date": '2012-11-02'
    # }
