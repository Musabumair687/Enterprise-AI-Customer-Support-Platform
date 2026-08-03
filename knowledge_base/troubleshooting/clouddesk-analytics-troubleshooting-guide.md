# CloudDesk Analytics
## Troubleshooting Guide

*Corvex Cloud — CloudDesk Analytics*
*This guide documents known issues, their causes, and their resolutions for CloudDesk Analytics. It is intended for administrators, team leads, and technical staff diagnosing problems with the platform. For general usage instructions, refer to the CloudDesk Analytics User Manual. For configuration guidance, refer to the CloudDesk Analytics Administrator Guide.*

---

## How to Use This Guide

Issues are grouped by category. Each entry includes the symptoms you may observe, the most common underlying cause, a recommended solution, steps to prevent recurrence, and related issues you may want to review if the listed solution does not fully resolve your problem.

---

## Section 1: Real-Time Dashboard

### CDA-1001 — Real-Time Dashboard Not Updating

**Symptoms:** The real-time queue dashboard shows a static snapshot that does not reflect new tickets or chats arriving in CloudDesk Tickets or CloudDesk Chat.

**Cause:** The browser tab lost its real-time connection, often due to an extended period of inactivity or a network interruption that was not automatically re-established.

**Solution:** Refresh the page to reestablish the real-time connection. If this occurs frequently, review network stability, particularly if working across a corporate proxy that may be terminating long-lived connections.

**Prevention:** Avoid leaving the dashboard open and idle for extended periods without periodic interaction; consider a periodic auto-refresh if your browser or network conditions make disconnection common.

**Related Issues:** CDA-1002, CDA-11001

---

### CDA-1002 — Real-Time Dashboard Showing a Different Count Than the Ticket Queue

**Symptoms:** The number of open tickets or active chats shown on the real-time dashboard does not match a manual count in CloudDesk Tickets or CloudDesk Chat.

**Cause:** A brief synchronization delay between the real-time aggregation layer and the underlying case data layer, typically resolving within seconds to a couple of minutes.

**Solution:** Refresh the dashboard; if the discrepancy persists beyond several minutes, contact Corvex support, as this may indicate a service degradation.

**Prevention:** No specific preventive action is available for this transient synchronization behavior.

**Related Issues:** CDA-1001

---

### CDA-1003 — Agent Availability Status Displaying Incorrectly on Team Dashboard

**Symptoms:** The team-wide real-time dashboard shows an agent as Available when they have actually set their status to Away.

**Cause:** The agent has more than one active session (for example, a desktop browser tab and a CloudDesk Mobile session) with conflicting status values, and the dashboard is displaying a stale value from one of them.

**Solution:** Ask the agent to confirm status consistency across all active sessions, and close any unused sessions to eliminate the conflict.

**Prevention:** Encourage agents to work from a single active session at a time where practical, to avoid state synchronization conflicts across the platform.

**Related Issues:** none

---

### CDA-1004 — Real-Time Dashboard Slow to Load with High Ticket Volume

**Symptoms:** The real-time dashboard takes noticeably longer to load or render for accounts with a very large active ticket and chat volume.

**Cause:** The dashboard is attempting to aggregate and render a very large real-time data set without narrowing filters applied.

**Solution:** Apply team or channel filters to reduce the real-time data set being rendered, particularly for large Enterprise accounts spanning multiple brands or regions.

**Prevention:** For large accounts, default to team-scoped or region-scoped dashboard views rather than an unfiltered account-wide view.

**Related Issues:** CDA-11002

---

## Section 2: Standard Reports

### CDA-2001 — Standard Report Showing Zero Data for a Known-Active Period

**Symptoms:** A standard volume or performance report displays no data for a date range known to have active ticket and chat volume.

**Cause:** The report's date range filter is referencing a different time zone than expected, shifting the effective query window outside the intended period.

**Solution:** Confirm the report's time zone setting under **Settings > Reports > Time Zone Preferences** matches your organization's expected reference time zone.

**Prevention:** Standardize on a single account-wide reporting time zone and document it for the team to avoid individual misinterpretation.

**Related Issues:** CDA-2002

---

### CDA-2002 — Standard Report Date Range Limited to 30 Days

**Symptoms:** Attempting to select a date range beyond 30 days in the past is not possible in Standard Reports.

