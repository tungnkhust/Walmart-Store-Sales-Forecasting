import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


def convert_datetime(date_s):
    # y, m, d = date_s.split('-')
    time = datetime.fromisoformat(date_s)
    return time


train_df = pd.read_csv('../data/train.csv')
feat_df = pd.read_csv('../data/features.csv')


data_df = pd.merge(train_df, feat_df, left_on=['Store', 'Date', "IsHoliday"], right_on=['Store', 'Date', "IsHoliday"])

data_df.to_csv('data.csv', index=False)


