import json, pathlib
import pandas as pd
from urllib.parse import urlparse

RAW_DIR = pathlib.Path("data/raw")

def latest_raw():
    files = sorted(RAW_DIR.glob("hn_*.json"))
    if not files:
        raise SystemExit("Sem dados. Corre primeiro: python ingest.py")
    return files[-1]

def transform():
    # Lê o JSON mais recente
    path = latest_raw()
    rows = json.loads(path.read_text())

    # Converte JSON -> DataFrame (tabela)
    df = pd.json_normalize(rows)

    # Seleciona colunas úteis e renomeia
    cols = ['id','title','by','score','time','url','type']
    df = df[[c for c in cols if c in df.columns]].copy()
    df.rename(columns={'by':'author'}, inplace=True)

    # Converte tempo (segundos desde 1970) para datetime
    df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)

    # Data/hora em que foi buscado (vem do nome do ficheiro)
    ts = path.stem.replace("hn_","")
    df['fetch_ts'] = pd.to_datetime(ts, format="%Y%m%dT%H%M%SZ", utc=True)

    # Extrai o domínio da URL (ex.: nytimes.com)
    df['domain'] = df['url'].apply(lambda u: urlparse(u).netloc if isinstance(u,str) else None)

    return df

if __name__ == "__main__":
    out = transform()
    print(out.head())  