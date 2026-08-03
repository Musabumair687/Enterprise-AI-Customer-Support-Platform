# CloudDesk Tickets
## Official User Manual

*Corvex Cloud — CloudDesk Tickets*
*This manual covers day-to-day use of CloudDesk Tickets for agents, team leads, and administrators. For pricing and plan details, refer to the Corvex Cloud Pricing Guide. For a general product description, refer to the CloudDesk Tickets Product Overview.*

---

## Table of Contents

1. Introduction
2. Installation
3. System Requirements
4. First Login
5. Dashboard Overview
6. Navigation
7. User Settings
8. Creating Your First Ticket Workflow
9. Daily Workflow
10. Best Practices
11. Tips
12. Keyboard Shortcuts
13. Frequently Used Features
14. Logging Out

---

## 1. Introduction

Welcome to CloudDesk Tickets, the case and ticket management module of the Corvex Cloud platform. This manual is designed to help new and existing users — agents, team leads, and administrators — become comfortable and productive with CloudDesk Tickets as quickly as possible.

CloudDesk Tickets is the system of record for every customer support issue your organization handles, regardless of where it originated: email, a chat that needed follow-up, a social message, or a web form submission. Every ticket carries a clear status, a defined owner, and a full history, so nothing is lost and every issue can be tracked from first contact through resolution.

This manual assumes you already have an active Corvex Cloud account. If your organization has not yet set up a Corvex Cloud account, contact your Corvex account representative or visit the Corvex Cloud website to begin a trial.

Throughout this manual, instructions apply to the standard web-based agent workspace unless otherwise noted. Mobile-specific instructions are covered separately in the CloudDesk Mobile documentation.

---

## 2. Installation

CloudDesk Tickets is a cloud-hosted application. There is no software to download or install for agents, team leads, or administrators — you access it entirely through your web browser. A small number of setup steps are required before your organization begins receiving tickets from all intended channels.

### 2.1 Connecting Your Support Email

1. Log in to CloudDesk Tickets as an administrator.
2. Navigate to **Settings > Channels > Email**.
3. Choose to either connect an existing support mailbox or set up a new Corvex-hosted support email address.
4. Follow the on-screen instructions to authorize the connection or update your domain's mail routing (DNS) records, if using an existing mailbox.
5. Send a test email to confirm messages are correctly converting into tickets.

### 2.2 Installing the Web Form Widget

1. Navigate to **Settings > Channels > Web Form**.
2. Configure the fields your form should capture (for example, name, email, issue type, order number).
3. Copy the provided embed snippet and paste it into your website's HTML wherever you want the contact form to appear.
4. Publish your website changes and submit a test form to confirm ticket creation.

### 2.3 Connecting CloudDesk Chat (If Applicable)

If your organization also uses CloudDesk Chat, no separate installation is required — conversations converted to tickets from CloudDesk Chat automatically appear in CloudDesk Tickets, since both modules share the same underlying case data layer.

### 2.4 Agent Workspace Access

No installation is required for agents, team leads, or administrators to use the agent workspace itself. Once your account has been created by an administrator, you can log in from any supported web browser, as described in Section 4.

---

## 3. System Requirements

### 3.1 For Agents, Team Leads, and Administrators (Agent Workspace)

- A supported desktop web browser: current or prior major version of Google Chrome, Mozilla Firefox, Apple Safari, or Microsoft Edge
- A stable internet connection
- A minimum screen resolution of 1280×800 is recommended for the best layout experience, though the workspace is responsive down to smaller screens
- No local software installation, plugins, or browser extensions are required

### 3.2 For Customers (Email and Web Form)

- Any standard email client for email-based ticket submission
- Any modern desktop or mobile browser supporting standard JavaScript execution for web form submission

### 3.3 For Integrations

- A supported CRM, e-commerce platform, or project management tool account, where applicable, as detailed in the CloudDesk Tickets Product Overview and Corvex Cloud developer documentation

---

## 4. First Login

### 4.1 Receiving Your Invitation

New agents, team leads, and administrators are invited to CloudDesk Tickets by an existing administrator on your account. You will receive an email invitation containing a secure link to set up your account.

### 4.2 Setting Up Your Account

1. Open the invitation email and click **Accept Invitation**.
2. You will be directed to the Corvex Cloud account setup page.
3. Create a password meeting your organization's password policy, or, if your organization uses Single Sign-On (SAML 2.0), you will instead be directed to authenticate through your organization's identity provider.
4. Confirm your name and time zone.
5. Click **Complete Setup**.

### 4.3 Logging In

1. Navigate to your organization's CloudDesk Tickets login page (typically `[yourcompany].corvexcloud.com`, or your organization's custom domain, if configured).
2. Enter your email address and password, or select **Sign in with SSO** if your organization uses Single Sign-On.
3. Click **Log In**.

Upon your first successful login, you will be presented with a brief guided walkthrough of the agent workspace. You can skip this walkthrough at any time and revisit it later from **Help > Getting Started**.

---

## 5. Dashboard Overview

