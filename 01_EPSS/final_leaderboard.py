import pandas as pd
import numpy as np

# Pre-convert to dicts once
old_dict = pd.read_csv('data/epss_scores-2025-10-01.csv.gz', compression='gzip', header=1, low_memory=False)\
             .set_index('cve')['epss'].to_dict()
new_dict = pd.read_csv('data/epss_scores-2026-01-15.csv.gz', compression='gzip', header=1, low_memory=False)\
             .set_index('cve')['epss'].to_dict()

marwan_cves = pd.read_csv('data/marwan.csv')['cve'].tolist()

table = []
for cve in marwan_cves:
    old_score = old_dict.get(cve, 0.0)
    new_score = new_dict.get(cve, 0.0)
    delta = (new_score / old_score) if old_score > 0 else np.inf if new_score > 0 else 1.0
    status = '🚀' if new_score > old_score * 1.5 else '📊' if new_score > old_score else '📉'
    table.append([cve, f"{old_score:.4f}", f"{new_score:.4f}", f"{delta:.1f}x", status])

df = pd.DataFrame(table, columns=['CVE', 'Oct_2025', 'Jan_2026', 'Δ', 'Status'])
print(df.to_markdown(index=False))
df.to_csv('data/leaderboard_final.csv', index=False)
