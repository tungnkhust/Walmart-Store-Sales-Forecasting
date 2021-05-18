import numpy as np


def weighted_mean_absolute_error(y_true, y_pred, weight=None):
    if weight is None:
        weight = np.ones(y_true.shape[0])
    weight_sum = weight.sum()
    wmea = 1/weight_sum * (weight*np.abs(y_true-y_pred)).sum()
    return wmea