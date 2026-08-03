# CloudDesk Chat
## Troubleshooting Guide

*Corvex Cloud — CloudDesk Chat*
*This guide documents known issues, their causes, and their resolutions for CloudDesk Chat. It is intended for administrators, agents, and technical staff diagnosing problems with the platform. For general usage instructions, refer to the CloudDesk Chat User Manual. For configuration guidance, refer to the CloudDesk Chat Administrator Guide.*

---

## How to Use This Guide

Issues are grouped by category. Each entry includes the symptoms you may observe, the most common underlying cause, a recommended solution, steps to prevent recurrence, and related issues you may want to review if the listed solution does not fully resolve your problem.

---

## Section 1: Installation and Widget Setup

### CDW-1001 — Widget Not Appearing on Website

**Symptoms:** The CloudDesk Chat widget does not appear on any page of the website after installation.

**Cause:** The installation snippet was not added to the site, was added incorrectly, or is blocked by a content security policy (CSP) that does not permit scripts from Corvex-hosted domains.

**Solution:** Confirm the snippet is present immediately before the closing `</body>` tag on the affected pages. If your site enforces a CSP, add the required Corvex Cloud domains to your `script-src` and `connect-src` directives, as listed in the widget installation instructions in the Admin Dashboard.

**Prevention:** Use the **Verify Installation** tool in **Settings > Chat Widget > Installation** immediately after publishing snippet changes, rather than assuming success.

**Related Issues:** CDW-1002, CDW-1003, CDW-1010

---

### CDW-1002 — Widget Appears on Some Pages but Not Others

**Symptoms:** The widget loads correctly on the homepage but is missing on other pages of the site.

**Cause:** The installation snippet was added to a page-specific template rather than a shared site-wide template or footer.

**Solution:** Move the snippet into a shared layout component, master template, or global footer that renders on every page where the widget should appear.

**Prevention:** When installing on multi-template sites (e.g., separate templates for product pages, blog, and checkout), confirm with your web team which shared component reliably renders across all intended page types before installation.

**Related Issues:** CDW-1001, CDW-1004

---

### CDW-1003 — Verification Fails Despite Snippet Being Present

**Symptoms:** The **Verify Installation** check returns a failure even though the snippet appears correctly in the page source.

**Cause:** The verification check timed out due to slow page load, or an ad blocker/privacy extension on the verifying browser blocked the widget's outbound request.

**Solution:** Retry verification from a browser without ad-blocking extensions enabled, or wait a few minutes for page caching (if using a CDN) to refresh before retrying.

**Prevention:** When testing installation, use a clean browser profile or incognito/private window without extensions to avoid false negatives during verification.

**Related Issues:** CDW-1001, CDW-1015

---

### CDW-1004 — Widget Loads Twice on the Same Page

**Symptoms:** Two identical chat widget bubbles appear on a single page.

**Cause:** The installation snippet was added in more than one location — for example, both a page-specific template and a shared global footer.

**Solution:** Search the site's codebase or CMS for all instances of the widget snippet and remove all but one.

**Prevention:** Maintain a single documented source of truth for where the snippet lives, and note it in your internal deployment documentation to prevent future duplicate additions.

**Related Issues:** CDW-1002

---

### CDW-1005 — Pre-Chat Form Not Displaying

**Symptoms:** Visitors can open the chat widget and message an agent directly, without being prompted to complete the configured pre-chat form.

**Cause:** The pre-chat form was disabled, saved as a draft rather than published, or the widget being displayed is a cached older version.

**Solution:** Confirm the pre-chat form toggle is enabled and published under **Settings > Chat Widget > Pre-Chat Form**, then clear browser and CDN caches before retesting.

**Prevention:** After any pre-chat form change, use a private browser window to confirm the change is live before considering the update complete.

**Related Issues:** CDW-1006, CDW-1023

---

### CDW-1006 — Pre-Chat Form Fields Not Saving Submitted Data

**Symptoms:** Visitors complete the pre-chat form, but the submitted information does not appear in the resulting conversation's customer context panel.

**Cause:** A custom field was renamed or deleted after conversations referencing the old field name were already in progress, or a required field's internal identifier was changed without updating the widget configuration.

**Solution:** Avoid renaming or deleting active custom fields. If a field must change, create a new field rather than editing an existing one, and update your form configuration accordingly.

**Prevention:** Treat published custom field identifiers as stable once in use; make cosmetic label changes only, and create new fields for structural changes.

**Related Issues:** CDW-1005

---

### CDW-1007 — Widget Branding Not Matching Configuration

**Symptoms:** The live widget shows default colors or a missing logo despite branding being configured in the Admin Dashboard.

**Cause:** Browser or CDN caching is serving a previous version of the widget assets.

**Solution:** Clear your CDN cache (if applicable) and instruct testers to use a private browser window. Widget branding changes typically propagate within a few minutes once caching is cleared.

**Prevention:** Build a brief cache-clearing step into your standard process for any widget appearance change.

**Related Issues:** CDW-1003

---

### CDW-1008 — Mobile SDK Fails to Initialize

**Symptoms:** The embedded chat widget does not load within the organization's own iOS or Android app using the CloudDesk Chat mobile SDK.

**Cause:** An invalid or expired SDK configuration key, or a mismatch between the SDK version integrated and the minimum supported version for the account's plan.

**Solution:** Confirm the SDK configuration key in your app matches the current key issued under **Settings > Chat Widget > Mobile SDK**, and verify your integrated SDK version against the current minimum supported version in the developer documentation.

**Prevention:** Subscribe to SDK release notifications in the developer documentation portal to stay ahead of minimum version changes.

**Related Issues:** CDW-1009, CDW-6002

---

### CDW-1009 — Mobile SDK Widget Displays but Cannot Send Messages

**Symptoms:** The embedded mobile widget renders correctly but messages fail to send, typically with a generic error in the app.