**Cause:** Custom date ranges beyond the standard 30-day lookback are a Professional and Enterprise plan feature; Starter plan accounts are limited to the standard rolling 30-day window by design.

**Solution:** Upgrade to Professional or Enterprise to access custom date ranges, as described in the Corvex Cloud Pricing Guide, or work within the available 30-day window on Starter.

**Prevention:** Review plan-specific reporting limitations in the CloudDesk Analytics Product Overview before relying on longer historical ranges in planning.

**Related Issues:** none

---

### CDA-2003 — First Response Time Metric Appears Inflated

**Symptoms:** The reported average first response time is significantly higher than agents' subjective sense of their own responsiveness.

**Cause:** The metric calculation includes time outside configured business hours by default, or a small number of outlier tickets (e.g., ones left open over a weekend) are skewing the average.

**Solution:** Confirm whether business-hours-only calculation is enabled under **Settings > Reports > Metric Definitions**, and consider reviewing the report using a median rather than average view, where available, to reduce outlier sensitivity.

**Prevention:** Align metric calculation settings (business hours vs. calendar time) with how your team actually communicates SLA expectations internally.

**Related Issues:** CDA-2004

---

### CDA-2004 — Resolution Time Metric Inconsistent Between Reports

**Symptoms:** Two different standard reports show different resolution time figures for what appears to be the same underlying period and team.

**Cause:** One report calculates resolution time from ticket creation to first resolution, while another calculates it from creation to final closure, which can differ when a ticket is reopened.

**Solution:** Review each report's specific metric definition under **Settings > Reports > Metric Definitions** to confirm which calculation basis is in use before comparing figures across reports.

**Prevention:** Reference the platform-wide metric definitions consistently applied across CloudDesk Analytics, and clarify which definition your team uses for internal targets.

**Related Issues:** CDA-2003

---

### CDA-2005 — CSAT Report Excluding Some Survey Responses

**Symptoms:** The count of CSAT responses in a standard report is lower than the number of surveys known to have been sent.

**Cause:** The report counts only responses received within the report's selected date range based on response date, not send date, so responses received after the window closes are excluded from that period's figures.

**Solution:** If aligning send and response counts is important, widen the report's date range slightly to capture delayed responses, understanding that some natural lag between send and response is expected.

**Prevention:** Set internal expectations that CSAT response rate figures reflect responses received within a period, not surveys sent within it.

**Related Issues:** none

---

### CDA-2006 — Channel Breakdown Report Miscategorizing Converted Chats

**Symptoms:** A conversation that started as a chat and was converted to a ticket appears entirely under the "Ticket" channel category, with no visibility into its chat origin.

**Cause:** Channel breakdown reporting categorizes by the case's current, final channel state rather than its full origin history, by design.

**Solution:** If origin channel visibility is important, review the specific ticket's history directly, which retains the full conversion record, rather than relying on the channel breakdown report for this detail.

**Prevention:** For teams that need origin-channel reporting specifically, consider applying a tag at conversion time to preserve this dimension in reporting.

**Related Issues:** none

---

## Section 3: Custom Dashboards

### CDA-3001 — Cannot Create a Custom Dashboard

**Symptoms:** The **Create Dashboard** option is missing or grayed out.

**Cause:** Custom dashboards are a Professional and Enterprise plan feature; Starter plan accounts do not have access, or the user's role lacks dashboard creation permission.

**Solution:** Confirm your plan tier under **Admin Dashboard > Billing & Plan**, and confirm your role includes dashboard configuration permission under **Admin Dashboard > Roles & Permissions**.

**Prevention:** Review plan-specific feature availability in the CloudDesk Analytics Product Overview before planning custom dashboard work.

**Related Issues:** none

---

### CDA-3002 — Widget Displaying "No Data" Despite Underlying Activity

**Symptoms:** A specific widget on a custom dashboard shows no data, while other widgets on the same dashboard populate normally.

**Cause:** The widget's filter configuration (e.g., a specific tag, team, or channel) does not match any data in the selected date range.

**Solution:** Review the individual widget's filter configuration for overly narrow or outdated conditions, adjusting or removing filters as needed.

**Prevention:** When building dashboards, test each widget individually with a broad date range before narrowing filters, to confirm the underlying data exists before adding constraints.

**Related Issues:** CDA-3003

---

### CDA-3003 — Widget Filter Referencing a Deleted Tag or Field

