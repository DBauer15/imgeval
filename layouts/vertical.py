import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


import util.config

def get_figure_data():
    bytestream = io.StringIO()
    plt.savefig(bytestream, format="svg")
    return bytestream.getvalue()

# def calculate_layout_dimensions(images, crops, layout):
#     # TODO: User section padding and item padding
#     section_padding = layout.get("padding", {}).get("section", 0)
#     padding_top = layout.get("padding", {}).get("top", 0)
#     padding_bottom = layout.get("padding", {}).get("bottom", 0)
#     padding_left = layout.get("padding", {}).get("left", 0)
#     padding_right = layout.get("padding", {}).get("right", 0)

#     num_images = len(images)
#     if num_images == 0:
#         return [0, 0]

#     # get image dimensions
#     image_height, image_width, _ = images[0]["data"].shape

#     num_ops = len(crops[0])

#     # get imop dimensions
#     crop_height, crop_width = (0, 0)
#     for crop in crops[0]:
#         crop_height, crop_width = max(crop_height, crop["data"].shape[0]), max(crop_width, crop["data"].shape[1])
    
#     # scale op size to slice width 
#     slice_width = image_width / num_images
#     crop_scale = slice_width / crop_width
#     crop_height, crop_width = crop_height*crop_scale, crop_width*crop_scale

#     layout_height = image_height + section_padding + num_ops*crop_height + padding_top + padding_bottom
#     layout_width = image_width + padding_left + padding_right

#     layout_dims = [ layout_height, layout_width, image_height, image_width, crop_height, crop_width ]
#     height_ratios = [ image_width, section_padding ]+ [ crop_height ] * len(crops[0])
#     padding = [ padding_top, padding_bottom, padding_left, padding_right ]

#     return layout_dims, height_ratios, padding

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
        # slice_img = image["data"][:, start:end]

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


# def plot_dividers(images, fig, layout_dims):
#     size = 1/len(images)
#     height = images[0]["data"].shape[0] / layout_dims[0]
#     for i in range(len(images)-1):
#         rect = patches.Rectangle(
#             ((i+1)*size-0.005, 1),
#             0.01, -height,
#             linewidth=0, edgecolor="w", facecolor="w", transform=fig.transFigure)

#         fig.patches.append(rect)

# def plot_crop_bboxes(crops, fig, layout_dims, padding):
#     for crop in crops:
#         # See https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Rectangle.html 
#         pos = crop["pos"][0] / layout_dims[1], 1.0 - (crop["pos"][1] / layout_dims[0])
#         size = crop["size"][0] / layout_dims[1], crop["size"][1] / layout_dims[0] 
#         rect = patches.Rectangle(
#             (pos[0], pos[1]), 
#             size[0], -size[1],
#             linewidth=2, edgecolor=crop.get("color", "r"), facecolor='none', transform=fig.transFigure)

#         # Add the rectangle to the figure
#         fig.patches.append(rect)

def compute_layout(layout, config):
    group = util.config.find_group(config, layout["groups"][0])
    images =  [image for image in group["images"]] + [group["baseline"]]
    crops = [[op for op in image["imageops"] if op["type"] == "crop"] for image in group["images"]] + [[op for op in group["baseline"]["imageops"] if op["type"] == "crop"]]
    # layout_dims, height_ratios, padding = calculate_layout_dimensions(images, crops, layout)

    # fig, axs = plt.subplots(
    #     ncols=len(images), 
    #     nrows=1+1+len(crops[0]), # Images + Spacing + Crops
    #     figsize=(layout_dims[1]/100, layout_dims[0]/100),
    #     gridspec_kw={
    #         'height_ratios': height_ratios
    #         }
    # )
    # for ax in axs.flatten():
    #     ax.axis("off")

    fig = plt.figure(1,
                     figsize=layout["figsize"],
                     layout="constrained"
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
    # plot_dividers(images, fig, layout_dims)
    for i, crop_fig in enumerate(crop_fgs):
        plot_crops(crops[i], crop_fig)
    # plot_crop_bboxes(crops[-1], fig)
    plot_crops_metrics([image["metrics"] for image in images], crop_metrics_fig)

    # plt.subplots_adjust(left=padding[2]/100, right=1-(padding[3]/100), top=1-(padding[0]/100), bottom=padding[1]/100, wspace=0, hspace=0)

    data = get_figure_data()
    plt.savefig("test.png")
    plt.clf()
    return data