# CloudDesk Mobile
## Official User Manual

*Corvex Cloud — CloudDesk Mobile*
*This manual covers day-to-day use of CloudDesk Mobile for agents, team leads, and administrators. For pricing and plan details, refer to the Corvex Cloud Pricing Guide. For a general product description, refer to the CloudDesk Mobile Product Overview.*

---

## Table of Contents

1. Introduction
2. Installation
3. System Requirements
4. First Login
5. Dashboard Overview
6. Navigation
7. User Settings
8. Setting Up Your First Device
9. Daily Workflow
10. Best Practices
11. Tips
12. Keyboard Shortcuts
13. Frequently Used Features
14. Logging Out

---

## 1. Introduction

Welcome to CloudDesk Mobile, the native mobile application for support agents, team leads, and administrators using Corvex Cloud. This manual is designed to help you become comfortable and productive using CloudDesk Mobile as quickly as possible.

CloudDesk Mobile connects to the same unified case data layer used by CloudDesk Chat, CloudDesk Tickets, and CloudDesk Analytics, allowing you to respond to tickets and chats, monitor queue health, and stay on top of urgent issues from your phone or tablet. Anything you do in CloudDesk Mobile is immediately reflected in the desktop workspace, and vice versa.

CloudDesk Mobile is distinct from the CloudDesk Chat mobile SDK, which is a separate, customer-facing tool your organization may use to embed a chat widget inside its own mobile app. This manual covers the internal-facing CloudDesk Mobile application your team uses to do its work, not the customer-facing widget.

This manual assumes you already have an active Corvex Cloud account with CloudDesk Chat and/or CloudDesk Tickets access, since CloudDesk Mobile is an extension of that existing account rather than a separate product purchase.

---

## 2. Installation

Unlike the desktop agent workspace, CloudDesk Mobile requires installing a native application on your device.

### 2.1 Downloading the App

1. On your iOS device, open the App Store and search for "CloudDesk Mobile" (or "Corvex Cloud"), or on your Android device, open the Google Play Store and search the same term.
2. Confirm the app is published by Corvex Technologies, Inc. before installing.
3. Tap **Install** (or **Get**) and wait for the download to complete.

### 2.2 Organization-Managed Installation (Optional)

Some organizations distribute CloudDesk Mobile through a mobile device management (MDM) system rather than the public app stores. If your organization uses this approach, your IT team will provide separate installation instructions; the login and usage steps described in this manual remain the same regardless of installation method.

### 2.3 Granting Permissions

After installation, open the app and grant the permissions it requests:

- **Push notifications** — required to receive alerts for new assignments, mentions, and SLA warnings
- **Biometric authentication** (optional) — required only if you choose to enable biometric app lock in Section 7.5

CloudDesk Mobile does not require access to your contacts, photos, or location to function.

---

## 3. System Requirements

### 3.1 iOS

- A device running a currently supported major iOS release or the immediately prior major release
- Sufficient device storage for the application and locally cached case data

### 3.2 Android

- A device running a currently supported major Android release or the immediately prior major release
- Sufficient device storage for the application and locally cached case data

### 3.3 Tablets

- CloudDesk Mobile supports both iOS and Android tablets with an optimized layout; no separate tablet-specific app is required

### 3.4 Connectivity

- A stable Wi-Fi or cellular data connection is required for real-time functionality
- Offline draft composition is supported, as described in Section 9.4, but requires connectivity to send

---

## 4. First Login

### 4.1 Using an Existing Corvex Cloud Account

If you already have an active Corvex Cloud account for CloudDesk Chat or CloudDesk Tickets, no separate invitation is needed to use CloudDesk Mobile — you'll log in with the same credentials.

### 4.2 Logging In

1. Open the CloudDesk Mobile app.
2. Enter your organization's Corvex Cloud domain (typically `[yourcompany].corvexcloud.com`) if prompted, or select your organization from a saved list if you've logged in on this device before.
3. Enter your email address and password, or tap **Sign in with SSO** if your organization uses Single Sign-On.
4. Tap **Log In**.

### 4.3 Enabling Notifications and Biometric Lock

On first login, you will be prompted to enable push notifications and, optionally, biometric app lock. Both can be adjusted later from **My Settings**, as described in Section 7.

### 4.4 Guided Walkthrough

After your first successful login, a brief guided walkthrough highlights the main areas of the app. You can skip this walkthrough at any time and revisit it later from **Settings > Help > Getting Started**.

---

## 5. Dashboard Overview

Once logged in, you land on the CloudDesk Mobile home screen. The layout is organized around four main areas, accessible via the bottom navigation bar:

