> NAVEX consolidated feedback on the first mock-up, 13 November 2026, from the VoC subject matter experts and the project lead. Source document; do not edit.

Thank you for turning the mock-up around so quickly. As discussed, I walked through it with Anirudh Mukhopadhaya (CSO and project lead) and then debriefed with Angie Funk, my fellow VoC SME. Below is our consolidated feedback, the user workflow we expect, and our open questions for your team.
 
Level set: the MVP is the current At-Risk Account Scorecard rebuilt as a stable, regularly refreshed platform with alerts. It is not a redesign. I do appreciate and we recognize several of the additions are good ideas, and we'd like to hold them for a later phase that Anirudh, Angie and I will define together.
 
Overall direction
Parity first. The MVP should match the content, logic and single-view layout of the current scorecard. Visual polish is welcome; restructuring is not.
One view. Please merge the dashboard, account list, themes and verbatim back into a single view. Adoption depends on a CXM getting the full picture without clicking through several pages.
Explainability of the why is the core value. Verbatim and Enterpret themes need to sit right next to the color rating, as they do today.
No net-new features without our sign-off. Please bring ideas to us as proposals and we'll decide what goes in and when.
MVP is done when we have parity with the current report, stable daily refresh, change-of-status email alerts, SSO-based access, and the Gainsight linkage described below.
Landing dashboard
Keep the count of Red and Yellow accounts and the impacted ARR.
Split impacted ARR into Red ARR and Yellow ARR.
Replace "What's new this week" with two figures: New Red this week and New Yellow this week.
Remove the "Next renewal date" tile. In aggregate it only reflects the soonest renewal and doesn't drive action.
Remove "Meetings in 20 days." This wasn't requested and hasn't been validated with us.
Replace the "Trend, last 9 weeks" line. It doesn't carry an insight as built. Instead, show total ARR with the percentage in Red and in Yellow as a week-over-week clustered bar, by both account volume and ARR value. This view matters most for CXM leadership.
Please do a full copy and grammar pass; there are several errors on this page.
Accounts table and filters
Keep the Red / Yellow / Green filter.
Remove the "High ARR only" filter. It would need a definition per segment, and sorting by ARR already puts the largest accounts on top.
Show multiple Enterpret theme chips per account, as the current report does. The mock-up shows one theme per account; Summit Energy, for example, would need both permissions and slow export to display.
Pull themes directly from the Enterpret taxonomy, with no custom layer on top.
Bring verbatim back into the main table view rather than a separate page.
Renewal: keep a single next-renewal date per account (see the workflow section for why it matters). Drop the Renewal quarter column. If a renewal-window filter is useful, build it as a rule-based filter that doesn't take a column.
Product placement at the account level is fine as shown.
Add an Excel download of the filtered table.
Account detail
The verbatim and theme content in the expanded account view belongs on the main view as well; the detail view can carry the fuller set.
The supporting feedback list is too long as shown. Please trim it to the records that drive the theme analysis.
CXM commentary: please remove for MVP. CXMs already log this in Salesforce and Gainsight, and we won't add a third place to enter it. The only version we'd consider is one that writes straight back to Gainsight on save.
The account brief can stay as is.
Roles, access and permissions
All access and hierarchy come from SSO and the org chart. No manual user management (deactivate, role edits) in the admin area.
A CXM sees only their own accounts. The Team and CXM filters should not appear for the CXM role; keep them for CXM leadership and admin.
The three roles shown (CXM user, CXM leadership, admin) are too narrow for an enterprise capability. At minimum we expect an all-access viewer level for ELT, and Sales access (AEs and their leadership) based on account ownership, the same way CXM access works. We'll confirm the full set of levels, including access for functions such as Product.
Usage and audit: we like this. Please make it reportable along the org chart: individual, team, segment and region. Remove panels that don't speak to engagement, such as Resolved product issues.
User workflow expectations
This platform is where CXMs come to understand an account's VoC friction, not where they do their work. Their work stays in Gainsight and Salesforce, and the design should follow from that.
The expected MVP flow:
The model refreshes and an account changes status (Green to Yellow, or Yellow to Red).
The owner gets a change-of-status email alert, and a VoC CTA lands in Gainsight (Angie is building the CTAs).
Clicking the account from the alert or the CTA opens that account directly in the platform, already signed in through SSO.
The CXM reviews the why (themes and verbatim), pulls an account brief if needed, and goes back to Gainsight to act.
What that means for the build:
Ideal state: No separate login or bookmark. If CXMs have to remember a URL, they won't go. A link or entry point on the Gainsight home page would help it feel native.
Every alert and digest says plainly whether action is needed or it's FYI. Otherwise it gets filtered out with everything else in their inbox.
Anything a user does here that matters downstream writes back to Gainsight or Salesforce. No duplicate data entry.
Email digests are fine to include. Set them up at the admin level with a few prebuilt options (for example, a weekly leadership digest), plus light personal configuration for CXMs.
Keep a single next-renewal date on each account. Renewal workflows start at T-180, and VoC risk inside that window will need to route into the renewal workflow later.
Churn score: please display the churn score alongside current VoC sentiment, clearly labeled as two distinct measures, each with an (i) tooltip explaining what it is and what a CXM should do with it. We can work to get the definitions when we meet again.
Of note for your architecture, though not in MVP scope: we expect later phases to add a simple action (a checkbox any CXM, leader or admin can set) that creates a CTA or issue in Gainsight or Salesforce with the account details attached. That logic will need to check whether the CXM is already mitigating the risk, route renewals inside T-180 into the renewal workflow, and draw on more signals than a red Enterpret rating alone. We may also feed the Enterpret Red / Yellow / Green summary into the TechTorch T-180 renewal brief. Please keep the data model open to these connections.
Added features: keep, hold or remove
For the features the mock-up adds beyond the current report:
Feature
	
Decision
	
Note


Meetings in 20 days
	
Remove
	
Not requested or validated


Next renewal date tile
	
Remove
	
Keep the date on each account instead


High ARR only filter
	
Remove
	
Sort by ARR covers it


Renewal quarter column
	
Remove
	
Filter rule only, if needed


Knowledge hub
	
Remove from MVP from CXM view
	
As previously requested


CXM commentary
	
Remove from MVP
	
We likely won't retain given we dont expect CXMs to work here


Manual user management
	
Remove
	
SSO handles it


Saved views
	
Keep
	
Nice to have


Scheduled digests
	
Keep
	
Admin-level, prebuilt options


Refresh three times daily
	
Keep, pending cost answer
	
See open questions


Usage and audit
	
Keep
	
Roll up by org chart


Account brief
	
Keep
	
As is