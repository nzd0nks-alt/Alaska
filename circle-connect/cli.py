#!/usr/bin/env python3
"""
Circle Connect MSP - Master Command Line Interface
Orchestrates multi-tenant audits, client onboarding, admin consent URLs, and Netlify deployment.
"""

import sys
import glob
import argparse
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from core.tenant_manager import TenantManager
from core.consent_generator import generate_consent_url
from tasks.task_exchange_report import run_exchange_audit
from tasks.task_sharepoint_report import run_sharepoint_audit
from tasks.task_dashboard import generate_tenant_dashboard, generate_master_msp_portal

def get_tenant_latest_stats(tenant_id):
    """Retrieve the latest storage metrics from saved reports if available."""
    reports_dir = BASE_DIR / "reports"
    ex_files = sorted(glob.glob(str(reports_dir / f"{tenant_id}_exchange_*.json")), reverse=True)
    sp_files = sorted(glob.glob(str(reports_dir / f"{tenant_id}_sharepoint_*.json")), reverse=True)
    
    mb_tb = "—"
    sp_tb = "—"
    status = "Pending Initial Audit"

    if ex_files and sp_files:
        try:
            with open(ex_files[0], "r", encoding="utf-8") as f:
                ex_data = json.load(f)
                mb_tb = f"{ex_data['summary']['total_storage_tb']} TB"
            with open(sp_files[0], "r", encoding="utf-8") as f:
                sp_data = json.load(f)
                sp_tb = f"{sp_data['summary']['total_storage_tb']} TB"
            status = "Audited & Active"
        except Exception:
            pass

    return mb_tb, sp_tb, status

def compile_all_tenant_summaries(mgr, fresh_results=None):
    """Compile summary metrics for all registered tenants for the Master Portal."""
    fresh_map = {r["id"]: r for r in (fresh_results or [])}
    summaries = []

    for tid, t in mgr.tenants.items():
        if tid in fresh_map:
            summaries.append(fresh_map[tid])
        else:
            mb_tb, sp_tb, status = get_tenant_latest_stats(tid)
            has_dash = (BASE_DIR / "web" / "tenants" / tid / "dashboard.html").exists()
            has_prop = (BASE_DIR / "web" / "tenants" / tid / "proposal.html").exists()
            summaries.append({
                "id": tid,
                "displayName": t.get("displayName", tid),
                "primaryDomain": t.get("primaryDomain", ""),
                "mailbox_tb": mb_tb,
                "sharepoint_tb": sp_tb,
                "status": status if has_dash else "Pending Initial Audit",
                "has_dashboard": has_dash,
                "has_proposal": has_prop
            })

    return summaries

def audit_tenant(mgr, tenant_id, period="D30"):
    """Run full audit for a single tenant."""
    print(f"\n========================================================")
    print(f" Auditing Tenant: [{tenant_id.upper()}]")
    print(f"========================================================")
    client = mgr.get_client(tenant_id)
    t_info = mgr.tenants.get(tenant_id.lower(), {})
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    
    reports_dir = BASE_DIR / "reports"
    web_tenant_dir = BASE_DIR / "web" / "tenants" / tenant_id.lower()
    reports_dir.mkdir(exist_ok=True)
    web_tenant_dir.mkdir(parents=True, exist_ok=True)

    print("[*] Running Exchange Online Mailbox & Quota Audit...")
    ex_res = run_exchange_audit(client, period=period)
    ex_file = reports_dir / f"{tenant_id}_exchange_{date_str}.json"
    with open(ex_file, "w", encoding="utf-8") as f:
        json.dump(ex_res, f, indent=2)

    print("[*] Running SharePoint Storage & Archiving Audit...")
    sp_res = run_sharepoint_audit(client, period=period)
    sp_file = reports_dir / f"{tenant_id}_sharepoint_{date_str}.json"
    with open(sp_file, "w", encoding="utf-8") as f:
        json.dump(sp_res, f, indent=2)

    print("[*] Generating Tenant Dashboard...")
    dash_file = web_tenant_dir / "dashboard.html"
    generate_tenant_dashboard(t_info, ex_res, sp_res, dash_file)

    return {
        "id": tenant_id,
        "displayName": t_info.get("displayName", tenant_id),
        "primaryDomain": t_info.get("primaryDomain", ""),
        "mailbox_tb": f"{ex_res['summary']['total_storage_tb']} TB",
        "sharepoint_tb": f"{sp_res['summary']['total_storage_tb']} TB",
        "status": "Audited & Active",
        "has_dashboard": True,
        "has_proposal": (web_tenant_dir / "proposal.html").exists()
    }

