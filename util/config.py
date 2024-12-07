import io
import matplotlib.pyplot as plt

def find_group(config, name):
    for group in config["inputs"]:
        if group["name"] == name:
            return group
    return None

def get_figure_data(format="svg"):
    if format == "svg":
        bytestream = io.StringIO()
    if format == "pdf":
        bytestream = io.BytesIO()
    plt.savefig(bytestream, format=format)
    return bytestream.getvalue()