# CloudDesk API Platform
## Official User Manual

*Corvex Cloud — CloudDesk API Platform*
*This manual covers day-to-day use of CloudDesk API Platform for developers, administrators, and integration users. For pricing and plan details, refer to the Corvex Cloud Pricing Guide. For a general product description, refer to the CloudDesk API Platform Product Overview.*

---

## Table of Contents

1. Introduction
2. Installation
3. System Requirements
4. First Login
5. Dashboard Overview
6. Navigation
7. User Settings
8. Creating Your First Integration
9. Daily Workflow
10. Best Practices
11. Tips
12. Keyboard Shortcuts
13. Frequently Used Features
14. Logging Out

---

## 1. Introduction

Welcome to CloudDesk API Platform, the developer and extensibility layer of the Corvex Cloud platform. This manual is designed to help developers, administrators, and integration users become comfortable and productive working with the API Platform as quickly as possible.

CloudDesk API Platform exposes the same unified case, customer, and reporting data model used by CloudDesk Chat, CloudDesk Tickets, and CloudDesk Analytics, allowing you to build custom integrations, automate workflows, and connect Corvex Cloud to the rest of your technology environment. This manual covers the developer portal itself — where you manage API keys, review documentation, configure webhooks, and monitor usage — rather than the specifics of any individual endpoint, which are covered in the separate Corvex Cloud API reference documentation.

This manual assumes you already have an active Corvex Cloud account with API access enabled for your role. If your organization has not yet set up a Corvex Cloud account, contact your Corvex account representative or visit the Corvex Cloud website to begin a trial.

---

## 2. Installation

CloudDesk API Platform is a cloud-hosted service. There is no software to install to access the developer portal itself — it is used entirely through your web browser. However, integrating with the API from your own systems requires some setup on your end.

### 2.1 Accessing the Developer Portal

No installation is required to access the developer portal. Once your account has API access enabled, you can log in from any supported web browser, as described in Section 4.

### 2.2 Preparing Your Development Environment

To make use of the API from your own systems, your development environment should be capable of making authenticated HTTPS requests. CloudDesk API Platform does not require any Corvex-provided software development kit for basic usage, though official client libraries are available for common languages via the developer documentation portal for teams who prefer them.

### 2.3 Preparing a Webhook Endpoint (Professional and Enterprise)

If you plan to use webhooks, your systems will need an HTTPS endpoint capable of receiving POST requests before you configure webhook delivery in Section 8. This endpoint does not need to be publicly documented, but it must be reachable from the public internet and capable of responding to Corvex's delivery attempts.

---

## 3. System Requirements

### 3.1 For the Developer Portal

- A supported desktop web browser: current or prior major version of Google Chrome, Mozilla Firefox, Apple Safari, or Microsoft Edge
- A stable internet connection
- No local software installation, plugins, or browser extensions are required

### 3.2 For API Integration

- A development environment or system capable of making authenticated HTTPS requests
- Familiarity with REST API concepts (endpoints, authentication headers, JSON payloads) is recommended but not required to follow this manual

### 3.3 For Webhook Integration (Professional and Enterprise)

- A publicly reachable HTTPS endpoint capable of receiving and responding to POST requests
- The ability to verify webhook payload signatures, as described in the Corvex Cloud developer documentation, is strongly recommended for production use

### 3.4 For Sandbox Access (Enterprise Only)

- No additional local requirements; the sandbox environment is accessed the same way as the production developer portal, using a separate sandbox account context

---

## 4. First Login

### 4.1 Receiving API Access

API access is granted by an existing administrator on your Corvex Cloud account. If your own account already exists for CloudDesk Chat, Tickets, or Analytics, an administrator can enable API Platform access for your existing login rather than creating a new account. New integration-only users receive a standard email invitation.

### 4.2 Setting Up Your Account (New Users)

1. Open the invitation email and click **Accept Invitation**.
2. You will be directed to the Corvex Cloud account setup page.
3. Create a password meeting your organization's password policy, or, if your organization uses Single Sign-On (SAML 2.0), you will instead be directed to authenticate through your organization's identity provider.
4. Confirm your name and time zone.
5. Click **Complete Setup**.

### 4.3 Logging In

1. Navigate to your organization's Corvex Cloud login page (typically `[yourcompany].corvexcloud.com`, or your organization's custom domain, if configured).
2. Enter your email address and password, or select **Sign in with SSO** if your organization uses Single Sign-On.
3. Click **Log In**, then select **Developer Portal** from the main application switcher.

Upon your first successful login to the Developer Portal, you will be presented with a brief guided walkthrough. You can skip this walkthrough at any time and revisit it later from **Help > Getting Started**.

---

