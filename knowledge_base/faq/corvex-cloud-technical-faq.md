# Corvex Cloud
## Technical FAQ

*This document answers common technical questions about integrating with and configuring the Corvex Cloud platform, including CloudDesk Chat, CloudDesk Tickets, CloudDesk Analytics, CloudDesk API Platform, and CloudDesk Mobile. It is intended for developers, administrators, and technical implementation staff. Where applicable, example commands use `curl` against the CloudDesk API Platform REST API; replace placeholder values (shown in `ALL_CAPS`) with your own.*

---

## Category: API Authentication

### 1. Question: How do I authenticate API requests to CloudDesk API Platform?

**Answer:** Include your API key in the `Authorization` header of every request as a Bearer token. Keys are generated under Admin Dashboard > API Platform > API Keys.

**Commands:**
```
curl -X GET https://api.corvexcloud.com/v1/tickets/12345 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Beginner

---

### 2. Question: How do I generate a new API key?

**Answer:** Navigate to Admin Dashboard > API Platform > API Keys, click Create API Key, name it, select a scope (read-only or read/write), and click Generate. The key value is displayed once and cannot be retrieved again.

**Commands:** Not applicable (UI-based action)

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Beginner

---

### 3. Question: Why does my API key only allow read operations?

**Answer:** API keys are scoped at creation time as read-only or read/write. Read/write scope requires a Professional or Enterprise plan; Starter accounts are limited to read-only access account-wide.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform Product Overview

**Difficulty Level:** Beginner

---

### 4. Question: How do I rotate an API key without breaking my integration?

**Answer:** Generate a new key with the same scope, update your integration's configuration to use the new key, confirm the integration is functioning correctly against the new key, then revoke the old key.

**Commands:**
```
# 1. Generate new key via Admin Dashboard
# 2. Update your secrets manager or environment variable
export CORVEX_API_KEY="NEW_KEY_VALUE"
# 3. Verify
curl -X GET https://api.corvexcloud.com/v1/account \
  -H "Authorization: Bearer $CORVEX_API_KEY"
# 4. Revoke old key via Admin Dashboard once verified
```

**Related Documentation:** CloudDesk API Platform Administrator Guide

**Difficulty Level:** Intermediate

---

### 5. Question: Can I have multiple API keys active at the same time?

**Answer:** Yes. There is no limit on the number of active API keys for an account; Corvex recommends a dedicated key per integration for clear usage attribution and independent revocation.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform Administrator Guide

**Difficulty Level:** Beginner

---

### 6. Question: How do I configure SSO for API-based authentication?

**Answer:** SSO governs human login to the Developer Portal and agent workspace; it does not apply to machine-to-machine API authentication, which always uses API keys regardless of whether SSO is enabled for user login.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform Administrator Guide

**Difficulty Level:** Intermediate

---

### 7. Question: What HTTP status code indicates an authentication failure?

**Answer:** A 401 Unauthorized response indicates the API key is missing, invalid, expired, or revoked. A 403 Forbidden response indicates the key is valid but lacks permission for the specific requested action.

**Commands:**
```
curl -i -X GET https://api.corvexcloud.com/v1/tickets/12345 \
  -H "Authorization: Bearer INVALID_KEY"
# HTTP/1.1 401 Unauthorized
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Beginner

---

### 8. Question: How do I scope an API key to specific endpoints only?

**Answer:** Endpoint-level scope restriction is configured at key creation time under advanced key settings, letting you limit a key to specific resource types (for example, tickets but not users).

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk API Platform Administrator Guide

**Difficulty Level:** Intermediate

---

### 9. Question: Does CloudDesk API Platform support OAuth 2.0?

**Answer:** Standard customer-facing API access uses API key authentication rather than OAuth 2.0. Marketplace and partner integrations use a separate, Corvex-managed OAuth flow for their own authorization, distinct from customer API keys.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform Product Overview

**Difficulty Level:** Intermediate

---

### 10. Question: How do I test authentication without affecting production data?

**Answer:** Use the sandbox environment (Enterprise) with a separate, sandbox-specific API key. Sandbox and production keys are entirely independent and cannot be used interchangeably.

**Commands:**
```
curl -X GET https://api-sandbox.corvexcloud.com/v1/account \
  -H "Authorization: Bearer SANDBOX_API_KEY"
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Intermediate

---

## Category: API Requests and Endpoints

### 11. Question: How do I retrieve a single ticket by ID?

**Answer:** Send a GET request to the tickets endpoint with the ticket ID as a path parameter.

**Commands:**
```
curl -X GET https://api.corvexcloud.com/v1/tickets/12345 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Beginner

---

### 12. Question: How do I create a new ticket via the API?

**Answer:** Send a POST request to the tickets endpoint with a JSON payload including at minimum a subject and requester email.

