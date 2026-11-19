#!/usr/bin/env python3
"""Werk data.json bij met gewijzigde en verwijderde voorspellingen.

Gebruik: python3 tools/apply_updates.py updates.json
updates.json = {"changed": [ {id, ...volledig document...}, ... ],
                "deleted": ["id", ...],
                "syncedAt": "2026-11-23T07:00:00Z"}
Schrijft data.json (gesorteerd op id) en tools/last_sync.txt.
"""
import json, sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(root, 'data.json')
upd = json.load(open(sys.argv[1], encoding='utf-8'))
docs = {d['id']: d for d in json.load(open(data_path, encoding='utf-8'))}
n_new = n_upd = n_del = 0
for d in upd.get('changed', []):
    if not d.get('id'): continue
    if d['id'] in docs: n_upd += 1
    else: n_new += 1
    docs[d['id']] = d
for i in upd.get('deleted', []):
    if docs.pop(i, None) is not None: n_del += 1
out = sorted(docs.values(), key=lambda d: d['id'])
json.dump(out, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
if upd.get('syncedAt'):
    open(os.path.join(root, 'tools', 'last_sync.txt'), 'w').write(upd['syncedAt'] + '\n')
print(f'nieuw {n_new}, bijgewerkt {n_upd}, verwijderd {n_del}, totaal {len(out)}')
