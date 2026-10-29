#!/usr/bin/env python3
"""
Task: Executive Audit Dashboard Generator
Generates a standalone, responsive HTML dashboard for Netlify deployment and local reporting.
Includes customizable themes: Circle IT (Teal/Cyan), Alaska (Forest/Orange), and Modern Slate,
with full Light/Dark mode toggling and local storage persistence.
"""

import json
from pathlib import Path

def generate_html_dashboard(tenant_info, exchange_data, sharepoint_data, output_file):
    """Render comprehensive HTML dashboard with customizable themes."""
    ex_sum = exchange_data["summary"]
    sp_sum = sharepoint_data["summary"]

    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="circleit" data-mode="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{tenant_info.get('displayName', 'M365 Audit')} - Microsoft 365 Cloud Audit</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    body {{ font-family: 'Inter', sans-serif; transition: background-color 0.25s ease, color 0.25s ease; }}

    /* ========================================================
       THEME DEFINITIONS (CSS CUSTOM PROPERTIES)
       ======================================================== */
    /* 1. CIRCLE IT THEME (Default) */
    [data-theme="circleit"][data-mode="dark"] {{
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
      --brand-accent: #7ad5df;
      --brand-btn: #45b9ca;
      --brand-btn-text: #00222d;
      --kpi-bg: rgba(69, 185, 202, 0.12);
      --table-header: #002936;
      --table-row-hover: rgba(69, 185, 202, 0.08);
      --badge-healthy: rgba(16, 185, 129, 0.2);
      --badge-healthy-text: #34d399;
    }}
    [data-theme="circleit"][data-mode="light"] {{
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
      --brand-accent: #45b9ca;
      --brand-btn: #07586a;
      --brand-btn-text: #ffffff;
      --kpi-bg: #eaf8fa;
      --table-header: #e6f6f9;
      --table-row-hover: #f3fbfc;
      --badge-healthy: #d1fae5;
      --badge-healthy-text: #065f46;
    }}

    /* 2. ALASKA THEME (Forest Green & Construction Orange) */
    [data-theme="alaska"][data-mode="dark"] {{
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
      --brand-accent: #f48c06;
      --brand-btn: #e85d04;
      --brand-btn-text: #ffffff;
      --kpi-bg: rgba(232, 93, 4, 0.12);
      --table-header: #182823;
      --table-row-hover: rgba(232, 93, 4, 0.08);
      --badge-healthy: rgba(31, 58, 52, 0.4);
      --badge-healthy-text: #4ade80;
    }}
    [data-theme="alaska"][data-mode="light"] {{
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
      --brand-accent: #e85d04;
      --brand-btn: #1f3a34;
      --brand-btn-text: #ffffff;
      --kpi-bg: #f2f7f5;
      --table-header: #f2f7f5;
      --table-row-hover: #f9fbfb;
      --badge-healthy: #dcfce7;
      --badge-healthy-text: #166534;
    }}

    /* 3. MODERN SLATE THEME */
    [data-theme="slate"][data-mode="dark"] {{
      --bg-page: #0b0f17;
      --bg-surface: #111827;
      --bg-card: #1f2937;
      --bg-card-hover: #374151;
      --bg-header: #0f172a;
      --border-color: #374151;
      --border-subtle: #2d3748;
      --text-main: #f9fafb;
      --text-muted: #9ca3af;
      --brand-primary: #3b82f6;
      --brand-accent: #60a5fa;
      --brand-btn: #3b82f6;
      --brand-btn-text: #ffffff;
      --kpi-bg: rgba(59, 130, 246, 0.12);
      --table-header: #182234;
      --table-row-hover: rgba(59, 130, 246, 0.08);
      --badge-healthy: rgba(16, 185, 129, 0.2);
      --badge-healthy-text: #34d399;
    }}
    [data-theme="slate"][data-mode="light"] {{
      --bg-page: #f8fafc;
      --bg-surface: #ffffff;
      --bg-card: #ffffff;
      --bg-card-hover: #f1f5f9;
      --bg-header: #ffffff;
      --border-color: #e2e8f0;
      --border-subtle: #edf2f7;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --brand-primary: #2563eb;
      --brand-accent: #3b82f6;
      --brand-btn: #2563eb;
      --brand-btn-text: #ffffff;
      --kpi-bg: #f0fdf4;
      --table-header: #f1f5f9;
      --table-row-hover: #f8fafc;
      --badge-healthy: #dcfce7;
      --badge-healthy-text: #166534;
    }}

    /* Apply variables */
    body {{
      background-color: var(--bg-page);
      color: var(--text-main);
    }}
    .bg-theme-header {{ background-color: var(--bg-header); }}
    .bg-theme-card {{ background-color: var(--bg-card); }}
    .border-theme {{ border-color: var(--border-color); }}
    .border-subtle {{ border-color: var(--border-subtle); }}
    .text-theme-main {{ color: var(--text-main); }}
    .text-theme-muted {{ color: var(--text-muted); }}
    .text-theme-brand {{ color: var(--brand-primary); }}
    .bg-theme-brand {{ background-color: var(--brand-btn); color: var(--brand-btn-text); }}
    .bg-theme-kpi {{ background-color: var(--kpi-bg); }}
    .bg-theme-th {{ background-color: var(--table-header); }}
    .hover-theme-row:hover {{ background-color: var(--table-row-hover); }}

    @media print {{
      .no-print {{ display: none !important; }}
      body {{ background: white !important; color: black !important; }}
    }}
  </style>
