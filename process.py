import pandas as pd
import math
from sklearn.preprocessing import LabelBinarizer
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import LinearSVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import datetime


def convert_date(date):
    if date is None:
        return None
    date = datetime.strptime(date, '%Y-%m-%d')
    return date


def get_holiday(date):
    holidays = {
        "2010-02-12": "super_bowl",
        "2011-02-11": "super_bowl",
        "2012-02-10": "super_bowl",
        "2013-02-08": "super_bowl",
        "2010-09-10": "labor_day",
        "2011-09-09": "labor_day",
        "2012-09-07": "labor_day",
        "2013-09-06": "labor_day",
        "2010-11-26": "thanksgiving",
        "2011-11-25": "thanksgiving",
        "2012-11-23": "thanksgiving",
        "2013-11-29": "thanksgiving",
        "2010-12-31": "christmas",
        "2011-12-30": "christmas",
        "2012-12-28": "christmas",
        "2013-12-27": "christmas"
    }
    if date not in holidays:
        return 'not_holiday'
    return holidays[date]


def process_date(df):
    df['Year'] = df['Date'].apply(lambda date: convert_date(date).year)
    df['Month'] = df['Date'].apply(lambda date: convert_date(date).month)
    df['Week'] = df['Date'].apply(lambda date: convert_date(date).isocalendar()[1])
    df['Holiday'] = df['Date'].apply(lambda date: get_holiday(date))
    return df


def fill_na(df: pd.DataFrame):
    df['MarkDown1'] = df['MarkDown1'].fillna(value=0.0)
    df['MarkDown2'] = df['MarkDown2'].fillna(value=0.0)
    df['MarkDown3'] = df['MarkDown3'].fillna(value=0.0)
    df['MarkDown4'] = df['MarkDown4'].fillna(value=0.0)
    df['MarkDown5'] = df['MarkDown5'].fillna(value=0.0)
    df['CPI'] = df['CPI'].fillna(value=0.0)
    df['Unemployment'] = df['Unemployment'].fillna(value=0.0)
    return df


def process_markdown_na(df: pd.DataFrame):
    df['MarkDown1_na'] = df['MarkDown1'].apply(lambda x: 1 if math.isnan(x) else 0)
    df['MarkDown2_na'] = df['MarkDown2'].apply(lambda x: 1 if math.isnan(x) else 0)
    df['MarkDown3_na'] = df['MarkDown3'].apply(lambda x: 1 if math.isnan(x) else 0)
    df['MarkDown4_na'] = df['MarkDown4'].apply(lambda x: 1 if math.isnan(x) else 0)
    df['MarkDown5_na'] = df['MarkDown5'].apply(lambda x: 1 if math.isnan(x) else 0)
    df['CPI_na'] = df['CPI'].apply(lambda x: 1 if math.isnan(x) else 0)
    df['Unemployment_na'] = df['Unemployment'].apply(lambda x: 1 if math.isnan(x) else 0)
    return df


def process_num_type(df: pd.DataFrame):
    df['MarkDown1'] = df['MarkDown1'].apply(lambda x: x/1000)
    df['MarkDown2'] = df['MarkDown2'].apply(lambda x: x / 1000)
    df['MarkDown3'] = df['MarkDown3'].apply(lambda x: x / 1000)
    df['MarkDown4'] = df['MarkDown4'].apply(lambda x: x / 1000)
    df['MarkDown5'] = df['MarkDown5'].apply(lambda x: x / 1000)
    df['Size'] = df['Size'].apply(lambda x: x / 1000)
    return df


def process_category(df: pd.DataFrame, cols=['Type', 'Holiday']):
    cates = {
        "Type": [
            "A",
            "B",
            "C"
        ],
        "Holiday": [
            "super_bowl",
            "labor_day",
            "thanksgiving",
            "christmas",
            "not_holiday"
        ]
    }
    x = []
    for col in cols:
        cate = df[col].tolist()
        if col in cates:
            cate.extend(cates[col])
        encoder = LabelBinarizer().fit(cate)
        one_hot = encoder.transform(df[col].tolist())
        x.append(one_hot)

    one_hot_vector = np.concatenate(x, axis=-1)
    return one_hot_vector


def get_weight(df):
    df['weight'] = df['IsHoliday'].apply(lambda x: 5 if x is True else 1)

    return df


def convert_type(x):
    type_ = {
        'A': 3,
        'B': 2,
        'C': 1
    }
    return type_[x]


def process_df(df: pd.DataFrame):
    # -----
    df['Year'] = df['Date'].apply(lambda date: convert_date(date).year)
    df['Month'] = df['Date'].apply(lambda date: convert_date(date).month)
    df['Week'] = df['Date'].apply(lambda date: convert_date(date).isocalendar()[1])
    df['Holiday'] = df['Date'].apply(lambda date: get_holiday(date))

    # -----
    df['MarkDown1'] = df['MarkDown1'].fillna(value=0.0)
    df['MarkDown2'] = df['MarkDown2'].fillna(value=0.0)
    df['MarkDown3'] = df['MarkDown3'].fillna(value=0.0)
    df['MarkDown4'] = df['MarkDown4'].fillna(value=0.0)
    df['MarkDown5'] = df['MarkDown5'].fillna(value=0.0)
    df['CPI'] = df['CPI'].fillna(value=0.0)
    df['Unemployment'] = df['Unemployment'].fillna(value=0.0)

    # -----
    type_ = {
        'A': 3,
        'B': 2,
        'C': 1
    }

    df['Type_'] = df['Type'].apply(lambda x: type_[x])
    # -----
    return df


def process_pipeline(df: pd.DataFrame):
    df = process_date(df)
    # df = fill_na(df)
    # df = process_markdown_na(df)

    df['Type_'] = df['Type'].apply(lambda x: convert_type(x))
    df_numeric = df[['Store', 'Dept', 'IsHoliday', 'Week', 'Size', 'Year', 'Type_']]
    x1 = df_numeric.to_numpy()

    return x1