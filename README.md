
## Live dashboard
https://joaofsant.github.io/mini-de/

## Design choices

- **API ingestion** — fetches JSON data from the public Hacker News API, simulating a real-world external data source.
- **Transformation with pandas** — normalizes nested JSON, renames columns, adds derived fields (`fetch_ts`, domain).
- **Quality checks** — assertions ensure schema, non-negative scores, and reasonable null percentages. Fail fast if data quality is poor.
- **Storage in Parquet** — columnar, compressed, efficient to query at scale. Partitioned by date for easier historical access.
- **Static dashboard** — simple HTML + matplotlib chart, generated daily and published via GitHub Pages. Demonstrates data delivery to stakeholders.
- **Automation** — GitHub Actions runs the pipeline daily and redeploys the dashboard automatically.

## Next steps

- **Database integration**: load Parquet into DuckDB/SQLite for ad-hoc SQL queries and joins with other datasets.
- **Unit tests**: expand pytest coverage for ingestion and transformation logic.
- **Incremental loads**: store only new/updated records instead of reprocessing all.
- **Schema versioning**: define explicit column contracts and detect breaking changes.
- **Visualization**: move from matplotlib to lightweight web dashboards (Plotly Dash, Streamlit, or plain JS).
- **Monitoring**: track pipeline runs, data freshness, and validation metrics.

