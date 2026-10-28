"""
components.py - High-fidelity Plotly Visualizations with Neon Dark Theme
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Palette constants
PALETTE = {
    'bg': 'rgba(0,0,0,0)',
    'paper_bg': 'rgba(0,0,0,0)',
    'font': '#E2E8F0',
    'grid': 'rgba(255, 255, 255, 0.06)',
    'cyan': '#06B6D4',
    'emerald': '#10B981',
    'blue': '#3B82F6',
    'purple': '#8B5CF6',
    'amber': '#F59E0B',
    'rose': '#F43F5E',
    'category_colors': {
        'Equity': '#10B981',
        'Debt': '#3B82F6',
        'Hybrid': '#F59E0B',
        'Other': '#8B5CF6',
        'Solution Oriented': '#06B6D4'
    }
}

def apply_chart_theme(fig, height=360):
    """Applies sleek dark theme styling to Plotly charts"""
    fig.update_layout(
        paper_bgcolor=PALETTE['paper_bg'],
        plot_bgcolor=PALETTE['bg'],
        font=dict(family='Plus Jakarta Sans, sans-serif', color=PALETTE['font'], size=12),
        margin=dict(l=20, r=20, t=40, b=20),
        height=height,
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_size=12,
            font_family="Plus Jakarta Sans",
            bordercolor="rgba(255,255,255,0.2)"
        ),
        xaxis=dict(
            gridcolor=PALETTE['grid'],
            zerolinecolor=PALETTE['grid'],
            tickfont=dict(color='#94A3B8')
        ),
        yaxis=dict(
            gridcolor=PALETTE['grid'],
            zerolinecolor=PALETTE['grid'],
            tickfont=dict(color='#94A3B8')
        )
    )
    return fig

def create_category_volume_chart(df):
    """
    Replicates & upgrades Power BI: Total Investment Volume by Fund Type
    """
    grouped = df.groupby('category')['fund_size_cr'].sum().reset_index()
    grouped = grouped.sort_values(by='fund_size_cr', ascending=False)
    
    colors = [PALETTE['category_colors'].get(cat, PALETTE['blue']) for cat in grouped['category']]
    
    # Format labels (e.g. ₹1.35M Cr)
    text_labels = []
    for val in grouped['fund_size_cr']:
        if val >= 100000:
            text_labels.append(f"₹{val/100000:.2f}L Cr")
        elif val >= 1000:
            text_labels.append(f"₹{val/1000:.1f}K Cr")
        else:
            text_labels.append(f"₹{val:.0f} Cr")
            
    fig = go.Figure(data=[
        go.Bar(
            x=grouped['category'],
            y=grouped['fund_size_cr'],
            text=text_labels,
            textposition='outside',
            textfont=dict(color='#FFFFFF', size=11, family='JetBrains Mono'),
            marker=dict(
                color=colors,
                line=dict(color='rgba(255,255,255,0.15)', width=1),
                opacity=0.9
            ),
            hovertemplate="<b>%{x}</b><br>Total AUM: ₹%{y:,.0f} Cr<extra></extra>"
        )
    ])
    
    fig.update_layout(
        title=dict(text="<b>Total Investment Volume by Fund Type</b>", font=dict(size=14, color='#F8FAFC')),
        xaxis_title="",
        yaxis_title="Sum of Fund Size (₹ Cr)",
        showlegend=False
    )
    return apply_chart_theme(fig, height=340)

def create_gauge(value, min_val, max_val, title, prefix="₹", suffix="", color="#3B82F6"):
    """
    Replicates & modernizes Power BI: Radial Speedometer Gauges for SIP & Lumpsum
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"<b>{title}</b>", 'font': {'size': 13, 'color': '#94A3B8'}},
        number={
            'prefix': prefix,
            'suffix': suffix,
            'font': {'size': 26, 'color': '#FFFFFF', 'family': 'JetBrains Mono'}
        },
        gauge={
            'axis': {'range': [min_val, max_val], 'tickcolor': '#64748B', 'tickwidth': 1, 'tickfont': {'color': '#94A3B8'}},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': 'rgba(255,255,255,0.05)',
            'borderwidth': 1,
            'bordercolor': 'rgba(255,255,255,0.1)',
            'steps': [
                {'range': [min_val, max_val * 0.4], 'color': 'rgba(16, 185, 129, 0.1)'},
                {'range': [max_val * 0.4, max_val * 0.75], 'color': 'rgba(59, 130, 246, 0.1)'},
                {'range': [max_val * 0.75, max_val], 'color': 'rgba(245, 158, 11, 0.1)'}
            ],
            'threshold': {
                'line': {'color': "#EF4444", 'width': 3},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    return apply_chart_theme(fig, height=200)

def create_amc_returns_chart(df, top_n=6):
    """
    Replicates Power BI: 1-Year Returns by Fund House (AMC)
    """
    grouped = df.groupby('amc_name')['returns_1yr'].mean().reset_index()
    top_amcs = grouped.sort_values(by='returns_1yr', ascending=False).head(top_n)
    
    # shorten names for clean display
    top_amcs['short_name'] = top_amcs['amc_name'].str.replace('Mutual Fund', 'MF').str.replace('Sun Life', 'SL')
    
    fig = go.Figure(go.Bar(
        x=top_amcs['short_name'],
        y=top_amcs['returns_1yr'],
        text=[f"{val:.1f}%" for val in top_amcs['returns_1yr']],
        textposition='outside',
        textfont=dict(color='#FFFFFF', size=11, family='JetBrains Mono'),
        marker=dict(
            color=top_amcs['returns_1yr'],
            colorscale='Tealgrn',
            line=dict(color='rgba(255,255,255,0.15)', width=1)
        ),
        hovertemplate="<b>%{x}</b><br>1Y Avg Return: %{y:.2f}%<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text="<b>1-Year Returns by Fund House (AMC)</b>", font=dict(size=14, color='#F8FAFC')),
        xaxis_title="",
        yaxis_title="Average 1-Yr Return (%)",
        showlegend=False
    )
    return apply_chart_theme(fig, height=340)

def create_top_managers_chart(df, top_n=6):
    """
    Replicates Power BI: Assets Managed by Top Fund Managers
    """
    grouped = df.groupby('fund_manager')['fund_size_cr'].sum().reset_index()
    top_managers = grouped.sort_values(by='fund_size_cr', ascending=True).tail(top_n)
    
    text_labels = [f"₹{val/1000:.1f}k Cr" if val >= 1000 else f"₹{val:.0f} Cr" for val in top_managers['fund_size_cr']]
    
    fig = go.Figure(go.Bar(
        x=top_managers['fund_size_cr'],
        y=top_managers['fund_manager'],
        orientation='h',
        text=text_labels,
        textposition='outside',
        textfont=dict(color='#FFFFFF', size=11, family='JetBrains Mono'),
        marker=dict(
            color='#3B82F6',
            line=dict(color='rgba(255,255,255,0.15)', width=1),
            opacity=0.85
        ),
        hovertemplate="<b>%{y}</b><br>Total AUM Managed: ₹%{x:,.0f} Cr<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text="<b>Assets Managed by Top Fund Managers</b>", font=dict(size=14, color='#F8FAFC')),
        xaxis_title="Sum of Fund Size (₹ Cr)",
        yaxis_title="",
        showlegend=False
    )
    return apply_chart_theme(fig, height=340)

def create_expense_by_strategy_chart(df, top_n=6):
    """
    Replicates Power BI: Average Management Fees by Fund Strategy (Lowest expense ratios)
    """
    grouped = df.groupby('sub_category')['expense_ratio'].mean().reset_index()
    lowest_exp = grouped.sort_values(by='expense_ratio', ascending=True).head(top_n)
    lowest_exp = lowest_exp.sort_values(by='expense_ratio', ascending=False)
    
    fig = go.Figure(go.Bar(
        x=lowest_exp['expense_ratio'],
        y=lowest_exp['sub_category'],
        orientation='h',
        text=[f"{val:.2f}%" for val in lowest_exp['expense_ratio']],
        textposition='outside',
        textfont=dict(color='#FFFFFF', size=11, family='JetBrains Mono'),
        marker=dict(
            color='#10B981',
            line=dict(color='rgba(255,255,255,0.15)', width=1),
            opacity=0.85
        ),
        hovertemplate="<b>%{y}</b><br>Avg Expense Ratio: %{x:.2f}%<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text="<b>Lowest Cost Fund Strategies (Expense Ratio)</b>", font=dict(size=14, color='#F8FAFC')),
        xaxis_title="Average Expense Ratio (%)",
        yaxis_title="",
        showlegend=False
    )
    return apply_chart_theme(fig, height=340)

def create_3yr_distribution_donut(df):
    """
    Replicates Power BI: 3-Year Fund Count & Return Distribution by Investment Type Donut
    """
    grouped = df.groupby('category').agg(
        count=('scheme_name', 'count'),
        avg_3yr=('returns_3yr', 'mean')
    ).reset_index()
    
    colors = [PALETTE['category_colors'].get(cat, PALETTE['blue']) for cat in grouped['category']]
    
    fig = go.Figure(go.Pie(
        labels=grouped['category'],
        values=grouped['count'],
        hole=0.6,
        marker=dict(colors=colors, line=dict(color='#0F172A', width=2)),
        textinfo='label+percent',
        textfont=dict(color='#FFFFFF', size=11),
        hovertemplate="<b>%{label}</b><br>Schemes: %{value}<br>Share: %{percent}<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text="<b>Fund Distribution by Category</b>", font=dict(size=14, color='#F8FAFC')),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(size=10, color='#94A3B8')),
        annotations=[dict(text='<b>FUNDS</b>', x=0.5, y=0.5, font_size=13, font_color='#E2E8F0', showarrow=False)]
    )
    return apply_chart_theme(fig, height=340)

def create_risk_return_scatter(df, x_col='sd', y_col='returns_3yr'):
    """
    Advanced 4-Quadrant Matrix: Risk vs Return with category bubbles & AUM sizing
    """
    plot_df = df[(df[x_col] > 0) & (df[y_col] > -50) & (df[y_col] < 120)].copy()
    
    median_x = plot_df[x_col].median()
    median_y = plot_df[y_col].median()
    
    fig = px.scatter(
        plot_df,
        x=x_col,
        y=y_col,
        color='category',
        size='fund_size_cr',
        size_max=35,
        hover_name='scheme_name',
        hover_data={
            'amc_name': True,
            'expense_ratio': ':.2f',
            'sharpe': ':.2f',
            'returns_1yr': ':.1f',
            'returns_3yr': ':.1f',
            'fund_size_cr': ':,.0f'
        },
        color_discrete_map=PALETTE['category_colors']
    )
    
    # Add quadrant dividing lines
    fig.add_hline(y=median_y, line_dash="dash", line_color="rgba(255,255,255,0.2)", line_width=1)
    fig.add_vline(x=median_x, line_dash="dash", line_color="rgba(255,255,255,0.2)", line_width=1)
    
    # Quadrant annotations
    fig.add_annotation(x=plot_df[x_col].min(), y=plot_df[y_col].max(), text="★ Star Outperformers (Low Risk, High Return)", 
                       showarrow=False, font=dict(color="#10B981", size=10), xanchor='left')
    fig.add_annotation(x=plot_df[x_col].max(), y=plot_df[y_col].max(), text="⚡ High Beta Growth", 
                       showarrow=False, font=dict(color="#F59E0B", size=10), xanchor='right')
    fig.add_annotation(x=plot_df[x_col].min(), y=plot_df[y_col].min(), text="🛡️ Capital Preservation", 
                       showarrow=False, font=dict(color="#3B82F6", size=10), xanchor='left')
    fig.add_annotation(x=plot_df[x_col].max(), y=plot_df[y_col].min(), text="⚠️ Lagging Funds", 
                       showarrow=False, font=dict(color="#EF4444", size=10), xanchor='right')
                       
    fig.update_layout(
        title=dict(text=f"<b>Risk vs Return Matrix ({y_col.upper()} vs {x_col.upper()})</b>", font=dict(size=14, color='#F8FAFC')),
        xaxis_title=f"Risk Metric: {x_col.upper()} (Standard Dev / Volatility)",
        yaxis_title=f"Return Metric: {y_col.upper()} (%)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(size=10, color='#94A3B8'))
    )
    return apply_chart_theme(fig, height=450)

def create_radar_chart(funds_df):
    """
    Radar Spider chart comparing 1 to 3 funds across key performance dimensions
    """
    categories = ['3Y Return', '5Y Return', 'Sharpe Ratio', 'Alpha', 'Low Cost (Inv Expense)', 'Low Beta']
    
    fig = go.Figure()
    
    colors = ['#10B981', '#3B82F6', '#F59E0B']
    
    for idx, (_, row) in enumerate(funds_df.iterrows()):
        # Normalize to 0-100 scale for comparison
        r_3yr = min(max(row['returns_3yr'] * 2, 0), 100)
        r_5yr = min(max(row['returns_5yr'] * 4, 0), 100)
        r_sharpe = min(max(row['sharpe'] * 35, 0), 100)
        r_alpha = min(max(row['alpha'] * 4 + 40, 0), 100)
        r_cost = min(max((2.5 - row['expense_ratio']) * 40, 0), 100)
        r_beta = min(max((2.0 - row['beta']) * 50, 0), 100)
        
        values = [r_3yr, r_5yr, r_sharpe, r_alpha, r_cost, r_beta]
        values.append(values[0]) # close loop
        
        color = colors[idx % len(colors)]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself',
            name=row['scheme_name'][:25] + '...',
            line=dict(color=color, width=2),
            fillcolor=f"rgba{tuple(list(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.2])}"
        ))
        
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor='rgba(255,255,255,0.1)'),
            angularaxis=dict(tickfont=dict(size=10, color='#CBD5E1'), linecolor='rgba(255,255,255,0.1)')
        ),
        title=dict(text="<b>Multi-Dimensional Fund Battle (Radar Profile)</b>", font=dict(size=14, color='#F8FAFC')),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=10, color='#94A3B8'))
    )
    return apply_chart_theme(fig, height=380)

