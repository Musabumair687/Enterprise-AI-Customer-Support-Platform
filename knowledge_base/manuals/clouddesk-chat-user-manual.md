# CloudDesk Chat
## Official User Manual

*Corvex Cloud — CloudDesk Chat*
*This manual covers day-to-day use of CloudDesk Chat for agents, team leads, and administrators. For pricing and plan details, refer to the Corvex Cloud Pricing Guide. For a general product description, refer to the CloudDesk Chat Product Overview.*

---

## Table of Contents

1. Introduction
2. Installation
3. System Requirements
4. First Login
5. Dashboard Overview
6. Navigation
7. User Settings
8. Creating Your First Chat Widget
9. Daily Workflow
10. Best Practices
11. Tips
12. Keyboard Shortcuts
13. Frequently Used Features
14. Logging Out

---

## 1. Introduction

Welcome to CloudDesk Chat, the real-time messaging module of the Corvex Cloud platform. This manual is designed to help new and existing users — agents, team leads, and administrators — become comfortable and productive with CloudDesk Chat as quickly as possible.

CloudDesk Chat allows your organization to have live, real-time conversations with customers through a chat widget embedded on your website or mobile app. Every conversation you handle in CloudDesk Chat shares the same underlying customer and case history as the rest of Corvex Cloud, so context follows the customer even if their issue later becomes a ticket or continues over email.

This manual assumes you already have an active Corvex Cloud account. If your organization has not yet set up a Corvex Cloud account, contact your Corvex account representative or visit the Corvex Cloud website to begin a trial.

Throughout this manual, instructions apply to the standard web-based agent workspace unless otherwise noted. Mobile-specific instructions are covered separately in the CloudDesk Mobile documentation.

---

## 2. Installation

CloudDesk Chat is a cloud-hosted application. There is no software to download or install for agents, team leads, or administrators to use the agent workspace — you access it entirely through your web browser.

However, two components do require a brief setup step before your organization can begin receiving live chats:

### 2.1 Installing the Chat Widget on Your Website

An administrator must add a small snippet of code to your website so that the CloudDesk Chat widget appears for your visitors.

1. Log in to CloudDesk Chat as an administrator.
2. Navigate to **Settings > Chat Widget > Installation**.
3. Copy the provided widget installation snippet.
4. Paste the snippet into your website's HTML, immediately before the closing `</body>` tag, on every page where you want the chat widget to appear.
5. Save and publish your website changes.
6. Return to CloudDesk Chat and click **Verify Installation** to confirm the widget is live.

Most website platforms allow this snippet to be added once, in a shared template or footer, so it appears across your entire site without needing to be repeated on every page individually.

### 2.2 Installing the Mobile SDK (Optional)

If your organization wants to embed live chat inside your own iOS or Android app, your development team can install the CloudDesk Chat mobile SDK. This is a separate, developer-led process documented in the Corvex Cloud developer documentation and is not required to use CloudDesk Chat on your website.

### 2.3 Agent Workspace Access

No installation is required for agents, team leads, or administrators to use the agent workspace itself. Once your account has been created by an administrator, you can log in from any supported web browser, as described in Section 4.

---

## 3. System Requirements

### 3.1 For Agents, Team Leads, and Administrators (Agent Workspace)

- A supported desktop web browser: current or prior major version of Google Chrome, Mozilla Firefox, Apple Safari, or Microsoft Edge
- A stable internet connection
- A minimum screen resolution of 1280×800 is recommended for the best layout experience, though the workspace is responsive down to smaller screens
- No local software installation, plugins, or browser extensions are required

### 3.2 For Website Visitors (Chat Widget)

- Any modern desktop or mobile browser supporting standard JavaScript execution
- A stable internet connection to establish and maintain the real-time chat connection

### 3.3 For Mobile SDK Integration (Optional, Developer-Led)

- iOS: current or prior major supported iOS release
- Android: current or prior major supported Android release
- Development environment capable of integrating a native SDK, as detailed in the Corvex Cloud developer documentation

---

## 4. First Login

### 4.1 Receiving Your Invitation

New agents, team leads, and administrators are invited to CloudDesk Chat by an existing administrator on your account. You will receive an email invitation containing a secure link to set up your account.

### 4.2 Setting Up Your Account

1. Open the invitation email and click **Accept Invitation**.
2. You will be directed to the Corvex Cloud account setup page.
3. Create a password meeting your organization's password policy, or, if your organization uses Single Sign-On (SAML 2.0), you will instead be directed to authenticate through your organization's identity provider.
4. Confirm your name and time zone.
5. Click **Complete Setup**.

### 4.3 Logging In

1. Navigate to your organization's CloudDesk Chat login page (typically `[yourcompany].corvexcloud.com`, or your organization's custom domain, if configured).
2. Enter your email address and password, or select **Sign in with SSO** if your organization uses Single Sign-On.
3. Click **Log In**.