Once logged in, you land on the CloudDesk Tickets dashboard, sometimes referred to as the agent workspace home. The dashboard is organized into four main areas:

### 5.1 Left Navigation Panel

A persistent vertical panel on the left side of the screen, providing access to your ticket queues, Reports (if your role includes reporting access), and Settings.

### 5.2 Ticket Queue

The center panel displays tickets organized into views such as **My Open Tickets**, **Unassigned**, **Pending**, and **Resolved**. Team leads and administrators can also view team-wide and account-wide queues.

### 5.3 Ticket Detail Panel

Selecting a ticket opens its full detail in the main panel: the conversation thread, customer context, applied tags, and a reply composer, along with quick access to macros and internal notes.

### 5.4 Customer Context Panel

A collapsible panel showing the customer's full history: prior tickets, chat conversations, and, where integrated, relevant CRM or order data — giving you complete context without leaving the ticket.

---

## 6. Navigation

### 6.1 Moving Between Sections

Use the left navigation panel to move between the main sections of CloudDesk Tickets:

- **My Tickets** — your personally assigned queue
- **Team Queue** — (Team Lead and Administrator roles) a view of all tickets across your team
- **Unassigned** — tickets awaiting assignment
- **Reports** — access to CloudDesk Analytics dashboards relevant to ticket performance (availability depends on your plan and role)
- **Settings** — account, channel, automation, and integration configuration (Administrator role)

### 6.2 Opening and Switching Between Tickets

Click any ticket in the queue to open its detail view. Use the **Next** and **Previous** controls, or the corresponding keyboard shortcuts (Section 12), to move through your queue efficiently without returning to the list each time.

### 6.3 Searching

Use the search bar at the top of the ticket queue to search by customer name, email address, ticket number, or ticket content. Search results update as you type.

### 6.4 Filtering

Use the filter icon above the ticket queue to filter by status, priority, tag, assigned agent, or channel. Saved filters (Professional and Enterprise plans) can be created for filter combinations you use frequently.

---

## 7. User Settings

Access your personal settings by clicking your profile icon in the bottom-left corner of the screen and selecting **My Settings**.

### 7.1 Profile

Update your display name, profile photo, and time zone. Your display name is what customers and colleagues see associated with your responses.

### 7.2 Notifications

Configure how you're notified of new assignments, mentions, and SLA warnings:

- **Desktop notifications** — browser-based alerts when the workspace is open in a background tab
- **Email notifications** — configurable alerts for assignment, mentions, and SLA breaches
- **Notification digest** — (optional) a summary of unread activity, sent on a configurable schedule

### 7.3 Macros and Canned Responses

Manage your personal canned responses and, where permitted, personal macros from **My Settings > Macros & Responses**, in addition to team-wide options configured by an administrator.

### 7.4 Default Views

Set your default landing view (for example, **My Open Tickets** or **Unassigned**) so the workspace opens to the queue you use most.

### 7.5 Password and Security

Change your password (if not using SSO) and, where available, enable biometric app lock for CloudDesk Mobile from this section.

---

## 8. Creating Your First Ticket Workflow

If you are an administrator setting up CloudDesk Tickets for the first time, your first task will typically be configuring your organization's core ticket workflow — the statuses, fields, and rules that shape how tickets move from creation to resolution.

### 8.1 Step 1: Define Ticket Statuses and Priorities

1. Navigate to **Settings > Workflow > Statuses**.
2. Review the default statuses (New, Open, Pending, Resolved, Closed) and adjust or add statuses to match your team's process, if needed.
3. Configure priority levels (for example, Low, Normal, High, Urgent) and their default assignment behavior.

### 8.2 Step 2: Set Up Ticket Fields

1. Navigate to **Settings > Workflow > Fields**.
2. Add any custom fields your team needs to capture on every ticket (for example, order number, product area, or account tier). Custom fields are available on Professional and Enterprise plans.

### 8.3 Step 3: Configure Assignment Rules

1. Navigate to **Settings > Workflow > Assignment**.
2. Choose whether tickets are assigned manually, round-robin, or based on skill tags and workload balancing.
3. Set a fallback rule for tickets that go unassigned after a defined period.

### 8.4 Step 4: Set SLA Targets (Professional and Enterprise)

1. Navigate to **Settings > Workflow > SLAs**.
2. Define response and resolution time targets by priority level or category.
3. Configure breach alerts so team leads are notified before, not only after, an SLA is missed.

### 8.5 Step 5: Connect Your Channels

1. Confirm your email, web form, and (if applicable) CloudDesk Chat connections from Section 2 are active.
2. Send a test message through each connected channel to confirm tickets are created correctly and routed according to your new workflow.
3. Once verified, your ticket workflow is live and ready to handle real customer issues.

---

## 9. Daily Workflow

A typical day using CloudDesk Tickets as an agent generally follows this pattern:

### 9.1 Starting Your Shift

1. Log in and review your **My Open Tickets** queue.
2. Check the **Unassigned** queue if your team pulls tickets manually, or confirm your assignment rules have distributed new tickets appropriately.
3. Review any SLA warnings for tickets approaching a breach.