</head>
<body class="min-h-screen">
  <!-- Top Navigation & Theme Customizer Bar -->
  <header class="no-print border-b border-theme bg-theme-header sticky top-0 z-50 backdrop-blur">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="h-9 w-9 rounded-lg flex items-center justify-center font-bold text-white shadow-md bg-theme-brand">
          <i class="fa-solid fa-cloud"></i>
        </div>
        <div>
          <h1 class="text-base sm:text-lg font-bold tracking-tight text-theme-main">{tenant_info.get('displayName', 'M365 Tenant')}</h1>
          <p class="text-xs text-theme-muted">Tenant: <span class="font-semibold text-theme-brand">{tenant_info.get('primaryDomain', '')}</span> &bull; Cloud Audit</p>
        </div>
      </div>

      <!-- Action & Customizer Controls -->
      <div class="flex items-center space-x-2 sm:space-x-3">
        <!-- Brand Theme Picker Dropdown -->
        <div class="flex items-center space-x-1.5 bg-theme-card border border-theme rounded-lg px-2.5 py-1 text-xs">
          <i class="fa-solid fa-palette text-theme-brand text-2xs"></i>
          <span class="text-theme-muted text-2xs hidden sm:inline">Theme:</span>
          <select id="themeSelector" onchange="changeTheme(this.value)" class="bg-transparent text-theme-main font-semibold text-xs outline-none cursor-pointer">
            <option value="circleit" class="bg-slate-900 text-white">Circle IT (Teal/Cyan)</option>
            <option value="alaska" class="bg-slate-900 text-white">Alaska (Forest/Orange)</option>
            <option value="slate" class="bg-slate-900 text-white">Modern Slate</option>
          </select>
        </div>

        <!-- Mode Toggle (Light/Dark) -->
        <button id="modeToggleBtn" onclick="toggleMode()" class="px-2.5 py-1.5 rounded-lg border border-theme bg-theme-card hover:opacity-90 text-xs font-semibold text-theme-main transition flex items-center space-x-1.5" title="Toggle Light/Dark Mode">
          <i id="modeIcon" class="fa-solid fa-sun text-amber-400"></i>
          <span id="modeLabel" class="hidden sm:inline">Light</span>
        </button>

        <!-- SOW Proposal Link -->
        <a href="proposal.html" class="px-3 py-1.5 rounded-lg bg-theme-brand hover:opacity-90 text-xs font-bold transition shadow-sm flex items-center">
          <i class="fa-solid fa-file-contract mr-1.5"></i> <span class="hidden sm:inline">Modernization </span>Proposal
        </a>

        <!-- Export -->
        <button onclick="window.print()" class="px-2.5 py-1.5 rounded-lg border border-theme bg-theme-card hover:opacity-90 text-xs font-medium text-theme-main transition" title="Print Report">
          <i class="fa-solid fa-print"></i>
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <!-- Executive KPI Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
      <!-- KPI 1 -->
      <div class="bg-theme-card border border-theme rounded-xl p-5 shadow-sm">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-theme-muted">Mailbox Storage</span>
          <span class="h-8 w-8 rounded-lg bg-theme-kpi flex items-center justify-center text-theme-brand">
            <i class="fa-solid fa-envelope"></i>
          </span>
        </div>
        <div class="mt-3 flex items-baseline justify-between">
          <div class="text-2xl font-extrabold text-theme-main">{ex_sum['total_storage_tb']} TB</div>
          <span class="text-xs text-theme-muted">{ex_sum['total_storage_gb']:,} GB</span>
        </div>
        <p class="text-xs text-theme-muted mt-2">
          <span class="font-bold text-emerald-500">{ex_sum['active_mailboxes']}</span> active &bull; 
          <span class="font-bold text-amber-500">{ex_sum['inactive_mailboxes']}</span> inactive (&gt;30d)
        </p>
      </div>

      <!-- KPI 2 -->
      <div class="bg-theme-card border border-theme rounded-xl p-5 shadow-sm">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-theme-muted">Quota Risk Mailboxes</span>
          <span class="h-8 w-8 rounded-lg bg-rose-500/10 text-rose-500 flex items-center justify-center">
            <i class="fa-solid fa-triangle-exclamation"></i>
          </span>
        </div>
        <div class="mt-3 flex items-baseline justify-between">
          <div class="text-2xl font-extrabold text-rose-500">
            {ex_sum['critical_over_100_pct'] + ex_sum['warning_over_80_pct']} Users
          </div>
          <span class="text-xs text-rose-500 font-bold">{ex_sum['critical_over_100_pct']} Over 100%</span>
        </div>
        <p class="text-xs text-theme-muted mt-2">Require immediate Archiving expansion</p>
      </div>

      <!-- KPI 3 -->
      <div class="bg-theme-card border border-theme rounded-xl p-5 shadow-sm">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-theme-muted">SharePoint Storage</span>
          <span class="h-8 w-8 rounded-lg bg-theme-kpi flex items-center justify-center text-theme-brand">
            <i class="fa-solid fa-folder-tree"></i>
          </span>
        </div>
        <div class="mt-3 flex items-baseline justify-between">
          <div class="text-2xl font-extrabold text-theme-main">{sp_sum['total_storage_tb']} TB</div>
          <span class="text-xs text-theme-muted">{sp_sum['total_files']:,} Files</span>
        </div>
        <p class="text-xs text-theme-muted mt-2">
          Across <span class="font-bold text-theme-main">{sp_sum['total_sites']}</span> sites ({sp_sum['active_sites']} active)
        </p>
      </div>

      <!-- KPI 4 -->
      <div class="bg-theme-card border border-theme rounded-xl p-5 shadow-sm">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold uppercase tracking-wider text-theme-muted">Est. Storage Savings</span>
          <span class="h-8 w-8 rounded-lg bg-emerald-500/10 text-emerald-500 flex items-center justify-center">
            <i class="fa-solid fa-piggy-bank"></i>
          </span>
        </div>
        <div class="mt-3 flex items-baseline justify-between">
          <div class="text-2xl font-extrabold text-emerald-500">${sp_sum['est_annual_savings_nzd']:,.0f} NZD</div>
          <span class="text-xs text-theme-muted">/ year</span>
        </div>
        <p class="text-xs text-theme-muted mt-2">
          By tiering <span class="font-bold text-emerald-500">{sp_sum['cold_archive_storage_gb']:,.0f} GB</span> cold archive sites
        </p>
      </div>
    </div>

    <!-- Urgent Action Banner if Over Quota -->
    {'<div class="rounded-xl border border-rose-500/30 bg-rose-500/10 p-4 flex items-start space-x-3"><i class="fa-solid fa-circle-exclamation text-rose-500 text-lg mt-0.5"></i><div><h3 class="text-sm font-bold text-rose-500">Action Required: Mailbox Quota Limits Reached</h3><p class="text-xs text-theme-muted mt-1">Users are currently above or near 100% of their prohibit-send threshold. Incoming and outgoing emails will bounce if not archived.</p></div></div>' if ex_sum['critical_over_100_pct'] > 0 else ''}

    <!-- SECTION 1: Exchange Mailbox Deep Dive -->
    <div class="bg-theme-card border border-theme rounded-2xl overflow-hidden shadow-sm">
      <div class="px-6 py-4 border-b border-theme flex items-center justify-between bg-theme-th">
        <div>
          <h2 class="text-base font-bold text-theme-main">Exchange Online Mailbox & Quota Analysis</h2>
          <p class="text-xs text-theme-muted">Top storage consumers and quota risk status</p>
        </div>
        <span class="text-xs px-2.5 py-1 rounded bg-theme-kpi text-theme-main font-semibold">Total: {ex_sum['total_mailboxes']} Mailboxes</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-theme-th text-theme-muted border-b border-theme uppercase font-semibold">
            <tr>
              <th class="px-6 py-3.5">User / Mailbox</th>
              <th class="px-6 py-3.5">Used Storage</th>
              <th class="px-6 py-3.5">Quota %</th>
              <th class="px-6 py-3.5">Archive Enabled</th>
              <th class="px-6 py-3.5">Last Active</th>
              <th class="px-6 py-3.5">Recommended Action</th>
            </tr>
          </thead>
          <tbody class="divide-y border-subtle">
