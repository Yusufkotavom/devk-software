#!/usr/bin/env python3
"""
scripts/migrate_domain.py - Automated Domain Migration Tool for Kotacom EmDash

Usage:
    # Full migration (Code + DB + Docker Swarm + Verification):
    python3 scripts/migrate_domain.py new-domain.com --all

    # Code and .env only:
    python3 scripts/migrate_domain.py new-domain.com --update-code

    # Database canonical and URLs only:
    python3 scripts/migrate_domain.py new-domain.com --update-db

    # Dry-run preview:
    python3 scripts/migrate_domain.py new-domain.com --dry-run
"""

import argparse
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ASTRO_CONFIG_PATH = REPO_ROOT / "astro.config.mjs"
ENV_PATH = REPO_ROOT / ".env"

def log(msg: str, status: str = "INFO"):
    colors = {
        "INFO": "\033[94m[*]\033[0m",
        "SUCCESS": "\033[92m[✓]\033[0m",
        "WARN": "\033[93m[!]\033[0m",
        "ERROR": "\033[91m[✗]\033[0m",
        "STEP": "\033[95m[==>]\033[0m",
    }
    prefix = colors.get(status, f"[{status}]")
    print(f"{prefix} {msg}")

def clean_domain(domain_str: str) -> str:
    cleaned = domain_str.strip()
    if cleaned.startswith("http://"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("https://"):
        cleaned = cleaned[8:]
    return cleaned.rstrip("/")

def find_db_container(name_pattern: str = "devk-software-db") -> str:
    try:
        cmd = ["sudo", "docker", "ps", "--filter", f"name={name_pattern}", "--format", "{{.ID}}"]
        output = subprocess.check_output(cmd, text=True).strip().split()
        if output:
            return output[0]
    except Exception as e:
        log(f"Failed to query docker ps for db container: {e}", "WARN")
    return ""

def update_astro_config(new_domain: str, dry_run: bool = False) -> bool:
    log(f"Checking astro.config.mjs for domain {new_domain}...", "INFO")
    if not ASTRO_CONFIG_PATH.exists():
        log(f"astro.config.mjs not found at {ASTRO_CONFIG_PATH}", "ERROR")
        return False

    content = ASTRO_CONFIG_PATH.read_text(encoding="utf-8")
    modified = False

    # Check allowedDomains
    domain_entry = f'{{ protocol: "https", hostname: "{new_domain}" }}'
    wildcard_entry = f'{{ protocol: "https", hostname: "**.{new_domain}" }}'

    if f'"{new_domain}"' not in content:
        # Insert into allowedDomains
        pattern = r'(allowedDomains:\s*\[)([\s\S]*?)(\s*\])'
        match = re.search(pattern, content)
        if match:
            existing = match.group(2)
            indent = "\t\t\t"
            additions = f"\n{indent}{domain_entry},"
            # If domain is not localhost or an IP, add wildcard as well
            if "." in new_domain and not new_domain.startswith("localhost"):
                # derive root domain if sub-level
                parts = new_domain.split(".")
                if len(parts) == 2:
                    additions += f"\n{indent}{wildcard_entry},"
            new_allowed = match.group(1) + existing + additions + match.group(3)
            content = content[:match.start()] + new_allowed + content[match.end():]
            modified = True
            log(f"Added {new_domain} to security.allowedDomains", "SUCCESS")

    # Check image.domains
    image_pattern = r'(image:\s*\{[\s\S]*?domains:\s*\[)([\s\S]*?)(\])'
    match_img = re.search(image_pattern, content)
    if match_img:
        existing_domains = match_img.group(2)
        if f'"{new_domain}"' not in existing_domains:
            new_img_domains = f'{match_img.group(1)}{existing_domains.rstrip()}, "{new_domain}"]'
            content = content[:match_img.start()] + new_img_domains + content[match_img.end():]
            modified = True
            log(f"Added {new_domain} to image.domains", "SUCCESS")

    if modified:
        if dry_run:
            log("[DRY-RUN] astro.config.mjs would be modified.", "INFO")
        else:
            # Backup
            bak_path = ASTRO_CONFIG_PATH.with_suffix(".mjs.bak")
            bak_path.write_text(ASTRO_CONFIG_PATH.read_text(encoding="utf-8"))
            ASTRO_CONFIG_PATH.write_text(content, encoding="utf-8")
            log(f"Updated {ASTRO_CONFIG_PATH} (backup at {bak_path.name})", "SUCCESS")
    else:
        log(f"{new_domain} is already present in astro.config.mjs", "INFO")

    return True

def update_env_file(new_domain: str, old_domain: str, dry_run: bool = False) -> bool:
    if not ENV_PATH.exists():
        log(f".env file not found at {ENV_PATH}", "WARN")
        return False

    content = ENV_PATH.read_text(encoding="utf-8")
    new_origin = f"https://{new_domain}"
    old_origin = f"https://{old_domain}"

    keys = ["SITE_URL", "EMDASH_SITE_URL", "BETTER_AUTH_URL", "EMDASH_BASE_URL"]
    modified = False

    for key in keys:
        pattern = rf'^{key}=.*$'
        if re.search(pattern, content, flags=re.MULTILINE):
            content = re.sub(pattern, f'{key}={new_origin}', content, flags=re.MULTILINE)
            modified = True
            log(f"Updated .env {key}={new_origin}", "SUCCESS")
        else:
            content += f"\n{key}={new_origin}"
            modified = True
            log(f"Appended .env {key}={new_origin}", "SUCCESS")

    if modified:
        if dry_run:
            log("[DRY-RUN] .env would be modified.", "INFO")
        else:
            bak_path = ENV_PATH.with_suffix(".env.bak")
            bak_path.write_text(ENV_PATH.read_text(encoding="utf-8"))
            ENV_PATH.write_text(content, encoding="utf-8")
            log(f"Updated {ENV_PATH} (backup at {bak_path.name})", "SUCCESS")

    return True

def update_database(new_domain: str, old_domain: str, db_container: str, dry_run: bool = False) -> bool:
    log(f"Updating database on container '{db_container}'...", "STEP")
    if not db_container:
        log("No database container specified or detected.", "ERROR")
        return False

    sql_statements = [
        # 1. Update _emdash_seo.seo_canonical
        f"UPDATE _emdash_seo SET seo_canonical = REPLACE(seo_canonical, '{old_domain}', '{new_domain}') WHERE seo_canonical LIKE '%{old_domain}%';",
        # 2. Update _emdash_seo.seo_image
        f"UPDATE _emdash_seo SET seo_image = REPLACE(seo_image, '{old_domain}', '{new_domain}') WHERE seo_image LIKE '%{old_domain}%';",
        # Also handle software.devk.my.id / kc.devk.my.id if old domain was devk.my.id
        f"UPDATE _emdash_seo SET seo_canonical = REPLACE(seo_canonical, 'devk.my.id', '{new_domain}') WHERE seo_canonical LIKE '%devk.my.id%';",
        f"UPDATE _emdash_seo SET seo_image = REPLACE(seo_image, 'software.devk.my.id', '{new_domain}') WHERE seo_image LIKE '%software.devk.my.id%';",
        # 3. Update _emdash_menu_items.custom_url
        f"UPDATE _emdash_menu_items SET custom_url = REPLACE(custom_url, 'devk.my.id', '{new_domain}') WHERE custom_url LIKE '%devk.my.id%';",
    ]

    for sql in sql_statements:
        log(f"SQL: {sql}", "INFO")
        if dry_run:
            continue
        try:
            cmd = ["sudo", "docker", "exec", "-i", db_container, "psql", "-U", "dokploy", "-d", "kotacom_emdash", "-c", sql]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            log(f"Result: {result.stdout.strip()}", "SUCCESS")
        except subprocess.CalledProcessError as e:
            log(f"SQL execution failed: {e.stderr}", "ERROR")
            return False

    return True

def update_swarm_service(new_domain: str, service_name: str, dry_run: bool = False) -> bool:
    log(f"Updating Docker Swarm service '{service_name}'...", "STEP")
    new_origin = f"https://{new_domain}"

    cmd = [
        "sudo", "docker", "service", "update",
        "--env-add", f"SITE_URL={new_origin}",
        "--env-add", f"EMDASH_SITE_URL={new_origin}",
        "--env-add", f"BETTER_AUTH_URL={new_origin}",
        "--env-add", f"EMDASH_BASE_URL={new_origin}",
        service_name
    ]

    log(f"Command: {' '.join(cmd)}", "INFO")
    if dry_run:
        log("[DRY-RUN] Swarm service update skipped.", "INFO")
        return True

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        log("Docker Swarm service updated successfully.", "SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        log(f"Swarm service update failed: {e.stderr}", "ERROR")
        return False

def verify_domain(new_domain: str):
    log(f"Verifying endpoints on https://{new_domain}...", "STEP")
    endpoints = [
        "/robots.txt",
        "/sitemap.xml",
        "/sitemap-projects.xml",
        "/llms.txt",
        "/pricing.md",
    ]

    headers = {"User-Agent": "Mozilla/5.0 (Automated Verification)"}
    all_ok = True

    for ep in endpoints:
        url = f"https://{new_domain}{ep}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.status
                sample = resp.read(200).decode("utf-8", errors="ignore").replace("\n", " ")
                log(f"GET {ep} -> HTTP {status} | Sample: {sample[:60]}...", "SUCCESS")
        except Exception as e:
            log(f"GET {ep} failed: {e}", "WARN")
            all_ok = False

    return all_ok

def main():
    parser = argparse.ArgumentParser(
        description="Automated Domain Migration Script for Kotacom EmDash",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("new_domain", help="Target domain (e.g., kotacom.id, staging.kotacom.id)")
    parser.add_argument("--old-domain", default="staging.devk.my.id", help="Old domain to replace (default: staging.devk.my.id)")
    parser.add_argument("--all", action="store_true", help="Execute all steps (code, db, swarm, verify)")
    parser.add_argument("--update-code", action="store_true", help="Update astro.config.mjs and .env")
    parser.add_argument("--update-db", action="store_true", help="Update canonical URLs in PostgreSQL")
    parser.add_argument("--update-swarm", action="store_true", help="Update Docker Swarm service environment variables")
    parser.add_argument("--verify", action="store_true", help="Verify endpoints on new domain")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without executing")
    parser.add_argument("--db-container", default="", help="Docker container name or ID for PostgreSQL")
    parser.add_argument("--swarm-service", default="app-program-online-application-cfreew", help="Docker Swarm service name")

    args = parser.parse_args()

    new_domain = clean_domain(args.new_domain)
    old_domain = clean_domain(args.old_domain)

    if not (args.all or args.update_code or args.update_db or args.update_swarm or args.verify):
        # Default behavior: run code and DB if no specific flags passed
        log("No action flags specified. Defaulting to: --update-code and --update-db.", "INFO")
        args.update_code = True
        args.update_db = True

    if args.all:
        args.update_code = True
        args.update_db = True
        args.update_swarm = True
        args.verify = True

    db_container = args.db_container or find_db_container()
    log(f"Target Domain: {new_domain}", "INFO")
    log(f"Old Domain:    {old_domain}", "INFO")
    if db_container:
        log(f"DB Container:  {db_container}", "INFO")

    success = True

    if args.update_code:
        log("Step 1: Updating Astro configuration and .env...", "STEP")
        c_ok = update_astro_config(new_domain, dry_run=args.dry_run)
        e_ok = update_env_file(new_domain, old_domain, dry_run=args.dry_run)
        success = success and c_ok and e_ok

    if args.update_db:
        log("Step 2: Updating PostgreSQL database canonicals...", "STEP")
        db_ok = update_database(new_domain, old_domain, db_container, dry_run=args.dry_run)
        success = success and db_ok

    if args.update_swarm:
        log("Step 3: Updating Docker Swarm service...", "STEP")
        sw_ok = update_swarm_service(new_domain, args.swarm_service, dry_run=args.dry_run)
        success = success and sw_ok

    if args.verify:
        log("Step 4: Running verification tests...", "STEP")
        v_ok = verify_domain(new_domain)
        success = success and v_ok

    if success:
        log(f"Domain migration process completed successfully for {new_domain}!", "SUCCESS")
    else:
        log("Migration encountered warnings or errors. Check log output above.", "WARN")

if __name__ == "__main__":
    main()