**Cause:** The host app's network configuration is blocking outbound requests to Corvex Cloud's real-time messaging endpoints, often due to an overly restrictive network security configuration on Android or App Transport Security exception missing on iOS.

**Solution:** Review your app's network security configuration to permit connections to the domains listed in the CloudDesk Chat mobile SDK documentation.

**Prevention:** Include the required domain allowlist as a standard step in your SDK integration checklist for future app updates.

**Related Issues:** CDW-1008, CDW-3004

---

### CDW-1010 — Content Security Policy Blocking Widget Scripts

**Symptoms:** Browser console shows CSP violation errors referencing Corvex Cloud domains; the widget fails to load.

**Cause:** The site's Content-Security-Policy header does not include the domains required by the CloudDesk Chat widget.

**Solution:** Add the required domains to the appropriate CSP directives (`script-src`, `connect-src`, `frame-src`, `style-src`) as documented in the widget installation guide.

**Prevention:** Review CSP compatibility as a standard step before installing the widget on any site with an existing strict CSP.

**Related Issues:** CDW-1001

---

## Section 2: Widget Display and Behavior

### CDW-2001 — Widget Bubble Overlaps Other Page Elements

**Symptoms:** The chat bubble visually overlaps a footer element, cookie consent banner, or other fixed-position page element.

**Cause:** A z-index or positioning conflict between the widget and another fixed or sticky element on the page.

**Solution:** Adjust the widget's position offset under **Settings > Chat Widget > Appearance > Position Offset**, or adjust the conflicting element's z-index in your site's CSS.

**Prevention:** Test widget placement against all fixed-position page elements (cookie banners, sticky headers/footers) as part of installation on any new page template.

**Related Issues:** CDW-2002

---

### CDW-2002 — Widget Not Responsive on Mobile Browsers

**Symptoms:** The widget displays correctly on desktop but appears cut off or improperly sized on mobile web browsers.

**Cause:** A custom CSS override applied to the page is conflicting with the widget's responsive styling.

**Solution:** Review any custom CSS applied to the page for rules unintentionally targeting the widget's container elements, and scope custom styles more narrowly.

**Prevention:** When applying broad CSS rules (e.g., targeting all `div` or `iframe` elements sitewide), explicitly exclude the widget's container class.

**Related Issues:** CDW-2001

---

### CDW-2003 — Offline Message Not Displaying Outside Business Hours

**Symptoms:** Visitors see an empty or default chat window instead of the configured offline message when no agents are available.

**Cause:** Business hours were not configured, or the configured time zone does not match the organization's intended reference time zone.

**Solution:** Confirm business hours and time zone are correctly set under **Settings > Chat Widget > Routing > Availability**, and that an offline message has been published.

**Prevention:** Review business hours configuration after any daylight saving time transition or office relocation affecting your organization's primary time zone.

**Related Issues:** CDW-3005

---

### CDW-2004 — Widget Greeting Message Not Updating

**Symptoms:** A newly edited greeting message does not appear to visitors after being saved.

**Cause:** The greeting message change was saved as a draft, or the change targets a widget variant not currently published as live.

**Solution:** Confirm the change was published, not just saved, under **Settings > Chat Widget > Appearance**, and confirm you are editing the correct widget if your account has more than one configured.

**Prevention:** When managing multiple widgets, adopt a clear naming convention to avoid editing the wrong one.

**Related Issues:** CDW-1007

---

### CDW-2005 — Multi-Language Widget Displaying Wrong Language

**Symptoms:** Visitors see the widget in the account's default language rather than their browser or page-configured language.

**Cause:** Language detection is based on a page-level language attribute (`lang` in HTML) that is missing or incorrectly set, or the visitor's language is not among the configured supported languages.

**Solution:** Confirm the site's `<html lang="...">` attribute is correctly set per page, and confirm the visitor's language is included under **Settings > Chat Widget > Languages** (up to 5 languages on Professional, unlimited on Enterprise).

**Prevention:** Include the `lang` attribute as a standard requirement in your site's page template documentation.

**Related Issues:** CDW-2006

---

### CDW-2006 — Translated Content Displaying Incorrectly

**Symptoms:** Canned responses or the pre-chat form display partially translated or garbled text in a non-default language.

**Cause:** A translation was not provided for a specific field, causing a fallback that mixes default and translated content, or special characters were not properly encoded when the translation was entered.

**Solution:** Review the affected content under **Settings > Chat Widget > Languages** and ensure all fields have complete translations entered using UTF-8 compatible input.

**Prevention:** Use a translation review checklist covering every configurable text field before publishing a new supported language.

**Related Issues:** CDW-2005

---

## Section 3: Connectivity and Real-Time Messaging

### CDW-3001 — Agent Not Receiving New Chat Notifications

**Symptoms:** New conversations arrive in the queue but the agent does not see a desktop notification or sound alert.

**Cause:** Browser-level notification permissions were denied, or the agent's individual notification preferences were disabled under **My Settings > Notifications**.

**Solution:** Confirm browser notification permissions are granted for the CloudDesk Chat domain, and confirm desktop and sound notification toggles are enabled in the agent's personal settings.

**Prevention:** Include notification permission setup as a standard step in new agent onboarding.

**Related Issues:** CDW-3002, CDW-7001

---

### CDW-3002 — Delayed Message Delivery in Active Conversations

**Symptoms:** Messages sent by an agent or customer take an unusually long time (more than a few seconds) to appear on the other side.

**Cause:** An unstable network connection on either party's side, or an active browser tab in the background being deprioritized by the operating system's power-saving behavior.

**Solution:** Ask the affected party to check their network connection, and, for agents, keep the CloudDesk Chat tab active or use desktop notifications to avoid tab throttling delaying real-time updates.

**Prevention:** For agents on laptops, disable aggressive battery-saving or tab-throttling settings in the browser while actively working conversations.

**Related Issues:** CDW-3003

---

### CDW-3003 — Conversation Appears Frozen or Unresponsive

**Symptoms:** The active conversation panel stops updating; new messages do not appear until the page is manually refreshed.

