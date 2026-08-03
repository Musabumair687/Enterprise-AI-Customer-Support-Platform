# CloudDesk API Platform
## Administrator Guide

*Corvex Cloud — CloudDesk API Platform*
*This guide covers administrative configuration and operation of CloudDesk API Platform. It is intended for account administrators and IT/security staff responsible for managing the platform. For developer-focused usage instructions, refer to the CloudDesk API Platform User Manual. For pricing and plan details, refer to the Corvex Cloud Pricing Guide.*

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

The Admin Dashboard is the central console for configuring and overseeing your organization's use of CloudDesk API Platform. It is accessible only to users with the Administrator role and is shared with the broader Corvex Cloud Admin Dashboard used to administer CloudDesk Chat, CloudDesk Tickets, and CloudDesk Analytics, since all modules operate on one account.

### 1.1 Accessing the Admin Dashboard

1. Log in to Corvex Cloud with an account holding the Administrator role.
2. Click your profile icon in the bottom-left corner and select **Admin Dashboard**.
3. Navigate to the **API Platform** section within the Admin Dashboard, or open the Developer Portal directly, to reach API-specific administrative settings.

### 1.2 Dashboard Layout

The API Platform section of the Admin Dashboard is organized as follows, each covered in detail later in this guide:

- **API Keys** — account-wide view of all issued API keys, their scopes, and their owners
- **Webhooks** — account-wide view of all configured webhook endpoints
- **Developer Access** — manage which users can access the Developer Portal and at what scope
- **Rate Limits & Usage** — monitor account-wide API consumption against plan limits
- **Sandbox Management** — (Enterprise) oversee the sandbox environment
- **Security** — SSO, IP allowlisting, and key rotation policy
- **Audit Logs** — a searchable record of API-related administrative activity

### 1.3 Account Health Summary

The API Platform section of the Admin Dashboard displays a summary panel showing the number of active API keys, configured webhooks, current usage against your plan's rate limit, and any outstanding security recommendations, such as an API key that has not been rotated within your organization's configured policy window.

### 1.4 Who Should Have Admin Dashboard Access

Corvex recommends limiting Administrator role assignment to a small number of trusted individuals — typically IT, security, or engineering leads — given that API Platform administration involves direct control over programmatic access to your organization's support data.

---

## 2. User Management

### 2.1 Viewing Users and Developer Access

Navigate to **Admin Dashboard > Users** to view all users on your account. CloudDesk API Platform does not maintain a separate user list; instead, it uses the same account-wide user list shared with the rest of Corvex Cloud, with Developer Portal access and API key ownership layered on top.

### 2.2 Granting Developer Portal Access

For users who need to manage API keys or webhooks but may not need agent-level chat or ticket access (for example, a backend engineer):

1. Click **Invite User** from **Admin Dashboard > Users**, or select an existing user.
2. Assign a role that includes Developer Portal access (Section 3).
3. If the user is new, they will receive a standard email invitation as described in the CloudDesk API Platform User Manual.

### 2.3 Managing API Key Ownership

Each API key is associated with the user who created it, visible under **Admin Dashboard > API Platform > API Keys**. Administrators can view key ownership account-wide, which is particularly useful when a key's original creator has since left the organization.

### 2.4 Deactivating a User

Deactivating a user does not automatically revoke API keys they created; keys continue to function until explicitly revoked, since they are frequently tied to system-level integrations that should keep running independently of any individual's employment status. Administrators should review a departing user's owned API keys, described further in Section 2.5, as part of standard offboarding.

### 2.5 Offboarding Checklist for Developer Users

When deactivating a user with Developer Portal access, Corvex recommends:

1. Reviewing all API keys owned by the user under **API Platform > API Keys**, filtered by owner.
2. Reassigning any keys tied to ongoing, business-critical integrations to a service-oriented owner or another team member.
3. Rotating or revoking any keys not clearly tied to an ongoing integration.
4. Reviewing any webhook endpoints configured by the user for continued validity.

---

## 3. Roles

CloudDesk API Platform uses the same role-based structure shared across the broader Corvex Cloud platform, with API-specific access layered on top.

### 3.1 Standard Roles and API Access

- **Agent** — no Developer Portal access by default
- **Team Lead / Supervisor** — no Developer Portal access by default
- **Administrator** — full Developer Portal access, including API key management, webhook configuration, and account-wide usage monitoring
- **Developer / Integration user** — a role (or custom role addition) specifically granting Developer Portal access, with API key scope (read-only or read/write) governed by the account's plan and the individual key's configuration

### 3.2 Custom Roles (Professional and Enterprise)