**Commands:**
```
curl -X POST https://api.corvexcloud.com/v1/tickets \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"subject":"Order issue","requester_email":"customer@example.com"}'
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Beginner

---

### 13. Question: How do I update a custom field on a ticket via the API?

**Answer:** Send a PATCH request referencing the field's internal identifier (retrieved from the fields listing endpoint), not its display label.

**Commands:**
```
curl -X GET https://api.corvexcloud.com/v1/fields \
  -H "Authorization: Bearer YOUR_API_KEY"

curl -X PATCH https://api.corvexcloud.com/v1/tickets/12345 \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"custom_fields":{"order_number":"ORD-98765"}}'
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Intermediate

---

### 14. Question: How do I paginate through a large list of tickets?

**Answer:** Use cursor-based pagination rather than offset-based pagination for stability against concurrent data changes. Each response includes a `next_cursor` value to pass into the subsequent request.

**Commands:**
```
curl -X GET "https://api.corvexcloud.com/v1/tickets?limit=100" \
  -H "Authorization: Bearer YOUR_API_KEY"

curl -X GET "https://api.corvexcloud.com/v1/tickets?limit=100&cursor=NEXT_CURSOR_VALUE" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Intermediate

---

### 15. Question: How do I filter API results by date range?

**Answer:** Pass `created_after` and `created_before` query parameters using ISO 8601 formatted UTC timestamps.

**Commands:**
```
curl -X GET "https://api.corvexcloud.com/v1/tickets?created_after=2026-07-01T00:00:00Z&created_before=2026-07-31T23:59:59Z" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Beginner

---

### 16. Question: Why are timestamps in API responses not in my local time zone?

**Answer:** All API timestamps are returned in UTC by design. Convert to your desired local time zone within your own integration code.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Beginner

---

### 17. Question: How do I limit which fields are returned in an API response?

**Answer:** Use the `fields` query parameter with a comma-separated list of field names to reduce response payload size.

**Commands:**
```
curl -X GET "https://api.corvexcloud.com/v1/tickets/12345?fields=id,status,priority" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Intermediate

---

### 18. Question: How do I perform a bulk update on multiple tickets via the API?

**Answer:** Send a POST request to the bulk update endpoint with an array of ticket IDs and the desired changes. Review the response's per-record status array, since a successful overall response does not guarantee every individual record succeeded.

**Commands:**
```
curl -X POST https://api.corvexcloud.com/v1/tickets/bulk_update \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ticket_ids":[101,102,103],"changes":{"status":"resolved"}}'
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Advanced

---

### 19. Question: What API version should I use, and how do I specify it?

**Answer:** Specify the API version using the `Corvex-Version` header. Omitting it defaults to the current stable version, which may change over time as new versions are released.

**Commands:**
```
curl -X GET https://api.corvexcloud.com/v1/tickets/12345 \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Corvex-Version: 2026-06-01"
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Intermediate

---

### 20. Question: How do I retrieve a customer's full conversation history across channels via the API?

**Answer:** Use the customer endpoint with the `include=conversations` parameter to retrieve a customer's combined ticket and chat history in a single request.

**Commands:**
```
curl -X GET "https://api.corvexcloud.com/v1/customers/CUST_ID?include=conversations" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Intermediate

---

## Category: Webhooks

### 21. Question: How do I configure a webhook endpoint?

**Answer:** Navigate to Admin Dashboard > API Platform > Webhooks, click Add Webhook Endpoint, enter your endpoint URL, select event types, save, and send a test event to confirm connectivity.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Beginner

---

### 22. Question: How do I verify a webhook payload is genuinely from Corvex?

**Answer:** Compute an HMAC-SHA256 signature of the raw request body using your webhook's signing secret, and compare it against the `Corvex-Signature` header. Reject the request if they don't match.

**Commands:**
```
# Example (Python)
import hmac, hashlib

signature = hmac.new(
    SIGNING_SECRET.encode(),
    request_body,
    hashlib.sha256
).hexdigest()

assert hmac.compare_digest(signature, request.headers["Corvex-Signature"])
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Advanced

---

### 23. Question: What event types can I subscribe to?

**Answer:** Standard event types include ticket created, ticket updated, ticket resolved, chat conversation started, and chat conversation closed, among others. The full list is available in the developer documentation.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Beginner

---

### 24. Question: How do I handle duplicate webhook deliveries?

**Answer:** Design your receiving endpoint to be idempotent, using the event's unique `event_id` to detect and skip already-processed events, since at-least-once delivery means duplicates are expected under retry conditions.

**Commands:**
```
# Example logic
if event_id in processed_events:
    return 200  # already handled, acknowledge without reprocessing
