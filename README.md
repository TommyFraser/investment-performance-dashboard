# Investment Performance Dashboard

An interactive web dashboard built with Python and Streamlit that visualises multi-asset portfolio performance against a benchmark, including returns, drawdown, rolling averages, and asset allocation.

## What it does

The dashboard displays:

- **Portfolio vs Benchmark Growth** — compounded growth of $100 invested over time
- **Monthly Excess Return** — how much the portfolio beat or missed the benchmark each month
- **Rolling 3-Month Average Return** — smoothed trend for both portfolio and benchmark
- **Portfolio Drawdown** — how far the portfolio has fallen from its previous peak
- **Asset Allocation Pie Chart** — latest split across Australian Equities, International Equities, Fixed Income, Cash, and Property
- **Summary KPIs** — total return, benchmark return, excess return, average monthly return, volatility, and max drawdown
- **Date range filter** — sidebar slider to zoom into any period

## Data

The dataset covers **January 2020 to April 2026** (76 months) and is modelled on a large Australian multi-asset institutional fund.

| File | Description |
|------|-------------|
| `investment_data.csv` | Combined file used by the app |
| `portfolio_returns.csv` | Monthly portfolio and benchmark returns |
| `asset_allocation.csv` | Monthly asset allocation weights |
| `investment_data_backup.csv` | Backup copy of the combined file |

### Data sources and methodology

Monthly returns are synthetic distributions anchored to confirmed public figures:

- **Portfolio** — annual compounded returns match published [AustralianSuper Balanced](https://www.australiansuper.com/compare-us/our-performance) crediting rates (FY2021–FY2025). April 2026 uses the published 2.51% monthly figure.
- **Benchmark** — annual compounded returns match confirmed [S&P/ASX 200](https://au.finance.yahoo.com/quote/%5EAXJO/history/) calendar year returns (CY2020–CY2024).
- **Asset allocation** — approximate weights based on AustralianSuper's publicly stated ~70% growth / 30% defensive strategic asset allocation ranges.

Key market events reflected in the monthly patterns:

| Period | Event |
|--------|-------|
| Feb–Mar 2020 | COVID-19 crash |
| Apr–May 2020 | Government stimulus recovery |
| Nov 2020 | Vaccine announcement rally |
| 2021 | Post-COVID bull market |
| Jan–Jun 2022 | RBA rate rise bear market |
| 2023–2024 | Recovery and AI-driven equity rally |

## Tech stack

| Library | Purpose |
|---------|---------|
| [Streamlit](https://streamlit.io) | Web app framework |
| [Pandas](https://pandas.pydata.org) | Data manipulation |
| [Plotly Express](https://plotly.com/python/plotly-express/) | Interactive charts |

## Running locally

1. Clone the repo
   ```bash
   git clone https://github.com/TommyFraser/investment-performance-dashboard.git
   cd investment-performance-dashboard
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app
   ```bash
   streamlit run app.py
   ```

4. Open your browser at `http://localhost:8501`

## Deploying online (Streamlit Community Cloud)

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
2. Click **New app** and select this repository
3. Set the main file to `app.py`
4. Click **Deploy**

Anyone with the link can view the dashboard — no installation required.

## Security

API keys and secrets should never be committed to this repo. A `.gitignore` is in place to block `.env` files and `secrets.toml`. See [Streamlit secrets management](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management) if you need to add credentials for a deployed app.
