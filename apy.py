import streamlit as st
import pandas as pd
import os

# Function to load and cache the dataset
@st.cache_data
def load_data():
    # Load the dataset from the Dataset folder
    # Use script directory as base to make path work on any system
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try to load from Process_data folder
    csv_path = os.path.join(script_dir, "Process_data", "df_preprocessed.csv")
    
    # If Process_data file doesn't exist, try Dataset/Test.csv as fallback
    if not os.path.exists(csv_path):
        fallback_path = os.path.join(script_dir, "Dataset", "Test.csv")
        if os.path.exists(fallback_path):
            csv_path = fallback_path
        else:
            raise FileNotFoundError(f"Could not find data file at {csv_path} or {fallback_path}")
    
    df = pd.read_csv(csv_path) 
    return df

def main():
    # Load the dataset
    df = load_data()

    # Display the first few rows of the dataset
    st.write(df.head())

if __name__ == '__main__':
    main()