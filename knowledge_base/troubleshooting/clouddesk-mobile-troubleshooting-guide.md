# CloudDesk Mobile
## Troubleshooting Guide

*Corvex Cloud — CloudDesk Mobile*
*This guide documents known issues, their causes, and their resolutions for CloudDesk Mobile. It is intended for administrators, agents, and technical staff diagnosing problems with the platform. For general usage instructions, refer to the CloudDesk Mobile User Manual. For configuration guidance, refer to the CloudDesk Mobile Administrator Guide.*

---

## How to Use This Guide

Issues are grouped by category. Each entry includes the symptoms you may observe, the most common underlying cause, a recommended solution, steps to prevent recurrence, and related issues you may want to review if the listed solution does not fully resolve your problem.

---

## Section 1: Installation and App Store

### CDM-1001 — App Not Found in App Store

**Symptoms:** Searching for "CloudDesk Mobile" in the Apple App Store or Google Play Store returns no results or an unrelated app.

**Cause:** A regional app store availability restriction, or the search term used does not closely match the app's current listed name.

**Solution:** Search for "Corvex Cloud" as an alternate term, or use the direct app store link provided in your invitation email or by your administrator.

**Prevention:** Bookmark or distribute the direct app store link to new agents rather than relying on search, particularly for organizations in regions with variable app store indexing.

**Related Issues:** none

---

### CDM-1002 — Installation Fails with Insufficient Storage Error

**Symptoms:** The app store reports insufficient device storage despite the app's relatively small file size.

**Cause:** The device's available storage is genuinely low once accounting for the app's temporary installation overhead and any pending OS update reserving space.

**Solution:** Free up device storage by removing unused apps or files, or complete any pending OS update that may be reserving space, then retry installation.

**Prevention:** Recommend a minimum free storage threshold for devices used for work purposes as part of your organization's device readiness guidance.

**Related Issues:** none

---

### CDM-1003 — App Installed but Will Not Open

**Symptoms:** Tapping the app icon results in a brief flash or no response, with the app failing to launch.

**Cause:** An incomplete or corrupted installation, often due to an interrupted download or update.

**Solution:** Uninstall and reinstall the app from the app store.

**Prevention:** Ensure a stable network connection during app installation and updates to reduce the likelihood of a corrupted download.

**Related Issues:** CDM-1004

---

### CDM-1004 — App Crashes Immediately on Launch After an Update

**Symptoms:** The app previously worked normally but crashes immediately on launch following an automatic or manual update.

**Cause:** A device operating system version no longer meets the minimum supported requirement for the latest app version, or locally cached data from a much older app version is incompatible with the updated version's data format.

**Solution:** Confirm your device meets the current minimum supported OS version documented in the CloudDesk Mobile Product Overview; if it does, try clearing the app's local cache/storage through your device settings, or reinstall the app.

**Prevention:** Keep device operating systems reasonably current to avoid falling behind the app's minimum supported version over time.

**Related Issues:** CDM-1003, CDM-9001

---

### CDM-1005 — MDM-Distributed App Not Appearing on Managed Device

**Symptoms:** An organization using mobile device management (MDM) to distribute CloudDesk Mobile does not see the app appear on a newly enrolled device.

**Cause:** The device has not yet completed a full policy sync with the MDM server, or the device was not included in the deployment group configured to receive the app.

**Solution:** Trigger a manual policy sync from the device or MDM console, and confirm the device is correctly assigned to the deployment group configured to receive CloudDesk Mobile.

**Prevention:** Verify new device enrollment against expected deployment groups as a standard step in device provisioning.

**Related Issues:** none

---

## Section 2: Login and Authentication

### CDM-2001 — Cannot Log In with Correct Credentials

**Symptoms:** Entering an email and password believed to be correct results in a login failure.

**Cause:** The account is configured for SSO-only login and cannot use standard password authentication, or the account was recently deactivated.

**Solution:** Confirm your organization's login method and account status with your administrator; use **Sign in with SSO** if applicable rather than standard password login.

**Prevention:** Communicate clearly with users when SSO is newly enforced account-wide, since password login will no longer function for affected accounts.

**Related Issues:** CDM-2002

---

### CDM-2002 — SSO Login Redirect Failing on Mobile

**Symptoms:** Tapping **Sign in with SSO** opens a browser view that fails to complete the authentication redirect back into the app.

**Cause:** The device's default browser or in-app browser view is blocking a required redirect, often due to overly aggressive tracking prevention or pop-up blocking settings.

**Solution:** Review browser or in-app webview settings for restrictions on redirects or pop-ups, and temporarily relax them if needed to complete the SSO flow.

