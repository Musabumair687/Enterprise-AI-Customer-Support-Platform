# CloudDesk Tickets
## Troubleshooting Guide

*Corvex Cloud — CloudDesk Tickets*
*This guide documents known issues, their causes, and their resolutions for CloudDesk Tickets. It is intended for administrators, agents, and technical staff diagnosing problems with the platform. For general usage instructions, refer to the CloudDesk Tickets User Manual. For configuration guidance, refer to the CloudDesk Tickets Administrator Guide.*

---

## How to Use This Guide

Issues are grouped by category. Each entry includes the symptoms you may observe, the most common underlying cause, a recommended solution, steps to prevent recurrence, and related issues you may want to review if the listed solution does not fully resolve your problem.

---

## Section 1: Email Channel Intake

### CDT-1001 — Inbound Emails Not Creating Tickets

**Symptoms:** Emails sent to the connected support address are received but no corresponding ticket appears in the queue.

**Cause:** The mailbox connection's authentication token has expired, or DNS mail routing records were changed after the initial connection was established.

**Solution:** Navigate to **Settings > Channels > Email** and check the connection status; reauthorize the mailbox if flagged, and verify DNS routing records match the values provided at setup.

**Prevention:** Coordinate with your IT/DNS team before making any changes to mail routing records associated with the connected support address.

**Related Issues:** CDT-1002, CDT-1003

---

### CDT-1002 — Duplicate Tickets Created from a Single Email

**Symptoms:** One inbound email results in two or more separate tickets.

**Cause:** The email was sent to more than one connected support address (e.g., both a general and a department-specific mailbox both configured to ingest the same forwarded message), or an autoresponder loop caused repeated ingestion.

**Solution:** Review your mail forwarding configuration for overlapping ingestion paths, and merge the resulting duplicate tickets using **Merge Tickets**.

**Prevention:** Map out your mail forwarding rules before connecting multiple mailboxes to avoid the same message reaching more than one ingestion point.

**Related Issues:** CDT-1001, CDT-4001

---

### CDT-1003 — Email Reply Not Threading to Existing Ticket

**Symptoms:** A customer's reply to an existing ticket creates a new ticket instead of adding to the original thread.

**Cause:** The customer used a different email client that stripped the threading reference header, or they replied to a forwarded copy of the original message rather than the original itself.

**Solution:** Manually merge the new ticket into the original using **Merge Tickets**. There is no way to retroactively force correct threading once the header is lost, since threading depends on data the customer's client controls.

**Prevention:** Include a visible ticket reference number in outbound email templates as a fallback identifier customers can reference even if automatic threading fails.

**Related Issues:** CDT-1002, CDT-4001

---

### CDT-1004 — Email Attachments Missing from Created Ticket

**Symptoms:** A ticket created from an inbound email is missing an attachment the sender confirms they included.

**Cause:** The attachment exceeded the maximum allowed size, or its file type is on the platform's restricted list for security reasons.

**Solution:** Ask the sender to resend the attachment in a supported format and within size limits, documented in the CloudDesk Tickets Product Overview, or share the file through an alternate secure channel if it cannot meet those limits.

**Prevention:** Include attachment size and type limits in your public-facing support contact instructions.

**Related Issues:** none

---

### CDT-1005 — Auto-Reply Not Sending to New Ticket Submitters

**Symptoms:** Customers do not receive the expected automatic acknowledgment email after submitting a new ticket.

**Cause:** The auto-reply template was disabled during a recent workflow change, or the sending mailbox's authentication has degraded, silently failing outbound send while inbound ingestion continues to work.

**Solution:** Confirm the auto-reply template is enabled under **Settings > Channels > Email > Auto-Reply**, and check outbound send health under the same connection's status indicator.

**Prevention:** Periodically send a test ticket to confirm both inbound ingestion and outbound auto-reply are functioning together, since one can fail independently of the other.

**Related Issues:** CDT-1001

---

### CDT-1006 — Email Signature or Formatting Breaking Ticket Display

**Symptoms:** A ticket's message content displays broken formatting, stray HTML tags, or an oversized embedded image from the sender's email signature.

**Cause:** The sender's email client generated non-standard HTML markup that the ticket rendering view does not fully normalize.

**Solution:** This is a display-only issue; the original message content and any attachments are preserved and unaffected. If the formatting significantly hinders readability, request the sender resend as plain text.

**Prevention:** No specific preventive action is available for inbound formatting variation, since it originates from the sender's own email client.

**Related Issues:** none

---

## Section 2: Web Form Channel

### CDT-2001 — Web Form Submissions Not Creating Tickets

**Symptoms:** Visitors report submitting the contact form, but no corresponding ticket is created.