Administrators can create custom roles under **Admin Dashboard > Roles & Permissions > Custom Roles** that grant Developer Portal access without full administrative rights elsewhere in the platform — for example, an engineer who should manage API keys and webhooks but not user accounts or billing.

### 3.3 Assigning Developer Portal Access

Developer Portal access can be granted as part of a user's primary role or added independently via custom role configuration, without requiring every developer to hold the full Administrator role.

### 3.4 Role Changes and Effective Timing

Role changes take effect immediately upon saving. Revoking Developer Portal access from a user does not affect API keys they have already created; those keys remain active and manageable by other authorized users until explicitly revoked.

---

## 4. Permissions

### 4.1 Permission Categories

API Platform permissions fall into several categories, each independently configurable for custom roles on Professional and Enterprise plans:

- **API key permissions** — create, view, rotate, revoke keys; view keys owned by others
- **Webhook permissions** — create, edit, delete webhook endpoints; view delivery history
- **Usage and monitoring permissions** — view account-wide rate limit and usage data
- **Sandbox permissions** — (Enterprise) access to and configuration of the sandbox environment
- **Security permissions** — manage IP allowlisting and key rotation policy specific to API access

### 4.2 Read-Only vs. Read/Write Key Scope

Independent of a user's Developer Portal role, individual API keys are scoped as read-only or read/write at creation time. Read/write access is available only on Professional and Enterprise plans; Starter accounts are limited to read-only API access account-wide.

### 4.3 Principle of Least Privilege

Corvex recommends creating API keys scoped to the minimum access level and, where relevant, the minimum set of endpoints required for a given integration's purpose, rather than issuing broad read/write keys by default.

### 4.4 Reviewing Current Permissions

Navigate to **Admin Dashboard > Roles & Permissions** to view a matrix of all roles (standard and custom) against Developer Portal permission categories, useful for periodic access review.

---

## 5. Security

### 5.1 Single Sign-On (SSO)

CloudDesk API Platform uses the same account-wide SSO configuration as the rest of Corvex Cloud; no separate SSO setup is required for Developer Portal access. Refer to **Admin Dashboard > Security > Single Sign-On** for configuration, available on Professional and Enterprise plans.

### 5.2 IP Allowlisting

IP allowlisting configured under **Admin Dashboard > Security > IP Allowlisting** can be applied to API requests as well as standard workspace access, available on Professional and Enterprise plans. Administrators can configure API-specific IP allowlisting separately from Developer Portal login access under **Admin Dashboard > API Platform > Security**.

### 5.3 API Key Rotation Policy

Administrators can define a recommended or mandatory key rotation interval under **Admin Dashboard > API Platform > Security > Key Rotation Policy**. Keys approaching or exceeding the configured interval are flagged in the Account Health Summary (Section 1.3) and, where mandatory rotation is enabled, may be automatically disabled until rotated.

### 5.4 Webhook Endpoint Verification

CloudDesk API Platform signs all webhook payloads, allowing receiving systems to verify authenticity. Administrators should confirm that any team building a webhook integration implements signature verification, consistent with the guidance in the CloudDesk API Platform User Manual.

### 5.5 Data Encryption

All API and webhook traffic is HTTPS-only, and underlying data is encrypted in transit (TLS 1.2+) and at rest (AES-256), consistent with the Corvex Cloud platform-wide standard. These settings are managed by Corvex and are not independently configurable.

### 5.6 SCIM Provisioning (Enterprise)

Enterprise customers can configure SCIM-based user provisioning under **Admin Dashboard > Security > SCIM**, which extends to Developer Portal access assignment as part of a user's broader provisioned role.

### 5.7 Rate Limiting as a Security Control

In addition to protecting platform stability, standard rate limiting (Section 10) serves as a security control against unauthorized bulk data extraction. Administrators should treat an unexpected, sustained increase in a key's usage as a signal worth investigating, not only a capacity concern.

---

## 6. Audit Logs

### 6.1 What Is Logged

CloudDesk API Platform contributes the following actions to the account-wide audit log:

- API key creation, rotation, and revocation, including the creating or acting user
- Webhook endpoint creation, modification, and deletion
- Changes to Developer Portal access for any user or role
- IP allowlisting and key rotation policy changes
- Sandbox environment access and configuration changes (Enterprise)

### 6.2 Viewing Audit Logs

Navigate to **Admin Dashboard > Audit Logs** and filter by category to isolate API Platform-related entries. Each entry records the action taken, the user who performed it, and a timestamp.

### 6.3 Retention

Audit log retention is tied to your plan tier, consistent with the Corvex Cloud Pricing Guide: 90 days on Professional, with extended custom retention available on Enterprise.

### 6.4 Exporting Audit Logs