**Prevention:** Test the SSO mobile login flow against your organization's standard device configuration profile before broad rollout.

**Related Issues:** CDM-2001

---

### CDM-2003 — Organization Domain Not Recognized During Login

**Symptoms:** Entering the organization's Corvex Cloud domain at login returns a "not found" error.

**Cause:** The domain was entered with a typo, or with an unnecessary `https://` prefix or trailing slash not expected by the login field.

**Solution:** Re-enter the domain exactly as provided in your invitation email or by your administrator, without additional prefixes or trailing characters.

**Prevention:** Provide the exact domain string in new agent onboarding materials to reduce manual entry errors.

**Related Issues:** none

---

### CDM-2004 — Biometric Login Prompt Not Appearing

**Symptoms:** Despite enabling biometric app lock, the app does not prompt for fingerprint or face authentication on launch.

**Cause:** The device's own biometric authentication is not currently configured at the OS level, or the app does not have permission to access the device's biometric authentication API.

**Solution:** Confirm biometric authentication is set up in the device's system settings, and confirm the app has been granted the relevant permission if prompted separately by the OS.

**Prevention:** Set up device-level biometric authentication before enabling biometric app lock within CloudDesk Mobile.

**Related Issues:** CDM-2005

---

### CDM-2005 — Biometric Lock Repeatedly Failing to Recognize Valid Fingerprint or Face

**Symptoms:** Biometric authentication consistently fails despite using a valid, previously enrolled fingerprint or face.

**Cause:** This is typically a device-level biometric hardware or sensor issue (dirty sensor, poor lighting for face recognition) rather than an app-specific problem.

**Solution:** Clean the biometric sensor if applicable, ensure adequate lighting for face recognition, or fall back to the device passcode/app password if biometric authentication continues to fail.

**Prevention:** No specific app-level preventive action is available for device hardware sensor performance.

**Related Issues:** CDM-2004

---

### CDM-2006 — Session Expiring Immediately After Successful Login

**Symptoms:** A user successfully logs in but is immediately returned to the login screen.

**Cause:** The device's system clock is significantly out of sync with actual current time, causing session token validation to fail.

**Solution:** Confirm the device's date and time settings are set to automatic/network-provided time rather than a manually configured, incorrect value.

**Prevention:** Recommend automatic date and time settings as standard device configuration guidance for all users.

**Related Issues:** none

---

### CDM-2007 — Remote-Revoked Session Not Prompting Re-Login

**Symptoms:** After an administrator remotely revokes a device's session, the app continues to appear functional for a period before eventually failing.

**Cause:** Revocation takes effect on the device's next connectivity check-in rather than instantaneously, so a device that briefly loses connectivity around the revocation time may not immediately reflect the change.

**Solution:** This is expected behavior within a short window; if immediate effect is critical (e.g., a confirmed stolen device), also use your MDM platform's remote wipe capability, where available, for immediate effect independent of the app's own check-in cycle.

**Prevention:** For high-urgency device loss scenarios, rely on MDM remote wipe in addition to in-app session revocation rather than the app's check-in cycle alone.

**Related Issues:** none

---

## Section 3: Push Notifications

### CDM-3001 — Not Receiving Any Push Notifications

**Symptoms:** No push notifications are received for new assignments, mentions, or alerts, despite being enabled in the app.

**Cause:** Device-level notification permissions for the app were denied or later revoked at the OS level, independent of the app's own internal notification settings.

**Solution:** Check device system settings to confirm notifications are permitted for CloudDesk Mobile, since both app-level and device-level permissions must allow notifications.

**Prevention:** Include a device-level notification permission check as a standard step in new agent mobile onboarding.

**Related Issues:** CDM-3002

---

### CDM-3002 — Push Notifications Delayed by Several Minutes

**Symptoms:** Notifications eventually arrive but consistently several minutes after the triggering event.

**Cause:** Device-level battery optimization or "Doze mode" (Android) or Low Power Mode (iOS) is deferring background network activity, including push notification delivery, to conserve battery.

**Solution:** Review device battery optimization settings and exempt CloudDesk Mobile from aggressive background restriction where your device and role require timely notifications.

**Prevention:** Recommend appropriate battery optimization exemptions as part of device setup guidance for agents relying on prompt mobile alerts.

**Related Issues:** CDM-3001, CDM-3003

---

### CDM-3003 — Notifications Received for Disabled Alert Types

**Symptoms:** A user continues to receive push notifications for an alert type they explicitly disabled in **My Settings > Notification Preferences**.

**Cause:** A brief propagation delay between changing the preference and the change taking effect, or the specific notification originated from an account-wide notification policy override configured by an administrator that takes precedence over individual preferences.

