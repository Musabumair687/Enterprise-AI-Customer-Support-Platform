# CloudDesk Tickets
## Administrator Guide

*Corvex Cloud — CloudDesk Tickets*
*This guide covers administrative configuration and operation of CloudDesk Tickets. It is intended for account administrators and IT/security staff responsible for managing the platform. For end-user instructions, refer to the CloudDesk Tickets User Manual. For pricing and plan details, refer to the Corvex Cloud Pricing Guide.*

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

The Admin Dashboard is the central console for configuring and overseeing your organization's CloudDesk Tickets deployment. It is accessible only to users with the Administrator role and is separate from the standard agent workspace described in the CloudDesk Tickets User Manual.

### 1.1 Accessing the Admin Dashboard

1. Log in to CloudDesk Tickets with an account holding the Administrator role.
2. Click your profile icon in the bottom-left corner and select **Admin Dashboard**.
3. You will be taken to the administrative console, distinguished visually from the agent workspace by a persistent header bar and a different left navigation structure.

If your organization also uses CloudDesk Chat, the Admin Dashboard is shared across both products — administrative changes made in one context (for example, a new user invitation) are reflected consistently across the account.

### 1.2 Dashboard Layout

The Admin Dashboard is organized into the following sections, each covered in detail later in this guide:

- **Users** — manage agent, team lead, and administrator accounts
- **Roles & Permissions** — configure access levels and custom permission sets
- **Workflow & Channels** — configure ticket statuses, fields, SLAs, assignment rules, and connected channels
- **Security** — SSO, IP allowlisting, session policies, and data handling settings
- **Audit Logs** — a searchable record of administrative and security-relevant activity
- **Integrations** — manage connected CRM, e-commerce, project management, and API integrations
- **Billing & Plan** — view current plan, seat usage, and billing details (linked to the Corvex Cloud Pricing Guide)

### 1.3 Account Health Summary

The top of the Admin Dashboard displays a summary panel showing current seat usage against your plan's limits, storage usage, open ticket backlog size, and any outstanding security recommendations Corvex has flagged for your account.

### 1.4 Who Should Have Admin Dashboard Access

Corvex recommends limiting Administrator role assignment to a small number of trusted individuals — typically IT, security, or designated support operations leads — consistent with the principle of least privilege described further in Section 4.

---

## 2. User Management

### 2.1 Viewing Users

Navigate to **Admin Dashboard > Users** to view a list of all users on your account, including their role, status (Active, Invited, Deactivated), and last login date.

### 2.2 Inviting a New User

1. Click **Invite User**.
2. Enter the user's name and email address.
3. Assign a role (Section 3) and, if applicable, a team.
4. Click **Send Invitation**. The user will receive an email invitation as described in the CloudDesk Tickets User Manual.

### 2.3 Bulk User Invitation

For onboarding larger teams, administrators can upload a CSV file of users under **Users > Bulk Invite**, specifying name, email, role, and team for each row. This is available on all plans, though the practical seat minimums and maximums described in the Corvex Cloud Pricing Guide still apply.

### 2.4 Editing a User

Click any user from the list to update their role, team assignment, or display information. Editing a user's role takes effect immediately.

### 2.5 Deactivating a User

1. Select the user and click **Deactivate**.
2. Deactivated users lose login access immediately but their historical activity (tickets handled, notes added, macros used) remains intact in the account's records.
3. Deactivating a user frees the associated seat, which may then be reassigned to a new invitation.
4. Tickets still assigned to a deactivated user should be reassigned manually or through an assignment rule fallback; deactivation does not automatically reassign open tickets.

### 2.6 Reactivating a User

Deactivated users can be reactivated from the same list within **Users > Deactivated**, restoring their prior role and team assignment unless manually changed.

### 2.7 Removing a User Permanently

Permanent removal (as opposed to deactivation) is available under **Users > [User] > Remove Permanently** and is intended for cases such as an employee departure combined with a data handling requirement. Corvex recommends deactivation over permanent removal in most cases, since deactivation preserves historical record integrity for reporting and audit purposes.

---

## 3. Roles

CloudDesk Tickets uses a role-based structure that is consistent across the broader Corvex Cloud platform, ensuring a user's permissions behave the same way whether they're working in CloudDesk Tickets, CloudDesk Chat, or CloudDesk Analytics.

### 3.1 Standard Roles

- **Agent** — works assigned and queued tickets; no administrative or configuration access
- **Team Lead / Supervisor** — includes all Agent capabilities, plus visibility into team-wide queues, the ability to reassign tickets, and access to team-level reporting
- **Administrator** — full configuration access, including workflow setup, SLA management, integrations, security settings, and user management
- **Read-only / Reporting user** — (Professional and Enterprise) view access to reporting without ticket or configuration access

### 3.2 Custom Roles (Professional and Enterprise)

