# Circle Connect MSP — Multi-Tenant Microsoft 365 Automation Platform

A multi-tenant automation and cloud auditing suite built for **Circle IT Limited** to manage Microsoft 365 tenants, generate executive storage & mailbox audits, and produce fixed-fee modernization proposals.

---

## Architecture Overview

```
circle-connect/
├── cli.py                             # Master CLI: run audits, onboard clients, generate URLs
├── core/
│   ├── consent_generator.py           # Generates 1-click Admin Consent URLs for client onboarding
│   ├── m365_client.py                 # Graph client supporting multi-tenant & dedicated credentials
│   └── tenant_manager.py              # Central tenant registry manager
├── tasks/
│   ├── task_exchange_report.py        # Mailbox storage, quotas & inactive user discovery
│   ├── task_sharepoint_report.py      # Site storage, file activity & cold archive savings
│   └── task_dashboard.py             # Generates client dashboards & Master MSP Portal
├── config/
│   ├── tenants.template.json          # Template for managing multiple clients
│   └── tenants.json                   # Private client registry (Git-ignored)
├── web/                               # Web build deployed to Netlify (circle-m365-reports.netlify.app)
│   ├── index.html                     # Master MSP Multi-Tenant Portal & Client Directory
│   └── tenants/
│       └── alaska/
│           ├── dashboard.html         # Alaska live telemetry dashboard
│           └── proposal.html          # Alaska modernization statement of work
└── reports/                           # Timestamped JSON audit files (Git-ignored)
```

---

## Setting Up Circle IT's Master Multi-Tenant App (Method A)

With a multi-tenant app registration, Circle IT can audit **unlimited customer tenants** without needing to create new app registrations or secrets inside each customer portal.

### 1. In Circle IT's Own Entra Portal (`entra.microsoft.com` under `circleit.co.nz`):
1. Navigate to **Identity > Applications > App registrations > New registration**.
2. **Name**: `Circle Connect MSP`
3. **Supported account types**: Select **Accounts in any organizational directory (Any Microsoft Entra ID tenant - Multitenant)**.
4. **Redirect URI**: Web -> `https://circleit.co.nz`
5. Click **Register**.
6. Under **API permissions**:
   - Add **Microsoft Graph > Application permissions**:
     - `Reports.Read.All`
     - `Sites.ReadWrite.All`
     - `Group.ReadWrite.All`
     - `User.Read.All`
   - Click **Grant admin consent for Circle IT**.
7. Under **Certificates & secrets**:
   - Create a Client Secret and copy its value.
8. Store these in `circle-connect/config/tenants.json` under `masterApp`:
   ```json
   {
     "masterApp": {
       "clientId": "<CIRCLE_IT_MULTI_TENANT_CLIENT_ID>",
       "clientSecret": "<CIRCLE_IT_CLIENT_SECRET>"
     }
   }
   ```

---

## Onboarding Any Customer Tenant (1-Click Consent)

To grant Circle Connect access to any customer tenant:

1. Generate the consent URL:
   ```bash
   python3 cli.py --consent-url
   ```
2. Open that URL while signed into the client's Microsoft tenant (or via your Microsoft Partner GDAP session).
3. Click **Accept**.
4. Register the tenant in Circle Connect:
   ```bash
   python3 cli.py --add-tenant
   ```
   *(You only need their Tenant ID and domain! No customer-specific client secret needed.)*

---

## Running Multi-Tenant Audits

```bash
# List all registered clients
python3 cli.py --list-tenants

# Run full audit for a single client (e.g. Alaska)
python3 cli.py --audit alaska

# Run full audit for ALL managed clients in one batch
python3 cli.py --audit all

# Refresh the Master MSP portal HTML
python3 cli.py --refresh-portal
```

---

## Netlify Deployment

The output in `circle-connect/web/` automatically syncs to your live Netlify site:
- **Master MSP Portal**: `https://circle-m365-reports.netlify.app/`
- **Alaska Dashboard**: `https://circle-m365-reports.netlify.app/tenants/alaska/dashboard.html`
- **Alaska SOW Proposal**: `https://circle-m365-reports.netlify.app/tenants/alaska/proposal.html`