**Cause:** The embed snippet was removed or altered during a website update, or a required field's validation is silently failing without clearly informing the visitor.

**Solution:** Confirm the web form snippet is correctly installed under **Settings > Channels > Web Form > Installation**, and review field validation rules for any recently introduced misconfiguration.

**Prevention:** Include a web form submission test as a standard step in any website deployment checklist that touches the page hosting the form.

**Related Issues:** CDT-2002

---

### CDT-2002 — Web Form Custom Fields Not Mapping to Ticket Fields

**Symptoms:** Data submitted through custom web form fields does not appear in the corresponding ticket fields.

**Cause:** The web form field's internal identifier does not match the ticket field it is intended to populate, often after one was renamed independently of the other.

**Solution:** Review field mapping under **Settings > Channels > Web Form > Field Mapping** and correct any mismatched identifiers.

**Prevention:** Treat field identifiers as stable once mapped; use display label changes for cosmetic updates rather than altering the underlying identifier.

**Related Issues:** CDT-2001, CDT-9002

---

### CDT-2003 — Web Form Submission Rejected as Spam

**Symptoms:** A legitimate customer reports their form submission was not received; the submission appears in a spam-filtered queue instead of the main ticket queue.

**Cause:** Automated spam filtering flagged the submission based on content patterns or submission velocity from the same IP address.

**Solution:** Review the spam-filtered queue under **Settings > Channels > Web Form > Spam Review**, and release legitimate submissions manually.

**Prevention:** If legitimate submissions are frequently flagged, review and adjust spam sensitivity settings, particularly for high-volume, legitimate use cases like bulk order support forms.

**Related Issues:** none

---

### CDT-2004 — File Upload Failing on Web Form

**Symptoms:** A visitor cannot attach a file when submitting the web form.

**Cause:** The file exceeds configured size limits, or the visitor's browser is blocking the upload due to a mixed-content warning on a non-HTTPS page hosting the form.

**Solution:** Confirm the hosting page uses HTTPS, and confirm the file meets size and type requirements documented in the CloudDesk Tickets Product Overview.

**Prevention:** Host the web form only on HTTPS pages, consistent with modern web security practice.

**Related Issues:** CDT-1004

---

## Section 3: CloudDesk Chat to Ticket Conversion

### CDT-3001 — Converted Chat Missing Prior Message History

**Symptoms:** A chat conversation converted into a ticket does not display the full prior chat transcript.

**Cause:** The conversion was performed on a chat that had already been split or merged in CloudDesk Chat prior to conversion, creating an incomplete reference chain.

**Solution:** Use the customer context panel to locate the original chat conversation directly, since full history remains accessible there even if the converted ticket's inline display is incomplete.

**Prevention:** Avoid merging or splitting a chat conversation immediately before converting it to a ticket; complete one action before performing the other.

**Related Issues:** none

---

### CDT-3002 — Duplicate Ticket Created After Chat Conversion

**Symptoms:** Converting a chat to a ticket results in two tickets instead of one.

**Cause:** The conversion action was triggered twice in quick succession, often due to a slow page response leading the agent to click **Convert to Ticket** a second time.

**Solution:** Merge the duplicate tickets using **Merge Tickets**, keeping the one with the complete reference to the original chat.

**Prevention:** Wait for visual confirmation after clicking **Convert to Ticket** before taking any further action on the conversation.

**Related Issues:** CDT-4001

---

### CDT-3003 — Converted Ticket Not Reflecting Chat Tags

**Symptoms:** Tags applied to a chat conversation do not carry over to the resulting ticket after conversion.

**Cause:** A tag applied in CloudDesk Chat does not exist in the CloudDesk Tickets tag list, since tag lists, while shared at the account level, can diverge if a tag was created channel-specifically before a recent platform update.

**Solution:** Manually reapply the missing tag on the ticket; going forward, confirm tag lists are unified under **Settings > Tags** to prevent recurrence.

**Prevention:** Create and manage tags centrally rather than allowing ad hoc tag creation in individual channel contexts.

**Related Issues:** CDT-9003

---

## Section 4: Ticket Workflow (Status, Priority, Merge, Split)

### CDT-4001 — Merge Tickets Option Not Available

**Symptoms:** The **Merge Tickets** action is missing or grayed out when attempting to consolidate duplicate tickets.

**Cause:** The user's role does not include merge permission, or one of the two tickets involved has already been merged into a third ticket, and a ticket cannot be merged twice.

**Solution:** Confirm the user's role includes ticket merge permission under **Admin Dashboard > Roles & Permissions**, and confirm neither ticket has already been merged elsewhere.

**Prevention:** Grant merge permission to all agent-level roles by default, since it is a routine part of ticket hygiene rather than a sensitive administrative action.

