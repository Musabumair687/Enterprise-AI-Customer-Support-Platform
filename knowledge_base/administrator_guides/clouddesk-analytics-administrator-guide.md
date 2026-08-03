# CloudDesk Analytics
## Administrator Guide

*Corvex Cloud — CloudDesk Analytics*
*This guide covers administrative configuration and operation of CloudDesk Analytics. It is intended for account administrators and IT/security staff responsible for managing the platform. For end-user instructions, refer to the CloudDesk Analytics User Manual. For pricing and plan details, refer to the Corvex Cloud Pricing Guide.*

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

The Admin Dashboard is the central console for configuring and overseeing your organization's CloudDesk Analytics deployment. It is accessible only to users with the Administrator role and is shared with the broader Corvex Cloud Admin Dashboard used to administer CloudDesk Chat and CloudDesk Tickets, since all three modules operate on one account.

### 1.1 Accessing the Admin Dashboard

1. Log in to Corvex Cloud with an account holding the Administrator role.
2. Click your profile icon in the bottom-left corner and select **Admin Dashboard**.
3. Navigate to the **Analytics** section within the Admin Dashboard to reach reporting-specific administrative settings.

### 1.2 Dashboard Layout

The Analytics section of the Admin Dashboard is organized as follows, each covered in detail later in this guide:

- **Report Access** — manage which users and roles can view standard reports, custom dashboards, and raw exports
- **Custom Dashboard Governance** — review and manage account-wide custom dashboards, including shared and private dashboards
- **Scheduled Delivery** — oversee scheduled report distribution across the account
- **Data Warehouse Export** — configure and monitor Enterprise data warehouse export connections
- **Security** — SSO, IP allowlisting, and session policies specific to reporting access
- **Audit Logs** — a searchable record of reporting-related administrative activity

### 1.3 Account Health Summary

The Analytics section of the Admin Dashboard displays a summary panel showing the number of active custom dashboards, scheduled deliveries currently configured, and, for Enterprise accounts, data warehouse export connection status.

### 1.4 Who Should Have Admin Dashboard Access

Corvex recommends limiting Administrator role assignment to a small number of trusted individuals — typically IT, security, or designated support operations leads — consistent with the principle of least privilege described further in Section 4. Because CloudDesk Analytics can expose account-wide performance data, including individual agent performance, administrator access to reporting configuration should be treated as sensitive.

---

## 2. User Management

### 2.1 Viewing Users and Reporting Access

Navigate to **Admin Dashboard > Users** to view all users on your account. CloudDesk Analytics does not maintain a separate user list; instead, it uses the same account-wide user list shared with CloudDesk Chat and CloudDesk Tickets, with reporting access layered on top via role and permission configuration.

### 2.2 Inviting a Reporting-Only User

For stakeholders who need dashboard access but no ticket or chat handling responsibility (for example, a Product Manager or an executive):

1. Click **Invite User** from **Admin Dashboard > Users**.
2. Enter the user's name and email address.
3. Assign the **Read-only / Reporting user** role (Section 3), available on Professional and Enterprise plans.
4. Click **Send Invitation**.

### 2.3 Editing Reporting Access

Click any existing user from the list to adjust their reporting access, either by changing their overall role or, on Professional and Enterprise plans, by editing their specific reporting permissions independent of their operational (chat/ticket) role.

### 2.4 Deactivating a User

Deactivating a user, as described in the CloudDesk Chat and CloudDesk Tickets Administrator Guides, immediately removes their reporting access as well, including any personal saved views or custom dashboards marked private to them.

### 2.5 Handling a Departing Dashboard Owner

If a user who owns shared custom dashboards or scheduled deliveries is deactivated, administrators should reassign ownership of those dashboards under **Admin Dashboard > Custom Dashboard Governance** before or shortly after deactivation, to prevent shared reporting from being orphaned.

---

## 3. Roles

CloudDesk Analytics uses the same role-based structure shared across the broader Corvex Cloud platform.

### 3.1 Standard Roles and Reporting Access

- **Agent** — access to their own individual performance summary only; no team- or account-level reporting
- **Team Lead / Supervisor** — full access to team-level dashboards, real-time queue views, and standard reporting for their team
- **Administrator** — full reporting access account-wide, plus configuration of report access permissions, custom dashboards, and data export settings
- **Read-only / Reporting user** — (Professional and Enterprise) dashboard and report viewing access without any ticket, chat, or configuration access

