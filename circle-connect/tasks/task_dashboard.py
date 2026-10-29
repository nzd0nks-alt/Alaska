#!/usr/bin/env python3
"""
Dashboard Generator for Circle Connect
Generates:
1. Individual Tenant Dashboard (web/tenants/{tenant_id}/dashboard.html)
2. Master MSP Multi-Tenant Portal (web/index.html)
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
WEB_DIR = BASE_DIR / "web"

THEME_CSS = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    body { font-family: 'Inter', sans-serif; transition: background-color 0.25s ease, color 0.25s ease; }

    /* CIRCLE IT THEME (Default) */
    [data-theme="circleit"][data-mode="dark"] {
      --bg-page: #001a22;
      --bg-surface: #003343;
      --bg-card: #042530;
      --bg-card-hover: #073847;
      --bg-header: #00222d;
      --border-color: #0b4959;
      --border-subtle: #083c4a;
      --text-main: #f0fbfc;
      --text-muted: #7ad5df;
      --brand-primary: #45b9ca;
      --brand-btn: #45b9ca;
      --brand-btn-text: #00222d;
      --kpi-bg: rgba(69, 185, 202, 0.12);
      --table-header: #002936;
      --table-row-hover: rgba(69, 185, 202, 0.08);
    }
    [data-theme="circleit"][data-mode="light"] {
      --bg-page: #f0f9fb;
      --bg-surface: #ffffff;
      --bg-card: #ffffff;
      --bg-card-hover: #eaf8fa;
      --bg-header: #ffffff;
      --border-color: #d0edf2;
      --border-subtle: #e1f4f7;
      --text-main: #002733;
      --text-muted: #075566;
      --brand-primary: #07586a;
      --brand-btn: #07586a;
      --brand-btn-text: #ffffff;
      --kpi-bg: #eaf8fa;
      --table-header: #e6f6f9;
      --table-row-hover: #f3fbfc;
    }

    /* ALASKA THEME */
    [data-theme="alaska"][data-mode="dark"] {
      --bg-page: #0e1412;
      --bg-surface: #15221e;
      --bg-card: #1b2b26;
      --bg-card-hover: #223730;
      --bg-header: #111a17;
      --border-color: #26423a;
      --border-subtle: #1e332c;
      --text-main: #f2f7f5;
      --text-muted: #93b3a9;
      --brand-primary: #e85d04;
      --brand-btn: #e85d04;
      --brand-btn-text: #ffffff;
      --kpi-bg: rgba(232, 93, 4, 0.12);
      --table-header: #182823;
      --table-row-hover: rgba(232, 93, 4, 0.08);
    }
    [data-theme="alaska"][data-mode="light"] {
      --bg-page: #f8faf9;
      --bg-surface: #ffffff;
      --bg-card: #ffffff;
      --bg-card-hover: #f2f7f5;
      --bg-header: #ffffff;
      --border-color: #e2e8e5;
      --border-subtle: #edf2f0;
      --text-main: #111827;
      --text-muted: #4b5563;
      --brand-primary: #1f3a34;
      --brand-btn: #1f3a34;
      --brand-btn-text: #ffffff;
      --kpi-bg: #f2f7f5;
      --table-header: #f2f7f5;
      --table-row-hover: #f9fbfb;
    }

    body { background-color: var(--bg-page); color: var(--text-main); }
    .bg-theme-header { background-color: var(--bg-header); }
    .bg-theme-card { background-color: var(--bg-card); }
    .border-theme { border-color: var(--border-color); }
    .border-subtle { border-color: var(--border-subtle); }
    .text-theme-main { color: var(--text-main); }
    .text-theme-muted { color: var(--text-muted); }
    .text-theme-brand { color: var(--brand-primary); }
    .bg-theme-brand { background-color: var(--brand-btn); color: var(--brand-btn-text); }
    .bg-theme-kpi { background-color: var(--kpi-bg); }
    .bg-theme-th { background-color: var(--table-header); }
    .hover-theme-row:hover { background-color: var(--table-row-hover); }
"""

THEME_JS = """
    function applySavedTheme() {
      const savedTheme = localStorage.getItem('circle_theme') || 'circleit';
      const savedMode = localStorage.getItem('circle_mode') || 'dark';
      document.documentElement.setAttribute('data-theme', savedTheme);
      document.documentElement.setAttribute('data-mode', savedMode);
      const sel = document.getElementById('themeSelector');
      if (sel) sel.value = savedTheme;
      updateModeButton(savedMode);
    }
    function changeTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('circle_theme', theme);
    }
    function toggleMode() {
      const current = document.documentElement.getAttribute('data-mode') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-mode', next);
      localStorage.setItem('circle_mode', next);
      updateModeButton(next);
    }
    function updateModeButton(mode) {
      const icon = document.getElementById('modeIcon');
      const label = document.getElementById('modeLabel');
      if (mode === 'dark') {
        if (icon) icon.className = 'fa-solid fa-sun text-amber-400';
        if (label) label.textContent = 'Light';
      } else {
        if (icon) icon.className = 'fa-solid fa-moon text-indigo-500';
        if (label) label.textContent = 'Dark';
      }
    }
    document.addEventListener('DOMContentLoaded', applySavedTheme);
    applySavedTheme();
"""