**Solution:** Allow a short period for preference changes to propagate; if the issue persists, check with an administrator whether an account-wide notification policy is overriding individual preferences for that alert type.

**Prevention:** Administrators should communicate clearly when an account-wide notification policy is intentionally set to override individual user preferences.

**Related Issues:** none

---

### CDM-3004 — Duplicate Push Notifications for the Same Event

**Symptoms:** A single new assignment triggers two separate push notifications.

**Cause:** The user has more than one active mobile session (for example, the app installed on both a phone and a tablet under the same account) and each device independently generates a notification.

**Solution:** This is expected behavior when logged in on multiple devices; if undesired, log out of the device not actively in use.

**Prevention:** Encourage single-device mobile usage per user where practical, or accept duplicate notifications as a known trade-off of multi-device access.

**Related Issues:** none

---

### CDM-3005 — SLA Breach Alert Not Received on Mobile Despite Being Enabled

**Symptoms:** An SLA breach occurs and a desktop notification is received by a colleague, but the mobile user with SLA alerts enabled does not receive one.

**Cause:** SLA breach alerting on mobile is available only on Professional and Enterprise plans, and the specific role may not have SLA visibility permission even on a qualifying plan.

**Solution:** Confirm your account's plan tier and the user's role permissions under **Admin Dashboard > Roles & Permissions**, ensuring SLA visibility is included.

**Prevention:** Review plan-specific feature availability in the CloudDesk Mobile Product Overview before assuming SLA alerting is universally available.

**Related Issues:** none

---

### CDM-3006 — Notification Sound Not Playing Despite Notification Appearing

**Symptoms:** A push notification banner appears but no sound is played, even with device volume audible.

**Cause:** The device is in silent or Do Not Disturb mode, which suppresses notification sounds while still displaying the visual banner.

**Solution:** Check the device's silent/Do Not Disturb status; if intentional, this is expected behavior. If unintentional, disable silent mode or add an app-specific exception where the device OS supports it.

**Prevention:** Include device sound/notification mode as a standard check for agents relying on audible alerts during active shifts.

**Related Issues:** none

---

## Section 4: Sync and Connectivity

### CDM-4001 — Tickets or Chats Not Syncing to the App

**Symptoms:** Recently created or updated tickets and chats visible on desktop do not appear in CloudDesk Mobile.

**Cause:** The app has lost its background sync connection, often due to the OS suspending background network activity, or the device has no active network connection.

**Solution:** Manually pull to refresh within the app, or fully close and reopen the app to force a fresh sync; confirm the device has an active Wi-Fi or cellular data connection.

**Prevention:** Review device battery optimization settings to ensure background sync is permitted for CloudDesk Mobile.

**Related Issues:** CDM-3002

---

### CDM-4002 — App Stuck on a Loading Spinner Indefinitely

**Symptoms:** A specific screen (e.g., a ticket detail view) displays a loading spinner that never resolves.

**Cause:** A network request for that specific screen's data failed silently without displaying an error message, often due to an unstable or very slow connection.

**Solution:** Return to the previous screen and try again, or fully close and reopen the app; if the issue is consistent for a specific item, try accessing it from desktop to determine whether the issue is mobile-specific or affects the underlying record.

**Prevention:** No specific preventive action is available for occasional network instability; the app's retry behavior is designed to self-resolve on reconnection.

**Related Issues:** CDM-4001

---

### CDM-4003 — App Showing Outdated Data After Reconnecting

**Symptoms:** After a period offline, the app displays data that appears stale even though the device shows an active connection.

**Cause:** A brief delay between reconnection and the app's background sync process completing a full refresh.

**Solution:** Manually pull to refresh the relevant screen to force an immediate sync rather than waiting for the automatic background process.

**Prevention:** No specific preventive action is available; manual refresh is a reliable, immediate remedy when needed.

**Related Issues:** CDM-4001

---

### CDM-4004 — Slow Sync Performance on Cellular Data

**Symptoms:** Sync and data loading are noticeably slower on cellular data compared to Wi-Fi.

**Cause:** Cellular network conditions, particularly on lower-generation networks or in areas of weak signal, inherently provide lower throughput and higher latency than typical Wi-Fi connections.

**Solution:** Connect to Wi-Fi where available for data-intensive tasks, or reduce the data caching limit to prioritize essential sync over comprehensive local caching on constrained connections.

**Prevention:** Set expectations with mobile-dependent agents that performance may vary meaningfully based on network type and signal strength.

**Related Issues:** none

---

### CDM-4005 — App Consuming Excessive Cellular Data