**Related Issues:** CDT-1002, CDT-3002

---

### CDT-4002 — Split Ticket Losing Original Attachments

**Symptoms:** After splitting a multi-issue ticket into two, an attachment from the original message is present on only one of the resulting tickets.

**Cause:** Split behavior assigns the original message, including its attachments, to the ticket branch containing that original message; attachments are not duplicated across both resulting tickets by default.

**Solution:** Manually re-attach the relevant file to the second ticket if it is genuinely needed there as well.

**Prevention:** When splitting a ticket, review which resulting branch retains the original message and its attachments before considering the split complete.

**Related Issues:** none

---

### CDT-4003 — Ticket Status Reverting Unexpectedly

**Symptoms:** A ticket manually set to Resolved automatically reverts to Open shortly afterward.

**Cause:** An automation rule configured to reopen a ticket upon any new customer reply is functioning as designed, and the customer sent a follow-up message after the agent marked it resolved.

**Solution:** This is typically expected behavior; review the specific automation rule under **Settings > Workflow > Automation** if reopening behavior should be scoped more narrowly (e.g., excluding auto-generated confirmation replies).

**Prevention:** Configure automation rules to distinguish between substantive customer replies and automated bounce or confirmation messages, where your email provider allows this distinction.

**Related Issues:** CDT-4004

---

### CDT-4004 — Automation Rule Not Triggering

**Symptoms:** A configured automation rule (e.g., auto-tagging based on keyword) does not appear to be running on matching tickets.

**Cause:** The rule's trigger condition uses an outdated field reference, or the rule was saved but left in a disabled state.

**Solution:** Review the rule's configuration and enabled status under **Settings > Workflow > Automation**, and confirm all referenced fields and values are current.

**Prevention:** Test new automation rules against a sample ticket before relying on them broadly across the queue.

**Related Issues:** CDT-4003

---

### CDT-4005 — Bulk Action Applying to Wrong Set of Tickets

**Symptoms:** A bulk status or tag update was applied to more tickets than intended.

**Cause:** The bulk action was performed with an active filter broader than assumed, or a "select all" action selected all tickets matching the current filter across multiple pages rather than only the visible page.

**Solution:** Review the affected tickets and manually revert the unintended changes; going forward, always confirm the exact scope shown in the bulk action confirmation dialog before proceeding.

**Prevention:** Apply narrow, specific filters before using "select all," and review the confirmation count shown before finalizing a bulk action.

**Related Issues:** none

---

### CDT-4006 — Custom Status Not Appearing in Filter Options

**Symptoms:** A newly created custom ticket status is not selectable when building a filter or saved view.

**Cause:** A short propagation delay following status creation, or the status was created but not added to the default status set used in filter dropdowns.

**Solution:** Refresh the page after a brief wait; if the status remains unavailable, confirm it was properly saved (not left in draft) under **Settings > Workflow > Statuses**.

**Prevention:** Allow a short buffer after creating new configuration elements before relying on them in saved views or reporting.

**Related Issues:** none

---

## Section 5: Assignment and Routing

### CDT-5001 — New Tickets Not Being Assigned

**Symptoms:** Tickets accumulate in the Unassigned queue despite an active assignment rule.

**Cause:** The assignment rule's conditions do not match the actual incoming tickets, or all eligible agents are currently marked unavailable.

**Solution:** Review the assignment rule's conditions under **Settings > Workflow > Assignment**, and confirm at least one eligible agent has an Available status.

**Prevention:** Configure a fallback assignment rule that assigns to a general queue or team lead when no specific condition matches, avoiding tickets sitting unassigned indefinitely.

**Related Issues:** CDT-5002

---

### CDT-5002 — Assignment Skewing Toward a Single Agent

**Symptoms:** One agent consistently receives a disproportionate share of assigned tickets under round-robin or workload-balanced assignment.

**Cause:** The affected agent's availability status remains Available for longer periods than teammates, or a skill tag is disproportionately assigned to that agent alone, funneling more matching tickets their way.

**Solution:** Review team availability patterns and skill tag distribution under **Admin Dashboard > Users**, adjusting either to achieve intended balance.

**Prevention:** Periodically review assignment distribution reporting in CloudDesk Analytics to catch skew early.

**Related Issues:** CDT-5001

---

### CDT-5003 — SLA Target Not Applying to a Specific Ticket

**Symptoms:** A ticket that should be subject to an SLA target shows no SLA indicator or countdown.

**Cause:** The ticket's priority or category does not match any configured SLA rule's conditions, or SLA management is not enabled for the plan tier.

