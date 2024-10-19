from argparse import ArgumentParser
import util.io
import metrics
import imgops
import json


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("config", type=str, help="The config file to process")
    parser.add_argument("-o", "--outdir", type=str, default="./", help="The output dir to write to")
    return parser.parse_args()

def find_group(config, name):
    for group in config["inputs"]:
        if group["name"] == name:
            return group
    return None

def process_inputs(config):
    for group in config["inputs"]:
        util.io.load_group(group)

def process_imageops(config):
    for imageop in config["imageops"]:
        for groupname in imageop["groups"]:
            group = find_group(config, groupname)
            if group == None:
                continue
            imgops.compute_group(group, imageop)

def process_metrics(config):
    for metric in config["metrics"]:
        for groupname in metric["groups"]:
            group = find_group(config, groupname)
            if group == None:
                continue
            metrics.compute_group(group, metric)


def process_outputs(config):
    for output in config["outputs"]:
        for groupname in output["groups"]:
            group = find_group(config, groupname)
            if group == None:
                continue
            if output["type"] == "images":
                util.io.save_group(group)
            if output["type"] == "metrics":
                util.io.save_metrics(group)
                    


if __name__ == "__main__":
    args = parse_args()
    util.io.BASEDIR = args.outdir

    config = {}
    with open(args.config) as configfile:
        config = json.load(configfile)

    # print(json.dumps(config, indent=2))

    process_inputs(config)
    process_imageops(config)
    process_metrics(config)
    process_outputs(config)
