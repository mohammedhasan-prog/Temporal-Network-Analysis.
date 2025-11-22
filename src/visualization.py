import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
import pandas as pd
import os
import community.community_louvain as community_louvain
from matplotlib.animation import FuncAnimation

def plot_graph_communities(G, partition, title, filename, output_dir='output'):
    """
    Draws the graph with nodes colored by community.
    """
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)  # Consistent layout
    
    # Color mapping
    cmap = plt.cm.get_cmap('viridis', max(partition.values()) + 1)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=50,
                           cmap=cmap, node_color=list(partition.values()))
                           
    # Draw edges (thickness proportional to weight)
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    # Normalize weights for visualization width
    if weights:
        max_w = max(weights)
        widths = [0.5 + (w / max_w) * 2 for w in weights]
    else:
        widths = 1.0
        
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=widths)
    
    plt.title(title)
    plt.axis('off')
    
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()

def plot_metrics_over_time(stats_df, output_dir='output'):
    """
    Plots metrics over time (HS1-HS5).
    """
    # Filter for daily graphs (assuming 'Graph' column has 'Day X')
    daily_df = stats_df[stats_df['Graph'].str.contains('Day')].copy()
    daily_df['Day_Num'] = daily_df['Graph'].apply(lambda x: int(x.split(' ')[1]))
    daily_df = daily_df.sort_values('Day_Num')
    
    metrics_to_plot = ['Num_Communities', 'Modularity', 'Avg_Path_Length', 'Avg_Clustering_Coeff']
    
    for metric in metrics_to_plot:
        plt.figure(figsize=(8, 5))
        sns.lineplot(data=daily_df, x='Day_Num', y=metric, marker='o')
        plt.title(f'{metric} over Time')
        plt.xlabel('Day')
        plt.ylabel(metric)
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, f'metric_{metric}.png'))
        plt.close()

def plot_correlation_matrix(stats_df, output_dir='output'):
    """
    Computes and plots correlation matrix for HS1-HS5.
    """
    daily_df = stats_df[stats_df['Graph'].str.contains('Day')]
    cols = ['Num_Communities', 'Modularity', 'Density', 'Diameter', 
            'Avg_Clustering_Coeff', 'Avg_Path_Length']
    
    # Ensure columns are numeric
    corr_data = daily_df[cols].astype(float)
    corr_matrix = corr_data.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix of Network Metrics (HS1-HS5)')
    plt.savefig(os.path.join(output_dir, 'correlation_matrix.png'))
    plt.close()

def visualize_louvain_toy_example(output_dir='output'):
    """
    Creates a didactic visualization of Louvain on a toy graph.
    """
    # Create a toy graph with clear community structure
    G = nx.Graph()
    # Community 1
    G.add_edges_from([(1,2), (1,3), (2,3), (3,4)])
    # Community 2
    G.add_edges_from([(5,6), (6,7), (5,7), (7,8)])
    # Bridge
    G.add_edge(4, 5)
    
    pos = nx.spring_layout(G, seed=42)
    
    # Step 1: Initial state (each node own community)
    initial_partition = {n: i for i, n in enumerate(G.nodes())}
    
    plt.figure(figsize=(12, 4))
    
    # Plot 1: Initial
    plt.subplot(1, 3, 1)
    nx.draw(G, pos, node_color=list(initial_partition.values()), cmap=plt.cm.tab10, with_labels=True)
    plt.title("Step 1: Each node is a community")
    
    # Step 2: Intermediate (Manual grouping for demonstration)
    # Let's say 1,2,3,4 merge and 5,6,7,8 merge
    inter_partition = {1:0, 2:0, 3:0, 4:0, 5:1, 6:1, 7:1, 8:1}
    
    plt.subplot(1, 3, 2)
    nx.draw(G, pos, node_color=list(inter_partition.values()), cmap=plt.cm.tab10, with_labels=True)
    plt.title("Step 2: Nodes merge to max modularity")
    
    # Step 3: Final (Aggregated view - conceptual)
    # We just show the same coloring but maybe different title as toy graph is simple
    plt.subplot(1, 3, 3)
    nx.draw(G, pos, node_color=list(inter_partition.values()), cmap=plt.cm.tab10, with_labels=True)
    plt.title("Step 3: Final Communities")
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'louvain_didactic.png'))
    plt.close()

