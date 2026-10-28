"""
styles.py - Modern Luxury Financial Dark UI System for Streamlit
"""

CUSTOM_CSS = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Global Reset & Base */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #F3F4F6;
}

/* Background gradient */
.stApp {
    background: radial-gradient(circle at 15% 10%, rgba(16, 185, 129, 0.04) 0%, transparent 40%),
                radial-gradient(circle at 85% 15%, rgba(59, 130, 246, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 50% 90%, rgba(139, 92, 246, 0.04) 0%, transparent 50%),
                #090D16;
}

/* Header Container */
.dash-header {
    background: linear-gradient(135deg, rgba(17, 24, 39, 0.9) 0%, rgba(31, 41, 55, 0.6) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px 30px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.dash-title-group h1 {
    font-size: 2.1rem;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(135deg, #FFFFFF 0%, #E2E8F0 50%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
}

.dash-title-group p {
    font-size: 0.95rem;
    color: #94A3B8;
    margin: 6px 0 0 0;
    font-weight: 400;
}

.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.badge-live {
    background: rgba(16, 185, 129, 0.12);
    color: #10B981;
    border: 1px solid rgba(16, 185, 129, 0.3);
    box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
}

.badge-pulse {
    width: 8px;
    height: 8px;
    background-color: #10B981;
    border-radius: 50%;
    animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* Metric Cards */
.kpi-card {
    background: linear-gradient(145deg, rgba(17, 24, 39, 0.85) 0%, rgba(24, 33, 49, 0.65) 100%);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 8px 20px -6px rgba(0, 0, 0, 0.4);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    overflow: hidden;
    height: 100%;
}

.kpi-card:hover {
    transform: translateY(-3px);
    border-color: rgba(59, 130, 246, 0.3);
    box-shadow: 0 14px 28px -8px rgba(0, 0, 0, 0.6), 0 0 20px rgba(59, 130, 246, 0.15);
}

.kpi-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.kpi-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.kpi-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
}

.kpi-value {
    font-size: 1.85rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.03em;
    line-height: 1.1;
    font-family: 'JetBrains Mono', monospace;
}

.kpi-subtext {
    font-size: 0.78rem;
    color: #64748B;
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.kpi-delta-up {
    color: #10B981;
    font-weight: 600;
}

.kpi-delta-down {
    color: #EF4444;
    font-weight: 600;
}

/* Insight Card Box (replaces Power BI left text box) */
.insights-banner {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(20, 30, 50, 0.8) 100%);
    border-left: 4px solid #3B82F6;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    border-right: 1px solid rgba(255, 255, 255, 0.06);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 22px;
}

.insights-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.95rem;
    font-weight: 700;
    color: #38BDF8;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.insight-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 0.88rem;
    color: #CBD5E1;
    margin-bottom: 8px;
    line-height: 1.45;
}

.insight-bullet {
    width: 6px;
    height: 6px;
    background-color: #38BDF8;
    border-radius: 50%;
    margin-top: 6px;
    flex-shrink: 0;
}

/* Glass Card Container */
.glass-panel {
    background: linear-gradient(145deg, rgba(17, 24, 39, 0.75) 0%, rgba(24, 33, 49, 0.5) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 22px;
    box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.35);
}

.panel-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.panel-subtitle {
    font-size: 0.8rem;
    color: #64748B;
    font-weight: 400;
}

/* Streamlit Tabs Customization */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(17, 24, 39, 0.7);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 20px;
}

.stTabs [data-baseweb="tab"] {
    height: 42px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 8px;
    color: #94A3B8;
    font-weight: 600;
    font-size: 0.88rem;
    border: none;
    padding: 0 18px;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.25) 0%, rgba(37, 99, 235, 0.35) 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(59, 130, 246, 0.4) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2) !important;
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B0F19 0%, #0F172A 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

[data-testid="stSidebar"] .stMarkdown h2, 
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #F8FAFC;
    font-weight: 700;
    letter-spacing: -0.02em;
}

/* Modern Table Enhancements */
.dataframe {
    border-collapse: separate !important;
    border-spacing: 0 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    font-size: 0.85rem !important;
}

.dataframe th {
    background-color: #1F2937 !important;
    color: #E2E8F0 !important;
    padding: 10px 14px !important;
    font-weight: 600 !important;
}

.dataframe td {
    padding: 10px 14px !important;
    border-top: 1px solid rgba(255, 255, 255, 0.04) !important;
}

/* Button Styling */
.stButton>button {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    color: white;
    font-weight: 600;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 8px 18px;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
    transition: all 0.2s ease;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.45);
    transform: translateY(-1px);
}

/* Tooltip & Help Icon */
.stTooltipIcon {
    color: #64748B;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 7px;
    height: 7px;
}
::-webkit-scrollbar-track {
    background: #090D16;
}
::-webkit-scrollbar-thumb {
    background: #1F2937;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #374151;
}
</style>
"""

def metric_card(title, value, subtext="", delta=None, delta_text="", icon="📊", color="blue"):
    """
    Renders a high-tech glassmorphic metric card
    """
    color_map = {
        "blue": ("rgba(59, 130, 246, 0.15)", "#3B82F6"),
        "green": ("rgba(16, 185, 129, 0.15)", "#10B981"),
        "purple": ("rgba(139, 92, 246, 0.15)", "#8B5CF6"),
        "amber": ("rgba(245, 158, 11, 0.15)", "#F59E0B"),
        "cyan": ("rgba(6, 182, 212, 0.15)", "#06B6D4"),
        "rose": ("rgba(244, 63, 94, 0.15)", "#F43F5E")
    }
    bg_tint, border_tint = color_map.get(color, color_map["blue"])
    
    delta_html = ""
    if delta is not None:
        delta_class = "kpi-delta-up" if delta >= 0 else "kpi-delta-down"
        arrow = "▲" if delta >= 0 else "▼"
        delta_html = f'<span class="{delta_class}">{arrow} {delta_text or f"{delta:.1f}%"}</span>'
    
    return f"""
    <div class="kpi-card" style="border-top: 2px solid {border_tint};">
        <div class="kpi-top">
            <span class="kpi-label">{title}</span>
            <div class="kpi-icon" style="background: {bg_tint};">{icon}</div>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtext">
            {delta_html} {subtext}
        </div>
    </div>
    """
