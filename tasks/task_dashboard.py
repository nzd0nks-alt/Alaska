#!/usr/bin/env python3
"""
Task: Executive Audit Dashboard Generator
Generates a standalone, responsive HTML dashboard for Netlify deployment and local reporting.
"""

import json
from pathlib import Path

def generate_html_dashboard(tenant_info, exchange_data, sharepoint_data, output_file):
    """Render comprehensive HTML dashboard."""
    ex_sum = exchange_data["summary"]
    sp_sum = sharepoint_data["summary"]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{tenant_info.get('displayName', 'M365 Audit')} - Microsoft 365 Cloud Audit</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    body {{ font-family: 'Inter', sans-serif; }}
  </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen">
  <!-- Top Navigation -->
  <header class="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="h-9 w-9 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20">
          <i class="fa-solid fa-cloud"></i>
        </div>
        <div>
          <h1 class="text-lg font-bold text-white tracking-tight">{tenant_info.get('displayName', 'M365 Tenant')}</h1>
          <p class="text-xs text-slate-400">Tenant: <span class="text-blue-400">{tenant_info.get('primaryDomain', '')}</span> &bull; Automated Audit</p>
        </div>
      </div>
      <div class="flex items-center space-x-3">
        <a href="proposal.html" class="px-3 py-1.5 rounded-lg bg-orange-600 hover:bg-orange-500 text-xs font-bold text-white transition shadow-sm">
          <i class="fa-solid fa-file-contract mr-1.5"></i> Modernization Proposal
        </a>
        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span> Live Graph API Connected
        </span>
        <button onclick="window.print()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 transition">
          <i class="fa-solid fa-print mr-1.5"></i> Export Report
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <!-- Executive KPI Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
      <!-- KPI 1 -->
      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-5 shadow-sm">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium uppercase tracking-wider text-slate-400">Mailbox Storage</span>
          <span class="h-8 w-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
            <i class="fa-solid fa-envelope"></i>
          </span>
        </div>
        <div class="mt-3 flex items-baseline justify-between">
          <div class="text-2xl font-bold text-white">{ex_sum['total_storage_tb']} TB</div>
          <span class="text-xs text-slate-400">{ex_sum['total_storage_gb']:,} GB</span>
        </div>
        <p class="text-xs text-slate-400 mt-2">
          <span class="text-emerald-400 font-medium">{ex_sum['active_mailboxes']}</span> active &bull; 
          <span class="text-amber-400 font-medium">{ex_sum['inactive_mailboxes']}</span> inactive (&gt;30d)
        </p>
      </div>

      <!-- KPI 2 -->
      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-5 shadow-sm">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium uppercase tracking-wider text-slate-400">Quota Risk Mailboxes</span>
          <span class="h-8 w-8 rounded-lg bg-rose-500/10 text-rose-400 flex items-center justify-center">
            <i class="fa-solid fa-triangle-exclamation"></i>
          </span>
        </div>
        <div class="mt-3 flex items-baseline justify-between">
          <div class="text-2xl font-bold {'text-rose-400' if ex_sum['critical_over_100_pct'] > 0 else 'text-white'}">
            {ex_sum['critical_over_100_pct'] + ex_sum['warning_over_80_pct']} Users
          </div>
          <span class="text-xs text-rose-400 font-semibold">{ex_sum['critical_over_100_pct']} Over 100%</span>
        </div>
        <p class="text-xs text-slate-400 mt-2">Require immediate Archiving or Quota expansion</p>
      </div>

      <!-- KPI 3 -->
      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-5 shadow-sm">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium uppercase tracking-wider text-slate-400">SharePoint Storage</span>
          <span class="h-8 w-8 rounded-lg bg-cyan-500/10 text-cyan-400 flex items-center justify-center">
            <i class="fa-solid fa-folder-tree"></i>
          </span>
        </div>
        <div class="mt-3 flex items-baseline justify-between">
          <div class="text-2xl font-bold text-white">{sp_sum['total_storage_tb']} TB</div>
          <span class="text-xs text-slate-400">{sp_sum['total_files']:,} Files</span>
        </div>
        <p class="text-xs text-slate-400 mt-2">
          Across <span class="text-white font-medium">{sp_sum['total_sites']}</span> sites ({sp_sum['active_sites']} active)
        </p>
      </div>

      <!-- KPI 4 -->
      <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-5 shadow-sm">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium uppercase tracking-wider text-slate-400">Est. Storage Savings</span>
          <span class="h-8 w-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
            <i class="fa-solid fa-piggy-bank"></i>
          </span>
        </div>
        <div class="mt-3 flex items-baseline justify-between">
          <div class="text-2xl font-bold text-emerald-400">${sp_sum['est_annual_savings_nzd']:,.0f} NZD</div>
          <span class="text-xs text-slate-400">/ year</span>
        </div>
        <p class="text-xs text-slate-400 mt-2">
          By tiering <span class="text-emerald-400 font-medium">{sp_sum['cold_archive_storage_gb']:,.0f} GB</span> cold archive sites
        </p>
      </div>
    </div>

    <!-- Urgent Action Banner if Over Quota -->
    {'<div class="rounded-xl border border-rose-500/30 bg-rose-950/30 p-4 flex items-start space-x-3"><i class="fa-solid fa-circle-exclamation text-rose-400 text-lg mt-0.5"></i><div><h3 class="text-sm font-semibold text-rose-300">Action Required: Mailbox Quota Limits Reached</h3><p class="text-xs text-rose-200/80 mt-1">Users are currently above or near 100% of their prohibit-send threshold. Incoming and outgoing emails will bounce if not archived.</p></div></div>' if ex_sum['critical_over_100_pct'] > 0 else ''}

    <!-- SECTION 1: Exchange Mailbox Deep Dive -->
    <div class="bg-slate-800/40 border border-slate-800 rounded-2xl overflow-hidden">
      <div class="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-800/60">
        <div>
          <h2 class="text-base font-semibold text-white">Exchange Online Mailbox & Quota Analysis</h2>
          <p class="text-xs text-slate-400">Top storage consumers and quota risk status</p>
        </div>
        <span class="text-xs px-2.5 py-1 rounded bg-slate-700 text-slate-300">Total: {ex_sum['total_mailboxes']} Mailboxes</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-900/50 text-slate-400 border-b border-slate-800 uppercase font-semibold">
            <tr>
              <th class="px-6 py-3">User / Mailbox</th>
              <th class="px-6 py-3">Used Storage</th>
              <th class="px-6 py-3">Quota %</th>
              <th class="px-6 py-3">Archive Enabled</th>
              <th class="px-6 py-3">Last Active</th>
              <th class="px-6 py-3">Recommended Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800 text-slate-300">
