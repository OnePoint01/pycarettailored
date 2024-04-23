# Import necessary libraries
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Import necessary functions from PyCaret
from pycaret.classification import setup as setup_clf,compare_models as compare_models_clf
from pycaret.regression import setup as setup_reg,compare_models as compare_models_reg

# Function to handle missing values
def handle_missing_values(df):
    le = LabelEncoder()
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna(df[col].mode()[0])  # fill missing values with mode for categorical columns
            df[col] = le.fit_transform(df[col].astype(str))  # transform with LabelEncoder
        else:
            df[col] = df[col].fillna(df[col].mean())  # fill missing values with mean for numeric columns
    return df

# Function to display DataFrame information
def display_df_info(df):
    st.write('Head of Dataset:', df.head())
    st.write('Data Shape:', df.shape)
    st.write('Column Names:', df.columns.tolist())
    st.write('Column Data Types:', df.dtypes)
    st.write('Summary Statistics:', df.describe().transpose())

# Function to setup and compare models
def setup_and_compare_models(df, target_col):
    if pd.api.types.is_numeric_dtype(df[target_col]):
        exp_reg = setup_reg(data = df, target = target_col, session_id=123, verbose=False)
        best_model = compare_models_reg()
    else:
        exp_clf = setup_clf(data = df, target = target_col, session_id=123, verbose=False)
        best_model = compare_models_clf()
    st.write(best_model)

# Title of the app
st.title('PyCaret & Streamlit App Capstone')

# Add a sidebar
st.sidebar.title("Settings Sidebar")

# Add a file uploader to the sidebar
uploaded_file = st.sidebar.file_uploader(label="Upload your input CSV file", type=['csv'])

# Check if a file is uploaded
if uploaded_file is not None:
    # Read the uploaded file
    df = pd.read_csv(uploaded_file)

    # Show the uploaded file
    st.write(df)

    # Display DataFrame information
    display_df_info(df)

    # Ask user for the target column
    target_col = st.sidebar.selectbox("Select the target column", df.columns)

    # Handle missing values
    df = handle_missing_values(df)

    # Setup and compare models
    setup_and_compare_models(df, target_col)