```

**Related Documentation:** CloudDesk API Platform Troubleshooting Guide

**Difficulty Level:** Advanced

---

### 25. Question: My webhook endpoint isn't receiving events. How do I debug this?

**Answer:** Check delivery attempt history and response codes under Admin Dashboard > API Platform > Webhooks. Confirm your endpoint is publicly reachable, returns a 2xx status quickly, and that the relevant event type is included in your subscription.

**Commands:**
```
curl -X POST https://your-endpoint.example.com/webhooks/corvex \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
# Confirm your endpoint returns HTTP 200
```

**Related Documentation:** CloudDesk API Platform Troubleshooting Guide

**Difficulty Level:** Intermediate

---

### 26. Question: How quickly must my endpoint respond to a webhook delivery?

**Answer:** Your endpoint should respond with a success status within a few seconds. If processing takes longer, acknowledge receipt immediately with a 200 response and perform lengthy processing asynchronously.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Intermediate

---

### 27. Question: Can I subscribe to CloudDesk Analytics threshold alert events via webhook?

**Answer:** Yes, on Professional and Enterprise plans. Configure the specific threshold alert event type under your webhook's event subscription in the Developer Portal.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Analytics Administrator Guide

**Difficulty Level:** Intermediate

---

### 28. Question: How do I rotate my webhook signing secret?

**Answer:** Generate a new signing secret under Admin Dashboard > API Platform > Webhooks, update your receiving system's verification logic to use the new secret, and confirm successful verification with a test event before considering the rotation complete.

**Commands:** Not applicable (UI-based configuration, then verify with test event)

**Related Documentation:** CloudDesk API Platform Administrator Guide

**Difficulty Level:** Intermediate

---

### 29. Question: Do webhook events guarantee strict delivery order?

**Answer:** No. Webhook delivery does not guarantee strict ordering, particularly under retry conditions. Design your integration to compare an event's timestamp or version against last-processed state rather than assuming sequential arrival.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform Troubleshooting Guide

**Difficulty Level:** Advanced

---

### 30. Question: How do I get access to dedicated webhook infrastructure for high-volume delivery?

**Answer:** Dedicated webhook infrastructure is available on Enterprise plans. Contact your Corvex account representative or Technical Account Manager to discuss configuration for your expected volume.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform Product Overview

**Difficulty Level:** Advanced

---

## Category: Rate Limiting

### 31. Question: What are the API rate limits per plan?

**Answer:** Starter allows 60 requests per minute, Professional allows 300 requests per minute, and Enterprise offers elevated or custom limits.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform Product Overview

**Difficulty Level:** Beginner

---

### 32. Question: How do I check my current rate limit usage programmatically?

**Answer:** Rate limit status is returned in response headers on every API request, including remaining quota and reset time.

**Commands:**
```
curl -i -X GET https://api.corvexcloud.com/v1/tickets \
  -H "Authorization: Bearer YOUR_API_KEY"
# Look for headers:
# X-RateLimit-Limit: 300
# X-RateLimit-Remaining: 287
# X-RateLimit-Reset: 1735689600
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Intermediate

---

### 33. Question: How should I implement backoff when I receive a 429 response?

**Answer:** Implement exponential backoff, respecting the `Retry-After` header if present, rather than retrying immediately.

**Commands:**
```
# Example (pseudocode)
if response.status_code == 429:
    wait = int(response.headers.get("Retry-After", 2 ** attempt))
    sleep(wait)
    retry()
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Intermediate

---

### 34. Question: Is the rate limit per API key or per account?

**Answer:** Depending on your plan configuration, the rate limit may apply per key, with an additional shared account-level ceiling. Review aggregate usage by key under Admin Dashboard > API Platform > Rate Limits & Usage.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform Troubleshooting Guide

**Difficulty Level:** Intermediate

---

### 35. Question: How do I request a temporary elevated rate limit for a data migration?

**Answer:** Contact Corvex support ahead of a planned large-scale migration to discuss a temporary elevated rate limit, available for Enterprise accounts.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform Troubleshooting Guide

**Difficulty Level:** Advanced

---

### 36. Question: Does the rate limit apply to webhook deliveries as well as API requests?

**Answer:** No. Rate limiting applies to inbound API requests you make to Corvex; outbound webhook deliveries from Corvex to your endpoint are governed separately by webhook delivery infrastructure, not your account's API rate limit.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform Product Overview

**Difficulty Level:** Intermediate

---

## Category: Widget and SDK Installation

### 37. Question: How do I install the CloudDesk Chat widget on my website?

**Answer:** Copy the installation snippet from Admin Dashboard > Chat Widget > Installation, and paste it into your site's HTML immediately before the closing `</body>` tag.

**Commands:**
```
<script>
  (function(c,d,e){/* widget loader */})(window,document,"CORVEX_WIDGET_ID");
</script>
```

**Related Documentation:** CloudDesk Chat User Manual

**Difficulty Level:** Beginner

---

### 38. Question: How do I allow the chat widget through a strict Content Security Policy?

**Answer:** Add the required Corvex Cloud domains to your `script-src`, `connect-src`, `frame-src`, and `style-src` CSP directives, as listed in the widget installation guide.

**Commands:**
```
Content-Security-Policy: script-src 'self' https://widget.corvexcloud.com; connect-src 'self' https://api.corvexcloud.com wss://realtime.corvexcloud.com;
```

**Related Documentation:** CloudDesk Chat Troubleshooting Guide

**Difficulty Level:** Advanced

---

### 39. Question: How do I install the CloudDesk Chat mobile SDK in an iOS app?

**Answer:** Add the SDK via your preferred dependency manager (Swift Package Manager or CocoaPods), initialize it with your SDK configuration key at app launch, and present the chat view controller where needed.

**Commands:**
```
# Podfile
pod 'CorvexChatSDK'