"""

    for u in exchange_data["top_mailboxes"]:
        pct = u["pct"]
        if pct >= 100:
            badge = '<span class="px-2 py-0.5 rounded text-2xs font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30">OVER QUOTA</span>'
            rec = '<span class="text-rose-400 font-medium">Enable Online Archive immediately</span>'
        elif pct >= 80:
            badge = '<span class="px-2 py-0.5 rounded text-2xs font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">WARNING</span>'
            rec = '<span class="text-amber-400">Plan Archive migration</span>'
        else:
            badge = '<span class="px-2 py-0.5 rounded text-2xs font-semibold bg-emerald-500/10 text-emerald-400">HEALTHY</span>'
            rec = '<span class="text-slate-400">Normal</span>'

        archive_icon = '<i class="fa-solid fa-check text-emerald-400"></i> Yes' if u['has_archive'] else '<i class="fa-solid fa-xmark text-slate-500"></i> No'

        html += f"""            <tr class="hover:bg-slate-800/30 transition">
              <td class="px-6 py-3.5">
                <div class="font-medium text-white">{u['name']}</div>
                <div class="text-2xs text-slate-400">{u['upn']}</div>
              </td>
              <td class="px-6 py-3.5 font-medium">{u['used_gb']} GB <span class="text-slate-500 text-2xs">/ {u['quota_gb']} GB</span></td>
              <td class="px-6 py-3.5">
                <div class="flex items-center space-x-2">
                  <div class="w-20 bg-slate-700 rounded-full h-1.5 overflow-hidden">
                    <div class="h-full {'bg-rose-500' if pct >= 100 else ('bg-amber-400' if pct >= 80 else 'bg-blue-500')}" style="width: {min(pct, 100)}%"></div>
                  </div>
                  <span class="font-semibold text-2xs">{pct}%</span>
                  {badge}
                </div>
              </td>
              <td class="px-6 py-3.5">{archive_icon}</td>
              <td class="px-6 py-3.5 text-slate-400">{u['last_activity']}</td>
              <td class="px-6 py-3.5">{rec}</td>
            </tr>
