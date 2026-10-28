"""
app.py - Advanced Interactive Mutual Fund Intelligence & Analytics Dashboard
Replaces Power BI with a modern, high-performance Streamlit fintech cockpit.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration - MUST BE FIRST STREAMLIT CALL
st.set_page_config(
    page_title="Mutual Fund Overview & Insights | Apex Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules
from styles import CUSTOM_CSS, metric_card
from data_loader import load_and_preprocess_data, compute_rankings, load_top_30_funds, load_macro_universe, DEFAULT_WEIGHTS
import components as comp

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA INGESTION
# ---------------------------------------------------------
df_raw = load_and_preprocess_data()
df_macro = load_macro_universe()
df_top30_actual = load_top_30_funds()

# ---------------------------------------------------------
# SIDEBAR CONTROLS & NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <div style="background: linear-gradient(135deg, #3B82F6, #10B981); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">
            📊
        </div>
        <div>
            <div style="font-weight: 800; font-size: 1.15rem; color: #FFFFFF; letter-spacing: -0.02em;">APEX FUNDS</div>
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">Financial Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Menu
    menu_choice = st.radio(
        "NAVIGATION",
        [
            "🏛️ Executive Cockpit (Power BI+)",
            "🏆 Top 30 Alpha Funds Screener",
            "⚡ Risk vs Return Matrix",
            "🧮 SIP & Lumpsum Simulator",
            "⚔️ Head-to-Head Fund Battle",
            "🌐 Macro Universe (2,500+ Funds)"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("### 🔍 Global Filters")

    # Category Filter
    all_categories = sorted(df_raw['category'].dropna().unique().tolist())
    selected_categories = st.multiselect(
        "Fund Category",
        options=all_categories,
        default=all_categories
    )

    # AMC Filter
    all_amcs = sorted(df_raw['amc_name'].dropna().unique().tolist())
    selected_amcs = st.multiselect(
        "Fund House (AMC)",
        options=all_amcs,
        default=[]
    )

    # Risk Level Slider
    min_risk, max_risk = int(df_raw['risk_level'].min()), int(df_raw['risk_level'].max())
    selected_risk = st.slider(
        "Risk Level Range (1: Low -> 6: Very High)",
        min_value=min_risk,
        max_value=max_risk,
        value=(min_risk, max_risk)
    )

    # Rating Filter
    min_rating = st.selectbox(
        "Minimum Rating",
        options=[0, 1, 2, 3, 4, 5],
        index=0,
        format_func=lambda x: "All Ratings" if x == 0 else f"{'⭐' * x} ({x}+ Stars)"
    )

    # Min SIP Slider
    max_sip_val = int(df_raw['min_sip'].max())
    sip_budget = st.slider(
        "Max Monthly SIP Budget (₹)",
        min_value=0,
        max_value=max_sip_val,
        value=max_sip_val,
        step=100
    )

    # Quick Summary Statistics in Sidebar
    st.markdown("---")
    st.markdown("### 📊 Database Snapshot")
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06); font-size: 0.8rem; line-height: 1.6;">
        <div><b>Analyzed Schemes:</b> <span style="color:#10B981;">{len(df_raw)}</span></div>
        <div><b>Fund Houses:</b> <span style="color:#3B82F6;">{df_raw['amc_name'].nunique()}</span></div>
        <div><b>Total Universe:</b> <span style="color:#F59E0B;">{len(df_macro)} Schemes</span></div>
        <div><b>Model Engine:</b> <span style="color:#8B5CF6;">Scikit-Learn MinMaxScaler</span></div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# FILTER APPLICATION
# ---------------------------------------------------------
filtered_df = df_raw.copy()

if selected_categories:
    filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]

if selected_amcs:
    filtered_df = filtered_df[filtered_df['amc_name'].isin(selected_amcs)]

filtered_df = filtered_df[
    (filtered_df['risk_level'] >= selected_risk[0]) & 
    (filtered_df['risk_level'] <= selected_risk[1]) &
    (filtered_df['rating'] >= min_rating) &
    (filtered_df['min_sip'] <= sip_budget)
]

# Safeguard against empty selection
if filtered_df.empty:
    filtered_df = df_raw.copy()
    st.warning("⚠️ No mutual funds match the current filter selection. Displaying all funds.")

# ---------------------------------------------------------
# TOP APP HEADER
# ---------------------------------------------------------
st.markdown("""
<div class="dash-header">
    <div class="dash-title-group">
        <h1>📊 Mutual Fund Overview & Insights</h1>
        <p>Interactive Data Intelligence, Alpha Discovery & Risk Analytics Dashboard</p>
    </div>
    <div>
        <div class="badge-pill badge-live">
            <span class="badge-pulse"></span>
            Streamlit Interactive Engine
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# TAB 1: EXECUTIVE COCKPIT (THE POWER BI UPGRADE)
# =========================================================
if menu_choice == "🏛️ Executive Cockpit (Power BI+)":
    
    # 1. Top KPI Metric Cards (Matching & Upgrading Power BI)
    total_aum = filtered_df['fund_size_cr'].sum()
    avg_lumpsum = filtered_df['min_lumpsum'].mean()
    total_lumpsum = filtered_df['min_lumpsum'].sum()
    avg_sip = filtered_df['min_sip'].mean()
    total_sip = filtered_df['min_sip'].sum()
    avg_expense = filtered_df['expense_ratio'].mean()
    avg_age = filtered_df['fund_age_yr'].mean()
    avg_1yr_return = filtered_df['returns_1yr'].mean()
    avg_3yr_return = filtered_df['returns_3yr'].mean()

    # Format AUM in Lakh Cr or M Cr
    if total_aum >= 1000000:
        aum_str = f"₹{total_aum/1000000:.2f}M Cr"
    elif total_aum >= 100000:
        aum_str = f"₹{total_aum/100000:.2f}L Cr"
    else:
        aum_str = f"₹{total_aum:,.0f} Cr"

    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)
    
    with kpi_col1:
        st.markdown(metric_card(
            "Total Investment Fund",
            aum_str,
            subtext="Total AUM Assets",
            delta=None,
            icon="💼",
            color="blue"
        ), unsafe_allow_html=True)

    with kpi_col2:
        lump_str = f"₹{avg_lumpsum/1000:.2f}K" if avg_lumpsum >= 1000 else f"₹{avg_lumpsum:.0f}"
        st.markdown(metric_card(
            "Average Lumpsum",
            lump_str,
            subtext=f"Total: ₹{total_lumpsum/1000000:.1f}M",
            icon="💰",
            color="amber"
        ), unsafe_allow_html=True)

    with kpi_col3:
        sip_str = f"₹{avg_sip:.2f}"
        st.markdown(metric_card(
            "Average SIP Amount",
            sip_str,
            subtext=f"Total: ₹{total_sip/1000:.0f}K/mo",
            icon="🔄",
            color="purple"
        ), unsafe_allow_html=True)

    with kpi_col4:
        st.markdown(metric_card(
            "Avg Expense Ratio",
            f"{avg_expense:.2f}%",
            subtext="Category Benchmark",
            icon="🧾",
            color="green"
        ), unsafe_allow_html=True)

    with kpi_col5:
        st.markdown(metric_card(
            "Average Fund Age",
            f"{avg_age:.2f} Yrs",
            subtext=f"Max: {filtered_df['fund_age_yr'].max():.0f} Yrs",
            icon="📅",
            color="cyan"
        ), unsafe_allow_html=True)

    with kpi_col6:
        ret_class = "green" if avg_1yr_return >= 0 else "rose"
        st.markdown(metric_card(
            "1-Yr Average Return",
            f"{avg_1yr_return:.2f}%",
            subtext=f"3Y Avg: {avg_3yr_return:.1f}%",
            delta=avg_1yr_return,
            icon="📈",
            color=ret_class
        ), unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # 2. Key Dynamic Insights Panel (Directly replicating and dynamically updating Power BI insights)
    top_cat = filtered_df.groupby('category')['fund_size_cr'].sum().idxmax()
    top_cat_size = filtered_df.groupby('category')['fund_size_cr'].sum().max()
    top_mgr = filtered_df.groupby('fund_manager')['fund_size_cr'].sum().idxmax()
    top_mgr_size = filtered_df.groupby('fund_manager')['fund_size_cr'].sum().max()
    lowest_exp_strat = filtered_df.groupby('sub_category')['expense_ratio'].mean().idxmin()
    lowest_exp_val = filtered_df.groupby('sub_category')['expense_ratio'].mean().min()
    best_amc_1y = filtered_df.groupby('amc_name')['returns_1yr'].mean().idxmax()
    best_amc_1y_val = filtered_df.groupby('amc_name')['returns_1yr'].mean().max()

    st.markdown(f"""
    <div class="insights-banner">
        <div class="insights-header">
            <span>💡 Mutual Fund Market Insights & Executive Summary</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 10px 24px;">
            <div class="insight-item">
                <div class="insight-bullet"></div>
                <div><b>Investment Trends:</b> <span style="color:#10B981;">{top_cat} funds</span> dominate the portfolio with <b>₹{top_cat_size/100000:.2f} Lakh Cr</b> in total asset size.</div>
            </div>
            <div class="insight-item">
                <div class="insight-bullet"></div>
                <div><b>Top Fund Manager:</b> <span style="color:#38BDF8;">{top_mgr}</span> manages the largest aggregate AUM of <b>₹{top_mgr_size/1000:.1f}k Cr</b>.</div>
            </div>
            <div class="insight-item">
                <div class="insight-bullet"></div>
                <div><b>Cost Efficiency:</b> <b>{lowest_exp_strat}</b> features the lowest management expense ratio at just <b>{lowest_exp_val:.2f}%</b>.</div>
            </div>
            <div class="insight-item">
                <div class="insight-bullet"></div>
                <div><b>Top 1Y Performance:</b> <b>{best_amc_1y}</b> delivers the highest average 1-year return at <b>{best_amc_1y_val:.1f}%</b>.</div>
            </div>
            <div class="insight-item">
                <div class="insight-bullet"></div>
                <div><b>Capital Entry Point:</b> Average minimum SIP is <b>₹{avg_sip:.2f}/mo</b>, while average minimum Lumpsum is <b>₹{avg_lumpsum/1000:.2f}K</b>.</div>
            </div>
            <div class="insight-item">
                <div class="insight-bullet"></div>
                <div><b>Category Returns:</b> Equity funds drive multi-year alpha, with 3-year annualized returns averaging <b>{filtered_df[filtered_df['category']=='Equity']['returns_3yr'].mean():.1f}%</b>.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Main Dashboard Charts - Row 1
    col_r1_left, col_r1_right = st.columns([2, 1])
    
    with col_r1_left:
        st.plotly_chart(comp.create_category_volume_chart(filtered_df), use_container_width=True)
        
    with col_r1_right:
        # Radial Gauges for SIP and Lumpsum
        st.plotly_chart(comp.create_gauge(avg_sip, 0, 2000, "Average SIP Amount", prefix="₹", color="#3B82F6"), use_container_width=True)
        st.plotly_chart(comp.create_gauge(avg_lumpsum, 0, 25000, "Average Lumpsum Amount", prefix="₹", color="#10B981"), use_container_width=True)

    # Main Dashboard Charts - Row 2
    col_r2_left, col_r2_right = st.columns([1, 1])
    
    with col_r2_left:
        st.plotly_chart(comp.create_amc_returns_chart(filtered_df, top_n=6), use_container_width=True)
        
    with col_r2_right:
        st.plotly_chart(comp.create_3yr_distribution_donut(filtered_df), use_container_width=True)

    # Main Dashboard Charts - Row 3
    col_r3_left, col_r3_right = st.columns([1, 1])
    
    with col_r3_left:
        st.plotly_chart(comp.create_top_managers_chart(filtered_df, top_n=6), use_container_width=True)
        
    with col_r3_right:
        st.plotly_chart(comp.create_expense_by_strategy_chart(filtered_df, top_n=6), use_container_width=True)


# =========================================================
# TAB 2: TOP 30 ALPHA FUNDS SCREENER (ML COMPOSITE SCORING)
# =========================================================
elif menu_choice == "🏆 Top 30 Alpha Funds Screener":
    st.markdown("### 🏆 Top 30 Alpha Mutual Funds Screener")
    st.markdown("Ranked using **Scikit-Learn MinMaxScaler Normalization** and multi-factor composite risk-return scoring.")

    with st.expander("⚙️ Customize Machine Learning Factor Weights", expanded=False):
        st.markdown("Adjust the relative weights for each financial parameter to simulate custom investment strategies:")
        w_cols = st.columns(4)
        with w_cols[0]:
            w_exp = st.slider("Low Expense Ratio (20%)", 0.0, 0.5, 0.20, 0.05)
            w_r1 = st.slider("1-Year Returns (15%)", 0.0, 0.5, 0.15, 0.05)
        with w_cols[1]:
            w_r3 = st.slider("3-Year Returns (15%)", 0.0, 0.5, 0.15, 0.05)
            w_r5 = st.slider("5-Year Returns (15%)", 0.0, 0.5, 0.15, 0.05)
        with w_cols[2]:
            w_sharpe = st.slider("Sharpe Ratio (10%)", 0.0, 0.5, 0.10, 0.05)
            w_sortino = st.slider("Sortino Ratio (10%)", 0.0, 0.5, 0.10, 0.05)
        with w_cols[3]:
            w_alpha = st.slider("Alpha Generation (10%)", 0.0, 0.5, 0.10, 0.05)
            w_beta = st.slider("Low Beta Risk (5%)", 0.0, 0.5, 0.05, 0.05)
            
        custom_weights = {
            'expense_ratio': w_exp,
            'returns_1yr': w_r1,
            'returns_3yr': w_r3,
            'returns_5yr': w_r5,
            'sharpe': w_sharpe,
            'sortino': w_sortino,
            'alpha': w_alpha,
            'beta': w_beta
        }

    # Compute rankings dynamically
    ranked_universe = compute_rankings(filtered_df, custom_weights)
    top_30 = ranked_universe.head(30).copy()

    # Format table for display
    display_df = top_30[[
        'rank', 'scheme_name', 'amc_name', 'category', 'composite_score',
        'returns_1yr', 'returns_3yr', 'returns_5yr', 'expense_ratio',
        'sharpe', 'alpha', 'fund_size_cr'
    ]].copy()

    # Medals formatting
    def format_rank(r):
        if r == 1: return "🥇 1"
        elif r == 2: return "🥈 2"
        elif r == 3: return "🥉 3"
        return str(r)
        
    display_df['rank_badge'] = display_df['rank'].apply(format_rank)

    # Summary metric cards for top funds
    top_f = top_30.iloc[0]
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown(metric_card("Rank #1 Scheme", top_f['scheme_name'][:25]+"...", subtext=top_f['amc_name'], icon="🥇", color="green"), unsafe_allow_html=True)
    with m_col2:
        st.markdown(metric_card("Highest Composite Score", f"{top_f['composite_score']:.4f}", subtext=f"Category: {top_f['category']}", icon="⭐", color="blue"), unsafe_allow_html=True)
    with m_col3:
        st.markdown(metric_card("Top 3-Yr Return", f"{top_30['returns_3yr'].max():.1f}%", subtext=f"Scheme: {top_30.sort_values('returns_3yr', ascending=False).iloc[0]['scheme_name'][:20]}...", icon="🚀", color="amber"), unsafe_allow_html=True)
    with m_col4:
        st.markdown(metric_card("Lowest Top-30 Expense", f"{top_30['expense_ratio'].min():.2f}%", subtext="Direct Plan Efficiency", icon="🏷️", color="purple"), unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Interactive Table
    st.markdown("#### 📋 Top 30 Mutual Funds Leaderboard")
    
    st.dataframe(
        display_df[[
            'rank_badge', 'scheme_name', 'category', 'amc_name', 'composite_score',
            'returns_1yr', 'returns_3yr', 'returns_5yr', 'expense_ratio', 'sharpe', 'alpha', 'fund_size_cr'
        ]].rename(columns={
            'rank_badge': 'Rank',
            'scheme_name': 'Mutual Fund Scheme',
            'category': 'Category',
            'amc_name': 'Fund House',
            'composite_score': 'Score',
            'returns_1yr': '1Y Ret (%)',
            'returns_3yr': '3Y Ret (%)',
            'returns_5yr': '5Y Ret (%)',
            'expense_ratio': 'Exp Ratio (%)',
            'sharpe': 'Sharpe',
            'alpha': 'Alpha',
            'fund_size_cr': 'AUM (₹ Cr)'
        }),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Composite Score",
                format="%.3f",
                min_value=0.0,
                max_value=1.0
            ),
            "1Y Ret (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "3Y Ret (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "5Y Ret (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Exp Ratio (%)": st.column_config.NumberColumn(format="%.2f%%"),
            "AUM (₹ Cr)": st.column_config.NumberColumn(format="₹%d Cr"),
        }
    )

    # Drill-down Fund Factsheet
    st.markdown("---")
    st.markdown("#### 🔬 Detailed Scheme Factsheet & Risk Profile")
    selected_scheme_name = st.selectbox(
        "Select a fund from the Top 30 to inspect complete metrics:",
        options=top_30['scheme_name'].tolist()
    )
    
    scheme_detail = top_30[top_30['scheme_name'] == selected_scheme_name].iloc[0]
    
    dcol1, dcol2, dcol3 = st.columns([1, 1, 1])
    with dcol1:
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">FUND METADATA</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #FFF; margin: 8px 0;">{scheme_detail['scheme_name']}</div>
            <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.8;">
                <div><b>AMC:</b> {scheme_detail['amc_name']}</div>
                <div><b>Manager:</b> {scheme_detail['fund_manager']}</div>
                <div><b>Fund Age:</b> {scheme_detail['fund_age_yr']} Years</div>
                <div><b>Rating:</b> {'⭐' * int(scheme_detail['rating']) if scheme_detail['rating'] > 0 else 'Unrated'}</div>
                <div><b>Risk Level:</b> {scheme_detail['risk_level']} / 6</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with dcol2:
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">RETURNS & CAPITAL</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #10B981; margin: 8px 0;">Performance Matrix</div>
            <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.8;">
                <div><b>1-Year Return:</b> <span style="color:#10B981;">{scheme_detail['returns_1yr']:.2f}%</span></div>
                <div><b>3-Year Return:</b> <span style="color:#10B981;">{scheme_detail['returns_3yr']:.2f}%</span></div>
                <div><b>5-Year Return:</b> <span style="color:#10B981;">{scheme_detail['returns_5yr']:.2f}%</span></div>
                <div><b>Min Monthly SIP:</b> ₹{scheme_detail['min_sip']:,}</div>
                <div><b>Min Lumpsum:</b> ₹{scheme_detail['min_lumpsum']:,}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with dcol3:
        st.markdown(f"""
        <div class="kpi-card">
            <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">RISK & EFFICIENCY</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #3B82F6; margin: 8px 0;">Risk Ratios</div>
            <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.8;">
                <div><b>Sharpe Ratio:</b> {scheme_detail['sharpe']:.2f}</div>
                <div><b>Sortino Ratio:</b> {scheme_detail['sortino']:.2f}</div>
                <div><b>Alpha:</b> {scheme_detail['alpha']:.2f}</div>
                <div><b>Beta:</b> {scheme_detail['beta']:.2f}</div>
                <div><b>Expense Ratio:</b> <span style="color:#F59E0B;">{scheme_detail['expense_ratio']:.2f}%</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Download Button
    csv_data = top_30.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Top 30 Funds Dataset (CSV)",
        data=csv_data,
        file_name="top_30_mutual_funds_ranked.csv",
        mime="text/csv"
    )


# =========================================================
# TAB 3: RISK VS RETURN MATRIX & EFFICIENT FRONTIER
# =========================================================
elif menu_choice == "⚡ Risk vs Return Matrix":
    st.markdown("### ⚡ Risk vs. Return Matrix & Volatility Frontier")
    st.markdown("Interactive 4-quadrant bubble map evaluating risk-adjusted returns, fund volatility, and asset size.")

    col_ax1, col_ax2 = st.columns(2)
    with col_ax1:
        x_axis_choice = st.selectbox(
            "Select X-Axis (Risk / Volatility Metric)",
            options=['sd', 'beta', 'risk_level', 'expense_ratio'],
            index=0,
            format_func=lambda x: {
                'sd': 'Standard Deviation (Total Volatility)',
                'beta': 'Beta (Systematic Market Risk)',
                'risk_level': 'Risk Level (1-6 Category Scale)',
                'expense_ratio': 'Expense Ratio (%)'
            }.get(x, x)
        )
    with col_ax2:
        y_axis_choice = st.selectbox(
            "Select Y-Axis (Performance Metric)",
            options=['returns_3yr', 'returns_1yr', 'returns_5yr', 'sharpe', 'alpha'],
            index=0,
            format_func=lambda y: {
                'returns_3yr': '3-Year Annualized Return (%)',
                'returns_1yr': '1-Year Trailing Return (%)',
                'returns_5yr': '5-Year Annualized Return (%)',
                'sharpe': 'Sharpe Ratio (Risk-Adjusted Return)',
                'alpha': 'Alpha Generation over Benchmark'
            }.get(y, y)
        )

    st.plotly_chart(comp.create_risk_return_scatter(filtered_df, x_col=x_axis_choice, y_col=y_axis_choice), use_container_width=True)

    # Quadrant explanation cards
    st.markdown("#### 🎯 Quadrant Strategy Guide")
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        st.markdown("""
        <div class="kpi-card" style="border-top: 2px solid #10B981;">
            <div style="font-weight: 700; color: #10B981;">★ Top Left: Star Alpha</div>
            <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 6px;">
                Low volatility coupled with high returns. Best risk-adjusted wealth generators.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with q2:
        st.markdown("""
        <div class="kpi-card" style="border-top: 2px solid #F59E0B;">
            <div style="font-weight: 700; color: #F59E0B;">⚡ Top Right: Aggressive Growth</div>
            <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 6px;">
                High return accompanied by high volatility. Ideal for long horizons (>5-10 yrs).
            </div>
        </div>
        """, unsafe_allow_html=True)
    with q3:
        st.markdown("""
        <div class="kpi-card" style="border-top: 2px solid #3B82F6;">
            <div style="font-weight: 700; color: #3B82F6;">🛡️ Bottom Left: Capital Shield</div>
            <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 6px;">
                Low risk, modest returns. Debt, liquid, and conservative funds for capital preservation.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with q4:
        st.markdown("""
        <div class="kpi-card" style="border-top: 2px solid #EF4444;">
            <div style="font-weight: 700; color: #EF4444;">⚠️ Bottom Right: Drag Zone</div>
            <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 6px;">
                High risk with below-average returns. Funds to scrutinize or rebalance away from.
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# TAB 4: SIP & LUMPSUM SIMULATOR
# =========================================================
elif menu_choice == "🧮 SIP & Lumpsum Simulator":
    st.markdown("### 🧮 Smart SIP vs. Lumpsum Investment Forecaster")
    st.markdown("Calculate compounding wealth generation, monthly SIP growth, and milestone targets.")

    sim_col1, sim_col2 = st.columns([1, 2])
    
    with sim_col1:
        st.markdown("#### ⚙️ Investment Parameters")
        
        # Fund selector for presets
        preset_mode = st.radio("Expected Return Preset", ["Custom Rate", "Match Scheme 3Y Return", "Match Scheme 5Y Return"])
        
        if preset_mode != "Custom Rate":
            selected_sim_fund = st.selectbox(
                "Choose Fund Scheme:",
                options=filtered_df['scheme_name'].tolist()
            )
            fund_data = filtered_df[filtered_df['scheme_name'] == selected_sim_fund].iloc[0]
            rate_val = fund_data['returns_3yr'] if "3Y" in preset_mode else fund_data['returns_5yr']
            default_rate = max(float(rate_val), 1.0)
        else:
            default_rate = 14.0

        sip_amt = st.number_input("Monthly SIP Investment (₹)", min_value=0, max_value=1000000, value=10000, step=1000)
        lump_amt = st.number_input("One-Time Initial Lumpsum (₹)", min_value=0, max_value=100000000, value=100000, step=10000)
        horizon_yrs = st.slider("Investment Horizon (Years)", min_value=1, max_value=30, value=10)
        expected_ret = st.slider("Expected Annual Return / CAGR (%)", min_value=1.0, max_value=40.0, value=float(default_rate), step=0.5)
        inflation_pct = st.slider("Inflation Rate Adjustment (%)", min_value=0.0, max_value=10.0, value=6.0, step=0.5)

    with sim_col2:
        chart_fig, invested_tot, nominal_tot, real_tot = comp.create_wealth_growth_chart(
            years=horizon_yrs,
            monthly_sip=sip_amt,
            lumpsum=lump_amt,
            expected_cagr=expected_ret,
            inflation_rate=inflation_pct
        )
        
        # Simulator Metric Cards
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            st.markdown(metric_card("Total Invested", f"₹{invested_tot/100000:.2f} L", subtext="Principal Capital", icon="💳", color="blue"), unsafe_allow_html=True)
        with sc2:
            st.markdown(metric_card("Future Value", f"₹{nominal_tot/100000:.2f} L", subtext=f"Gain: +₹{(nominal_tot-invested_tot)/100000:.2f} L", icon="🚀", color="green"), unsafe_allow_html=True)
        with sc3:
            st.markdown(metric_card("Real Purchasing Power", f"₹{real_tot/100000:.2f} L", subtext=f"Inflation {inflation_pct}%", icon="⚖️", color="amber"), unsafe_allow_html=True)
        with sc4:
            wealth_multiple = nominal_tot / invested_tot if invested_tot > 0 else 1
            st.markdown(metric_card("Wealth Multiplier", f"{wealth_multiple:.2f}x", subtext=f"{horizon_yrs} Years Horizon", icon="✨", color="purple"), unsafe_allow_html=True)

        st.plotly_chart(chart_fig, use_container_width=True)

    # Year-by-year schedule table
    st.markdown("#### 📅 Projected Annual Compounding Schedule")
    schedule = []
    r_mo = (1 + expected_ret / 100) ** (1 / 12) - 1
    
    for y in range(1, horizon_yrs + 1):
        m = y * 12
        inv = m * sip_amt + lump_amt
        sip_val = sip_amt * (((1 + r_mo) ** m - 1) / r_mo) * (1 + r_mo) if r_mo > 0 else m * sip_amt
        lump_val = lump_amt * ((1 + r_mo) ** m)
        tot = sip_val + lump_val
        real = tot / ((1 + inflation_pct / 100) ** y)
        schedule.append({
            "Year": f"Year {y}",
            "Invested Capital (₹)": f"₹{inv:,.0f}",
            "Future Portfolio Value (₹)": f"₹{tot:,.0f}",
            "Net Wealth Profit (₹)": f"₹{tot - inv:,.0f}",
            "Real Inflation Adjusted Value (₹)": f"₹{real:,.0f}"
        })
    st.dataframe(pd.DataFrame(schedule), use_container_width=True, hide_index=True)


# =========================================================
# TAB 5: HEAD-TO-HEAD FUND BATTLE
# =========================================================
elif menu_choice == "⚔️ Head-to-Head Fund Battle":
    st.markdown("### ⚔️ Mutual Fund Head-to-Head Duel")
    st.markdown("Compare 2 or 3 mutual funds side-by-side across performance, risk ratios, and fee impacts.")

    battle_funds = st.multiselect(
        "Select 2 or 3 Mutual Funds to Duel:",
        options=filtered_df['scheme_name'].tolist(),
        default=df_top30_actual['scheme_name'].head(2).tolist()
    )

    if len(battle_funds) >= 2:
        compare_df = filtered_df[filtered_df['scheme_name'].isin(battle_funds)].copy()
        
        # Display Radar Chart
        st.plotly_chart(comp.create_radar_chart(compare_df), use_container_width=True)

        # Side by side cards
        b_cols = st.columns(len(compare_df))
        for idx, (_, fund) in enumerate(compare_df.iterrows()):
            with b_cols[idx]:
                st.markdown(f"""
                <div class="glass-panel" style="border-top: 3px solid #3B82F6;">
                    <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">SCHEME {idx + 1}</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #FFF; margin: 8px 0 14px 0;">{fund['scheme_name']}</div>
                    
                    <div style="font-size: 0.88rem; line-height: 2; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 10px;">
                        <div><b>Fund House:</b> {fund['amc_name']}</div>
                        <div><b>Category:</b> {fund['category']} ({fund['sub_category']})</div>
                        <div><b>Fund Manager:</b> {fund['fund_manager']}</div>
                        <div><b>AUM Size:</b> ₹{fund['fund_size_cr']:,.0f} Cr</div>
                        <div><b>Expense Ratio:</b> <span style="color:#F59E0B; font-weight:700;">{fund['expense_ratio']:.2f}%</span></div>
                        <div><b>1-Year Return:</b> <span style="color:#10B981; font-weight:700;">{fund['returns_1yr']:.2f}%</span></div>
                        <div><b>3-Year Return:</b> <span style="color:#10B981; font-weight:700;">{fund['returns_3yr']:.2f}%</span></div>
                        <div><b>5-Year Return:</b> <span style="color:#10B981; font-weight:700;">{fund['returns_5yr']:.2f}%</span></div>
                        <div><b>Sharpe Ratio:</b> {fund['sharpe']:.2f}</div>
                        <div><b>Sortino Ratio:</b> {fund['sortino']:.2f}</div>
                        <div><b>Alpha:</b> {fund['alpha']:.2f}</div>
                        <div><b>Beta:</b> {fund['beta']:.2f}</div>
                        <div><b>Std Deviation:</b> {fund['sd']:.2f}</div>
                        <div><b>Min SIP / Lumpsum:</b> ₹{fund['min_sip']:,} / ₹{fund['min_lumpsum']:,}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # 10-Year Fee Drag Analysis
        st.markdown("#### 💸 10-Year Expense Ratio Drag Simulator")
        st.markdown("How much do management fees erode your potential returns on a ₹10 Lakh initial investment?")
        
        fee_data = []
        for _, fund in compare_df.iterrows():
            gross_cagr = fund['returns_3yr']
            net_cagr = gross_cagr - fund['expense_ratio']
            gross_val = 1000000 * ((1 + gross_cagr/100) ** 10)
            net_val = 1000000 * ((1 + net_cagr/100) ** 10)
            fee_lost = gross_val - net_val
            fee_data.append({
                "Scheme Name": fund['scheme_name'],
                "Expense Ratio": f"{fund['expense_ratio']:.2f}%",
                "Gross Value (Zero Fees)": f"₹{gross_val:,.0f}",
                "Net Realized Value": f"₹{net_val:,.0f}",
                "Fees Paid to AMC": f"₹{fee_lost:,.0f}",
                "Fee Drag (%)": f"{(fee_lost / gross_val * 100):.1f}%"
            })
        st.dataframe(pd.DataFrame(fee_data), use_container_width=True, hide_index=True)
    else:
        st.info("💡 Please select at least 2 mutual fund schemes above to begin comparison.")


# =========================================================
# TAB 6: MACRO MARKET UNIVERSE (2,500+ FUNDS)
# =========================================================
elif menu_choice == "🌐 Macro Universe (2,500+ Funds)":
    st.markdown("### 🌐 Complete Indian Mutual Funds Universe (2,500+ Schemes)")
    st.markdown("Search, filter, and inspect the macro fund universe from `Mutual_Funds.csv`.")

    if not df_macro.empty:
        search_query = st.text_input("🔎 Search by Scheme Name or Benchmark:", placeholder="e.g. HDFC, Kotak, Nifty 50, Small Cap...")
        
        macro_filtered = df_macro.copy()
        if search_query:
            macro_filtered = macro_filtered[
                macro_filtered['Scheme'].str.contains(search_query, case=False, na=False) |
                macro_filtered['Benchmark'].str.contains(search_query, case=False, na=False)
            ]

        m_kpi1, m_kpi2, m_kpi3 = st.columns(3)
        with m_kpi1:
            st.markdown(metric_card("Total Schemes in Database", f"{len(df_macro):,}", subtext="All AMCs in India", icon="🏛️", color="blue"), unsafe_allow_html=True)
        with m_kpi2:
            st.markdown(metric_card("Filtered Schemes", f"{len(macro_filtered):,}", subtext="Matching Current Search", icon="🔍", color="green"), unsafe_allow_html=True)
        with m_kpi3:
            avg_cagr_1y = macro_filtered['CAGR% 1 Year'].dropna().mean() if 'CAGR% 1 Year' in macro_filtered else 0
            st.markdown(metric_card("Average 1-Year CAGR", f"{avg_cagr_1y:.2f}%", subtext="Market Wide Average", icon="📊", color="purple"), unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        st.dataframe(
            macro_filtered,
            use_container_width=True,
            hide_index=True
        )

        csv_macro = macro_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Universe (CSV)",
            data=csv_macro,
            file_name="macro_mutual_funds_universe.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Macro dataset not loaded.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.8rem; padding: 20px 0;">
    <b>Apex Mutual Fund Intelligence System</b> • Developed with Python, Scikit-Learn, Streamlit & Plotly • Replacing Power BI with High-Performance Interactive Analytics
</div>
""", unsafe_allow_html=True)