**Solution:** Confirm SLA management is available on your plan (Professional and Enterprise) and review SLA rule conditions under **Settings > Workflow > SLAs** against the specific ticket's priority and category.

**Prevention:** Configure a default SLA rule covering any priority/category combination not explicitly addressed by a more specific rule.

**Related Issues:** CDT-5004

---

### CDT-5004 — SLA Countdown Displaying Incorrect Remaining Time

**Symptoms:** The SLA countdown shown on a ticket does not match the expected remaining time based on the configured target.

**Cause:** Business hours configuration (excluding nights/weekends from the countdown) is enabled but not accounted for in the agent's mental calculation, or the ticket's priority was changed mid-flight, recalculating the target based on the new priority's SLA rule.

**Solution:** Confirm whether business-hours-only SLA calculation is enabled under **Settings > Workflow > SLAs**, and check the ticket's audit history for any priority changes that would have reset the countdown basis.

**Prevention:** Clearly communicate to the team whether SLA countdowns reflect calendar time or business hours only, to avoid mental miscalculation.

**Related Issues:** CDT-5003

---

### CDT-5005 — Escalation Not Notifying the Correct Team Lead

**Symptoms:** An SLA breach or manual escalation is not reaching the intended team lead.

**Cause:** The escalation path is configured to notify a specific named individual rather than a role or team, and that individual has since changed roles or left the organization.

**Solution:** Update the escalation path under **Settings > Workflow > SLAs > Escalation** to target a role or team distribution rather than a specific named person, where possible, and correct the current configuration.

**Prevention:** Favor role-based escalation targets over named individuals wherever the platform supports it, to remain accurate through personnel changes.

**Related Issues:** CDT-5003

---

### CDT-5006 — Reassignment Not Updating the Ticket Owner Field

**Symptoms:** A ticket manually reassigned to a different agent still displays the previous agent as the owner in some views or reports.

**Cause:** A caching delay in a specific report or saved view, distinct from the underlying, correctly updated ticket record.

**Solution:** Refresh the affected report or view; the underlying ticket record itself is accurate immediately upon reassignment.

**Prevention:** No specific preventive action is available for this transient reporting cache behavior.

**Related Issues:** none

---

## Section 6: Macros and Canned Responses

### CDT-6001 — Macro Not Appearing for a Specific Agent

**Symptoms:** A team-wide macro is visible to most agents but missing for one specific agent.

**Cause:** The affected agent belongs to a team the macro was not scoped to, often due to a recent team reassignment that was not reflected in macro visibility settings.

**Solution:** Review macro scoping under **Settings > Macros & Responses**, and confirm the agent's current team assignment matches the macro's intended audience.

**Prevention:** Review macro scope whenever a broad team restructuring occurs, rather than assuming existing scoping remains correct.

**Related Issues:** CDT-6002

---

### CDT-6002 — Macro Executing Only Part of Its Configured Actions

**Symptoms:** Running a macro applies the tag and status change but does not send the associated reply, or vice versa.

**Cause:** One step within the macro references a canned response or field that was deleted after the macro was originally built.

**Solution:** Review each step of the macro under **Settings > Macros & Responses**, and replace any reference to deleted content with a current equivalent.

**Prevention:** Before deleting a canned response or field, search for macros referencing it and update them first.

**Related Issues:** CDT-6001

---

### CDT-6003 — Canned Response Formatting Lost When Inserted

**Symptoms:** A canned response with formatting (bold text, bullet points, links) inserts as plain, unformatted text in the reply composer.

**Cause:** The canned response was originally created by pasting from an external source that embedded incompatible formatting markup, which is stripped on insertion.

**Solution:** Recreate the canned response's formatting using the composer's native formatting tools rather than pasting from an external document.

**Prevention:** Build canned responses directly within the CloudDesk Tickets composer where formatting is required, rather than pasting from Word processors or other external tools.

**Related Issues:** none

---

### CDT-6004 — Shared Macro Edited Without Team Awareness

**Symptoms:** A macro begins behaving differently than agents expect, with no clear explanation.

**Cause:** Another administrator or team lead edited the shared macro's configuration without communicating the change to the team.

**Solution:** Review the macro's edit history via the Audit Log, and communicate the current, correct behavior to the affected team.

**Prevention:** Establish an internal change communication process for shared macros, given their account-wide, multi-user impact.

**Related Issues:** none

---

## Section 7: Tagging and Custom Fields

### CDT-7001 — Custom Field Not Appearing on Ticket Form

**Symptoms:** A newly created custom field does not appear when viewing or editing a ticket.

**Cause:** The field was created but not added to the active ticket form layout, or it was scoped to a specific ticket category that does not match the ticket being viewed.

**Solution:** Confirm the field is added to the relevant form layout and category scope under **Settings > Workflow > Fields**.

