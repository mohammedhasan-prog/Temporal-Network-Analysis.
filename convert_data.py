import pandas as pd
import numpy as np
import os

def convert_data():
    input_path = r'c:\Users\Admin\OneDrive\Desktop\WorkOnPper\contact-high-school-proj-graph\contact-high-school-proj-graph.txt'
    output_path = r'c:\Users\Admin\OneDrive\Desktop\WorkOnPper\data\high_school_contacts.csv'
    
    print(f"Reading from {input_path}...")
    
    # The file format is: node1 node2 weight
    # It does NOT have time/day information.
    # To make it work with our "5-day" pipeline, we will simulate days.
    # We'll randomly assign each interaction (or a fraction of its weight) to one of 5 days.
    
    try:
        df = pd.read_csv(input_path, sep=' ', names=['source', 'target', 'weight'])
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print(f"Loaded {len(df)} edges.")
    
    # Expand the weighted edges into individual interactions to distribute over days
    # or just assign each edge to a random day (simpler for structure preservation)
    # But the paper is about time-variant networks.
    # Let's replicate the edges 'weight' times and then assign random days?
    # That might be too much data.
    # Alternative: Assign each edge to a random day, or split its weight across days.
    # Our pipeline expects: source, target, day.
    # And it builds graphs by counting interactions.
    
    # Strategy:
    # For each row (u, v, w), we generate 'w' rows of (u, v, random_day).
    # If w is huge, we might scale it down.
    
    print("Expanding weighted edges into temporal interactions...")
    
    expanded_rows = []
    np.random.seed(42)
    
    for _, row in df.iterrows():
        u, v, w = int(row['source']), int(row['target']), int(row['weight'])
        
        # Scale down if weight is too large to avoid massive CSV, 
        # but keep at least 1 interaction if w > 0
        # The weights in the file look like 183, 511... manageable.
        
        # Generate 'w' timestamps (days 1-5)
        days = np.random.randint(1, 6, size=w)
        
        for day in days:
            expanded_rows.append({'source': u, 'target': v, 'day': day})
            
    new_df = pd.DataFrame(expanded_rows)
    
    print(f"Generated {len(new_df)} interactions across 5 days.")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    new_df.to_csv(output_path, index=False)
    print(f"Saved converted data to {output_path}")

if __name__ == "__main__":
    convert_data()