def create_wealth_growth_chart(years, monthly_sip, lumpsum, expected_cagr, inflation_rate=0.0):
    """
    Simulates monthly SIP and one-time lumpsum compound wealth generation over time
    """
    months = np.arange(1, years * 12 + 1)
    monthly_rate = (1 + expected_cagr / 100) ** (1 / 12) - 1
    
    # SIP calculation: FV = P * [((1 + r)^n - 1) / r] * (1 + r)
    sip_invested = months * monthly_sip
    if monthly_rate > 0:
        sip_wealth = monthly_sip * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
    else:
        sip_wealth = sip_invested.copy()
        
    # Lumpsum calculation: FV = P * (1 + r)^n
    lump_invested = np.full_like(months, lumpsum)
    lump_wealth = lumpsum * ((1 + monthly_rate) ** months)
    
    total_invested = sip_invested + lump_invested
    total_wealth = sip_wealth + lump_wealth
    
    # Inflation adjusted real wealth
    if inflation_rate > 0:
        inflation_factor = (1 + inflation_rate / 100) ** (months / 12)
        real_wealth = total_wealth / inflation_factor
    else:
        real_wealth = total_wealth.copy()
        
    year_points = months / 12
    
    fig = go.Figure()
    
    # Area for Invested Capital
    fig.add_trace(go.Scatter(
        x=year_points,
        y=total_invested,
        mode='lines',
        name='Principal Invested',
        line=dict(color='#64748B', width=2),
        fill='tozeroy',
        fillcolor='rgba(100, 116, 139, 0.15)',
        hovertemplate="Year %{x:.1f}<br>Invested: ₹%{y:,.0f}<extra></extra>"
    ))
    
    # Area for Total Nominal Wealth
    fig.add_trace(go.Scatter(
        x=year_points,
        y=total_wealth,
        mode='lines',
        name='Compound Future Value',
        line=dict(color='#10B981', width=3),
        fill='tonexty',
        fillcolor='rgba(16, 185, 129, 0.2)',
        hovertemplate="Year %{x:.1f}<br>Future Value: ₹%{y:,.0f}<extra></extra>"
    ))
    
    if inflation_rate > 0:
        fig.add_trace(go.Scatter(
            x=year_points,
            y=real_wealth,
            mode='lines',
            name=f'Real Purchasing Power ({inflation_rate}% Infl)',
            line=dict(color='#F59E0B', width=2, dash='dot'),
            hovertemplate="Year %{x:.1f}<br>Real Value: ₹%{y:,.0f}<extra></extra>"
        ))
        
    # Milestones: 10 Lakhs, 50 Lakhs, 1 Crore
    milestones = [1000000, 5000000, 10000000, 50000000]
    for m in milestones:
        if m < total_wealth[-1]:
            # find month reached
            reach_idx = np.where(total_wealth >= m)[0]
            if len(reach_idx) > 0:
                yr = year_points[reach_idx[0]]
                label = f"₹{m/10000000:.1f} Cr" if m >= 10000000 else f"₹{m/100000:.0f} L"
                fig.add_hline(y=m, line_dash="dot", line_color="rgba(255,255,255,0.15)")
                fig.add_annotation(x=yr, y=m, text=f"🎯 {label} @ Yr {yr:.1f}", 
                                   showarrow=True, arrowhead=2, arrowcolor="#10B981",
                                   font=dict(color="#10B981", size=10))

    fig.update_layout(
        title=dict(text="<b>Compound Wealth Accumulation Curve</b>", font=dict(size=14, color='#F8FAFC')),
        xaxis_title="Investment Horizon (Years)",
        yaxis_title="Portfolio Value (₹)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(size=10, color='#94A3B8'))
    )
    return apply_chart_theme(fig, height=400), total_invested[-1], total_wealth[-1], real_wealth[-1]