"""

    for u in exchange_data["top_mailboxes"]:
        pct = u["pct"]
        if pct >= 100:
            badge = '<span class="px-2 py-0.5 rounded text-2xs font-extrabold bg-rose-500/20 text-rose-500 border border-rose-500/30">OVER QUOTA</span>'
            rec = '<span class="text-rose-500 font-bold">Enable Online Archive immediately</span>'
        elif pct >= 80:
            badge = '<span class="px-2 py-0.5 rounded text-2xs font-bold bg-amber-500/20 text-amber-500 border border-amber-500/30">WARNING</span>'
            rec = '<span class="text-amber-500 font-semibold">Plan Archive migration</span>'
        else:
            badge = '<span class="px-2 py-0.5 rounded text-2xs font-semibold bg-emerald-500/10 text-emerald-500">HEALTHY</span>'
            rec = '<span class="text-theme-muted">Normal</span>'

        archive_icon = '<i class="fa-solid fa-check text-emerald-500"></i> Yes' if u['has_archive'] else '<i class="fa-solid fa-xmark text-slate-400"></i> No'

        html += f"""            <tr class="hover-theme-row transition">
              <td class="px-6 py-3.5">
                <div class="font-bold text-theme-main">{u['name']}</div>
                <div class="text-2xs text-theme-muted">{u['upn']}</div>
              </td>
              <td class="px-6 py-3.5 font-medium">{u['used_gb']} GB <span class="text-theme-muted text-2xs">/ {u['quota_gb']} GB</span></td>
              <td class="px-6 py-3.5">
                <div class="flex items-center space-x-2">
                  <div class="w-20 bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 overflow-hidden">
                    <div class="h-full {'bg-rose-500' if pct >= 100 else ('bg-amber-400' if pct >= 80 else 'bg-blue-500')}" style="width: {min(pct, 100)}%"></div>
                  </div>
                  <span class="font-bold text-2xs">{pct}%</span>
                  {badge}
                </div>
              </td>
              <td class="px-6 py-3.5 font-medium">{archive_icon}</td>
              <td class="px-6 py-3.5 text-theme-muted">{u['last_activity']}</td>
              <td class="px-6 py-3.5">{rec}</td>
            </tr>
