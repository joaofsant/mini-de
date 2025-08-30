# dashboard.py
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DOCS = Path("docs"); DOCS.mkdir(parents=True, exist_ok=True)
PROC = Path("data/processed")

def latest_parquet():
    parts = sorted(PROC.glob("date=*/hn.parquet"))
    if not parts:
        raise SystemExit("No processed data found. Run: python storage.py")
    return parts[-1]

def build_dashboard():
    pf = latest_parquet()
    df = pd.read_parquet(pf, engine="fastparquet")

    top = df["domain"].value_counts().head(10)
    plt.figure()
    top.plot(kind="bar", title="Top domains")
    plt.tight_layout()
    (DOCS / "top_domains.png").unlink(missing_ok=True)
    plt.savefig(DOCS / "top_domains.png")

    titles = df["title"].fillna("n/a").head(10).to_list()
    html = f"""<html><head><meta charset='utf-8'><title>HN Mini</title></head>
    <body style="font-family:-apple-system,Arial,sans-serif;max-width:800px;margin:40px auto;">
      <h1>Hacker News — Mini Dashboard</h1>
      <p>Rows: {len(df)}</p>
      <p>Source: {pf}</p>
      <img src="top_domains.png" alt="Top Domains" style="max-width:100%;height:auto;"/>
      <h2>Sample titles</h2>
      <ul>{''.join(f'<li>{t}</li>' for t in titles)}</ul>
    </body></html>"""
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    print("Dashboard generated → docs/index.html")

if __name__ == "__main__":
    build_dashboard()