### 9.2 Working Through Your Queue

1. Open the highest-priority ticket in your queue.
2. Review the customer context panel for prior history before replying.
3. Respond using a macro or canned response where appropriate, or compose a custom reply.
4. Update the ticket's status, priority, and tags as needed to reflect its current state.
5. Add internal notes for anything a colleague, team lead, or Product/Engineering stakeholder should know — these are never visible to the customer.

### 9.3 Resolving, Merging, or Escalating

1. Once the customer's issue is resolved, update the ticket status to **Resolved**.
2. If you discover a duplicate ticket for the same issue, use **Merge Tickets** to consolidate the history into one record.
3. If a single ticket actually covers multiple unrelated issues, use **Split Ticket** to separate them for clearer tracking.
4. If a ticket needs to move to another agent or team, reassign it directly rather than asking the customer to start over.

### 9.4 Collaborating on Complex Tickets

Use @mentions within internal notes to bring a colleague, team lead, or another team into a ticket without leaving the record. For product-related issues, apply the appropriate tag so the ticket is correctly reflected in CloudDesk Analytics trend reporting.

### 9.5 Ending Your Shift

1. Ensure all tickets you've worked are in an accurate status, and any needing further attention have a clear internal note for handoff.
2. Confirm no tickets assigned to you are approaching an SLA breach without a plan in place.

---

## 10. Best Practices

- **Keep statuses current.** A ticket's status should always reflect reality; outdated statuses undermine both your team's workflow and leadership's reporting.
- **Use tags consistently.** Tags power search, automation, and the trend reporting that Product and Engineering rely on — inconsistent tagging weakens all three.
- **Write internal notes for your future self, not just your colleagues.** A ticket reopened weeks later is much easier to pick back up with a clear note explaining what was tried and why.
- **Merge before you duplicate work.** Check for existing tickets on the same issue before starting fresh, particularly for widely reported problems.
- **Respect SLA warnings.** Treat an SLA warning as an early signal to act, not a deadline to approach at the last minute.
- **Don't resolve prematurely.** Confirm the customer's issue is actually resolved, not just that a reply was sent, before closing a ticket.

---

## 11. Tips

- Use the customer context panel before replying to a returning customer — it often surfaces relevant history the customer hasn't mentioned yet.
- Build macros for your most common multi-step actions (for example, "apply refund tag, set status to Pending, send acknowledgment reply") to save time across similar tickets.
- Team leads: review the Unassigned queue and SLA warnings at set points throughout the day, not only when an alert fires.
- Use saved filters to create a personal view of exactly the tickets relevant to your role, rather than scrolling through the full team queue.
- When splitting a ticket, take a moment to make sure each resulting ticket has an accurate, specific summary — this saves confusion for whoever picks it up next.

---

## 12. Keyboard Shortcuts

| Action | Shortcut |
|---|---|
| Open next ticket in queue | `J` |
| Open previous ticket in queue | `K` |
| Reply to open ticket | `R` |
| Insert macro or canned response | `/` |
| Mark ticket as Resolved | `Ctrl/Cmd + Enter` |
| Assign or reassign ticket | `A` |
| Add internal note | `N` |
| Add tag | `G` |
| Search | `Ctrl/Cmd + K` |
| Toggle customer context panel | `C` |

Keyboard shortcuts can be viewed at any time from within the application by pressing `?`.

---

## 13. Frequently Used Features

- **Macros** — multi-step, reusable actions combining a reply, status change, and tagging in a single click
- **Canned Responses** — reusable reply templates for common questions
- **Internal Notes and @Mentions** — private, customer-invisible collaboration within a ticket
- **Merge and Split** — consolidate duplicate tickets or separate multi-issue tickets
- **Tags** — categorization for search, automation, and reporting
- **Customer Context Panel** — a consolidated view of customer history across tickets and chat conversations
- **SLA Indicators** — visual cues showing how close a ticket is to breaching its response or resolution target (Professional and Enterprise)
- **Saved Filters** — (Professional and Enterprise) save frequently used queue filter combinations

---

## 14. Logging Out

To log out of CloudDesk Tickets:

1. Click your profile icon in the bottom-left corner of the screen.
2. Select **Log Out** from the menu.
3. You will be returned to the CloudDesk Tickets login screen.

### 14.1 Before You Log Out

As a best practice, before logging out at the end of a shift:

- Ensure all tickets you've worked have an accurate, current status
- Leave internal notes on any ticket requiring follow-up by another agent
- Check for any tickets approaching an SLA breach that need attention before you leave

### 14.2 Automatic Logout

For security purposes, your session may automatically log out after a period of inactivity, as configured by your administrator. If Single Sign-On is enabled for your organization, your session behavior may also be governed by your identity provider's session policies.

---

*This User Manual covers standard usage of CloudDesk Tickets. For information on plan-specific feature availability, refer to the CloudDesk Tickets Product Overview and the Corvex Cloud Pricing Guide.*
