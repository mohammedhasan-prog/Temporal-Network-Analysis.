import pandas as pd
import numpy as np
import os

def load_data(filepath):
    """
    Loads the contact dataset from a CSV file.
    Expected columns: 'source', 'target', 'timestamp' (or 'day').
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    df = pd.read_csv(filepath)
    return df

def split_data_by_day(df, day_col='day'):
    """
    Splits the dataframe into a dictionary of dataframes keyed by day.
    If 'day' column doesn't exist, tries to infer from 'timestamp'.
    """
    if day_col not in df.columns:
        # Fallback: try to create a day column from timestamp if it exists
        if 'timestamp' in df.columns:
            # Assuming timestamp is unix or similar, simple binning or conversion might be needed
            # For this specific project, we'll assume the input CSV has a 'day' column 
            # or we map timestamp to 1-5.
            # Let's just raise for now if explicit day isn't there, 
            # or assume the user pre-processed it.
            raise ValueError(f"Column '{day_col}' not found in dataframe.")
    
    days = sorted(df[day_col].unique())
    daily_data = {day: df[df[day_col] == day].copy() for day in days}
    return daily_data
