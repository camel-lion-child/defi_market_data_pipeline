import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def load_latest_file(prefix: str) -> Path:
    """
    Lấy file mới nhất bắt đầu bằng prefix trong data/raw/.
    Ví dụ prefix: 'defi_core_tvl', 'defi_prices'.
    """
    files = sorted(RAW_DIR.glob(f"{prefix}*.parquet"))
    if not files:
        raise FileNotFoundError(f"No files for prefix {prefix}")
    return files[-1]


def merge_tvl_prices():
    # Load TVL file
    tvl_file = load_latest_file("defi_core_tvl")
    tvl_df = pd.read_parquet(tvl_file)

    # Load price file
    price_file = load_latest_file("defi_prices")
    prices_df = pd.read_parquet(price_file)

    # Merge on date
    merged = tvl_df.merge(
        prices_df,
        how="left",
        left_on="date",
        right_on="datetime"
    )

    # Drop duplicate columns
    merged = merged.drop(columns=["datetime"], errors="ignore")

    # Save output
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / "merged_tvl_prices.parquet"
    merged.to_parquet(out_path, index=False)

    print(f"Saved merged file to {out_path}")
    print(merged.head())


if __name__ == "__main__":
    merge_tvl_prices()
