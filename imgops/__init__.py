import imgops.crop
import imgops.tonemap

def compute_group(group, imageop):
    compute_imageop_fn = None
    if imageop["type"] == "crop":
        compute_imageop_fn = imgops.crop.compute_imageop
    elif imageop["type"] == "tonemap":
        compute_imageop_fn = imgops.tonemap.compute_imageop
    
    baseline = group["baseline"]
    result = compute_imageop_fn(imageop, baseline["data"])
    if "imageops" not in baseline:
        baseline["imageops"] = []
    baseline["imageops"].append(imageop.copy())
    baseline["imageops"][-1]["data"] = result

    for image in group["images"]:
        result = compute_imageop_fn(imageop, image["data"])

        if "imageops" not in image:
            image["imageops"] = []
        
        image["imageops"].append(imageop.copy())
        image["imageops"][-1]["data"] = result