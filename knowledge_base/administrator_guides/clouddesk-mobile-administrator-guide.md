# CloudDesk Mobile
## Administrator Guide

*Corvex Cloud — CloudDesk Mobile*
*This guide covers administrative configuration and operation of CloudDesk Mobile. It is intended for account administrators and IT/security staff responsible for managing the platform. For end-user instructions, refer to the CloudDesk Mobile User Manual. For pricing and plan details, refer to the Corvex Cloud Pricing Guide.*

---

## Table of Contents

1. Admin Dashboard
2. User Management
3. Roles
4. Permissions
5. Security
6. Audit Logs
7. Backup
8. Restore
9. Integrations
10. Monitoring
11. Maintenance
12. Common Administrative Tasks

---

## 1. Admin Dashboard

The Admin Dashboard is the central console for configuring and overseeing your organization's use of CloudDesk Mobile. It is accessible only to users with the Administrator role and is shared with the broader Corvex Cloud Admin Dashboard used to administer CloudDesk Chat, CloudDesk Tickets, and CloudDesk Analytics, since CloudDesk Mobile is a client application against the same account rather than a separately administered product.

### 1.1 Accessing the Admin Dashboard

1. Log in to Corvex Cloud with an account holding the Administrator role, from either desktop or the CloudDesk Mobile app itself.
2. Navigate to **Admin Dashboard > Mobile** to reach mobile-specific administrative settings.

Most mobile administration is performed from the desktop Admin Dashboard, though a limited subset of settings — such as remotely revoking a specific device's session — is also accessible from within the CloudDesk Mobile app for administrators who need to act quickly while away from a desktop.

### 1.2 Dashboard Layout

The Mobile section of the Admin Dashboard is organized as follows, each covered in detail later in this guide:

- **Device Sessions** — view and manage all active CloudDesk Mobile sessions account-wide
- **Notification Policy** — configure account-wide defaults for push notification behavior
- **Security Policy** — biometric lock requirements, data caching limits, and session timeout settings specific to mobile
- **Audit Logs** — a searchable record of mobile-related administrative and security activity

### 1.3 Account Health Summary

The Mobile section of the Admin Dashboard displays a summary panel showing the number of active mobile sessions, devices without biometric lock enabled (where your policy recommends but does not mandate it), and any flagged security signals specific to mobile access.

### 1.4 Who Should Have Admin Dashboard Access

Corvex recommends limiting Administrator role assignment to a small number of trusted individuals — typically IT, security, or designated support operations leads — consistent with the principle of least privilege described further in Section 4. Given that mobile devices are more prone to loss or theft than desktop workstations, administrators with mobile session management responsibility should be reachable outside standard business hours for urgent device revocation needs.

---

## 2. User Management

### 2.1 Viewing Users and Mobile Access

Navigate to **Admin Dashboard > Users** to view all users on your account. CloudDesk Mobile does not maintain a separate user list; it uses the same account-wide user list shared with the rest of Corvex Cloud. Any user with an active Corvex Cloud account can install and log in to CloudDesk Mobile using their existing credentials, unless mobile access is specifically restricted for their role (Section 4).

### 2.2 No Separate Mobile Invitation Required

Because CloudDesk Mobile authenticates against the same account used for the desktop workspace, there is no separate mobile-specific user invitation process. Administrators inviting a new user through **Admin Dashboard > Users > Invite User**, as described in the CloudDesk Chat and CloudDesk Tickets Administrator Guides, automatically grant that user the ability to log in to CloudDesk Mobile as well, unless mobile access has been explicitly restricted.

### 2.3 Viewing a User's Mobile Devices

Click any user from **Admin Dashboard > Users** and select the **Devices** tab to view that user's currently logged-in mobile devices, including device type, last active time, and app version.

### 2.4 Deactivating a User

Deactivating a user, as described in the CloudDesk Chat and CloudDesk Tickets Administrator Guides, immediately terminates any active CloudDesk Mobile sessions for that user across all their devices, consistent with how deactivation revokes desktop access.

### 2.5 Handling a Lost or Stolen Device

If a user reports a lost or stolen device, administrators should immediately revoke that specific device's session under **Admin Dashboard > Mobile > Device Sessions**, rather than waiting to deactivate the user's entire account, since the user likely still needs access from other devices. See Section 5.4 for the full remote revocation procedure.

---

## 3. Roles

CloudDesk Mobile uses the same role-based structure shared across the broader Corvex Cloud platform; it does not introduce any mobile-specific roles.

### 3.1 Standard Roles and Mobile Access

- **Agent** — full mobile access to their assigned tickets and chats, mirroring their desktop permissions
- **Team Lead / Supervisor** — full mobile access to team queue views, escalation approval, and team performance snapshots, mirroring their desktop permissions
- **Administrator** — full mobile access, plus the ability to manage mobile-specific settings such as device sessions and notification policy from the Admin Dashboard
- **Read-only / Reporting user** — mobile access to condensed performance snapshots only, mirroring their desktop-equivalent restrictions

