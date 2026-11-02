import csv, json, subprocess, re, os
from urllib.parse import urlparse

BASE_DIR = '/home/ubuntu/projects/kotacom-emdash'

# 1. Load wilayah mapping
with open(f'{BASE_DIR}/src/data/wilayah.ts') as f:
    w_text = f.read()

city_prov_map = {}
for line in w_text.splitlines():
    m = re.search(r'"([^"]+)":\s*"([^"]+)"', line)
    if m:
        city_prov_map[m.group(1)] = m.group(2)

print(f"Loaded {len(city_prov_map)} city-province mappings.")

# 2. Load GSC data
gsc_csv = '/home/ubuntu/kotacom/sanity-nextjs-kotacom/frontend/tmp/gsc-kotacom-full/gsc-pages.csv'
gsc_data = {}
with open(gsc_csv, 'r', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        p = urlparse(r['page'].strip()).path.rstrip('/') or '/'
        gsc_data[p] = int(r.get('impressions', 0))

# 3. Load DB credentials
with open(f'{BASE_DIR}/.env') as f:
    for line in f:
        if line.startswith('DATABASE_URL='):
            pw = line.split('://dokploy:')[1].split('@')[0]
            break

def run_psql(sql):
    cmd = ['sudo', 'docker', 'exec', '-i', '-e', f'PGPASSWORD={pw}', 'devk-software-db-hfl2l5.1.mydjd6wgx9s8ledrfqf7chlz6', 'psql', '-U', 'dokploy', '-d', 'kotacom_emdash']
    p = subprocess.run(cmd, input=sql, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"psql error: {p.stderr}\nSQL: {sql[:300]}")
    return p.stdout

# 4. Fetch all jasa-cetak-buku-* pages from ec_pages
res = run_psql("SELECT id, slug FROM ec_pages WHERE slug LIKE 'jasa-cetak-buku-%';")
db_pages = []
for line in res.strip().splitlines():
    if '|' in line and not line.startswith(' id') and not line.startswith('-'):
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 2:
            db_pages.append({'id': parts[0], 'slug': parts[1]})

print(f"Total halaman 'jasa-cetak-buku-*' di DB: {len(db_pages)}")

# 5. Filter zero impressions
zero_impr_pages = []
zero_slugs_set = set()
pruned_redirects = {}

for page in db_pages:
    slug = page['slug']
    path = f"/{slug}"
    if gsc_data.get(path, 0) == 0:
        city_key = slug.replace('jasa-cetak-buku-', '')
        prov = city_prov_map.get(city_key, 'hub-nasional')
        target = f"/percetakan/cetak-buku/{prov}" if prov != 'hub-nasional' else "/percetakan/cetak-buku"
        zero_impr_pages.append(page)
        zero_slugs_set.add(slug)
        pruned_redirects[path] = target

print(f"Halaman 0 impresi yang akan dihapus & di-redirect: {len(zero_impr_pages)}")

# Simpan pruned_redirects.json
redirects_file = f'{BASE_DIR}/src/data/pruned_city_redirects.json'
with open(redirects_file, 'w') as f:
    json.dump(pruned_redirects, f, indent=2)
print(f"Saved {len(pruned_redirects)} redirects to {redirects_file}")

# 6. Hapus dari DB (ec_pages & revisions)
ids_tuple = "('" + "','".join(p['id'] for p in zero_impr_pages) + "')"
sql_delete = f"""
UPDATE ec_pages SET live_revision_id = NULL, draft_revision_id = NULL WHERE id IN {ids_tuple};
DELETE FROM revisions WHERE collection = 'pages' AND entry_id IN {ids_tuple};
DELETE FROM _emdash_seo WHERE collection = 'pages' AND content_id IN {ids_tuple};
DELETE FROM ec_pages WHERE id IN {ids_tuple};
SELECT count(*) FROM ec_pages WHERE slug LIKE 'jasa-cetak-buku-%';
"""
out_del = run_psql(sql_delete)
print("DB Deletion result:\n", out_del.strip())

# 7. Update dataset generator di _plugin_storage
res_ds = run_psql("SELECT data FROM _plugin_storage WHERE id = 'ds_cetak_buku_399';")
# Parse JSON from psql output
raw_json = res_ds.strip()
if raw_json.startswith('data\n'):
    raw_json = raw_json.split('\n', 2)[2].strip()

ds = json.loads(raw_json)
orig_rows = ds.get('rows', [])
new_rows = []

for row in orig_rows:
    kab = row.get('kabupaten', '')
    # create slug from kab
    kab_slug = re.sub(r'[^a-z0-9]+', '-', kab.lower()).strip('-')
    page_slug = f"jasa-cetak-buku-{kab_slug}"
    if page_slug not in zero_slugs_set:
        new_rows.append(row)

print(f"Dataset generator: {len(orig_rows)} rows -> {len(new_rows)} rows (pruned {len(orig_rows) - len(new_rows)})")

ds['rows'] = new_rows
# Rebuild csvContent
csv_lines = ["kabupaten,layanan"]
for r in new_rows:
    csv_lines.append(f'"{r.get("kabupaten","")}","{r.get("layanan","")}"')
ds['csvContent'] = "\n".join(csv_lines)
ds['name'] = f"Kabupaten Kota Cetak Buku ({len(new_rows)} Wilayah High-Intent)"

escaped_ds = json.dumps(ds).replace("'", "''")
run_psql(f"UPDATE _plugin_storage SET data = '{escaped_ds}' WHERE id = 'ds_cetak_buku_399';")
print("Updated dataset in _plugin_storage successfully.")

# 8. Update url_comparison.json & urls_not_in_gsc.json
with open(f'{BASE_DIR}/src/data/url_comparison.json') as f:
    cmp_data = json.load(f)

for item in cmp_data:
    if item['path'] in pruned_redirects:
        item['category'] = 'redirected'
        item['status'] = '301'
        item['note'] = f"Redirect 301 ke {pruned_redirects[item['path']]}"

with open(f'{BASE_DIR}/src/data/url_comparison.json', 'w') as f:
    json.dump(cmp_data, f, indent=2)

with open(f'{BASE_DIR}/src/data/urls_not_in_gsc.json') as f:
    not_gsc = json.load(f)

not_gsc = [u for u in not_gsc if u not in pruned_redirects]
with open(f'{BASE_DIR}/src/data/urls_not_in_gsc.json', 'w') as f:
    json.dump(not_gsc, f, indent=2)

print("Updated url_comparison.json and urls_not_in_gsc.json.")
print("=== SEMUA PROSES SELESAI ===")
