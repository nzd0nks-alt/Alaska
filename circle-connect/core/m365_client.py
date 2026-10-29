#!/usr/bin/env python3
"""
Multi-Tenant Microsoft Graph API Client for Circle Connect
Handles OAuth2 token requests against any Microsoft Entra ID tenant using:
- Master Multi-Tenant Client Credentials, OR
- Dedicated Client-Specific Credentials
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
    def __init__(self, tenant_id, client_id, client_secret, token_cache_dir=None):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_cache_dir = Path(token_cache_dir) if token_cache_dir else Path(__file__).parent.parent / ".cache"
        self.token_cache_dir.mkdir(exist_ok=True)
        self.token_cache_file = self.token_cache_dir / f"token_{self.tenant_id[:8]}.json"
        self.access_token = None
        self.token_expiry = 0
        self.ssl_ctx = get_ssl_context()

    def get_token(self, force_refresh=False):
        """Retrieve a valid Graph API access token for this tenant."""
        now = time.time()
        if not force_refresh and self.access_token and now < self.token_expiry - 120:
            return self.access_token

        # Check local cache file
        if not force_refresh and self.token_cache_file.exists():
            try:
                with open(self.token_cache_file, "r") as f:
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
                with open(self.token_cache_file, "w") as f:
                    json.dump({"access_token": self.access_token, "expiry": self.token_expiry}, f)
            except Exception:
                pass

        return self.access_token

    def request(self, endpoint, method="GET", body=None, headers=None, raw_response=False):
        """Make an authenticated request to Microsoft Graph API for this tenant."""
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

    # Reporting endpoints
    def get_mailbox_usage_detail(self, period="D30"):
        return self.request(f"reports/getMailboxUsageDetail(period='{period}')")

    def get_sharepoint_site_usage_detail(self, period="D30"):
        return self.request(f"reports/getSharePointSiteUsageDetail(period='{period}')")

    def get_m365_active_user_detail(self, period="D30"):
        return self.request(f"reports/getOffice365ActiveUserDetail(period='{period}')")

    def list_sites(self, query=None):
        if query:
            return self.request(f"sites?search={urllib.parse.quote(query)}")
        return self.request("sites/root")

    def list_groups(self):
        return self.request("groups?$select=id,displayName,description,mail&$top=25")
