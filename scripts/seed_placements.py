#!/usr/bin/env python3
"""Create demo reusable-section placements (popup, sticky bar, slot)."""
import json
import subprocess
import sys

sys.path.insert(0, "scripts")
from emdash_mcp import load_pat, rpc, parse_result

TOKEN = load_pat()

SECTIONS = [
    {
        "slug": "popup-konsultasi-cetak-buku",
        "data": {
            "title": "Popup Konsultasi Cetak Buku",
            "description": "Modal konsultasi gratis untuk pembaca artikel kategori percetakan/produk.",
            "display_type": "popup",
            "popup_trigger": "scroll",
            "popup_threshold": 50,
            "frequency_days": 7,
            "target_collections": ["posts"],
            "target_categories": "",
            "is_active": True,
            "blocks": [
                {
                    "_key": "popup_cta_1",
                    "_type": "marketing_cta",
                    "_version": 1,
                    "headline": "Butuh Cetak Buku atau Sistem Digital?",
                    "body": "Tim Kotacom siap bantu hitung estimasi biaya cetak, desain cover, sampai sistem POS & website bisnis Anda.\n\nKonsultasi gratis, tanpa biaya tersembunyi.",
                    "primary_cta_label": "Konsultasi via WhatsApp",
                    "primary_cta_url": "https://wa.me/6285799520350?text=Halo%20Kotacom%2C%20saya%20mau%20konsultasi%20dari%20artikel",
                    "secondary_cta_label": "Lihat Katalog Produk",
                    "secondary_cta_url": "/products",
                }
            ],
        },
    },
    {
        "slug": "banner-gratis-konsultasi",
        "data": {
            "title": "Sticky Bar Konsultasi Gratis",
            "description": "Banner melayang di bagian bawah semua halaman.",
            "display_type": "sticky_bar",
            "frequency_days": 3,
            "target_collections": ["all"],
            "target_categories": "",
            "is_active": True,
            "blocks": [
                {
                    "_key": "sticky_wa_1",
                    "_type": "marketing_whatsapp_cta",
                    "_version": 1,
                    "headline": "Konsultasi Cetak Buku & IT Gratis",
                    "body": "Ceritakan kebutuhan Anda — kami beri rekomendasi spesifikasi dan estimasi biaya.",
                    "label": "Chat WhatsApp Sekarang",
                    "custom_message": "Halo Kotacom, saya ingin konsultasi layanan.",
                    "variant": "banner",
                }
            ],
        },
    },
    {
        "slug": "slot-cta-setelah-judul",
        "data": {
            "title": "Slot CTA Setelah Judul",
            "description": "Disuntikkan otomatis tepat setelah judul artikel.",
            "display_type": "slot",
            "slot_position": "after_title",
            "target_collections": ["posts"],
            "target_categories": "",
            "is_active": True,
            "blocks": [
                {
                    "_key": "slot_wa_1",
                    "_type": "marketing_whatsapp_cta",
                    "_version": 1,
                    "headline": "Ingin Hasil Cetak yang Rapi & Sesuai Anggaran?",
                    "body": "Kirim kebutuhan Anda, kami cek spesifikasi bahan dan estimasi biayanya tanpa biaya konsultasi.",
                    "label": "Minta Estimasi Gratis",
                    "custom_message": "Halo Kotacom, saya mau minta estimasi cetak.",
                    "variant": "banner",
                }
            ],
        },
    },
]


def main():
    for spec in SECTIONS:
        out = rpc(
            TOKEN,
            "tools/call",
            {
                "name": "content_create",
                "arguments": {
                    "collection": "reusable_sections",
                    "data": spec["data"],
                    "slug": spec["slug"],
                    "status": "published",
                },
            },
        )
        res = parse_result(out)
        ok = isinstance(res, dict) and "item" in res
        print(("OK  " if ok else "FAIL"), spec["slug"], "" if ok else json.dumps(res)[:400])


if __name__ == "__main__":
    main()