### 3.2 Custom Roles (Professional and Enterprise)

Custom roles created under **Admin Dashboard > Roles & Permissions > Custom Roles** apply identically on mobile and desktop; CloudDesk Mobile does not support configuring a different permission set for the same role across platforms.

### 3.3 Restricting Mobile Access for a Role

Administrators who wish to prevent a specific role from using CloudDesk Mobile entirely — for example, a compliance reason requiring certain data to remain accessible only from managed desktop workstations — can disable mobile access for that role under **Admin Dashboard > Mobile > Security Policy > Role Restrictions**, available on Professional and Enterprise plans.

### 3.4 Role Changes and Effective Timing

Role changes take effect immediately upon saving, including on any currently active mobile session, which will reflect updated permissions on its next sync with the server.

---

## 4. Permissions

### 4.1 Permission Categories

CloudDesk Mobile does not introduce mobile-specific permission categories; it inherits the same permission structure used across CloudDesk Chat, CloudDesk Tickets, and CloudDesk Analytics, as described in those products' Administrator Guides. The permission categories relevant to mobile use are:

- **Ticket and conversation permissions** — view, reply, transfer, resolve, escalate
- **Team visibility permissions** — team queue view, escalation approval
- **Reporting permissions** — performance snapshot access
- **Mobile-specific administrative permissions** — device session management, notification policy configuration, mobile security policy configuration

### 4.2 Mobile-Specific Administrative Permissions

Access to mobile-specific administrative functions (Sections 5–11 of this guide) is governed by a dedicated permission category, allowing administrators to grant mobile device management responsibility to a user (for example, an IT security lead) without necessarily granting broader account administrative rights, on Professional and Enterprise plans.

### 4.3 Principle of Least Privilege

As with the rest of Corvex Cloud, Corvex recommends assigning the minimum permission set necessary for each user's function. Given that mobile devices carry locally cached data, administrators should give particular thought to which roles genuinely need mobile access versus which are better served by desktop-only access.

### 4.4 Reviewing Current Permissions

Navigate to **Admin Dashboard > Roles & Permissions** to view a matrix of all roles against all permission categories, including mobile-specific administrative permissions, useful for periodic access review.

---

## 5. Security

### 5.1 Biometric Lock Policy

Administrators can configure whether biometric app lock is optional, recommended, or mandatory account-wide under **Admin Dashboard > Mobile > Security Policy > Biometric Lock**. When set to mandatory, users are required to enable biometric lock (or an equivalent device passcode, where biometric hardware is unavailable) before the app allows continued use.

### 5.2 Data Caching Limits

Administrators can set the maximum amount of case data permitted to be cached locally on a device for offline access under **Admin Dashboard > Mobile > Security Policy > Data Caching**. Lower limits reduce the amount of customer data resident on a device at any given time, at some cost to offline usability.

### 5.3 Session Timeout

Configure automatic session timeout duration specific to mobile under **Admin Dashboard > Mobile > Security Policy > Session Timeout**, independent of the desktop session timeout setting, since mobile usage patterns and risk profile often warrant a different value.

### 5.4 Remote Session Revocation

1. Navigate to **Admin Dashboard > Mobile > Device Sessions**.
2. Locate the relevant device by user, device type, or last active time.
3. Click **Revoke Session**. The device is logged out immediately on its next connectivity check-in, without requiring physical access to the device.

### 5.5 Single Sign-On (SSO)

CloudDesk Mobile uses the same account-wide SSO configuration as the rest of Corvex Cloud, where supported by the customer's identity provider's mobile authentication flow. Refer to **Admin Dashboard > Security > Single Sign-On** for configuration, available on Professional and Enterprise plans.

### 5.6 Mobile Device Management (MDM) Compatibility

For organizations managing devices through an MDM system, CloudDesk Mobile supports standard managed app configuration and remote wipe commands issued through the organization's MDM platform, in addition to the in-app remote session revocation described in Section 5.4. MDM configuration itself is performed through the organization's MDM platform, not the Corvex Admin Dashboard.

### 5.7 Data Encryption

CloudDesk Mobile encrypts data in transit (TLS 1.2+) consistent with the Corvex Cloud platform-wide standard, and locally cached data on the device is encrypted at rest using the device operating system's standard application data protection. These settings are managed by Corvex and the device operating system and are not independently configurable beyond the caching limits described in Section 5.2.

---

## 6. Audit Logs

### 6.1 What Is Logged

CloudDesk Mobile contributes the following actions to the account-wide audit log:

