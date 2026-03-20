"""I load the latest DeFi TVL (Total Value Locked) and price datasets, merge them on date, and produce a unified dataset for downstream analysis.

Ce script charge les dernières données TVL et de prix DeFi, les fusionne par date, puis génère un dataset unifié pour l’analyse."""


import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def load_latest_file(prefix: str) -> Path:
    #load the most recent parquet file matching a given prefix (useful for versioned & raw timestamped files)
    files = sorted(RAW_DIR.glob(f"{prefix}*.parquet"))
    if not files:
        raise FileNotFoundError(f"No files for prefix {prefix}")
    return files[-1] #return lasted file (last in sorted list)


def merge_tvl_prices():
    #load lagest TVL dataset
    tvl_file = load_latest_file("defi_core_tvl")
    tvl_df = pd.read_parquet(tvl_file)
    #load latest price dataset
    price_file = load_latest_file("defi_prices")
    prices_df = pd.read_parquet(price_file)
    #merge TVL & price data on date (left join keeps all TVL rows even if price is missing)
    merged = tvl_df.merge(
        prices_df,
        how="left",
        left_on="date",
        right_on="datetime"
    )

    merged = merged.drop(columns=["datetime"], errors="ignore") #drop duplicate datetime column after join

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True) #ensure output directory exists
    #save merged dataset
    out_path = PROCESSED_DIR / "merged_tvl_prices.parquet"
    merged.to_parquet(out_path, index=False)

    print(f"Saved merged file to {out_path}")
    print(merged.head())


if __name__ == "__main__":
    merge_tvl_prices() #entry point: merge Defi TVL with price data 
