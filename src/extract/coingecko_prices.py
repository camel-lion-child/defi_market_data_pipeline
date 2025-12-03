import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

BASE_URL = "https://api.coingecko.com/api/v3"


def fetch_price_history(coin_id: str, days: int = 90) -> pd.DataFrame:
    
    url = f"{BASE_URL}/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}

    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()

    data = resp.json()
    prices = data.get("prices", [])

    df = pd.DataFrame(prices, columns=["timestamp_ms", "price"])
    df["datetime"] = pd.to_datetime(df["timestamp_ms"], unit="ms")
    df["coin_id"] = coin_id

    return df[["datetime", "coin_id", "price"]]


def save_raw(df: pd.DataFrame, name: str) -> Path:
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = out_dir / f"{name}_prices_{ts}.parquet"
    df.to_parquet(path, index=False)
    return path


if __name__ == "__main__":
    coins = ["aave", "uniswap", "curve-dao-token"]
    all_df = []

    for coin in coins:
        df = fetch_price_history(coin)
        all_df.append(df)

    final_df = pd.concat(all_df, ignore_index=True)
    path = save_raw(final_df, "defi_prices")
    print("Saved prices file:", path)