# AppDelegate.swift
CorvexChat.initialize(configKey: "YOUR_SDK_KEY")
```

**Related Documentation:** CloudDesk Chat Product Overview

**Difficulty Level:** Advanced

---

### 40. Question: How do I install the CloudDesk Chat mobile SDK in an Android app?

**Answer:** Add the SDK dependency via Gradle, initialize it in your Application class with your SDK configuration key, and launch the chat activity where needed.

**Commands:**
```
// build.gradle
implementation 'com.corvexcloud:chat-sdk:latest.release'

// Application.kt
CorvexChat.initialize(context, "YOUR_SDK_KEY")
```

**Related Documentation:** CloudDesk Chat Product Overview

**Difficulty Level:** Advanced

---

### 41. Question: How do I configure network security settings to allow the mobile SDK to connect on Android?

**Answer:** Update your app's network security configuration XML to permit connections to the domains listed in the mobile SDK documentation.

**Commands:**
```
<!-- res/xml/network_security_config.xml -->
<network-security-config>
  <domain-config>
    <domain includeSubdomains="true">corvexcloud.com</domain>
  </domain-config>
</network-security-config>
```

**Related Documentation:** CloudDesk Chat Troubleshooting Guide

**Difficulty Level:** Advanced

---

### 42. Question: How do I add an App Transport Security exception for the SDK on iOS?

**Answer:** Add the required domain exceptions to your app's Info.plist under `NSAppTransportSecurity` if your app's default ATS configuration is more restrictive than needed.

**Commands:**
```
<key>NSAppTransportSecurity</key>
<dict>
  <key>NSExceptionDomains</key>
  <dict>
    <key>corvexcloud.com</key>
    <dict>
      <key>NSIncludesSubdomains</key><true/>
    </dict>
  </dict>
</dict>
```

**Related Documentation:** CloudDesk Chat Troubleshooting Guide

**Difficulty Level:** Advanced

---

### 43. Question: How do I connect a support email address for ticket intake?

**Answer:** Navigate to Admin Dashboard > Channels > Email, choose to connect an existing mailbox or use a Corvex-hosted address, and follow the guided authorization or DNS configuration steps.

**Commands:**
```
# Example DNS records for a custom domain (values provided during setup)
MX   support.example.com   10 mx.corvexcloud.com
TXT  support.example.com   "v=spf1 include:corvexcloud.com ~all"
```

**Related Documentation:** CloudDesk Tickets User Manual

**Difficulty Level:** Intermediate

---

### 44. Question: How do I embed the web form widget for ticket submission?

**Answer:** Configure your desired fields under Admin Dashboard > Channels > Web Form, then copy the provided embed snippet into your website's HTML.

**Commands:**
```
<div id="corvex-webform" data-form-id="FORM_ID"></div>
<script src="https://forms.corvexcloud.com/embed.js" async></script>
```

**Related Documentation:** CloudDesk Tickets User Manual

**Difficulty Level:** Beginner

---

### 45. Question: How do I verify my widget installation is working correctly?

**Answer:** Use the Verify Installation tool under Admin Dashboard > Chat Widget > Installation, which checks for a correctly loading widget script from a clean browser session.

**Commands:** Not applicable (UI-based verification)

**Related Documentation:** CloudDesk Chat Troubleshooting Guide

**Difficulty Level:** Beginner

---

### 46. Question: How do I load the widget asynchronously to avoid blocking page load?

**Answer:** Use the current recommended installation snippet, which loads asynchronously by default. Older, synchronous snippet versions should be replaced if still in use.

**Commands:**
```
<script async src="https://widget.corvexcloud.com/loader.js" data-widget-id="WIDGET_ID"></script>
```

**Related Documentation:** CloudDesk Chat Troubleshooting Guide

**Difficulty Level:** Intermediate

---

## Category: SSO and SCIM

### 47. Question: How do I configure SAML SSO for my account?

**Answer:** Navigate to Admin Dashboard > Security > Single Sign-On, enter your identity provider's metadata URL or upload the metadata file, map required attributes, and test the connection before enforcing SSO account-wide.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Chat Administrator Guide

**Difficulty Level:** Intermediate

---

### 48. Question: What SAML attributes does Corvex Cloud require?

**Answer:** At minimum, `email` and `name` attributes are required. Additional attributes such as role or group membership can be mapped for use with SCIM-based provisioning.

**Commands:**
```
<!-- Example SAML attribute statement -->
<saml:AttributeStatement>
  <saml:Attribute Name="email">
    <saml:AttributeValue>user@example.com</saml:AttributeValue>
  </saml:Attribute>
  <saml:Attribute Name="name">
    <saml:AttributeValue>Jane Doe</saml:AttributeValue>
  </saml:Attribute>