Administrators can create custom roles under **Admin Dashboard > Roles & Permissions > Custom Roles**, combining specific permissions (Section 4) outside the standard role definitions. This is useful for scenarios such as a compliance reviewer who needs read access to tickets and audit logs but no reply or configuration ability.

### 3.3 Assigning Roles

Roles are assigned per user, either individually or via bulk invitation, as described in Section 2. A user may hold only one role at a time within CloudDesk Tickets, though custom roles can be configured to closely match a blended set of responsibilities where needed.

### 3.4 Role Changes and Effective Timing

Role changes take effect immediately upon saving. If a user is actively logged in when their role changes, updated permissions apply on their next action or page refresh.

---

## 4. Permissions

### 4.1 Permission Categories

Permissions in CloudDesk Tickets fall into several categories, each independently configurable for custom roles on Professional and Enterprise plans:

- **Ticket permissions** — view, reply, reassign, merge/split, delete, change status or priority
- **Configuration permissions** — statuses, fields, SLAs, assignment rules, macro management
- **User management permissions** — invite, edit, deactivate users; assign roles
- **Reporting permissions** — view standard reports, view custom dashboards, export data
- **Security permissions** — manage SSO, IP allowlisting, audit log access
- **Integration permissions** — connect, configure, or remove integrations and API keys

### 4.2 Principle of Least Privilege

Corvex recommends assigning the minimum permission set necessary for each user's function. Standard roles (Section 3.1) are designed to reflect common, sensible permission groupings; custom roles should be used deliberately rather than as a default approach to account setup.

### 4.3 Reviewing Current Permissions

Navigate to **Admin Dashboard > Roles & Permissions** to view a matrix of all roles (standard and custom) against all permission categories, useful for periodic access review.

### 4.4 Permission Inheritance

Team Lead and Administrator roles inherit all Agent-level ticket permissions by default; this inheritance is not configurable for standard roles but can be adjusted when building a custom role from scratch.

---

## 5. Security

### 5.1 Single Sign-On (SSO)

Available on Professional and Enterprise plans, SSO via SAML 2.0 can be configured under **Admin Dashboard > Security > Single Sign-On**.

1. Enter your identity provider's metadata URL or upload the metadata file.
2. Map required attributes (name, email) according to your identity provider's configuration.
3. Test the connection using the provided test login flow before enforcing SSO account-wide.
4. Once verified, choose whether to make SSO optional or mandatory for all users.

### 5.2 IP Allowlisting

Available on Professional and Enterprise plans, IP allowlisting restricts agent workspace and Admin Dashboard access to specified IP ranges. Configure this under **Admin Dashboard > Security > IP Allowlisting**. Corvex recommends maintaining a documented list of approved ranges and reviewing it periodically, particularly after office location or VPN infrastructure changes.

### 5.3 Password Policy

For accounts not using SSO, administrators can configure password complexity requirements and expiration intervals under **Admin Dashboard > Security > Password Policy**.

### 5.4 Session Management

Configure automatic session timeout duration under **Admin Dashboard > Security > Sessions**. Administrators can also view and remotely revoke active sessions for any user, including CloudDesk Mobile sessions, from **Security > Active Sessions**.

### 5.5 Data Encryption

CloudDesk Tickets encrypts data in transit (TLS 1.2+) and at rest (AES-256) by default, consistent with the Corvex Cloud platform-wide standard. These settings are managed by Corvex and are not independently configurable, ensuring a consistent security baseline across all accounts.

### 5.6 Data Residency (Enterprise)

Enterprise customers with regional compliance requirements can request specific data residency configurations through their Customer Success Manager; this is established during contracting rather than through a self-service Admin Dashboard toggle.

### 5.7 SCIM Provisioning (Enterprise)

Enterprise customers can configure SCIM-based user provisioning under **Admin Dashboard > Security > SCIM**, allowing user creation, role assignment, and deactivation to be managed automatically from your identity provider.

---

## 6. Audit Logs

### 6.1 What Is Logged

CloudDesk Tickets maintains an audit log of security- and configuration-relevant actions, including:

- User invitations, role changes, deactivations, and removals
- Workflow configuration changes (statuses, fields, SLAs, assignment rules)
- Ticket deletions and merges
- SSO, IP allowlisting, and password policy changes
- API key creation, rotation, and deletion
- Integration connections and removals
- Data export actions

### 6.2 Viewing Audit Logs

Navigate to **Admin Dashboard > Audit Logs**. Each entry records the action taken, the user who performed it, and a timestamp. Use the filter and search tools to narrow results by user, action type, or date range.

### 6.3 Retention

Audit log retention is tied to your plan tier, consistent with the Corvex Cloud Pricing Guide: 90 days on Professional, with extended custom retention available on Enterprise.