### 3.2 Custom Roles (Professional and Enterprise)

Administrators can create custom roles under **Admin Dashboard > Roles & Permissions > Custom Roles** that include specific reporting permissions independent of a user's chat or ticket handling role — for example, a Team Lead who should see only their own team's dashboards, not account-wide data.

### 3.3 Assigning Reporting-Specific Roles

Reporting access can be scoped more narrowly than a user's primary role using the permission categories described in Section 4, without requiring a fully separate custom role for every variation.

### 3.4 Role Changes and Effective Timing

Role and reporting permission changes take effect immediately upon saving. If a user is actively viewing a dashboard when their access changes, updated permissions apply on their next page refresh.

---

## 4. Permissions

### 4.1 Permission Categories

Reporting permissions in CloudDesk Analytics fall into several categories, each independently configurable for custom roles on Professional and Enterprise plans:

- **View permissions** — real-time dashboard, standard reports, custom dashboards
- **Scope permissions** — own performance only, team-level, or account-wide visibility
- **Export permissions** — CSV export, scheduled delivery configuration, data warehouse export access
- **Dashboard configuration permissions** — create, edit, or delete custom dashboards; share dashboards account-wide
- **Administrative permissions** — manage report access for other users, configure data warehouse export connections

### 4.2 Principle of Least Privilege

Corvex recommends assigning the minimum reporting scope necessary for each user's function. In particular, account-wide visibility into individual agent performance should be limited to roles that genuinely require it (team leads for their own team, administrators, and CX leadership), consistent with treating performance data thoughtfully.

### 4.3 Reviewing Current Permissions

Navigate to **Admin Dashboard > Roles & Permissions** to view a matrix of all roles (standard and custom) against all reporting permission categories, useful for periodic access review.

### 4.4 Permission Inheritance

Team Lead and Administrator roles inherit all Agent-level reporting access by default (their own performance data), with team-level and account-wide access layered on top; this inheritance is not configurable for standard roles but can be adjusted when building a custom role from scratch.

---

## 5. Security

### 5.1 Single Sign-On (SSO)

CloudDesk Analytics uses the same account-wide SSO configuration as CloudDesk Chat and CloudDesk Tickets; no separate SSO setup is required. Refer to **Admin Dashboard > Security > Single Sign-On** for configuration, available on Professional and Enterprise plans.

### 5.2 IP Allowlisting

IP allowlisting configured under **Admin Dashboard > Security > IP Allowlisting** applies account-wide, including access to CloudDesk Analytics dashboards, on Professional and Enterprise plans.

### 5.3 Dashboard Sharing Controls

Administrators can restrict whether custom dashboards may be shared outside the account (for example, via a public link) under **Admin Dashboard > Analytics > Security > Sharing Controls**. By default, dashboard sharing is limited to authenticated users within the account.

### 5.4 Scheduled Delivery Recipient Controls

To prevent sensitive performance data from being routed to unintended recipients, administrators can restrict scheduled report delivery to internal company email domains under **Admin Dashboard > Analytics > Security > Delivery Restrictions**, available on Professional and Enterprise plans.

### 5.5 Data Encryption

CloudDesk Analytics encrypts data in transit (TLS 1.2+) and at rest (AES-256) by default, consistent with the Corvex Cloud platform-wide standard. These settings are managed by Corvex and are not independently configurable.

### 5.6 Data Residency (Enterprise)

Enterprise customers with regional compliance requirements can request specific data residency configurations through their Customer Success Manager, applying account-wide including reporting data.

### 5.7 Data Warehouse Export Security (Enterprise)

Data warehouse export connections require authenticated, encrypted delivery to the customer's destination environment. Administrators should ensure destination credentials are stored securely on their own end and rotated periodically, consistent with their organization's broader security practices.

---

## 6. Audit Logs

### 6.1 What Is Logged

CloudDesk Analytics contributes the following actions to the account-wide audit log:

- Changes to reporting access permissions for any user or role
- Custom dashboard creation, sharing, and deletion
- Scheduled report delivery configuration changes
- Data warehouse export connection setup, modification, or removal
- Data exports (CSV) initiated by any user

### 6.2 Viewing Audit Logs

Navigate to **Admin Dashboard > Audit Logs** and filter by category to isolate Analytics-related entries. Each entry records the action taken, the user who performed it, and a timestamp.

### 6.3 Retention

