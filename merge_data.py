import pandas as pd


features_df = pd.read_csv('data/features.csv')
train_df = pd.read_csv('data/train.csv')
store_df = pd.read_csv('data/stores.csv')

data_df = train_df.merge(features_df, how='inner', on=['Store', 'Date', 'IsHoliday'])
data_df = data_df.merge(store_df, how='inner', on='Store')
data_df.to_csv("data.csv", index=False)

num_samples = len(data_df)
n_train = int(0.8*num_samples)
train_df_split = data_df[:n_train]
test_df_split = data_df[n_train:]

train_df_split.to_csv('train_split.csv', index=False)
test_df_split.to_csv('test_split.csv', index=False)