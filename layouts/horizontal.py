import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import util.config

def get_figure_data():
    bytestream = io.StringIO()
    plt.savefig(bytestream, format="svg")
    return bytestream.getvalue()

# def get_image_data(image):
#     img = [op["data"] for op in image["imageops"] if op["type"] == "tonemap"]
#     if len(img) > 0:
#         img = img[0]
#     else:
#         img = image["data"]
#     return img


# def calculate_layout_dimensions(image, crops, layout):
#     # TODO: User section padding and item padding
#     section_padding = layout["padding"].get("section", 0)
#     padding_top = layout["padding"].get("top", 0)
#     padding_bottom = layout["padding"].get("bottom", 0)
#     padding_left = layout["padding"].get("left", 0)
#     padding_right = layout["padding"].get("right", 0)

#     num_crops = len(crops[0])
#     crop_height, crop_width = (0, 0)
#     for crop in crops:
#         crop_height = max(crop_height, crop[0]["data"].shape[0])
#         crop_width = max(crop_width, crop[0]["data"].shape[1])

#     image_height, image_width, _ = image["data"].shape
#     width_ratios = [ image_width ] + [ image_width ]
#     print(width_ratios, image_width, crop_width)

#     crop_scale = crop_width / (crop_width * len(crops[0]))
#     crop_height, crop_width = crop_height * crop_scale, crop_width * crop_scale

#     layout_height = image["data"].shape[0]
#     layout_width = image["data"].shape[1] + ( section_padding + crop_width ) * num_crops
    
#     layout_dims = [ layout_height, layout_width ]


#     padding = [ padding_top, padding_bottom, padding_left, padding_right ]

#     return layout_dims, width_ratios, padding

def plot_reference(image, crops, fig, title):
    ax = fig.subplots(1)
    ax.set_ylabel(title, fontsize="12")
    ax.set_yticks([])
    ax.set_xticks([])

    # plot image
    ax.imshow(image["data"], interpolation="none", aspect="equal")

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
        ax.imshow(crop["data"], interpolation="none", aspect="equal")

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

    fig = plt.figure(1,
            figsize=layout["figsize"],
            layout="constrained"
    )
    fgs = fig.subfigures(nrows=3,
                         ncols=2,
                         height_ratios=[0.05, 1, 0.1],
                         width_ratios=[1, 1.8]
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
    plot_crops_titles([image["name"] for image in images], crop_title_fig)
    plot_crops_metrics([image["metrics"] for image in images], crop_metrics_fig)

    # plt.subplots_adjust(left=padding[2]/100, right=1-(padding[3]/100), top=1-(padding[0]/100), bottom=padding[1]/100, wspace=0, hspace=0)
    data = get_figure_data()
    plt.clf()
    return data
