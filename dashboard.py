# dashboard.py (top of file)
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DOCS = Path("docs"); DOCS.mkdir(parents=True, exist_ok=True)
PROC = Path("data/processed")

def find_parquet() -> Path:
    parts = sorted(PROC.glob("date=*/hn.parquet"))
    if parts:
        return parts[-1]
    single = PROC / "hn.parquet"
    if single.exists():
        return single
    raise SystemExit("No processed data found. Run: python storage.py")

def build_dashboard():
    pf = find_parquet()
    df = pd.read_parquet(pf, engine="fastparquet")

    # last updated timestamp (UTC)
    last_run = pd.to_datetime(df["fetch_ts"]).max().strftime("%Y-%m-%d %H:%M UTC")

    # simple chart: top domains
    top = df["domain"].fillna("unknown").value_counts().head(10)
    plt.figure()
    top.plot(kind="bar", title="Top domains")
    plt.tight_layout()
    (DOCS / "top_domains.png").unlink(missing_ok=True)
    plt.savefig(DOCS / "top_domains.png")

    # clickable links for top 10 rows
    rows = df[["id", "title", "url"]].head(10).fillna({"title": "n/a", "url": ""})
    items = []
    for _, row in rows.iterrows():
        url = row["url"] or f"https://news.ycombinator.com/item?id={int(row['id'])}"
        title = row["title"]
        items.append(
            f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a></li>'
        )
    links_html = "".join(items)

    html = f"""<html><head><meta charset="utf-8"><title>HN Mini</title></head>
<body style="font-family:-apple-system,Arial,sans-serif;max-width:900px;margin:40px auto;">
  <h1>Hacker News — Mini Dashboard</h1>
  <p><strong>Rows:</strong> {len(df)} &nbsp;|&nbsp; <strong>Last updated:</strong> {last_run}</p>
  <img src="top_domains.png" alt="Top Domains" style="max-width:100%;height:auto;"/>
  <h2>Sample titles</h2>
  <ul>{links_html}</ul>
  <p style="color:#888;font-size:12px;">Source file: {pf}</p>
</body></html>"""
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    print("Dashboard generated → docs/index.html")

if __name__ == "__main__":
    build_dashboard()