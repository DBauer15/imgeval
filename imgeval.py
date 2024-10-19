from argparse import ArgumentParser
import imgops.io
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
        imgops.io.load_group(group)

def process_outputs(config):
    for output in config["outputs"]:
        if output["type"] == "images":
            group = find_group(config, output["group"])
            if group:
                imgops.io.save_group(group)
                    


if __name__ == "__main__":
    args = parse_args()
    imgops.io.BASEDIR = args.outdir

    config = {}
    with open(args.config) as configfile:
        config = json.load(configfile)

    print(json.dumps(config, indent=2))

    process_inputs(config)
    process_outputs(config)