**Symptoms:** A user notices unexpectedly high cellular data usage attributed to CloudDesk Mobile.

**Cause:** A high data caching limit configured by the administrator, combined with heavy usage, results in substantial background data transfer, particularly for image and file attachments viewed within conversations.

**Solution:** Review and, if appropriate, request a lower data caching limit from your administrator under **Admin Dashboard > Mobile > Security Policy > Data Caching**, or restrict background app refresh to Wi-Fi only in device settings where supported.

**Prevention:** Set data caching limits with cellular data cost in mind for organizations with a significant portion of mobile-first, cellular-dependent users.

**Related Issues:** none

---

## Section 5: Offline Drafts

### CDM-5001 — Offline Draft Not Sending After Reconnecting

**Symptoms:** A reply composed while offline remains in a pending state well after connectivity is restored.

**Cause:** The app has not yet detected the restored connection, or a background sync restriction is delaying automatic send.

**Solution:** Manually reopen the conversation containing the pending draft to trigger an immediate send attempt, or fully close and reopen the app.

**Prevention:** Confirm connectivity is fully restored (not just a weak or intermittent signal) before assuming a queued draft should have sent.

**Related Issues:** CDM-4001

---

### CDM-5002 — Offline Draft Lost After App Update

**Symptoms:** A draft composed while offline is missing after the app was updated before reconnecting.

**Cause:** In rare cases, an app update process can clear certain local application data depending on the nature of the update, particularly a major version update rather than a minor patch.

**Solution:** This data is not recoverable from the server, since it was never transmitted, as described in the CloudDesk Mobile Administrator Guide; the reply must be recomposed.

**Prevention:** Where possible, send pending drafts before initiating an app update, or wait until reconnected to update the app.

**Related Issues:** none

---

### CDM-5003 — Duplicate Message Sent from a Queued Draft

**Symptoms:** A customer receives the same reply twice after an agent worked offline and reconnected.

**Cause:** The agent manually resent the draft, unaware that the automatic queued send had already succeeded once connectivity was restored.

**Solution:** No corrective action is available for a message already delivered; acknowledge the duplication to the customer if it causes confusion.

**Prevention:** After reconnecting, check whether a queued draft has already sent (reflected in the conversation thread) before manually resending it.

**Related Issues:** CDM-5001

---

### CDM-5004 — Cannot Compose a New Draft While Fully Offline

**Symptoms:** Attempting to start a reply to a conversation not previously loaded while offline results in an error rather than allowing draft composition.

**Cause:** Offline draft composition requires the conversation's base data to have been previously cached locally; a conversation never loaded while online has no local record to attach a draft to.

**Solution:** This is expected behavior; only previously viewed conversations support offline draft composition. Wait for connectivity to view and reply to conversations not already cached.

**Prevention:** Review recently assigned conversations while still connected, where possible, before anticipated periods offline.

**Related Issues:** none

---

## Section 6: Biometric Lock and Device Security

### CDM-6001 — App Locking Out After Too Many Failed Biometric Attempts

**Symptoms:** After several failed biometric authentication attempts, the app requires falling back to a password or device passcode.

**Cause:** This is a standard device operating system security behavior after repeated biometric authentication failures, not an app-specific restriction.

**Solution:** Use your account password or device passcode to unlock the app, then retry biometric authentication on the next launch.

**Prevention:** No specific preventive action is available for standard OS-level biometric security behavior.

**Related Issues:** CDM-2005

---

### CDM-6002 — Mandatory Biometric Lock Policy Preventing Access on Devices Without Biometric Hardware

**Symptoms:** A user on an older device without fingerprint or face recognition hardware cannot satisfy an administrator-enforced mandatory biometric lock policy.

**Cause:** The mandatory policy did not account for devices lacking biometric hardware entirely.

**Solution:** The app should fall back to requiring the device's standard passcode/PIN as an equivalent when biometric hardware is unavailable; if this fallback is not functioning, contact Corvex support to investigate.

**Prevention:** Confirm device passcode fallback behavior is correctly enabled when configuring a mandatory biometric lock policy.

**Related Issues:** none

---

### CDM-6003 — Remote Wipe Command Not Removing Cached Data

**Symptoms:** After an MDM-issued remote wipe, some app data appears to remain briefly accessible before the device fully processes the command.

**Cause:** Remote wipe commands depend on the device successfully receiving and processing the command, which requires an active network connection at the time of transmission.

**Solution:** Confirm the device successfully received the wipe command by checking its status in the MDM console; a device with no connectivity will not process the command until it reconnects.

