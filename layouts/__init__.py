import layouts.vertical
import layouts.horizontal

def compute_layout(layout, config):
    compute_layout_fn = None
    if layout["type"] == "vertical":
        compute_layout_fn = layouts.vertical.compute_layout
    if layout["type"] == "horizontal":
        compute_layout_fn = layouts.horizontal.compute_layout
    
    layout["data"] = compute_layout_fn(layout, config)