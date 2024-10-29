import metrics.aggregate
import metrics.imgmap

def compute_group(group, metric):
    compute_metric_fn = None;
    if metric["type"] == "map":
        compute_metric_fn = metrics.imgmap.compute_metric;
    if metric["type"] == "aggregate":
        compute_metric_fn = metrics.aggregate.compute_metric;

    
    baseline = group["baseline"]["data"]
    for image in group["images"]:
        result = compute_metric_fn(metric["metric"], image["data"], baseline)
        if "metrics" not in image:
            image["metrics"] = []

        image["metrics"].append(metric.copy())
        image["metrics"][-1]["data"] = result
    result = compute_metric_fn(metric["metric"], baseline, baseline)
    if "metrics" not in group["baseline"]:
        group["baseline"]["metrics"] = []

    group["baseline"]["metrics"].append(metric.copy())
    group["baseline"]["metrics"][-1]["data"] = result
    