**Prevention:** For high-urgency scenarios, also revoke the device's session directly in the Corvex Admin Dashboard (Section 5.4 of the Administrator Guide) as an immediate, independent measure alongside MDM remote wipe.

**Related Issues:** none

---

### CDM-6004 — Data Caching Limit Change Not Taking Effect on an Existing Device

**Symptoms:** After an administrator lowers the account-wide data caching limit, a specific device continues to retain more cached data than the new limit specifies.

**Cause:** The policy change applies to new data caching going forward; it does not automatically purge data already cached under the previous, higher limit.

**Solution:** If immediate compliance with the new limit is required, the user can clear the app's local cache through device settings or by logging out and back in, forcing a fresh cache under the new limit.

**Prevention:** Communicate to users when a data caching policy change requires a manual cache clear to take full effect immediately, rather than assuming automatic enforcement.

**Related Issues:** none

---

## Section 7: Device Sessions and MDM

### CDM-7001 — Cannot Locate a Specific User's Device in Device Sessions

**Symptoms:** An administrator searching for a specific user's active device under **Admin Dashboard > Mobile > Device Sessions** cannot find it.

**Cause:** The device's session may have already expired due to inactivity, or the user has not yet completed their first mobile login.

**Solution:** Confirm with the user whether they have successfully logged in to CloudDesk Mobile at least once, and whether their session may have already timed out per the configured session timeout policy.

**Prevention:** Cross-reference expected mobile user onboarding against actual first-login confirmation as part of the onboarding checklist.

**Related Issues:** none

---

### CDM-7002 — Revoked Session Reappearing as Active

**Symptoms:** A device session revoked by an administrator later reappears as active without the user manually logging back in.

**Cause:** The device automatically re-authenticated using a cached refresh token that had not yet been fully invalidated at the time of revocation, a narrow timing edge case.

**Solution:** Revoke the session a second time to ensure full invalidation, and confirm resolution by checking the device's status shortly afterward.

**Prevention:** For high-urgency device loss scenarios, pair session revocation with an MDM-issued remote wipe for a more immediate, comprehensive result.

**Related Issues:** CDM-6003

---

### CDM-7003 — MDM Push Configuration Not Applying to CloudDesk Mobile

**Symptoms:** An MDM-managed app configuration setting (such as a pre-filled organization domain) is not reflected when a user first opens the app.

**Cause:** The MDM managed app configuration payload was not correctly formatted according to the schema documented for CloudDesk Mobile, or the device has not yet synced the latest MDM profile.

**Solution:** Review the managed app configuration schema in the developer documentation, correct any formatting issues, and trigger a fresh MDM profile sync on the affected device.

**Prevention:** Validate MDM managed app configuration against a test device before deploying broadly across the organization's device fleet.

**Related Issues:** CDM-1005

---

### CDM-7004 — Device Showing an Outdated App Version in Device Sessions

**Symptoms:** The Device Sessions view shows an app version for a device that the user confirms has already been updated.

**Cause:** The version reported updates only on the device's next active session check-in with the server, causing a brief lag after a local update before the Admin Dashboard reflects it.

**Solution:** Ask the user to open and actively use the app briefly to trigger a check-in, after which the reported version should update.

**Prevention:** No specific preventive action is needed; this reporting lag is minor and self-resolving with normal app usage.

**Related Issues:** none

---

## Section 8: Performance

### CDM-8001 — App Running Slowly on an Older Device

**Symptoms:** The app is noticeably slower to navigate and load content on an older device model compared to a newer one.

**Cause:** Older device hardware processes rendering and local data operations more slowly, particularly for accounts with a large cached data volume.

**Solution:** Reduce the data caching limit to decrease the volume of local data the device must manage, and close other resource-intensive apps running in the background.

**Prevention:** Where feasible, prioritize newer, currently supported devices for roles requiring frequent, performance-sensitive mobile access.

**Related Issues:** CDM-8002

---

### CDM-8002 — App Consuming Excessive Battery

**Symptoms:** A user notices CloudDesk Mobile listed as a significant battery consumer in device battery usage statistics.

**Cause:** Frequent background sync activity and push notification handling, particularly for very active accounts with high conversation volume, inherently consumes some background battery.

**Solution:** This is generally expected for an actively used real-time communication app; if usage seems disproportionate, confirm the app is on its current version, since performance optimizations are included in regular updates.

**Prevention:** Keep the app updated to the current version to benefit from ongoing performance and efficiency improvements.

**Related Issues:** CDM-8001

---

### CDM-8003 — App Becoming Unresponsive with a Very Large Number of Open Tabs or Conversations Cached