- Mobile session logins and logouts, including device type
- Remote session revocations, including the administrator who performed the action
- Changes to mobile security policy (biometric lock requirement, data caching limits, session timeout, role restrictions)
- All standard ticket, chat, and reporting actions performed via mobile, tagged with their originating platform for traceability

### 6.2 Viewing Audit Logs

Navigate to **Admin Dashboard > Audit Logs** and filter by platform to isolate mobile-originated entries specifically. Each entry records the action taken, the user who performed it, the device involved (where applicable), and a timestamp.

### 6.3 Retention

Audit log retention is tied to your plan tier, consistent with the Corvex Cloud Pricing Guide: 90 days on Professional, with extended custom retention available on Enterprise.

### 6.4 Exporting Audit Logs

Administrators can export audit log data as a CSV file for external record-keeping or compliance review under **Audit Logs > Export**.

### 6.5 Using Audit Logs for Device Security Review

Corvex recommends periodic review of mobile-originated audit log entries, particularly session revocation history, to confirm lost or stolen device reports were acted upon promptly and that no unexpected devices have accessed the account.

---

## 7. Backup

### 7.1 How Backup Works in CloudDesk Mobile

CloudDesk Mobile does not maintain a separate data store to back up independently; it reads from and writes to the same case data layer used by CloudDesk Chat and CloudDesk Tickets, which is covered by Corvex's infrastructure-level backup practices as described in those products' Administrator Guides. What is specific to CloudDesk Mobile, and therefore relevant to consider separately, is device-level configuration: mobile security policy settings and, on the device itself, locally cached data and unsent offline drafts.

### 7.2 Administrator-Initiated Configuration Export

1. Navigate to **Admin Dashboard > Mobile > Export Configuration**.
2. The export includes mobile security policy settings (biometric lock policy, data caching limits, session timeout, role restrictions).
3. Click **Generate Export**. The export is delivered as a downloadable JSON file.

### 7.3 Locally Cached Data and Offline Drafts

Data cached locally on a device, and any offline drafts queued for sending, exist only on that device until synced. Corvex does not back up device-local data independently, since it is, by design, a temporary local copy of data already stored durably in the account's case data layer, or a draft not yet submitted to it. Users composing a significant reply while offline should be aware that an uninstalled app or a factory-reset device before reconnection could result in the loss of that specific unsent draft.

### 7.4 Recommended Backup Cadence

Corvex recommends exporting mobile security policy configuration after any significant policy change, in addition to any regular cadence your organization maintains for other account configuration backups.

---

## 8. Restore

### 8.1 Underlying Data Restoration

