# CloudDesk API Platform
## Troubleshooting Guide

*Corvex Cloud — CloudDesk API Platform*
*This guide documents known issues, their causes, and their resolutions for CloudDesk API Platform. It is intended for developers, administrators, and technical staff diagnosing problems with API and webhook integrations. For general usage instructions, refer to the CloudDesk API Platform User Manual. For configuration guidance, refer to the CloudDesk API Platform Administrator Guide.*

---

## How to Use This Guide

Issues are grouped by category. Each entry includes the symptoms you may observe, the most common underlying cause, a recommended solution, steps to prevent recurrence, and related issues you may want to review if the listed solution does not fully resolve your problem.

---

## Section 1: Authentication and API Keys

### CDP-1001 — API Request Returns 401 Unauthorized

**Symptoms:** Every request using a specific API key fails with a 401 Unauthorized response, even though the key was working previously.

**Cause:** The API key was rotated or revoked, either intentionally by an administrator or automatically due to a mandatory rotation policy being reached.

**Solution:** Check the key's status under **Admin Dashboard > API Platform > API Keys**; if revoked or expired, generate a new key and update the value in your integration's configuration.

**Prevention:** Subscribe to key rotation policy notifications so your team has advance warning before a mandatory rotation deadline.

**Related Issues:** CDP-1002, CDP-1003

---

### CDP-1002 — API Key Works in Testing but Fails in Production

**Symptoms:** A request succeeds when tested manually but fails with an authentication error when run from the production system.

**Cause:** The production system is using a different, older, or incorrectly copied key value than the one tested manually, often due to a key being partially truncated during copy-paste into a configuration file or secrets manager.

**Solution:** Re-copy the full key value directly from **API Keys** into the production configuration, verifying no leading or trailing whitespace or truncation occurred.

**Prevention:** Use a secrets manager with integrity verification where possible, rather than manual copy-paste into production configuration.

**Related Issues:** CDP-1001

---

### CDP-1003 — Newly Generated API Key Not Working Immediately

**Symptoms:** A freshly generated API key returns an authentication error on the first few requests.

**Cause:** A brief propagation delay between key generation and full activation across the platform's authentication infrastructure.

**Solution:** Wait approximately one minute after generating a new key before making requests; if authentication errors persist beyond a few minutes, verify the key was copied correctly.

**Prevention:** Build a short delay into automated deployment scripts that generate and immediately use a new API key.

**Related Issues:** CDP-1002

---

### CDP-1004 — Cannot Retrieve a Previously Generated API Key's Value

**Symptoms:** A developer attempts to view the value of an existing API key and finds it unavailable.

**Cause:** API key secret values are displayed only once at creation time and are not retrievable afterward, by design, for security reasons.

**Solution:** Generate a new API key and update your integration with the new value; the original key's value cannot be recovered under any circumstance.

**Prevention:** Store newly generated key values immediately and securely (e.g., in a secrets manager) at the time of creation, since this is the only opportunity to capture the value.

**Related Issues:** none

---

### CDP-1005 — Read-Only Key Rejected When Attempting a Write Operation

**Symptoms:** A request to create or update a resource fails with a permissions error despite the key appearing valid.

**Cause:** The API key was scoped as read-only at creation time, and the account's plan or the key's specific configuration does not permit write access.

**Solution:** Generate a new key with read/write scope, available on Professional and Enterprise plans, and update your integration accordingly. Starter plan accounts are limited to read-only API access account-wide.

**Prevention:** Confirm the required scope for your integration's use case before generating a key, to avoid a late-stage discovery that read-only access is insufficient.

**Related Issues:** CDP-1006

---

### CDP-1006 — API Key Scope More Restrictive Than Expected

**Symptoms:** A read/write key can read data but fails when attempting to modify a specific resource type.

**Cause:** Some accounts configure endpoint-level scope restrictions in addition to the general read/write designation, limiting a key to specific resource types (for example, tickets but not users).

**Solution:** Review the key's specific scope configuration under **API Keys**, and adjust or generate a new key with the necessary endpoint-level access.

**Prevention:** Document each API key's intended scope clearly at creation time to avoid ambiguity about what access level was intended.

**Related Issues:** CDP-1005

---

### CDP-1007 — Multiple Integrations Sharing a Single API Key Causing Confusion

**Symptoms:** It becomes difficult to determine which integration is responsible for a given request pattern or error in usage monitoring.

**Cause:** A single API key was reused across multiple, unrelated integrations rather than issuing a dedicated key per integration.

**Solution:** Generate separate, dedicated API keys for each distinct integration, and migrate each integration to its own key.

**Prevention:** Adopt a one-key-per-integration policy from the outset, as recommended in the CloudDesk API Platform User Manual, to preserve clear usage attribution.

**Related Issues:** none

---

## Section 2: Rate Limiting

### CDP-2001 — Requests Failing with 429 Too Many Requests

