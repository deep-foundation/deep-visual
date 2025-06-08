"""
deepvisual
classes:
- visualize_triplet_graph:
- visualize_doblet_graph:
- visualize_link_doublet: draws doublet links (the table format is from:to)
- visualize_link_doublet_cluster: clusters links using the Louvain method
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
from community import community_louvain

__version__ = "0.1.0"
__all__ = ['visualize_triplet_graph', 'visualize_doblet_graph', 'visualize_link_doublet', 'visualize_link_doublet_cluster']  # Exported classes

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

def visualize_link_doublet(
    df,
    loop_color='red',
    edge_color='black',
    inter_edge_color='blue',
    background_color='white',
    title='',
    color_title='black',
    figsize=(12, 8),
    show_labels=True
):

    existing_ids = set(df.index + 1)

    loops = df[df['from'] == df['to']].copy()
    first_level = df[(df['from'] != df['to']) & df['from'].isin(loops.index + 1) & df['to'].isin(loops.index + 1)].copy()
    second_level = df[~df.index.isin(loops.index) & ~df.index.isin(first_level.index)].copy()
    second_level = second_level[
        (second_level['from'].isin(first_level.index + 1) | second_level['from'].isin(loops.index + 1)) &
        (second_level['to'].isin(first_level.index + 1) | second_level['to'].isin(loops.index + 1))
    ]

    G = nx.DiGraph()
    nodes = pd.concat([loops['from'], loops['to'], first_level['from'], first_level['to']]).unique()
    G.add_nodes_from(nodes)
    G.add_edges_from(zip(first_level['from'], first_level['to']))
    pos = nx.circular_layout(G)

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    operation_positions = {}

    def draw_infinity_loop(ax, x, y, label_id=None, size=0.12, color='red'):
        t = np.linspace(0, 2 * np.pi, 500)
        a = size
        x_loop = a * np.sin(t) / (1 + np.cos(t)**2)
        y_loop = a * np.sin(t) * np.cos(t) / (1 + np.cos(t)**2)
        x_loop += x
        y_loop += y
        ax.plot(x_loop, y_loop, color=color, lw=2)
        arrow_idx = -20
        arrow = FancyArrowPatch((x_loop[arrow_idx], y_loop[arrow_idx]),
                                (x_loop[arrow_idx + 1], y_loop[arrow_idx + 1]),
                                arrowstyle='->', color=color, mutation_scale=15, lw=2)
        ax.add_patch(arrow)
        if label_id is not None and show_labels:
            ax.text(x, y - 0.10, str(label_id), fontsize=10, color=color,
                    ha='center', va='center', zorder=5)

    for i, row in df.iterrows():
        src, dst = row['from'], row['to']
        op_id = i + 1

        if src == dst and src in pos:
            x, y = pos[src]
            draw_infinity_loop(ax, x, y, label_id=op_id, color=loop_color)

        elif src in pos and dst in pos:
            x1, y1 = pos[src]
            x2, y2 = pos[dst]
            arrow = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='->',
                                    color=edge_color, mutation_scale=20, lw=2)
            ax.add_patch(arrow)

            dx, dy = x2 - x1, y2 - y1
            length = np.hypot(dx, dy)
            if length != 0:
                ux, uy = dx / length, dy / length
                perp_x, perp_y = -uy, ux
                cross_length = 0.03
                start_x = x1 + ux * 0.07
                start_y = y1 + uy * 0.07
                line = Line2D(
                    [start_x - perp_x * cross_length, start_x + perp_x * cross_length],
                    [start_y - perp_y * cross_length, start_y + perp_y * cross_length],
                    color=edge_color, lw=2, zorder=1
                )
                ax.add_line(line)

            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            if show_labels:
                ax.text(mid_x + 0.03, mid_y + 0.03, str(op_id), fontsize=10,
                        color=edge_color, ha='left', va='bottom', zorder=5)
            operation_positions[op_id] = ((x1, y1), (x2, y2))

        elif ((src in operation_positions or src in pos) and
              (dst in operation_positions or dst in pos)):
            if src in operation_positions:
                (x1_start, y1_start), (x1_end, y1_end) = operation_positions[src]
                p1_x = (x1_start + x1_end) / 2
                p1_y = (y1_start + y1_end) / 2
            else:
                p1_x, p1_y = pos[src]

            if dst in operation_positions:
                (x2_start, y2_start), (x2_end, y2_end) = operation_positions[dst]
                p2_x = (x2_start + x2_end) / 2
                p2_y = (y2_start + y2_end) / 2
            else:
                p2_x, p2_y = pos[dst]

            rad = -0.9 if p1_y > p2_y else 0.9
            arrow = FancyArrowPatch((p1_x, p1_y), (p2_x, p2_y),
                                    connectionstyle=f"arc3,rad={rad}",
                                    arrowstyle='->', color=inter_edge_color,
                                    mutation_scale=20, lw=2)
            ax.add_patch(arrow)

            mid_x = (p1_x + p2_x) / 2
            mid_y = (p1_y + p2_y) / 2
            dx, dy = p2_x - p1_x, p2_y - p1_y
            length = np.hypot(dx, dy)
            perp_dx, perp_dy = -dy / length, dx / length
            offset = abs(rad) * 0.3
            arc_mid_x = mid_x + perp_dx * offset
            arc_mid_y = mid_y + perp_dy * offset
            if show_labels:
                ax.text(arc_mid_x, arc_mid_y, str(op_id), fontsize=10,
                        color=inter_edge_color, ha='center', va='center', zorder=5)

    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(title, color=color_title)
    plt.tight_layout()
    plt.show()

#---------------------------------------------------------------------------------------------------

def visualize_link_doublet_cluster(df, background_color='white', title=''):
    """visualization of links with louvain clustering"""
    
    # 1. built-in clustering function
    def cluster_links(df):
        """internal function for clustering links"""
        df['link'] = df['from'].astype(str) + '→' + df['to'].astype(str)
        G = nx.Graph()
        G.add_nodes_from(df['link'])
        
        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                a_from, a_to = df.iloc[i]['from'], df.iloc[i]['to']
                b_from, b_to = df.iloc[j]['from'], df.iloc[j]['to']
                if {a_from, a_to} & {b_from, b_to}:
                    G.add_edge(df.iloc[i]['link'], df.iloc[j]['link'])
        
        return community_louvain.best_partition(G)
    
    # 2. perform clustering
    clusters = cluster_links(df)
    
    # 3. create graph and node positions
    G = nx.DiGraph()
    G.add_nodes_from(pd.concat([df['from'], df['to']]).unique())
    G.add_edges_from(zip(df['from'], df['to']))
    pos = nx.circular_layout(G)
    
    # 4. color palette for clusters
    unique_clusters = set(clusters.values())
    palette = plt.cm.tab10.colors
    cluster_colors = {c: palette[i % len(palette)] for i, c in enumerate(unique_clusters)}
    
    # 5. visualization setup
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)
    
    operation_positions = {}
    loops = df[df['from'] == df['to']]
    loop_nodes = set(loops['from'])
    
    # 6. draw all elements
    for i, row in df.iterrows():
        src, dst = row['from'], row['to']
        link = f"{src}→{dst}"
        op_id = i + 1
        color = cluster_colors.get(clusters.get(link, -1), 'gray')
        
        # closed loops
        if src == dst:
            t = np.linspace(0, 2*np.pi, 500)
            a = 0.12
            x_loop = a*np.sin(t)/(1+np.cos(t)**2) + pos[src][0]
            y_loop = a*np.sin(t)*np.cos(t)/(1+np.cos(t)**2) + pos[src][1]
            ax.plot(x_loop, y_loop, color=color, lw=2)
            
            arrow_idx = -20
            ax.add_patch(FancyArrowPatch(
                (x_loop[arrow_idx], y_loop[arrow_idx]),
                (x_loop[arrow_idx+1], y_loop[arrow_idx+1]),
                arrowstyle='->', color=color, mutation_scale=15, lw=2
            ))
            ax.text(pos[src][0], pos[src][1]-0.10, str(op_id),
                   fontsize=10, color=color, ha='center', va='center')
        
        # links between nodes
        elif src in loop_nodes and dst in loop_nodes:
            x1, y1 = pos[src]
            x2, y2 = pos[dst]
            
            ax.add_patch(FancyArrowPatch(
                (x1, y1), (x2, y2),
                arrowstyle='->', color=color,
                mutation_scale=20, lw=2
            ))
            
            # cross at arrow start
            dx, dy = x2-x1, y2-y1
            length = np.hypot(dx, dy)
            if length > 0:
                ux, uy = dx/length, dy/length
                perp_x, perp_y = -uy, ux
                start_x = x1 + ux*0.07
                start_y = y1 + uy*0.07
                ax.add_line(Line2D(
                    [start_x-perp_x*0.03, start_x+perp_x*0.03],
                    [start_y-perp_y*0.03, start_y+perp_y*0.03],
                    color=color, lw=2
                ))
            
            # id label
            ax.text((x1+x2)/2+0.03, (y1+y2)/2+0.03, str(op_id),
                   fontsize=10, color=color, ha='left', va='bottom')
            operation_positions[op_id] = ((x1, y1), (x2, y2))
        
        # links between links
        else:
            if src in operation_positions and dst in operation_positions:
                (x1s, y1s), (x1e, y1e) = operation_positions[src]
                (x2s, y2s), (x2e, y2e) = operation_positions[dst]
                mid1 = ((x1s+x1e)/2, (y1s+y1e)/2)
                mid2 = ((x2s+x2e)/2, (y2s+y2e)/2)
                
                rad = -0.9 if mid1[1] > mid2[1] else 0.9
                ax.add_patch(FancyArrowPatch(
                    mid1, mid2,
                    connectionstyle=f"arc3,rad={rad}",
                    arrowstyle='->', color=color,
                    mutation_scale=20, lw=2
                ))
                
                # id label
                dx = mid2[0]-mid1[0]
                dy = mid2[1]-mid1[1]
                length = np.hypot(dx, dy)
                perp_dx, perp_dy = -dy/length, dx/length
                offset = 0.3*abs(rad)
                text_x = (mid1[0]+mid2[0])/2 + perp_dx*offset
                text_y = (mid1[1]+mid2[1])/2 + perp_dy*offset
                ax.text(text_x, text_y, str(op_id),
                       fontsize=10, color=color, ha='center', va='center')
    
    # 7. add legend
    legend_elements = [Line2D([0], [0], color=c, lw=2, label=f'Cluster {k}') 
                      for k, c in cluster_colors.items()]
    ax.legend(handles=legend_elements, loc='upper right')
    
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(title)
    plt.tight_layout()
    plt.show()