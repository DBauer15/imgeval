import numpy as np

def linear(img):
    return img

def reinhard(img):
    return img / (img + 1.0)

def exposure(img, exp):
    return 1.0 - np.exp(-img * exp)

def filmic(img):
    a = 2.51
    b = 0.03
    c = 2.43
    d = 0.59
    e = 0.14
    return np.clip((img * (a * img + b)) / (img * (c * img + d) + e), 0.0, 1.0)


def compute_imageop(imageop, image):
    if imageop["method"] == "linear":
        return linear(image[..., :3])
    if imageop["method"] == "reinhard":
        return reinhard(image[..., :3])
    if imageop["method"] == "exposure":
        return exposure(image[..., :3], imageop["exposure"])
    if imageop["method"] == "filmic":
        return filmic(image[..., :3])