def generate_tenant_dashboard(tenant_info, exchange_data, sharepoint_data, output_file):
    """Render client-specific dashboard."""
    ex_sum = exchange_data["summary"]
    sp_sum = sharepoint_data["summary"]
    t_id = tenant_info.get("id", "alaska")

    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="circleit" data-mode="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{tenant_info.get('displayName')} - M365 Cloud Audit</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>{THEME_CSS}</style>
</head>
<body class="min-h-screen">
  <header class="no-print border-b border-theme bg-theme-header sticky top-0 z-50 backdrop-blur">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <a href="../../index.html" class="h-9 w-9 rounded-lg flex items-center justify-center font-bold shadow-md bg-theme-brand" title="Back to All Tenants">
          <i class="fa-solid fa-arrow-left"></i>
        </a>
        <div>
          <h1 class="text-base sm:text-lg font-bold tracking-tight text-theme-main">{tenant_info.get('displayName')}</h1>
          <p class="text-xs text-theme-muted">Tenant: <span class="font-semibold text-theme-brand">{tenant_info.get('primaryDomain')}</span> &bull; Cloud Audit</p>
        </div>
      </div>
      <div class="flex items-center space-x-2 sm:space-x-3">
        <div class="flex items-center space-x-1.5 bg-theme-card border border-theme rounded-lg px-2.5 py-1 text-xs">
          <i class="fa-solid fa-palette text-theme-brand text-2xs"></i>
          <select id="themeSelector" onchange="changeTheme(this.value)" class="bg-transparent text-theme-main font-semibold text-xs outline-none cursor-pointer">
            <option value="circleit" class="bg-slate-900 text-white">Circle IT (Teal/Cyan)</option>
            <option value="alaska" class="bg-slate-900 text-white">Alaska (Forest/Orange)</option>
          </select>
        </div>
        <button id="modeToggleBtn" onclick="toggleMode()" class="px-2.5 py-1.5 rounded-lg border border-theme bg-theme-card text-xs font-semibold text-theme-main">
          <i id="modeIcon" class="fa-solid fa-sun text-amber-400"></i>
          <span id="modeLabel" class="hidden sm:inline">Light</span>
        </button>
        <a href="proposal.html" class="px-3 py-1.5 rounded-lg bg-theme-brand text-xs font-bold shadow-sm">
          <i class="fa-solid fa-file-contract mr-1.5"></i> Modernization Proposal
        </a>
        <button onclick="window.print()" class="px-2.5 py-1.5 rounded-lg border border-theme bg-theme-card text-xs">
          <i class="fa-solid fa-print"></i>
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
      <div class="bg-theme-card border border-theme rounded-xl p-5 shadow-sm">
        <span class="text-xs font-semibold uppercase tracking-wider text-theme-muted">Mailbox Storage</span>
        <div class="mt-3 flex items-baseline justify-between">
          <div class="text-2xl font-extrabold text-theme-main">{ex_sum['total_storage_tb']} TB</div>
          <span class="text-xs text-theme-muted">{ex_sum['total_storage_gb']:,} GB</span>
        </div>
        <p class="text-xs text-theme-muted mt-2">
          <span class="font-bold text-emerald-500">{ex_sum['active_mailboxes']}</span> active &bull; 
          <span class="font-bold text-amber-500">{ex_sum['inactive_mailboxes']}</span> inactive (>30d)
        </p>
      </div>

      <div class="bg-theme-card border border-theme rounded-xl p-5 shadow-sm">
        <span class="text-xs font-semibold uppercase tracking-wider text-theme-muted">Quota Risk Mailboxes</span>
        <div class="mt-3 flex items-baseline justify-between">
          <div class="text-2xl font-extrabold text-rose-500">{ex_sum['critical_over_100_pct'] + ex_sum['warning_over_80_pct']} Users</div>
          <span class="text-xs text-rose-500 font-bold">{ex_sum['critical_over_100_pct']} Over 100%</span>
        </div>
        <p class="text-xs text-theme-muted mt-2">Require immediate Archiving expansion</p>
      </div>

      <div class="bg-theme-card border border-theme rounded-xl p-5 shadow-sm">
        <span class="text-xs font-semibold uppercase tracking-wider text-theme-muted">SharePoint Storage</span>
        <div class="mt-3 flex items-baseline justify-between">
          <div class="text-2xl font-extrabold text-theme-main">{sp_sum['total_storage_tb']} TB</div>
          <span class="text-xs text-theme-muted">{sp_sum['total_files']:,} Files</span>
        </div>
        <p class="text-xs text-theme-muted mt-2">Across <span class="font-bold text-theme-main">{sp_sum['total_sites']}</span> sites</p>
      </div>

      <div class="bg-theme-card border border-theme rounded-xl p-5 shadow-sm">
        <span class="text-xs font-semibold uppercase tracking-wider text-theme-muted">Est. Storage Savings</span>
        <div class="mt-3 flex items-baseline justify-between">
          <div class="text-2xl font-extrabold text-emerald-500">${sp_sum['est_annual_savings_nzd']:,.0f} NZD</div>
          <span class="text-xs text-theme-muted">/ year</span>
        </div>
        <p class="text-xs text-theme-muted mt-2">By tiering <span class="font-bold text-emerald-500">{sp_sum['cold_archive_storage_gb']:,.0f} GB</span> cold sites</p>
      </div>
    </div>

    <!-- Exchange Breakdown -->
    <div class="bg-theme-card border border-theme rounded-2xl overflow-hidden shadow-sm">
      <div class="px-6 py-4 border-b border-theme bg-theme-th flex justify-between items-center">
        <h2 class="text-base font-bold text-theme-main">Exchange Online Mailbox & Quota Analysis</h2>
        <span class="text-xs px-2.5 py-1 rounded bg-theme-kpi text-theme-main font-semibold">Total: {ex_sum['total_mailboxes']} Mailboxes</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-theme-th text-theme-muted uppercase font-semibold border-b border-theme">
            <tr>
              <th class="px-6 py-3.5">User</th>
              <th class="px-6 py-3.5">Storage</th>
              <th class="px-6 py-3.5">Quota %</th>
              <th class="px-6 py-3.5">Archive</th>
              <th class="px-6 py-3.5">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y border-subtle">