**Symptoms:** The app becomes sluggish or briefly unresponsive after extended use across a long shift without restarting the app.

**Cause:** Accumulated in-memory state from extended use without a restart, particularly on devices with limited available memory.

**Solution:** Fully close and reopen the app periodically during long shifts to clear accumulated in-memory state.

**Prevention:** Encourage a periodic app restart as a routine practice for agents working extended mobile shifts, particularly on lower-memory devices.

**Related Issues:** CDM-8001

---

### CDM-8004 — Team View Loading Slowly for Large Teams

**Symptoms:** The Team tab takes noticeably longer to load for administrators or team leads overseeing a very large team.

**Cause:** Rendering real-time status for a large number of agents simultaneously on a mobile device's more limited processing capacity takes longer than the equivalent desktop view.

**Solution:** Use available filters within the Team tab to narrow the view to a specific sub-team or status category, reducing the amount of data rendered at once.

**Prevention:** For very large teams, consider using desktop for comprehensive team oversight and mobile primarily for quick status checks and urgent items.

**Related Issues:** none

---

## Section 9: Display and UI

### CDM-9001 — Text or Interface Elements Rendering Incorrectly

**Symptoms:** Text overlaps, buttons are misaligned, or other visual rendering defects appear on a specific device or OS version.

**Cause:** A device-specific rendering inconsistency, often on an unusually large or small screen size, or an OS version not fully covered by the app's current supported range.

**Solution:** Confirm your device OS version falls within the currently supported range documented in the CloudDesk Mobile Product Overview; if it does and the issue persists, report the specific device model and OS version to Corvex support.

**Prevention:** Keep device operating systems reasonably current, and report new device model compatibility issues promptly so they can be addressed in future app updates.

**Related Issues:** CDM-1004

---

### CDM-9002 — Dark Mode Not Applying Consistently

**Symptoms:** Some screens within the app respect the device's dark mode setting while others display in light mode.

**Cause:** A specific screen or component was not fully updated in a recent release to support dark mode theming.

**Solution:** This is a cosmetic issue only and does not affect functionality; report the specific screen to Corvex support so it can be addressed in a future release.

**Prevention:** No user-side preventive action is available for incomplete theming coverage in a specific app version.

**Related Issues:** none

---

### CDM-9003 — Tablet Layout Not Utilizing Available Screen Space

**Symptoms:** On a tablet, the app displays a phone-style single-column layout rather than the expected tablet-optimized layout.

**Cause:** The device is running in a screen size or orientation mode (such as split-screen multitasking) that falls below the threshold for triggering the tablet-optimized layout.

**Solution:** Exit split-screen or reduced-window multitasking mode, or rotate the device, to allow the app to detect sufficient screen space for the tablet layout.

**Prevention:** No specific preventive action is available; this is an intentional, threshold-based layout behavior.

**Related Issues:** none

---

### CDM-9004 — Language Setting Not Matching Device Language

**Symptoms:** The app displays in a different language than the device's overall system language setting.

**Cause:** The app's language follows the user's CloudDesk Cloud profile language preference, which may differ from the device's system language if not explicitly aligned.

**Solution:** Review and update the language preference under the user's profile settings, accessible from both desktop and mobile, rather than relying solely on device system language.

**Prevention:** Confirm profile language preference is set correctly during initial account setup, particularly for multilingual teams.

**Related Issues:** none

---

## Section 10: Team View, Escalations, and Reporting

### CDM-10001 — Escalation Approval Action Not Available on Mobile

**Symptoms:** A team lead expects to approve an escalation directly from a push notification but finds no approval action available.

**Cause:** Escalation approval from mobile is available only on Professional and Enterprise plans, or the specific escalation type was not configured to support mobile approval.

**Solution:** Confirm your account's plan tier, and review the escalation workflow configuration on desktop to confirm mobile approval is enabled for the relevant escalation type.

**Prevention:** Review plan-specific feature availability in the CloudDesk Mobile Product Overview before relying on mobile escalation approval as a primary workflow.

**Related Issues:** none

---

### CDM-10002 — Performance Snapshot Showing Different Figures Than Desktop Analytics

**Symptoms:** A metric shown in the mobile performance snapshot does not exactly match the equivalent figure in the full desktop CloudDesk Analytics report.

**Cause:** The mobile snapshot uses a simplified, pre-aggregated calculation optimized for fast loading, which may differ slightly from the full desktop report's more detailed calculation.

**Solution:** For any figure requiring precise accuracy, rely on the full desktop report rather than the mobile snapshot, consistent with guidance in the CloudDesk Analytics Troubleshooting Guide.

