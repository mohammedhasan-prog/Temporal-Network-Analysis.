import os
import pandas as pd
import numpy as np
from src.data_loading import load_data, split_data_by_day
from src.graphs import build_daily_graphs, build_aggregated_graph
from src.community_detection import detect_communities
from src.metrics import compute_network_stats
from src.visualization import (plot_graph_communities, plot_metrics_over_time, 
                               plot_correlation_matrix, visualize_louvain_toy_example,
                               animate_louvain_toy_example)

def generate_dummy_data(filepath):
    """Generates a dummy high school contact dataset."""
    print("Generating dummy data...")
    np.random.seed(42)
    num_students = 50
    days = 5
    records = []
    
    for day in range(1, days + 1):
        # Random interactions
        num_interactions = np.random.randint(100, 200)
        for _ in range(num_interactions):
            u = np.random.randint(1, num_students + 1)
            v = np.random.randint(1, num_students + 1)
            if u != v:
                records.append({'source': u, 'target': v, 'day': day})
                
    df = pd.DataFrame(records)
    df.to_csv(filepath, index=False)
    print(f"Dummy data saved to {filepath}")

def main():
    # Setup paths
    data_path = os.path.join('data', 'high_school_contacts.csv')
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if data exists, else generate dummy
    if not os.path.exists(data_path):
        print("Data file not found. Please run convert_data.py or provide data.")
        # generate_dummy_data(data_path) # Disable dummy generation to use real data

        
    # 1. Load Data
    print("Loading data...")
    df = load_data(data_path)
    
    # 2. Split by Day
    print("Splitting data by day...")
    daily_data = split_data_by_day(df, day_col='day')
    
    # 3. Build Graphs
    print("Building graphs...")
    daily_graphs = build_daily_graphs(daily_data)
    agg_graph = build_aggregated_graph(daily_graphs)
    
    # 4. Run Analysis (Louvain + Metrics)
    print("Running analysis...")
    results = []
    
    # Process Daily Graphs
    for day, G in daily_graphs.items():
        print(f"Processing Day {day}...")
        partition, modularity = detect_communities(G)
        stats = compute_network_stats(G, partition, modularity)
        stats['Graph'] = f'Day {day}'
        results.append(stats)
        
        # Visualize
        plot_graph_communities(G, partition, f'Day {day} Communities', 
                               f'HS{day}.png', output_dir)
                               
    # Process Aggregated Graph
    print("Processing Aggregated Graph...")
    part_agg, mod_agg = detect_communities(agg_graph)
    stats_agg = compute_network_stats(agg_graph, part_agg, mod_agg)
    stats_agg['Graph'] = 'Aggregated (HS0)'
    results.append(stats_agg)
    
    plot_graph_communities(agg_graph, part_agg, 'Aggregated Graph Communities', 
                           'HS0.png', output_dir)
                           
    # 5. Save Results
    results_df = pd.DataFrame(results)
    results_path = os.path.join(output_dir, 'network_statistics.csv')
    results_df.to_csv(results_path, index=False)
    print(f"Statistics saved to {results_path}")
    print(results_df)
    
    # 6. Visualizations
    print("Generating metric plots...")
    plot_metrics_over_time(results_df, output_dir)
    plot_correlation_matrix(results_df, output_dir)
    
    print("Generating didactic Louvain visualization...")
    visualize_louvain_toy_example(output_dir)
    
    print("Generating Louvain animation...")
    gif_path = animate_louvain_toy_example(output_dir)
    print(f"Animation saved to {gif_path}")
    
    # Try to open the animation automatically
    if os.name == 'nt': # Windows
        os.startfile(os.path.abspath(gif_path))
    
    print("Done! Check the 'output' directory.")

if __name__ == "__main__":
    main()
