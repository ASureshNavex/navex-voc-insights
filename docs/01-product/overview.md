# Product overview

## What the application is

The VoC Insights Workspace is NAVEX's internal view of customer friction by account. It rebuilds the current At-Risk Account Scorecard, which is produced by hand each week, as a stable platform that refreshes on a schedule and alerts account owners when an account's status changes.

For each account in a user's book it shows a Red, Yellow or Green VoC rating, the rule that produced it, the Enterpret themes behind it, and the customer's own words. The rating and its explanation sit together in one view, because the explanation is the core value.

It is where a Customer Experience Manager (CXM) comes to understand an account's friction. It is not where they do their work: that stays in Gainsight and Salesforce.

## Problem it solves

| Today | With the platform |
|---|---|
| One VoC specialist runs the scorecard by hand with AI skills each week | A scheduled ingestion task and the Account Scoring Agent run the same logic as code |
| Output is a static report | A live, filterable view scoped to each user's accounts |
| Owners learn about changes when they read the report | An email alert and a Gainsight CTA when a status changes |
| Access is by sharing a file | Sign-in through NAVEX SSO, scope from the org chart |
| No record of who used it | Usage and audit along the org chart |

## Users

A closed internal audience of about 100 to 150 people, fewer than 10 of them VoC admins.

| Role | Uses it to |
|---|---|
| CXM | See their own accounts' ratings, themes and verbatims; pull an account brief; go back to Gainsight to act |
| CXM leadership | See their team's accounts, the week-over-week share of red and yellow, the manager summary and custom reports |
| VoC admin | Watch refreshes and data sources, manage digests and the knowledge hub, review weekly changes, usage and audit |
| ELT viewer, Sales (AE), Sales leadership | Access levels exist; their modules are still to be decided |

## The expected flow

1. The refresh runs and an account's confirmed status changes, for example Green to Yellow.
2. The owner gets a change-of-status email, and a VoC CTA lands in Gainsight.
3. The link in either opens that account in the workspace, signed in through SSO.
4. The CXM reads the themes and verbatims, pulls a brief if needed, and returns to Gainsight to act.

## Data sources

| Source | Role | Access |
|---|---|---|
| Snowflake | System of record for accounts, ARR, renewal dates, ownership, churn score | Key-pair over PrivateLink, read only |
| Enterpret | Classifies feedback into the taxonomy; provides themes, sentiment and verbatims | MCP API, service account |
| Microsoft Entra ID (Corp AD) | Identity, groups and the org chart | OIDC and Microsoft Graph |
| Gainsight | Hosts the VoC CTA that links into the workspace | Link only in the MVP |

## Phases

| Phase | Dates | Scope |
|---|---|---|
| MVP | 26 October to 8 December 2026 | Scorecard parity, scheduled refresh, alerts, SSO, Gainsight link, admin views, digests, knowledge hub |
| Phase 1 | 9 December 2026 to 15 February 2027 | Product workspace, research agents, knowledge hub files as evidence, Gainsight write-back |
| Phase 2 | 16 February to 30 March 2027 | Fact Base, enterprise views, further integrations |

## MVP definition of done

1. Parity with the current report in content, logic and single-view layout
2. Stable scheduled refresh
3. Change-of-status email alerts
4. SSO-based access
5. Gainsight linkage: a CTA opens the account directly, already signed in

## Rules that shape every decision

- Parity first. Visual polish is welcome; restructuring is not.
- One view. A CXM gets the full picture without moving between pages.
- No net-new features without NAVEX sign-off. Ideas go to NAVEX as proposals.
- No duplicate data entry. Anything that matters downstream is written to Gainsight or Salesforce, in a later phase.
- Access and hierarchy come only from SSO and the org chart.
