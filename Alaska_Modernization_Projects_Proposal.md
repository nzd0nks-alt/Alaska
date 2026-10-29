# Professional Services Statement of Work & Project Proposal
## Microsoft 365 Cloud Modernization, Storage Optimization & Governance

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

Following Circle IT's comprehensive live cloud estate audit of Alaska Construction & Interiors' Microsoft 365 tenant (`alaska.co.nz`), three distinct operational profiles were identified:

1. **SharePoint Storage Overage & Archival Inefficiencies (Primary Critical Priority)**:  
   Alaska currently stores **4.48 TB** across 29 site collections comprising over **2.11 million files**. Of this, **over 790 GB** consists of completely stagnant legacy project archives (*Archive Contracts* at 530 GB and *Archive Tenders* at 260 GB) that have seen fewer than 20 files accessed in the last 30 days. Microsoft charges standard high-performance active storage rates for this data, driving substantial recurring monthly overage penalties.
2. **Exchange Mailbox Quotas & Unmanaged Departed Users**:  
   **2.95 TB** across 149 mailboxes, with several commercial leads at or exceeding 100% quota capacity, alongside 43 unmanaged inactive mailboxes holding paid licenses.
3. **Project & Scheduling Software Right-Sizing**:  
   Multiple project leads are currently provisioned with high-tier **Project Plan 3** subscriptions ($80+/user/month) but require collaborative task and milestone boards rather than enterprise Gantt scheduling engines.

### Recommended Implementation Strategy

Because **Project 1 (SharePoint Estate Rationalization & Cold Storage Migration)** addresses Alaska's largest immediate financial leakage—delivering **~$13,139 NZD / year** in direct recurring storage savings—it serves as the flagship modernization initiative with a rapid **12-month payback period**.

Each project is scoped on a **predictable, fixed-investment professional services basis**, delivering comprehensive engineering, compliance preservation, and operational handover.

---

## Commercial Summary & Investment Schedule

| Project Code | Project Title | Project Type | Fixed Investment (NZD) | Projected Client Annual Savings | Payback Period / ROI |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **PRJ-01** | **SharePoint Estate Rationalization & Cold Storage Migration**<br>• Comprehensive archival of 790+ GB dormant tenders & contracts<br>• Version sprawl remediation across 2.11M files<br>• NZ Building Act compliance & continuous lifecycle automation | **Flagship Priority** | **$14,850** | **~$13,139 / yr** *(Recurring storage overages)* | **~13.5 Months** *(Self-funding)* |
| **PRJ-02** | **Exchange Online Quota Remediation & Inactive License Recovery**<br>• Emergency quota expansion & 1.5 TB Auto-Expanding Archives<br>• Reclaim 43 inactive departed employee licenses | Operational Defense | **$7,850** | **~$2,400 / yr** *(License recovery)* | Risk Mitigation & Outage Defense |
| **PRJ-03** | **Project & Planner Modernization & Software License Rationalization**<br>• Transition non-schedulers off Project Plan 3 ($80/mo)<br>• Build standardized Teams Planner project boards & SOP | Software Right-Sizing | **$9,800** | **~$5,814 / yr** *(Subscription reduction)* | ~20 Months |

> [!IMPORTANT]
> **Value Proposition:** PRJ-01 can be executed as an independent standalone project. By eliminating ~$13,139 NZD per year in recurring cloud storage surcharges, Alaska permanently cleans up its data footprint, maintains full regulatory compliance, and recovers the entire project investment within the first year.

---

## Flagship Project Scope: SharePoint Estate Rationalization & Cold Storage Migration (PRJ-01)

### Executive Overview
- **Project Classification:** Enterprise Storage Optimization, Archival Migration & Data Governance
- **Commercial Structure:** Fixed-Fee Professional Services Engagement (**$14,850 NZD + GST**)
- **Data Footprint:** 4.48 TB | 29 Site Collections | 2,113,819 Files
- **Primary Financial Objective:** Permanently eliminate tenant storage overage penalties, capturing **~$13,139 NZD / year** in recurring cost avoidance.
- **Primary Operational Objective:** Transition 790+ GB of cold archives into compliant, searchable low-cost storage tiers while optimizing active document libraries with zero downtime for live project teams.

---

