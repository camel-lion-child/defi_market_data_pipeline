# DeFi Market Data Pipeline (TVL + Prices)

This project is a small **Data Engineering** pipeline for DeFi.

It does three main things:

1. Fetch **TVL history** for core DeFi protocols (Aave v3, Uniswap v3, Curve) from the free **DefiLlama API**.
2. Fetch **price history** for the same tokens (AAVE, UNI, CRV) from the free **CoinGecko API**.
3. Merge TVL and prices into a processed dataset that can be used for analysis (risk, liquidity, market structure, etc.).

---

## Project Structure

```text
defi_market_data_pipeline/
│
├── src/
│   ├── defillama_tvl.py            # Extract TVL from DefiLlama
│   ├── extract/
│   │   └── coingecko_prices.py     # Extract prices from CoinGecko
│   ├── transform/
│   │   └── merge_tvl_prices.py     # Merge TVL + prices
│   └── inspect_parquet.py          # Helper to inspect parquet files
│
├── data/
│   ├── raw/                        # Raw API outputs (parquet)
│   └── processed/                  # Cleaned / merged data
│
├── venv/                           # Local virtual environment (not needed for review)
├── requirements.txt                # Python dependencies
└── README.md