**Prevention:** When creating a new custom field, immediately confirm its visibility on a live test ticket before considering setup complete.

**Related Issues:** none

---

### CDT-7002 — Custom Field Value Not Saving

**Symptoms:** An agent enters a value into a custom field, but it does not persist after navigating away and returning.

**Cause:** The field has a validation rule (such as a required format or numeric range) that the entered value does not satisfy, and the resulting error was not clearly surfaced to the agent.

**Solution:** Review the field's validation rules under **Settings > Workflow > Fields**, and confirm the entered value matches the expected format.

**Prevention:** Provide clear placeholder text or helper descriptions on custom fields with specific format requirements.

**Related Issues:** none

---

### CDT-7003 — Duplicate Tags with Inconsistent Capitalization

**Symptoms:** The tag list contains what appear to be duplicate entries differing only in capitalization (e.g., "Refund" and "refund"), fragmenting reporting.

**Cause:** Tag creation was not restricted to administrators, allowing inconsistent manual entry by multiple agents over time.

**Solution:** Consolidate duplicate tags under **Settings > Tags** by merging them into a single canonical entry, then update any saved filters or automation rules referencing the removed variant.

**Prevention:** Restrict tag creation to administrators, or enable tag autocomplete/suggestion to reduce free-text entry.

**Related Issues:** CDT-3003

---

### CDT-7004 — Field Data Missing After Bulk Import

**Symptoms:** Tickets created via a bulk data import are missing values in custom fields that were included in the import file.

**Cause:** A column header in the import file did not exactly match the custom field's internal identifier.

**Solution:** Review the import file's column headers against the exact field identifiers documented in the import template, and re-import the affected records with corrected headers.

**Prevention:** Always start from the current, downloadable import template under **Admin Dashboard > Data > Import** rather than a previously saved template that may be outdated.

**Related Issues:** none

---

## Section 8: Reporting and Analytics

### CDT-8001 — Ticket Volume Report Not Matching Manual Count

**Symptoms:** A standard volume report shows a different ticket count than manually counting tickets in a filtered queue view for the same period.

**Cause:** The report and the queue view are using different date basis definitions — for example, the report counts by creation date while the queue filter is based on last-updated date.

**Solution:** Confirm both the report and the queue filter are using the same date field (created, updated, or resolved) before comparing counts.

**Prevention:** Standardize on a single date basis for routine reporting comparisons across your team to avoid this recurring confusion.

**Related Issues:** none

---

### CDT-8002 — SLA Compliance Percentage Lower Than Expected

**Symptoms:** The SLA compliance report shows a lower percentage than the team's informal sense of performance would suggest.

**Cause:** A recently changed SLA target (made stricter) is being applied retroactively to the full reporting period, including tickets handled under the previous, more lenient target.

**Solution:** Review the SLA rule's change history via the Audit Log, and consider filtering reports to periods after the target change for an accurate comparison against current performance.

**Prevention:** When tightening an SLA target, communicate the change and expect a temporary compliance percentage shift as reporting adjusts to the new baseline.

**Related Issues:** CDT-5003

---

### CDT-8003 — Custom Field Not Available as a Reporting Filter

**Symptoms:** A custom field used consistently on tickets cannot be selected as a filter or grouping option in CloudDesk Analytics.

**Cause:** The field type (e.g., a long free-text field) is not supported for use as a report filter or grouping dimension, since only structured field types (dropdown, tag, numeric) support this.

**Solution:** If reporting on this data is a priority, consider converting the field to a structured type (such as a dropdown) going forward; existing free-text data will not retroactively become filterable.

**Prevention:** Choose structured field types over free text when designing new custom fields, if reporting on that data is anticipated.

**Related Issues:** none

---

### CDT-8004 — Exported Report Missing Recently Resolved Tickets

**Symptoms:** A CSV export of resolved tickets is missing tickets resolved within the last few minutes before export.

**Cause:** A brief indexing delay between a ticket's resolution and its availability in the reporting and export pipeline.

**Solution:** Wait a few minutes and re-run the export if very recent tickets are required; this is typically not an issue for exports covering periods more than an hour in the past.

**Prevention:** For time-sensitive exports, build in a short buffer before generating the report relative to the most recent activity.

**Related Issues:** none

---

## Section 9: Integrations

### CDT-9001 — CRM Sync Creating Duplicate Customer Records

**Symptoms:** The same customer appears as two separate records after CRM integration sync.

**Cause:** The customer's contact information in CloudDesk Tickets and the CRM do not use a consistent matching key (e.g., different email addresses on file), causing the sync to treat them as separate individuals.

