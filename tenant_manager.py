#!/usr/bin/env python3
"""
Tenant Manager
Loads and manages Microsoft 365 tenant configurations for multi-tenant automated audits and operations.
"""

import os
import json
from pathlib import Path
from m365_client import M365GraphClient

BASE_DIR = Path(__file__).parent
TENANTS_CONFIG_FILE = BASE_DIR / "tenants" / "tenants.json"

class TenantManager:
    def __init__(self, config_file=TENANTS_CONFIG_FILE):
        self.config_file = config_file
        self.tenants = {}
        self.load_tenants()

    def load_tenants(self):
        """Load tenant configurations from json file or environment fallback."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data.get("tenants", []):
                        self.tenants[item["id"].lower()] = item
            except Exception as e:
                print(f"[Warning] Failed to read {self.config_file}: {e}")

        # Fallback to .env default if not present
        if "alaska" not in self.tenants:
            tenant_id = os.getenv("AZURE_TENANT_ID")
            client_id = os.getenv("AZURE_CLIENT_ID")
            client_secret = os.getenv("AZURE_CLIENT_SECRET")
            if tenant_id and client_id and client_secret:
                self.tenants["alaska"] = {
                    "id": "alaska",
                    "displayName": "Alaska Construction & Interiors",
                    "primaryDomain": os.getenv("PRIMARY_DOMAIN", "alaska.co.nz"),
                    "tenantId": tenant_id,
                    "clientId": client_id,
                    "clientSecret": client_secret
                }

    def list_tenants(self):
        """Return list of configured tenant summaries."""
        return [
            {
                "id": t["id"],
                "displayName": t.get("displayName", t["id"]),
                "primaryDomain": t.get("primaryDomain", ""),
                "tenantId": t.get("tenantId", "")
            }
            for t in self.tenants.values()
        ]

    def get_client(self, tenant_id="alaska"):
        """Get an authenticated M365GraphClient for the specified tenant."""
        tid = tenant_id.lower()
        if tid not in self.tenants:
            available = ", ".join(self.tenants.keys())
            raise ValueError(f"Tenant '{tenant_id}' not found. Configured tenants: {available}")

        t = self.tenants[tid]
        return M365GraphClient(
            tenant_id=t["tenantId"],
            client_id=t["clientId"],
            client_secret=t["clientSecret"]
        )

if __name__ == "__main__":
    mgr = TenantManager()
    print("Configured tenants:")
    for t in mgr.list_tenants():
        print(f" - [{t['id']}] {t['displayName']} ({t['primaryDomain']})")
