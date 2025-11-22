import networkx as nx
import numpy as np

def compute_network_stats(G, partition=None, modularity=None):
    """
    Computes network statistics for a given graph.
    
    Args:
        G (nx.Graph): The graph.
        partition (dict, optional): Community partition.
        modularity (float, optional): Modularity score.
        
    Returns:
        dict: Dictionary of network statistics.
    """
    stats = {}
    
    # Basic counts
    stats['Nodes'] = G.number_of_nodes()
    stats['Edges'] = G.number_of_edges()
    
    # Community stats
    if partition:
        stats['Num_Communities'] = len(set(partition.values()))
    if modularity is not None:
        stats['Modularity'] = modularity
        
    # Degrees
    degrees = [d for n, d in G.degree()]
    weighted_degrees = [d for n, d in G.degree(weight='weight')]
    stats['Avg_Degree'] = np.mean(degrees) if degrees else 0
    stats['Avg_Weighted_Degree'] = np.mean(weighted_degrees) if weighted_degrees else 0
    
    # Density
    stats['Density'] = nx.density(G)
    
    # Clustering Coefficient (Average)
    # For weighted graphs, clustering can be computed with weight parameter, 
    # but standard definition often ignores weight or uses specific weighted clustering.
    # We'll use the standard unweighted for simplicity unless specified otherwise, 
    # or weighted if supported. NetworkX average_clustering supports weight.
    stats['Avg_Clustering_Coeff'] = nx.average_clustering(G, weight='weight')
    
    # Path Length & Diameter (only for connected components)
    # If graph is not connected, we take the largest connected component
    if nx.is_connected(G):
        stats['Diameter'] = nx.diameter(G)
        stats['Avg_Path_Length'] = nx.average_shortest_path_length(G, weight=None) # Usually topological distance
    else:
        # Use largest connected component
        if len(G) > 0:
            largest_cc = max(nx.connected_components(G), key=len)
            subG = G.subgraph(largest_cc)
            stats['Diameter'] = nx.diameter(subG)
            stats['Avg_Path_Length'] = nx.average_shortest_path_length(subG)
        else:
            stats['Diameter'] = 0
            stats['Avg_Path_Length'] = 0
            
    return stats
