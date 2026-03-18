"""This script collects historical TVL data from multiple DeFi protocols using the DeFiLlama API, standardizes the data, 
and stores it as versioned parquet files for downstream analysis.

Ce script collecte les données historiques de TVL de plusieurs protocoles DeFi via l’API DeFiLlama, 
les standardise et les sauvegarde en fichiers parquet versionnés pour l’analyse."""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime


BASE_URL = "https://api.llama.fi"


def fetch_protocol_tvl(protocol_slug: str) -> pd.DataFrame:
    #build API endpoint for a specific protocol, ex: AAVE, Uniswap etc...
    url = f"{BASE_URL}/protocol/{protocol_slug}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    history = data.get("tvl", []) #extract 
    if not history:
        print(f"No TVL data for {protocol_slug}")
        return pd.DataFrame()

    df = pd.DataFrame(history)
    df["date"] = pd.to_datetime(df["date"], unit="s")
    df = df.rename(columns={"totalLiquidityUSD": "tvl_usd"})
    df["protocol"] = data.get("name", protocol_slug) #add protocol name for multi-protocol analysis

    return df[["date", "protocol", "tvl_usd"]]


def save_raw(df: pd.DataFrame, name: str) -> Path:
    out_dir = Path("data/raw") #create raw data folder if needed
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S") #generate timestamped filename for versioning
    path = out_dir / f"{name}_tvl_{ts}.parquet" #build output file path
    df.to_parquet(path, index=False) #save to parquet
    return path



if __name__ == "__main__":
    protocols = ["aave-v3", "uniswap-v3", "curve-dex"] #Defi protocol to fetch
    all_df = []

    for slug in protocols: #loop through protocols and collect TVL data
        print(f"Fetching TVL for {slug}...")
        df = fetch_protocol_tvl(slug)
        if not df.empty: #keep only non-empty datasets
            all_df.append(df)

    if not all_df: #handle case where no data was retrieved
        print("No data fetched.")
    else:
        big_df = pd.concat(all_df, ignore_index=True) #combine all protocols into a single dataset
        path = save_raw(big_df, "defi_core") #save raw data for downstream processing
        print(f"Saved TVL data to {path}")
        print(big_df.head())