### 5.1 Inbox Tab

Your personal queue of assigned tickets and active chats, sorted by priority and recency by default.

### 5.2 Team Tab

(Team Lead and Administrator roles) A condensed view of team queue status, including unassigned items and agent availability. Available on Professional and Enterprise plans.

### 5.3 Alerts Tab

A consolidated feed of push notifications received within the app — new assignments, mentions, and, on Professional and Enterprise plans, SLA warnings — even if you dismissed the original device notification.

### 5.4 More Tab

Access to Reports (condensed CloudDesk Analytics snapshots), account settings, and app-level settings such as notification preferences and biometric lock.

---

## 6. Navigation

### 6.1 Moving Between Sections

Use the bottom navigation bar to move between Inbox, Team, Alerts, and More. Your place within each tab is generally preserved when you switch away and back.

### 6.2 Opening a Ticket or Chat

Tap any item in your Inbox or Team queue to open its full detail view, including conversation history and customer context.

### 6.3 Returning to the List

Use the back gesture (swipe from the left edge on iOS, or the system back button on Android) or tap the back arrow in the top-left corner to return to the previous list view.

### 6.4 Searching

Tap the search icon at the top of the Inbox or Team tab to search by customer name, email address, or ticket/conversation content.

### 6.5 Filtering

Tap the filter icon to narrow the current list by status, priority, or channel. Saved filters configured on desktop (Professional and Enterprise) are also available here.

---

## 7. User Settings

Access your personal settings by tapping **More > My Settings**.

### 7.1 Profile

View your display name, profile photo, and time zone. Profile photo and display name updates made on desktop are reflected automatically here.

### 7.2 Notification Preferences

Configure which alerts trigger a push notification on this device:

- New assignments
- Mentions
- SLA warnings (Professional and Enterprise)
- Escalation approval requests (Team Lead and Administrator roles, Professional and Enterprise)

### 7.3 Availability Status

Set your availability status directly from mobile, just as you would on desktop. Your status affects whether new chats and tickets are routed to you.

### 7.4 Data Caching

Adjust how much recent case data is cached locally on your device for offline viewing, within limits configured by your administrator.

### 7.5 Biometric App Lock

Enable fingerprint- or face-based app lock, requiring biometric authentication each time you open the app, in addition to your standard account login.

### 7.6 Password and Security

Change your password (if not using SSO) from this section, or manage session settings.

---

## 8. Setting Up Your First Device

If this is the first time you're using CloudDesk Mobile — whether as a new agent or an existing desktop user adding mobile access — this section walks through getting your device fully ready for daily use.

### 8.1 Step 1: Complete Installation and Login

Follow the steps in Sections 2 and 4 to install the app and log in with your existing Corvex Cloud credentials.

### 8.2 Step 2: Configure Notifications

1. Navigate to **More > My Settings > Notification Preferences**.
2. Enable the alert types most relevant to your role, referring to Section 7.2.
3. Confirm your device's system-level notification permissions are also enabled, since both app-level and device-level settings must allow notifications for alerts to appear.

### 8.3 Step 3: Enable Biometric Lock (Recommended)

1. Navigate to **More > My Settings > Biometric App Lock**.
2. Toggle biometric lock on and follow your device's standard biometric enrollment prompts, if not already configured at the device level.

### 8.4 Step 4: Review Your Inbox and Team View

1. Open the Inbox tab and confirm your assigned tickets and chats appear as expected.
2. If you are a team lead or administrator, open the Team tab and confirm you can see team-wide queue status.

### 8.5 Step 5: Set Your Availability

1. Set your availability status appropriately for your current shift, as described in Section 7.3.
2. You're now ready to begin working from CloudDesk Mobile.

---

## 9. Daily Workflow

A typical day using CloudDesk Mobile generally follows one of two patterns: as a supplement to desktop work, or as your primary interface during periods away from a desk.

### 9.1 Starting Your Session

1. Open the app and confirm you're logged in and your availability status reflects your current situation.
2. Review the Alerts tab for anything that arrived since you last checked.

### 9.2 Responding to Urgent Items

1. When a push notification arrives for a new assignment or mention, tap it to open the relevant ticket or chat directly.
2. Review customer context before replying, just as you would on desktop.
3. Send your reply, or use a canned response or macro if the situation matches a common scenario.

### 9.3 Monitoring as a Team Lead

1. Periodically check the Team tab for queue status, unassigned items, and SLA warnings.
2. Approve or reassign escalations directly from an alert, where your plan and role support this action.
3. Check the Reports section under More for a condensed performance snapshot when a quick status check is needed.