</saml:AttributeStatement>
```

**Related Documentation:** CloudDesk Chat Administrator Guide

**Difficulty Level:** Advanced

---

### 49. Question: How do I configure SCIM provisioning?

**Answer:** Navigate to Admin Dashboard > Security > SCIM, generate a SCIM bearer token, and configure your identity provider's SCIM connector using the provided base URL and token.

**Commands:**
```
curl -X GET https://api.corvexcloud.com/scim/v2/Users \
  -H "Authorization: Bearer SCIM_TOKEN"
```

**Related Documentation:** CloudDesk Chat Administrator Guide

**Difficulty Level:** Advanced

---

### 50. Question: How do I test SSO before enforcing it account-wide?

**Answer:** Use the provided test login flow within the SSO configuration screen, which lets you validate the connection with a sample login before making SSO mandatory for all users.

**Commands:** Not applicable (UI-based test flow)

**Related Documentation:** CloudDesk Chat Administrator Guide

**Difficulty Level:** Intermediate

---

### 51. Question: How do I resolve a SAML certificate expiration issue?

**Answer:** Obtain updated metadata or a renewed certificate from your identity provider, then re-upload it under Admin Dashboard > Security > Single Sign-On, and retest the connection before certificate expiration to avoid a login outage.

**Commands:** Not applicable

**Related Documentation:** CloudDesk Chat Troubleshooting Guide

**Difficulty Level:** Intermediate

---

### 52. Question: Can I map SAML groups to Corvex Cloud roles automatically?

**Answer:** Yes, on Enterprise plans using SCIM-based provisioning, where identity provider group membership can be mapped to specific Corvex Cloud roles during user provisioning.

**Commands:** Not applicable (configured via SCIM connector settings)

**Related Documentation:** CloudDesk Chat Administrator Guide

**Difficulty Level:** Advanced

---

### 53. Question: How do I deprovision a user automatically when they're removed from my identity provider?

**Answer:** With SCIM enabled, removing a user or their group membership in your identity provider triggers a deprovisioning event that deactivates their Corvex Cloud account automatically.

**Commands:**
```
curl -X DELETE https://api.corvexcloud.com/scim/v2/Users/USER_ID \
  -H "Authorization: Bearer SCIM_TOKEN"