**Symptoms:** API requests begin failing with a 429 status code during periods of high integration activity.

**Cause:** The integration is exceeding the rate limit associated with its plan tier (60 requests/minute on Starter, 300 on Professional, elevated/custom on Enterprise).

**Solution:** Review current usage under **Admin Dashboard > API Platform > Rate Limits & Usage**, and implement request throttling or batching in your integration to remain within the applicable limit, or consider a plan upgrade if sustained higher volume is required.

**Prevention:** Design integrations to respect published rate limits proactively, using response headers indicating remaining quota where provided, rather than reacting only after receiving 429 errors.

**Related Issues:** CDP-2002

---

### CDP-2002 — Integration Not Backing Off Properly After Rate Limit Errors

**Symptoms:** A 429 error triggers an immediate retry, which also fails, resulting in a rapid failure loop.

**Cause:** The integration's retry logic does not implement a backoff delay, retrying immediately rather than waiting an appropriate interval.

**Solution:** Implement exponential backoff in your integration's retry logic, respecting any `Retry-After` header returned with the 429 response.

**Prevention:** Follow the retry and backoff guidance provided in the Corvex Cloud developer documentation when initially building any integration.

**Related Issues:** CDP-2001

---

### CDP-2003 — Rate Limit Reached Despite Low Apparent Request Volume

**Symptoms:** An integration hits its rate limit despite the developer's own estimate of request volume appearing well within the limit.

**Cause:** Multiple API keys or integrations under the same account may share a combined account-level rate limit ceiling in addition to any per-key limit, depending on plan configuration.

**Solution:** Review aggregate account-wide usage under **Admin Dashboard > API Platform > Rate Limits & Usage**, broken down by key, to identify whether another integration is contributing to the shared limit.

**Prevention:** Monitor usage by key regularly, particularly in accounts running multiple concurrent integrations, to catch unexpected contribution to a shared limit early.

**Related Issues:** CDP-2001

---

### CDP-2004 — Bulk Data Migration Repeatedly Hitting Rate Limits

**Symptoms:** A one-time bulk data migration script consistently triggers rate limit errors despite backoff logic being implemented.

**Cause:** The migration's total required request volume, even with proper backoff, exceeds what is practical within the account's standard rate limit over a reasonable migration window.

**Solution:** Contact Corvex support ahead of a planned large-scale migration to discuss a temporary elevated rate limit, available for Enterprise accounts, or plan the migration across a longer time window compatible with standard limits.

**Prevention:** Plan bulk operations in advance and coordinate with Corvex before beginning, rather than discovering rate limit constraints mid-migration.

**Related Issues:** CDP-2001

---

## Section 3: REST API Requests and Responses

### CDP-3001 — API Request Returns 404 for a Resource Known to Exist

**Symptoms:** A GET request for a specific ticket or chat ID returns a 404 Not Found, despite the resource being visible in the standard workspace.

**Cause:** The API key's scope does not include access to the specific resource type or team the resource belongs to, and the platform returns 404 rather than 403 for resources outside a key's visibility, as a deliberate security practice to avoid confirming the existence of inaccessible resources.

**Solution:** Confirm the API key's scope includes the relevant resource type and team under **API Keys**, and adjust scope if necessary.

**Prevention:** Document expected resource scope clearly when provisioning a new API key for an integration with a specific, limited purpose.

**Related Issues:** CDP-1006

---

### CDP-3002 — Unexpected 500 Internal Server Error on a Specific Request

**Symptoms:** A specific, repeatable request consistently returns a 500 error, while similar requests succeed.

**Cause:** This may indicate a platform-side issue with a specific edge case in the request payload; it is not typically a client-side configuration error.

**Solution:** Capture the full request (with sensitive data redacted) and the response, including any request ID provided in the response headers, and report it to Corvex developer support for investigation.

**Prevention:** No client-side preventive action is generally available for genuine platform-side errors; reporting with full detail helps Corvex resolve the underlying issue.

**Related Issues:** none

---

### CDP-3003 — Pagination Returning Duplicate Records Across Pages

**Symptoms:** Iterating through paginated results using an integration script returns the same record on two different pages.

**Cause:** New records were created or existing records were updated between paginated requests, shifting the underlying result ordering if pagination is based on a mutable sort field rather than a stable cursor.

**Solution:** Use cursor-based pagination, where available, rather than offset-based pagination, since cursor-based pagination is stable against concurrent data changes.

**Prevention:** Prefer cursor-based pagination for any integration iterating through a data set that may be actively changing during iteration.

**Related Issues:** none

---

### CDP-3004 — Date Fields Returned in Unexpected Time Zone

**Symptoms:** Timestamp fields in API responses do not match the expected local time zone.

**Cause:** API responses return timestamps in UTC by design, and the consuming integration is not converting to the intended local time zone before display or comparison.

