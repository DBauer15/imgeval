def find_group(config, name):
    for group in config["inputs"]:
        if group["name"] == name:
            return group
    return None