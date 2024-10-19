import metrics.imgmap as imgmap
import numpy as np
import skimage.metrics as skm

def mae(img0, img1):
    return np.mean(imgmap.mae(img0, img1))

def mse(img0, img1):
    return np.mean(imgmap.mse(img0, img1))

def rmse(img0, img1):
    return np.mean(imgmap.rmse(img0, img1))

def smape(img0, img1):
    return np.mean(imgmap.rmse(img0, img1))

def psnr(img0, img1):
    range = np.max(img1) - np.min(img1)
    return skm.peak_signal_noise_ratio(img1, img0, data_range=range)
    
def ssim(img0, img1):
    range = np.max(img1) - np.min(img1)
    return skm.structural_similarity(img0, img1, data_range=range)

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
    elif (metric == "psnr"):
        return psnr(img0, img1)
    elif (metric == "ssim"):
        return ssim(img0, img1)
    elif (metric == "flip"):
        return flip(img0, img1)