**Solution:** Review and merge the duplicate customer records manually under **Admin Dashboard > Data**, and confirm the CRM's matching field configuration under **Admin Dashboard > Integrations**.

**Prevention:** Establish email address as a consistently maintained, unique identifier across both systems where possible.

**Related Issues:** none

---

### CDT-9002 — Project Management Tool Link Not Creating Linked Issue

**Symptoms:** Attempting to link a ticket to a new issue in a connected project management tool fails or does nothing.

**Cause:** The integration's authentication token has expired, or the target project in the external tool was renamed, archived, or deleted.

**Solution:** Reauthorize the integration under **Admin Dashboard > Integrations**, and confirm the target project still exists and is selectable in the current configuration.

**Prevention:** Coordinate with your engineering team before archiving or renaming a project actively used for ticket-to-issue linking.

**Related Issues:** CDT-2002

---

### CDT-9003 — Ticket Tags Not Syncing to Linked Engineering Issue

**Symptoms:** Tags applied to a ticket do not appear on its linked issue in the connected project management tool.

**Cause:** Tag sync is a one-way integration by design (ticket to issue at creation time only) rather than a continuous two-way sync; tags added after the initial link was created do not propagate automatically.

**Solution:** Manually add relevant tags to the external issue if needed after the fact; this is expected behavior given the integration's one-way sync design.

**Prevention:** Apply all relevant tags to a ticket before creating the linked issue, ensuring the initial sync captures complete information.

**Related Issues:** CDT-7003

---

### CDT-9004 — Webhook Delivering Duplicate Events

**Symptoms:** A configured webhook endpoint receives the same ticket event delivered more than once.

**Cause:** The receiving endpoint did not respond with a success status code quickly enough, causing the platform's retry logic to redeliver the event as a precaution.

**Solution:** Ensure your receiving endpoint responds with a success status promptly, and design your endpoint to handle potential duplicate delivery idempotently (e.g., by checking a unique event ID before processing).

**Prevention:** Build webhook consumers to be idempotent by design, since at-least-once delivery is standard behavior for reliable webhook systems generally.

**Related Issues:** none

---

### CDT-9005 — E-Commerce Order Data Not Displaying on Ticket

**Symptoms:** Order history expected to appear alongside a ticket is missing.

**Cause:** The customer's ticket submission email does not exactly match the email on file in the e-commerce platform.

**Solution:** Confirm the email used in the ticket matches the customer's e-commerce account email; this is expected behavior when they differ, such as with a guest checkout.

**Prevention:** Encourage capturing an order number directly via a custom field as a matching fallback independent of email address.

**Related Issues:** none

---

## Section 10: Security and Access

### CDT-10001 — Agent Cannot Delete a Ticket

**Symptoms:** The delete action is unavailable for a ticket an agent believes should be removable.

**Cause:** Ticket deletion is intentionally restricted to the Administrator role by default, distinct from resolution or closing, which agents can perform.

**Solution:** Request the deletion from an administrator, or, if the intent was simply to remove the ticket from an active queue, use **Resolve** or **Close** instead.

**Prevention:** Clarify with your team the distinction between resolving/closing a ticket (routine, agent-level) and deleting one (administrative, exceptional).

**Related Issues:** none

---

### CDT-10002 — SSO Users Unable to See Tickets Assigned Before SSO Was Enabled

**Symptoms:** After enabling SSO, a user cannot see tickets that were previously assigned to their old password-based account.

**Cause:** SSO login created a new user identity rather than linking to the existing account, typically because the email address used for SSO authentication does not exactly match the original account's email.

**Solution:** An administrator should merge the duplicate user records under **Admin Dashboard > Users**, consolidating ticket assignment history under a single identity.

**Prevention:** Confirm SSO-provided email attributes exactly match existing account emails before enforcing SSO account-wide.

**Related Issues:** CDT-10003

---

### CDT-10003 — SCIM Provisioning Not Deactivating Users on Schedule

**Symptoms:** A user removed from the identity provider continues to show as Active in CloudDesk Tickets.

**Cause:** A SCIM sync delay, or the identity provider's offboarding process removed the user from a group without triggering an explicit deprovisioning event recognized by the SCIM integration.

**Solution:** Manually deactivate the user under **Admin Dashboard > Users** as an immediate step, and review your identity provider's offboarding workflow to ensure it triggers a proper deprovisioning event going forward.

**Prevention:** Test your organization's specific offboarding workflow end-to-end against SCIM deprovisioning behavior before relying on it exclusively for access removal.

**Related Issues:** CDT-10002

---

### CDT-10004 — Custom Role Unable to View SLA Data

**Symptoms:** A user with a custom role cannot see SLA countdown indicators on tickets, despite having ticket view permission.

