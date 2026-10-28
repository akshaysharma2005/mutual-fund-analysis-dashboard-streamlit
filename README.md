# 📈 Apex Mutual Fund Intelligence & Analytics Dashboard
### *Next-Generation Interactive Dashboard Powered by Python, Scikit-Learn & Streamlit*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.66%2B-FF4B4B.svg)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75.svg)](https://plotly.com)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-MinMaxScaler%20Scoring-F7931E.svg)](https://scikit-learn.org)

---

## 🌟 Overview & Transformation

This project has been upgraded from a static **Power BI dashboard (`.pbix`)** into a **Full-Stack, Real-Time Interactive Streamlit Application** featuring luxury fintech dark aesthetics, dynamic ML scoring, risk-return matrices, and investment compounding simulators.

| Dimension | Previous Power BI Version | Upgraded Streamlit Architecture |
| :--- | :--- | :--- |
| **Platform** | Desktop Power BI (`.pbix` dependent) | **Browser-Based Interactive Streamlit Web App** |
| **Aesthetics** | Standard corporate canvas | **Luxury Obsidian & Emerald Fintech Theme (Glassmorphism)** |
| **Visualizations** | Static Power BI cards & visuals | **GPU-Accelerated Interactive Plotly Charts with Tooltips & Zoom** |
| **Alpha Model** | Pre-calculated Excel rankings | **Live Scikit-Learn Normalization with Dynamic Factor Weight Sliders** |
| **Risk Analysis** | High-level summary cards | **Interactive 4-Quadrant Volatility Frontier (Sharpe, Beta, SD)** |
| **Forecasting** | None | **Interactive SIP & Lumpsum Compounding Wealth Simulator with Inflation** |
| **Fund Comparison** | Basic filters | **Head-to-Head Fund Battle with 6-Axis Radar Spider Charts & Fee Drag** |
| **Dataset Access** | Top 30 summary only | **Dual Mode: 814 Analyzed Funds + Full 2,556 Market Scheme Screener** |

---

## 🏛️ Application Modules

### 1. 🏛️ Executive Cockpit (Upgraded Power BI Dashboard)
Replicates and elevates all original visual elements and KPIs:
- **Real-Time KPI Cards:** Total Investment Fund (₹3.10M Cr AUM), Average Lumpsum (₹3.05K), Average SIP (₹528.50), Benchmark Expense Ratio (0.71%), Average Fund Age (8.32 Yrs), 1-Year Average Return (3.92%).
- **Dynamic Executive Key Insights:** Live narrative summary synthesizing top AMCs, fund managers, asset allocation dominance, and cost leaders.
- **Investment Volume by Category:** High-contrast bar chart depicting AUM across Equity, Debt, Hybrid, and Solution Oriented.
- **Radial Speedometer Gauges:** High-fidelity speedometer gauges for Average SIP (₹0–₹2,000) and Average Lumpsum (₹0–₹25,000).
- **1-Year Returns by AMC:** Performance hierarchy of fund houses (Bank of India MF, HDFC, ICICI Prudential, Nippon, SBI).
- **Assets Managed by Top Fund Managers:** AUM ranking (Vivek Sharma ₹7.3k Cr, Vishal Mishra, Yogesh Patil, etc.).
- **Strategy Fee Efficiency:** Cost comparison across strategies highlighting Index Funds (0.26%), Money Market, and Liquid funds.
- **Category Share Donut:** Interactive multi-slice donut showing fund distribution.

### 2. 🏆 Top 30 Alpha Funds Screener & Ranking
- Uses **Scikit-Learn `MinMaxScaler`** to normalize multi-dimensional financial metrics.
- **Dynamic Weight Adjuster:** Tweak factor weights in real time (Expense Ratio, 1Y/3Y/5Y Returns, Sharpe, Sortino, Alpha, Beta) to simulate custom investment strategies.
- **Interactive Leaderboard:** Medal ranking (🥇, 🥈, 🥉), composite score progress bars, returns heatmaps, and category tags.
- **Scheme Deep-Dive Factsheet:** Click any scheme to inspect complete metadata, fund manager, risk rating, and ratio breakdown.
- **Instant CSV Export:** Download filtered top 30 funds for offline research.