**Solution:** Convert UTC timestamps to the desired local time zone within your integration code; the API does not return pre-localized timestamps.

**Prevention:** Document this UTC-by-default behavior clearly for any team building a new integration to avoid repeated confusion.

**Related Issues:** none

---

### CDP-3005 — Request Payload Rejected with a Validation Error

**Symptoms:** A POST or PATCH request fails with a validation error despite the payload appearing correctly formatted.

**Cause:** A field expected as a string is being sent as a different data type (e.g., a numeric ticket ID sent as an integer rather than a string), or a required field was omitted.

**Solution:** Review the specific validation error message returned in the response body, which identifies the offending field, and compare your payload against the current endpoint schema in the developer documentation.

**Prevention:** Validate request payloads against the published schema before sending, particularly after any endpoint documentation update.

**Related Issues:** CDP-3006

---

### CDP-3006 — Custom Field Not Settable via the API

**Symptoms:** An API request attempting to set a custom field's value succeeds but the value does not appear on the resulting ticket.

**Cause:** The custom field's internal identifier used in the API request does not match its actual identifier, which can differ from its display label.

**Solution:** Retrieve the correct field identifier via the fields listing endpoint rather than assuming it matches the field's display name, and update your request accordingly.

**Prevention:** Always retrieve field identifiers programmatically rather than hardcoding based on assumed naming conventions.

**Related Issues:** CDP-3005

---

### CDP-3007 — API Response Missing an Expected Field

**Symptoms:** A field visible in the standard workspace does not appear in the corresponding API response for the same resource.

**Cause:** The field was not included in the requested response's field selection, if your integration is using field filtering to limit response payload size, or the field requires a specific API version not currently in use.

**Solution:** Review the request's field selection parameters and API version header, adjusting as needed to include the desired field.

**Prevention:** Reference the current endpoint documentation for the specific field selection syntax rather than assuming all fields are returned by default.

**Related Issues:** none

---

### CDP-3008 — Bulk Endpoint Silently Skipping Some Records

**Symptoms:** A bulk update request reports success but not all intended records reflect the change.

**Cause:** One or more records in the batch failed individual validation, and the bulk endpoint processes valid records while reporting per-record failures in a separate section of the response rather than failing the entire batch.

**Solution:** Review the full response body for a per-record status or error array, rather than relying solely on the overall request's success status code.

**Prevention:** Always parse and check per-record results from bulk endpoints, since a 200-level overall status does not guarantee every individual record succeeded.

**Related Issues:** none

---

## Section 4: Webhooks

### CDP-4001 — Webhook Not Receiving Any Events

**Symptoms:** A configured webhook endpoint receives no events at all, despite matching activity occurring in the account.

**Cause:** The webhook endpoint URL is unreachable from the public internet, or the endpoint's event subscription does not include the event types actually occurring.

**Solution:** Confirm the endpoint is publicly reachable and review the webhook's event subscription under **Admin Dashboard > API Platform > Webhooks**, adding the relevant event types if missing.

**Prevention:** Use the **Send Test Event** function immediately after configuring a new webhook to confirm basic connectivity before relying on live events.

**Related Issues:** CDP-4002, CDP-4003

---

### CDP-4002 — Webhook Delivery Repeatedly Failing

**Symptoms:** The webhook delivery history shows repeated failed attempts for a specific endpoint.

**Cause:** The receiving endpoint is returning a non-success (4xx or 5xx) HTTP status code, or taking too long to respond, exceeding the delivery timeout.

**Solution:** Review delivery attempt history and response codes under **Admin Dashboard > API Platform > Webhooks**, and investigate the receiving endpoint's logs to determine why it is not responding successfully within the expected timeframe.

**Prevention:** Ensure your endpoint responds quickly with a success status immediately upon receipt, performing any lengthy processing asynchronously after acknowledging receipt.

**Related Issues:** CDP-4001, CDP-4004

---

### CDP-4003 — Webhook Signature Verification Failing

**Symptoms:** Your receiving system rejects incoming webhook payloads as invalid, despite Corvex showing successful delivery.

**Cause:** The signature verification logic on the receiving end is using an outdated or incorrect signing secret, often because the secret was rotated in the Developer Portal without updating the receiving system.

**Solution:** Confirm the current signing secret under **Admin Dashboard > API Platform > Webhooks**, and update your receiving system's verification logic to use the current value.

**Prevention:** Treat webhook signing secret rotation with the same coordination discipline as API key rotation, updating all dependent systems in the same change window.

**Related Issues:** none

---

### CDP-4004 — Webhook Receiving Duplicate Events

**Symptoms:** The same event is delivered to the webhook endpoint more than once.

**Cause:** The receiving endpoint did not respond with a success status quickly enough on the first attempt, causing the platform's at-least-once delivery guarantee to redeliver the event as a precaution.