Audit log retention is tied to your plan tier, consistent with the Corvex Cloud Pricing Guide: 90 days on Professional, with extended custom retention available on Enterprise.

### 6.4 Exporting Audit Logs

Administrators can export audit log data as a CSV file for external record-keeping or compliance review under **Audit Logs > Export**.

### 6.5 Using Audit Logs for Data Governance

Because CloudDesk Analytics can expose sensitive performance and customer trend data, Corvex recommends periodic review of who has exported data, configured scheduled deliveries, or connected data warehouse exports, particularly as part of a broader internal data governance process.

---

## 7. Backup

### 7.1 How Backup Works in CloudDesk Analytics

CloudDesk Analytics does not maintain a separate data store to back up independently; it reads in real time from the same case data layer used by CloudDesk Chat and CloudDesk Tickets, which is covered by Corvex's infrastructure-level backup practices as described in those products' Administrator Guides. What is specific to CloudDesk Analytics, and therefore relevant to back up independently, is your configuration: custom dashboards, saved views, and scheduled delivery settings.

### 7.2 Administrator-Initiated Configuration Export

1. Navigate to **Admin Dashboard > Analytics > Export Configuration**.
2. Select the scope: custom dashboards, saved views, or scheduled delivery settings.
3. Click **Generate Export**. The export is delivered as a downloadable JSON file describing the selected configuration.

### 7.3 Backing Up Report Output

For organizations that want a point-in-time record of report output itself (as opposed to configuration), standard reports and custom dashboards can be exported as CSV files at any time from within the reporting interface, as described in the CloudDesk Analytics User Manual.

### 7.4 Recommended Backup Cadence

Corvex recommends exporting custom dashboard and scheduled delivery configuration after any significant reporting structure change, in addition to any regular cadence your organization maintains for other account configuration backups.

---

## 8. Restore

### 8.1 Underlying Data Restoration