```

**Related Documentation:** CloudDesk Tickets Administrator Guide

**Difficulty Level:** Advanced

---

### 54. Question: How do I configure IP allowlisting?

**Answer:** Navigate to Admin Dashboard > Security > IP Allowlisting and add approved IP ranges in CIDR notation.

**Commands:**
```
# Example allowlist entries
203.0.113.0/24
198.51.100.42/32
```

**Related Documentation:** CloudDesk Chat Administrator Guide

**Difficulty Level:** Intermediate

---

## Category: Integrations

### 55. Question: How do I connect a CRM integration?

**Answer:** Navigate to Admin Dashboard > Integrations, select your CRM platform, and click Connect, then follow the guided OAuth authorization flow specific to that CRM.

**Commands:** Not applicable (UI-based OAuth flow)

**Related Documentation:** CloudDesk Tickets Product Overview

**Difficulty Level:** Beginner

---

### 56. Question: How do I generate a Zapier API key?

**Answer:** Navigate to Admin Dashboard > Integrations > Zapier > Generate Key, then enter the resulting key when configuring your Zap's Corvex Cloud connection in Zapier.

**Commands:** Not applicable (UI-based)

**Related Documentation:** CloudDesk Chat Administrator Guide

**Difficulty Level:** Beginner

---

### 57. Question: How do I connect a data warehouse export destination?

**Answer:** Navigate to Admin Dashboard > Analytics > Data Warehouse Export (Enterprise only), click Add Connection, select your destination platform, and follow the guided authentication flow.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Analytics Administrator Guide

**Difficulty Level:** Advanced

---

### 58. Question: What format is data delivered in for data warehouse export?

**Answer:** Data is delivered in a structured, columnar format compatible with common business intelligence and data warehouse platforms, as detailed in the developer documentation's export schema reference.

**Commands:** Not applicable

**Related Documentation:** CloudDesk Analytics Product Overview

**Difficulty Level:** Advanced

---

### 59. Question: How do I link a ticket to an issue in a project management tool?

**Answer:** With the relevant project management integration connected, use the Link Issue action from within a ticket, select the target project, and create or link to an existing issue.

**Commands:** Not applicable (UI-based action)

**Related Documentation:** CloudDesk Tickets Product Overview

**Difficulty Level:** Beginner

---

### 60. Question: How do I set up a custom integration using the Corvex partner API (Enterprise)?

**Answer:** Contact your Corvex Technical Account Manager to establish partner API credentials, then follow the partner API-specific documentation for authentication and available bespoke endpoints.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform Administrator Guide

**Difficulty Level:** Advanced

---

### 61. Question: How do I troubleshoot a CRM integration showing an "Error" status?

**Answer:** The CRM's authentication token has likely expired. Navigate to Admin Dashboard > Integrations, select the CRM, and reauthorize the connection following the guided flow.

**Commands:** Not applicable

**Related Documentation:** CloudDesk Chat Troubleshooting Guide

**Difficulty Level:** Intermediate

---

### 62. Question: How does customer matching work between Corvex Cloud and a connected e-commerce platform?

**Answer:** Matching is based on email address by default. A customer's chat or ticket email must exactly match their e-commerce account email for order data to display correctly.

**Commands:** Not applicable

**Related Documentation:** CloudDesk Chat Troubleshooting Guide

**Difficulty Level:** Intermediate

---

### 63. Question: How do I disconnect an integration without losing previously synced data?

**Answer:** Select the integration under Admin Dashboard > Integrations and click Disconnect. This halts future sync but does not delete data already synced or created as a result of the integration.

**Commands:** Not applicable

**Related Documentation:** CloudDesk Chat Administrator Guide

**Difficulty Level:** Beginner

---

### 64. Question: How do I request Corvex-assisted support for a complex custom integration?

**Answer:** Submit a request from Admin Dashboard > API Platform > Request Integration Support (Professional and Enterprise), including as much technical detail as possible to expedite the response.

**Commands:** Not applicable (UI-based request)

**Related Documentation:** CloudDesk API Platform Administrator Guide

**Difficulty Level:** Intermediate

---

## Category: Data Import and Export

### 65. Question: How do I export conversation and ticket data?

**Answer:** Navigate to Admin Dashboard > Data > Export, select the data scope and date range, and click Generate Export. Larger exports are prepared asynchronously and delivered as a downloadable file.

**Commands:** Not applicable (UI-based export)

**Related Documentation:** CloudDesk Tickets Administrator Guide

**Difficulty Level:** Beginner

---

### 66. Question: What file formats are available for data export?

**Answer:** Tabular data (ticket lists, customer records) exports as CSV. Structured configuration data (workflow rules, SLA definitions) exports as JSON.

**Commands:** Not applicable

**Related Documentation:** CloudDesk Tickets Administrator Guide

**Difficulty Level:** Beginner

---

### 67. Question: How do I bulk-import historical tickets from another system?

**Answer:** Download the current import template under Admin Dashboard > Data > Import, populate it with your historical data matching the exact column headers to field identifiers, and upload the file.

**Commands:** Not applicable (template-based CSV upload)

**Related Documentation:** CloudDesk Tickets Troubleshooting Guide

**Difficulty Level:** Intermediate

---

### 68. Question: My bulk import failed partway through. How do I identify which records failed?

**Answer:** Review the automatically generated import error report following a failed or partial import, which identifies the specific rows and fields causing validation rejection.

**Commands:** Not applicable

**Related Documentation:** CloudDesk Tickets Troubleshooting Guide

**Difficulty Level:** Intermediate

---

### 69. Question: How do I restore an accidentally deleted ticket?

**Answer:** Navigate to Admin Dashboard > Data > Recently Deleted, locate the item, and click Restore, provided the deletion occurred within your plan's recovery window.

**Commands:** Not applicable (UI-based restoration)

**Related Documentation:** CloudDesk Tickets Administrator Guide

**Difficulty Level:** Beginner

---

### 70. Question: How do I export API key and webhook configuration for backup purposes?

**Answer:** Navigate to Admin Dashboard > API Platform > Export Configuration, select the scope (key metadata, webhook configuration, or security policy settings), and generate a downloadable JSON export. Note that API key secret values themselves are never included.

**Commands:** Not applicable (UI-based export)

**Related Documentation:** CloudDesk API Platform Administrator Guide

**Difficulty Level:** Intermediate

---

### 71. Question: How do I use the API to export data programmatically instead of the UI export tool?

**Answer:** Use paginated GET requests against the relevant resource endpoint (tickets, customers, etc.), iterating through all pages using cursor-based pagination.

**Commands:**
```
curl -X GET "https://api.corvexcloud.com/v1/tickets?limit=100&created_after=2026-01-01T00:00:00Z" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Intermediate

---

### 72. Question: How do I preserve historical timestamps when bulk-importing backdated tickets?

**Answer:** Include a `created_at` value in ISO 8601 format for each row in your import file if your import template supports timestamp override; otherwise, imported records default to the import date.

**Commands:** Not applicable (template-based)

**Related Documentation:** CloudDesk Analytics Troubleshooting Guide

**Difficulty Level:** Advanced

---

## Category: Automation and Workflow Configuration

### 73. Question: How do I create an assignment rule based on skill tags?

**Answer:** Navigate to Admin Dashboard > Workflow > Assignment, create a new rule, set the condition to match a specific skill tag, and assign agents the corresponding skill tag under their user profile.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Tickets Administrator Guide

**Difficulty Level:** Intermediate

---

### 74. Question: How do I configure an SLA target by priority level?

**Answer:** Navigate to Admin Dashboard > Workflow > SLAs, create a rule scoped to a specific priority or category, and define response and resolution time targets, along with breach alert recipients.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Tickets Administrator Guide