**Solution:** Ensure your endpoint responds with a success status promptly, and design your endpoint to handle potential duplicate delivery idempotently, using the event's unique ID to detect and skip already-processed events.

**Prevention:** Build webhook consumers to be idempotent by design, since at-least-once delivery is standard, expected behavior for reliable webhook systems generally.

**Related Issues:** CDP-4002

---

### CDP-4005 — Webhook Events Arriving Out of Order

**Symptoms:** A sequence of related events (e.g., ticket created, then immediately updated) arrives at the receiving endpoint in reverse or otherwise unexpected order.

**Cause:** Webhook delivery does not guarantee strict ordering across events, particularly under retry conditions or high account activity volume.

**Solution:** Design your integration to be resilient to out-of-order delivery, for example by comparing an event's timestamp or version number against the last-processed state rather than assuming strict sequential arrival.

**Prevention:** Do not build webhook consumers that assume strict delivery ordering; reference the developer documentation's guidance on designing for eventual consistency.

**Related Issues:** CDP-4004

---

### CDP-4006 — Webhook Endpoint URL Change Not Taking Effect

**Symptoms:** After updating a webhook's endpoint URL, events continue to be delivered to the old URL.

**Cause:** The change was saved to a draft configuration rather than the active webhook, or a browser caching issue displayed a stale confirmation.

**Solution:** Confirm the updated URL is reflected under **Admin Dashboard > API Platform > Webhooks** after a page refresh, and use **Send Test Event** to confirm delivery to the new URL specifically.

**Prevention:** Always verify a webhook configuration change with a test event before considering the change complete.

**Related Issues:** none

---

### CDP-4007 — High-Volume Account Experiencing Webhook Delivery Delays

**Symptoms:** Webhook events arrive with a noticeable delay during periods of very high account activity.

**Cause:** Standard webhook infrastructure is processing a high volume of events across the shared delivery pipeline; Enterprise accounts have access to dedicated webhook infrastructure designed for higher-throughput, lower-latency delivery.

**Solution:** For accounts on Starter or Professional experiencing this consistently, consider Enterprise's dedicated webhook infrastructure, available as described in the CloudDesk API Platform Product Overview.

**Prevention:** Discuss expected webhook volume with your Corvex account representative ahead of a known high-traffic event to determine whether dedicated infrastructure is warranted.

**Related Issues:** none

---

## Section 5: Sandbox Environment (Enterprise)

### CDP-5001 — Sandbox Environment Not Accessible

**Symptoms:** The **Sandbox** option is missing from the environment switcher.

**Cause:** Sandbox access is an Enterprise-exclusive feature, or the specific user's role does not include sandbox permission even on an Enterprise account.

**Solution:** Confirm your plan tier under **Admin Dashboard > Billing & Plan**, and confirm your role includes sandbox access permission under **Admin Dashboard > Roles & Permissions**.

**Prevention:** Review plan-specific feature availability in the CloudDesk API Platform Product Overview before planning sandbox-dependent integration testing.

**Related Issues:** none

---

### CDP-5002 — Sandbox Data Not Resetting as Expected

**Symptoms:** Test data created during a previous sandbox testing session persists longer than expected, cluttering subsequent test runs.

**Cause:** Sandbox data persists until explicitly cleared or reset; it does not automatically reset on a fixed schedule.

**Solution:** Use the **Reset Sandbox** function under **Admin Dashboard > API Platform > Sandbox Management** to clear test data before beginning a new testing cycle.

**Prevention:** Build a sandbox reset step into your team's standard integration testing workflow, rather than assuming a clean state at the start of each session.

**Related Issues:** none

---

### CDP-5003 — API Key Created in Sandbox Not Working in Production

**Symptoms:** An API key generated while in the sandbox environment fails authentication when used against the production API endpoint.

**Cause:** Sandbox and production environments maintain entirely separate API keys by design, since they represent distinct, isolated data environments.

**Solution:** Generate a separate, dedicated API key within the production environment; a sandbox key cannot be used against production, and vice versa.

**Prevention:** Clearly label keys by environment at creation time to avoid confusion between sandbox and production credentials.

**Related Issues:** CDP-1001

---

### CDP-5004 — Webhook Test Events in Sandbox Reaching Production Endpoint

**Symptoms:** A webhook endpoint configured for production unexpectedly receives test events generated during sandbox testing.

**Cause:** The webhook endpoint was configured once and inadvertently shared across both environments, rather than being configured separately per environment.

**Solution:** Configure separate webhook endpoints for sandbox and production, ensuring sandbox test events are directed only to a designated test-receiving endpoint.

**Prevention:** Maintain clearly separate endpoint URLs (or at minimum, clearly distinguishable payload markers) for sandbox versus production webhook configurations.

**Related Issues:** CDP-5003

---

## Section 6: Documentation Portal and Request Tester

### CDP-6001 — Request Tester Returning a Different Result Than Production Code

