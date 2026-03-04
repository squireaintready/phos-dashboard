"""
First Phosphate Corp (CSE: PHOS) — Financial Analysis Dashboard
Interactive Streamlit app built from comprehensive Excel financial model.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import openpyxl

st.set_page_config(
    page_title="PHOS Financial Dashboard",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #0f3460;
        margin: 5px 0;
    }
    .metric-value { font-size: 28px; font-weight: 700; color: #e94560; }
    .metric-label { font-size: 13px; color: #a0a0a0; margin-top: 4px; }
    .section-header { 
        font-size: 24px; font-weight: 700; 
        border-bottom: 2px solid #e94560; 
        padding-bottom: 8px; margin: 30px 0 15px 0;
    }
    div[data-testid="stMetricValue"] { font-size: 24px; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    wb = openpyxl.load_workbook("data.xlsx", data_only=True)
    sheets = {}
    for name in wb.sheetnames:
        ws = wb[name]
        data = []
        for row in ws.iter_rows(values_only=True):
            data.append(list(row))
        sheets[name] = data
    return sheets


def parse_number(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    return None


def fmt_cad(val, decimals=1):
    if val is None:
        return "N/A"
    if abs(val) >= 1_000_000_000:
        return f"C${val/1_000_000_000:.{decimals}f}B"
    if abs(val) >= 1_000_000:
        return f"C${val/1_000_000:.{decimals}f}M"
    if abs(val) >= 1_000:
        return f"C${val/1_000:.{decimals}f}K"
    return f"C${val:,.{decimals}f}"


def fmt_pct(val):
    if val is None:
        return "N/A"
    return f"{val*100:.1f}%"


data = load_data()

# --- Sidebar ---
st.sidebar.image("https://img.shields.io/badge/CSE-PHOS-e94560?style=for-the-badge", width=120)
st.sidebar.title("⛏️ PHOS Dashboard")
st.sidebar.markdown("**First Phosphate Corp.**")
st.sidebar.markdown("Pre-revenue LFP battery phosphate developer")
st.sidebar.divider()

page = st.sidebar.radio("Navigate", [
    "📊 Overview",
    "📈 Financial Statements",
    "🔥 Cash Burn Analysis",
    "🏢 Peer Comparison",
    "💰 Valuation Model",
    "⚡ Risk & Summary"
])

# ============================================================
# OVERVIEW
# ============================================================
if page == "📊 Overview":
    st.title("⛏️ First Phosphate Corp. (CSE: PHOS)")
    st.caption("Pre-Revenue LFP Battery Phosphate Developer | Quebec, Canada | Data from SEDAR+ Filings")
    
    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Share Price", "C$1.05", "↑ 193% 1yr")
    col2.metric("Market Cap", "~C$158M", "FD ~C$202M")
    col3.metric("Cash Position", "C$20.0M", "Q3 FY26")
    col4.metric("PEA NPV (8%)", "C$1.59B", "After-tax")
    col5.metric("Mkt Cap / NPV", "~11%", "LFP premium")
    
    st.divider()
    
    # Two column layout
    left, right = st.columns(2)
    
    with left:
        st.subheader("💵 Cash Position Over Time")
        quarters = ["Q4 FY24", "Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26", "Q3 FY26"]
        cash = [7496238, 1651673, 410444, 149983, 1873550, 3173855, 7590632, 19983238]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=quarters, y=[c/1e6 for c in cash],
            marker_color=['#e94560' if c < 1e6 else '#0f3460' for c in cash],
            text=[f"${c/1e6:.1f}M" for c in cash],
            textposition='outside'
        ))
        fig.update_layout(
            yaxis_title="Cash (C$ Millions)",
            template="plotly_dark",
            height=350,
            margin=dict(t=20, b=40),
            yaxis=dict(gridcolor='#333')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with right:
        st.subheader("📉 Share Dilution")
        shares = [73786772, 74867570, 76103368, 77198802, 89947551, 97023899, 123546512, 151220000]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=quarters, y=[s/1e6 for s in shares],
            mode='lines+markers+text',
            line=dict(color='#e94560', width=3),
            marker=dict(size=10),
            text=[f"{s/1e6:.0f}M" for s in shares],
            textposition='top center'
        ))
        fig.update_layout(
            yaxis_title="Shares Outstanding (Millions)",
            template="plotly_dark",
            height=350,
            margin=dict(t=20, b=40),
            yaxis=dict(gridcolor='#333')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Investment thesis
    st.subheader("🎯 Investment Thesis")
    bull, base, bear = st.columns(3)
    with bull:
        st.success("**🟢 Bull Case — C$1.84/sh**\n\n"
                   "FS confirms PEA → 20% NPV discount\n"
                   "OEM partnership / offtake secured\n"
                   "LFP demand accelerates")
    with base:
        st.info("**🔵 Base Case — C$1.01/sh**\n\n"
               "Current market pricing (~11% NPV)\n"
               "Drill program progresses on schedule\n"
               "LFP premium maintained")
    with bear:
        st.error("**🔴 Bear Case — C$0.28/sh**\n\n"
                "Resource downgrade in PFS\n"
                "Capex funding failure\n"
                "3% NPV discount (typical PEA explorer)")

# ============================================================
# FINANCIAL STATEMENTS
# ============================================================
elif page == "📈 Financial Statements":
    st.title("📈 Financial Statements")
    st.caption("All figures in CAD | Source: SEDAR+ Annual & Interim Filings")
    
    tab1, tab2, tab3 = st.tabs(["Balance Sheet", "Income Statement", "Key Ratios"])
    
    with tab1:
        periods = ["FY2024", "FY2025", "Q1 FY26", "Q2 FY26", "Q3 FY26"]
        
        # Assets chart
        st.subheader("Total Assets vs Liabilities")
        assets = [12995758, 7452772, 8735500, 14682667, 25126133]
        liabs = [3684258, 1063172, 809820, 758567, 1235763]
        equity = [9311500, 6389600, 7925680, 13924100, 23890370]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(name="Total Assets", x=periods, y=[a/1e6 for a in assets], 
                            marker_color='#0f3460', text=[f"${a/1e6:.1f}M" for a in assets], textposition='outside'))
        fig.add_trace(go.Bar(name="Liabilities", x=periods, y=[l/1e6 for l in liabs], 
                            marker_color='#e94560', text=[f"${l/1e6:.1f}M" for l in liabs], textposition='outside'))
        fig.add_trace(go.Scatter(name="Equity", x=periods, y=[e/1e6 for e in equity],
                               mode='lines+markers', line=dict(color='#53d769', width=3)), secondary_y=True)
        fig.update_layout(template="plotly_dark", height=400, barmode='group',
                         margin=dict(t=30, b=40), legend=dict(orientation="h", y=1.1))
        fig.update_yaxes(title_text="C$ Millions", secondary_y=False, gridcolor='#333')
        fig.update_yaxes(title_text="Equity (C$M)", secondary_y=True, gridcolor='#333')
        st.plotly_chart(fig, use_container_width=True)
        
        # Balance sheet table
        st.subheader("Balance Sheet Detail")
        bs_data = {
            "Line Item": ["Cash & Equivalents", "Prepaid Expenses", "Tax Credits", "Total Current Assets",
                         "E&E Assets", "Total Assets", "Total Liabilities", "Shareholders' Equity",
                         "Book Value / Share"],
            "FY2024": ["$7.50M", "$0.41M", "$0", "$8.97M", "$3.56M", "$13.0M", "$3.68M", "$9.31M", "$0.126"],
            "FY2025": ["$1.87M", "$0.16M", "$1.24M", "$3.69M", "$3.59M", "$7.45M", "$1.06M", "$6.39M", "$0.071"],
            "Q3 FY26": ["$19.98M", "$0.79M", "$0.35M", "$21.33M", "$3.59M", "$25.13M", "$1.24M", "$23.89M", "$0.158"],
        }
        st.dataframe(pd.DataFrame(bs_data), use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Net Loss Trend")
        loss_q = ["Q4 FY24", "Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26"]
        loss_v = [-3764747, -4185217, -170997, -1681986, -1589214, -1748338, -2006009]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=loss_q, y=[abs(v)/1e6 for v in loss_v],
            marker_color=['#e94560' if abs(v) > 2e6 else '#ff8a5c' for v in loss_v],
            text=[f"$(${abs(v)/1e6:.1f}M)" for v in loss_v],
            textposition='outside'
        ))
        fig.update_layout(
            yaxis_title="Net Loss (C$ Millions)",
            template="plotly_dark", height=350,
            margin=dict(t=20, b=40),
            yaxis=dict(gridcolor='#333')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("**Note:** Q2 FY25 net loss of only $171K was anomalous — likely one-time gain or timing. "
               "Annualized burn rate is ~C$12.7M based on recent quarters.")
    
    with tab3:
        st.subheader("Key Financial Ratios")
        ratio_data = {
            "Ratio": ["Current Ratio", "Debt/Equity", "Cash Burn (Qtr)", "Cash Runway", 
                      "P/B Ratio", "Working Capital"],
            "FY2024": ["2.7x", "0.40x", "~$3.8M", "~25 months", "N/A", "$5.3M"],
            "FY2025": ["4.0x", "0.17x", "~$2.7M", "~3 months", "~14x", "$2.6M"],
            "Q3 FY26": ["17.3x", "0.05x", "~$2.7M", "~24+ months", "~6.6x", "$20.1M"],
        }
        st.dataframe(pd.DataFrame(ratio_data), use_container_width=True, hide_index=True)

# ============================================================
# CASH BURN
# ============================================================
elif page == "🔥 Cash Burn Analysis":
    st.title("🔥 Cash Burn & Runway Analysis")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Quarterly Burn", "~C$2.7M", "Operating expenses")
    col2.metric("Cash (est. Jan 2026)", "~C$32.6M", "Post Dec/Jan raises")
    col3.metric("Runway (Base)", "~30 months", "Through mid-2028")
    
    st.divider()
    
    # Runway scenarios
    st.subheader("📊 Runway Scenarios")
    
    scenarios = {
        "Scenario": ["🟢 Bull (Lower Burn)", "🔵 Base Case", "🔴 Bear (Drill Ramp)"],
        "Quarterly Burn": ["C$2.5M", "C$3.2M", "C$4.5M"],
        "Runway": ["39 months", "30.5 months", "21.7 months"],
        "Cash Runs Out": ["Apr 2029", "Jul 2028", "Oct 2027"],
    }
    st.dataframe(pd.DataFrame(scenarios), use_container_width=True, hide_index=True)
    
    # Burn visualization
    st.subheader("💸 Cash Burn vs Equity Raised")
    quarters = ["Q4 FY24", "Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25", "Q1 FY26", "Q2 FY26"]
    burn = [3764747, 4185217, 170997, 1681986, 1589214, 1748338, 2006009]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Net Loss", x=quarters, y=[b/1e6 for b in burn],
        marker_color='#e94560',
        text=[f"${b/1e6:.1f}M" for b in burn],
        textposition='outside'
    ))
    fig.update_layout(template="plotly_dark", height=350, 
                     yaxis_title="C$ Millions", margin=dict(t=30, b=40),
                     yaxis=dict(gridcolor='#333'))
    st.plotly_chart(fig, use_container_width=True)
    
    # Dilution tracker
    st.subheader("📈 Cumulative Dilution from FY24 Base")
    cum_dil = [1.5, 3.1, 4.6, 21.9, 31.5, 67.4, 104.9]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=quarters, y=cum_dil,
        mode='lines+markers+text',
        fill='tozeroy',
        line=dict(color='#e94560', width=3),
        text=[f"{d:.0f}%" for d in cum_dil],
        textposition='top center',
        fillcolor='rgba(233, 69, 96, 0.2)'
    ))
    fig.update_layout(template="plotly_dark", height=300,
                     yaxis_title="Cumulative Dilution %", margin=dict(t=20, b=40),
                     yaxis=dict(gridcolor='#333'))
    st.plotly_chart(fig, use_container_width=True)
    
    st.warning("⚠️ **Capex Gap:** PEA estimates C$675M+ construction cost vs ~C$33M current cash. "
              "Project financing, government grants, or JV partnership required.")

# ============================================================
# PEER COMPARISON
# ============================================================
elif page == "🏢 Peer Comparison":
    st.title("🏢 Peer Comparison")
    st.caption("Phosphate / LFP Battery Supply Chain Comparables | Data as of Mar 2026")
    
    tab1, tab2 = st.tabs(["Peer Table", "Valuation Chart"])
    
    with tab1:
        peers = {
            "Company": ["First Phosphate\n(PHOS)", "Arianne Phosphate\n(DAN)", "Itafos\n(IFOS)", "Mosaic\n(MOS)"],
            "Type": ["Junior Dev", "Junior Dev", "Mid Producer", "Large Producer"],
            "Market Cap": ["C$158M", "C$55M", "C$609M", "US$8.8B"],
            "Stage": ["Pre-Rev (PEA)", "Pre-Rev (FS)", "Producing", "Producing"],
            "LFP Focus": ["✅ Core", "Exploring", "❌", "❌"],
            "Cash": ["C$20M", "~C$2M", "N/A", "N/A"],
            "Cash Runway": ["24+ mo", "~6 mo", "N/A (profitable)", "N/A (profitable)"],
            "1yr Return": ["+193%", "+28%", "N/A", "N/A"],
            "NPV Discount": ["~11%", "~1.5%", "N/A", "N/A"],
        }
        st.dataframe(pd.DataFrame(peers), use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Market Cap / NPV Comparison")
        companies = ["PHOS\n(Phosphate)", "DAN\n(Phosphate)", "NMG\n(Graphite)", "PMET\n(Lithium)"]
        npv_pct = [11, 1.5, 34, 37]
        colors = ['#e94560', '#0f3460', '#53d769', '#ff8a5c']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=companies, y=npv_pct,
            marker_color=colors,
            text=[f"{p}%" for p in npv_pct],
            textposition='outside',
            textfont=dict(size=16)
        ))
        fig.update_layout(
            template="plotly_dark", height=400,
            yaxis_title="Market Cap as % of NPV",
            margin=dict(t=30, b=40),
            yaxis=dict(gridcolor='#333')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("**Key Insight:** PHOS is the cheapest entry point in the North American LFP supply chain "
                  "at ~11% of NPV, compared to 34% (NMG) and 37% (PMET). This suggests either an opportunity "
                  "or the market is pricing in higher execution risk.")

# ============================================================
# VALUATION MODEL
# ============================================================
elif page == "💰 Valuation Model":
    st.title("💰 Valuation Model")
    st.caption("NAV Discount Framework | Pre-Revenue Explorer/Developer | Not investment advice")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("PEA NPV (8%)", "C$1.59B")
    col2.metric("Share Price", "C$1.05")
    col3.metric("Shares (FD)", "~192.4M")
    col4.metric("Mkt Cap / NPV", "~12.7%")
    
    st.divider()
    
    # Interactive NPV slider
    st.subheader("🎚️ NAV Discount Sensitivity")
    npv_pct = st.slider("Select % of NPV applied", 3, 30, 11, 1)
    
    npv = 1_590_000_000
    implied_nav = npv * (npv_pct / 100)
    implied_price_basic = implied_nav / 173_267_217
    implied_price_fd = implied_nav / 192_400_000
    upside = (implied_price_fd / 1.05) - 1
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Implied NAV", fmt_cad(implied_nav))
    c2.metric("Implied Price (FD)", f"C${implied_price_fd:.2f}", 
              f"{'↑' if upside > 0 else '↓'} {abs(upside)*100:.0f}% vs C$1.05")
    c3.metric("Assessment", 
              "Very Cheap" if npv_pct <= 3 else "Cheap" if npv_pct <= 5 else 
              "Fair" if npv_pct <= 7 else "~Current" if npv_pct <= 12 else 
              "Rich" if npv_pct <= 15 else "Advanced Stage")
    
    # Sensitivity table
    st.subheader("📊 Full Sensitivity Table")
    pcts = [3, 5, 7, 10, 11, 15, 20, 25, 30]
    sens_data = {
        "NPV %": [f"{p}%" for p in pcts],
        "Implied NAV": [fmt_cad(npv * p / 100) for p in pcts],
        "Price (Basic)": [f"C${npv * p / 100 / 173267217:.2f}" for p in pcts],
        "Price (FD)": [f"C${npv * p / 100 / 192400000:.2f}" for p in pcts],
        "vs C$1.05": [f"{'+'if (npv*p/100/192400000/1.05-1)>0 else ''}{(npv*p/100/192400000/1.05-1)*100:.0f}%" for p in pcts],
        "Assessment": ["Very Cheap", "Cheap", "Fair", "Slightly Rich", "~Current", 
                       "Rich", "Advanced", "FS Complete", "Construction"],
    }
    st.dataframe(pd.DataFrame(sens_data), use_container_width=True, hide_index=True)
    
    # Scenario chart
    st.subheader("🎯 Scenario Analysis")
    fig = go.Figure()
    scenarios = ["Bear\n(3% NPV)", "Base\n(11% NPV)", "Bull\n(20% NPV)"]
    prices = [0.28, 1.01, 1.84]
    colors = ['#e94560', '#0f3460', '#53d769']
    
    fig.add_trace(go.Bar(
        x=scenarios, y=prices, marker_color=colors,
        text=[f"C${p:.2f}" for p in prices],
        textposition='outside', textfont=dict(size=18)
    ))
    fig.add_hline(y=1.05, line_dash="dash", line_color="white", 
                  annotation_text="Current: C$1.05")
    fig.update_layout(template="plotly_dark", height=350,
                     yaxis_title="Implied Share Price (C$)",
                     margin=dict(t=30, b=40), yaxis=dict(gridcolor='#333'))
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# RISK & SUMMARY
# ============================================================
elif page == "⚡ Risk & Summary":
    st.title("⚡ Analysis & Summary")
    
    st.subheader("📋 Key Findings")
    findings = {
        "Section": ["Financial Statements", "Financial Statements", "Cash Burn", "Cash Burn",
                    "Peer Analysis", "Valuation"],
        "Finding": [
            "Rapid balance sheet growth from equity raises",
            "Operating losses accelerating",
            "Cash runway adequate if burn stable",
            "Massive capex gap unfunded",
            "Only pure-play LFP phosphate junior",
            "Significant upside in bull scenario"
        ],
        "Key Metric": [
            "Assets: C$7.5M → C$25.1M (+237%)",
            "Net Loss annualizing ~C$12.7M",
            "~24 months at C$2.7M/qtr",
            "C$675M+ vs C$33M cash",
            "No direct comparable exists",
            "Bear C$0.28 → Bull C$1.84"
        ],
        "Risk": ["🟡 Medium", "🟡 Medium", "🟡 Medium", "🔴 HIGH", "🟢 Low", "🟡 Medium"],
    }
    st.dataframe(pd.DataFrame(findings), use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Risk framework
    st.subheader("⚠️ Risk / Reward Framework")
    
    risks = {
        "Risk": ["Resource downgrade in PFS/FS", "Capex funding failure", 
                 "Continued dilution", "LFP chemistry shift"],
        "Severity": ["🔴 High", "🔴 Critical", "🔴 High", "🟡 Medium"],
        "Probability": ["🟡 Medium", "🟡 Medium", "🔴 High", "🟢 Low"],
        "Mitigation": [
            "30,000m drill program underway",
            "Govt grants, JV potential",
            "None — inherent to model",
            "LFP gaining share; fertilizer fallback"
        ],
    }
    st.dataframe(pd.DataFrame(risks), use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Catalysts
    st.subheader("🚀 Upcoming Catalysts")
    catalysts = [
        "**Q4 FY26 Results** (Feb 2026) — Full-year financials + updated burn rate",
        "**PFS/FS Completion** (2026-2027) — Major re-rating event if resource upgraded",
        "**OEM Partnership / Offtake** — LFP battery manufacturer agreement",
        "**Federal Critical Minerals Grant** — C$4.9M from NRCan",
        "**ADR Listing** — US market access (FRSPF on OTCQX already active)",
        "**30,000m Drill Program** — Resource upgrade from 83% Inferred → Indicated",
    ]
    for c in catalysts:
        st.markdown(f"• {c}")
    
    st.divider()
    st.subheader("📝 Conclusion")
    st.markdown("""
    First Phosphate trades at a **premium to traditional phosphate juniors** (~11% of NPV vs <5% typical) 
    but at a **discount to the broader LFP supply chain** (NMG 34%, PMET 37%). The premium is justified by:
    
    1. **Only pure-play LFP phosphate junior** in North America
    2. **Strong PEA economics** (33% IRR, 2.9yr payback)  
    3. **Recent catalysts** (CSE25 listing, critical minerals designation, federal grant)
    
    **Key risk** remains the C$675M+ capex gap and continued dilution. The stock is a **high-conviction 
    speculative buy** for investors with a 3-5 year horizon who believe in the LFP battery thesis.
    """)

# Footer
st.sidebar.divider()
st.sidebar.caption("Built by Samuel Jo")
st.sidebar.caption("Data: SEDAR+ filings | Not investment advice")
st.sidebar.caption("[GitHub](https://github.com/squireaintready/phos-dashboard)")