**Cause:** The real-time connection (WebSocket) was silently dropped, often due to a corporate proxy or firewall terminating long-lived connections after a period of inactivity.

**Solution:** Refresh the page to reestablish the connection. If this occurs frequently on a specific network, work with your IT team to allow long-lived WebSocket connections to Corvex Cloud domains through your proxy or firewall.

**Prevention:** Share the required domain and port allowlist from the developer documentation with your network team when deploying CloudDesk Chat broadly across a corporate network.

**Related Issues:** CDW-3002, CDW-3004

---

### CDW-3004 — Widget Fails to Connect from Visitor's Browser

**Symptoms:** A visitor reports the chat widget shows a persistent "Connecting..." state and never becomes usable.

**Cause:** The visitor's network (often a restrictive corporate or public Wi-Fi network) is blocking the WebSocket connection required for real-time messaging.

**Solution:** Advise the visitor to try a different network if possible. On your end, confirm the widget correctly falls back to a polling-based connection method when WebSocket is unavailable, under **Settings > Chat Widget > Advanced > Connection Fallback**.

**Prevention:** Enable connection fallback for widgets deployed on sites with a broad, unpredictable visitor network profile.

**Related Issues:** CDW-3003

---

### CDW-3005 — Availability Status Not Updating Routing Behavior

**Symptoms:** An agent set their status to Away, but new conversations continue to be routed to them.

**Cause:** A browser tab left open in a different window is holding an active session with a stale Available status that has not yet synced, or a routing rule is configured to ignore individual availability status for a specific team.

**Solution:** Close duplicate open sessions in other tabs or windows, and confirm the relevant routing rule's availability behavior under **Settings > Chat Widget > Routing**.

**Prevention:** Encourage agents to work from a single browser tab/window per session to avoid state synchronization conflicts.

**Related Issues:** CDW-2003, CDW-4001

---

### CDW-3006 — Typing Indicator Not Displaying

**Symptoms:** Neither party sees the "is typing..." indicator during an active conversation, even though both are actively composing messages.

**Cause:** A degraded real-time connection is delivering standard messages but dropping lower-priority presence signals such as typing indicators.

**Solution:** This typically resolves once full connectivity is restored; if it persists, refresh the page to reestablish a clean connection.

**Prevention:** No specific preventive action is available for this cosmetic, connection-quality-dependent behavior; it does not affect message delivery reliability.

**Related Issues:** CDW-3002

---

## Section 4: Routing and Assignment

### CDW-4001 — Conversations Not Routing to the Correct Team

**Symptoms:** New conversations are routed to a general queue instead of the specific team configured to handle them.

**Cause:** A routing rule's conditions (such as a required skill tag or pre-chat form response) do not match the actual data being submitted, often due to a recent pre-chat form field change.

**Solution:** Review the routing rule's conditions under **Settings > Chat Widget > Routing** against the current pre-chat form field configuration, and adjust the rule to match current field names and expected values.

**Prevention:** When modifying pre-chat form fields, review dependent routing rules in the same change, rather than as a separate, easily forgotten step.

**Related Issues:** CDW-1006, CDW-4002

---

### CDW-4002 — Round-Robin Assignment Skewing Toward One Agent

**Symptoms:** One agent on a team consistently receives significantly more conversations than teammates under round-robin routing.

**Cause:** The affected agent has a longer average session duration (staying logged in and Available longer than others), which increases their share under a purely availability-weighted round-robin algorithm, or another agent's status is incorrectly stuck as Away.

**Solution:** Review team member availability status accuracy under **Team Queue**, and confirm the round-robin configuration's weighting behavior matches your team's intended distribution model.

**Prevention:** Periodically review assignment distribution reporting in CloudDesk Analytics to catch skew early.

**Related Issues:** CDW-3005, CDW-4003

---

### CDW-4003 — Conversation Stuck in Unassigned Queue

**Symptoms:** A conversation remains unassigned despite available agents matching its routing criteria.

**Cause:** No routing rule matches the conversation's specific combination of conditions, causing it to fall through to a default unassigned state without a configured fallback rule.

**Solution:** Add a fallback routing rule to catch conversations that don't match any specific condition, ensuring every conversation has a defined assignment path.

**Prevention:** Always configure a fallback/catch-all routing rule as the last rule in your routing configuration.

**Related Issues:** CDW-4001

---

### CDW-4004 — Transferred Conversation Loses Context

**Symptoms:** After a conversation is transferred to another agent, the receiving agent does not see prior message history or internal notes.

**Cause:** The conversation was transferred as a new conversation rather than using the **Transfer Conversation** function, often due to the customer starting a new chat session instead of continuing the existing one.

**Solution:** Confirm agents are using the in-app **Transfer Conversation** action rather than asking the customer to start a new chat. If context is genuinely missing after a proper transfer, check the customer context panel, which retains full history independent of the transfer action itself.

**Prevention:** Include correct transfer procedure in agent onboarding and reference materials.

**Related Issues:** none

---

### CDW-4005 — Skill-Based Routing Not Matching Agents Correctly

**Symptoms:** A conversation tagged with a specific skill requirement is not routed to any agent with that skill.

**Cause:** No currently available agent has been assigned the required skill tag under their user profile, or the skill tag on the routing rule does not exactly match the skill tag assigned to agents (case sensitivity or a trailing space, for example).

**Solution:** Review agent skill tag assignments under **Admin Dashboard > Users**, and confirm exact matching with the routing rule's configured skill tag.

**Prevention:** Maintain a documented, centrally managed list of valid skill tags to avoid inconsistent tagging across configuration screens.

**Related Issues:** CDW-4001

---

### CDW-4006 — Priority Routing Not Escalating VIP Customers

**Symptoms:** A returning customer expected to receive priority routing (based on CRM data such as account tier) is routed through standard queue logic instead.

**Cause:** The CRM integration providing account tier data is not currently syncing correctly, or the priority routing rule's condition references an outdated CRM field name.

