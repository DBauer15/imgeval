import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


import util.config

def get_figure_data():
    bytestream = io.StringIO()
    plt.savefig(bytestream, format="svg")
    return bytestream.getvalue()

def calculate_layout_dimensions(images, crops, layout):
    # TODO: User section padding and item padding
    section_padding = layout["padding"].get("section", 0)
    item_padding = layout["padding"].get("item", 0)

    num_images = len(images)
    if num_images == 0:
        return [0, 0]

    # get image dimensions
    image_height, image_width, _ = images[0].shape

    num_ops = len(crops[0])

    # get imop dimensions
    crop_height, crop_width = (0, 0)
    for crop in crops[0]:
        crop_height, crop_width = max(crop_height, crop["data"].shape[0]), max(crop_width, crop["data"].shape[1])
    
    # scale op size to slice width 
    slice_width = image_width / num_images
    crop_scale = slice_width / crop_width
    crop_height, crop_width = crop_height*crop_scale, crop_width*crop_scale

    layout_height = image_height + section_padding + num_ops*crop_height
    layout_width = image_width

    return [ layout_height, layout_width, image_height, image_width, crop_height, crop_width ], [ image_width, section_padding ] + [ crop_height ] * len(crops[0])

def plot_slices_horizontally(images, axs):
    n = len(images)
    _, image_width, _ = images[0].shape
    
    # Loop through each slice and plot it
    for i, (image, ax) in enumerate(zip(images, axs)):
        # Determine the slice for the current segment (each taking 1/n width of the image)
        start = int(np.ceil(i * image_width / n))
        end = int((i + 1) * image_width / n)
        slice_img = image[:, start:end]
        
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        print(slice_img.shape)

        ax.imshow(slice_img, aspect='equal')

def plot_crops_vertically(crops, axs):
    for i, (crop, ax) in enumerate(zip(crops, axs)):
        ax.imshow(crop["data"])
        rect = patches.Rectangle(
            (0.01, 0.01), 
            0.975, 0.975,
            linewidth=2, edgecolor=crop.get("color", "r"), facecolor="none", transform=ax.transAxes)
        ax.add_patch(rect)

def plot_dividers(images, fig, layout_dims):
    size = 1/len(images)
    height = images[0].shape[0] / layout_dims[0]
    for i in range(len(images)-1):
        rect = patches.Rectangle(
            ((i+1)*size-0.005, 1),
            0.01, -height,
            linewidth=0, edgecolor="w", facecolor="w", transform=fig.transFigure)

        fig.patches.append(rect)

def plot_crop_bboxes(crops, fig, layout_dims):
    for crop in crops:
        # See https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Rectangle.html 
        pos = crop["pos"][0] / layout_dims[1], 1.0 - (crop["pos"][1] / layout_dims[0])
        size = crop["size"][0] / layout_dims[1], crop["size"][1] / layout_dims[0]
        print(pos, size)
        rect = patches.Rectangle(
            (pos[0], pos[1]), 
            size[0], -size[1],
            linewidth=2, edgecolor=crop.get("color", "r"), facecolor='none', transform=fig.transFigure)

        # Add the rectangle to the figure
        fig.patches.append(rect)

def compute_layout(layout, config):

    group = util.config.find_group(config, layout["groups"][0])
    images =  [image["data"] for image in group["images"]] + [group["baseline"]["data"]]
    crops = [[op for op in image["imageops"] if op["type"] == "crop"] for image in group["images"]] + [[op for op in group["baseline"]["imageops"] if op["type"] == "crop"]]
    layout_dims, height_ratios = calculate_layout_dimensions(images, crops, layout)

    fig, axs = plt.subplots(
        ncols=len(images), 
        nrows=1+1+len(crops[0]), # Images + Spacing + Crops
        figsize=(layout_dims[1]/100, layout_dims[0]/100),
        gridspec_kw={
            'height_ratios': height_ratios
            }
    )
    for ax in axs.flatten():
        ax.axis("off")

    print(axs.shape)
    plot_slices_horizontally(images, axs[0])
    plot_dividers(images, fig, layout_dims)
    for i, op in enumerate(crops):
        plot_crops_vertically(op, 
            [ax[i] for ax in axs[2:]]
        )
    plot_crop_bboxes(crops[-1], fig, layout_dims)

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    plt.savefig('test.png')

    return get_figure_data()