Upon your first successful login, you will be presented with a brief guided walkthrough of the agent workspace. You can skip this walkthrough at any time and revisit it later from **Help > Getting Started**.

---

## 5. Dashboard Overview

Once logged in, you land on the CloudDesk Chat dashboard, sometimes referred to as the agent workspace home. The dashboard is organized into four main areas:

### 5.1 Left Navigation Panel

A persistent vertical panel on the left side of the screen, providing access to your Inbox, active Conversations, Reports (if your role includes reporting access), and Settings.

### 5.2 Conversation List

The center panel displays your list of active and queued chat conversations. Conversations are organized by status: **Waiting**, **Active**, and **Resolved**. Team leads and administrators may also see a **Team Queue** view showing conversations across the whole team.

### 5.3 Active Conversation Panel

When you select a conversation from the list, it opens in the main panel to the right, showing the full message thread, a composer for your reply, and quick-access tools such as canned responses and internal notes.

### 5.4 Customer Context Panel

A collapsible panel on the far right displays customer details and history: past conversations, associated tickets, and (where integrated) relevant CRM or order information. This gives you full context without leaving the conversation.

---

## 6. Navigation

### 6.1 Moving Between Sections

Use the left navigation panel to move between the main sections of CloudDesk Chat:

- **Inbox** — your personal queue of assigned and unassigned conversations
- **Team Queue** — (Team Lead and Administrator roles) a view of all active conversations across your team
- **Reports** — access to CloudDesk Analytics dashboards relevant to chat performance (availability depends on your plan and role)
- **Settings** — account, widget, and integration configuration (Administrator role)

### 6.2 Switching Between Conversations

Click any conversation in the Conversation List to open it in the Active Conversation Panel. Your place in each open conversation is preserved as you switch between them, so you can manage multiple simultaneous chats without losing your draft replies.

### 6.3 Searching

Use the search bar at the top of the Conversation List to search by customer name, email address, or conversation content. Search results update as you type.

### 6.4 Filtering

Use the filter icon above the Conversation List to filter by status, tag, assigned agent, or channel. Saved filters (Professional and Enterprise plans) can be created for filter combinations you use frequently.

---

## 7. User Settings

Access your personal settings by clicking your profile icon in the bottom-left corner of the screen and selecting **My Settings**.

### 7.1 Profile

Update your display name, profile photo, and time zone. Your display name is what customers and colleagues see associated with your responses.

### 7.2 Notifications

Configure how you're notified of new conversations, mentions, and assignments:

- **Desktop notifications** — browser-based alerts when the workspace is open in a background tab
- **Sound alerts** — audible notification for new incoming chats
- **Email digest** — (optional) a summary of missed conversations, sent on a configurable schedule

### 7.3 Availability Status

Set your status to **Available**, **Away**, or **Do Not Disturb**. Your status affects whether new conversations are routed to you. Team leads and administrators can view team member availability from the Team Queue.

### 7.4 Canned Response Preferences

Manage your personal canned responses (in addition to team-wide canned responses configured by an administrator) from **My Settings > Canned Responses**.

### 7.5 Password and Security

Change your password (if not using SSO) and, where available, enable biometric app lock for CloudDesk Mobile from this section.

---

## 8. Creating Your First Chat Widget

If you are an administrator setting up CloudDesk Chat for the first time, your first task will typically be configuring and publishing your organization's chat widget.

### 8.1 Step 1: Create the Widget

1. Navigate to **Settings > Chat Widget**.
2. Click **Create Widget**.
3. Give your widget a name (for internal reference only; customers will not see this name).

### 8.2 Step 2: Customize Appearance

1. Choose your widget's primary color, position on the page (bottom-left or bottom-right), and greeting message.
2. Upload your company logo, if desired, to display within the widget header.
3. Preview your changes in real time using the live preview panel.

### 8.3 Step 3: Configure the Pre-Chat Form (Optional)

1. Decide whether visitors must complete a short form before starting a chat.
2. Add fields such as name, email, and a brief issue description, or custom fields relevant to your business.

### 8.4 Step 4: Set Up Routing

1. Navigate to **Settings > Chat Widget > Routing**.
2. Choose whether incoming chats route to a specific team, based on availability, or based on configured skill tags.
3. Configure an offline message for times when no agents are available.

### 8.5 Step 5: Install and Verify

1. Follow the installation steps in Section 2.1 to add the widget to your website.
2. Send a test chat message from your website to confirm the widget is working and routing correctly.
3. Once verified, your widget is live and ready to receive real customer conversations.

---

## 9. Daily Workflow

A typical day using CloudDesk Chat as an agent generally follows this pattern:

### 9.1 Starting Your Shift