**Difficulty Level:** Intermediate

---

### 75. Question: How do I build a macro that applies a tag, changes status, and sends a reply in one action?

**Answer:** Navigate to Settings > Macros, create a new macro, and add each desired action (tag, status change, reply) as a step; agents can then run the macro from the ticket view.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Tickets User Manual

**Difficulty Level:** Beginner

---

### 76. Question: How do I configure a routing rule to send high-value customers to a priority queue?

**Answer:** Configure a routing rule referencing a CRM-sourced field (such as account tier) as a condition, ensuring the CRM integration is actively syncing that field correctly.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Chat Troubleshooting Guide

**Difficulty Level:** Advanced

---

### 77. Question: How do I set up an automation rule that reopens a ticket when a customer replies?

**Answer:** This behavior is included by default in standard workflow automation. To scope it more narrowly (for example, excluding auto-generated bounce replies), adjust the rule's trigger conditions under Admin Dashboard > Workflow > Automation.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Tickets Troubleshooting Guide

**Difficulty Level:** Intermediate

---

### 78. Question: How do I configure business-hours-only SLA calculation?

**Answer:** Enable business-hours-only calculation under Admin Dashboard > Workflow > SLAs, and confirm your account's configured business hours and time zone are accurate.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Tickets Troubleshooting Guide

**Difficulty Level:** Intermediate

---

### 79. Question: How do I configure a fallback routing rule to catch unmatched conversations?

**Answer:** Add a rule as the last entry in your routing configuration with no specific conditions, ensuring every conversation has a defined assignment path even if it doesn't match a more specific rule.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Chat Troubleshooting Guide

**Difficulty Level:** Intermediate

---

### 80. Question: How do I use the API to trigger an automation action programmatically?

**Answer:** Rather than triggering an automation rule directly, send a PATCH request to update the relevant field (status, tag, assignment) that your automation rule is configured to watch for.

**Commands:**
```
curl -X PATCH https://api.corvexcloud.com/v1/tickets/12345 \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tags":["escalated"]}'
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Advanced

---

## Category: Security Configuration

### 81. Question: How do I enable mandatory biometric lock for CloudDesk Mobile account-wide?

**Answer:** Navigate to Admin Dashboard > Mobile > Security Policy > Biometric Lock, and set the policy to Mandatory. Users without biometric hardware will be required to use their device passcode as a fallback.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Mobile Administrator Guide

**Difficulty Level:** Beginner

---

### 82. Question: How do I remotely revoke a lost mobile device's session?

**Answer:** Navigate to Admin Dashboard > Mobile > Device Sessions, locate the device, and click Revoke Session. This takes effect on the device's next connectivity check-in.

**Commands:** Not applicable (UI-based action)

**Related Documentation:** CloudDesk Mobile Administrator Guide

**Difficulty Level:** Beginner

---

### 83. Question: How do I configure a mandatory API key rotation policy?

**Answer:** Navigate to Admin Dashboard > API Platform > Security > Key Rotation Policy, and set a rotation interval. Keys approaching or exceeding the interval are flagged, and, if mandatory rotation is enabled, may be automatically disabled until rotated.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk API Platform Administrator Guide

**Difficulty Level:** Intermediate

---

### 84. Question: How do I set a custom session timeout duration?

**Answer:** Navigate to Admin Dashboard > Security > Sessions, and configure the desired automatic timeout duration. A separate, mobile-specific timeout can be configured under Admin Dashboard > Mobile > Security Policy.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Chat Administrator Guide

**Difficulty Level:** Beginner

---

### 85. Question: How do I restrict scheduled report delivery to internal email domains only?

**Answer:** Navigate to Admin Dashboard > Analytics > Security > Delivery Restrictions (Professional and Enterprise), and enable internal-domain-only delivery.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Analytics Administrator Guide

**Difficulty Level:** Intermediate

---

### 86. Question: How do I disable external dashboard sharing account-wide?

**Answer:** Navigate to Admin Dashboard > Analytics > Security > Sharing Controls, and disable external sharing to restrict dashboard visibility to authenticated internal users only.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Analytics Administrator Guide

**Difficulty Level:** Intermediate

---

### 87. Question: How do I set a maximum local data caching limit for mobile devices?

**Answer:** Navigate to Admin Dashboard > Mobile > Security Policy > Data Caching, and set the maximum amount of case data permitted to be cached locally on a device.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Mobile Administrator Guide

**Difficulty Level:** Intermediate

---

### 88. Question: How do I review which API keys have write access to my account?

**Answer:** Navigate to Admin Dashboard > API Platform > API Keys, which lists every key's scope (read-only or read/write) alongside its owner and creation date.

**Commands:** Not applicable (UI-based review)

**Related Documentation:** CloudDesk API Platform Administrator Guide

**Difficulty Level:** Beginner

---

## Category: Mobile Technical Configuration

### 89. Question: How do I configure managed app configuration for CloudDesk Mobile via MDM?

**Answer:** Reference the managed app configuration schema in the developer documentation to correctly format your MDM's configuration payload (for example, pre-filling the organization domain), then deploy it through your MDM console.

**Commands:**
```
<!-- Example MDM managed configuration payload -->
<dict>
  <key>organizationDomain</key>
  <string>yourcompany.corvexcloud.com</string>
