"""This script is a quick data inspection tool to validate raw parquet files before integrating them into a data pipeline.

Ce script permet d’inspecter rapidement un fichier parquet afin de valider les données avant leur intégration dans un pipeline."""

import pandas as pd
from pathlib import Path

def inspect_parquet(path: str, n: int = 5):
    p = Path(path) #convert string path to Path object for easier file handling
    if not p.exists(): #check if file exists before attemping to read
        print(f"File doesn't exist: {p}")
        return

    df = pd.read_parquet(p)
    #print basic metadata and preview of the dataset
    print(f"File: {p}")
    print(f"Number of rows: {len(df)}")
    print("5 first rows:")
    print(df.head(n))

if __name__ == "__main__":
    #run quick inspection on a raw DeFi dataset (debug, data validation step)
    inspect_parquet("data/raw/defi_prices_prices_20251202_133359.parquet")
