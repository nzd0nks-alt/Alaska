# Professional Services Statement of Work & Project Proposal
## Microsoft 365 Cloud Modernization, Storage Optimization & License Rationalization

**Prepared For:**  
**Alaska Construction & Interiors**  
PO Box 90148 Victoria Street West, Auckland 1142  

**Prepared By:**  
**Circle IT Limited**  
Lead Architect: Michael Blackman  
Date: October 2026  
Status: Executive Proposal  

---

## Executive Summary

Following Circle IT's comprehensive live cloud estate audit of Alaska Construction & Interiors' Microsoft 365 tenant (`alaska.co.nz`), three high-impact operational inefficiencies and business risks were identified:

1. **SharePoint Storage Overage & Inactive Data**: Over **4.48 TB** across 29 sites. Over **790 GB** consists of completely stagnant legacy tenders and contract archives (*Archive Contracts* and *Archive Tenders*), driving unnecessary Microsoft monthly storage overage costs.
2. **Exchange Mailbox Quotas & Unmanaged Departed Users**: **2.95 TB** of mailbox storage across 149 mailboxes. **Key project leads are currently at or over 100% capacity** (actively at risk of email delivery failure), while **43 inactive mailboxes** (>30 days no activity) remain assigned to expensive paid licenses.
3. **Project Management Tool Redundancy**: Project leads and estimators are currently assigned high-cost **Project Plan 3** licenses without utilizing scheduling engines, while modern lightweight **Microsoft Planner & Teams** workflows remain under-deployed.

To resolve these risks and realize substantial recurring operational savings, Circle IT proposes **three standalone, fixed-scope migration and implementation projects**.

---

## Commercial Overview

Each project is scoped on a predictable, fixed-scope professional services basis at Circle IT’s senior consulting rate of **$175.00 NZD / hour (excl. GST)**, targeting **~$10,000 NZD** in high-value delivery per phase.

| Project Code | Project Title | Estimated Hours | Billing Rate | Fixed Investment (NZD) | Projected Annual Client Savings |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **PRJ-01** | **SharePoint Estate Rationalization & Cold Storage Migration** | 56 hrs | $175 / hr | **$9,800** | **~$13,139 / yr** *(Storage overages)* |
| **PRJ-02** | **Exchange Online Quota Remediation & Inactive License Recovery** | 56 hrs | $175 / hr | **$9,800** | **~$2,400 / yr** *(+ zero email outage)* |
| **PRJ-03** | **Project & Planner Modernization & License Rationalization** | 58 hrs | $175 / hr | **$10,150** | **~$5,814 / yr** *(Software right-sizing)* |
| **TOTAL** | **Full Estate Modernization Program (Bundled)** | **170 hrs** | **$175 / hr** | **$29,750** | **~$21,353 / yr recurring** |

> [!TIP]
> **Return on Investment (ROI):** The recurring licensing and cloud storage savings of **~$21,350 NZD per year** means the entire modernization program pays for itself in under 17 months, while permanently eliminating operational risk, data compliance exposure, and storage bottlenecks.

---

## Detailed Project Scopes & Work Breakdown Structure (WBS)

```
                       PROJECT ROADMAP (170 Hours Total)
 ┌───────────────────────────┐     ┌───────────────────────────┐     ┌───────────────────────────┐
 │   PROJECT 1: SHAREPOINT   │     │    PROJECT 2: EXCHANGE    │     │    PROJECT 3: PLANNER     │
 │  56 Hours • $9,800 NZD    │ ──> │   56 Hours • $9,800 NZD   │ ──> │  58 Hours • $10,150 NZD   │
 │ • Cold Archiving (790GB)  │     │ • Quota Emergency Fix     │     │ • Project Plan 3 Audit    │
 │ • Version Trim & Policies │     │ • Auto-Expanding Archive  │     │ • Planner Boards & Teams  │
 │ • $13.1k/yr Cost Savings  │     │ • 43 Inactive User Reclaim│     │ • $5.8k/yr License Rights │
 └───────────────────────────┘     └───────────────────────────┘     └───────────────────────────┘
```

---

### Project 1: SharePoint Estate Rationalization & Cold Storage Migration (PRJ-01)
**Scope:** 56 Hours | **Investment:** $9,800 NZD + GST | **Target Timeline:** 3 Weeks  
**Primary Objective:** Eliminate Microsoft tenant storage overage penalties by tiering 790+ GB of cold archives and establishing automated lifecycle policies.

#### Detailed WBS & Deliverables:
1. **Phase 1: Discovery & Data Inventory (10 hrs)**
   - Audit site collections (*Tenders*, *Contracts*, *Archive Tenders*, *Archive Contracts*).
   - Classify 2.11M files by last modified date, access patterns, and statutory construction retention periods (NZ Building Act / tax compliance).
   - Validate version history bloat across high-churn sites.

2. **Phase 2: Microsoft 365 Cold Archive & Azure Tiering Setup (16 hrs)**
   - Configure Microsoft 365 Archive / Azure Cold Blob Storage targets.
   - Establish secure retention, immutability, and search index policies to ensure archived tender files remain searchable and retrievable on demand.
   - Perform test migration of 50 GB to validate file hashes, metadata preservation, and retrieval latency.

3. **Phase 3: Production Archival Migration & Cutover (20 hrs)**
   - Execute staged migration of *Archive Contracts* (530 GB) and *Archive Tenders* (260 GB).
   - Implement storage versioning caps (reducing uncontrolled 500-version histories down to 50 versions across active project libraries).
   - Re-index and confirm permissions inheritance across Alaska project groups.

4. **Phase 4: Verification, Handover & Governance (10 hrs)**
   - Re-calculate live tenant storage footprint and confirm reduction below baseline overage threshold.
   - Deliver Alaska SharePoint Data Management & Archiving SOP for project managers.
   - Post-implementation monitoring and operational sign-off.