**Solution:** Check integration health under **Admin Dashboard > Integrations**, and confirm the routing rule's field reference matches the current CRM integration's field mapping.

**Prevention:** Review priority routing rules whenever the CRM integration's field mappings are updated.

**Related Issues:** CDW-6001, CDW-6002

---

## Section 5: Notifications

### CDW-5001 — Email Digest Not Being Received

**Symptoms:** An agent who enabled the optional email digest of missed conversations is not receiving it.

**Cause:** The digest email is being filtered to spam/junk by the recipient's email provider, or the digest schedule was set to a frequency the agent doesn't expect (e.g., weekly instead of daily).

**Solution:** Confirm the digest schedule under **My Settings > Notifications**, and ask the agent to check spam/junk folders and mark Corvex Cloud email as safe.

**Prevention:** Provide new agents with recommended email allowlist entries during onboarding.

**Related Issues:** none

---

### CDW-5002 — SLA Breach Alert Not Firing

**Symptoms:** A conversation exceeds its configured response time target without triggering an alert to the team lead.

**Cause:** SLA breach alerting was not enabled for the specific team or routing path the conversation followed, or the recipient's notification preferences have breach alerts disabled.

**Solution:** Confirm SLA breach alerting is enabled under the relevant workflow configuration and that the intended recipient has breach alert notifications enabled in their personal settings.

**Prevention:** Include SLA alert configuration review as part of onboarding any new team or routing path.

**Related Issues:** CDW-5003

---

### CDW-5003 — Duplicate SLA Alerts for the Same Conversation

**Symptoms:** A team lead receives multiple notifications for the same SLA breach.

**Cause:** Overlapping SLA rules (for example, both a team-level and an account-wide rule) are both configured to alert the same recipient for the same condition.

**Solution:** Review SLA rule configuration for overlapping conditions and consolidate or scope rules more specifically to avoid duplicate triggers.

**Prevention:** Maintain a single, clearly scoped SLA rule per priority level and team combination rather than layering multiple overlapping rules.

**Related Issues:** CDW-5002

---

### CDW-5004 — Mobile Push Notifications Delayed or Missing

**Symptoms:** An agent using CloudDesk Mobile does not receive timely push notifications for new assignments.

**Cause:** Device-level battery optimization settings are restricting background app activity, or the device's notification permissions for the app were revoked.

**Solution:** Review device-level notification and battery optimization settings for the CloudDesk Mobile app, ensuring background activity and notifications are permitted. Refer to the CloudDesk Mobile Troubleshooting Guide for device-specific steps.

**Prevention:** Include device notification permission setup as a standard step when onboarding agents to mobile access.

**Related Issues:** CDW-3001

---

### CDW-5005 — Threshold Alert Firing Too Frequently

**Symptoms:** A team lead receives an excessive number of threshold-based alerts, reducing their usefulness.

**Cause:** The configured threshold is too close to normal operating conditions, causing routine fluctuation to repeatedly cross the alert boundary.

**Solution:** Adjust the threshold value under the relevant alert configuration in CloudDesk Analytics to better reflect a genuinely actionable condition rather than normal variance.

**Prevention:** When first configuring a threshold alert, observe typical metric behavior for a week or two before finalizing the threshold value.

**Related Issues:** CDW-5002

---

## Section 6: Canned Responses and Macros

### CDW-6001 — Canned Response Not Appearing in Composer

**Symptoms:** A canned response created by an administrator is not visible to agents when typing `/` in the message composer.

**Cause:** The canned response was saved but not assigned to the team or role the agent belongs to, or it remains in draft status.

**Solution:** Confirm the canned response is published and correctly scoped to the relevant team(s) under **Settings > Canned Responses**.

**Prevention:** Establish a standard scoping convention (e.g., always assign new canned responses to "All Teams" unless deliberately restricted) to avoid accidental omissions.

**Related Issues:** CDW-6002

---

### CDW-6002 — Canned Response Inserting Broken Placeholder Text

**Symptoms:** A canned response containing a dynamic placeholder (such as customer name) inserts literal placeholder syntax instead of the actual value.

**Cause:** The conversation lacks the underlying data field the placeholder references — for example, a customer name field left blank because the pre-chat form was skipped or the field is optional.

**Solution:** Add a fallback default value to the placeholder configuration under **Settings > Canned Responses**, so it degrades gracefully (e.g., "there" instead of a broken tag) when the underlying data is missing.

**Prevention:** Design canned responses using placeholders only for fields that are reliably populated, or always configure a fallback value.

**Related Issues:** CDW-1006

---

### CDW-6003 — Personal Canned Response Not Syncing Across Devices

**Symptoms:** An agent's personally created canned response is visible on desktop but not on CloudDesk Mobile, or vice versa.

**Cause:** A temporary sync delay, or the canned response was created while the device was offline and has not yet synced to the account.

**Solution:** Ensure both devices have an active connection and allow a brief period for sync; if the issue persists beyond a few minutes, log out and back in on the affected device to force a full resync.

**Prevention:** Avoid creating personal canned responses while offline when possible.

**Related Issues:** none

---

### CDW-6004 — Macro Applying Incorrect Tag or Status

**Symptoms:** Running a macro results in an unexpected tag or status being applied to the ticket, different from what the macro was configured to do.

**Cause:** The macro was edited after initial creation and the change was not communicated to agents relying on its previous, different behavior.

**Solution:** Review the macro's current configuration under **Settings > Macros** and confirm it matches the intended behavior; communicate any recent changes to the affected team.

**Prevention:** Maintain a changelog or notification process for macro edits, since macros are shared, reusable configuration that affects all users relying on them.

**Related Issues:** none

---

## Section 7: Conversation Management

### CDW-7001 — Unable to Reply to a Conversation

**Symptoms:** The message composer is grayed out or reply attempts silently fail in an otherwise normal-looking conversation.

