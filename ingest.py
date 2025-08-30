
import requests, json, time, pathlib

RAW_DIR = pathlib.Path('data/raw'); RAW_DIR.mkdir(parents=True, exist_ok=True)

TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"

def fetch_top_ids(n=30):
    ids = requests.get(TOP_URL, timeout=30).json() #lista de IDs (números)
    return ids[:n]

def fetch_items(ids):
    items = []
    for i in ids:
        r = requests.get(ITEM_URL.format(id=i), timeout=30)
        if r.ok:
            items.append(r.json()) 
        time.sleep(0.05)
    return items

if __name__ == "__main__":
    ids = fetch_top_ids(30)
    items = fetch_items(ids)
    from time import gmtime, strftime
    ts = strftime("%Y%m%dT%H%M%SZ", gmtime())
    (RAW_DIR / f"hn_{ts}.json").write_text(json.dumps(items))
    print(f"Guardado: data/raw/hn_{ts}.json com {len(items)} items")