1. Log in and set your availability status to **Available**.
2. Review your Inbox for any conversations assigned to you from a previous shift or handoff.
3. Check any team announcements or notes left by your team lead.

### 9.2 Handling Incoming Conversations

1. When a new chat arrives, you'll receive a notification based on your settings from Section 7.2.
2. Open the conversation and review any pre-chat form information and customer context.
3. Respond to the customer, using canned responses where appropriate to save time on common questions.
4. Add internal notes if you need to flag something for a colleague or your team lead — these are never visible to the customer.

### 9.3 Resolving or Escalating

1. Once the customer's issue is resolved, mark the conversation as **Resolved**.
2. If the issue requires longer-term tracking (for example, it needs engineering follow-up), convert the conversation into a ticket so it continues in CloudDesk Tickets with full history intact.
3. If a conversation needs to go to another agent or team, use **Transfer Conversation** rather than asking the customer to start over.

### 9.4 Managing Multiple Conversations

Most agents handle more than one conversation at a time. Use the Conversation List to keep track of which chats are waiting on your reply versus waiting on the customer, and prioritize accordingly.

### 9.5 Ending Your Shift

1. Ensure all active conversations are either resolved, transferred, or clearly noted for handoff.
2. Set your availability status to **Away** or log out, depending on your organization's process.

---

## 10. Best Practices

- **Acknowledge quickly, even before you have a full answer.** A fast initial response, even a brief one, significantly improves customer experience while you look into the details.
- **Use internal notes generously.** Leaving context for the next agent — or your future self — prevents customers from having to repeat information.
- **Don't let conversations sit in limbo.** Regularly review conversations marked as waiting on you, particularly toward the end of your shift.
- **Convert to a ticket when appropriate.** If an issue will take longer than a single chat session to resolve, converting it to a ticket preserves accountability and visibility better than leaving it open indefinitely as a chat.
- **Keep canned responses personal.** Canned responses save time, but take a moment to adjust them so they read naturally rather than obviously templated.
- **Set your status honestly.** Availability status directly affects routing; leaving your status as Available when you're not actually able to respond promptly can create a poor customer experience.

---

## 11. Tips

- Use the customer context panel before responding to a returning customer — it often answers questions before the customer has to ask them again.
- Pin frequently used canned responses to the top of your list from **My Settings > Canned Responses** for faster access.
- If you're handling several conversations at once, use filters to temporarily narrow your Conversation List to just the ones awaiting your reply.
- Team leads: review the Team Queue periodically throughout the day, not only when an SLA alert fires, to catch workload imbalances early.
- Use tags consistently — they power both search and the reporting your team lead and CX leadership rely on in CloudDesk Analytics.

---

## 12. Keyboard Shortcuts

| Action | Shortcut |
|---|---|
| Open next conversation in queue | `J` |
| Open previous conversation in queue | `K` |
| Reply to active conversation | `R` |
| Insert canned response | `/` |
| Mark conversation as Resolved | `Ctrl/Cmd + Enter` |
| Transfer conversation | `T` |
| Add internal note | `N` |
| Search | `Ctrl/Cmd + K` |
| Toggle customer context panel | `C` |
| Set status to Away | `Ctrl/Cmd + Shift + A` |

Keyboard shortcuts can be viewed at any time from within the application by pressing `?`.

---

## 13. Frequently Used Features

- **Canned Responses** — reusable reply templates accessible via the `/` shortcut or the composer toolbar
- **Internal Notes** — private, customer-invisible notes attached to a conversation
- **Conversation Transfer** — move a conversation to another agent or team without losing context
- **Customer Context Panel** — a consolidated view of customer history, past conversations, and related tickets
- **Tags** — apply categorization tags to conversations for organization and reporting
- **Saved Filters** — (Professional and Enterprise) save frequently used Conversation List filter combinations
- **Availability Status** — controls whether new conversations route to you
- **Ticket Conversion** — turn a chat conversation into a trackable CloudDesk Tickets case

---

## 14. Logging Out

To log out of CloudDesk Chat:

1. Click your profile icon in the bottom-left corner of the screen.
2. Select **Log Out** from the menu.
3. You will be returned to the CloudDesk Chat login screen.

### 14.1 Before You Log Out

As a best practice, before logging out at the end of a shift:

- Ensure no active conversations are left without a clear next step (resolved, transferred, or noted for handoff)
- Update your availability status if your organization expects this as part of shift handoff
- Save any draft replies you intend to finish later, or leave an internal note summarizing where you left off

### 14.2 Automatic Logout

For security purposes, your session may automatically log out after a period of inactivity, as configured by your administrator. If Single Sign-On is enabled for your organization, your session behavior may also be governed by your identity provider's session policies.

---

*This User Manual covers standard usage of CloudDesk Chat. For information on plan-specific feature availability, refer to the CloudDesk Chat Product Overview and the Corvex Cloud Pricing Guide.*