**Cause:** The conversation has already been marked as Resolved or Closed by another agent, and the interface has not yet visually refreshed to reflect the new status.

**Solution:** Refresh the page to confirm the current status; if a reply is still needed, reopen the conversation before continuing.

**Prevention:** Use internal notes to communicate handoff intentions when multiple agents may be working related conversations, reducing conflicting simultaneous actions.

**Related Issues:** CDW-3001

---

### CDW-7002 — Internal Note Visible to Customer

**Symptoms:** A customer references content from what an agent believed was a private internal note.

**Cause:** The agent used the standard reply composer instead of the internal note composer, which are visually similar but functionally distinct.

**Solution:** Review agent training on the visual distinction between the reply and internal note composers (typically differentiated by background color). There is no way to retract a message already delivered to the customer; if sensitive information was disclosed, follow your organization's internal incident process.

**Prevention:** Reinforce the visual distinction during onboarding, and consider enabling the optional confirmation prompt for internal notes under **My Settings**.

**Related Issues:** none

---

### CDW-7003 — Customer Context Panel Showing Outdated Information

**Symptoms:** The customer context panel displays stale order or account information that doesn't match what the customer describes.

**Cause:** The connected CRM or e-commerce integration has not synced recently, often due to a temporary integration failure.

**Solution:** Check integration health under **Admin Dashboard > Integrations**; if a specific integration shows a Warning or Error status, review its configuration or reauthorize the connection.

**Prevention:** Enable integration health alerts so administrators are notified promptly when a sync begins failing, rather than discovering it through agent reports.

**Related Issues:** CDW-9001, CDW-9002

---

### CDW-7004 — Duplicate Conversations for the Same Customer Issue

**Symptoms:** A customer's issue appears as two separate active conversations rather than one continuous thread.

**Cause:** The customer opened a new chat session instead of returning to their existing conversation, often because they closed their browser or cleared cookies between sessions.

**Solution:** Manually merge context by referencing the customer's history in the context panel, and resolve the duplicate conversation with a note pointing to the active one. Native chat-to-chat merging is not currently supported; converting to a ticket, where merge is supported, is an option for ongoing multi-session issues.

**Prevention:** Encourage returning customers to use any "continue previous chat" prompt the widget offers when it detects a returning visitor with a recent open conversation.

**Related Issues:** none

---

### CDW-7005 — Tag Not Appearing in Search or Filter Results

**Symptoms:** A tag applied to a conversation does not appear when filtering or searching by that tag.

**Cause:** A search index sync delay, typically resolving within a few minutes, or the tag was applied with inconsistent capitalization creating what the system treats as two distinct tags.

**Solution:** Wait a few minutes and retry; if the issue persists, review the tag list under **Settings > Tags** for near-duplicate entries with inconsistent capitalization and consolidate them.

**Prevention:** Restrict tag creation to administrators, or enable tag suggestion/autocomplete to reduce inconsistent manual entry.

**Related Issues:** none

---

### CDW-7006 — Conversation Export Missing Expected Data

**Symptoms:** A CSV export of conversation data is missing fields expected to be present, such as custom pre-chat form responses.

**Cause:** The export template used does not include the specific custom field, since export templates default to a standard field set.

**Solution:** Customize the export field selection under **Admin Dashboard > Data > Export** to include the specific custom fields needed before generating the export.

**Prevention:** Save a custom export template with your organization's commonly needed fields to avoid reconfiguring on each export.

**Related Issues:** none

---

## Section 8: Integrations

### CDW-8001 — CRM Integration Showing "Error" Status

**Symptoms:** The Integrations page displays an Error status for a previously working CRM connection.

**Cause:** The CRM's authentication token has expired or been revoked, often due to a password change or security policy change on the CRM side.

**Solution:** Navigate to **Admin Dashboard > Integrations**, select the affected CRM, and reauthorize the connection following the guided flow.

**Prevention:** Use a dedicated service account for the CRM integration where supported, rather than an individual employee's credentials, to avoid disruption from personal password changes.

**Related Issues:** CDW-7003, CDW-8002

---

### CDW-8002 — E-Commerce Order Data Not Displaying in Conversations

**Symptoms:** Order history that should appear in the customer context panel is missing for a specific customer.

**Cause:** The customer's chat session email does not exactly match the email on file in the e-commerce platform, preventing the integration from matching records.

**Solution:** Confirm the customer's email used in the chat session matches their e-commerce account email; if it differs (e.g., a guest checkout with a different email), this is expected behavior given identity matching by email.

**Prevention:** Encourage use of pre-chat form fields that capture order number directly, providing a matching fallback independent of email address.

**Related Issues:** CDW-7003

---

### CDW-8003 — Zapier Connection Not Triggering

**Symptoms:** A configured Zapier automation (e.g., posting new conversations to a spreadsheet) is not firing as expected.

**Cause:** The Zapier API key was regenerated in CloudDesk Chat, invalidating the previously connected Zap without updating it, or the specific trigger event was disabled during a recent Zap edit.

**Solution:** Confirm the current API key in Zapier matches the key shown under **Admin Dashboard > Integrations > Zapier**, and confirm the Zap's trigger step is enabled and correctly configured.

**Prevention:** Avoid regenerating API keys used by active Zaps unless necessary; if regeneration is required, update all dependent Zaps in the same change window.

**Related Issues:** CDW-8004

---

### CDW-8004 — Webhook Not Delivering Events

**Symptoms:** A configured webhook endpoint is not receiving expected event payloads.

**Cause:** The receiving endpoint's URL changed without updating the webhook configuration, or the endpoint is returning a non-success HTTP status code, causing Corvex to treat delivery as failed.

**Solution:** Review delivery attempt history and response codes under the CloudDesk API Platform Developer Portal, and confirm the endpoint URL and its response behavior are correct.

**Prevention:** Monitor webhook delivery health regularly rather than only after a downstream process is noticed to be failing.

**Related Issues:** CDW-8003

---

### CDW-8005 — Collaboration Tool Alerts Not Posting

