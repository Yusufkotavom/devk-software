#!/usr/bin/env python3
"""
Migrate legacy EmDash entries (content stored inline) to revision-based architecture.
"""
import psycopg2
import json
import os
from datetime import datetime

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "kotacom_emdash"
DB_USER = "dokploy"
DB_PASS = os.getenv("DB_PASS", "")

def migrate_collection(cursor, table_name, collection_name):
    """Migrate entries from inline content to revisions table."""
    
    # Find entries with inline content but no live_revision_id
    cursor.execute(f"""
        SELECT id, content, author_id, created_at
        FROM {table_name}
        WHERE status = 'published'
          AND live_revision_id IS NULL
          AND content IS NOT NULL
    """)
    
    entries = cursor.fetchall()
    print(f"\n{collection_name}: Found {len(entries)} entries with inline content")
    
    migrated = 0
    for entry_id, content_json, author_id, created_at in entries:
        # Generate revision ID (ULID-style)
        import time
        timestamp = int(time.time() * 1000)
        import random
        rand_part = ''.join(random.choices('0123456789ABCDEFGHJKMNPQRSTVWXYZ', k=16))
        revision_id = f"01M{timestamp % 1000000:06d}{rand_part}"
        
        # Parse content
        if isinstance(content_json, str):
            content_data = json.loads(content_json)
        else:
            content_data = content_json
        
        # Create revision data structure matching EmDash format
        revision_data = {
            "content": content_data if isinstance(content_data, list) else []
        }
        
        # Insert into revisions table
        cursor.execute("""
            INSERT INTO revisions (id, collection, entry_id, data, author_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            revision_id,
            collection_name,
            entry_id,
            json.dumps(revision_data),
            author_id,
            created_at
        ))
        
        # Update entry to point to new revision
        cursor.execute(f"""
            UPDATE {table_name}
            SET live_revision_id = %s
            WHERE id = %s
        """, (revision_id, entry_id))
        
        migrated += 1
    
    print(f"{collection_name}: Migrated {migrated} entries")
    return migrated

def main():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    
    try:
        cursor = conn.cursor()
        
        total = 0
        total += migrate_collection(cursor, "ec_posts", "posts")
        total += migrate_collection(cursor, "ec_pages", "pages")
        
        conn.commit()
        print(f"\n✅ Total migrated: {total} entries")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
