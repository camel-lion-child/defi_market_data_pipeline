import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

BASE_URL = "https://api.binance.com/api/v3/klines"
RAW_DIR = Path("data/raw")


def fetch_daily_close(symbol: str, limit: int = 1000) -> pd.DataFrame:
    params = {
        "symbol": symbol,
        "interval": "1d",
        "limit": limit
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_volume",
        "taker_buy_quote_volume",
        "ignore"
    ])

    df["date"] = pd.to_datetime(df["open_time"], unit="ms").dt.normalize()
    df["close"] = df["close"].astype(float)

    return df[["date", "close"]]


def main():
    print("Fetching BTC and ETH daily prices from Binance...")

    btc_df = fetch_daily_close("BTCUSDT").rename(columns={"close": "btc_close"})
    eth_df = fetch_daily_close("ETHUSDT").rename(columns={"close": "eth_close"})

    market_df = btc_df.merge(eth_df, on="date", how="inner")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RAW_DIR / "market_prices.parquet"
    market_df.to_parquet(output_path, index=False)

    print(f"Saved market prices to {output_path}")
    print(market_df.head())


if __name__ == "__main__":
    main()
