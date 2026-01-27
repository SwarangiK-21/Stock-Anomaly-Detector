# 📈 Intelligent Stock Anomaly Detector

**Live Production Deployment:** [👉 Click Here to View App](https://stock-anomaly-detector.onrender.com)

A real-time financial analytics microservice that detects pricing anomalies in stock market data using statistical algorithms. This application is **containerized with Docker** and deployed on a **cloud-native architecture**, serving live insights via an interactive dashboard.

---

## ⚙️ How It Works (The Logic)
Unlike simple threshold-based alerts, this system uses a **statistical approach** to adapt to market volatility dynamically.

### 1. Data Ingestion Pipeline
* The system establishes a real-time connection to the **Yahoo Finance API (yfinance)** to fetch live historical data for user-selected tickers (e.g., AAPL, TSLA).

### 2. The Algorithm: Sliding Window Z-Score
To distinguish between normal fluctuations and true anomalies, we implement a **Sliding Window Algorithm** (Window Size = 20 days).

For every data point $x$, the system calculates:
1. **Rolling Mean ($\mu$):** The average price over the last 20 days.
2. **Rolling Standard Deviation ($\sigma$):** The volatility measurement over the window.
3. **Z-Score Calculation:**
   $$Z = \frac{X - \mu}{\sigma}$$

### 3. Anomaly Detection Decision
* **Logic:** If the Z-Score is **$> 3$** or **$< -3$**, the price deviation is statistically significant (3 standard deviations away from the mean).
* **Outcome:** The system flags this specific timestamp as a "CRITICAL ANOMALY" and visualizes it on the dashboard.

---

## 🛠️ Tech Stack & Architecture

| Category | Technologies Used |
| :--- | :--- |
| **Core Language** | Python 3.9 |
| **Data Science** | Pandas (Rolling Windows), NumPy, Scikit-Learn |
| **Visualization** | Plotly Express (Interactive Financial Charts) |
| **Containerization** | **Docker** (Multi-stage build, Alpine Linux base) |
| **Cloud & DevOps** | **Render** (Cloud PaaS), GitHub Actions (CI/CD) |
| **Frontend** | Streamlit |

---

## 📂 Project Structure

```text
├── Dockerfile          # Blueprint for the containerized environment
├── main.py             # Entry point for the Streamlit application
├── requirements.txt    # Python dependencies
├── anomalies.db        # SQLite database for persisting anomaly history
└── README.md           # Project documentation


