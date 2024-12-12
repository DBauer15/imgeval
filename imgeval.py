from argparse import ArgumentParser
import util.io
import util.config
import metrics
import imgops
import layouts
import json


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("config", type=str, help="The config file to process")
    parser.add_argument("-o", "--outdir", type=str, default="./", help="The output dir to write to")
    parser.add_argument("-i", "--indir", type=str, default="./", help="The input dir to read relative from")
    return parser.parse_args()

def process_inputs(config):
    for group in config.get("inputs", []):
        util.io.load_group(group)

def process_imageops(config):
    for imageop in config.get("imageops", []):
        for groupname in imageop["groups"]:
            group = util.config.find_group(config, groupname)
            if group == None:
                continue
            imgops.compute_group(group, imageop)

def process_metrics(config):
    for metric in config.get("metrics", []):
        for groupname in metric["groups"]:
            group = util.config.find_group(config, groupname)
            if group == None:
                continue
            metrics.compute_group(group, metric)

def process_layouts(config):
    for layout in config.get("layouts", []):
        layouts.compute_layout(layout, config)

def process_outputs(config):
    for output in config["outputs"]:
        if output["type"] in [ "images", "metrics" ]:
            for groupname in output["groups"]:
                group = util.config.find_group(config, groupname)
                if group == None:
                    continue
                if output["type"] == "images":
                    util.io.save_group(group)
                if output["type"] == "metrics":
                    util.io.save_metrics(group)
        if output["type"] == "layouts":
            for layout in config["layouts"]:
                util.io.save_layout(layout)


if __name__ == "__main__":
    args = parse_args()
    util.io.BASEDIR = args.outdir
    util.io.INDIR = args.indir

    config = {}
    with open(args.config) as configfile:
        config = json.load(configfile)

    # print(json.dumps(config, indent=2))

    process_inputs(config)
    process_imageops(config)
    process_metrics(config)
    process_layouts(config)
    process_outputs(config)