### 6.4 Exporting Audit Logs

Administrators can export audit log data as a CSV file for external record-keeping or compliance review under **Audit Logs > Export**.

### 6.5 Using Audit Logs for Security and Process Review

Corvex recommends periodic review of audit logs, particularly after a role change, an offboarding, a workflow redesign, or a suspected security incident, to confirm that account activity and configuration changes match expectations.

---

## 7. Backup

### 7.1 How Backup Works in CloudDesk Tickets

As a cloud-hosted service, CloudDesk Tickets data is not backed up using traditional local or on-premises backup tools. Instead, Corvex maintains infrastructure-level backups of all customer data as part of the underlying platform's operational reliability practices, covering ticket history, customer records, and configuration data such as workflows, fields, and SLAs.

### 7.2 Administrator-Initiated Data Export

In addition to Corvex-managed infrastructure backups, administrators can perform their own data exports for independent recordkeeping:

1. Navigate to **Admin Dashboard > Data > Export**.
2. Select the data scope: ticket history, customer records, or full account configuration (statuses, fields, SLAs, assignment rules).
3. Choose a date range, if applicable.
4. Click **Generate Export**. Larger exports are prepared asynchronously and delivered as a downloadable file with a notification when ready.

### 7.3 Export Formats

Standard exports are provided in CSV format for tabular data (e.g., ticket lists, customer records) and JSON format for structured configuration data (e.g., workflow rules, SLA definitions).

### 7.4 Recommended Export Cadence

While Corvex maintains infrastructure-level backups independent of any customer action, organizations with internal data governance requirements may choose to schedule periodic manual exports (for example, monthly or quarterly) as an additional, independently controlled recordkeeping practice.

---

## 8. Restore

### 8.1 Corvex-Managed Restoration

In the event of a platform-level incident affecting customer data, Corvex's infrastructure team is responsible for restoring affected data from managed backups, consistent with the reliability commitments described in your account's service agreement. This process does not require administrator action to initiate, though Corvex will communicate with affected customers as appropriate during any such incident.

### 8.2 Restoring Individual Tickets or Records

For more routine situations — such as a ticket accidentally deleted by an agent, or a merge performed in error — administrators can restore individual items under **Admin Dashboard > Data > Recently Deleted**, provided the deletion occurred within the account's recovery window (30 days on Starter and Professional; extended windows available on Enterprise).

1. Navigate to **Admin Dashboard > Data > Recently Deleted**.
2. Locate the deleted or merged ticket using search or filters.
3. Click **Restore**. The item is returned to its prior state, including associated tags, fields, and notes.

### 8.3 Restoring a Workflow Configuration

If a workflow change (a status, field, or SLA edit) needs to be reverted, administrators can reference the Audit Log (Section 6) to identify the prior configuration and manually reapply it under **Workflow & Channels**. Workflow configuration does not currently support one-click historical rollback and should be changed deliberately, ideally after testing in a sandbox environment where available (Enterprise).

### 8.4 Restoring from a Prior Export

If your organization maintains its own periodic exports as described in Section 7.4, restoring from an export is not a self-service Admin Dashboard action, since it involves reintroducing historical data into a live account. Contact Corvex Customer Success to coordinate a restoration of this kind.

### 8.5 Limitations

Items permanently removed (as opposed to deactivated or routinely deleted) may fall outside the standard recovery window described in Section 8.2. Administrators should use permanent removal actions deliberately, understanding that some such actions may not be reversible through self-service tools.

---

## 9. Integrations

### 9.1 Managing Integrations

Navigate to **Admin Dashboard > Integrations** to view, add, or remove integrations connected to your CloudDesk Tickets account.

### 9.2 Native Integrations

Available native integrations (CRM, e-commerce, project management and engineering tools, collaboration tools) are listed with a **Connect** button. Selecting one walks you through an authentication flow specific to that integration, consistent with the integration categories described in the CloudDesk Tickets Product Overview. Native integrations beyond a limited starter set require a Professional or Enterprise plan.

### 9.3 Zapier

Zapier connections are configured from the Zapier platform itself, using an API key generated under **Admin Dashboard > Integrations > Zapier > Generate Key**. Starter plans have access to a limited set of Zapier-based connections; Professional and Enterprise have full access.

### 9.4 API Keys and Webhooks

Full management of API keys and webhooks is handled through the CloudDesk API Platform Developer Portal, linked from **Admin Dashboard > Integrations > Developer Portal**, rather than duplicated within the CloudDesk Tickets Admin Dashboard itself.

### 9.5 Removing an Integration

Select any connected integration and click **Disconnect**. Disconnecting an integration halts data sync going forward but does not delete data previously synced or created as a result of that integration.

### 9.6 Integration Health Monitoring