"""

    html += f"""          </tbody>
        </table>
      </div>
    </div>

    <!-- SECTION 2: SharePoint Sites & Storage Savings -->
    <div class="bg-slate-800/40 border border-slate-800 rounded-2xl overflow-hidden">
      <div class="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-800/60">
        <div>
          <h2 class="text-base font-semibold text-white">SharePoint Sites Storage & Cold Tier Opportunities</h2>
          <p class="text-xs text-slate-400">Large sites identified for Microsoft 365 Archive / Azure Cold tiering</p>
        </div>
        <span class="text-xs px-2.5 py-1 rounded bg-slate-700 text-slate-300">Total: {sp_sum['total_sites']} Sites ({sp_sum['total_storage_tb']} TB)</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-900/50 text-slate-400 border-b border-slate-800 uppercase font-semibold">
            <tr>
              <th class="px-6 py-3">Site Collection</th>
              <th class="px-6 py-3">Storage Used</th>
              <th class="px-6 py-3">Total Files</th>
              <th class="px-6 py-3">Active Files (30d)</th>
              <th class="px-6 py-3">Stagnant Ratio</th>
              <th class="px-6 py-3">Tiering Recommendation</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800 text-slate-300">
"""

    for s in sharepoint_data["top_sites"]:
        is_candidate = any(c["name"] == s["name"] for c in sharepoint_data["archive_candidates"])
        if is_candidate:
            rec = '<span class="inline-flex items-center text-emerald-400 font-semibold"><i class="fa-solid fa-arrow-down-to-bracket mr-1"></i> M365 Cold Archive Candidate</span>'
        else:
            rec = '<span class="text-slate-400">Standard Active Storage</span>'

        html += f"""            <tr class="hover:bg-slate-800/30 transition">
              <td class="px-6 py-3.5">
                <div class="font-medium text-white">{s['name']}</div>
                <div class="text-2xs text-slate-500">{s['template']}</div>
              </td>
              <td class="px-6 py-3.5 font-bold text-white">{s['used_gb']:,} GB</td>
              <td class="px-6 py-3.5">{s['files']:,}</td>
              <td class="px-6 py-3.5 text-emerald-400 font-medium">{s['active_files']:,}</td>
              <td class="px-6 py-3.5">
                <div class="flex items-center space-x-2">
                  <span class="font-medium text-slate-300">{s['stagnant_pct']}%</span>
                  <div class="w-16 bg-slate-700 rounded-full h-1.5 overflow-hidden">
                    <div class="h-full bg-indigo-500" style="width: {s['stagnant_pct']}%"></div>
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

    <!-- SECTION 3: Executive Action Items & Licensing Roadmap -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-slate-800/40 border border-slate-800 rounded-xl p-5">
        <div class="h-9 w-9 rounded-lg bg-rose-500/10 text-rose-400 flex items-center justify-center font-bold mb-3">
          1
        </div>
        <h3 class="text-sm font-semibold text-white">Resolve Quota Risks</h3>
        <p class="text-xs text-slate-400 mt-2 leading-relaxed">
          Enable Exchange Online Archiving for users nearing or over 100% (Matthew Wade, Brian Phelan, Adam Olson). This provides an additional 1.5 TB of auto-expanding archive capacity.
        </p>
      </div>

      <div class="bg-slate-800/40 border border-slate-800 rounded-xl p-5">
        <div class="h-9 w-9 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center font-bold mb-3">
          2
        </div>
        <h3 class="text-sm font-semibold text-white">Reclaim SharePoint Storage</h3>
        <p class="text-xs text-slate-400 mt-2 leading-relaxed">
          Move stagnant sites like <em>Archive Contracts</em> (530 GB) and <em>Archive Tenders</em> (260 GB) to Microsoft 365 Archive. Saves an estimated ~${sp_sum['est_annual_savings_nzd']:,.0f} NZD annually in overage charges.
        </p>
      </div>

      <div class="bg-slate-800/40 border border-slate-800 rounded-xl p-5">
        <div class="h-9 w-9 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center font-bold mb-3">
          3
        </div>
        <h3 class="text-sm font-semibold text-white">License Optimization</h3>
        <p class="text-xs text-slate-400 mt-2 leading-relaxed">
          Audit the <strong>{ex_sum['inactive_mailboxes']} inactive mailboxes</strong> (&gt;30 days no sign-in). Converting departed staff mailboxes to Shared Mailboxes allows unassigning paid Exchange Online Plan 2 licenses.
        </p>
      </div>
    </div>
  </main>

  <footer class="border-t border-slate-800/80 py-6 text-center text-xs text-slate-500">
    Generated automatically by Circle Connect M365 Automation Engine &bull; {exchange_data['audited_at'][:10]}
  </footer>
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Report generated successfully at: {output_file}")