Because CloudDesk Analytics reflects the same underlying case data used by CloudDesk Chat and CloudDesk Tickets, any restoration of ticket or chat data (as described in those products' Administrator Guides) is automatically reflected in Analytics reporting without any separate Analytics-specific restoration step.

### 8.2 Restoring a Deleted Custom Dashboard

1. Navigate to **Admin Dashboard > Data > Recently Deleted**.
2. Locate the deleted custom dashboard using search or filters.
3. Click **Restore**. The dashboard is returned with its prior widget configuration and sharing settings intact, provided the deletion occurred within the account's recovery window (30 days on Professional; extended windows available on Enterprise).

### 8.3 Restoring from a Configuration Export

If your organization maintains its own configuration exports as described in Section 7.2, restoring from an export is not a self-service Admin Dashboard action. Contact Corvex Customer Success to coordinate reimporting exported dashboard or scheduled delivery configuration.

### 8.4 Limitations

Standard reports are built into the platform and cannot be deleted or need restoration; only custom dashboards, saved views, and scheduled delivery configurations are subject to the deletion and restoration process described above.

---

## 9. Integrations

### 9.1 Managing Integrations

Navigate to **Admin Dashboard > Integrations** to view integrations relevant to CloudDesk Analytics. Because Analytics reports on data generated elsewhere in the platform, most relevant integrations (CRM, e-commerce) are configured once at the account level and automatically enrich Analytics reporting without separate Analytics-specific setup.

### 9.2 Business Intelligence Tool Connections (Enterprise)

1. Navigate to **Admin Dashboard > Analytics > Data Warehouse Export**.
2. Click **Add Connection**.
3. Select your destination business intelligence or data warehouse platform and follow the guided authentication flow.
4. Select which datasets to include and configure the export schedule.
5. Confirm the connection using the provided test export before relying on it for production use.

### 9.3 Webhook-Based Reporting Events

Administrators can configure webhooks for specific analytics events (for example, a threshold alert firing) under **Admin Dashboard > Integrations > Developer Portal**, shared with the broader CloudDesk API Platform webhook configuration, available on Professional and Enterprise plans.

### 9.4 Removing an Integration

Select any connected data warehouse export or webhook and click **Disconnect**. Disconnecting halts data delivery going forward but does not delete data already delivered to the destination system.

### 9.5 Integration Health Monitoring

The Data Warehouse Export section displays a status indicator (Healthy, Warning, Error) for each connection, allowing administrators to quickly identify a failed or delayed export without needing to investigate from the destination system first.

---

## 10. Monitoring

### 10.1 Real-Time Account Monitoring

The Analytics section of the Admin Dashboard's account health summary (Section 1.3) provides real-time visibility into active custom dashboards, scheduled deliveries, and export connection status.

### 10.2 Scheduled Delivery Monitoring

Navigate to **Admin Dashboard > Analytics > Scheduled Delivery** to view all currently configured scheduled reports account-wide, including delivery success and failure history, useful for identifying a broken delivery before a stakeholder notices a missing report.

### 10.3 Data Warehouse Export Monitoring

For Enterprise accounts, **Admin Dashboard > Analytics > Data Warehouse Export** provides export run history, including timestamps, record counts, and any errors encountered during the most recent export.

### 10.4 Usage Monitoring

Navigate to **Admin Dashboard > Monitoring > Usage** to review overall account usage, including reporting-related API usage if the Developer Portal is used to build custom reporting integrations.

### 10.5 Security Monitoring

The Admin Dashboard surfaces security-relevant monitoring signals, such as unusual export activity or dashboard sharing changes, under **Monitoring > Security Signals**, available on Professional and Enterprise plans.

---

## 11. Maintenance

### 11.1 Platform Maintenance

As a cloud-hosted service, routine platform maintenance and updates are managed entirely by Corvex and typically require no administrator action. Corvex schedules maintenance windows to minimize disruption and communicates any maintenance expected to have visible impact through the Corvex Cloud status page.

### 11.2 Dashboard and Report Maintenance

Administrators are responsible for the ongoing maintenance of their account's reporting configuration, including:

- Periodically reviewing custom dashboards for continued relevance, particularly after team or organizational changes (Section 2.5)
- Reviewing scheduled delivery recipient lists to ensure they remain accurate as staff change roles or leave the organization
- Auditing data warehouse export connections for continued relevance and correct dataset scope (Enterprise)

### 11.3 Reporting Access Review

Because reporting access can expose sensitive performance data, Corvex recommends a periodic (at minimum semi-annual) review of who holds account-wide or team-wide reporting access, removing access that is no longer needed for a user's current role.

### 11.4 Threshold Alert Maintenance

Threshold alerts configured by team leads or administrators should be periodically reviewed for continued relevance; thresholds set for a prior staffing level or business condition can become noisy or irrelevant as circumstances change.

### 11.5 Seat and Plan Maintenance

Review current seat usage and reporting feature utilization against your plan regularly, particularly ahead of renewal. Refer to the Corvex Cloud Pricing Guide for upgrade, downgrade, and renewal terms.

---

## 12. Common Administrative Tasks

The following is a quick-reference summary of frequently performed administrative tasks and where to find them.

| Task | Location |
|---|---|
| Invite a reporting-only user | Admin Dashboard > Users > Invite User |
| Grant team-wide reporting access | Admin Dashboard > Roles & Permissions |
| Create a custom reporting role | Admin Dashboard > Roles & Permissions > Custom Roles |
| Reassign a departing user's shared dashboards | Admin Dashboard > Analytics > Custom Dashboard Governance |
| Enable SSO | Admin Dashboard > Security > Single Sign-On |
| Restrict scheduled delivery to internal domains | Admin Dashboard > Analytics > Security > Delivery Restrictions |
| Review recent reporting-related activity | Admin Dashboard > Audit Logs |
| Export dashboard/report configuration | Admin Dashboard > Analytics > Export Configuration |
| Restore a deleted custom dashboard | Admin Dashboard > Data > Recently Deleted |
| Connect a data warehouse export (Enterprise) | Admin Dashboard > Analytics > Data Warehouse Export > Add Connection |
| Review scheduled delivery status account-wide | Admin Dashboard > Analytics > Scheduled Delivery |
| Check data warehouse export run history | Admin Dashboard > Analytics > Data Warehouse Export |
| Review reporting permission matrix | Admin Dashboard > Roles & Permissions |
| Restrict dashboard external sharing | Admin Dashboard > Analytics > Security > Sharing Controls |
| View or revoke active user sessions | Admin Dashboard > Security > Active Sessions |

---

*This Administrator Guide covers standard administrative functionality for CloudDesk Analytics. For information on plan-specific feature availability, refer to the CloudDesk Analytics Product Overview and the Corvex Cloud Pricing Guide. For end-user instructions, refer to the CloudDesk Analytics User Manual.*
