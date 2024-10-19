import os
import pyexr

from util.crop import *

BASEDIR = './'

def make_dir(path):
    path = os.path.join(BASEDIR, path)
    if not os.path.exists(path):
        os.makedirs(path)

def load_img(path):
    with pyexr.open(path) as file:
        return file.get()

def load_group(group):
    group["baseline"]["data"] = load_img(group["baseline"]["path"])
    group["baseline"]["data_crops"] = []
    for crop in group["crops"]:
        group["baseline"]["data_crops"].append(crop_img(group["baseline"]["data"], crop["pos"], crop["size"]))

    for image in group["images"]:
        image["data"] = load_img(image["path"])
        image["data_crops"] = []

    for image in group["images"]:
        for crop in group["crops"]:
            image["data_crops"].append(crop_img(image["data"], crop["pos"], crop["size"]))

def save_img(img, path):
    pyexr.write(os.path.join(BASEDIR, path), img)

def save_group(group):
    imgpath = os.path.join(group["name"], group["baseline"]["name"])
    make_dir(imgpath)
    save_img(group["baseline"]["data"], os.path.join(imgpath, "image.exr"))
    for i, crop in enumerate(group["baseline"]["data_crops"]):
        croppath = os.path.join(imgpath, f"crop{i}")
        save_img(crop, f"{croppath}.exr")

    for image in group["images"]:
        imgpath = os.path.join(group["name"], image["name"])
        make_dir(imgpath)
        save_img(image["data"], os.path.join(imgpath, "image.exr"))
        for i, crop in enumerate(image["data_crops"]):
            croppath = os.path.join(imgpath, f"crop{i}")
            save_img(crop, f"{croppath}.exr")
        
        if "metrics" in image:
            for i, metric in enumerate(image["metrics"]):
                if (metric["type"] != "map"):
                    continue
                metricpath = os.path.join(imgpath, f"{metric['metric']}")
                save_img(metric["data"], f"{metricpath}.exr")