Administrators can export audit log data as a CSV file for external record-keeping or compliance review under **Audit Logs > Export**.

### 6.5 Using Audit Logs for Security Review

Because API keys represent standing, programmatic access to support data, Corvex strongly recommends periodic audit log review specifically for API key creation and usage patterns, particularly following a security incident, an employee departure, or a broader security review cycle.

---

## 7. Backup

### 7.1 How Backup Works in CloudDesk API Platform

CloudDesk API Platform does not maintain a separate data store to back up independently; API requests read from and write to the same case data layer used by CloudDesk Chat and CloudDesk Tickets, which is covered by Corvex's infrastructure-level backup practices as described in those products' Administrator Guides. What is specific to the API Platform, and therefore relevant to back up independently, is its configuration: API key metadata (names, scopes, and ownership, though not key secret values themselves), webhook endpoint configuration, and rate limit or rotation policy settings.

### 7.2 Administrator-Initiated Configuration Export

1. Navigate to **Admin Dashboard > API Platform > Export Configuration**.
2. Select the scope: API key metadata, webhook configuration, or security policy settings.
3. Click **Generate Export**. The export is delivered as a downloadable JSON file describing the selected configuration.

### 7.3 Important Note on API Key Secrets

Because API key secret values are displayed only once at creation time and are not retrievable afterward for security reasons, configuration exports include key metadata (name, scope, owner, creation date) but never the key secret itself. Organizations should maintain their own secure record of active key values as they are issued, separate from any Corvex-provided export.

### 7.4 Recommended Backup Cadence

Corvex recommends exporting API Platform configuration after any significant change to key issuance patterns, webhook architecture, or security policy, in addition to any regular cadence your organization maintains for other account configuration backups.

---

## 8. Restore

### 8.1 Underlying Data Restoration

