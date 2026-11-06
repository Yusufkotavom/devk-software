#!/bin/bash
set -e

CONTAINER="devk-software-db-hfl2l5.1.mydjd6wgx9s8ledrfqf7chlz6"
DB_USER="dokploy"
DB_NAME="kotacom_emdash"

echo "=== Fixing migrated revisions: merge metadata from ec_posts/ec_pages ==="

echo ""
echo "--- Fixing posts revisions ---"
sudo docker exec -i "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" <<'SQL'
DO $$
DECLARE
    rec RECORD;
    current_data JSONB;
    merged_data JSONB;
    counter INT := 0;
BEGIN
    FOR rec IN 
        SELECT 
            p.id,
            p.slug,
            p.title,
            p.featured_image,
            p.content as post_content,
            p.excerpt,
            p.access,
            r.id as revision_id,
            r.data::jsonb as revision_data
        FROM ec_posts p
        JOIN revisions r ON r.entry_id = p.id AND r.collection = 'posts'
        WHERE p.live_revision_id = r.id
          AND r.data::jsonb ? 'content'
          AND NOT (r.data::jsonb ? 'title')
        LIMIT 200
    LOOP
        -- Merge: keep content from revision, add metadata from table
        merged_data := jsonb_build_object(
            'title', rec.title,
            'content', rec.revision_data->'content',
            'featured_image', COALESCE(rec.featured_image::jsonb, 'null'::jsonb),
            'excerpt', rec.excerpt,
            'access', rec.access,
            '_slug', rec.slug
        );
        
        -- Update revision
        UPDATE revisions 
        SET data = merged_data::text
        WHERE id = rec.revision_id;
        
        counter := counter + 1;
        IF counter % 50 = 0 THEN
            RAISE NOTICE 'Fixed % posts...', counter;
        END IF;
    END LOOP;
    
    RAISE NOTICE 'Posts batch complete: % revisions fixed', counter;
END $$;
SQL

echo ""
echo "--- Fixing pages revisions ---"
sudo docker exec -i "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" <<'SQL'
DO $$
DECLARE
    rec RECORD;
    current_data JSONB;
    merged_data JSONB;
    counter INT := 0;
BEGIN
    FOR rec IN 
        SELECT 
            p.id,
            p.slug,
            p.title,
            p.featured_image,
            p.content as page_content,
            r.id as revision_id,
            r.data::jsonb as revision_data
        FROM ec_pages p
        JOIN revisions r ON r.entry_id = p.id AND r.collection = 'pages'
        WHERE p.live_revision_id = r.id
          AND r.data::jsonb ? 'content'
          AND NOT (r.data::jsonb ? 'title')
        LIMIT 200
    LOOP
        -- Merge metadata
        merged_data := jsonb_build_object(
            'title', rec.title,
            'content', rec.revision_data->'content',
            'featured_image', COALESCE(rec.featured_image::jsonb, 'null'::jsonb),
            '_slug', rec.slug
        );
        
        UPDATE revisions 
        SET data = merged_data::text
        WHERE id = rec.revision_id;
        
        counter := counter + 1;
        IF counter % 50 = 0 THEN
            RAISE NOTICE 'Fixed % pages...', counter;
        END IF;
    END LOOP;
    
    RAISE NOTICE 'Pages batch complete: % revisions fixed', counter;
END $$;
SQL

echo ""
echo "=== Verification ==="
sudo docker exec -i "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" <<'SQL'
SELECT 
    'posts' as collection,
    COUNT(*) FILTER (WHERE r.data::jsonb ? 'title') as has_title,
    COUNT(*) FILTER (WHERE NOT (r.data::jsonb ? 'title')) as missing_title,
    COUNT(*) as total
FROM revisions r
WHERE r.collection = 'posts'
UNION ALL
SELECT 
    'pages' as collection,
    COUNT(*) FILTER (WHERE r.data::jsonb ? 'title') as has_title,
    COUNT(*) FILTER (WHERE NOT (r.data::jsonb ? 'title')) as missing_title,
    COUNT(*) as total
FROM revisions r
WHERE r.collection = 'pages';
SQL

echo ""
echo "✅ Fix complete!"
