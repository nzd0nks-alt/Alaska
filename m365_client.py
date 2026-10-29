#!/usr/bin/env python3
"""
Alaska Construction & Interiors - Microsoft 365 Graph Client
Handles OAuth2 Client Credentials authentication and Graph API operations for:
- Automated IT & Usage Reporting
- SharePoint Document Libraries & Project Proposals
- Groups and Planner Workflows
"""

import os
import sys
import json
import time
import ssl
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

ENV_PATH = Path(__file__).parent / ".env"

def load_env():
    """Load key-value pairs from .env into os.environ if present."""
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

load_env()

TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
TOKEN_CACHE_FILE = Path(__file__).parent / ".token_cache.json"

def get_ssl_context():
    for ca in ["/private/etc/ssl/cert.pem", "/etc/ssl/cert.pem"]:
        if os.path.exists(ca):
            try:
                return ssl.create_default_context(cafile=ca)
            except Exception:
                pass
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        pass
    return ssl.create_default_context()

class M365GraphClient:
    def __init__(self, tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiry = 0
        self.ssl_ctx = get_ssl_context()

    def get_token(self, force_refresh=False):
        """Retrieve a valid Graph API access token, caching until expiry."""
        now = time.time()
        if not force_refresh and self.access_token and now < self.token_expiry - 120:
            return self.access_token

        # Check local cache file
        if not force_refresh and TOKEN_CACHE_FILE.exists():
            try:
                with open(TOKEN_CACHE_FILE, "r") as f:
                    cache = json.load(f)
                    if cache.get("expiry", 0) > now + 120:
                        self.access_token = cache.get("access_token")
                        self.token_expiry = cache.get("expiry")
                        return self.access_token
            except Exception:
                pass

        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        data = urllib.parse.urlencode({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials"
        }).encode("utf-8")

        req = urllib.request.Request(token_url, data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")

        with urllib.request.urlopen(req, context=self.ssl_ctx) as response:
            res_body = json.loads(response.read().decode("utf-8"))
            self.access_token = res_body["access_token"]
            expires_in = int(res_body.get("expires_in", 3600))
            self.token_expiry = now + expires_in

            try:
                with open(TOKEN_CACHE_FILE, "w") as f:
                    json.dump({"access_token": self.access_token, "expiry": self.token_expiry}, f)
            except Exception:
                pass

        return self.access_token

    def request(self, endpoint, method="GET", body=None, headers=None, raw_response=False):
        """Make an authenticated request to Microsoft Graph API."""
        token = self.get_token()
        if not endpoint.startswith("https://"):
            url = f"https://graph.microsoft.com/v1.0/{endpoint.lstrip('/')}"
        else:
            url = endpoint

        req_headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        if headers:
            req_headers.update(headers)

        data = None
        if body is not None:
            if isinstance(body, (dict, list)):
                data = json.dumps(body).encode("utf-8")
                req_headers["Content-Type"] = "application/json"
            elif isinstance(body, bytes):
                data = body
            elif isinstance(body, str):
                data = body.encode("utf-8")

        req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
        try:
            with urllib.request.urlopen(req, context=self.ssl_ctx) as resp:
                raw = resp.read()
                if raw_response:
                    return raw
                try:
                    return json.loads(raw.decode("utf-8"))
                except Exception:
                    return raw.decode("utf-8")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            print(f"[Error {e.code}] {e.reason}: {err_body}", file=sys.stderr)
            raise

    # --- REPORTING ENDPOINTS ---
    def get_mailbox_usage_detail(self, period="D30"):
        """Get Exchange mailbox usage details."""
        endpoint = f"reports/getMailboxUsageDetail(period='{period}')"
        return self.request(endpoint)

    def get_sharepoint_site_usage_detail(self, period="D30"):
        """Get SharePoint site usage storage detail."""
        endpoint = f"reports/getSharePointSiteUsageDetail(period='{period}')"
        return self.request(endpoint)

    def get_m365_active_user_detail(self, period="D30"):
        """Get active user activity details across all M365 services."""
        endpoint = f"reports/getOffice365ActiveUserDetail(period='{period}')"
        return self.request(endpoint)

    # --- SITES & PROPOSALS ENDPOINTS ---
    def list_sites(self, query=None):
        """Search or list SharePoint sites in the Alaska tenant."""
        if query:
            endpoint = f"sites?search={urllib.parse.quote(query)}"
        else:
            endpoint = "sites/root"
        return self.request(endpoint)

    def list_groups(self):
        """List groups (teams / project groups)."""
        return self.request("groups?$select=id,displayName,description,mail&$top=25")

    def get_group_plans(self, group_id):
        """List Planner plans belonging to a Group."""
        return self.request(f"groups/{group_id}/planner/plans")

if __name__ == "__main__":
    client = M365GraphClient()
    print("Testing token retrieval...")
    token = client.get_token()
    print("Token retrieved successfully! (Length:", len(token), ")")
    print("\nFetching SharePoint root site...")
    root_site = client.list_sites()
    print("Root site:", json.dumps(root_site, indent=2))
    print("\nFetching first few Groups...")
    groups = client.list_groups()
    print(f"Groups found: {len(groups.get('value', []))}")
    for g in groups.get('value', [])[:5]:
        print(f" - {g.get('displayName')} (ID: {g.get('id')})")