**Prevention:** Communicate to the team that mobile snapshots are intended for quick reference, with desktop serving as the authoritative source for precise figures.

**Related Issues:** none

---

### CDM-10003 — Team Availability Status Not Reflecting Recent Changes

**Symptoms:** The Team tab shows an agent's availability status as outdated compared to their actual current status.

**Cause:** A brief synchronization delay, or the agent has multiple active sessions with conflicting status values, similar to the desktop real-time dashboard behavior.

**Solution:** Pull to refresh the Team tab; if the discrepancy persists, ask the agent to confirm status consistency across all their active sessions.

**Prevention:** Encourage agents to work from a single active session where practical, to avoid state synchronization conflicts.

**Related Issues:** none

---

### CDM-10004 — Reassigning a Ticket from Mobile Not Reflecting Immediately on Desktop

**Symptoms:** A team lead reassigns a ticket from mobile, but a colleague viewing the same ticket on desktop still sees the previous assignee briefly.

**Cause:** A brief propagation delay between the mobile action and the desktop view's real-time update.

**Solution:** Ask the desktop user to refresh their view; the underlying reassignment is applied immediately and accurately, with only the visual display briefly lagging.

**Prevention:** No specific preventive action is needed for this typically sub-minute propagation delay.

**Related Issues:** none

---

## Section 11: Attachments and Media

### CDM-11001 — Cannot View an Attachment on Mobile

**Symptoms:** Tapping an attachment within a conversation on mobile results in an error or blank screen, though the same attachment opens fine on desktop.

**Cause:** The file type is not natively supported for in-app preview on mobile, even though it may be viewable through a desktop browser's broader native format support.

**Solution:** Download the attachment to view it using a compatible app installed on the device, if in-app preview is not supported for that specific file type.

**Prevention:** Where possible, standardize on commonly supported attachment formats for internal workflows involving frequent mobile review.

**Related Issues:** none

---

### CDM-11002 — Camera Attachment Upload Failing

**Symptoms:** Attempting to attach a photo taken directly through the app's camera integration fails to upload.

**Cause:** The app was not granted camera or photo library permission at the device OS level, or the resulting image file exceeds the maximum allowed attachment size.

**Solution:** Confirm camera and photo library permissions are granted to CloudDesk Mobile in device settings, and confirm the resulting file size is within platform limits.

**Prevention:** Grant relevant permissions during initial app setup rather than waiting for an in-the-moment failure.

**Related Issues:** none

---

### CDM-11003 — Attachment Upload Stuck at 0% Progress

**Symptoms:** An attachment upload progress indicator remains at 0% and never advances.

**Cause:** A weak or unstable network connection is preventing the upload from initiating successfully.

**Solution:** Move to an area with a stronger connection, or switch between Wi-Fi and cellular data to determine whether one offers more stable connectivity for the upload.

**Prevention:** For agents frequently attaching larger files from mobile, prioritize Wi-Fi connectivity when available.

**Related Issues:** CDM-4004

---

## Section 12: General Behavior and Edge Cases

### CDM-12001 — Pull-to-Refresh Gesture Not Working

**Symptoms:** The pull-to-refresh gesture at the top of a list does not trigger a refresh.

**Cause:** The list was not scrolled fully to the top before attempting the gesture, since the refresh trigger requires starting from the topmost scroll position.

**Solution:** Scroll fully to the top of the list before performing the pull-to-refresh gesture.

**Prevention:** No specific preventive action needed; this is standard gesture behavior across most mobile applications.

**Related Issues:** none

---

### CDM-12002 — App Requesting Login Again Shortly After a Successful Login

**Symptoms:** A user logs in successfully but is prompted to log in again within a few minutes.

**Cause:** The account's session timeout is configured to an unusually short duration, or the device is experiencing the clock synchronization issue described in Section 2.

**Solution:** Review session timeout configuration with an administrator if the duration seems unintentionally short, and confirm device date/time settings are correct.

**Prevention:** Administrators should periodically review session timeout settings against actual team usage patterns.

**Related Issues:** CDM-2006

---

### CDM-12003 — Search Results Differing Between Mobile and Desktop

**Symptoms:** Searching for the same term on mobile and desktop returns a different number or order of results.

**Cause:** Mobile search may apply a more limited default scope (such as recent conversations only) to optimize performance on smaller devices, compared to desktop's more comprehensive default search scope.

**Solution:** Use available mobile search filters to broaden scope if needed, or perform an exhaustive search from desktop when comprehensive historical results are required.

**Prevention:** Communicate to the team that mobile search is optimized for quick, recent lookups rather than comprehensive historical search.

**Related Issues:** none

---

