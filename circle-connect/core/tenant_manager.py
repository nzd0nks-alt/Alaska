#!/usr/bin/env python3
"""
Tenant Manager for Circle Connect
Loads tenant configurations and orchestrates M365GraphClient creation.
Supports using Master Multi-Tenant App Credentials or Dedicated App Credentials per tenant.
"""

import os
import json
from pathlib import Path
from core.m365_client import M365GraphClient

BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / "config" / "tenants.json"
ENV_FILE = BASE_DIR / ".env"

def load_local_env():
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

load_local_env()

class TenantManager:
    def __init__(self, config_file=CONFIG_FILE):
        self.config_file = config_file
        self.master_app = {}
        self.tenants = {}
        self.load()

    def load(self):
        """Load tenant configuration from JSON or environment."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.master_app = data.get("masterApp", {})
                    for t in data.get("tenants", []):
                        self.tenants[t["id"].lower()] = t
            except Exception as e:
                print(f"[Warning] Failed to load {self.config_file}: {e}")

        # Check environment variables for master app fallback
        if not self.master_app.get("clientId"):
            self.master_app["clientId"] = os.getenv("CIRCLE_MSP_CLIENT_ID", "")
            self.master_app["clientSecret"] = os.getenv("CIRCLE_MSP_CLIENT_SECRET", "")

    def list_tenants(self):
        """Return list of all configured tenants."""
        return [
            {
                "id": t["id"],
                "displayName": t.get("displayName", t["id"]),
                "primaryDomain": t.get("primaryDomain", ""),
                "tenantId": t.get("tenantId", ""),
                "useMasterApp": t.get("useMasterApp", False)
            }
            for t in self.tenants.values()
        ]

    def get_client(self, tenant_id):
        """Instantiate an authenticated M365GraphClient for a specific tenant."""
        tid = tenant_id.lower()
        if tid not in self.tenants:
            available = ", ".join(self.tenants.keys())
            raise ValueError(f"Tenant '{tenant_id}' not found. Available tenants: {available}")

        t = self.tenants[tid]
        
        # Determine whether to use Master Multi-Tenant credentials or Dedicated credentials
        if t.get("useMasterApp", False):
            client_id = self.master_app.get("clientId")
            client_secret = self.master_app.get("clientSecret")
            if not client_id or not client_secret:
                raise ValueError(
                    f"Tenant '{tenant_id}' is configured to use Master App, but masterApp credentials are not set in config/tenants.json or .env"
                )
        else:
            client_id = t.get("clientId")
            client_secret = t.get("clientSecret")
            if not client_id or not client_secret:
                raise ValueError(f"Tenant '{tenant_id}' is missing dedicated clientId or clientSecret.")

        return M365GraphClient(
            tenant_id=t["tenantId"],
            client_id=client_id,
            client_secret=client_secret
        )

    def add_tenant(self, tenant_id, display_name, primary_domain, azure_tenant_id, use_master_app=True, client_id="", client_secret=""):
        """Programmatically register a new tenant."""
        entry = {
            "id": tenant_id.lower().strip(),
            "displayName": display_name.strip(),
            "primaryDomain": primary_domain.strip(),
            "tenantId": azure_tenant_id.strip(),
            "useMasterApp": use_master_app
        }
        if not use_master_app:
            entry["clientId"] = client_id.strip()
            entry["clientSecret"] = client_secret.strip()

        self.tenants[entry["id"]] = entry
        
        data = {
            "masterApp": self.master_app,
            "tenants": list(self.tenants.values())
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"[+] Tenant '{display_name}' ({tenant_id}) successfully saved to {self.config_file}")