**Symptoms:** A previously functioning widget begins showing an error or empty state after an unrelated configuration change elsewhere in the account.

**Cause:** The widget's filter references a tag or custom field that was deleted or renamed in CloudDesk Tickets or CloudDesk Chat.

**Solution:** Edit the widget under the custom dashboard and update the filter to reference the current, correct tag or field name.

**Prevention:** Before deleting or renaming a tag or field, search for custom dashboards referencing it and update them first.

**Related Issues:** CDA-3002

---

### CDA-3004 — Shared Dashboard Not Visible to Intended Team

**Symptoms:** A custom dashboard marked as shared is not appearing for the team members it was intended for.

**Cause:** The dashboard's sharing scope was set to a specific team or role that does not match the intended recipients, or sharing controls (Section 9) restrict visibility account-wide.

**Solution:** Review the dashboard's sharing configuration under **Dashboard Settings > Sharing**, and confirm the intended recipients' team or role assignment matches the configured scope.

**Prevention:** Confirm sharing scope immediately after creating a shared dashboard by checking with a sample recipient that it appears as expected.

**Related Issues:** CDA-9001

---

### CDA-3005 — Dashboard Owner Departure Leaving Orphaned Dashboard

**Symptoms:** A shared custom dashboard becomes uneditable or its scheduled delivery stops after the original creator's account is deactivated.

**Cause:** Ownership was not reassigned prior to deactivation, as described in the CloudDesk Analytics Administrator Guide, leaving the dashboard without an active owner able to modify it.

**Solution:** An administrator should reassign ownership under **Admin Dashboard > Analytics > Custom Dashboard Governance**, restoring full edit and delivery management capability.

**Prevention:** Reassign dashboard ownership as a standard step whenever deactivating a user known to own shared dashboards.

**Related Issues:** none

---

### CDA-3006 — Dashboard Layout Resetting After Editing

**Symptoms:** A custom dashboard's widget arrangement reverts to a previous layout after an editing session.

**Cause:** The dashboard was being edited simultaneously by two users, and the second save overwrote the first without merging changes, since concurrent editing does not merge conflicting layout changes.

**Solution:** Reapply the intended layout changes; going forward, coordinate with colleagues before simultaneously editing the same shared dashboard.

**Prevention:** Establish a single-owner-edits convention for shared dashboards, or communicate before making layout changes to a widely used dashboard.

**Related Issues:** none

---

### CDA-3007 — Custom Dashboard Widget Chart Type Not Available for Selected Metric

**Symptoms:** A desired chart type (e.g., pie chart) is not selectable for a specific metric when configuring a widget.

**Cause:** Certain chart types are only compatible with certain metric structures — for example, a time-series metric like resolution time trend does not support a static pie chart visualization.

**Solution:** Select a chart type compatible with the metric's data structure, as indicated by the available options in the widget configuration panel.

**Prevention:** Consider the intended visualization type before selecting a metric, since not all combinations are supported.

**Related Issues:** none

---

## Section 4: Scheduled Delivery

### CDA-4001 — Scheduled Report Not Being Delivered

**Symptoms:** A scheduled report configured for email delivery is not arriving for recipients.

**Cause:** The recipient's email address was removed from the account (e.g., due to deactivation), or delivery is being filtered as spam by the recipient's email system.

**Solution:** Confirm the recipient list under **Settings > Reports > Scheduled Delivery** includes current, active email addresses, and ask recipients to check spam/junk folders.

**Prevention:** Review scheduled delivery recipient lists periodically, particularly after any team personnel changes.

**Related Issues:** CDA-4002

---

### CDA-4002 — Scheduled Delivery Failing Silently

**Symptoms:** A scheduled report stops arriving with no visible error, and administrators only notice when a recipient asks about it.

**Cause:** A dependent widget or filter within the scheduled dashboard began referencing deleted data (Section 3.3), causing generation to fail without a user-facing alert being configured.

**Solution:** Review delivery status and failure history under **Admin Dashboard > Analytics > Scheduled Delivery**, and correct the underlying widget or filter issue causing generation failure.

**Prevention:** Enable delivery failure notifications for administrators under **Admin Dashboard > Analytics > Scheduled Delivery > Notifications**, so failures are caught proactively.

**Related Issues:** CDA-3003

---

### CDA-4003 — Scheduled Delivery Sent to Unintended External Recipient

**Symptoms:** A scheduled report was received by an email address outside the organization that should not have had access.

