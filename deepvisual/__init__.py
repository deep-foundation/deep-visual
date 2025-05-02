"""
deepvisual
classes:
- visualize_triplet_graph:
- visualize_doblet_graph:
- visualize_link_doublet: draws doublet links (the table format is from:to)
"""

import pandas as pd
import matplotlib.pyplot as plt
import math
import random
from matplotlib.patches import ArrowStyle
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.lines import Line2D
import networkx as nx

__version__ = "0.1.0"
__all__ = ['visualize_triplet_graph', 'visualize_doblet_graph', 'visualize_link_doublet']  # Exported classes

def visualize_triplet_graph(
    df,
    edge_color="gray",
    node_color="lightblue", 
    node_text_color="black", 
    background_color="white", 
    figsize=(10, 8),
    title='',
    color_title='black'
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
    plt.title(title, color=color_title)
    plt.tight_layout()
    plt.show()

#---------------------------------------------------------------------------------------------------

def visualize_doblet_graph(
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

#---------------------------------------------------------------------------------------------------

def visualize_link_doublet(df, loop_color='red', edge_color='black', inter_edge_color='blue', background_color='white', title='', color_title='black'):
    # creating a graph
    G = nx.DiGraph()
    G.add_nodes_from(pd.concat([df['from'], df['to']]).unique())
    edges = list(zip(df['from'], df['to']))
    G.add_edges_from(edges)

    # node positions
    pos = nx.circular_layout(G)

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    # dictionaries for storing arrow positions
    operation_positions = {}

    # number of closed connections
    loops = df[df['from'] == df['to']]
    loop_nodes = set(loops['from'])
    max_loop_id = len(loops)

    for i, row in df.iterrows():
        src, dst = row['from'], row['to']
        op_id = i + 1  # operation ID = line number + 1

        # if it's a closed loop
        if src == dst:
            def draw_infinity_loop(ax, x, y, label_id=None, size=0.12, color=loop_color):
                t = np.linspace(0, 2 * np.pi, 500)
                a = size
                x_loop = a * np.sin(t) / (1 + np.cos(t)**2)
                y_loop = a * np.sin(t) * np.cos(t) / (1 + np.cos(t)**2)
                x_loop += x
                y_loop += y
                ax.plot(x_loop, y_loop, color=color, lw=2)

                arrow_idx = -20
                arrow = FancyArrowPatch(
                    (x_loop[arrow_idx], y_loop[arrow_idx]),
                    (x_loop[arrow_idx + 1], y_loop[arrow_idx + 1]),
                    arrowstyle='->', color=color, mutation_scale=15, lw=2
                )
                ax.add_patch(arrow)

                if label_id is not None:
                    ax.text(x, y - 0.10, str(label_id),
                            fontsize=10, color=color, ha='center', va='center', zorder=5)

            x, y = pos[src]
            draw_infinity_loop(ax, x, y, label_id=op_id)

        # if it's a regular arrow between loops
        elif src in loop_nodes and dst in loop_nodes:
            x1, y1 = pos[src]
            x2, y2 = pos[dst]

            arrow = FancyArrowPatch(
                (x1, y1), (x2, y2),
                arrowstyle='->', color=edge_color,
                mutation_scale=20, lw=2
            )
            ax.add_patch(arrow)

            # a cross at the beginning
            dx, dy = x2 - x1, y2 - y1
            length = np.hypot(dx, dy)
            if length != 0:
                ux, uy = dx / length, dy / length
                perp_x, perp_y = -uy, ux
                cross_length = 0.03 # crosshair length
                start_x = x1 + ux * 0.07 # 0.07 - distance from the beginning
                start_y = y1 + uy * 0.07
                line = Line2D(
                    [start_x - perp_x * cross_length, start_x + perp_x * cross_length],
                    [start_y - perp_y * cross_length, start_y + perp_y * cross_length],
                    color=edge_color, lw=2, zorder=1
                )
                ax.add_line(line)

            # signature of the operation ID
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            ax.text(mid_x + 0.03, mid_y + 0.03, str(op_id),
                    fontsize=10, color=edge_color, ha='left', va='bottom', zorder=5)

            # memorizing the middle of this arrow for possible further connections
            operation_positions[op_id] = ((x1, y1), (x2, y2))

        # otherwise, this is the connection between the operations (arrows)
        else:
            # where from and where to - these are the operation IDs
            from_op = src
            to_op = dst

            if from_op in operation_positions and to_op in operation_positions:
                (x1_start, y1_start), (x1_end, y1_end) = operation_positions[from_op]
                (x2_start, y2_start), (x2_end, y2_end) = operation_positions[to_op]

                # we take the middle of the arrows
                mid1_x, mid1_y = (x1_start + x1_end) / 2, (y1_start + y1_end) / 2
                mid2_x, mid2_y = (x2_start + x2_end) / 2, (y2_start + y2_end) / 2

                # we will automatically determine the direction of the radius (up/down)
                rad = 0.9
                if mid1_y > mid2_y:
                  rad = -0.9  # if the first one is higher than the second one, we bend the arc down
                else:
                  rad = 0.9   # otherwise up

                arrow = FancyArrowPatch(
                  (mid1_x, mid1_y), (mid2_x, mid2_y),
                  connectionstyle=f"arc3,rad={rad}",  # new bend
                  arrowstyle='->', color=inter_edge_color,
                  mutation_scale=20, lw=2
                )
                ax.add_patch(arrow)

                # signature of the operation ID
                # the center is between the beginning and the end
                mid_x = (mid1_x + mid2_x) / 2
                mid_y = (mid1_y + mid2_y) / 2

                # vector direction from mid1 to mid2
                dx = mid2_x - mid1_x
                dy = mid2_y - mid1_y
                length = np.hypot(dx, dy)

                # perpendicular vector (normalized)
                perp_dx = -dy / length
                perp_dy = dx / length

                # offset along the perpendicular
                curvature = abs(rad)
                offset_magnitude = curvature * 0.3  # adjust the value for yourself
                offset_x = perp_dx * offset_magnitude
                offset_y = perp_dy * offset_magnitude

                # a new center, taking into account the bend
                arc_mid_x = mid_x + offset_x
                arc_mid_y = mid_y + offset_y

                ax.text(arc_mid_x, arc_mid_y, str(op_id),
                        fontsize=10, color=inter_edge_color, ha='center', va='center', zorder=5)

    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(title, color=color_title)
    plt.tight_layout()
    plt.show()