</dict>
```

**Related Documentation:** CloudDesk Mobile Administrator Guide

**Difficulty Level:** Advanced

---

### 90. Question: How do I issue a remote wipe command to a managed device?

**Answer:** Use your MDM platform's own remote wipe capability, which operates independently of and in addition to Corvex's in-app session revocation.

**Commands:** Not applicable (MDM-platform-specific)

**Related Documentation:** CloudDesk Mobile Administrator Guide

**Difficulty Level:** Advanced

---

### 91. Question: How do I configure push notification credentials for the CloudDesk Chat mobile SDK?

**Answer:** Upload your APNs certificate (iOS) and FCM server key (Android) under Admin Dashboard > Chat Widget > Mobile SDK > Push Configuration.

**Commands:** Not applicable (UI-based upload)

**Related Documentation:** CloudDesk Chat Troubleshooting Guide

**Difficulty Level:** Advanced

---

### 92. Question: How do I pass an authenticated user identifier to the mobile SDK for persistent conversation history?

**Answer:** Pass your app's authenticated user ID to the SDK's identity configuration method at initialization or login, ensuring conversation history persists correctly across app sessions for logged-in users.

**Commands:**
```
CorvexChat.identify(userId: "internal_user_12345")
```

**Related Documentation:** CloudDesk Chat Troubleshooting Guide

**Difficulty Level:** Advanced

---

### 93. Question: How do I restrict CloudDesk Mobile access for a specific role?

**Answer:** Navigate to Admin Dashboard > Mobile > Security Policy > Role Restrictions (Professional and Enterprise), and disable mobile access for the relevant role.

**Commands:** Not applicable (UI-based configuration)

**Related Documentation:** CloudDesk Mobile Administrator Guide

**Difficulty Level:** Intermediate

---

### 94. Question: How do I check which app version a specific user's device is running?

**Answer:** Navigate to Admin Dashboard > Users > [User] > Devices, or Admin Dashboard > Mobile > Device Sessions, both of which display the app version currently in use.

**Commands:** Not applicable (UI-based review)

**Related Documentation:** CloudDesk Mobile Administrator Guide

**Difficulty Level:** Beginner

---

## Category: Sandbox and Testing (Enterprise)

### 95. Question: How do I access the sandbox environment?

**Answer:** Use the environment switcher in the top navigation bar of the Developer Portal to move between production and sandbox. Sandbox access requires an Enterprise plan and the sandbox permission on your role.

**Commands:** Not applicable (UI-based switch)

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Intermediate

---

### 96. Question: How do I reset sandbox test data?

**Answer:** Navigate to Admin Dashboard > API Platform > Sandbox Management, and use the Reset Sandbox function to clear test data before a new testing cycle.

**Commands:** Not applicable (UI-based action)

**Related Documentation:** CloudDesk API Platform Administrator Guide

**Difficulty Level:** Intermediate

---

### 97. Question: How do I point my integration at the sandbox API endpoint instead of production?

**Answer:** Use the sandbox base URL (`api-sandbox.corvexcloud.com`) along with a sandbox-specific API key, which is entirely separate from your production key.

**Commands:**
```
curl -X GET https://api-sandbox.corvexcloud.com/v1/tickets \
  -H "Authorization: Bearer SANDBOX_API_KEY"
```

**Related Documentation:** CloudDesk API Platform User Manual

**Difficulty Level:** Intermediate

---

### 98. Question: How do I test a webhook in sandbox without it reaching my production endpoint?

**Answer:** Configure a separate webhook endpoint specifically for sandbox testing, distinct from your production webhook URL, to ensure test events never reach production-handling logic.

**Commands:** Not applicable (UI-based configuration, separate endpoints)

**Related Documentation:** CloudDesk API Platform Troubleshooting Guide

**Difficulty Level:** Intermediate

---

### 99. Question: Is sandbox performance representative of production performance?

**Answer:** No. Sandbox infrastructure is provisioned for functional testing, not performance testing, and is not scaled to match production performance characteristics. For load or performance testing, contact your Technical Account Manager.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform Troubleshooting Guide

**Difficulty Level:** Advanced

---

### 100. Question: How do I request early access to a new API endpoint before general availability?

**Answer:** Early access endpoints are available to Enterprise customers. Contact your Technical Account Manager or Corvex developer support to request access and receive documentation for endpoints not yet generally available.

**Commands:** Not applicable

**Related Documentation:** CloudDesk API Platform Product Overview

**Difficulty Level:** Advanced

---

*This Technical FAQ covers common configuration and integration questions for Corvex Cloud. For step-by-step diagnostic troubleshooting, refer to the Troubleshooting Guide for the relevant CloudDesk product. For complete endpoint references, refer to the Corvex Cloud developer documentation.*