**Cause:** A recipient list was edited to include an incorrect address, or delivery restrictions limiting recipients to internal company domains were not enabled.

**Solution:** Immediately remove the unintended recipient from the scheduled delivery configuration, and enable delivery restrictions under **Admin Dashboard > Analytics > Security > Delivery Restrictions** (Professional and Enterprise) to prevent recurrence.

**Prevention:** Enable internal-domain-only delivery restrictions as a standing account-wide policy, particularly for reports containing sensitive performance data.

**Related Issues:** CDA-9002

---

### CDA-4004 — Scheduled Delivery Time Not Matching Configured Schedule

**Symptoms:** A report configured to arrive at 8:00 AM consistently arrives at a different time.

**Cause:** The scheduled delivery time is interpreted in the account's configured reporting time zone (Section 2.1), which may differ from the recipient's local time zone.

**Solution:** Confirm the account's reporting time zone under **Settings > Reports > Time Zone Preferences**, and adjust the schedule configuration to account for the difference from the recipient's local time, if needed.

**Prevention:** Document the account's reporting time zone clearly for anyone configuring scheduled deliveries.

**Related Issues:** CDA-2001

---

### CDA-4005 — Duplicate Scheduled Reports Being Received

**Symptoms:** A recipient receives the same scheduled report twice for a single delivery cycle.

**Cause:** The recipient is included both individually and as part of a distribution list also configured for delivery, resulting in two separate deliveries.

**Solution:** Review the full recipient configuration under **Settings > Reports > Scheduled Delivery**, removing the redundant individual or list-based entry.

**Prevention:** Standardize on either individual recipient entries or distribution list entries per scheduled report, avoiding mixing both for the same recipients.

**Related Issues:** none

---

## Section 5: Data Warehouse Export (Enterprise)

### CDA-5001 — Data Warehouse Export Connection Showing "Error" Status

**Symptoms:** The Data Warehouse Export connection status displays Error, halting scheduled exports.

**Cause:** The destination environment's authentication credentials have expired or been rotated on the destination side without updating the connection in CloudDesk Analytics.

**Solution:** Navigate to **Admin Dashboard > Analytics > Data Warehouse Export**, and reauthorize the connection with current destination credentials.

**Prevention:** Coordinate with your data engineering team before rotating destination credentials used by an active Corvex export connection.

**Related Issues:** CDA-5002

---

### CDA-5002 — Data Warehouse Export Missing Recent Records

**Symptoms:** Data available in CloudDesk Analytics dashboards is not yet present in the destination data warehouse.

**Cause:** The export runs on a scheduled interval rather than continuously, and the most recent data has not yet been included in the next scheduled run.

**Solution:** Confirm the export schedule under **Admin Dashboard > Analytics > Data Warehouse Export**, and, if more frequent delivery is needed, adjust the schedule or discuss a higher-frequency option with your Customer Success Manager.

**Prevention:** Set expectations with downstream data consumers about the export's actual refresh interval, rather than assuming real-time availability.

**Related Issues:** CDA-5001

---

### CDA-5003 — Data Warehouse Export Schema Mismatch After Platform Update

**Symptoms:** A downstream process consuming exported data begins failing after a Corvex platform update, citing an unexpected field or data type.

**Cause:** A new field was added to the export schema, or an existing field's data type was refined, and the downstream process was not built to tolerate additive schema changes.

**Solution:** Review the current export schema documentation in the Corvex Cloud developer documentation, and update the downstream process to handle the current schema, including any new fields.

**Prevention:** Design downstream data pipelines to tolerate additive schema changes gracefully, and subscribe to schema change notifications where available.

**Related Issues:** none

---

### CDA-5004 — Selected Dataset Not Appearing in Export

**Symptoms:** A specific dataset selected for inclusion in the data warehouse export does not appear in the destination environment.

**Cause:** The dataset selection was saved but not applied to the active export schedule, requiring a manual trigger or waiting for the next scheduled run to take effect.

**Solution:** Confirm the dataset selection is saved under **Admin Dashboard > Analytics > Data Warehouse Export**, and either trigger a manual export run or wait for the next scheduled cycle.

**Prevention:** After changing dataset selection, verify the change took effect on the next run rather than assuming immediate application.

**Related Issues:** none

---

## Section 6: Cross-Team and Cross-Region Reporting (Enterprise)

