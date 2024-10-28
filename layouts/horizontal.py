import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import util.config

def get_figure_data():
    bytestream = io.StringIO()
    plt.savefig(bytestream, format="svg")
    return bytestream.getvalue()

def calculate_layout_dimensions(image, crops, layout):
    # TODO: User section padding and item padding
    section_padding = layout["padding"].get("section", 0)
    padding_top = layout["padding"].get("top", 0)
    padding_bottom = layout["padding"].get("bottom", 0)
    padding_left = layout["padding"].get("left", 0)
    padding_right = layout["padding"].get("right", 0)

    num_crops = len(crops)
    crop_height, crop_width = (0, 0)
    for crop in crops:
        crop_height = max(crop_height, crop["data"].shape[0])
        crop_width = max(crop_width, crop["data"].shape[1])

    image_height, image_width, _ = image["data"].shape

    layout_height = image["data"].shape[0]
    layout_width = image["data"].shape[1] + ( section_padding + crop_width ) * num_crops
    
    layout_dims = [ layout_height, layout_width ]

    width_ratios = [ image_width ] + [ section_padding, crop_width ] * num_crops

    padding = [ padding_top, padding_bottom, padding_left, padding_right ]

    return layout_dims, width_ratios, padding

def plot_reference(image, ax):
    ax.imshow(image["data"], interpolation="none", aspect="equal")

def compute_layout(layout, config):
    group = util.config.find_group(config, layout["groups"][0])
    image = group["baseline"]
    crops = [([op for op in image["imageops"] if op["type"] == "crop"])[0] for image in group["images"]]
    layout_dims, width_ratios, padding = calculate_layout_dimensions(image, crops, layout)

    fig, axs = plt.subplots(
        ncols=1+2*len(crops),
        nrows=1,
        figsize=(layout_dims[1]/100, layout_dims[0]/100),
        gridspec_kw = {
            'width_ratios': width_ratios
        }
    )
    for ax in axs.flatten():
        ax.axis("off")

    plot_reference(group["baseline"], axs[0])

    plt.subplots_adjust(left=padding[2]/100, right=1-(padding[3]/100), top=1-(padding[0]/100), bottom=padding[1]/100, wspace=0, hspace=0)
    plt.savefig("test.png")
    return get_figure_data()