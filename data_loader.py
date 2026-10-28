"""
data_loader.py - Data ingestion, cleaning, normalization and ML composite scoring
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import streamlit as st

DEFAULT_WEIGHTS = {
    'expense_ratio': 0.20,
    'returns_1yr': 0.15,
    'returns_3yr': 0.15,
    'returns_5yr': 0.15,
    'sharpe': 0.10,
    'sortino': 0.10,
    'alpha': 0.10,
    'beta': 0.05
}

@st.cache_data(show_spinner=False)
def load_and_preprocess_data():
    """
    Loads comprehensive mutual funds data and cleans columns
    according to the methodology defined in the original Jupyter Notebook.
    """
    df = pd.read_csv('comprehensive_mutual_funds_data.csv')
    
    # 1. Fill missing returns with mean as done in the notebook
    mean_3yr = df['returns_3yr'].mean()
    mean_5yr = df['returns_5yr'].mean()
    df['returns_3yr'] = df['returns_3yr'].fillna(mean_3yr)
    df['returns_5yr'] = df['returns_5yr'].fillna(mean_5yr)
    
    # 2. Standardize numeric columns that contain hyphens or strings
    numeric_cols = ['expense_ratio', 'returns_1yr', 'returns_3yr', 'returns_5yr', 
                    'sharpe', 'sortino', 'alpha', 'beta', 'sd', 'min_sip', 'min_lumpsum', 'fund_size_cr', 'fund_age_yr']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace('-', '').replace('', np.nan), errors='coerce')
    
    # Fill remaining NaNs in ratio columns with 0
    df[['sortino', 'alpha', 'sd', 'beta', 'sharpe']] = df[['sortino', 'alpha', 'sd', 'beta', 'sharpe']].fillna(0)
    
    # Fill any remaining NaNs
    df['fund_size_cr'] = df['fund_size_cr'].fillna(0)
    df['expense_ratio'] = df['expense_ratio'].fillna(df['expense_ratio'].median())
    
    return df

def compute_rankings(df_input, weights=None):
    """
    Computes composite score and ranking using Scikit-Learn MinMaxScaler,
    inverting metrics where lower is better (expense_ratio, beta).
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS
        
    df = df_input.copy()
    columns_to_normalize = ['expense_ratio', 'returns_1yr', 'returns_3yr', 'returns_5yr', 
                            'sharpe', 'sortino', 'alpha', 'beta']
    
    scaler = MinMaxScaler()
    norm_vals = scaler.fit_transform(df[columns_to_normalize])
    df_normalized = pd.DataFrame(norm_vals, columns=columns_to_normalize, index=df.index)
    
    # Invert metrics where lower is better
    df_normalized['expense_ratio'] = 1.0 - df_normalized['expense_ratio']
    df_normalized['beta'] = 1.0 - df_normalized['beta']
    
    # Weighted composite score
    composite_series = sum(df_normalized[col] * weights[col] for col in weights.keys())
    df['composite_score'] = composite_series
    df['rank'] = df['composite_score'].rank(ascending=False, method='min').astype(int)
    
    return df.sort_values(by='rank', ascending=True)

@st.cache_data(show_spinner=False)
def load_top_30_funds():
    """
    Loads pre-calculated top 30 funds or computes dynamically
    """
    try:
        df_top30 = pd.read_excel('top_30_mutual_funds.xlsx')
        return df_top30
    except Exception:
        df = load_and_preprocess_data()
        df_ranked = compute_rankings(df)
        return df_ranked.head(30)

@st.cache_data(show_spinner=False)
def load_macro_universe():
    """
    Loads the 2,556 mutual fund schemes dataset from Mutual_Funds.csv
    """
    try:
        df = pd.read_csv('Mutual_Funds.csv')
        # Clean columns
        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'])
        
        # Clean currency and percentage signs
        for col in ['Net_Asset_Value(Rs.)', 'Min. Invest(Rs.)', 'SIP Min. Inv.(Rs.)']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '').str.replace(' ', '').str.replace('N/A', '')
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
        for col in ['CAGR% 6 Months', 'CAGR% 1 Year', 'CAGR% 3 Year', 'Exp. Ratio(%)']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace('%', '').str.replace(',', ''), errors='coerce')
                
        return df
    except Exception as e:
        print("Could not load Mutual_Funds.csv:", e)
        return pd.DataFrame()
