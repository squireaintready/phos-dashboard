# PHOS Financial Dashboard ⛏️

Interactive financial analysis dashboard for **First Phosphate Corp. (CSE: PHOS | OTCQX: FRSPF)** — a pre-revenue LFP battery phosphate developer in Quebec, Canada.

## Live Demo

🔗 **[View Dashboard](https://phos-dashboard.streamlit.app)** *(deploy on Streamlit Cloud)*

## Features

- **📊 Overview** — Key metrics, cash position chart, dilution tracker, investment thesis
- **📈 Financial Statements** — Balance sheet, income statement, key ratios across 5 periods
- **🔥 Cash Burn Analysis** — Quarterly burn tracking, runway scenarios, cumulative dilution
- **🏢 Peer Comparison** — PHOS vs Arianne, Itafos, Mosaic + LFP supply chain comps
- **💰 Valuation Model** — Interactive NAV discount slider, sensitivity table, scenario analysis
- **⚡ Risk & Summary** — Risk framework, upcoming catalysts, investment conclusion

## Screenshots

*Dashboard features interactive Plotly charts, dark theme, and responsive layout.*

## Tech Stack

- **Framework:** Streamlit
- **Charts:** Plotly
- **Data:** Pandas, OpenPyXL
- **Source Data:** SEDAR+ annual & interim filings (7 PDFs → Excel model)

## Data Sources

All financial data sourced from official SEDAR+ filings:
- FY2024 & FY2025 audited annual reports
- Q1, Q2, Q3 FY2026 interim financial statements
- Management Discussion & Analysis (MDA) for each period
- Peer data from public market sources (Mar 2026)

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub and select this repo
4. Set main file: `app.py`
5. Deploy!

## Disclaimer

This dashboard is for **educational and personal portfolio purposes only**. It does not constitute investment advice. All data is sourced from public filings and may contain errors. Do your own research.

## Author

**Samuel Jo** — [GitHub](https://github.com/squireaintready) · [LinkedIn](https://linkedin.com/in/samuel-jo)