**Symptoms:** A request sent using the Documentation section's built-in request tester succeeds, but the equivalent request from application code fails.

**Cause:** The request tester automatically applies the currently logged-in user's session context, which may differ from the API key and headers actually used by the production integration.

**Solution:** Confirm the request tester is configured to use the same specific API key intended for production, under the tester's authentication settings, rather than relying on session-based testing defaults.

**Prevention:** Always test using the exact API key and headers intended for production use, rather than the convenience of session-based testing.

**Related Issues:** none

---

### CDP-6002 — Documentation Search Not Returning Expected Endpoint

**Symptoms:** Searching the Documentation section for a known endpoint by name does not surface it in results.

**Cause:** The endpoint may be indexed under a different name or category than expected, or a recent documentation update temporarily affected search indexing.

**Solution:** Browse the relevant category directly from the Documentation table of contents rather than relying solely on search, or try alternate search terms.

**Prevention:** No specific preventive action is available for occasional search indexing behavior; browsing by category remains a reliable fallback.

**Related Issues:** none

---

### CDP-6003 — Code Sample Not Matching Current API Behavior

**Symptoms:** A code sample copied from the documentation produces an error or unexpected result when run as-is.

**Cause:** The documentation code sample may not have been updated to reflect a recent, minor endpoint change, or the sample uses a placeholder value that must be replaced before use.

**Solution:** Compare the sample against the endpoint's current parameter reference, replace any placeholder values, and report the discrepancy to Corvex developer support if the sample itself appears genuinely outdated.

**Prevention:** Treat code samples as a starting point requiring adaptation to your specific use case, rather than copy-paste-ready production code.

**Related Issues:** none

---

## Section 7: Integration Marketplace and Partner API

### CDP-7001 — Marketplace Integration Not Appearing After Connection

**Symptoms:** A marketplace integration was connected but does not appear as active anywhere in the account.

**Cause:** The connection process completed on the partner's side but the final authorization callback to Corvex Cloud did not complete successfully, often due to the browser session timing out mid-flow.

**Solution:** Retry the connection process from **Admin Dashboard > Integrations > Marketplace**, ensuring the full authorization flow, including any final redirect back to Corvex Cloud, completes without interruption.

**Prevention:** Complete marketplace integration setup in a single, uninterrupted session to avoid a partial authorization state.

**Related Issues:** none

---

### CDP-7002 — Marketplace Integration Using Unexpectedly High API Quota

**Symptoms:** Overall account rate limit usage increases significantly after connecting a new marketplace integration.

**Cause:** The marketplace integration operates using its own managed API credentials, which contribute to overall account usage separately from customer-created API keys, and its configured sync frequency may be more aggressive than expected.

**Solution:** Review the marketplace integration's sync frequency settings, where configurable, and reduce frequency if the default is unnecessarily aggressive for your use case.

**Prevention:** Review a new marketplace integration's expected usage pattern before connecting, particularly for accounts already operating close to their rate limit.

**Related Issues:** CDP-2001

---

### CDP-7003 — Partner API Credentials Not Working (Enterprise)

**Symptoms:** A bespoke internal integration using Corvex partner API credentials fails authentication.

**Cause:** Partner API credentials are managed separately from standard customer-facing API keys and may have been individually revoked or require a distinct renewal process.

**Solution:** Review partner API credential status under **Admin Dashboard > API Platform > Partner API**, and contact your Corvex Technical Account Manager if credentials require renewal or reissuance.

**Prevention:** Maintain awareness of partner API credential renewal timelines separately from standard API key rotation policy, since the two are managed independently.

**Related Issues:** none

---

## Section 8: Security

### CDP-8001 — IP Allowlisting Blocking Legitimate API Traffic

**Symptoms:** API requests from a legitimate, known integration begin failing after IP allowlisting is enabled or updated.

**Cause:** The integration's outbound IP address, particularly if hosted on infrastructure with dynamic or rotating IP addresses (such as some cloud auto-scaling configurations), is not included in the current allowlist.

**Solution:** Add the integration's current, stable IP range to the allowlist under **Admin Dashboard > API Platform > Security**, or, for infrastructure with genuinely dynamic IPs, consider a static IP or NAT gateway solution on your infrastructure side.

**Prevention:** Use stable, static outbound IP addresses for production integrations where IP allowlisting is enabled, to avoid unpredictable blocking.

**Related Issues:** none

---

### CDP-8002 — Suspicious API Usage Pattern Flagged by Security Monitoring

**Symptoms:** An administrator receives a security signal notification about unusual API usage from a specific key.

**Cause:** A legitimate change in integration behavior (such as a new bulk processing job) triggered an anomaly detection threshold, or the key's credentials were genuinely compromised and are being used by an unauthorized party.

**Solution:** Review the flagged usage pattern under **Monitoring > Security Signals**; if the activity is confirmed legitimate, no action is needed beyond acknowledgment. If compromise is suspected, immediately revoke the affected key and issue a new one.