**Symptoms:** SLA breach or escalation alerts configured to post to a team messaging channel are not appearing.

**Cause:** The collaboration tool integration's authentication token expired, or the target channel was renamed or deleted after the integration was configured.

**Solution:** Reauthorize the collaboration tool integration under **Admin Dashboard > Integrations**, and reselect a valid target channel.

**Prevention:** Coordinate with your collaboration tool administrators before renaming or archiving channels used by active integrations.

**Related Issues:** CDW-5002

---

### CDW-8006 — SSO Login Failing After Integration Configured Correctly

**Symptoms:** Users attempting to log in via SSO receive an error, despite the SSO configuration appearing correct in the Admin Dashboard.

**Cause:** A certificate used by the identity provider has expired, or the attribute mapping (e.g., email field) no longer matches what the identity provider is sending.

**Solution:** Review the identity provider's current metadata and certificate status, and re-verify attribute mapping under **Admin Dashboard > Security > Single Sign-On** using the test login flow.

**Prevention:** Track your identity provider's certificate expiration date and renew or update the SAML configuration proactively before expiration.

**Related Issues:** CDW-10001

---

## Section 9: Reporting and Analytics

### CDW-9001 — Real-Time Dashboard Showing Incorrect Queue Count

**Symptoms:** The real-time dashboard displays a different number of active conversations than what appears in the Conversation List.

**Cause:** A brief synchronization delay between the real-time aggregation layer and the underlying case data, typically resolving within seconds to a couple of minutes.

**Solution:** Refresh the dashboard; if the discrepancy persists beyond several minutes, contact Corvex support, as this may indicate a service degradation.

**Prevention:** No specific preventive action is available for this transient synchronization behavior.

**Related Issues:** none

---

### CDW-9002 — CSAT Survey Response Rate Appears Unusually Low

**Symptoms:** Reported CSAT survey response rates drop significantly compared to historical norms.

**Cause:** A recent widget update inadvertently disabled the post-conversation survey trigger, or the survey delivery method (in-widget vs. follow-up email) was changed without an equivalent audience able to respond.

**Solution:** Confirm CSAT survey settings are enabled and correctly configured under **Settings > Chat Widget > Surveys**, reviewing any recent configuration changes around the time the drop began.

**Prevention:** Monitor survey response rate as a tracked metric, so unexpected drops are caught quickly rather than discovered later during a broader review.

**Related Issues:** none

---

### CDW-9003 — Custom Dashboard Widget Showing "No Data"

**Symptoms:** A specific widget on a custom dashboard displays no data, while other widgets on the same dashboard populate normally.

**Cause:** The widget's filter configuration (e.g., a specific tag or team) does not match any data in the selected date range.

**Solution:** Review the individual widget's filter configuration for overly narrow or outdated conditions, adjusting or removing filters as needed.

**Prevention:** When building dashboards, test each widget individually with a broad date range before narrowing filters, to confirm the underlying data exists before adding constraints.

**Related Issues:** none

---

### CDW-9004 — Scheduled Report Not Being Delivered

**Symptoms:** A scheduled report configured for email delivery is not arriving for recipients.

**Cause:** The recipient's email address was removed from the account (e.g., due to deactivation), or delivery is being filtered as spam by the recipient's email system.

**Solution:** Confirm the recipient list under **Settings > Reports > Scheduled Delivery** includes current, active email addresses, and ask recipients to check spam/junk folders.

**Prevention:** Review scheduled delivery recipient lists periodically, particularly after any team personnel changes.

**Related Issues:** CDW-5001

---

## Section 10: Security and Access

### CDW-10001 — User Unable to Log In Despite Correct Credentials

**Symptoms:** A user receives an "invalid credentials" error despite being confident their password is correct.

**Cause:** The account was recently deactivated, the password was recently reset by an administrator without the user being informed, or the account is configured for SSO-only login and the user is attempting standard password login.

**Solution:** Confirm the user's account status and login method under **Admin Dashboard > Users**, and direct the user to the correct login method (SSO vs. password) accordingly.

**Prevention:** Communicate clearly with users when SSO is newly enforced account-wide, since password login will no longer function for affected accounts.

**Related Issues:** CDW-8006

---

### CDW-10002 — IP Allowlisting Blocking Legitimate Access

**Symptoms:** A user working from a new location (e.g., traveling, a new office, or a new VPN endpoint) is unable to access CloudDesk Chat.

**Cause:** The user's current IP address is not included in the account's configured IP allowlist.

**Solution:** An administrator should add the new IP range under **Admin Dashboard > Security > IP Allowlisting**, or provide a temporary exception if the access is short-term.

**Prevention:** Maintain a process for quickly reviewing and approving new IP ranges, particularly for organizations with distributed or traveling staff.

**Related Issues:** none

---

### CDW-10003 — Session Timing Out More Frequently Than Expected

**Symptoms:** Agents are logged out and required to re-authenticate more often than the configured session timeout would suggest.

**Cause:** The organization's identity provider (if using SSO) enforces its own, shorter session policy that overrides the CloudDesk Chat-configured timeout.

**Solution:** Review session timeout settings on both the CloudDesk Chat Admin Dashboard and the identity provider's own session policy configuration, since the shorter of the two effectively governs actual session duration.

**Prevention:** Align session timeout expectations between IT/security teams managing the identity provider and the CloudDesk Chat administrator during initial SSO setup.

**Related Issues:** CDW-8006

---

### CDW-10004 — Custom Role Missing Expected Permissions

**Symptoms:** A user assigned a custom role cannot perform an action expected to be included in that role's configuration.

**Cause:** The specific permission was not included when the custom role was originally built, or a related permission it depends on (e.g., view access as a prerequisite for edit access) was not also granted.

**Solution:** Review the custom role's full permission set under **Admin Dashboard > Roles & Permissions > Custom Roles**, checking for both the specific permission and any prerequisite permissions it depends on.

