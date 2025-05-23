import io
import imgops.tonemap as tonemap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import util.config

def plot_reference(image, crops, fig, title):
    ax = fig.subplots(1)
    ax.set_ylabel(title, fontsize="12")
    ax.set_yticks([])
    ax.set_xticks([])

    # plot image
    ax.imshow(tonemap.exposure(image["data"][..., :3], 2.2), interpolation="none", aspect="equal", vmin=0.0, vmax=1.0)

    # plot crop bboxes
    image_height, image_width, _ = image["data"].shape
    for crop in crops:
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
    axs = fig.subplots(1, len(crops))
    for ax, crop in zip(axs, crops):
        ax.axis("off")

        # plot image
        ax.imshow(tonemap.exposure(crop["data"][..., :3], 2.2), interpolation="none", aspect="equal", vmin=0.0, vmax=1.0)

        # plot crop border
        rect = patches.Rectangle(
            xy = (0, 0),
            height = 1.0, width = 1.0,
            linewidth = 5,
            edgecolor = crop.get("color", "r"), facecolor = "none",
            transform = ax.transAxes
        )
        ax.add_patch(rect)

def plot_crops_titles(titles, fig):
    axs = fig.subplots(1, len(titles))
    for ax, title in zip(axs, titles):
        ax.axis("off")
        ax.text(0.5, 1, title, horizontalalignment="center", verticalalignment="top")


def plot_crops_metrics(metrics, fig):
    axs = fig.subplots(1, len(metrics))
    for ax, metric_group in zip(axs, metrics):
        ax.axis("off")
        text = ""
        for metric in metric_group:
            if metric["type"] != "aggregate": continue
            text += f"{metric['metric']}: {metric['data']:.3f}\n" 
        ax.text(0.1, 1, text, horizontalalignment="left", verticalalignment="top")

def compute_layout(layout, config):
    group = util.config.find_group(config, layout["groups"][0])
    images = group["images"] + [group["baseline"]]
    crops = [([op for op in image["imageops"] if op["type"] == "crop"]) for image in images]

    height_ratios = [0.05, 1, 0.1]
    if "height_ratios" in layout:
        height_ratios = layout["height_ratios"]

    width_ratios = [1, 0.6]
    if "width_ratios" in layout:
        width_ratios = layout["width_ratios"]

    fig = plt.figure(1,
            figsize=layout["figsize"],
            layout="constrained",
            clear=True
    )
    fgs = fig.subfigures(nrows=3,
                         ncols=2,
                         height_ratios=height_ratios,
                         width_ratios=width_ratios
                         )
    crop_title_fig = fgs[0][1].subfigures(nrows=1,
                                         ncols=1)
    crop_fgs = fgs[1][1].subfigures(nrows=len(crops[0]),
                                    ncols=1)
    crop_metrics_fig = fgs[2][1].subfigures(nrows=1,
                                           ncols=1)

    plot_reference(group["baseline"], crops[0], fgs[1][0], group["name"])
    for i, fig in enumerate(crop_fgs):
        plot_crops([crop[i] for crop in crops], fig)

    if not layout.get("hide_titles", False):
        plot_crops_titles([image["name"] for image in images], crop_title_fig)
    plot_crops_metrics([image["metrics"] for image in images], crop_metrics_fig)

    data_svg = util.config.get_figure_data("svg")
    data_pdf = util.config.get_figure_data("pdf")
    plt.clf()
    plt.close()
    return [ data_svg, data_pdf ]