**Prevention:** Notify your Corvex administrator in advance of planned changes to integration behavior that may significantly increase usage volume, to avoid unnecessary alarm.

**Related Issues:** CDP-2001

---

### CDP-8003 — API Key Exposed in a Public Code Repository

**Symptoms:** An API key value is discovered committed to a public or improperly access-controlled code repository.

**Cause:** The key was hardcoded directly into application source code rather than referenced via environment variable or secrets manager, and the repository was subsequently made public or shared beyond its intended audience.

**Solution:** Immediately revoke the exposed key under **API Keys**, generate a replacement, update all dependent systems, and review the repository's commit history to remove the exposed value from version control history as well.

**Prevention:** Never hardcode API key values directly in source code; use environment variables or a dedicated secrets management solution, and add key-pattern scanning to your repository's pre-commit or CI checks.

**Related Issues:** CDP-1004

---

### CDP-8004 — Webhook Endpoint Receiving Unverified Requests Claiming to Be From Corvex

**Symptoms:** A receiving endpoint logs requests formatted like Corvex webhook events but that fail signature verification.

**Cause:** This may indicate an attempted spoofing request from an unauthorized source, testing whether your endpoint properly validates authenticity.

**Solution:** Confirm your endpoint correctly rejects any request failing signature verification and does not process its payload; this is the intended, correct behavior protecting your system from spoofed requests.

**Prevention:** Ensure signature verification is implemented and enforced on every webhook-receiving endpoint from initial deployment, never treating it as optional.

**Related Issues:** CDP-4003

---

## Section 9: Performance

### CDP-9001 — API Response Times Slower Than Expected

**Symptoms:** API requests that typically respond quickly begin taking noticeably longer.

**Cause:** A specific query pattern (for example, a broad, unfiltered list request against a very large data set) is inherently more resource-intensive, or the account is experiencing a temporary platform-wide performance degradation.

**Solution:** Check the Corvex Cloud status page for any active performance-related incidents; if none is reported, review your specific request for opportunities to narrow scope with more specific filters or field selection.

**Prevention:** Design integrations to request only the specific data needed, using filters and field selection, rather than broad, unfiltered queries against large data sets.

**Related Issues:** CDP-9002

---

### CDP-9002 — Bulk Export via API Timing Out

**Symptoms:** A script attempting to retrieve a very large data set in a single request times out before completing.

**Cause:** The request scope exceeds practical limits for a single synchronous API call.

**Solution:** Use pagination to break the request into multiple smaller calls rather than attempting to retrieve the full data set in one request, following the pagination pattern documented for the specific endpoint.

**Prevention:** Design integrations to paginate by default for any endpoint capable of returning a large result set, rather than assuming a single request will suffice.

**Related Issues:** CDP-3003

---

### CDP-9003 — Sandbox Environment Performance Slower Than Production (Enterprise)

**Symptoms:** Requests against the sandbox environment consistently take longer than equivalent requests against production.

**Cause:** Sandbox infrastructure is provisioned for testing and validation purposes and is not scaled to match production-level performance characteristics, by design.

**Solution:** This is expected behavior; sandbox is intended for functional validation rather than performance testing. For genuine load or performance testing, discuss options with your Corvex Technical Account Manager.

**Prevention:** Set expectations with your development team that sandbox performance is not representative of production performance.

**Related Issues:** none

---

## Section 10: General Behavior and Edge Cases

### CDP-10001 — API Version Header Ignored

**Symptoms:** A request including a specific API version header appears to be processed using a different, unintended version's behavior.

**Cause:** The version header name or format does not match the exact syntax expected by the platform, causing it to be silently ignored and the default (typically latest stable) version applied instead.

**Solution:** Review the exact version header syntax in the current developer documentation, and confirm your request matches it precisely.

**Prevention:** Copy version header syntax directly from current documentation rather than from memory or an older reference.

**Related Issues:** none

---

### CDP-10002 — Deprecated Endpoint Returning a Warning Instead of Failing

**Symptoms:** A request to a deprecated endpoint succeeds but includes an unexpected warning field or header in the response.

**Cause:** The endpoint is in a deprecation grace period, still functional but flagged for eventual removal, consistent with Corvex's standard deprecation communication practice.

**Solution:** Review the deprecation notice details included in the response or referenced developer documentation, and plan a migration to the recommended replacement endpoint before the announced removal date.

**Prevention:** Monitor deprecation warnings proactively in integration logs rather than waiting for a hard failure after final removal.

**Related Issues:** none

---

### CDP-10003 — Early Access Endpoint Behaving Inconsistently (Enterprise)

**Symptoms:** An early-access API endpoint, available ahead of general availability, produces inconsistent results between calls.

**Cause:** Early-access endpoints may still be under active development and are not guaranteed to have the same stability as generally available endpoints.

