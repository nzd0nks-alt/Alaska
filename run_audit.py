#!/usr/bin/env python3
"""
Master Audit CLI Runner
Runs catalogued M365 tasks across any configured tenant and generates reports & Netlify dashboard.
Usage:
  python3 run_audit.py --list-tenants
  python3 run_audit.py --tenant alaska --report all
  python3 run_audit.py --tenant alaska --report exchange
  python3 run_audit.py --tenant alaska --report sharepoint
"""

import sys
import argparse
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from tenant_manager import TenantManager
from tasks.task_exchange_report import run_exchange_audit
from tasks.task_sharepoint_report import run_sharepoint_audit
from tasks.task_dashboard import generate_html_dashboard

def main():
    parser = argparse.ArgumentParser(description="Multi-tenant Microsoft 365 Audit Runner")
    parser.add_argument("--tenant", default="alaska", help="Tenant ID from tenants.json (default: alaska)")
    parser.add_argument("--report", choices=["all", "exchange", "sharepoint"], default="all", help="Report to run")
    parser.add_argument("--period", default="D30", help="Report period (e.g. D7, D30, D90, D180)")
    parser.add_argument("--list-tenants", action="store_true", help="List all configured tenants")
    parser.add_argument("--deploy-netlify", action="store_true", help="Deploy the resulting dashboard to Netlify")

    args = parser.parse_args()
    mgr = TenantManager()

    if args.list_tenants:
        print("\nConfigured Tenants:")
        for t in mgr.list_tenants():
            print(f" - [{t['id']}] {t['displayName']} (Domain: {t['primaryDomain']}, TenantId: {t['tenantId']})")
        return

    print(f"\n========================================================")
    print(f" Starting M365 Audit for Tenant: [{args.tenant.upper()}]")
    print(f"========================================================")

    client = mgr.get_client(args.tenant)
    tenant_info = mgr.tenants.get(args.tenant.lower(), {})
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    reports_dir = BASE_DIR / "reports"
    web_dir = BASE_DIR / "web"
    reports_dir.mkdir(exist_ok=True)
    web_dir.mkdir(exist_ok=True)

    exchange_res = None
    sharepoint_res = None

    if args.report in ["all", "exchange"]:
        print("\n[*] Running Exchange Online Mailbox & Quota Audit...")
        exchange_res = run_exchange_audit(client, period=args.period)
        ex_file = reports_dir / f"{args.tenant}_exchange_{date_str}.json"
        with open(ex_file, "w", encoding="utf-8") as f:
            json.dump(exchange_res, f, indent=2)
        print(f"    Exchange report saved to: {ex_file}")
        print(f"    Total Mailboxes: {exchange_res['summary']['total_mailboxes']} | Storage: {exchange_res['summary']['total_storage_tb']} TB")
        print(f"    Over Quota / Warning: {exchange_res['summary']['critical_over_100_pct']} critical, {exchange_res['summary']['warning_over_80_pct']} warnings")

    if args.report in ["all", "sharepoint"]:
        print("\n[*] Running SharePoint Storage & Archiving Audit...")
        sharepoint_res = run_sharepoint_audit(client, period=args.period)
        sp_file = reports_dir / f"{args.tenant}_sharepoint_{date_str}.json"
        with open(sp_file, "w", encoding="utf-8") as f:
            json.dump(sharepoint_res, f, indent=2)
        print(f"    SharePoint report saved to: {sp_file}")
        print(f"    Total Sites: {sharepoint_res['summary']['total_sites']} | Storage: {sharepoint_res['summary']['total_storage_tb']} TB")
        print(f"    Est. Annual Archiving Savings: ${sharepoint_res['summary']['est_annual_savings_nzd']:,.0f} NZD")

    if args.report == "all" and exchange_res and sharepoint_res:
        print("\n[*] Generating Executive HTML Dashboard...")
        dash_file = reports_dir / f"{args.tenant}_dashboard_{date_str}.html"
        web_file = web_dir / "index.html"
        generate_html_dashboard(tenant_info, exchange_res, sharepoint_res, dash_file)
        generate_html_dashboard(tenant_info, exchange_res, sharepoint_res, web_file)
        print(f"    Dashboard generated: {dash_file}")
        print(f"    Web build updated: {web_file}")

    print("\n[+] Audit completed successfully!")

if __name__ == "__main__":
    main()

