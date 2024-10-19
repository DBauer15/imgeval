import numpy as np

def mae(img0, img1):
    return np.mean(np.abs(img0 - img1), axis=-1)

def mse(img0, img1):
    return np.mean((img0 - img1)**2, axis=-1)

def rmse(img0, img1):
    # from: https://github.com/tunabrain/tungsten/issues/57
    # sqr(imgA[i*3 + c] - imgB[i*3 + c])/(imgA[i*3 + c] + 1e-3f);
    return np.mean(((img0 - img1)**2) / ((img1 + 1e-3)**2), axis=-1)

def smape(img0, img1):
    # SMAPE = 100/n * sum(abs(img0 - img1) / ((abs(img0) + abs(img1)))/2))
    return np.mean(np.abs(img0 - img1) / ((np.abs(img1) + np.abs(img0)) / 2 + 1e-3), axis=-1)

def flip(img0, img1):
    raise "FLIP not implemented"


def compute_metric(metric, img0, img1):
    if (metric == "mae"):
        return mae(img0, img1)
    elif (metric == "mse"):
        return mse(img0, img1)
    elif (metric == "rmse"):
        return rmse(img0, img1)
    elif (metric == "smape"):
        return smape(img0, img1)
    elif (metric == "flip"):
        return flip(img0, img1)