import networkx as nx

def build_daily_graphs(daily_data):
    """
    Builds a dictionary of weighted undirected graphs for each day.
    
    Args:
        daily_data (dict): Dictionary of {day: dataframe}.
        
    Returns:
        dict: {day: nx.Graph}
    """
    daily_graphs = {}
    for day, df in daily_data.items():
        G = nx.Graph()
        
        # We need to count interactions between pairs to get weights
        # Assuming each row is an interaction.
        # Group by source, target and count.
        interactions = df.groupby(['source', 'target']).size().reset_index(name='weight')
        
        for _, row in interactions.iterrows():
            G.add_edge(row['source'], row['target'], weight=row['weight'])
            
        daily_graphs[day] = G
    return daily_graphs

def build_aggregated_graph(daily_graphs):
    """
    Builds an aggregated graph by combining all daily graphs and summing edge weights.
    
    Args:
        daily_graphs (dict): {day: nx.Graph}
        
    Returns:
        nx.Graph: Aggregated weighted graph.
    """
    G_agg = nx.Graph()
    
    for day, G in daily_graphs.items():
        for u, v, data in G.edges(data=True):
            weight = data.get('weight', 1)
            if G_agg.has_edge(u, v):
                G_agg[u][v]['weight'] += weight
            else:
                G_agg.add_edge(u, v, weight=weight)
                
    return G_agg