"""
    for u in exchange_data["top_mailboxes"][:10]:
        pct = u["pct"]
        rec = '<span class="text-rose-500 font-bold">Enable Online Archive</span>' if pct >= 80 else '<span class="text-theme-muted">Healthy</span>'
        html += f"""            <tr class="hover-theme-row">
              <td class="px-6 py-3.5"><div class="font-bold text-theme-main">{u['name']}</div><div class="text-2xs text-theme-muted">{u['upn']}</div></td>
              <td class="px-6 py-3.5 font-medium">{u['used_gb']} GB <span class="text-theme-muted text-2xs">/ {u['quota_gb']} GB</span></td>
              <td class="px-6 py-3.5"><span class="font-bold">{pct}%</span></td>
              <td class="px-6 py-3.5">{('Yes' if u['has_archive'] else 'No')}</td>
              <td class="px-6 py-3.5">{rec}</td>
            </tr>"""

    html += f"""          </tbody>
        </table>
      </div>
    </div>

    <!-- SharePoint Breakdown -->
    <div class="bg-theme-card border border-theme rounded-2xl overflow-hidden shadow-sm">
      <div class="px-6 py-4 border-b border-theme bg-theme-th flex justify-between items-center">
        <h2 class="text-base font-bold text-theme-main">SharePoint Sites Storage & Cold Tier Opportunities</h2>
        <span class="text-xs px-2.5 py-1 rounded bg-theme-kpi text-theme-main font-semibold">Total: {sp_sum['total_sites']} Sites</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-theme-th text-theme-muted uppercase font-semibold border-b border-theme">
            <tr>
              <th class="px-6 py-3.5">Site Collection</th>
              <th class="px-6 py-3.5">Storage Used</th>
              <th class="px-6 py-3.5">Total Files</th>
              <th class="px-6 py-3.5">Stagnant %</th>
              <th class="px-6 py-3.5">Tiering Target</th>
            </tr>
          </thead>
          <tbody class="divide-y border-subtle">
"""
    for s in sharepoint_data["top_sites"][:8]:
        is_candidate = any(c["name"] == s["name"] for c in sharepoint_data["archive_candidates"])
        rec = '<span class="text-emerald-500 font-bold">M365 Cold Archive Candidate</span>' if is_candidate else '<span class="text-theme-muted">Active Tier</span>'
        html += f"""            <tr class="hover-theme-row">
              <td class="px-6 py-3.5"><div class="font-bold text-theme-main">{s['name']}</div></td>
              <td class="px-6 py-3.5 font-bold">{s['used_gb']} GB</td>
              <td class="px-6 py-3.5">{s['files']:,}</td>
              <td class="px-6 py-3.5">{s['stagnant_pct']}%</td>
              <td class="px-6 py-3.5">{rec}</td>
            </tr>"""

    html += f"""          </tbody>
        </table>
      </div>
    </div>
  </main>

  <footer class="border-t border-theme py-6 text-center text-xs text-theme-muted">
    Circle Connect M365 Automation Engine &bull; {exchange_data['audited_at'][:10]}
  </footer>
  <script>{THEME_JS}</script>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Tenant dashboard generated: {output_file}")

