# DeFi Market Data Pipeline (TVL + Token Prices)

---

Project Highlights

- Built a full ETL pipeline using real DeFi APIs (DefiLlama & CoinGecko)

- Stored raw data in parquet format (industry standard)

- Implemented a transform layer to clean, standardize and merge data

- Performed EDA with rolling averages, correlation and liquidity analysis

- Visualized TVL dynamics across major protocols (Aave, Uniswap, Curve)

---

Tech Stack

- Python (pandas, requests)

- Jupyter / VS Code

- Git & GitHub

- Parquet storage

- API Engineering

- DeFi Protocol Analysis

---

[DefiLlama API] → (Extract) → raw parquet  
[CoinGecko API] → (Extract) → raw parquet  
        ↓  
    (Transform) merge/clean  
        ↓  
    (EDA Notebook)

---

Future Improvements

- Add per-token price mapping for more precise TVL/price alignment

- Store data in DuckDB for fast querying

- Automate the pipeline with Airflow or Prefect

- Deploy a dashboard using Streamlit