**Prevention:** Use the permission matrix view to review a new custom role's full configuration before assigning it to users, rather than testing permission-by-permission after deployment.

**Related Issues:** none

---

### CDW-10005 — Audit Log Missing an Expected Entry

**Symptoms:** An administrator cannot find a record of a specific configuration change in the audit log.

**Cause:** The change occurred outside the account's current audit log retention window (90 days on Professional; extended on Enterprise), or the action falls outside the categories of actions currently logged.

**Solution:** Confirm the date of the change against your plan's retention window; if within the window and still missing, contact Corvex support to investigate, as this may indicate a logging gap requiring escalation.

**Prevention:** Export audit logs periodically for long-term retention beyond the platform's built-in window if your organization requires longer historical records.

**Related Issues:** none

---

## Section 11: Performance

### CDW-11001 — Agent Workspace Loading Slowly

**Symptoms:** The agent workspace takes noticeably longer than usual to load conversations or switch between them.

**Cause:** A high number of browser extensions running simultaneously, an outdated browser version, or an unusually large number of open conversations being rendered at once.

**Solution:** Disable non-essential browser extensions, update to a current browser version, and use filters to reduce the number of conversations loaded in a single view.

**Prevention:** Recommend a standard, extension-minimal browser profile for agent workstations.

**Related Issues:** CDW-11002

---

### CDW-11002 — High Latency During Peak Traffic Periods

**Symptoms:** Message delivery and page responsiveness noticeably degrade during known high-traffic periods (e.g., a sales event).

**Cause:** A sharp, unplanned spike in concurrent conversations relative to typical account usage.

**Solution:** If a high-traffic event is planned in advance, contact Corvex Customer Success ahead of time so infrastructure capacity can be reviewed for your account, particularly on Enterprise plans with dedicated infrastructure options.

**Prevention:** Establish a standing practice of notifying Corvex ahead of known seasonal or promotional traffic spikes.

**Related Issues:** CDW-3002

---

### CDW-11003 — Search Returning Slow or Incomplete Results

**Symptoms:** Searching for a customer or conversation takes an unusually long time or returns incomplete results.

**Cause:** A very broad search term combined with a large historical data volume, or a temporary search index synchronization delay following a bulk data import.

**Solution:** Narrow search terms and apply filters to reduce the result set size; if a bulk import occurred recently, allow additional time for indexing to complete.

**Prevention:** Schedule bulk data imports during lower-traffic periods and communicate expected temporary search delays to the team in advance.

**Related Issues:** CDW-7005

---

### CDW-11004 — Widget Slowing Down Overall Page Load Time

**Symptoms:** Website performance monitoring shows a measurable increase in page load time attributable to the chat widget script.

**Cause:** The widget snippet is loaded synchronously and blocking, rather than using the recommended asynchronous loading pattern.

**Solution:** Confirm the installation snippet matches the current recommended asynchronous loading pattern provided under **Settings > Chat Widget > Installation**; older synchronous snippets should be replaced.

**Prevention:** Periodically compare your installed snippet against the current recommended version, particularly after platform updates are announced.

**Related Issues:** CDW-1001

---

## Section 12: Billing and Account

### CDW-12001 — Seat Count Discrepancy Between Admin Dashboard and Invoice

**Symptoms:** The number of active seats shown in the Admin Dashboard does not match the seat count reflected on a recent invoice.

**Cause:** A mid-cycle seat addition or removal has not yet been reflected in the current billing period's proration, or a deactivated user's seat was not yet released due to a brief processing delay.

**Solution:** Review seat change history under **Admin Dashboard > Billing & Plan**; discrepancies typically resolve at the next billing cycle. For urgent reconciliation, contact Corvex billing support.

**Prevention:** Review seat usage monthly rather than only at renewal, to catch and understand changes as they occur.

**Related Issues:** none

---

### CDW-12002 — Plan Upgrade Not Reflecting New Feature Access

**Symptoms:** An account was upgraded to a higher plan tier, but agents still cannot access features associated with the new tier.

**Cause:** A brief propagation delay following the upgrade, or the specific feature also requires an explicit configuration step (such as enabling SSO) beyond simply being on a qualifying plan.

**Solution:** Allow a short period for the upgrade to fully propagate; if access is still missing after some time, confirm whether the specific feature requires additional setup, as described in the CloudDesk Chat Product Overview.

**Prevention:** Review the relevant Product Overview's feature availability table ahead of an upgrade, to understand which changes are automatic versus requiring configuration.

**Related Issues:** none

---

### CDW-12003 — Trial Account Losing Access Unexpectedly

**Symptoms:** A trial account loses access to the platform before the expected end of the trial period.

**Cause:** The trial period genuinely expired, often because the expiration date was miscalculated from the trial start date, or trial usage exceeded a threshold that triggers early review.

**Solution:** Confirm the trial's actual start and end dates under **Admin Dashboard > Billing & Plan**; contact your Corvex sales representative if you believe the trial ended prematurely in error.

**Prevention:** Note your trial's exact end date in your team's calendar to plan a plan decision or extension request ahead of time.

**Related Issues:** none

---

## Section 13: Data Management

### CDW-13001 — Data Export Stuck in "Processing" State

**Symptoms:** A requested data export remains in a Processing state well beyond the typical completion time.

**Cause:** An unusually large export scope (e.g., full account history with no date range applied) is taking longer than typical to prepare.

**Solution:** Allow additional time for large exports; if the export remains stuck for more than 24 hours, contact Corvex support to investigate.

**Prevention:** Scope exports with a specific date range or data type where full history isn't required, reducing processing time.

**Related Issues:** none

---

### CDW-13002 — Restored Conversation Missing Some Tags

**Symptoms:** A conversation restored from **Admin Dashboard > Data > Recently Deleted** is missing tags that were applied before deletion.

**Cause:** One or more of the original tags were themselves deleted or renamed from the account's tag list after the conversation was deleted but before it was restored.

**Solution:** Reapply any missing tags manually after restoration; if the original tag was renamed rather than deleted, use the new tag name going forward.

