#!/usr/bin/env python3
"""
Consent URL Generator for Circle IT Multi-Tenant MSP App
Generates the 1-click Microsoft Entra ID admin consent URL for onboarding new client tenants.
"""

import urllib.parse

def generate_consent_url(client_id, redirect_uri="https://circleit.co.nz", state="circle-connect-onboard"):
    """
    Generate admin consent URL for a multi-tenant Microsoft Entra application.
    When a customer admin (or partner admin) opens this URL and accepts,
    the Circle IT app is provisioned into their tenant with all requested Graph permissions.
    """
    base_url = "https://login.microsoftonline.com/common/adminconsent"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"

if __name__ == "__main__":
    import sys
    client_id = sys.argv[1] if len(sys.argv) > 1 else "YOUR_CIRCLE_IT_CLIENT_ID"
    url = generate_consent_url(client_id)
    print("\n========================================================")
    print(" Circle IT Multi-Tenant App - Admin Consent URL")
    print("========================================================")
    print(f"\nSend this link to the client admin, or open it while signed in to their tenant:\n")
    print(url)
    print("\nOnce accepted, Circle IT has permission to run audits on their tenant!")