Because CloudDesk Mobile reads from and writes to the same underlying case data used by CloudDesk Chat and CloudDesk Tickets, any restoration of ticket or chat data (as described in those products' Administrator Guides) is automatically reflected on mobile devices on their next sync, without any separate mobile-specific restoration step.

### 8.2 Restoring Mobile Security Policy Configuration

If mobile security policy settings need to be reverted, administrators can reference the Audit Log (Section 6) to identify the prior configuration and manually reapply it under **Admin Dashboard > Mobile > Security Policy**. Policy configuration does not currently support one-click historical rollback.

### 8.3 Restoring a Revoked Device Session

A revoked device session cannot be "restored" directly; the affected user simply logs in again on that device using their standard credentials, which establishes a new session. This is by design, since session revocation is a deliberate security action rather than an error state requiring recovery.

### 8.4 Recovering an Unsent Offline Draft

Because unsent offline drafts exist only locally on the originating device, as described in Section 7.3, there is no server-side restoration path for a draft lost due to app removal or device reset before it was sent. Administrators should communicate this limitation to agents who frequently work offline, encouraging timely reconnection to sync pending drafts.

### 8.5 Limitations

There is no self-service or Corvex-assisted mechanism to recover data that existed only as an unsynced local draft on a device that was lost, wiped, or had the application uninstalled before that data reached the server.

---

## 9. Integrations

### 9.1 Mobile-Specific Integrations Are Limited by Design

CloudDesk Mobile does not introduce its own integrations; it surfaces the results of integrations configured elsewhere in Corvex Cloud (CRM data, e-commerce data, SSO) within its mobile interface. There is no mobile-specific integration configuration screen to administer beyond what is described below.

### 9.2 Push Notification Service Integration

CloudDesk Mobile relies on standard iOS and Android push notification infrastructure to deliver alerts. This integration is managed automatically by Corvex and requires no administrator configuration, though administrators should be aware that push notification delivery is ultimately mediated by the device operating system's own settings, which the account holder controls at the device level.

### 9.3 Mobile Device Management (MDM) Integration

As described in Section 5.6, organizations using an MDM platform integrate CloudDesk Mobile through their MDM system's own application management capabilities, rather than through a Corvex-side integration configuration.

### 9.4 Single Sign-On Extension to Mobile

SSO, configured account-wide as described in Section 5.5, extends automatically to mobile login where the organization's identity provider supports a mobile-compatible authentication flow; no separate mobile SSO integration step is required.

---

## 10. Monitoring

### 10.1 Real-Time Account Monitoring

The Mobile section of the Admin Dashboard's account health summary (Section 1.3) provides real-time visibility into active mobile sessions and devices without biometric lock enabled.

### 10.2 Device Session Monitoring

Navigate to **Admin Dashboard > Mobile > Device Sessions** to view all active sessions account-wide, including user, device type, app version, and last active time. This view is the primary tool for identifying stale, unexpected, or potentially compromised sessions.

### 10.3 App Version Monitoring

Administrators can review the distribution of app versions in use across their organization from **Admin Dashboard > Mobile > Device Sessions**, useful for identifying users on an outdated version who may be missing recent functionality or security updates, and encouraging update ahead of a planned deprecation of older versions.

### 10.4 Notification Delivery Monitoring

Navigate to **Admin Dashboard > Mobile > Notification Policy > Delivery Status** to review aggregate push notification delivery success rates, useful for identifying a systemic delivery issue as opposed to an individual user's device-level notification settings.

### 10.5 Security Monitoring

The Admin Dashboard surfaces security-relevant monitoring signals specific to mobile, such as a login from an unexpected device type pattern or unusually frequent session revocations, under **Monitoring > Security Signals**, available on Professional and Enterprise plans.

---

## 11. Maintenance

### 11.1 Platform Maintenance

As a cloud-hosted service, routine platform maintenance and updates to the CloudDesk Mobile backend are managed entirely by Corvex and typically require no administrator action. App updates themselves are distributed through the Apple App Store and Google Play Store, or through your organization's MDM platform, and administrators should encourage timely adoption of updates among users.

### 11.2 Device Session Hygiene

Administrators are responsible for the ongoing maintenance of device session hygiene, including:

- Periodically reviewing active device sessions for accuracy (Section 10.2), particularly for users who may have replaced or upgraded a device without properly logging out of the old one
- Promptly revoking sessions for lost or stolen devices as reported (Section 2.5 and 5.4)
- Reviewing and updating mobile security policy settings as organizational risk tolerance or device management practices evolve

### 11.3 App Version Maintenance

Corvex periodically deprecates support for older app versions in line with underlying operating system support timelines. Administrators should monitor app version distribution (Section 10.3) and communicate update expectations to users ahead of any announced deprecation, to avoid unexpected loss of access for users on unsupported versions.

### 11.4 Notification Policy Review

Notification policy settings should be periodically reviewed to ensure they remain aligned with how the team actually uses mobile access — for example, adjusting SLA alert thresholds on mobile if they were originally set for a different staffing level.

### 11.5 Seat and Plan Maintenance

Mobile access does not consume seats independently of the underlying Corvex Cloud plan; a user's mobile access is included as part of their existing seat. Administrators should review overall seat usage as described in the CloudDesk Chat and CloudDesk Tickets Administrator Guides, rather than tracking mobile usage as a separate cost center.

---

## 12. Common Administrative Tasks

The following is a quick-reference summary of frequently performed administrative tasks and where to find them.

| Task | Location |
|---|---|
| View a user's active mobile devices | Admin Dashboard > Users > [User] > Devices |
| Revoke a lost or stolen device's session | Admin Dashboard > Mobile > Device Sessions > Revoke Session |
| Set biometric lock policy account-wide | Admin Dashboard > Mobile > Security Policy > Biometric Lock |
| Configure data caching limits | Admin Dashboard > Mobile > Security Policy > Data Caching |
| Set mobile-specific session timeout | Admin Dashboard > Mobile > Security Policy > Session Timeout |
| Restrict mobile access for a specific role | Admin Dashboard > Mobile > Security Policy > Role Restrictions |
| Review recent mobile-related administrative activity | Admin Dashboard > Audit Logs (filter by platform: Mobile) |
| Export mobile security policy configuration | Admin Dashboard > Mobile > Export Configuration |
| Review all active mobile sessions account-wide | Admin Dashboard > Mobile > Device Sessions |
| Check app version distribution across the organization | Admin Dashboard > Mobile > Device Sessions |
| Review push notification delivery status | Admin Dashboard > Mobile > Notification Policy > Delivery Status |
| Grant mobile administrative permissions to a user | Admin Dashboard > Roles & Permissions > Custom Roles |
| Review mobile-specific security signals | Admin Dashboard > Monitoring > Security Signals |
| View or revoke active user sessions (desktop and mobile) | Admin Dashboard > Security > Active Sessions |

---

*This Administrator Guide covers standard administrative functionality for CloudDesk Mobile. For information on plan-specific feature availability, refer to the CloudDesk Mobile Product Overview and the Corvex Cloud Pricing Guide. For end-user instructions, refer to the CloudDesk Mobile User Manual.*
