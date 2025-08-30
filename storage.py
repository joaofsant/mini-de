# storage.py
from pathlib import Path
from transform import transform

PROC_DIR = Path("data/processed"); PROC_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    df = transform()
    out = PROC_DIR / "hn.parquet"
    df.to_parquet(out, index=False, engine="fastparquet")
    print(f"Wrote {len(df)} rows to {out}")

    