### Detailed Work Breakdown Structure (WBS)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                 PRJ-01: 6-PHASE SHAREPOINT STORAGE MIGRATION & GOVERNANCE                   │
├──────────────────┬──────────────────┬──────────────────┬──────────────────┬─────────────────┤
│ PHASE 1          │ PHASE 2          │ PHASE 3          │ PHASE 4          │ PHASE 5 & 6     │
│ Inventory & NZ   │ Cold Target &    │ Version Cleanup  │ Pilot Migration  │ Production      │
│ Building Act     │ Metadata Index   │ & Quota Quick    │ & Cryptographic  │ Cutover, SOPs   │
│ Compliance Audit │ Architecture     │ Wins             │ Hash Checks      │ & Automation    │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┴─────────────────┘
```

#### Phase 1: Estate Inventory, Version Audit & Statutory Compliance Classification
- **Deep Telemetry Scan:** Detailed cataloging of all 29 site collections, identifying storage consumption, file counts, and access recency across active vs dormant repositories.
- **Version Sprawl Analysis:** Audit multi-gigabyte version history bloat across frequently edited drawing sets, specifications, and large PDF tender documentation (many active files currently retain up to 500 unmanaged revision iterations).
- **Statutory Construction Retention Mapping:**
  - Classify historical project documents against the **New Zealand Building Act 2004** (10-year statutory liability period for building defects and structural records).
  - Verify producer statements (PS1, PS2, PS3, PS4), code compliance certificates (CCC), and as-built drawings are earmarked for immutable archival.
  - Align accounting and contract records with Inland Revenue Department (IRD) 7-year statutory retention obligations.
- **Boundary Delineation:** Isolate active project sites (*Tenders*, *Contracts*, *BNZ Ponsonby*) from dormant target repositories (*Archive Contracts* 530 GB, *Archive Tenders* 260 GB, and closed fitout projects).

#### Phase 2: Archival Target Architecture & Security Design
- **Tiering Target Design:** Architect the target storage topology utilizing **Microsoft 365 Cold Archive** and **Azure Cold/Cool Blob Storage** tiers, reducing per-gigabyte costs by over 75%.
- **Metadata & Search Index Preservation:**
  - Ensure that all migrated files retain native SharePoint metadata: original timestamps, Author/Created By attributes, custom project codes, and taxonomy tags.
  - Configure Microsoft Purview indexing so that cold-archived tender documents remain searchable via Microsoft Search and eDiscovery without requiring data to be re-hydrated to the expensive active tier.
- **Access Control & Permissions Modeling:** Replicate existing Alaska permission structures (Owners, Members, Visitors) across the archive targets to ensure strict confidential access controls remain enforced.

#### Phase 3: Automated Version Cleanup & Immediate Storage Reclamation
- **Version History Rationalization:** Configure automated version trimming policies across high-churn document libraries, reducing version caps from 500 down to a controlled 50-version threshold.
- **Orphaned Draft & Duplicate Purge:** Identify and remove temporary upload fragments, orphaned CAD lock files, and duplicate staging containers across active project libraries.
- **Baseline Space Recovery:** Execute the first-wave version purge to immediately halt ongoing tenant storage overage accumulation before moving bulk data.

#### Phase 4: Pilot Migration & Cryptographic Hash Validation
- **Representative Pilot Run:** Execute a controlled 50 GB migration batch encompassing all representative construction file types (`.dwg`, `.rvt`, `.pdf`, `.xlsx`, `.docx`, `.msg`, and large high-resolution site photography packages).
- **Integrity & Checksum Verification:** Validate 100% bit-level data integrity using SHA-256 cryptographic hash comparisons before and after transfer.
- **Re-hydration & Retrieval Testing:** Test on-demand retrieval latency with Alaska commercial staff to ensure archived files can be seamlessly reviewed if an old project requires reference.

#### Phase 5: Production Archival Migration & Staged Cutover
- **Bulk Migration Execution:** Conduct phased, throttled migration of the primary dormant archives:
  - *Archive Contracts* (530 GB / 537,350 files)
  - *Archive Tenders* (260 GB / 239,341 files)
  - Inactive historical fitout and commercial projects
- **Zero Business Interruption:** Execute data transfers during off-peak windows with bandwidth throttling to guarantee zero impact on live active tendering and site operations.
- **Navigation Redirection:** Establish clean, intuitive read-only shortcut links in SharePoint navigation so staff can easily navigate to historical records without confusion.

#### Phase 6: Continuous Lifecycle Automation, SOPs & Administrative Handover
- **Automated Archiving Lifecycle Rules:** Deploy automated Microsoft Graph / Power Automate triggers that prompt project managers upon project completion and automatically schedule closed jobs for cold archival after 12 months.
- **Alaska Project Data Management SOP:** Deliver a clear, concise Standard Operating Procedure for project managers and estimators detailing file naming, versioning hygiene, and archival workflows.
- **Executive Audit Validation:** Run a comprehensive post-implementation Graph API audit validating that Alaska's storage footprint has dropped below baseline overage thresholds, cementing the **~$13,139 NZD / year** in ongoing operational savings.

---

## Secondary Scopes Overview

### Project 2: Exchange Online Quota Remediation & Inactive License Recovery (PRJ-02)
- **Classification:** Operational Continuity & Licensing Optimization
- **Commercial Structure:** Fixed-Fee Professional Services Engagement (**$7,850 NZD + GST**)
- **Key Objectives:**
  - Emergency remediation for commercial leads currently at 95–101% mailbox quota capacity (Matthew Wade, Brian Phelan, Adam Olson) to prevent imminent email bounce and communication failure.
  - Enable 1.5 TB Auto-Expanding Cloud Archiving across all commercial and structural project managers.
  - Cross-reference the 43 inactive mailboxes with Alaska's employee directory, converting departed staff accounts to free Shared Mailboxes and deprovisioning paid Exchange Online Plan 2 subscriptions (~$2,400 NZD/yr savings).

### Project 3: Project & Planner Modernization & License Rationalization (PRJ-03)
- **Classification:** Software Right-Sizing & Workflow Standardization
- **Commercial Structure:** Fixed-Fee Professional Services Engagement (**$9,800 NZD + GST**)
- **Key Objectives:**
  - Audit actual scheduling needs across project leads (Lorenzo Larghi, Robert Stretton) and transition non-power users from expensive *Project Plan 3* ($80+/mo) to standard Microsoft Planner.
  - Save **~$5,814 NZD / year** in direct Microsoft licensing costs.
  - Standardize Alaska project boards across Teams (Procurement, Subcontractors, Health & Safety, Handover) with automated milestone notifications.

---

## Implementation Schedule & Milestone Phasing

```
┌──────────────────────────────────────┬───┬───┬───┬───┬───┬───┬───┬───┐
│ Workstream                           │W1 │W2 │W3 │W4 │W5 │W6 │W7 │W8 │
├──────────────────────────────────────┼───┼───┼───┼───┼───┼───┼───┼───┤
│ PRJ-01: Phase 1 (Inventory & Audit)  │███│   │   │   │   │   │   │   │
│ PRJ-01: Phase 2 (Archival Design)    │   │███│   │   │   │   │   │   │
│ PRJ-01: Phase 3 & 4 (Cleanup & Pilot)│   │   │███│   │   │   │   │   │
│ PRJ-01: Phase 5 (Bulk Migration)     │   │   │   │███│███│   │   │   │
│ PRJ-01: Phase 6 (SOP & Automation)   │   │   │   │   │   │███│   │   │
│ PRJ-02: Exchange Remediation (Opt.)  │   │   │   │   │   │   │███│   │
│ PRJ-03: Planner Rollout (Optional)   │   │   │   │   │   │   │   │███│
└──────────────────────────────────────┴───┴───┴───┴───┴───┴───┴───┴───┘
```

---

## Engagement Terms & Milestone Billing

1. **Fixed-Price Guarantee:** All professional services for approved scopes are delivered on a fixed-fee basis. There are no variable hourly overruns for the defined deliverables.
2. **Milestone Invoicing**:
   - 50% upon project authorization and kickoff.
   - 50% upon completion, integrity verification, and operational sign-off.
3. **Infrastructure Prerequisites:** All tenant administrative consent and Graph API automation tooling are already operational under Circle IT application `Alaska-Automation-Tool`.

---

### Authorization & Sign-Off

To approve **Project 1 (SharePoint Estate Rationalization)** or additional scopes, please sign below or confirm via email:

**For Alaska Construction & Interiors:**  
Signature: ____________________________________  
Name: ________________________________________  
Title: _________________________________________  
Date: _________________________________________  

**For Circle IT Limited:**  
Signature: ____________________________________  
Name: Michael Blackman  
Title: Principal Consultant & Lead Cloud Architect  
Date: 30 October 2026  