def generate_master_msp_portal(all_tenants_summary, output_file):
    """Generate the top-level MSP Portal listing all clients."""
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="circleit" data-mode="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Circle Connect — Multi-Tenant Microsoft 365 MSP Portal</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>{THEME_CSS}</style>
</head>
<body class="min-h-screen">
  <header class="no-print border-b border-theme bg-theme-header sticky top-0 z-50 backdrop-blur">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="h-9 w-9 rounded-lg flex items-center justify-center font-bold shadow-md bg-theme-brand">
          <i class="fa-solid fa-network-wired"></i>
        </div>
        <div>
          <h1 class="text-lg font-bold tracking-tight text-theme-main">Circle Connect MSP</h1>
          <p class="text-xs text-theme-muted">Managed Microsoft 365 Audit & Migration Command Center</p>
        </div>
      </div>
      <div class="flex items-center space-x-3">
        <button id="modeToggleBtn" onclick="toggleMode()" class="px-2.5 py-1.5 rounded-lg border border-theme bg-theme-card text-xs font-semibold text-theme-main">
          <i id="modeIcon" class="fa-solid fa-sun text-amber-400"></i>
          <span id="modeLabel" class="hidden sm:inline">Light</span>
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-2xl font-extrabold text-theme-main">Managed Client Tenants</h2>
        <p class="text-xs text-theme-muted mt-1">Select a tenant to view live audit telemetry, storage analysis, and modernization proposals.</p>
      </div>
      <span class="px-3 py-1 rounded-full text-xs font-bold bg-theme-kpi text-theme-brand border border-theme">
        {len(all_tenants_summary)} Tenants Active
      </span>
    </div>

    <!-- Tenants Card Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
"""
    for t in all_tenants_summary:
        t_id = t["id"]
        html += f"""      <div class="bg-theme-card border border-theme rounded-2xl p-6 shadow-sm hover:border-theme-brand transition space-y-4">
        <div class="flex justify-between items-start">
          <div class="h-10 w-10 rounded-xl bg-theme-kpi flex items-center justify-center text-theme-brand font-bold text-lg">
            <i class="fa-solid fa-building"></i>
          </div>
          <span class="inline-flex items-center px-2 py-0.5 rounded text-2xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1 animate-pulse"></span> Connected
          </span>
        </div>
        <div>
          <h3 class="text-base font-bold text-theme-main">{t['displayName']}</h3>
          <p class="text-xs text-theme-muted font-mono">{t['primaryDomain']}</p>
        </div>
        <div class="grid grid-cols-2 gap-3 pt-2 text-xs border-t border-subtle">
          <div class="p-2.5 rounded-lg bg-theme-header border border-theme">
            <div class="text-2xs text-theme-muted uppercase font-bold">Mailbox Storage</div>
            <div class="text-sm font-extrabold text-theme-main mt-0.5">{t.get('mailbox_tb', '2.95')} TB</div>
          </div>
          <div class="p-2.5 rounded-lg bg-theme-header border border-theme">
            <div class="text-2xs text-theme-muted uppercase font-bold">SharePoint Storage</div>
            <div class="text-sm font-extrabold text-theme-main mt-0.5">{t.get('sharepoint_tb', '4.48')} TB</div>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-2 pt-2">
          <a href="tenants/{t_id}/dashboard.html" class="px-3 py-2 rounded-lg bg-theme-brand text-xs font-bold text-center transition">
            <i class="fa-solid fa-chart-line mr-1"></i> Audit Telemetry
          </a>
          <a href="tenants/{t_id}/proposal.html" class="px-3 py-2 rounded-lg border border-theme bg-theme-header hover:bg-theme-card text-xs font-bold text-center text-theme-main transition">
            <i class="fa-solid fa-file-signature mr-1"></i> SOW Proposal
          </a>
        </div>
      </div>"""

    html += f"""    </div>
  </main>

  <footer class="border-t border-theme py-6 text-center text-xs text-theme-muted">
    Circle IT Limited &bull; Multi-Tenant MSP Automation Suite
  </footer>
  <script>{THEME_JS}</script>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Master MSP portal generated: {output_file}")