**Cause:** SLA visibility is governed by a separate permission from general ticket view access, and was not included when the custom role was configured.

**Solution:** Add the SLA visibility permission to the custom role under **Admin Dashboard > Roles & Permissions > Custom Roles**.

**Prevention:** Review the full permission matrix, including less obvious granular permissions like SLA visibility, when building a new custom role.

**Related Issues:** none

---

## Section 11: Performance

### CDT-11001 — Ticket Queue Loading Slowly with Large Backlogs

**Symptoms:** A queue view containing a very large number of tickets takes noticeably longer to load than smaller queues.

**Cause:** An unfiltered or broadly filtered view is attempting to render a very large result set at once.

**Solution:** Apply more specific filters (status, priority, date range) to reduce the result set size, and use pagination rather than scrolling through an extremely large unfiltered list.

**Prevention:** Encourage saved views scoped to manageable, relevant subsets of the backlog rather than routinely viewing the full unfiltered queue.

**Related Issues:** none

---

### CDT-11002 — Bulk Action Timing Out on Large Selections

**Symptoms:** A bulk status or tag update fails to complete when applied to a very large number of selected tickets.

**Cause:** The selected batch exceeds the platform's recommended bulk action size for your plan tier, causing the operation to time out before completion.

**Solution:** Break the bulk action into smaller batches, or, for very large operations, use the API (available via CloudDesk API Platform) with appropriate rate-limit-aware batching instead of the UI-based bulk action.

**Prevention:** Review the recommended maximum bulk action size for your plan tier before attempting very large batch operations through the UI.

**Related Issues:** CDT-4005

---

### CDT-11003 — Search Performance Degrading on Very Old Tickets

**Symptoms:** Searching for tickets from several years in the past is noticeably slower than searching recent tickets.

**Cause:** Older data may be stored in a different, less actively cached storage tier as part of standard data lifecycle management, resulting in slightly slower retrieval for infrequently accessed historical records.

**Solution:** This is expected behavior for very old records; no action is needed beyond allowing additional time for historical searches to complete.

**Prevention:** For Enterprise customers with frequent need for fast historical search across long time horizons, discuss data warehouse export as an alternative for deep historical analysis with your Customer Success Manager.

**Related Issues:** none

---

## Section 12: Data Management

### CDT-12001 — Restored Ticket Missing SLA History

**Symptoms:** A ticket restored from **Admin Dashboard > Data > Recently Deleted** no longer shows its original SLA breach or compliance status.

**Cause:** SLA calculation history is recalculated based on current SLA rules at the time of restoration rather than preserved from the original deletion moment, if the underlying SLA rule has since changed.

**Solution:** If historical accuracy for reporting purposes is important, note the discrepancy in an internal record; the restored ticket's live SLA status reflects current rules rather than a frozen historical snapshot.

**Prevention:** Export SLA-relevant reporting data before making significant SLA rule changes, preserving a historical record independent of any single ticket's live recalculated status.

**Related Issues:** CDT-8002

---

### CDT-12002 — Import Failing with Validation Errors

**Symptoms:** A bulk ticket import fails partway through, with some records successfully created and others rejected.

**Cause:** Specific rows in the import file violate field validation rules (e.g., an invalid status value or a malformed date).

**Solution:** Review the import error report, generated automatically after a failed or partial import, to identify and correct the specific rows and fields causing rejection, then re-import only the corrected rows.

**Prevention:** Validate import files against the current field configuration and template before attempting a full import, especially after recent field configuration changes.

**Related Issues:** CDT-7004

---

### CDT-12003 — Data Export Missing Merged Ticket History

**Symptoms:** An export of ticket data does not show the history of tickets that were merged into the exported ticket.

**Cause:** Standard exports include the current, consolidated ticket record but do not expand merged-in ticket history as separate export rows by default.

**Solution:** If full merge history is needed, request a detailed export scope under **Admin Dashboard > Data > Export**, which includes merge history as supplementary data where available on your plan tier.

**Prevention:** Note your organization's reporting requirements around merge history when selecting export scope, since the default scope is optimized for current-state reporting rather than full historical reconstruction.

**Related Issues:** none

---

### CDT-12004 — Unable to Restore a Permanently Removed Customer Record

**Symptoms:** A customer record removed via permanent deletion cannot be recovered, along with its associated ticket history.

**Cause:** Permanent removal is intentionally designed as an irreversible action for data handling compliance purposes, distinct from standard deletion.

**Solution:** This action is not reversible through self-service tools. If the removal was made in error, contact Corvex support to determine whether any options exist within your account's specific data retention configuration.

**Prevention:** Reserve permanent removal for cases where irreversible removal is genuinely intended, such as a specific data handling request; use standard deletion for routine cleanup.

