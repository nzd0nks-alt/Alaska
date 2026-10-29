#!/usr/bin/env python3
"""
Task: SharePoint Site Storage & Optimization Audit
Circle Connect Multi-Tenant Engine
"""

import csv
import io
from datetime import datetime

def run_sharepoint_audit(client, period="D30"):
    """
    Execute SharePoint storage audit against Microsoft Graph for the given tenant client.
    Returns structured analysis dictionary.
    """
    raw_data = client.get_sharepoint_site_usage_detail(period=period)
    reader = csv.DictReader(io.StringIO(raw_data))
    rows = list(reader)

    total_sites = len(rows)
    total_bytes = 0
    total_files = 0
    total_active_files = 0
    active_sites = 0
    stagnant_archive_candidates = []
    all_sites = []

    for r in rows:
        owner = r.get("Owner Display Name", "")
        template = r.get("Root Web Template", "")
        storage_used = int(r.get("Storage Used (Byte)", 0) or 0)
        files = int(r.get("File Count", 0) or 0)
        active_files = int(r.get("Active File Count", 0) or 0)
        last_activity = r.get("Last Activity Date", "")
        is_deleted = str(r.get("Is Deleted", "False")).lower() == "true"

        if is_deleted:
            continue

        total_bytes += storage_used
        total_files += files
        total_active_files += active_files

        used_gb = round(storage_used / (1024**3), 2)
        stagnant_pct = round(((files - active_files) / files * 100), 1) if files > 0 else 0.0

        site_info = {
            "name": owner,
            "template": template,
            "used_gb": used_gb,
            "files": files,
            "active_files": active_files,
            "stagnant_pct": stagnant_pct,
            "last_activity": last_activity or "No activity (>30d)"
        }

        if last_activity:
            active_sites += 1

        # Check for cold archive candidate: >50 GB with >95% stagnant files or "Archive" in title
        if (used_gb >= 50.0 and stagnant_pct >= 95.0) or ("archive" in owner.lower() and used_gb >= 10.0):
            stagnant_archive_candidates.append(site_info)

        all_sites.append(site_info)

    all_sites.sort(key=lambda x: x["used_gb"], reverse=True)
    stagnant_archive_candidates.sort(key=lambda x: x["used_gb"], reverse=True)

    # Estimate savings if cold archives moved to Microsoft 365 Archive / Azure Cold tier
    cold_gb = sum(s["used_gb"] for s in stagnant_archive_candidates)
    est_annual_savings_nzd = round(cold_gb * (0.33 - 0.08) * 12, 2)

    return {
        "task_name": "SharePoint Site Storage & Optimization Audit",
        "period": period,
        "audited_at": datetime.now().isoformat(),
        "summary": {
            "total_sites": total_sites,
            "active_sites": active_sites,
            "inactive_sites": total_sites - active_sites,
            "total_files": total_files,
            "total_active_files": total_active_files,
            "total_storage_gb": round(total_bytes / (1024**3), 2),
            "total_storage_tb": round(total_bytes / (1024**4), 2),
            "cold_archive_candidates_count": len(stagnant_archive_candidates),
            "cold_archive_storage_gb": round(cold_gb, 2),
            "est_annual_savings_nzd": est_annual_savings_nzd
        },
        "archive_candidates": stagnant_archive_candidates,
        "top_sites": all_sites[:15]
    }