Because CloudDesk API Platform reads from and writes to the same underlying case data used by CloudDesk Chat and CloudDesk Tickets, any restoration of ticket or chat data (as described in those products' Administrator Guides) is automatically reflected in data accessible via the API without any separate API Platform-specific restoration step.

### 8.2 Restoring a Deleted Webhook Configuration

1. Navigate to **Admin Dashboard > Data > Recently Deleted**.
2. Locate the deleted webhook endpoint configuration using search or filters.
3. Click **Restore**. The webhook configuration is returned with its prior endpoint URL and event subscriptions intact, provided the deletion occurred within the account's recovery window (30 days on Professional; extended windows available on Enterprise).

### 8.3 Restoring a Revoked API Key

Revoked API keys cannot be restored, since the underlying key secret is permanently invalidated upon revocation for security reasons. If an integration needs to resume, a new key must be generated and the secret value updated in the consuming system, as described in the CloudDesk API Platform User Manual.

### 8.4 Restoring from a Configuration Export

If your organization maintains its own configuration exports as described in Section 7.2, restoring webhook or policy configuration from an export is not a self-service Admin Dashboard action. Contact Corvex Customer Success to coordinate reimporting exported configuration; note that API key secrets cannot be restored under any circumstances, consistent with Section 8.3.

### 8.5 Limitations

Because key secrets are never retrievable or restorable once issued, administrators should treat API key revocation as a deliberate, difficult-to-reverse action and communicate clearly with any team relying on the key before revoking it.

---

## 9. Integrations

### 9.1 The API Platform as the Foundation for Integrations

Unlike CloudDesk Chat, Tickets, or Analytics, where "Integrations" refers primarily to connecting third-party systems, CloudDesk API Platform is itself the foundation those integrations are built on. This section covers administering the integrations and ecosystem connections that exist because of the API Platform, rather than configuring a separate integration into the API Platform.

### 9.2 Corvex Integration Marketplace

Navigate to **Admin Dashboard > Integrations > Marketplace** to view and manage native integrations — built by Corvex or by technology partners — that your organization has connected. Each marketplace integration operates using API credentials managed transparently on your behalf, distinct from customer-created API keys.

### 9.3 Custom, Customer-Built Integrations

Integrations your own team builds using API keys and webhooks are not centrally listed in the Marketplace section, since they are not Corvex- or partner-published. Administrators should maintain their own internal record of custom integrations, cross-referenced against **API Platform > API Keys** for visibility into what each key is used for.

### 9.4 Corvex Partner API (Enterprise)

Enterprise customers with access to the Corvex partner API for bespoke internal system connections can manage partner API credentials under **Admin Dashboard > API Platform > Partner API**, separate from standard customer-facing API keys.

### 9.5 Priority Support and Custom Integration Requests

Professional and Enterprise administrators can submit a request for Corvex-assisted custom integration support directly from **Admin Dashboard > API Platform > Request Integration Support**, routing the request to the appropriate Corvex team based on plan tier.

---

## 10. Monitoring

### 10.1 Real-Time Account Monitoring

The API Platform section of the Admin Dashboard's account health summary (Section 1.3) provides real-time visibility into active API keys, configured webhooks, and current rate limit usage.

### 10.2 Rate Limit and Usage Monitoring

Navigate to **Admin Dashboard > API Platform > Rate Limits & Usage** to review request volume over time, broken down by API key, useful for identifying which integration is consuming the most capacity and whether any key is approaching its rate limit.

### 10.3 Webhook Delivery Monitoring

Navigate to **Admin Dashboard > API Platform > Webhooks** to review delivery success and failure history for each configured endpoint, including response codes returned by the receiving system, useful for diagnosing a failing integration without needing to instrument the receiving system's own logs first.

### 10.4 Sandbox Monitoring (Enterprise)

Enterprise administrators can monitor sandbox environment usage separately from production under **Admin Dashboard > API Platform > Sandbox Management**, useful for confirming a team is validating integrations appropriately before deploying to production.

### 10.5 Security Monitoring

The Admin Dashboard surfaces security-relevant monitoring signals specific to API usage, such as an unexpected surge in request volume from a single key or repeated authentication failures, under **Monitoring > Security Signals**, available on Professional and Enterprise plans.

---

## 11. Maintenance

### 11.1 Platform Maintenance

As a cloud-hosted service, routine platform maintenance and updates are managed entirely by Corvex and typically require no administrator action. Corvex schedules maintenance windows to minimize disruption and communicates any maintenance expected to have visible impact, including any planned API endpoint deprecations, through the Corvex Cloud status page and developer documentation.

### 11.2 API Key Lifecycle Maintenance

Administrators are responsible for the ongoing maintenance of API key hygiene, including:

- Rotating keys according to the organization's configured policy (Section 5.3)
- Revoking keys tied to integrations that are no longer in use
- Reviewing key ownership after any relevant employee departure (Section 2.5)

### 11.3 Webhook Endpoint Maintenance

Periodically review configured webhook endpoints for continued validity, particularly after a receiving system's infrastructure changes (for example, a URL migration), to avoid silent delivery failures accumulating unnoticed.

### 11.4 API Version and Deprecation Awareness

Administrators, or the developers they designate, should monitor Corvex's developer documentation and status communications for any announced API version changes or endpoint deprecations, and plan integration updates accordingly ahead of any announced transition deadline.

### 11.5 Seat and Plan Maintenance

Review current API usage patterns against your plan's rate limits regularly, particularly ahead of renewal or before launching a new high-volume integration, to determine whether a plan change or a custom Enterprise rate limit is warranted. Refer to the Corvex Cloud Pricing Guide for upgrade, downgrade, and renewal terms.

---

## 12. Common Administrative Tasks

The following is a quick-reference summary of frequently performed administrative tasks and where to find them.

| Task | Location |
|---|---|
| Grant a user Developer Portal access | Admin Dashboard > Users > [User] > Edit Role |
| View all API keys account-wide | Admin Dashboard > API Platform > API Keys |
| Set an API key rotation policy | Admin Dashboard > API Platform > Security > Key Rotation Policy |
| Reassign or revoke a departing user's API keys | Admin Dashboard > API Platform > API Keys (filter by owner) |
| Review recent API-related administrative activity | Admin Dashboard > Audit Logs |
| Export API Platform configuration | Admin Dashboard > API Platform > Export Configuration |
| Restore a deleted webhook configuration | Admin Dashboard > Data > Recently Deleted |
| Review rate limit usage by key | Admin Dashboard > API Platform > Rate Limits & Usage |
| Review webhook delivery success/failure history | Admin Dashboard > API Platform > Webhooks |
| Manage a marketplace integration | Admin Dashboard > Integrations > Marketplace |
| Request Corvex-assisted custom integration support | Admin Dashboard > API Platform > Request Integration Support |
| Monitor sandbox usage (Enterprise) | Admin Dashboard > API Platform > Sandbox Management |
| Configure IP allowlisting for API access | Admin Dashboard > API Platform > Security |
| Manage Corvex partner API credentials (Enterprise) | Admin Dashboard > API Platform > Partner API |
| View or revoke active user sessions | Admin Dashboard > Security > Active Sessions |

---

*This Administrator Guide covers standard administrative functionality for CloudDesk API Platform. For information on plan-specific feature availability, refer to the CloudDesk API Platform Product Overview and the Corvex Cloud Pricing Guide. For developer-focused usage instructions, refer to the CloudDesk API Platform User Manual.*
