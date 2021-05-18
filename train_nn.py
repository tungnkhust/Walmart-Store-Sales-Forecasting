import numpy as np
import pandas as pd
from torch.utils.data import DataLoader
from nn.model import NNRegressor
from torch.optim import Adam, SGD, RMSprop
import torch
import torch.nn as nn
from nn.dataset import TensorDataset
from metrics import weighted_mean_absolute_error
data_df = pd.read_csv('/home/tungnk/Desktop/learning/20202/BA/project/data.csv')

dataset = TensorDataset(data_df=data_df)

model = NNRegressor(
    embed_dim=10,
    n_store=46,
    n_department=100,
    n_feat=13,
    n_type=3,
    hidden_dim1=100,
    hidden_dim2=50
)

optimizer = Adam(params=model.parameters(), lr=1)

n_epochs = 10

for epoch in range(n_epochs):
    train_loader = DataLoader(dataset, batch_size=64)

    y_preds = []
    y_trues = []
    for inputs, output_true in train_loader:
        output_pred = model(inputs)
        y_preds.append(output_pred.detach().numpy())
        y_trues.append(output_true.detach().numpy())
        loss = torch.nn.L1Loss()(output_true, output_pred)
        loss.backward()
        optimizer.step()
    y_preds_ = np.concatenate(y_preds, dim=-1)
    y_trues_ = np.concatenate(y_trues, dim=-1)

    wmae = weighted_mean_absolute_error(y_trues_, y_preds_)
    print("WMAE", wmae)