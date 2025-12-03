import pandas as pd
from pathlib import Path

def inspect_parquet(path: str, n: int = 5):
    p = Path(path)
    if not p.exists():
        print(f"File doesn't exist: {p}")
        return

    df = pd.read_parquet(p)
    print(f"File: {p}")
    print(f"Number of rows: {len(df)}")
    print("5 first rows:")
    print(df.head(n))

if __name__ == "__main__":
    
    inspect_parquet("data/raw/defi_prices_prices_20251202_133359.parquet")
