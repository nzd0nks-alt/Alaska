#!/usr/bin/env python3
"""
Task: Exchange Online Mailbox & Archiving Audit
Circle Connect Multi-Tenant Engine
"""

import csv
import io
from datetime import datetime

def run_exchange_audit(client, period="D30"):
    """
    Execute Exchange Mailbox audit against Microsoft Graph for the given tenant client.
    Returns structured analysis dictionary.
    """
    raw_data = client.get_mailbox_usage_detail(period=period)
    reader = csv.DictReader(io.StringIO(raw_data))
    rows = list(reader)

    total_mailboxes = len(rows)
    total_bytes = 0
    active_count = 0
    over_80_quota = []
    over_100_quota = []
    high_storage_no_archive = []
    inactive_accounts = []
    all_users = []

    for r in rows:
        upn = r.get("User Principal Name", "")
        name = r.get("Display Name", "")
        bytes_used = int(r.get("Storage Used (Byte)", 0) or 0)
        prohibit_send = int(r.get("Prohibit Send Quota (Byte)", 0) or 0)
        has_archive = str(r.get("Has Archive", "False")).lower() == "true"
        last_activity = r.get("Last Activity Date", "")
        is_deleted = str(r.get("Is Deleted", "False")).lower() == "true"
        items = int(r.get("Item Count", 0) or 0)

        if is_deleted:
            continue

        total_bytes += bytes_used
        used_gb = round(bytes_used / (1024**3), 2)
        quota_gb = round(prohibit_send / (1024**3), 1) if prohibit_send > 0 else 50.0
        pct = round((bytes_used / prohibit_send * 100), 1) if prohibit_send > 0 else 0.0

        user_summary = {
            "name": name,
            "upn": upn,
            "used_gb": used_gb,
            "quota_gb": quota_gb,
            "pct": pct,
            "items": items,
            "has_archive": has_archive,
            "last_activity": last_activity or "No activity (>30d)"
        }

        if last_activity:
            active_count += 1
        else:
            inactive_accounts.append(user_summary)

        if pct >= 100:
            over_100_quota.append(user_summary)
        elif pct >= 80:
            over_80_quota.append(user_summary)

        if used_gb >= 25.0 and not has_archive:
            high_storage_no_archive.append(user_summary)

        all_users.append(user_summary)

    all_users.sort(key=lambda x: x["used_gb"], reverse=True)
    inactive_accounts.sort(key=lambda x: x["used_gb"], reverse=True)

    return {
        "task_name": "Exchange Online Mailbox & Archiving Audit",
        "period": period,
        "audited_at": datetime.now().isoformat(),
        "summary": {
            "total_mailboxes": total_mailboxes,
            "active_mailboxes": active_count,
            "inactive_mailboxes": len(inactive_accounts),
            "total_storage_gb": round(total_bytes / (1024**3), 2),
            "total_storage_tb": round(total_bytes / (1024**4), 2),
            "critical_over_100_pct": len(over_100_quota),
            "warning_over_80_pct": len(over_80_quota),
            "high_storage_no_archive_count": len(high_storage_no_archive)
        },
        "critical_over_quota": over_100_quota,
        "warning_over_quota": over_80_quota,
        "high_storage_no_archive": high_storage_no_archive,
        "top_mailboxes": all_users[:15],
        "inactive_accounts": inactive_accounts
    }