### CDM-12004 — Time Displayed for a Conversation Inconsistent with Desktop

**Symptoms:** A timestamp for the same conversation event displays a different time on mobile versus desktop.

**Cause:** The mobile device's time zone setting differs from the profile time zone setting used on desktop, if the two were not kept in sync.

**Solution:** Confirm the device's time zone setting matches the intended profile time zone; where they are expected to differ intentionally (e.g., traveling), understand that displayed times reflect the device's local time zone by design.

**Prevention:** Keep device time zone settings set to automatic/network-provided values to stay aligned with actual current location.

**Related Issues:** none

---

### CDM-12005 — App Not Updating Automatically Despite Auto-Update Enabled

**Symptoms:** A new app version is available in the app store, but the device has not automatically updated despite auto-update settings being enabled.

**Cause:** Automatic app store updates typically require the device to be connected to Wi-Fi and, in some configurations, actively charging, and may not occur if these conditions have not been recently met.

**Solution:** Manually initiate the update from the app store if timely access to new features or fixes is needed rather than waiting for automatic update conditions to be met.

**Prevention:** Periodically check for manual updates during known low-usage periods rather than relying solely on automatic update timing.

**Related Issues:** none

---

### CDM-12006 — Two Users Sharing a Single Device Experiencing Data Crossover Confusion

**Symptoms:** A device shared between two agents (e.g., a shift-based shared tablet) shows one user's cached data briefly before the other logs in.

**Cause:** The previous user did not fully log out before handing off the device, leaving their session and cached data active.

**Solution:** Ensure the outgoing user fully logs out under **More > My Settings > Log Out** before handing off a shared device to another user.

**Prevention:** Establish a clear shift-handoff procedure requiring explicit logout for any shared-device usage pattern, and consider whether device-level user switching (where supported) offers cleaner separation than a single shared app session.

**Related Issues:** none

---

### CDM-12007 — Deep Link from an External Notification Not Opening the Correct Conversation

**Symptoms:** Tapping a link from an external system (e.g., an email notification) intended to open a specific conversation in CloudDesk Mobile instead opens the app to its default home screen.

**Cause:** The device does not have CloudDesk Mobile installed, causing the deep link to fail over to a generic app store or web fallback, or the app was installed after the link was originally generated and has not yet registered its deep link handling with the OS.

**Solution:** Ensure CloudDesk Mobile is installed and has been opened at least once to register deep link handling, then retry the link.

**Prevention:** Include app installation as a prerequisite step before distributing any workflow relying on deep links into CloudDesk Mobile.

**Related Issues:** CDM-1003

---

### CDM-12008 — Widget or App Icon Badge Count Not Matching Actual Unread Items

**Symptoms:** The app icon's notification badge shows a number that doesn't match the actual count of unread or unassigned items when opening the app.

**Cause:** The badge count is updated based on the most recent push notification payload and can drift from the true current count if several items were resolved by other agents between notification events.

**Solution:** Open the app to see the accurate, current count; the badge is a best-effort indicator rather than a guaranteed real-time count.

**Prevention:** Treat the badge count as a general indicator prompting a check-in, not an authoritative figure for workload planning.

**Related Issues:** none

---

### CDM-12009 — App Displaying a "New Version Required" Message and Blocking Access

**Symptoms:** The app refuses to proceed past a splash screen, displaying a message that an update is required.

**Cause:** The installed app version has reached its end-of-support date as part of Corvex's standard version deprecation policy, requiring an update to continue functioning.

**Solution:** Update the app to the current version through your device's app store, or through your organization's MDM platform if centrally managed.

**Prevention:** Monitor app version deprecation announcements and update devices proactively ahead of an announced enforcement date, as described in the CloudDesk Mobile Administrator Guide.

**Related Issues:** CDM-1004

---

### CDM-12010 — Copy-and-Paste Not Working Within the Reply Composer

**Symptoms:** Attempting to paste text into the reply composer from another app does nothing, or pastes only partial content.

**Cause:** A device OS clipboard permission restriction, common on newer OS versions with stricter cross-app clipboard access controls, is blocking the paste action.

**Solution:** When prompted by the OS for clipboard access permission, confirm access; if no prompt appeared, check the app's clipboard permission under device privacy settings.

**Prevention:** Review and grant relevant clipboard and privacy permissions during initial app setup to avoid mid-task interruptions.

**Related Issues:** none

---

*This Troubleshooting Guide covers common CloudDesk Mobile issues and their resolutions. If an issue is not listed here or a documented solution does not resolve your problem, contact Corvex support through the channel appropriate to your plan tier, as described in the Corvex Cloud Pricing Guide.*
