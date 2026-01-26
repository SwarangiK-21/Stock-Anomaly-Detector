import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import sqlite3  # <--- NEW: Import SQL tool
from datetime import datetime

# --- 1. DATABASE SETUP (The "Memory") ---
def init_db():
    """Creates a database and a table if they don't exist yet."""
    conn = sqlite3.connect('anomalies.db')
    c = conn.cursor()
    # Create a table to store anomalies: Ticker, Date, Price, and When we found it
    c.execute('''
        CREATE TABLE IF NOT EXISTS anomaly_history (
            ticker TEXT,
            anomaly_date TEXT,
            close_price REAL,
            found_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_anomaly_to_db(ticker, date, price):
    """Saves a single anomaly into the database."""
    conn = sqlite3.connect('anomalies.db')
    c = conn.cursor()
    # Check if we already saved this exact anomaly (to avoid duplicates)
    c.execute("SELECT * FROM anomaly_history WHERE ticker=? AND anomaly_date=?", (ticker, str(date)))
    if not c.fetchone():
        # Only insert if it's new
        c.execute("INSERT INTO anomaly_history VALUES (?, ?, ?, ?)", 
                  (ticker, str(date), price, str(datetime.now())))
        conn.commit()
    conn.close()

def fetch_history():
    """Gets all saved anomalies to show the user."""
    conn = sqlite3.connect('anomalies.db')
    df = pd.read_sql("SELECT * FROM anomaly_history ORDER BY found_at DESC", conn)
    conn.close()
    return df

# Initialize the DB immediately when app starts
init_db()

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Pro Stock Anomaly Detector", layout="wide")
st.title("📈 Pro Stock Anomaly Detector (with SQL DB)")

# --- 3. SIDEBAR ---
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")

# --- 4. GET DATA ---
@st.cache_data
def get_data(ticker_symbol):
    try:
        data = yf.download(ticker_symbol, period="2y")
        if data.empty: return None
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data
    except Exception as e:
        return None

df = get_data(ticker)

# --- 5. MAIN LOGIC ---
if df is not None:
    # A. Calculate Stats
    window = 20
    df['Moving_Avg'] = df['Close'].rolling(window=window).mean()
    df['Std_Dev'] = df['Close'].rolling(window=window).std()
    df['Z_Score'] = (df['Close'] - df['Moving_Avg']) / df['Std_Dev']
    
    # B. Find Anomalies
    df['Anomaly'] = df['Z_Score'].apply(lambda x: abs(x) > 3)
    anomalies = df[df['Anomaly'] == True]

    # --- NEW: SAVE TO DATABASE ---
    # Loop through the anomalies and save them to SQL
    if not anomalies.empty:
        for index, row in anomalies.iterrows():
            save_anomaly_to_db(ticker, index.date(), row['Close'])

    # C. Visualization
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(f"Live Analysis: {ticker}")
        fig = px.line(df, x=df.index, y='Close', title=f"{ticker} Price Trend")
        if not anomalies.empty:
            fig.add_scatter(x=anomalies.index, y=anomalies['Close'], 
                            mode='markers', marker=dict(color='red', size=10), 
                            name='Anomaly')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Database History 🗄️")
        st.write("These are anomalies saved permanently in your SQL database.")
        
        # Fetch from DB and show
        history_df = fetch_history()
        if not history_df.empty:
            st.dataframe(history_df[['ticker', 'anomaly_date', 'close_price']])
        else:
            st.info("No anomalies saved in DB yet.")

else:
    st.error("Could not fetch data.")