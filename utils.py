import pickle


def load_model(model_path):
    # load model pickle)
    model = pickle.load(open(model_path, 'rb'))
    return model


def create_id(df):
    # ceate id to submit on kaggle
    ids = []
    for _, row in df.iterrows():
        store = row['Store']
        dept = row['Dept']
        date = row['Date']
        id = f'{store}_{dept}_{date}'
        ids.append(id)
    df['ID'] = ids
    return df