### CDA-6001 — Cross-Region Report Excluding a Known Region

**Symptoms:** A cross-region report intended to cover all account regions is missing data from one region.

**Cause:** The region was recently added to the account and has not yet been included in the cross-region report's configured scope.

**Solution:** Review the report's region scope configuration under **Settings > Reports > Cross-Region Configuration**, and add the missing region explicitly.

**Prevention:** Update cross-region and cross-brand report scope as a standard step whenever a new region or brand is added to the account.

**Related Issues:** none

---

### CDA-6002 — Cross-Brand Report Mixing Data Incorrectly

**Symptoms:** A report intended to separate performance by brand shows combined figures instead of a per-brand breakdown.

**Cause:** The underlying tickets or chats were not correctly tagged or associated with a specific brand at the time of creation, causing them to fall into an "unassigned brand" bucket rather than being properly separated.

**Solution:** Review brand tagging configuration under **Admin Dashboard > Analytics > Cross-Brand Configuration**, ensuring incoming channels are correctly associated with their intended brand.

**Prevention:** Confirm brand association is correctly configured for every channel (email address, chat widget, web form) before relying on cross-brand reporting.

**Related Issues:** CDA-6001

---

## Section 7: Metrics and Calculations

### CDA-7001 — NPS Score Displaying as a Negative Number Unexpectedly

**Symptoms:** A reported Net Promoter Score appears as a negative value, which a user assumes is an error.

**Cause:** This is expected behavior; NPS is calculated as the percentage of promoters minus the percentage of detractors and is mathematically capable of ranging from -100 to +100.

**Solution:** No action needed; a negative NPS indicates more detractors than promoters in the response set and is a valid, meaningful result.

**Prevention:** Include a brief explanation of NPS calculation methodology in internal reporting documentation for teams unfamiliar with the metric.

**Related Issues:** none

---

### CDA-7002 — Team Performance Benchmark Comparing Against an Inactive Agent

**Symptoms:** A team performance analytics view includes a deactivated agent in comparative benchmarking, skewing the visible range.

**Cause:** Historical data for a deactivated agent remains in the reporting period by design, since their historical activity is still valid data for the period in which it occurred.

**Solution:** Apply an "active agents only" filter, where available, under the team performance widget configuration to exclude historical data from agents no longer on the team for forward-looking comparisons.

**Prevention:** Establish a standard practice of filtering to currently active agents when presenting forward-looking staffing or performance discussions.

**Related Issues:** none

---

### CDA-7003 — Backlog Trend Showing an Unexpected Spike on a Single Day

**Symptoms:** A backlog trend chart shows an unusual single-day spike not corresponding to any known event.

**Cause:** A bulk import of historical tickets (for example, during a data migration) created a large number of tickets with a creation timestamp on that single day, rather than reflecting genuine same-day volume.

**Solution:** Cross-reference the spike date against any known bulk import or migration activity under **Admin Dashboard > Data > Import History** before treating it as a genuine operational signal.

**Prevention:** When performing bulk historical imports, consider whether backdating creation timestamps to reflect true historical dates (where supported) would better preserve accurate trend reporting.

**Related Issues:** none

---

### CDA-7004 — Average Handle Time Metric Not Matching Manual Calculation

**Symptoms:** A manually calculated average handle time for a small sample of tickets does not match the reported platform figure.

**Cause:** The platform's calculation excludes time the ticket spent in a Pending status (waiting on the customer) by default, while a manual calculation may have included total elapsed time regardless of status.

**Solution:** Review the metric definition under **Settings > Reports > Metric Definitions** to confirm which status durations are included or excluded, and align manual calculations to the same methodology for accurate comparison.

**Prevention:** Reference platform metric definitions before performing manual spot-checks, to avoid comparing figures calculated on different bases.

**Related Issues:** CDA-2003

---

## Section 8: Filters and Date Ranges

### CDA-8001 — Applied Filter Not Persisting Between Sessions

**Symptoms:** A filter applied to a report or dashboard resets to default after logging out and back in.

**Cause:** The filter was applied as a temporary view adjustment rather than saved as a named saved view or default.

**Solution:** Use **Save View** to persist a frequently used filter combination, rather than reapplying it manually each session.

**Prevention:** Encourage saving any filter combination used more than once as a named saved view.

**Related Issues:** none

---

### CDA-8002 — Custom Date Range Producing Inconsistent Results on Refresh