## 5. Dashboard Overview

Once logged in, you land on the Developer Portal home dashboard. The dashboard is organized into four main areas:

### 5.1 Left Navigation Panel

A persistent vertical panel on the left side of the screen, providing access to API Keys, Webhooks, Documentation, Usage & Rate Limits, and Settings.

### 5.2 Usage Summary

A summary panel at the top of the dashboard showing current API usage against your plan's rate limit, along with recent request volume trends.

### 5.3 Main Content Area

The center of the screen displays whichever section you've selected from the left navigation — for example, your list of API keys, configured webhooks, or embedded documentation.

### 5.4 Recent Activity Panel

A panel showing recent API requests and webhook delivery attempts, useful for a quick sanity check that your integration is functioning as expected, without needing to leave the portal.

---

## 6. Navigation

### 6.1 Moving Between Sections

Use the left navigation panel to move between the main sections of the Developer Portal:

- **API Keys** — create, view, and rotate API keys
- **Webhooks** — configure and monitor webhook endpoints (Professional and Enterprise)
- **Documentation** — browse the full API reference, including endpoint details and example requests
- **Usage & Rate Limits** — monitor current usage against your plan's limits
- **Sandbox** — (Enterprise) switch into the sandbox environment for safe testing
- **Settings** — IP allowlisting, audit log access, and integration-related account settings

### 6.2 Searching Documentation

Use the search bar within the Documentation section to quickly locate a specific endpoint, event type, or concept, rather than browsing the full reference sequentially.

### 6.3 Switching Between Production and Sandbox (Enterprise)

Use the environment switcher in the top navigation bar to move between your production account and sandbox environment. The two are clearly distinguished by a persistent visual indicator to reduce the risk of accidentally testing against live data.

---

## 7. User Settings

Access your personal settings by clicking your profile icon in the bottom-left corner of the screen and selecting **My Settings**.

### 7.1 Profile

Update your display name, profile photo, and time zone.

### 7.2 Notification Preferences

Configure alerts related to API and webhook activity:

- **Rate limit warnings** — notification when your account approaches its rate limit
- **Webhook delivery failures** — notification when a configured webhook endpoint repeatedly fails to accept delivery
- **API key expiration or rotation reminders** — notification ahead of any scheduled key rotation requirements set by your administrator

### 7.3 Default Landing Section

Set whether the Developer Portal opens to API Keys, Documentation, or Usage & Rate Limits when you log in.

### 7.4 Password and Security

Change your password (if not using SSO) from this section.

---

## 8. Creating Your First Integration

This section walks through the process of building your first basic integration: creating an API key, making a first request, and, if applicable, configuring a webhook.

### 8.1 Step 1: Generate an API Key

1. Navigate to **API Keys**.
2. Click **Create API Key**.
3. Give the key a descriptive name (for example, "Internal Order Sync – Production").
4. Select the appropriate scope: read-only or read/write, based on your plan and use case.
5. Click **Generate**. Your API key will be displayed once — copy and store it securely, as Corvex does not retain a recoverable copy of the key value.

### 8.2 Step 2: Make Your First API Request

1. Navigate to **Documentation** and locate a simple, read-only endpoint (for example, retrieving a single ticket by ID) to use as a first test.
2. Using your preferred HTTP client or the documentation portal's built-in request tester, include your API key in the authentication header as shown in the example request.
3. Send the request and confirm you receive a successful response containing the expected data.

### 8.3 Step 3: Configure a Webhook (Professional and Enterprise)

1. Navigate to **Webhooks**.
2. Click **Add Webhook Endpoint**.
3. Enter your endpoint URL and select which event types you want to receive (for example, ticket created, ticket resolved, chat conversation closed).
4. Save the configuration, then use the **Send Test Event** option to confirm your endpoint correctly receives and acknowledges a sample payload.

### 8.4 Step 4: Verify in the Sandbox (Enterprise, Recommended)

1. Switch to the **Sandbox** environment using the environment switcher.
2. Repeat Steps 1 through 3 within the sandbox to validate your full integration flow against non-production data before deploying against your live account.

### 8.5 Step 5: Move to Production

1. Once your integration is validated, switch back to the production environment (or, if you are not on Enterprise, proceed directly with your original production API key and webhook configuration).
2. Monitor the **Recent Activity Panel** and **Usage & Rate Limits** section over the following hours to confirm your integration is behaving as expected under real usage.

---

## 9. Daily Workflow

A typical day using CloudDesk API Platform as a developer or integration owner generally follows this pattern:

### 9.1 Morning Check-In

1. Log in and review the Usage Summary for any unusual spikes or approaching rate limit thresholds.
2. Check the Recent Activity Panel for any failed requests or webhook delivery failures from overnight processing.

