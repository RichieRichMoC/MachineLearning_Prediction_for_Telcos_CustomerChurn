import streamlit as st
import numpy as np
import pandas as pd
import os

st.set_page_config(
    page_title='History',
    page_icon=':)',
    layout='wide'
)

st.title("Prediction History")

# History page to display previous predictions
def display_prediction_history():
    
    csv_path = "./Data/Prediction_history.csv"
    df = pd.read_csv(csv_path)
    
    return df

if __name__ == "__main__":
    df = display_prediction_history()
    st.dataframe(df)