**Solution:** Report the specific inconsistency to Corvex developer support through your priority support channel; avoid relying on early-access endpoints for business-critical production workflows until they reach general availability.

**Prevention:** Treat early-access endpoints as suitable for evaluation and feedback rather than production dependency, consistent with their intended purpose.

**Related Issues:** none

---

### CDP-10004 — Custom Integration Support Request Not Receiving a Timely Response

**Symptoms:** A submitted request for Corvex-assisted custom integration support has not received a response within the expected timeframe.

**Cause:** Response time targets differ by plan tier, and the request may have been submitted with insufficient detail for the assigned team to begin investigation efficiently.

**Solution:** Review the expected response time for your plan tier, and consider following up with additional technical detail (endpoint, error messages, request IDs) to help the assigned team investigate more efficiently.

**Prevention:** Include as much specific technical detail as possible when initially submitting a custom integration support request, reducing back-and-forth clarification delay.

**Related Issues:** none

---

### CDP-10005 — Response Encoding Causing Parsing Errors in Consuming Application

**Symptoms:** A consuming application throws a parsing error when processing an otherwise valid API response.

**Cause:** The consuming application is not correctly handling UTF-8 encoded content, particularly for responses containing customer-submitted text with special characters or emoji.

**Solution:** Confirm your application's JSON parsing library correctly handles UTF-8 encoded responses, which is the standard encoding used across all CloudDesk API Platform responses.

**Prevention:** Use a well-maintained, standard JSON parsing library that handles UTF-8 correctly by default, rather than a custom parsing implementation.

**Related Issues:** none

---

### CDP-10006 — Integration Behaving Differently After a Corvex Platform Update

**Symptoms:** A previously stable integration begins behaving unexpectedly following an announced Corvex platform update.

**Cause:** The update may have introduced an additive change (such as a new field) that the integration did not anticipate, even though the update was designed to be backward-compatible.

**Solution:** Review the release notes for the update in question, identify any additive changes relevant to your integration's data handling, and adjust your integration to tolerate the new structure gracefully.

**Prevention:** Design integrations to tolerate additive schema changes gracefully from the outset, and review release notes for updates relevant to endpoints your integration depends on.

**Related Issues:** CDP-10002

---

## Section 11: Additional Integration Scenarios

### CDP-11001 — SDK Client Library Version Incompatible with Current API

**Symptoms:** An officially supported client library throws unexpected errors after a Corvex platform update.

**Cause:** The client library version in use predates a recent, non-breaking API change that the library's older parsing logic does not fully anticipate.

**Solution:** Update to the current version of the official client library, available through your language's standard package manager, as referenced in the developer documentation.

**Prevention:** Subscribe to client library release notifications and periodically update dependencies rather than pinning indefinitely to an older version.

**Related Issues:** CDP-10006

---

### CDP-11002 — Concurrent Requests to the Same Resource Causing a Conflict Error

**Symptoms:** Two near-simultaneous requests updating the same ticket result in one succeeding and one failing with a conflict error.

**Cause:** The platform enforces optimistic concurrency control to prevent one update from silently overwriting another, and the failing request's expected resource version did not match the current state after the first update completed.

**Solution:** Retrieve the resource's current state and version, then retry the update with the current version reference, rather than blindly retrying the original request.

**Prevention:** Design integrations that may race with other systems or agents to handle conflict errors gracefully with a re-fetch-and-retry pattern.

**Related Issues:** none

---

### CDP-11003 — API Key Rotation Breaking a Long-Running Integration Mid-Process

**Symptoms:** A long-running batch process fails partway through immediately after a key rotation policy takes effect.

**Cause:** The mandatory key rotation policy disabled the key mid-process, since the rotation deadline was reached without the process completing beforehand.

**Solution:** Complete the batch process using a newly generated key, resuming from the point of failure using the process's own checkpointing logic, if implemented; otherwise, restart the process fully with the new key.

**Prevention:** Schedule long-running batch processes well clear of any known upcoming mandatory key rotation deadline, or design processes to checkpoint progress for safe resumption.

**Related Issues:** CDP-1001

---

### CDP-11004 — Custom Integration Failing Only for a Subset of Customer Records

**Symptoms:** An integration processes most customer records successfully but consistently fails on a specific subset.

**Cause:** The failing records likely share a common data characteristic (such as an unusually long field value, a null value in a field the integration assumes is always populated, or a special character) that the integration's parsing logic does not handle.

**Solution:** Compare the failing records against successful ones to identify the differentiating data characteristic, and update the integration's handling logic to account for that edge case.

**Prevention:** Build integrations defensively, handling null, empty, or unusually formatted field values gracefully rather than assuming uniformly well-formed data across all records.

**Related Issues:** CDP-3005

---

### CDP-11005 — Zapier-Based Automation Failing After a Field Rename