"""

    html += f"""          </tbody>
        </table>
      </div>
    </div>

    <!-- SECTION 2: SharePoint Sites & Storage Savings -->
    <div class="bg-theme-card border border-theme rounded-2xl overflow-hidden shadow-sm">
      <div class="px-6 py-4 border-b border-theme flex items-center justify-between bg-theme-th">
        <div>
          <h2 class="text-base font-bold text-theme-main">SharePoint Sites Storage & Cold Tier Opportunities</h2>
          <p class="text-xs text-theme-muted">Large sites identified for Microsoft 365 Archive / Azure Cold tiering</p>
        </div>
        <span class="text-xs px-2.5 py-1 rounded bg-theme-kpi text-theme-main font-semibold">Total: {sp_sum['total_sites']} Sites ({sp_sum['total_storage_tb']} TB)</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-theme-th text-theme-muted border-b border-theme uppercase font-semibold">
            <tr>
              <th class="px-6 py-3.5">Site Collection</th>
              <th class="px-6 py-3.5">Storage Used</th>
              <th class="px-6 py-3.5">Total Files</th>
              <th class="px-6 py-3.5">Active Files (30d)</th>
              <th class="px-6 py-3.5">Stagnant Ratio</th>
              <th class="px-6 py-3.5">Tiering Recommendation</th>
            </tr>
          </thead>
          <tbody class="divide-y border-subtle">