def main():
    parser = argparse.ArgumentParser(description="Circle Connect - Multi-Tenant M365 Automation Platform")
    parser.add_argument("--audit", help="Audit specific tenant ID (e.g. 'alaska') or 'all'")
    parser.add_argument("--list-tenants", action="store_true", help="List all registered tenants")
    parser.add_argument("--consent-url", nargs="?", const="", help="Generate 1-click Admin Consent URL for onboarding")
    parser.add_argument("--add-tenant", action="store_true", help="Interactive wizard to add a new client tenant")
    parser.add_argument("--period", default="D30", help="Audit reporting period (default: D30)")
    parser.add_argument("--refresh-portal", action="store_true", help="Rebuild master MSP portal HTML")

    args = parser.parse_args()
    mgr = TenantManager()

    if args.list_tenants:
        print("\nCircle Connect Registered Tenants:")
        for t in mgr.list_tenants():
            auth_mode = "Master Multi-Tenant App" if t.get("useMasterApp") else "Dedicated App"
            print(f" - [{t['id']}] {t['displayName']} ({t['primaryDomain']}) | Mode: {auth_mode}")
        return

    if args.consent_url is not None:
        client_id = args.consent_url or mgr.master_app.get("clientId")
        if not client_id:
            print("[Error] No Client ID provided. Run: python3 cli.py --consent-url <YOUR_CIRCLE_IT_CLIENT_ID>")
            return
        url = generate_consent_url(client_id)
        print("\n========================================================")
        print(" Circle IT Multi-Tenant App - Admin Consent URL")
        print("========================================================")
        print("\nOpen or send this URL to customer admin to grant consent:\n")
        print(url)
        print("\n========================================================\n")
        return

    if args.add_tenant:
        print("\n=== Register New Client Tenant in Circle Connect ===")
        t_id = input("Tenant Short ID (e.g. 'acme', 'cango', 'vetta'): ").strip().lower()
        d_name = input("Display Name (e.g. 'Acme Corporation'): ").strip()
        domain = input("Primary Domain (e.g. 'acme.co.nz'): ").strip()
        azure_id = input("Azure Directory (Tenant) ID GUID: ").strip()
        use_master = input("Use Circle IT Master Multi-Tenant App? (Y/n): ").strip().lower() != "n"
        
        c_id = ""
        c_sec = ""
        if not use_master:
            c_id = input("Dedicated Application (client) ID: ").strip()
            c_sec = input("Dedicated Client Secret: ").strip()

        mgr.add_tenant(t_id, d_name, domain, azure_id, use_master, c_id, c_sec)
        
        # Refresh master portal to show new card
        portal_file = BASE_DIR / "web" / "index.html"
        summaries = compile_all_tenant_summaries(mgr)
        generate_master_msp_portal(summaries, portal_file)
        print(f"\n[+] Master MSP Portal updated at {portal_file}")
        print(f"[+] Run: python3 cli.py --audit {t_id} to execute the first audit!")
        return

    if args.audit:
        target = args.audit.lower()
        fresh = []
        if target == "all":
            for tid in mgr.tenants.keys():
                s = audit_tenant(mgr, tid, period=args.period)
                fresh.append(s)
        else:
            s = audit_tenant(mgr, target, period=args.period)
            fresh.append(s)

        # Update Master MSP Portal with all tenants (fresh + cached)
        portal_file = BASE_DIR / "web" / "index.html"
        all_summaries = compile_all_tenant_summaries(mgr, fresh_results=fresh)
        generate_master_msp_portal(all_summaries, portal_file)
        print(f"\n[+] Master MSP Portal updated at {portal_file}")
        return

    if args.refresh_portal:
        portal_file = BASE_DIR / "web" / "index.html"
        all_summaries = compile_all_tenant_summaries(mgr)
        generate_master_msp_portal(all_summaries, portal_file)
        print(f"[+] Master MSP portal refreshed: {portal_file}")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