The Integrations section displays a status indicator for each connected integration (Healthy, Warning, Error), allowing administrators to quickly identify a failing sync — for example, a broken project-tool link — without needing to investigate individual tickets first.

---

## 10. Monitoring

### 10.1 Real-Time Account Monitoring

The Admin Dashboard's account health summary (Section 1.3) provides a real-time view of seat usage, storage usage, open ticket backlog, and outstanding security recommendations.

### 10.2 Service Status

Corvex publishes platform-wide service status, including any active incidents or scheduled maintenance, at the Corvex Cloud status page. Administrators can subscribe to status updates by email or webhook from **Admin Dashboard > Monitoring > Status Subscriptions**.

### 10.3 Usage Monitoring

Navigate to **Admin Dashboard > Monitoring > Usage** to review seat utilization, storage consumption, and, where applicable, API usage against your plan's rate limits, supporting proactive plan management before limits are reached.

### 10.4 SLA and Backlog Monitoring

Administrators can monitor account-wide SLA compliance and backlog trends directly from **Monitoring > SLA Overview**, providing a higher-level view than any individual team lead's queue monitoring, useful for identifying systemic staffing or process issues.

### 10.5 Security Monitoring

The Admin Dashboard surfaces security-relevant monitoring signals, such as repeated failed login attempts or logins from unexpected locations, under **Monitoring > Security Signals**, available on Professional and Enterprise plans.

---

## 11. Maintenance

### 11.1 Platform Maintenance

As a cloud-hosted service, routine platform maintenance and updates are managed entirely by Corvex and typically require no administrator action. Corvex schedules maintenance windows to minimize disruption and communicates any maintenance expected to have visible impact through the status page referenced in Section 10.2.

### 11.2 Configuration Maintenance

Administrators are responsible for the ongoing maintenance of their account's configuration, including:

- Periodically reviewing user accounts for accuracy (Section 2)
- Reviewing roles and permissions for continued appropriateness (Sections 3–4)
- Auditing connected integrations for continued relevance (Section 9)
- Reviewing security settings, particularly after organizational changes such as office relocations or identity provider migrations

### 11.3 Workflow, Field, and Macro Hygiene

Over time, ticket fields, tags, and macro libraries can accumulate unused or duplicate entries, particularly as teams and processes evolve. Corvex recommends a periodic review (quarterly or semi-annually, depending on team size) to archive unused fields and macros and consolidate overlapping tags, keeping reporting in CloudDesk Analytics meaningful.

### 11.4 SLA Review

SLA targets should be periodically reviewed against actual team performance and staffing levels. An SLA that is consistently missed may indicate a staffing gap rather than a process failure, and should prompt a staffing or workflow conversation rather than repeated escalation alone.

### 11.5 Seat and Plan Maintenance

Review current seat usage against your plan regularly, particularly ahead of renewal, to ensure your organization is neither paying for significantly underused seats nor approaching a plan limit unexpectedly. Refer to the Corvex Cloud Pricing Guide for upgrade, downgrade, and renewal terms.

---

## 12. Common Administrative Tasks

The following is a quick-reference summary of frequently performed administrative tasks and where to find them.

| Task | Location |
|---|---|
| Invite a new agent | Admin Dashboard > Users > Invite User |
| Deactivate a departing employee | Admin Dashboard > Users > [User] > Deactivate |
| Create a custom role | Admin Dashboard > Roles & Permissions > Custom Roles |
| Enable SSO | Admin Dashboard > Security > Single Sign-On |
| Configure IP allowlisting | Admin Dashboard > Security > IP Allowlisting |
| Review recent administrative activity | Admin Dashboard > Audit Logs |
| Export ticket data | Admin Dashboard > Data > Export |
| Restore an accidentally deleted ticket | Admin Dashboard > Data > Recently Deleted |
| Connect a CRM or project management integration | Admin Dashboard > Integrations > [Integration Name] > Connect |
| Generate a Zapier API key | Admin Dashboard > Integrations > Zapier > Generate Key |
| Check current seat and storage usage | Admin Dashboard > Monitoring > Usage |
| Review account-wide SLA compliance | Admin Dashboard > Monitoring > SLA Overview |
| Subscribe to platform status updates | Admin Dashboard > Monitoring > Status Subscriptions |
| Review team-wide permissions | Admin Dashboard > Roles & Permissions |
| Add or edit a custom ticket field | Admin Dashboard > Workflow & Channels > Fields |
| Update SLA targets | Admin Dashboard > Workflow & Channels > SLAs |
| View or revoke active user sessions | Admin Dashboard > Security > Active Sessions |

---

*This Administrator Guide covers standard administrative functionality for CloudDesk Tickets. For information on plan-specific feature availability, refer to the CloudDesk Tickets Product Overview and the Corvex Cloud Pricing Guide. For end-user instructions, refer to the CloudDesk Tickets User Manual.*