"""

    for s in sharepoint_data["top_sites"]:
        is_candidate = any(c["name"] == s["name"] for c in sharepoint_data["archive_candidates"])
        if is_candidate:
            rec = '<span class="inline-flex items-center text-emerald-500 font-bold"><i class="fa-solid fa-arrow-down-to-bracket mr-1"></i> M365 Cold Archive Candidate</span>'
        else:
            rec = '<span class="text-theme-muted">Standard Active Storage</span>'

        html += f"""            <tr class="hover-theme-row transition">
              <td class="px-6 py-3.5">
                <div class="font-bold text-theme-main">{s['name']}</div>
                <div class="text-2xs text-theme-muted">{s['template']}</div>
              </td>
              <td class="px-6 py-3.5 font-bold text-theme-main">{s['used_gb']:,} GB</td>
              <td class="px-6 py-3.5 text-theme-muted">{s['files']:,}</td>
              <td class="px-6 py-3.5 text-emerald-500 font-bold">{s['active_files']:,}</td>
              <td class="px-6 py-3.5">
                <div class="flex items-center space-x-2">
                  <span class="font-semibold">{s['stagnant_pct']}%</span>
                  <div class="w-16 bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 overflow-hidden">
                    <div class="h-full bg-theme-brand" style="width: {s['stagnant_pct']}%"></div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-3.5">{rec}</td>
            </tr>
"""

    html += f"""          </tbody>
        </table>
      </div>
    </div>

    <!-- SECTION 3: Executive Action Items -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-theme-card border border-theme rounded-xl p-5 shadow-sm">
        <div class="h-9 w-9 rounded-lg bg-theme-brand flex items-center justify-center font-bold mb-3">
          1
        </div>
        <h3 class="text-sm font-bold text-theme-main">SharePoint Cold Archival</h3>
        <p class="text-xs text-theme-muted mt-2 leading-relaxed">
          Move stagnant sites like <em>Archive Contracts</em> (530 GB) and <em>Archive Tenders</em> (260 GB) to Microsoft 365 Archive. Saves an estimated ~${sp_sum['est_annual_savings_nzd']:,.0f} NZD annually in overage charges.
        </p>
      </div>

      <div class="bg-theme-card border border-theme rounded-xl p-5 shadow-sm">
        <div class="h-9 w-9 rounded-lg bg-theme-brand flex items-center justify-center font-bold mb-3">
          2
        </div>
        <h3 class="text-sm font-bold text-theme-main">Resolve Quota Risks</h3>
        <p class="text-xs text-theme-muted mt-2 leading-relaxed">
          Enable Exchange Online Archiving for users nearing or over 100% (Matthew Wade, Brian Phelan, Adam Olson). This provides an additional 1.5 TB of auto-expanding archive capacity.
        </p>
      </div>

      <div class="bg-theme-card border border-theme rounded-xl p-5 shadow-sm">
        <div class="h-9 w-9 rounded-lg bg-theme-brand flex items-center justify-center font-bold mb-3">
          3
        </div>
        <h3 class="text-sm font-bold text-theme-main">License Optimization</h3>
        <p class="text-xs text-theme-muted mt-2 leading-relaxed">
          Audit the <strong>{ex_sum['inactive_mailboxes']} inactive mailboxes</strong> (&gt;30 days no sign-in). Converting departed staff mailboxes to Shared Mailboxes allows unassigning paid Exchange Online Plan 2 licenses.
        </p>
      </div>
    </div>
  </main>

  <footer class="border-t border-theme py-6 text-center text-xs text-theme-muted">
    Circle Connect M365 Automation Engine &bull; {exchange_data['audited_at'][:10]}
  </footer>

  <!-- Theme Engine Script -->
  <script>
    function applySavedTheme() {{
      const savedTheme = localStorage.getItem('circle_theme') || 'circleit';
      const savedMode = localStorage.getItem('circle_mode') || 'dark';
      document.documentElement.setAttribute('data-theme', savedTheme);
      document.documentElement.setAttribute('data-mode', savedMode);
      
      const sel = document.getElementById('themeSelector');
      if (sel) sel.value = savedTheme;
      
      updateModeButton(savedMode);
    }}

    function changeTheme(theme) {{
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('circle_theme', theme);
    }}

    function toggleMode() {{
      const current = document.documentElement.getAttribute('data-mode') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-mode', next);
      localStorage.setItem('circle_mode', next);
      updateModeButton(next);
    }}

    function updateModeButton(mode) {{
      const icon = document.getElementById('modeIcon');
      const label = document.getElementById('modeLabel');
      if (mode === 'dark') {{
        if (icon) icon.className = 'fa-solid fa-sun text-amber-400';
        if (label) label.textContent = 'Light';
      }} else {{
        if (icon) icon.className = 'fa-solid fa-moon text-indigo-500';
        if (label) label.textContent = 'Dark';
      }}
    }}

    document.addEventListener('DOMContentLoaded', applySavedTheme);
    applySavedTheme();
  </script>
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Report generated successfully at: {output_file}")