### 3. ⚡ Risk vs. Return Matrix & Volatility Frontier
- **4-Quadrant Bubble Plot:** Categorizes funds into:
  - 🌟 **Star Outperformers:** High Return + Low Risk
  - ⚡ **Aggressive Growth:** High Return + High Volatility
  - 🛡️ **Capital Preservation:** Low Volatility + Moderate Return
  - ⚠️ **Drag Zone:** High Volatility + Low Return
- Toggle X-Axis (Standard Deviation, Beta, Risk Level, Expense Ratio) and Y-Axis (3Y Return, 1Y Return, 5Y Return, Sharpe, Alpha).

### 4. 🧮 Smart SIP & Lumpsum Wealth Simulator
- Simulate compound wealth growth over **1 to 30 years**.
- Combines **Monthly SIP** and **Initial Lumpsum** compounding.
- Supports **Scheme Presets** (e.g. Quant Small Cap 44.1%, PPFAS Flexi Cap 33.6%) or custom CAGRs.
- **Inflation Adjustment:** Toggle purchasing power erosion at configurable inflation rates.
- **Milestone Detection:** Automatically plots timeline markers to reach **₹10 Lakhs, ₹50 Lakhs, ₹1 Crore, and ₹5 Crores**.
- Detailed year-by-year compounding schedule table.

### 5. ⚔️ Head-to-Head Fund Duel
- Select 2 or 3 mutual funds for direct battle.
- **6-Axis Radar Spider Chart:** Evaluates 3Y Returns, 5Y Returns, Sharpe Ratio, Alpha, Low Cost, and Low Beta.
- **Side-by-Side Scorecard:** Identifies category winners in green.
- **10-Year Fee Drag Analysis:** Computes the exact rupee cost of expense ratios on wealth compounding over a decade.

### 6. 🌐 Macro Universe Screener (2,500+ Schemes)
- Full access to all 2,556 mutual fund schemes across India (`Mutual_Funds.csv`).
- Search by scheme name, benchmark, or category.
- Filter and export directly to CSV.

---

## 🧠 Machine Learning Normalization & Scoring Formula

The ranking engine follows the mathematical formulation originally defined in `Mutual Fund Analysis.ipynb`:

$$\text{Norm}(X) = \frac{X - X_{\min}}{X_{\max} - X_{\min}}$$

For cost and risk metrics where lower values are preferable:
$$\text{Norm}_{\text{inv}}(X) = 1 - \text{Norm}(X)$$

$$\text{Composite Score} = \sum_{i=1}^{n} w_i \cdot \text{Norm}(F_i)$$

| Metric | Direction | Default Weight | Description |
| :--- | :--- | :--- | :--- |
| `expense_ratio` | Inverted (Lower is better) | **20%** | Annual fund management fee |
| `returns_1yr` | Direct (Higher is better) | **15%** | Short-term momentum |
| `returns_3yr` | Direct (Higher is better) | **15%** | Medium-term annualized return |
| `returns_5yr` | Direct (Higher is better) | **15%** | Long-term wealth generation |
| `sharpe` | Direct (Higher is better) | **10%** | Excess return per unit of total risk |
| `sortino` | Direct (Higher is better) | **10%** | Excess return per unit of downside risk |
| `alpha` | Direct (Higher is better) | **10%** | Excess return over benchmark |
| `beta` | Inverted (Lower is better) | **5%** | Market sensitivity/volatility |

---

## 🚀 Getting Started

### Quick Start (One Command)
Run the automated launcher script:
```bash
./run.sh
```

### Manual Installation & Launch
```bash
# 1. Activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install required packages
pip install streamlit pandas plotly scikit-learn openpyxl altair numpy

# 3. Launch Streamlit app
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 📁 Repository Structure

```text
├── app.py                             # Main Streamlit Dashboard Application
├── styles.py                          # Modern Luxury Financial Dark UI CSS & Components
├── components.py                      # Interactive Plotly Charts, Radial Gauges & Radar Visuals
├── data_loader.py                     # Data Preprocessing, MinMax ML Scoring & Caching
├── run.sh                             # One-click execution bash script
├── comprehensive_mutual_funds_data.csv# Primary 814-Fund Dataset with Full Ratios
├── top_30_mutual_funds.xlsx           # Top 30 Filtered Alpha Funds
├── Mutual_Funds.csv                   # Macro Universe of 2,556 Schemes
├── Mutual Fund Analysis.ipynb         # Original Data Cleaning & Modeling Notebook
├── Mutual Fund Dashboard .png         # Legacy Power BI Dashboard Preview
└── README.md                          # Documentation
```
