import community.community_louvain as community_louvain
import networkx as nx

def detect_communities(G, random_state=42):
    """
    Runs Louvain community detection on the graph.
    
    Args:
        G (nx.Graph): The network graph.
        random_state (int): Seed for reproducibility.
        
    Returns:
        dict: Partition dictionary {node: community_id}
        float: Modularity score
    """
    if len(G.nodes) == 0:
        return {}, 0.0
        
    # python-louvain's best_partition
    partition = community_louvain.best_partition(G, random_state=random_state, weight='weight')
    modularity = community_louvain.modularity(partition, G, weight='weight')
    
    return partition, modularity
