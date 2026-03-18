""" This script fetches daily BTC and ETH prices from Binance, aligns them into a single time series, 
and stores the data as a parquet file for downstream processing.

Ce script récupère les prix quotidiens du BTC et de l’ETH via Binance, les aligne dans une série temporelle commune 
et les sauvegarde en format parquet pour traitement ultérieur."""

import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

BASE_URL = "https://api.binance.com/api/v3/klines" #Binance API endpoint for historical price data (klines)
RAW_DIR = Path("data/raw")


def fetch_daily_close(symbol: str, limit: int = 1000) -> pd.DataFrame:
    #define API parameters , daily interval
    params = {
        "symbol": symbol,
        "interval": "1d",
        "limit": limit
    }

    response = requests.get(BASE_URL, params=params) #send request to Binance API
    response.raise_for_status()

    data = response.json() #parse JSON response into Dataframe

    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_volume",
        "taker_buy_quote_volume",
        "ignore"
    ])

    df["date"] = pd.to_datetime(df["open_time"], unit="ms").dt.normalize() #convert timestamp to daily date
    df["close"] = df["close"].astype(float)

    return df[["date", "close"]]


def main():
    print("Fetching BTC and ETH daily prices from Binance...")

    #fetch BTC & ETH daily closing prices
    btc_df = fetch_daily_close("BTCUSDT").rename(columns={"close": "btc_close"})
    eth_df = fetch_daily_close("ETHUSDT").rename(columns={"close": "eth_close"})

    market_df = btc_df.merge(eth_df, on="date", how="inner") #merge both datasets on date to align time series

    RAW_DIR.mkdir(parents=True, exist_ok=True) #ensure output directory exists
    output_path = RAW_DIR / "market_prices.parquet" #save combined dataset as parquet (raw layer)
    market_df.to_parquet(output_path, index=False)

    print(f"Saved market prices to {output_path}")
    print(market_df.head())


if __name__ == "__main__":
    main() #entry point: fetch & store BTC/ETH market data