### 9.2 Ongoing Development and Maintenance

1. Reference the Documentation section as needed while building or extending integrations.
2. Use the request tester within Documentation to validate new endpoint usage before implementing it in code.
3. Update webhook event subscriptions as your integration's requirements evolve.

### 9.3 Monitoring and Alerts

1. Respond promptly to any rate limit warning or webhook delivery failure notifications received during the day.
2. Review audit logs periodically to confirm API key usage matches expected patterns, particularly for accounts with multiple integrations or team members holding key management access.

### 9.4 Key and Access Management

1. Rotate API keys according to your organization's security policy, or when a key may have been exposed.
2. Remove or disable API keys and webhook endpoints that are no longer in active use.

---

## 10. Best Practices

- **Use separate API keys per integration.** A dedicated key for each integration makes it easier to monitor usage, rotate credentials, and revoke access without affecting unrelated systems.
- **Request only the access scope you need.** Use read-only keys wherever write access isn't required, limiting the impact of a potentially compromised credential.
- **Verify webhook payload signatures.** Always confirm that incoming webhook payloads are genuinely from Corvex Cloud before acting on them, particularly for any endpoint that triggers a downstream action.
- **Build for graceful rate limit handling.** Design your integration to respect rate limit responses and retry with appropriate backoff, rather than retrying immediately in a tight loop.
- **Test in sandbox before production, when available.** Enterprise customers should validate new or significantly changed integrations in the sandbox environment before pointing them at live data.
- **Document your integrations internally.** Maintain your own internal record of what each API key and webhook endpoint is used for — the Developer Portal shows what exists, but not necessarily why.

---

## 11. Tips

- Use the request tester in the Documentation section to quickly confirm expected response structure before writing integration code against a new endpoint.
- Set a rate limit warning threshold well below your actual limit, giving your team time to react before requests start being throttled.
- When debugging a webhook issue, the Recent Activity Panel's delivery attempt history is often faster to check than instrumenting your own endpoint's logs first.
- If your integration needs change significantly, consider creating a new API key with an updated scope rather than broadening an existing key's permissions, to keep access scoped tightly over time.
- For high-volume Enterprise integrations, reach out about dedicated webhook infrastructure before you hit sustained high throughput, rather than after delivery issues appear.

---

## 12. Keyboard Shortcuts

| Action | Shortcut |
|---|---|
| Open API Keys section | `Ctrl/Cmd + 1` |
| Open Webhooks section | `Ctrl/Cmd + 2` |
| Open Documentation section | `Ctrl/Cmd + 3` |
| Search documentation | `Ctrl/Cmd + K` |
| Open request tester | `Ctrl/Cmd + T` |
| Copy code sample | `Ctrl/Cmd + Shift + C` |
| Switch environment (production/sandbox) | `Ctrl/Cmd + E` |
| Refresh usage data | `Ctrl/Cmd + R` |

Keyboard shortcuts can be viewed at any time from within the application by pressing `?`.

---

## 13. Frequently Used Features

- **API Keys** — create, scope, and rotate credentials used to authenticate requests
- **Webhooks** — configure real-time event delivery to your own systems (Professional and Enterprise)
- **Documentation Portal** — browse endpoint references, event types, and example requests
- **Request Tester** — send test API requests directly from the browser without external tooling
- **Usage & Rate Limits** — monitor current usage against your plan's limits
- **Recent Activity Panel** — review recent API requests and webhook delivery attempts
- **Sandbox Environment** — (Enterprise) a safe, non-production space for testing integrations
- **Audit Logs** — review API key creation, rotation, and usage history

---

## 14. Logging Out

To log out of CloudDesk API Platform:

1. Click your profile icon in the bottom-left corner of the screen.
2. Select **Log Out** from the menu.
3. You will be returned to the Corvex Cloud login screen.

### 14.1 Before You Log Out

As a best practice, before logging out:

- Confirm any newly created API keys have been securely stored, since key values cannot be retrieved again after initial creation
- Confirm any webhook configuration changes have been tested with a sample event
- Review the Usage Summary one final time if you've made changes that could affect request volume

### 14.2 Automatic Logout

For security purposes, your session may automatically log out after a period of inactivity, as configured by your administrator. If Single Sign-On is enabled for your organization, your session behavior may also be governed by your identity provider's session policies. Note that automatic session logout affects your Developer Portal browser session only and does not disable or rotate any active API keys, which continue to function independently until explicitly revoked.

---

*This User Manual covers standard usage of CloudDesk API Platform. For information on plan-specific feature availability, refer to the CloudDesk API Platform Product Overview and the Corvex Cloud Pricing Guide.*
