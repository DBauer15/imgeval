import os
import pyexr
import matplotlib.pyplot as plt

from imgops.crop import *

BASEDIR = './'
INDIR = './'

def make_dir(path):
    path = os.path.join(BASEDIR, path)
    if not os.path.exists(path):
        os.makedirs(path)

def load_img(path):
    try:
        with pyexr.open(path) as file:
            return file.get()
    except:
        with pyexr.open(os.path.abspath(os.path.join(INDIR, path))) as file:
            return file.get()

def load_group(group):
    group["baseline"]["data"] = load_img(group["baseline"]["path"])
    for image in group["images"]:
        image["data"] = load_img(image["path"])

def save_svg(svg, path):
    with open(os.path.join(BASEDIR, path), "w") as file:
        file.write(svg)

def save_pdf(pdf, path):
    with open(os.path.join(BASEDIR, path), "wb") as file:
        file.write(pdf)

def save_img(img, path):
    if path.endswith(".exr"):
        pyexr.write(os.path.join(BASEDIR, path), img)
    if path.endswith(".png") or path.endswith(".jpg"):
        plt.imsave(os.path.join(BASEDIR, path), img.clip(0, 1))

def save_group(group):
    imgpath = os.path.join(group["name"], group["baseline"]["name"])
    make_dir(imgpath)
    save_img(group["baseline"]["data"], os.path.join(imgpath, "image.exr"))

    if "imageops" in group["baseline"]:
        for i, op in enumerate(group["baseline"]["imageops"]):
            oppath = os.path.join(imgpath, f"op{i}_{op["type"]}")
            save_img(op["data"], f"{oppath}.exr")
            save_img(op["data"], f"{oppath}.png")

    for image in group["images"]:
        imgpath = os.path.join(group["name"], image["name"])
        make_dir(imgpath)
        save_img(image["data"], os.path.join(imgpath, "image.exr"))

        if "imageops" in image:
            for i, op in enumerate(image["imageops"]):
                oppath = os.path.join(imgpath, f"op{i}_{op["type"]}")
                save_img(op["data"], f"{oppath}.exr")
                save_img(op["data"], f"{oppath}.png")
        
        if "metrics" in image:
            for i, metric in enumerate(image["metrics"]):
                if (metric["type"] != "map"):
                    continue
                metricpath = os.path.join(imgpath, f"{metric['metric']}")
                save_img(metric["data"], f"{metricpath}.exr")

def save_layout(layout):
    layoutpath = os.path.join("layouts", layout["type"])
    make_dir(layoutpath)

    save_svg(layout["data"][0], os.path.join(layoutpath, f"{layout["name"]}.svg"))
    save_pdf(layout["data"][1], os.path.join(layoutpath, f"{layout["name"]}.pdf"))
