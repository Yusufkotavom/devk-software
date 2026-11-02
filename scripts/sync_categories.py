import json, os, time, subprocess

with open('/home/ubuntu/projects/kotacom-emdash/.env') as f:
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

ENCODING = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
def generate_ulid():
    t = int(time.time() * 1000)
    time_part = ""
    for _ in range(10):
        time_part = ENCODING[t % 32] + time_part
        t //= 32
    rand_bytes = os.urandom(10)
    rand_int = int.from_bytes(rand_bytes, "big")
    rand_part = ""
    for _ in range(16):
        rand_part = ENCODING[rand_int % 32] + rand_part
        rand_int //= 32
    return time_part + rand_part

res_posts = run_psql("SELECT id, slug FROM ec_posts;")
db_posts = {}
for line in res_posts.strip().splitlines():
    if '|' in line and not line.startswith(' id') and not line.startswith('-'):
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 2:
            db_posts[parts[1]] = parts[0]

res_prods = run_psql("SELECT id, slug FROM ec_products;")
db_prods = {}
for line in res_prods.strip().splitlines():
    if '|' in line and not line.startswith(' id') and not line.startswith('-'):
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 2:
            db_prods[parts[1]] = parts[0]

print(f"Loaded {len(db_posts)} posts and {len(db_prods)} products from DB.")

with open('/home/ubuntu/sanity_categories.json') as f:
    cats_data = json.load(f)

with open('/home/ubuntu/sanity_posts.json') as f:
    s_posts = json.load(f)

with open('/home/ubuntu/sanity_products.json') as f:
    s_prods = json.load(f)

category_ulid_map = {}

for c in cats_data:
    cid = c['_id']
    slug = c.get('slug', {}).get('current')
    if not slug:
        continue
    label = c.get('title') or slug.replace('-', ' ').title()
    desc = c.get('description') or ""
    
    chk = run_psql(f"SELECT id FROM taxonomies WHERE name = 'category' AND slug = '{slug}' AND locale = 'en';").strip()
    lines = [l.strip() for l in chk.splitlines() if l.strip() and not l.startswith('id') and not l.startswith('-')]
    if lines and len(lines[0]) == 26:
        tax_id = lines[0]
    else:
        tax_id = generate_ulid()
        data_json = json.dumps({"description": desc})
        escaped_label = label.replace("'", "''")
        escaped_data = data_json.replace("'", "''")
        run_psql(f"INSERT INTO taxonomies (id, name, slug, label, locale, translation_group, sort_order, data) VALUES ('{tax_id}', 'category', '{slug}', '{escaped_label}', 'en', '{tax_id}', 0, '{escaped_data}') ON CONFLICT (name, slug, locale) DO UPDATE SET label = EXCLUDED.label;")
    
    category_ulid_map[cid] = tax_id

print(f"Taxonomies populated: {len(category_ulid_map)} categories mapped.")

post_links = 0
for sp in s_posts:
    slug = sp.get('slug', {}).get('current')
    post_id = db_posts.get(slug)
    if not post_id:
        continue
    for c in (sp.get('categories') or []):
        ref = c.get('_ref')
        tax_id = category_ulid_map.get(ref)
        if tax_id:
            run_psql(f"INSERT INTO content_taxonomies (collection, entry_id, taxonomy_id, status, locale) VALUES ('posts', '{post_id}', '{tax_id}', 'published', 'en') ON CONFLICT (collection, entry_id, taxonomy_id) DO NOTHING;")
            post_links += 1

prod_links = 0
for sp in s_prods:
    slug = sp.get('slug', {}).get('current')
    prod_id = db_prods.get(slug)
    if not prod_id:
        continue
    for c in (sp.get('categories') or []):
        ref = c.get('_ref')
        tax_id = category_ulid_map.get(ref)
        if tax_id:
            run_psql(f"INSERT INTO content_taxonomies (collection, entry_id, taxonomy_id, status, locale) VALUES ('products', '{prod_id}', '{tax_id}', 'published', 'en') ON CONFLICT (collection, entry_id, taxonomy_id) DO NOTHING;")
            prod_links += 1

print(f"Content taxonomies inserted: {post_links} post links, {prod_links} product links.")
