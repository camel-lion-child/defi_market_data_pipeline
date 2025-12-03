import requests
import pandas as pd
from pathlib import Path
from datetime import datetime


BASE_URL = "https://api.llama.fi"


def fetch_protocol_tvl(protocol_slug: str) -> pd.DataFrame:
    """
    'aave-v3', 'uniswap-v3', 'curve-dex'.
    """
    url = f"{BASE_URL}/protocol/{protocol_slug}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    history = data.get("tvl", [])
    if not history:
        print(f"No TVL data for {protocol_slug}")
        return pd.DataFrame()

    df = pd.DataFrame(history)
    # 'date' là timestamp (seconds)
    df["date"] = pd.to_datetime(df["date"], unit="s")
    df = df.rename(columns={"totalLiquidityUSD": "tvl_usd"})
    df["protocol"] = data.get("name", protocol_slug)

    return df[["date", "protocol", "tvl_usd"]]


def save_raw(df: pd.DataFrame, name: str) -> Path:
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = out_dir / f"{name}_tvl_{ts}.parquet"
    df.to_parquet(path, index=False)
    return path



if __name__ == "__main__":
    protocols = ["aave-v3", "uniswap-v3", "curve-dex"]
    all_df = []

    for slug in protocols:
        print(f"Fetching TVL for {slug}...")
        df = fetch_protocol_tvl(slug)
        if not df.empty:
            all_df.append(df)

    if not all_df:
        print("No data fetched.")
    else:
        big_df = pd.concat(all_df, ignore_index=True)
        # name = "defi_core"
        path = save_raw(big_df, "defi_core")
        print(f"Saved TVL data to {path}")
        print(big_df.head())