### 9.4 Working Offline

1. If you lose connectivity while composing a reply, CloudDesk Mobile will queue your draft locally.
2. Once connectivity is restored, queued drafts are sent automatically, and you'll receive confirmation within the app.

### 9.5 Ending Your Session

1. Update your availability status if you're stepping away for an extended period.
2. Ensure any urgent items have been addressed or clearly handed off before closing the app.

---

## 10. Best Practices

- **Keep notifications focused.** Enable only the alert types genuinely relevant to your role; over-broad notifications reduce the chance you'll notice the ones that matter.
- **Use mobile for triage, not deep work.** CloudDesk Mobile is well suited for responding to urgent items and monitoring status; complex, multi-step cases are often better finished at a desktop.
- **Keep your availability status accurate.** Since status affects routing, an inaccurate status on mobile can result in items being assigned to you when you're not able to respond promptly, or withheld when you are.
- **Enable biometric lock, especially on a personal device.** This adds a meaningful layer of protection for customer data if your device is lost or accessed by someone else.
- **Don't rely solely on push notifications.** Check the Alerts tab periodically, since notifications can be missed, dismissed accidentally, or delayed by device-level settings outside the app's control.

---

## 11. Tips

- Use the Team tab's queue view for a quick status check before joining a meeting, rather than opening the full desktop dashboard.
- If you frequently work from mobile during a specific shift, save a filtered view matching your typical priorities for faster access each session.
- Adjust your data caching setting higher if you often work in areas with unreliable connectivity, so more case history is available offline.
- Use the search function rather than scrolling when looking for a specific customer's history — it's typically faster on a smaller screen.
- If you're a team lead approving escalations frequently from mobile, review the Alerts tab rather than only individual push notifications, since it preserves a running history you can refer back to.

---

## 12. Keyboard Shortcuts

CloudDesk Mobile is primarily a touch-based application. The gestures below function as the mobile equivalent of desktop keyboard shortcuts. If you connect an external keyboard to a supported tablet, the keyboard shortcuts listed also apply.

| Action | Gesture | External Keyboard Shortcut |
|---|---|---|
| Return to previous screen | Swipe from left edge (iOS) / Back button (Android) | `Esc` |
| Open search | Tap search icon | `Cmd/Ctrl + K` |
| Refresh current list | Pull down to refresh | `Cmd/Ctrl + R` |
| Archive/resolve item | Swipe left on list item | `Cmd/Ctrl + Enter` |
| Reply to open item | Tap composer field | `R` |
| Switch tabs | Tap bottom navigation icon | `Cmd/Ctrl + 1–4` |

---

## 13. Frequently Used Features

- **Inbox** — your personal queue of assigned tickets and chats
- **Team View** — (Team Lead and Administrator, Professional and Enterprise) real-time team queue and SLA status
- **Push Notifications** — real-time alerts for assignments, mentions, and SLA warnings
- **Offline Drafts** — reply composition that queues and sends automatically once connectivity returns
- **Biometric App Lock** — device-level authentication layer beyond standard account login
- **Report Snapshots** — condensed CloudDesk Analytics views accessible from the More tab
- **Availability Status** — controls whether new items are routed to you, synced with desktop
- **Escalation Approval** — (Team Lead and Administrator, Professional and Enterprise) approve or reassign escalations directly from an alert

---

## 14. Logging Out

To log out of CloudDesk Mobile:

1. Navigate to **More > My Settings**.
2. Tap **Log Out** at the bottom of the settings screen.
3. Confirm when prompted. You will be returned to the login screen.

### 14.1 Before You Log Out

As a best practice, before logging out:

- Ensure any offline drafts have been sent successfully, since logging out may prevent queued drafts from completing
- Update your availability status if your organization expects this as part of ending a mobile session
- Consider whether logging out is necessary at all — for a personal device with biometric lock enabled, staying logged in between sessions is generally acceptable and avoids repeated re-authentication

### 14.2 Remote Logout by an Administrator

If a device is lost or stolen, an administrator can remotely revoke that device's session from the desktop admin console under **Settings > Security > Active Sessions**, immediately logging the app out on that device without requiring physical access to it.

### 14.3 Automatic Logout

For security purposes, your session may automatically log out after a period of inactivity, as configured by your administrator. If Single Sign-On is enabled for your organization, your session behavior may also be governed by your identity provider's session policies.

---

*This User Manual covers standard usage of CloudDesk Mobile. For information on plan-specific feature availability, refer to the CloudDesk Mobile Product Overview and the Corvex Cloud Pricing Guide.*