def animate_louvain_toy_example(output_dir='output'):
    """
    Creates an animation of the Louvain algorithm on a larger toy graph.
    Saves as a GIF.
    """
    # 1. Create Larger Toy Graph (3 Communities of 5 nodes each)
    G = nx.Graph()
    
    # Community 1 (Nodes 0-4)
    c1_nodes = [0, 1, 2, 3, 4]
    # Create dense connections (cycle + random or just clique)
    # Let's make them cliques for clear structure
    for i in range(len(c1_nodes)):
        for j in range(i + 1, len(c1_nodes)):
            G.add_edge(c1_nodes[i], c1_nodes[j])
            
    # Community 2 (Nodes 5-9)
    c2_nodes = [5, 6, 7, 8, 9]
    for i in range(len(c2_nodes)):
        for j in range(i + 1, len(c2_nodes)):
            G.add_edge(c2_nodes[i], c2_nodes[j])
            
    # Community 3 (Nodes 10-14)
    c3_nodes = [10, 11, 12, 13, 14]
    for i in range(len(c3_nodes)):
        for j in range(i + 1, len(c3_nodes)):
            G.add_edge(c3_nodes[i], c3_nodes[j])
    
    # Bridges between communities
    G.add_edge(4, 5)   # C1-C2
    G.add_edge(9, 10)  # C2-C3
    G.add_edge(0, 14)  # C1-C3
    
    # Layout
    pos = nx.spring_layout(G, seed=100, k=0.5)
    
    # 2. Define Sequence
    frames = []
    descriptions = []
    
    # Initial State: Everyone is their own community
    current_partition = {n: n for n in G.nodes()}
    frames.append(current_partition.copy())
    descriptions.append("Init: 15 separate communities")
    
    # Sequence: Merge nodes into their respective community leaders (0, 5, 10)
    
    # Form Community 1 (Target: 0)
    for n in [1, 2, 3, 4]:
        current_partition[n] = 0
        frames.append(current_partition.copy())
        descriptions.append(f"Node {n} joins Community 0")

    # Form Community 2 (Target: 5)
    for n in [6, 7, 8, 9]:
        current_partition[n] = 5
        frames.append(current_partition.copy())
        descriptions.append(f"Node {n} joins Community 5")

    # Form Community 3 (Target: 10)
    for n in [11, 12, 13, 14]:
        current_partition[n] = 10
        frames.append(current_partition.copy())
        descriptions.append(f"Node {n} joins Community 10")
    
    # Calculate modularity for all frames
    modularities = [community_louvain.modularity(f, G) for f in frames]
    
    # 3. Setup Plot with 2 subplots
    fig, (ax_graph, ax_mod) = plt.subplots(1, 2, figsize=(14, 6))
    plt.subplots_adjust(bottom=0.2) # Make room for text
    
    def update(frame_idx):
        ax_graph.clear()
        ax_mod.clear()
        
        partition = frames[frame_idx]
        desc = descriptions[frame_idx]
        
        # Identify moved node
        moved_node = None
        if frame_idx > 0:
            prev_part = frames[frame_idx-1]
            for n, c in partition.items():
                if prev_part[n] != c:
                    moved_node = n
                    break
        
        # --- Plot Graph ---
        # Use tab20 for more colors since we start with 15 communities
        cmap = plt.cm.get_cmap('tab20', 20)
        node_colors = [cmap(partition[n] % 20) for n in G.nodes()]
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, ax=ax_graph, alpha=0.3)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, ax=ax_graph, node_color=node_colors, 
                               node_size=400, alpha=0.9)
        
        # Highlight moved node
        if moved_node is not None:
            nx.draw_networkx_nodes(G, pos, ax=ax_graph, nodelist=[moved_node], 
                                   node_color=[node_colors[moved_node]], 
                                   node_size=700, edgecolors='red', linewidths=2.5)
            
        nx.draw_networkx_labels(G, pos, ax=ax_graph, font_color='black', font_size=9)
        
        ax_graph.set_title(f"Step {frame_idx}: {desc}")
        ax_graph.axis('off')
        
        # --- Plot Modularity ---
        steps = range(len(modularities))
        ax_mod.plot(steps, modularities, color='lightgray', marker='o', linestyle='--')
        # Highlight current progress
        ax_mod.plot(steps[:frame_idx+1], modularities[:frame_idx+1], 
                    color='blue', marker='o', linewidth=2)
        # Highlight current point
        ax_mod.plot(frame_idx, modularities[frame_idx], color='red', marker='o', markersize=10)
        
        ax_mod.set_title("Modularity Optimization")
        ax_mod.set_xlabel("Step")
        ax_mod.set_ylabel("Modularity (Q)")
        ax_mod.grid(True)
        if len(modularities) > 0:
            ax_mod.set_ylim(min(modularities)-0.05, max(modularities)+0.05)
        
    ani = FuncAnimation(fig, update, frames=len(frames), interval=1200, repeat=True)
    
    output_path = os.path.join(output_dir, 'louvain_optimization.gif')
    ani.save(output_path, writer='pillow', fps=1)
    plt.close()
    return output_path
