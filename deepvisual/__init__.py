"""
deepvisual
classes:
- visualize_triplet_graph:
- visualize_duplet_link:
"""

import pandas as pd
import matplotlib.pyplot as plt
import math
import random
from matplotlib.patches import ArrowStyle
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch

__version__ = "0.1.0"
__all__ = ['visualize_triplet_graph', 'visualize_duplet_link']  # Exported classes

def visualize_triplet_graph(
    df,
    edge_color="gray",
    node_color="lightblue", 
    node_text_color="black", 
    background_color="white", 
    figsize=(10, 8),
):
    # color validation
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

#---------------------------------------------------------------------------------------------------

def visualize_duplet_link(
    df,
    edge_color="gray",
    node_text_color="black", 
    background_color="white",
    figsize=(10, 8),
    curvature=0.3,
    seed=42,
    loop_radius=0.8,
    arrow_style="->,head_length=0.7,head_width=0.5",
    connection_style="arc3",
    node_text_visible=True
):
    # color validation
    valid_colors = {"black", "red", "green", "yellow", "orange", 
                   "gray", "lightblue", "brown", "blue", "white",
                   "lightgreen", "pink", "purple", "cyan", "magenta"}
    
    for param, value in [
        ("edge_color", edge_color),
        ("node_text_color", node_text_color),
        ("background_color", background_color)
    ]:
        if value not in valid_colors:
            raise ValueError(f"Invalid {param}: {value}. Permissible: {valid_colors}")

    # get unique links
    nodes = list(pd.unique(df.values.ravel()))
    node_pos = {}
    
    # generating positions on a circle
    radius = 5
    angle_step = 2 * math.pi / len(nodes)
    for i, node in enumerate(nodes):
        x = radius * math.cos(i * angle_step)
        y = radius * math.sin(i * angle_step)
        node_pos[node] = (x, y)

    # drawing
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)
    ax.set_aspect('equal')
    
    # draw text labels of links (if enabled)
    if node_text_visible:
        for node, (x, y) in node_pos.items():
            ax.text(x, y, node, 
                   ha="center", va="center", 
                   fontsize=12, 
                   weight="bold",
                   color=node_text_color,
                   bbox=dict(facecolor=background_color, 
                            edgecolor=background_color,
                            boxstyle='circle,pad=0.2'))
    
    # drawing associative connections
    for _, row in df.iterrows():
        src = row.iloc[0]
        dst = row.iloc[1]
        
        x1, y1 = node_pos[src]
        x2, y2 = node_pos[dst]
        
        if src == dst:  # connection itself is circular
            # drawing circle
            circle = Circle(
                (x1, y1),
                loop_radius,
                fill=False,
                edgecolor=edge_color,
                lw=1.5
            )
            ax.add_patch(circle)
            
            # add an arrow pointing to the center
            arrow_length = loop_radius * 0.3
            arrow_start_x = x1 + loop_radius * 0.8
            arrow_start_y = y1
            arrow_end_x = x1 + loop_radius * 0.5
            arrow_end_y = y1
            
            ax.add_patch(FancyArrowPatch(
                (arrow_start_x, arrow_start_y),
                (arrow_end_x, arrow_end_y),
                arrowstyle=arrow_style,
                color=edge_color,
                mutation_scale=15,
                shrinkA=0,
                shrinkB=0
            ))
            
        else:  # directed communication
            arrow = FancyArrowPatch(
                (x1, y1),
                (x2, y2),
                arrowstyle=arrow_style,
                connectionstyle=f"{connection_style},rad={curvature}",
                color=edge_color,
                lw=1.5,
                mutation_scale=20,
                shrinkA=0,
                shrinkB=0
            )
            ax.add_patch(arrow)

    plt.xlim(-radius*1.2, radius*1.2)
    plt.ylim(-radius*1.2, radius*1.2)
    plt.axis("off")
    plt.tight_layout()
    plt.show()