**Symptoms:** A custom date range report shows slightly different totals each time it is refreshed on the same day.

**Cause:** The custom date range includes "today" as the end date, and today's data is still actively accumulating as new tickets and chats arrive throughout the day.

**Solution:** This is expected behavior for any report including the current, incomplete day; for a stable, final figure, use a date range ending on the most recently completed full day.

**Prevention:** Default recurring reports intended for stable comparison to end on the prior complete day rather than including the current, in-progress day.

**Related Issues:** none

---

### CDA-8003 — Filter Combination Returning Unexpectedly Empty Results

**Symptoms:** Applying multiple filters together (e.g., team and tag) returns no results, though each filter individually returns data.

**Cause:** The combination of filters, while each individually valid, does not correspond to any actual tickets matching both conditions simultaneously — for example, a tag that happens not to be used by the selected team.

**Solution:** Verify the underlying data actually satisfies both conditions together by checking the ticket queue directly with the same combined filter; this may reflect a genuinely empty result rather than a reporting defect.

**Prevention:** When building complex filter combinations, add filters one at a time and observe the result at each step to catch an unexpectedly narrowing combination early.

**Related Issues:** none

---

## Section 9: Access and Sharing

### CDA-9001 — Read-Only User Unable to View a Specific Dashboard

**Symptoms:** A user with the Read-only / Reporting role cannot see a specific custom dashboard, despite being able to view others.

**Cause:** The specific dashboard's sharing configuration restricts visibility to a narrower set of roles or teams than the user belongs to.

**Solution:** Review the dashboard's sharing settings under **Dashboard Settings > Sharing**, and adjust scope to include the intended user or their role/team.

**Prevention:** Confirm sharing scope against intended audience whenever creating a dashboard meant for broad visibility.

**Related Issues:** CDA-3004

---

### CDA-9002 — Dashboard External Sharing Link Not Working

**Symptoms:** An external sharing link for a dashboard, generated for a stakeholder outside the account, returns an access error.

**Cause:** External dashboard sharing was disabled account-wide under sharing controls, or the specific link expired based on a configured expiration policy.

**Solution:** Confirm external sharing is enabled under **Admin Dashboard > Analytics > Security > Sharing Controls**, and generate a new link if the previous one expired.

**Prevention:** Communicate any account-wide sharing restriction change to teams that regularly share dashboards externally, to avoid confusion when links stop working.

**Related Issues:** CDA-4003

---

### CDA-9003 — Team Lead Able to See Another Team's Performance Data

**Symptoms:** A team lead's dashboard unexpectedly displays performance data for a team they do not manage.

**Cause:** The team lead's role or custom permission configuration grants account-wide reporting scope rather than being limited to their own team, often due to a permission template applied too broadly during setup.

**Solution:** Review the affected user's reporting scope under **Admin Dashboard > Roles & Permissions**, and narrow it to their intended team if account-wide access was not deliberate.

**Prevention:** Use custom roles deliberately scoped to team-level access for team leads, rather than defaulting to broader account-wide reporting permissions.

**Related Issues:** none

---

### CDA-9004 — Agent Unable to See Their Own Performance Summary

**Symptoms:** An agent cannot access even their own individual performance data, which should be available by default to the Agent role.

**Cause:** A custom role was applied to the agent that unintentionally omitted the baseline "own performance" viewing permission included in the standard Agent role.

**Solution:** Review the custom role's permission configuration under **Admin Dashboard > Roles & Permissions > Custom Roles**, and add the individual performance viewing permission if missing.

**Prevention:** When building a custom role based on the standard Agent role, explicitly confirm baseline permissions like own-performance visibility are retained.

**Related Issues:** none

---

## Section 10: Integrations

### CDA-10001 — Business Intelligence Tool Not Reflecting CRM-Enriched Data

**Symptoms:** Data exported to a business intelligence tool is missing CRM-sourced fields visible within the CloudDesk Analytics dashboard itself.

**Cause:** The data warehouse export dataset selection was not configured to include CRM-enriched fields, since these may be a separate, optional dataset from core ticket and chat data.

**Solution:** Review dataset selection under **Admin Dashboard > Analytics > Data Warehouse Export**, and include the CRM-enriched dataset if available on your integration configuration.

**Prevention:** Review available dataset options fully when initially configuring data warehouse export, rather than accepting only the default core dataset selection.

