import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


import util.config

def plot_slices_titles(titles, fig):
    axs = fig.subplots(ncols=len(titles))

    for ax, title in zip(axs, titles):
        ax.axis("off")
        ax.text(0.5, 0, title, horizontalalignment="center", verticalalignment="top")

def plot_slices(images, crops, fig):
    n = len(images)
    _, image_width, _ = images[0]["data"].shape
    ax = fig.subplots(1)

    slice_img = images[0]["data"].copy()
    
    # Loop through each slice and plot it
    for i, image in enumerate(images):
        # Determine the slice for the current segment (each taking 1/n width of the image)
        start = int(np.ceil(i * image_width / n))
        end = int((i + 1) * image_width / n)

        slice_img[:, start:end] = image["data"][:, start:end]
        
    ax.axis("off")
    ax.imshow(slice_img, interpolation="none", aspect="equal")

    # Plot dividers between slices
    for i in range(len(images)):
        width = 0.01
        rect = patches.Rectangle(
            xy = ((i+1)/len(images)-(width/2.0), 0.0),
            width = width, height = 1.0,
            linewidth = 5,
            edgecolor = "none", facecolor = "w",
            transform = ax.transAxes
        )
        ax.add_patch(rect)
    
    # Plot crop bounding boxes
    image_height, image_width, _ = images[0]["data"].shape
    for crop in crops[0]:
        pos = (
            crop["pos"][0] / image_width,
            1.0 - crop["pos"][1] / image_height
        )
        size = (
            crop["size"][0] / image_width,
            -crop["size"][1] / image_height,
        )
        rect = patches.Rectangle(
            xy = pos,
            width = size[0], height=size[1],
            linewidth = 3,
            edgecolor = crop.get("color", "r"), facecolor = "none",
            transform = ax.transAxes
        )
        fig.patches.append(rect)


def plot_crops(crops, fig):
    axs = fig.subplots(nrows=len(crops))
    for crop, ax in zip(crops, axs):
        ax.axis("off")

        # plot image
        ax.imshow(crop["data"], interpolation="none")

        # plot crop border
        rect = patches.Rectangle(
            xy = (0, 0), 
            height = 1.0, width = 1.0,
            linewidth = 5, 
            edgecolor = crop.get("color", "r"), facecolor="none", 
            transform = ax.transAxes
        )
        ax.add_patch(rect)

def plot_crops_metrics(metrics, fig):
    axs = fig.subplots(ncols=len(metrics))
    for ax, metric_group in zip(axs, metrics):
        ax.axis("off")
        text = ""
        for metric in metric_group:
            if metric["type"] != "aggregate": continue
            text += f"{metric['metric']}: {metric['data']:.3f}\n" 
        ax.text(0, 1, text, horizontalalignment="left", verticalalignment="top")

def compute_layout(layout, config):
    group = util.config.find_group(config, layout["groups"][0])
    images =  [image for image in group["images"]] + [group["baseline"]]
    crops = [[op for op in image["imageops"] if op["type"] == "crop"] for image in group["images"]] + [[op for op in group["baseline"]["imageops"] if op["type"] == "crop"]]

    fig = plt.figure(1,
                     figsize=layout["figsize"],
                     layout="constrained",
                     clear=True
    )
    fgs = fig.subfigures(nrows=4,
                         ncols=1,
                         height_ratios=[0.1, 1, 1.2, 0.1],
    )

    crop_fgs = fgs[2].subfigures(nrows=1,
                                 ncols=len(images),
    )
    crop_metrics_fig = fgs[3]

    plot_slices_titles([image["name"] for image in images], fgs[0])
    plot_slices(images, crops, fgs[1])
    for i, crop_fig in enumerate(crop_fgs):
        plot_crops(crops[i], crop_fig)
    plot_crops_metrics([image["metrics"] for image in images], crop_metrics_fig)

    data_svg = util.config.get_figure_data("svg")
    data_pdf = util.config.get_figure_data("pdf")
    plt.clf()
    plt.close()
    return [ data_svg, data_pdf ]