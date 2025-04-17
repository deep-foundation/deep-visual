"""
deepvisual
classes:
- visualize_triplet_graph:
"""

import pandas as pd
import matplotlib.pyplot as plt
import math

__version__ = "0.1.0"
__all__ = ['visualize_triplet_graph']  # Exported classes

def visualize_triplet_graph(
    df,
    edge_color="gray",
    node_color="lightblue", 
    node_text_color="black", 
    background_color="white", 
    figsize=(10, 8),
):
    # color Validation
    valid_colors = {"black", "red", "green", "yellow", "orange", 
                   "gray", "lightblue", "brown", "blue", "white"}
    
    for param, value in [
        ("edge_color", edge_color),
        ("node_color", node_color),
        ("node_text_color", node_text_color),
        ("background_color", background_color)
    ]:
        if value not in valid_colors:
            raise ValueError(f"Invalid {param}: {value}. Permissible: {valid_colors}")

    # assembling unique nodes
    nodes = list(pd.unique(df[[df.columns[0], df.columns[2]]].values.ravel()))
    node_pos = {}
    
    # node placement algorithm
    radius = 5
    angle_step = 2 * math.pi / len(nodes)
    for i, node in enumerate(nodes):
        x = radius * math.cos(i * angle_step)
        y = radius * math.sin(i * angle_step)
        node_pos[node] = (x, y)

    # create a drawing with background settings
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)
    
    # drawing nodes
    for node, (x, y) in node_pos.items():
        ax.scatter(x, y, s=1000, c=node_color, alpha=0.9)
        ax.text(x, y, node, 
               ha="center", va="center", 
               fontsize=10, 
               weight="bold",
               color=node_text_color)  # use the new parameter
    
    # drawing edge
    for _, row in df.iterrows():
        src = row.iloc[0]
        verb = row.iloc[1]
        dst = row.iloc[2]
        
        x1, y1 = node_pos[src]
        x2, y2 = node_pos[dst]
        dx, dy = x2 - x1, y2 - y1
        
        ax.arrow(
            x1, y1, dx, dy,
            head_width=0.2,
            head_length=0.3,
            fc=edge_color,
            ec=edge_color,
            length_includes_head=True
        )
        
        ax.text((x1+x2)/2, (y1+y2)/2, verb,
               color="red", fontsize=8,
               ha="center", va="center",
               bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"))

    plt.axis("off")
    plt.tight_layout()
    plt.show()