**Related Issues:** CDA-5004

---

### CDA-10002 — Webhook for Threshold Alert Not Firing

**Symptoms:** A configured webhook intended to notify an external system when a metric threshold is crossed does not deliver an event.

**Cause:** The webhook endpoint configuration was set up under the CloudDesk API Platform Developer Portal but the specific analytics threshold event type was not included in the endpoint's event subscription.

**Solution:** Review the webhook's event subscription under the Developer Portal, and add the specific threshold alert event type if missing.

**Prevention:** When configuring a new threshold alert intended to trigger a webhook, cross-check the Developer Portal's event subscription in the same session to avoid a missed step.

**Related Issues:** none

---

## Section 11: Performance

### CDA-11001 — Dashboard Rendering Slowly on Load

**Symptoms:** A custom dashboard with many widgets takes a noticeably long time to fully render.

**Cause:** A large number of widgets, particularly those with broad, unfiltered date ranges, are each independently querying and rendering simultaneously.

**Solution:** Reduce the number of widgets on a single dashboard, or narrow individual widget date ranges and filters to reduce the volume of data each widget must process.

**Prevention:** When designing dashboards intended for daily use, favor a smaller number of focused widgets over a comprehensive but slow-loading single view.

**Related Issues:** CDA-1004

---

### CDA-11002 — Export Generation Taking an Unusually Long Time

**Symptoms:** A CSV export of a large report remains in a processing state well beyond the typical completion time.

**Cause:** The export scope covers an unusually large volume of historical data without a narrowing date range or filter applied.

**Solution:** Allow additional time for large exports to complete; if the export remains stuck for more than 24 hours, contact Corvex support to investigate. Narrowing the export scope with a specific date range will speed up future exports.

**Prevention:** Scope exports with a specific date range or filter where full history isn't required, reducing processing time.

**Related Issues:** none

---

### CDA-11003 — Mobile Performance Snapshot Loading Slowly on Older Devices

**Symptoms:** The condensed CloudDesk Mobile performance snapshot loads noticeably slower on an older device compared to a newer one.

**Cause:** Older device hardware processes the snapshot's rendering more slowly, particularly for accounts with a large number of active teams or metrics.

**Solution:** Refer to the CloudDesk Mobile Troubleshooting Guide for device-specific performance guidance; on the Analytics side, no specific action is available beyond what is already optimized in the condensed snapshot view.

**Prevention:** Encourage use of currently supported device operating system versions, which generally include performance improvements over older, unsupported versions.

**Related Issues:** none

---

## Section 12: Security

### CDA-12001 — SSO User Losing Reporting Access After Identity Provider Change

**Symptoms:** A user who previously had reporting access loses it after an identity provider migration or attribute mapping change.

**Cause:** The SSO attribute mapping change altered how the user's role or group membership is communicated to CloudDesk Analytics, resulting in a different, more restrictive role being applied than before.

**Solution:** Review the current SSO attribute mapping under **Admin Dashboard > Security > Single Sign-On**, and confirm the mapping correctly reflects the user's intended role and reporting scope.

**Prevention:** Test SSO attribute mapping changes against a sample of representative users, including those with elevated reporting access, before rolling out account-wide.

**Related Issues:** CDA-9003

---

### CDA-12002 — IP Allowlisting Blocking Scheduled Delivery Configuration Access

**Symptoms:** An administrator working remotely cannot access scheduled delivery configuration, receiving an access-denied message.

**Cause:** IP allowlisting is restricting Admin Dashboard access, including Analytics configuration, to approved IP ranges that do not include the administrator's current location.

**Solution:** Access the Admin Dashboard from an approved network, or have another administrator add the current IP range under **Admin Dashboard > Security > IP Allowlisting**.

**Prevention:** Maintain a documented, quickly actionable process for temporarily approving a new IP range for legitimate remote administrative access.

**Related Issues:** none

---

### CDA-12003 — Audit Log Missing an Expected Dashboard Sharing Change

**Symptoms:** An administrator cannot find a record of a specific dashboard sharing configuration change in the audit log.

**Cause:** The change occurred outside the account's current audit log retention window (90 days on Professional; extended on Enterprise).

**Solution:** Confirm the date of the change against your plan's retention window; if within the window and still missing, contact Corvex support to investigate.

**Prevention:** Export audit logs periodically for long-term retention beyond the platform's built-in window if your organization requires longer historical records.

