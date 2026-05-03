import requests
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

API = "https://blox-fruits.fandom.com/api.php"
YEARS = [2022, 2023, 2024, 2025, 2026]
FROM_YEAR = 2026

FRUIT_ALIASES = {
    'falcon': 'eagle', 'chop': 'blade', 'leopard': 'tiger',
    'rumble': 'lightning', 'paw': 'pain', 'string': 'spider',
    'revive': 'ghost', 'soul': 'spirit', 'barrier': 'creation',
    'sping': 'spring', 'dimond': 'diamond', 'sprin': 'spring',
    'pheonix': 'phoenix', 'budda': 'buddha', 'ligthning': 'lightning',
}
ALWAYS_IN_STOCK = {'rocket', 'spin'}
KNOWN_FRUITS = {
    'rocket','spin','blade','spring','bomb','smoke','spike','flame','ice','sand',
    'dark','eagle','diamond','light','rubber','ghost','magma','quake','buddha',
    'love','creation','spider','sound','phoenix','portal','lightning','pain',
    'blizzard','gravity','mammoth','t-rex','dough','shadow','venom','gas',
    'spirit','tiger','yeti','kitsune','control','dragon',
}

def fetch_wikitext(year):
    res = requests.get(API, params={
        'action': 'parse',
        'page': f'History_of_Stock/{year}',
        'prop': 'wikitext',
        'format': 'json',
    }, headers={'User-Agent': 'BloxStockRateCalc/1.0'}, timeout=20)
    data = res.json()
    if 'error' in data:
        print(f"  [SKIP] {year}: {data['error'].get('info','unknown error')}")
        return None
    return data['parse']['wikitext']['*']

def parse_cell(cell_text):
    text = re.sub(r"'''?\[\[([^\]|]+)(?:\|[^\]]*)?\]\]'''?", r'\1', cell_text)
    text = re.sub(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', r'\1', text)
    text = text.replace("'''", '').replace("''", '')
    # Strip nowiki và html tags
    text = re.sub(r'<nowiki\s*/?>', '', text)
    text = re.sub(r'</nowiki>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    fruits = []
    # Split bằng cả , và . (wiki có người dùng dấu chấm thay dấu phẩy)
    for part in re.split(r'[,.]', text):
        name = part.strip().lower()
        if not name:
            continue
        name = FRUIT_ALIASES.get(name, name)
        if name in KNOWN_FRUITS and name not in ALWAYS_IN_STOCK:
            fruits.append(name)
    return fruits

def parse_wikitext(wikitext, year):
    cycles = []
    lines = wikitext.split('\n')
    TIME_PATTERN = re.compile(r'^\|\s*\d+:\d+\s*(AM|PM)\s*$', re.IGNORECASE)
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if TIME_PATTERN.match(line):
            i += 1
            while i < len(lines):
                cell = lines[i].strip()
                if cell.startswith('|-') or cell.startswith('!') or TIME_PATTERN.match(cell):
                    break
                if cell.startswith('|') and not cell.startswith('||'):
                    cell_content = cell[1:].strip()
                    fruits = parse_cell(cell_content)
                    if fruits:
                        cycles.append(fruits)
                i += 1
        else:
            i += 1
    return cycles

def main():
    all_cycles = []
    for year in YEARS:
        print(f"Fetching {year}...")
        wikitext = fetch_wikitext(year)
        if not wikitext:
            continue
        cycles = parse_wikitext(wikitext, year)
        print(f"  -> {len(cycles)} cycles found")
        for fruits in cycles:
            all_cycles.append((year, fruits))

    filtered = [(y, f) for y, f in all_cycles if y >= FROM_YEAR]
    total = len(filtered)
    print(f"\nTotal cycles from {FROM_YEAR}: {total}")
    if total == 0:
        print("No data!")
        return

    counts = defaultdict(int)
    for _, fruits in filtered:
        for f in set(fruits):
            counts[f] += 1

    print(f"\n{'Fruit':<15} {'Count':>6}  {'Rate':>7}")
    print('-' * 32)
    rates = {}
    for fruit, count in sorted(counts.items(), key=lambda x: -x[1]):
        rate = round(count / total * 100, 2)
        rates[fruit] = {'count': count, 'rate_pct': rate}
        print(f"  {fruit:<13} {count:>6}x  {rate:>6.2f}%")

    rates['rocket'] = {'count': total, 'rate_pct': 100.0}
    rates['spin']   = {'count': total, 'rate_pct': 100.0}

    output = {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'from_year': FROM_YEAR,
        'total_cycles': total,
        'rates': rates,
    }

    out_path = Path(__file__).parent / 'observed_rates.json'
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved -> {out_path}")

if __name__ == '__main__':
    main()