**Prevention:** Avoid deleting or renaming tags that may be referenced by recently deleted conversations still within the recovery window.

**Related Issues:** CDW-7005

---

### CDW-13003 — Unable to Restore a Deleted Conversation

**Symptoms:** A deleted conversation does not appear under **Admin Dashboard > Data > Recently Deleted**.

**Cause:** The deletion occurred outside the account's recovery window (30 days on Starter and Professional; extended on Enterprise), or the item was removed via permanent deletion rather than standard deletion.

**Solution:** Confirm the deletion date against your plan's recovery window; if the item was permanently removed, it is not recoverable through self-service tools, consistent with the CloudDesk Chat Administrator Guide.

**Prevention:** Reserve permanent deletion for cases where the intent is genuinely irreversible removal, and use standard deletion for routine cleanup.

**Related Issues:** none

---

## Section 14: Mobile SDK (Embedded Chat in Customer Apps)

### CDW-14001 — Push Notifications Not Delivering to End Customers via Mobile SDK

**Symptoms:** Customers using the organization's own mobile app do not receive push notifications for agent replies sent through the embedded CloudDesk Chat mobile SDK.

**Cause:** The host app's push notification credentials (APNs certificate for iOS, or FCM server key for Android) were not correctly configured within the SDK setup, or have expired.

**Solution:** Review and, if necessary, regenerate and re-upload push notification credentials under **Settings > Chat Widget > Mobile SDK > Push Configuration**.

**Prevention:** Track push credential expiration dates (particularly APNs certificates, which expire annually) and renew proactively.

**Related Issues:** CDW-1008

---

### CDW-14002 — SDK Widget Styling Not Matching Host App Theme

**Symptoms:** The embedded chat interface visually clashes with the surrounding native app design.

**Cause:** SDK theming configuration was left at default values rather than customized to match the host app's design system.

**Solution:** Review the SDK theming options in the developer documentation and apply custom colors, fonts, and spacing consistent with your app's design system.

**Prevention:** Include SDK theming as a standard design review step during initial mobile app integration, rather than an afterthought.

**Related Issues:** none

---

### CDW-14003 — SDK Causing Increased App Crash Rate

**Symptoms:** App crash reporting shows an increase in crashes correlated with SDK integration or a recent SDK version update.

**Cause:** An SDK version incompatibility with a specific OS version, or a conflict with another third-party SDK integrated in the same app.

**Solution:** Review crash logs for stack traces referencing the CloudDesk Chat SDK, confirm you are on the current recommended SDK version, and consult the developer documentation's known compatibility notes before escalating to Corvex developer support.

**Prevention:** Test SDK updates in a staging build against your app's specific device and OS matrix before releasing to production.

**Related Issues:** CDW-1008

---

### CDW-14004 — Conversation History Not Persisting Between App Sessions

**Symptoms:** A customer's conversation history disappears when they close and reopen the host app.

**Cause:** The SDK is not configured to persist a stable visitor identifier between sessions, causing each app launch to be treated as a new, unrecognized visitor.

**Solution:** Review the SDK integration's visitor identity configuration, ensuring a persistent identifier (such as a logged-in user ID, where available) is passed to the SDK consistently across sessions.

**Prevention:** Pass an authenticated user identifier to the SDK whenever the customer is logged in to the host app, rather than relying solely on anonymous session-based identity.

**Related Issues:** none

---

## Section 15: General Behavior and Edge Cases

### CDW-15001 — Emoji or Special Characters Displaying as Garbled Text

**Symptoms:** Messages containing emoji or non-Latin characters display as garbled text or placeholder boxes for one party in a conversation.

**Cause:** A character encoding mismatch, typically caused by a custom integration or webhook consumer not correctly handling UTF-8 encoded content.

**Solution:** If the issue is visible only in an integrated system (e.g., a synced record in a CRM), verify that system's encoding configuration; the issue does not typically occur within the CloudDesk Chat interface itself.

**Prevention:** Ensure any custom integration explicitly declares and handles UTF-8 encoding for all text fields.

**Related Issues:** CDW-2006

---

### CDW-15002 — File Attachment Upload Failing

**Symptoms:** An agent or customer attempts to attach a file to a conversation and receives an upload error.

**Cause:** The file exceeds the maximum allowed attachment size, or the file type is on the platform's restricted list for security reasons.

**Solution:** Confirm the file size and type against the limits documented in the CloudDesk Chat Product Overview; compress or convert the file if necessary.

**Prevention:** Share attachment size and type limits with customer-facing teams so they can set expectations with customers proactively.

**Related Issues:** none

---

### CDW-15003 — Conversation Timestamp Displaying in Wrong Time Zone

**Symptoms:** Conversation timestamps appear offset from the agent's actual local time.

**Cause:** The agent's profile time zone setting does not match their actual current location, often after relocating or traveling without updating their profile.

**Solution:** Update the time zone setting under **My Settings > Profile** to reflect the agent's current location.

**Prevention:** Include a time zone accuracy check as part of periodic profile review, particularly for distributed or remote teams.

**Related Issues:** none

---

### CDW-15004 — Browser Back Button Causing Unexpected Navigation

**Symptoms:** Using the browser's back button while in the agent workspace navigates away from CloudDesk Chat entirely instead of returning to a prior in-app view.

**Cause:** This is expected behavior for a single-page application when navigating beyond its initial in-app history state; it is not a defect but a common point of confusion for new agents.

**Solution:** Use the in-app navigation controls (back arrow within the workspace, or the left navigation panel) rather than the browser's back button when moving between conversations.

**Prevention:** Include this distinction in new agent onboarding materials.

**Related Issues:** none

---

*This Troubleshooting Guide covers common CloudDesk Chat issues and their resolutions. If an issue is not listed here or a documented solution does not resolve your problem, contact Corvex support through the channel appropriate to your plan tier, as described in the Corvex Cloud Pricing Guide.*
