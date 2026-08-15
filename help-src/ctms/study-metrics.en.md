---
title: Milestone Tracking & Enrollment Metrics
description: Learn Study Management's Milestone Tracking and Enrollment Metrics: from Plan Study generation to scheduling and completion, metric seeding, and Metrics Over Time gates.
last_updated: 2026-08-15
related:
  - study-lifecycle
  - dashboards
  - site-lifecycle
---

## Milestone Tracking

**Study Management → Milestone Tracking** lists all study milestones (the Milestone object, shared with eTMF); study managers track key study nodes here:

| Column | Meaning |
|--------|---------|
| **Milestone** | Milestone name (from template) |
| **Study / Study Country / Study Site** | Owning level |
| **Milestone Type** | e.g. `First Subject In (FSI)`, `Database Lock` |
| **Baseline / Planned / Actual Finish Date** | Baseline, planned, and actual finish dates |
| **% Complete / Completeness** | Completeness (auto-computed, icon) |
| **Completed EDL Item Records** | Count of completed expected-document entries |

Milestones are generated automatically by **Plan Study** from the master set (initial state **Unplanned**); countries/sites get their own milestones when entering Initiating. To schedule and complete:

1. **Plan Milestone**: set **Planned Finish Date**; downstream dependency dates follow; state → **Planned**.
2. **Mark Complete**: set **Actual Finish Date**; state → **Complete**.

> The dependency gate is enforced server-side: **Mark Complete** on a downstream milestone is rejected while the upstream is incomplete, unless a **Gating Override Date** is set.

Completeness is computed from "previous milestones complete + required tasks complete + expected documents collected and approved"; use **View Expected Documents** to see linked EDL Items. See [Milestones](../etmf/milestones.html) for the full state flow.

## Enrollment Metrics

**Study Management → Enrollment Metrics** maintains enrollment metrics per level (the Metric object). When a study enters Planning/Active — or a country/site enters Initiating — the system **seeds one record per metric** (initial value 0), in three level-based types:

| Type | Level |
|------|-------|
| **Study Metric** | Study |
| **Study Country Metric** | Study Country |
| **Study Site Metric** (default) | Study Site |

**Metric Type** has 11 values: Total In Screening, Total Screened, Total Screen Failed, Total Enrolled, Total Withdrawn, Total Completed, Enrollment Rate (subjects per month), Screen Failure Rate (%), Drop Out Rate (%), Total Randomized, Total End of Treatment.

Maintenance is **manual**: fill **Planned**, **Forecast**, and **Actual**; **Planned Roll Up** aggregates children's Planned automatically.

> The study's **Metrics Not In Use** setting trims which metric types get seeded and removes them from the homepages.

### Metrics Over Time

Run the object workflow from study/country/site detail pages (**All Actions**, e.g. Create Metrics Over Time) to generate per-period planned/actual/forecast records at the **Recruitment Planning Frequency** (default monthly). Gates:

- The study's **Metric Calculation** is Date-Based;
- The paired recruitment First/Last milestones have end dates (Last ≥ First);
- The metric's **Planned > 0**.

The generated trend overlays the **Study Management Homepage** Enrollment Status chart (Study/Country levels only; site enrollment is tracked in the subject list).

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| Milestone Tracking is empty | Run **Plan Study** and advance to Planning; countries/sites must enter Initiating |
| Metrics Over Time fails | Check the three gates: Date-Based, First/Last milestone dates, Planned > 0 |
| Enrollment Status chart is empty | The chart shows Study/Country levels only; confirm enrollment_status and metrics_over_time data exist |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Milestone: Read, Edit | Viewing and scheduling milestones |
| Lifecycle actions | Milestone: **Plan Milestone**, **Mark Complete** | Scheduling and completion |
| Object | Metric: Create, Read, Edit | Maintaining Planned / Forecast / Actual |
| Object action | Metric: **Create Metrics Over Time** (study/country/site) | Generating period trend data |

**CTMS Study Manager**, **CRA**, and **Central Monitor** maintain metrics and milestones; **CTMS Business/System Administrators** additionally hold delete and workflow execution rights.