**Related Issues:** none

---

## Section 13: Mobile Access

### CDT-13001 — Tickets Not Syncing to CloudDesk Mobile

**Symptoms:** Recently created or updated tickets do not appear in the CloudDesk Mobile app despite appearing correctly on desktop.

**Cause:** The mobile app has lost its background sync connection, often due to the operating system suspending background network activity to conserve battery.

**Solution:** Manually pull to refresh within the app, or fully close and reopen the app to force a fresh sync. Refer to the CloudDesk Mobile Troubleshooting Guide for device-specific background activity settings.

**Prevention:** Review device battery optimization settings for the CloudDesk Mobile app, ensuring background sync is permitted.

**Related Issues:** none

---

### CDT-13002 — Macro Not Available When Working a Ticket on Mobile

**Symptoms:** A macro available on desktop does not appear as an option when working the same ticket from CloudDesk Mobile.

**Cause:** The macro includes a step type not currently supported on mobile (for example, an advanced multi-condition action), causing it to be filtered from the mobile action list by design.

**Solution:** Complete the affected step from desktop, or simplify the macro's configuration if consistent mobile availability is a priority.

**Prevention:** When designing macros expected to be used from mobile, favor simpler step types with full cross-platform support.

**Related Issues:** none

---

## Section 14: General Behavior and Edge Cases

### CDT-14001 — Ticket Number Sequence Showing a Gap

**Symptoms:** Ticket numbers appear to skip values, with no corresponding ticket found for the missing number.

**Cause:** A ticket was created and then permanently deleted, or a ticket number was allocated to a submission that failed validation before a ticket record was fully created (for example, a spam-filtered web form submission).

**Solution:** This is expected behavior and does not indicate data loss for any ticket that was genuinely completed; sequence numbers are not guaranteed to be perfectly contiguous.

**Prevention:** No action needed; this behavior is inherent to systems that allocate identifiers before full record validation completes.

**Related Issues:** CDT-2003

---

### CDT-14002 — Customer Unable to Reply to Ticket via Email After Resolution

**Symptoms:** A customer's reply to a resolved ticket does not reopen it or does not appear at all.

**Cause:** The ticket was permanently closed (as opposed to resolved) after a configured period, and closed tickets do not accept new replies by design, requiring a new ticket instead.

**Solution:** If the customer's follow-up is a continuation of the same issue, manually link the new ticket to the closed one for context, since closed tickets are not reopened by design.

**Prevention:** Communicate your organization's closed-ticket policy to customers, particularly if a significant delay exists between Resolved and Closed status transitions.

**Related Issues:** CDT-4003

---

### CDT-14003 — Internal Note Formatting Displaying Differently Than Customer Replies

**Symptoms:** Internal notes appear with different formatting options available compared to customer-facing replies.

**Cause:** This is expected behavior; internal notes and customer replies use intentionally distinct composer configurations, since internal notes support certain formatting (such as @mentions) not relevant to customer-facing content.

**Solution:** No action needed; this is a deliberate product distinction rather than a defect.

**Prevention:** Include this distinction in agent onboarding materials to set correct expectations.

**Related Issues:** none

---

### CDT-14004 — Ticket Assigned to a Deactivated User Still Appearing in Their Name

**Symptoms:** A ticket assigned to a since-deactivated agent still displays that agent's name as the current owner.

**Cause:** Deactivating a user does not automatically reassign their open tickets, as described in the CloudDesk Tickets Administrator Guide, since automatic reassignment could route sensitive tickets unpredictably without human review.

**Solution:** An administrator or team lead should manually reassign any open tickets still attributed to the deactivated user.

**Prevention:** Include a review of a departing user's open ticket assignments as a standard step in your offboarding checklist, before or immediately after deactivation.

**Related Issues:** none

---

### CDT-14005 — Saved View Not Reflecting Recent Filter Changes for Other Team Members

**Symptoms:** A shared saved view edited by one team lead does not show the updated filter criteria for other team members using the same saved view.

**Cause:** The edit was saved as a personal copy rather than updating the shared saved view, often because the editor did not have permission to modify the shared version and was instead prompted to save a private copy.

**Solution:** Confirm the editor has permission to modify shared saved views, then reapply the intended changes directly to the shared view rather than a personal copy.

**Prevention:** Restrict shared saved view editing to team leads and administrators, and communicate before making changes that affect the whole team's default view.

**Related Issues:** none

---

*This Troubleshooting Guide covers common CloudDesk Tickets issues and their resolutions. If an issue is not listed here or a documented solution does not resolve your problem, contact Corvex support through the channel appropriate to your plan tier, as described in the Corvex Cloud Pricing Guide.*
