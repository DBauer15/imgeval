from argparse import ArgumentParser
import json

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("config", help="The config file to process")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    config = {}
    with open(args.config) as configfile:
        config = json.load(configfile)

    print(json.dumps(config, indent=2))