**Symptoms:** A Zapier automation built on top of the API Platform's Zapier integration stops working after a ticket field was renamed.

**Cause:** The Zap's configuration references the field by its identifier, and while renaming a field's display label is generally safe, an administrator may have deleted and recreated the field rather than renaming it, generating a new identifier.

**Solution:** Update the affected Zap's field reference to the current field identifier, and going forward, use display label edits for cosmetic changes rather than deleting and recreating fields.

**Prevention:** Communicate any planned custom field structural change to teams maintaining dependent Zapier automations before making the change.

**Related Issues:** CDP-3006

---

### CDP-11006 — Marketplace Integration and Custom API Key Both Writing to the Same Field, Causing Conflicts

**Symptoms:** A custom field's value appears to change unexpectedly, alternating between two different values.

**Cause:** Both a connected marketplace integration and a separate, custom-built integration using a customer API key are independently writing to the same field based on different source data, effectively racing each other.

**Solution:** Establish a single source of truth for the field, disabling write access from one of the two integrations, or reconciling their update logic so they do not conflict.

**Prevention:** Map out which system is the authoritative source for each synced field before connecting multiple integrations that could plausibly write to overlapping data.

**Related Issues:** CDP-11002

---

### CDP-11007 — Custom Integration Support Request Requiring NDA Coordination (Enterprise)

**Symptoms:** A custom integration support engagement is delayed pending legal or confidentiality documentation.

**Cause:** The integration scope involves sharing proprietary internal system details with Corvex's implementation team, requiring a mutual non-disclosure agreement to be finalized before detailed technical discussion can proceed.

**Solution:** Coordinate with your legal team and Corvex account team in parallel with initial technical scoping to avoid the NDA process becoming the critical path delay.

**Prevention:** Initiate any required legal documentation as early as possible when planning a custom integration engagement involving sensitive internal system details.

**Related Issues:** CDP-10004

---

### CDP-11008 — Rate Limit Errors Occurring Only During a Specific Time Window Daily

**Symptoms:** 429 errors cluster predictably around the same time each day, otherwise operating normally.

**Cause:** A scheduled batch job (such as a nightly data warehouse export trigger or an internal reporting script) runs on a fixed schedule that happens to coincide with other integration activity, temporarily pushing combined usage over the rate limit.

**Solution:** Stagger scheduled batch jobs to avoid overlapping time windows, spreading total API usage more evenly across the day.

**Prevention:** Maintain a shared internal schedule of all automated jobs consuming the API, to proactively identify and avoid overlapping high-usage windows.

**Related Issues:** CDP-2003

---

### CDP-11009 — Integration Breaking After Migrating Hosting Providers

**Symptoms:** A previously stable integration begins failing authentication or connectivity checks after the customer's own infrastructure was migrated to a new hosting provider.

**Cause:** The new hosting environment's outbound IP address differs from the previous one, and IP allowlisting configured under **Admin Dashboard > API Platform > Security** still references the old range.

**Solution:** Update the IP allowlist to include the new hosting provider's outbound IP range.

**Prevention:** Include API Platform IP allowlisting review as a standard step in any infrastructure migration checklist.

**Related Issues:** CDP-8001

---

### CDP-11010 — Sandbox-to-Production Promotion Introducing Unexpected Behavior Differences (Enterprise)

**Symptoms:** An integration validated successfully in sandbox behaves differently once pointed at production.

**Cause:** Sandbox data, being test data, may not exercise the same variety of edge cases (unusual field values, larger data volume, concurrent activity) present in genuine production data.

**Solution:** Review production-specific error details closely, and consider seeding sandbox test data with a wider variety of edge cases more representative of real production conditions for future testing cycles.

**Prevention:** Treat sandbox validation as necessary but not sufficient; plan a cautious, monitored initial production rollout rather than assuming sandbox success guarantees identical production behavior.

**Related Issues:** CDP-9003

---

### CDP-11011 — Developer Portal Session Timing Out During Long Documentation Review Sessions

**Symptoms:** A developer working through extended documentation is logged out mid-session despite active browser use.

**Cause:** The account's configured session timeout duration is shorter than the developer's uninterrupted reading time, and passive documentation browsing does not always register as sufficient activity to reset the timeout.

**Solution:** Log back in to resume; if this occurs frequently and disrupts workflow, ask an administrator to review the session timeout duration under **Admin Dashboard > Security > Sessions** for a value better suited to your team's typical usage patterns.

**Prevention:** Administrators should periodically review session timeout settings against actual team usage patterns rather than leaving default values unexamined indefinitely.

**Related Issues:** none

---

*This Troubleshooting Guide covers common CloudDesk API Platform issues and their resolutions. If an issue is not listed here or a documented solution does not resolve your problem, contact Corvex developer support through the channel appropriate to your plan tier, as described in the Corvex Cloud Pricing Guide.*