---

### Project 2: Exchange Online Quota Remediation & Inactive License Recovery (PRJ-02)
**Scope:** 56 Hours | **Investment:** $9,800 NZD + GST | **Target Timeline:** 3 Weeks  
**Primary Objective:** Prevent imminent email bounces for key personnel, implement 1.5 TB Auto-Expanding Archiving, and recover 43 unmanaged inactive licenses.

#### Detailed WBS & Deliverables:
1. **Phase 1: Emergency Quota Remediation & Retention Policies (12 hrs)**
   - Immediate intervention for accounts exceeding 90-100% quota (*Matthew Wade 101.6%*, *Brian Phelan 97.9%*, *Adam Olson 89.6%*, *James Ormond 88.8%*, *Accounts 87.1%*).
   - Apply retention and auto-archive policies to migrate emails older than 1-2 years into secondary cloud archive mailboxes without PST file corruption.

2. **Phase 2: Auto-Expanding Archive Rollout & Provisioning (14 hrs)**
   - Enable Microsoft Exchange Online Auto-Expanding Archiving across all commercial and structural project leads (expanding capacity from 50/100 GB up to 1.5 TB per user).
   - Validate Outlook client indexing (Mac, Windows, and Web) for seamless search performance across archived tender communications.

3. **Phase 3: Inactive User Audit & Shared Mailbox Conversion (18 hrs)**
   - Cross-reference the 43 identified inactive mailboxes (>30 days no sign-in) with Alaska's HR / Employee Directory.
   - Convert departed employee mailboxes to free Shared Mailboxes (preserving mailbox data, discovery capability, and forwarding rules indefinitely without a paid license).
   - Deprovision and reclaim paid Exchange Online Plan 2 licenses.

4. **Phase 4: Automation & Admin Controls (12 hrs)**
   - Deploy automated PowerShell / Graph API monthly quota and inactivity monitoring alerts.
   - Provide Alaska IT admin team with user onboarding / offboarding standard operating procedure.
   - Final audit report validating zero quota risks and updated license allocation.

---

### Project 3: Project & Planner Modernization & License Rationalization (PRJ-03)
**Scope:** 58 Hours | **Investment:** $10,150 NZD + GST | **Target Timeline:** 4 Weeks  
**Primary Objective:** Modernize project planning, migrate non-specialist users off expensive Project Plan 3 subscriptions, and standardize project boards in Microsoft Planner & Teams.

#### Detailed WBS & Deliverables:
1. **Phase 1: Project Management Workflow Assessment (12 hrs)**
   - Interview key leads (Lorenzo Larghi, Robert Stretton, Chris Robertson) to audit actual usage of Microsoft Project desktop client vs task boards.
   - Identify dedicated scheduling engineers requiring full Gantt/CPM tools versus project coordinators requiring agile kanban boards.

2. **Phase 2: Standardized Planner & Teams Architecture (16 hrs)**
   - Design standardized project template boards in Microsoft Planner for Alaska's projects (e.g. *BNZ Ponsonby*, *Commercial Fitouts*).
   - Configure buckets (Tender, Procurement, Subcontractor Management, Site Safety, Handover/Defects).
   - Integrate Planner boards directly into Microsoft Teams project channels.

3. **Phase 3: License Right-Sizing & Subscription Migration (18 hrs)**
   - Downgrade non-power users from **Planner and Project Plan 3** ($80+/user/month) to standard included M365 Planner licenses, saving ~$5,814 annually.
   - Migrate existing Project schedules and task lists into Microsoft Planner boards.
   - Set up automated milestone alerts and Power Automate notifications.

4. **Phase 4: Staff Training, Handover & Documentation (12 hrs)**
   - Conduct 2 interactive training workshops for project managers and site coordinators.
   - Supply quick-reference training guides for task assignment, timeline tracking, and mobile updates on site.
   - Post-launch check-in and formal project closeout.

---

## Program Delivery Schedule

```
Timeline: 8 - 10 Weeks Total (Phased Delivery)
┌──────────────────────────────────────┬───┬───┬───┬───┬───┬───┬───┬───┐
│ Workstream                           │W1 │W2 │W3 │W4 │W5 │W6 │W7 │W8 │
├──────────────────────────────────────┼───┼───┼───┼───┼───┼───┼───┼───┤
│ PRJ-01: SharePoint Storage Archiving │███│███│███│   │   │   │   │   │
│ PRJ-02: Exchange Quota & Inactive    │   │███│███│███│   │   │   │   │
│ PRJ-03: Planner Modernization & SOP  │   │   │   │███│███│███│███│   │
│ Program Review & Final Handover      │   │   │   │   │   │   │   │███│
└──────────────────────────────────────┴───┴───┴───┴───┴───┴───┴───┴───┘
```

---

## Terms & Engagement Agreement

1. **Billing & Invoicing**:
   - Each project is invoiced in two milestone installments:
     - 50% upon project kickoff and agreement.
     - 50% upon delivery, testing sign-off, and handover.
2. **Consulting Rate**: Additional out-of-scope advisory or custom development billed at standard senior consulting rate of $175 NZD / hr.
3. **Client Prerequisites**: Administrative consent for Circle IT cloud management tooling (already established under application `Alaska-Automation-Tool`).

---

### Approval & Sign-Off

To approve this proposal, please sign below or confirm via email indicating preferred project phases:

**For Alaska Construction & Interiors:**  
Signature: ____________________________________  
Name: ________________________________________  
Title: _________________________________________  
Date: _________________________________________  

**For Circle IT Limited:**  
Signature: ____________________________________  
Name: Michael Blackman  
Title: Principal Consultant & Architect  
Date: 30 October 2026  
