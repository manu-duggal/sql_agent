import json
import re
from pathlib import Path

CACHE_FILE = Path("sql_cache.json")

if CACHE_FILE.exists():
    cache = json.load(open(CACHE_FILE))
else:
    cache = {}

def normalize(q: str) -> str:
    q = q.lower()
    q = re.sub(r"[^\w\s]", "", q)
    return q.strip()

def get_cached(question):
    return cache.get(normalize(question))

def save_cache(question, sql):
    cache[normalize(question)] = {"sql": sql}
    json.dump(cache, open(CACHE_FILE, "w"), indent=2)
