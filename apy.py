import streamlit as st
import pandas as pd
import os

# Function to load and cache the dataset
@st.cache_data
def load_data():
    # Load the dataset from the Dataset folder
    # Use script directory as base to make path work on any system
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "Process_data", "df_preprocessed.csv")
    df = pd.read_csv(csv_path) 
    return df

def main():
    # Load the dataset
    df = load_data()

    # Display the first few rows of the dataset
    st.write(df.head())

if __name__ == '__main__':
    main()