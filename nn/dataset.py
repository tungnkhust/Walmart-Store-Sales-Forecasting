from torch.utils.data import Dataset
import pandas as pd
import torch
from sklearn.preprocessing import LabelEncoder
from datetime import datetime


class TensorDataset(Dataset):
    def __init__(self, data_df: pd.DataFrame):
        self.data_df = data_df
        self.type_encoder = LabelEncoder()
        self.type_encoder.fit(data_df['Type'])
        self._process()

    def __len__(self):
        return len(self.data_df)

    def _convert_date(self, date):
        if date is None:
            return None
        date = datetime.strptime(date, '%Y-%m-%d')
        return date

    def _process(self):
        df = self.data_df
        df['Year'] = df['Date'].apply(lambda date: self._convert_date(date).year)
        df['Month'] = df['Date'].apply(lambda date: self._convert_date(date).month)
        df['Week'] = df['Date'].apply(lambda date: self._convert_date(date).isocalendar()[1])
        # -----
        df['MarkDown1'] = df['MarkDown1'].fillna(value=0.0)
        df['MarkDown2'] = df['MarkDown2'].fillna(value=0.0)
        df['MarkDown3'] = df['MarkDown3'].fillna(value=0.0)
        df['MarkDown4'] = df['MarkDown4'].fillna(value=0.0)
        df['MarkDown5'] = df['MarkDown5'].fillna(value=0.0)
        df['CPI'] = df['CPI'].fillna(value=0.0)
        df['Unemployment'] = df['Unemployment'].fillna(value=0.0)
        # df['Type'] = df['Type'].apply(lambda x: 3 if x == 'A' else (2 if x == 'B' else 1))
        self.data_df = df

    def __getitem__(self, index):
        row = self.data_df.iloc[index]
        store_id = row['Store']
        dept_id = row['Dept']

        feature_f = row[['IsHoliday', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment',
                      'Year', 'Month', 'Size']].tolist()
        markdown_f = row[['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']].tolist()
        store_type = row['Type']
        weekly_sales = row['Weekly_Sales']
        inputs = {
            'store_id': store_id,
            'dept_id': dept_id,
            'markdown_f': torch.tensor(markdown_f, dtype=torch.float32),
            'feature_f': torch.tensor(feature_f, dtype=torch.float32),
            'store_type': self.type_encoder.transform([store_type])[0],
        }
        output = weekly_sales
        return inputs, output
