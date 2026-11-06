#!/bin/bash
set -e

CONTAINER="devk-software-db-hfl2l5.1.mydjd6wgx9s8ledrfqf7chlz6"
DB_USER="dokploy"
DB_NAME="kotacom_emdash"

echo "=== Migrating legacy inline content to revisions table ==="

# Migrate posts
echo ""
echo "--- Migrating posts collection ---"
sudo docker exec -i "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" <<'SQL'
DO $$
DECLARE
    rec RECORD;
    rev_id TEXT;
    rev_data JSONB;
BEGIN
    FOR rec IN 
        SELECT id, content, author_id, created_at
        FROM ec_posts
        WHERE status = 'published'
          AND live_revision_id IS NULL
          AND content IS NOT NULL
        ORDER BY created_at
    LOOP
        -- Generate revision ID (simplified ULID)
        rev_id := '01M' || LPAD((EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT::TEXT, 13, '0') || 
                  UPPER(SUBSTRING(MD5(RANDOM()::TEXT) FROM 1 FOR 10));
        
        -- Wrap content in revision structure
        rev_data := jsonb_build_object('content', rec.content);
        
        -- Insert revision
        INSERT INTO revisions (id, collection, entry_id, data, author_id, created_at)
        VALUES (rev_id, 'posts', rec.id, rev_data::text, rec.author_id, rec.created_at);
        
        -- Update post pointer
        UPDATE ec_posts 
        SET live_revision_id = rev_id 
        WHERE id = rec.id;
        
        RAISE NOTICE 'Migrated post: % -> revision %', SUBSTRING(rec.id, 1, 10), SUBSTRING(rev_id, 1, 10);
    END LOOP;
END $$;
SQL

echo ""
echo "--- Migrating pages collection ---"
sudo docker exec -i "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" <<'SQL'
DO $$
DECLARE
    rec RECORD;
    rev_id TEXT;
    rev_data JSONB;
BEGIN
    FOR rec IN 
        SELECT id, content, author_id, created_at
        FROM ec_pages
        WHERE status = 'published'
          AND live_revision_id IS NULL
          AND content IS NOT NULL
        ORDER BY created_at
        LIMIT 100  -- Process in batches to avoid timeout
    LOOP
        -- Generate revision ID
        rev_id := '01M' || LPAD((EXTRACT(EPOCH FROM NOW()) * 1000)::BIGINT::TEXT, 13, '0') || 
                  UPPER(SUBSTRING(MD5(RANDOM()::TEXT) FROM 1 FOR 10));
        
        -- Wrap content
        rev_data := jsonb_build_object('content', rec.content);
        
        -- Insert revision
        INSERT INTO revisions (id, collection, entry_id, data, author_id, created_at)
        VALUES (rev_id, 'pages', rec.id, rev_data::text, rec.author_id, rec.created_at);
        
        -- Update page pointer
        UPDATE ec_pages 
        SET live_revision_id = rev_id 
        WHERE id = rec.id;
        
        RAISE NOTICE 'Migrated page: % -> revision %', SUBSTRING(rec.id, 1, 10), SUBSTRING(rev_id, 1, 10);
    END LOOP;
END $$;
SQL

echo ""
echo "=== Checking migration results ==="
sudo docker exec -i "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" <<'SQL'
SELECT 
    'posts' as collection,
    COUNT(*) FILTER (WHERE live_revision_id IS NULL) as still_null,
    COUNT(*) FILTER (WHERE live_revision_id IS NOT NULL) as migrated
FROM ec_posts WHERE status = 'published'
UNION ALL
SELECT 
    'pages' as collection,
    COUNT(*) FILTER (WHERE live_revision_id IS NULL) as still_null,
    COUNT(*) FILTER (WHERE live_revision_id IS NOT NULL) as migrated
FROM ec_pages WHERE status = 'published';
SQL

echo ""
echo "✅ Migration complete!"