**Related Issues:** none

---

## Section 13: Threshold Alerts

### CDA-13001 — Threshold Alert Not Firing Despite Metric Crossing the Configured Value

**Symptoms:** A configured threshold alert (e.g., backlog exceeding 50 open tickets) does not trigger a notification despite the metric visibly crossing that value on the dashboard.

**Cause:** The alert's evaluation frequency (e.g., checked every 15 minutes) did not happen to coincide with the brief period the metric was above threshold, if the metric quickly returned below the value between evaluation checks.

**Solution:** Review the alert's evaluation frequency under **Settings > Reports > Threshold Alerts**, and consider a shorter evaluation interval for metrics known to fluctuate quickly, if available on your plan.

**Prevention:** Set thresholds and evaluation frequency with an understanding of how quickly the underlying metric typically changes, to avoid missing brief threshold crossings.

**Related Issues:** none

---

### CDA-13002 — Threshold Alert Recipient Not Receiving Notifications

**Symptoms:** A user configured as a threshold alert recipient does not receive notifications despite the alert firing for other recipients.

**Cause:** The individual recipient has threshold alert notifications disabled in their personal notification preferences, which take precedence over account-wide alert configuration.

**Solution:** Ask the affected user to enable threshold alert notifications under **My Settings > Notifications**.

**Prevention:** Communicate to new threshold alert recipients that they must also enable the corresponding personal notification preference for delivery to occur.

**Related Issues:** CDA-4001

---

## Section 14: General Behavior and Edge Cases

### CDA-14001 — Report Data Differing Slightly Between Desktop and Mobile Views

**Symptoms:** A performance snapshot on CloudDesk Mobile shows a slightly different figure than the equivalent full report on desktop for the same period.

**Cause:** The mobile snapshot uses a simplified, pre-aggregated calculation optimized for fast loading, which may round or approximate certain figures differently than the full desktop report.

**Solution:** For any figure requiring precise accuracy (e.g., for external reporting), rely on the full desktop report rather than the mobile snapshot, which is optimized for quick status checks.

**Prevention:** Communicate to the team that mobile snapshots are intended for quick reference, with the desktop report serving as the authoritative source for precise figures.

**Related Issues:** none

---

### CDA-14002 — Saved View Disappearing After Role Change

**Symptoms:** A user's previously saved dashboard view is no longer accessible after their role was changed.

**Cause:** The saved view referenced a filter scope (e.g., a specific team) no longer available to the user's new, more restricted role.

**Solution:** Recreate the saved view within the scope now available to the user's updated role, or adjust their role's permissions if the previous scope should still be accessible.

**Prevention:** Review a user's saved views before making a role change that narrows their reporting scope, to set expectations about what will remain accessible.

**Related Issues:** CDA-9003

---

### CDA-14003 — Exported CSV File Displaying Garbled Characters in Spreadsheet Software

**Symptoms:** Non-Latin characters (such as accented letters or non-English text) display incorrectly when a CSV export is opened directly in certain spreadsheet applications.

**Cause:** The spreadsheet application's default import settings are not correctly detecting the file's UTF-8 encoding.

**Solution:** When opening the CSV, use your spreadsheet application's explicit import function and select UTF-8 encoding, rather than double-clicking to open the file with default settings.

**Prevention:** Include a brief note on correct CSV import settings in internal documentation for teams that regularly work with exported data containing non-English text.

**Related Issues:** none

---

### CDA-14004 — Dashboard Timestamp Displaying in Server Time Instead of Local Time

**Symptoms:** Timestamps shown on a dashboard appear offset from the viewer's actual local time.

**Cause:** The dashboard is rendering according to the account's configured reporting time zone (Section 2.1) rather than the individual viewer's browser or profile time zone.

**Solution:** This is expected behavior for account-wide reporting consistency; if individual local time display is needed, review your profile time zone setting, which governs certain personal views distinct from shared account-wide reports.

**Prevention:** Clarify for the team which views reflect account-wide reporting time zone versus individual profile time zone, to avoid confusion when comparing timestamps.

**Related Issues:** CDA-2001

---

*This Troubleshooting Guide covers common CloudDesk Analytics issues and their resolutions. If an issue is not listed here or a documented solution does not resolve your problem, contact Corvex support through the channel appropriate to your plan tier, as described in the Corvex Cloud Pricing Guide.*
