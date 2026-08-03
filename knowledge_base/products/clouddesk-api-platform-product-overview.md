# Product Overview
## CloudDesk API Platform — by Corvex Cloud

*An official product brochure from Corvex Technologies, Inc.*

---

## 1. Product Introduction

**CloudDesk API Platform** is the developer and extensibility layer of the Corvex Cloud platform — the set of APIs, webhooks, and developer tooling that allows customers and technology partners to build on top of the same case data layer used by CloudDesk Chat, CloudDesk Tickets, and CloudDesk Analytics. Rather than treating extensibility as an afterthought, the API Platform exposes the same underlying data model that powers the core product, so anything an agent can see or do inside Corvex Cloud can, within defined limits, be read, triggered, or extended programmatically.

The API Platform is not a standalone product a customer purchases in isolation; it is the connective layer available across every Corvex Cloud plan, at a depth and scale appropriate to that plan, that makes the rest of the CloudDesk suite embeddable, automatable, and integrable with a customer's broader technology environment.

---

## 2. Product Purpose

CloudDesk API Platform exists because no support platform, however complete, fits every customer's technology environment out of the box. Its purpose is to make Corvex Cloud a flexible foundation rather than a closed system — allowing customers and partners to connect it to internal tools, automate repetitive work, and build custom experiences on top of reliable, well-documented interfaces.

Its purpose is threefold:
- Give technical teams reliable, well-documented programmatic access to case, customer, and reporting data
- Enable real-time, event-driven integration with a customer's broader technology stack through webhooks
- Support the Corvex partner and integration ecosystem, allowing third-party and custom-built tools to extend the CloudDesk suite

---

## 3. Target Users

CloudDesk API Platform is designed for:

- **In-house developers and IT teams** building custom integrations between Corvex Cloud and internal systems
- **Systems integrators and implementation partners** delivering tailored Corvex Cloud deployments for enterprise customers
- **Corvex technology partners** building native integrations listed in the Corvex integration marketplace
- **Data and analytics teams** consuming case and reporting data for use in external business intelligence environments
- **IT and security administrators** managing API credentials, access scopes, and monitoring API usage

The API Platform is most heavily used by technically resourced organizations — larger e-commerce, fintech, and B2B SaaS customers in particular — though basic, read-only usage is available even to smaller teams on the Starter plan.

---

## 4. Business Benefits

- **Fits existing technology investments.** Rather than requiring a customer to work exclusively inside Corvex Cloud, the API Platform allows support data and workflows to connect with whatever systems the business already relies on.
- **Reduces manual, repetitive work.** Webhook-driven automation removes the need for staff to manually move data between Corvex Cloud and other systems.
- **Enables custom, differentiated experiences.** Customers with in-house development capacity can build support experiences tailored precisely to their product or brand, using Corvex Cloud as the underlying engine.
- **Supports a growing partner ecosystem.** The same APIs that power custom customer integrations also power the Corvex integration marketplace, giving customers a growing set of pre-built options over time.
- **Protects data portability.** Full API access to case and reporting data, particularly at higher tiers, ensures customers are never locked into viewing their own data only through the standard Corvex Cloud interface.

---

## 5. Core Features

- **REST API access** to core case, customer, and reporting data, consistent with the access level defined by the customer's plan
- **API authentication and credential management** via account-level API keys, managed by administrators
- **Standard rate limiting**, scaled by plan tier, to ensure platform stability for all customers
- **Developer documentation portal** with endpoint references, authentication guides, and example requests
- **Sandbox testing support** for validating integrations before deploying against live data (availability by tier, see Section 13)
- **Zapier connectivity**, providing lower-code automation options for customers without dedicated developer resources
- **Standard event types** covering core lifecycle actions (e.g., ticket created, ticket resolved, chat conversation closed)

---

## 6. Premium Features

Available on **Professional** and **Enterprise** plans (per the Corvex Cloud Pricing Guide):

- **Full read/write API access**, beyond the read-only access available on Starter
- **Webhook support**, delivering real-time event notifications to a customer-specified endpoint
- **Higher standard rate limits**, supporting higher-volume automated usage
- **Access to the Corvex integration marketplace**, including both Corvex-built and partner-built native integrations
- **Custom integration support from Corvex**, assisting technically resourced customers with complex or non-standard integration requirements

**Enterprise-exclusive additions:**

- **Elevated default rate limits**, with custom limits available on request for high-volume accounts
- **Priority API support**, including access to a dedicated technical contact for integration-related issues
- **Early access to new API endpoints and capabilities** ahead of general availability
- **Dedicated webhook infrastructure**, supporting higher-throughput, higher-reliability event delivery for large-scale integrations
- **Access to the Corvex partner API**, supporting bespoke internal system connections beyond standard integration patterns

---

## 7. Supported Platforms

- **REST API**, accessible over HTTPS from any standard HTTP client or programming language capable of making authenticated web requests
- **Webhooks**, delivered as HTTPS POST requests to a customer-configured endpoint (Professional and Enterprise)
- **Developer documentation portal**, accessible from any modern desktop or mobile browser
- **Sandbox environment**, browser- and API-accessible, provided for Enterprise customers per the Corvex Cloud Pricing Guide

The API Platform does not require any client-side software installation; integration work is performed against Corvex-hosted endpoints using the customer's own development environment and tooling.

---

## 8. Integrations

Because the API Platform is the mechanism through which most other Corvex Cloud integrations are built, its own "integrations" are best understood as the ecosystem it enables:

- **CRM platforms** — native CRM integrations are themselves built on the same APIs available to customers directly
- **E-commerce platforms** — order and account data integrations rely on the same API and webhook infrastructure
- **Collaboration tools** — real-time alerting integrations (e.g., SLA breach notifications) are typically implemented via webhook
- **Business intelligence tools** — Enterprise data warehouse export is a specialized, higher-throughput extension of the same underlying API data model
- **Zapier** — a lower-code entry point to the same event and action model exposed by the full API
- **Corvex integration marketplace** — the collection of native integrations, both Corvex-built and partner-built, that exist because of this platform

---

## 9. Security Features

- **API key-based authentication**, with keys scoped to specific access levels and rotatable by administrators at any time
- **Role-based access control**, ensuring API access reflects the same permission model applied elsewhere in Corvex Cloud
- **Encryption in transit**, consistent with Corvex Cloud's platform-wide standard (TLS 1.2+); all API and webhook traffic is HTTPS-only
- **Rate limiting and abuse protection**, scaled by plan tier, to protect platform stability and prevent unauthorized bulk data extraction
- **Audit logging** of API key creation, rotation, and usage patterns, retained per the customer's plan tier
- **IP allowlisting** available for API access at Professional and Enterprise tiers
- **Webhook endpoint verification**, ensuring event payloads can be cryptographically verified as originating from Corvex Cloud
- **SCIM-based provisioning support** at the Enterprise tier for programmatic user and access management, distinct from case-data API access

The API Platform does not expose payment data through any endpoint; access to case, customer, and reporting data is governed by the same data-handling and retention policies applied elsewhere in Corvex Cloud.

---

## 10. Architecture Overview (Conceptual)

CloudDesk API Platform is built as a governed access layer sitting directly on top of Corvex Cloud's shared case data layer, rather than as a separate system requiring its own data synchronization. At a conceptual level:

- **Gateway layer** — authenticates and authorizes every API request, enforces rate limits, and routes requests to the appropriate internal service
- **Data access layer** — exposes the same unified case, customer, and reporting data model used by CloudDesk Chat, Tickets, and Analytics, ensuring API responses are always consistent with what an agent sees in the product
- **Event and webhook layer** — captures lifecycle events across the platform (ticket status changes, new chats, resolved cases) and delivers them to configured webhook endpoints in near real time
- **Developer tooling layer** — powers the documentation portal, API key management interface, and (for Enterprise customers) the sandbox testing environment
- **Governance layer** — applies role-based access control, audit logging, and plan-based feature gating consistently across all API and webhook activity

Because the API Platform reads from and writes to the same data layer used by the rest of Corvex Cloud, there is no separate "API copy" of a customer's data to keep in sync — an update made via the API is immediately reflected in the agent workspace, and vice versa. This overview is intentionally conceptual; detailed technical architecture, including specific endpoint schemas, is documented separately in the Corvex Cloud developer documentation.

---

## 11. User Roles

- **Developer / Integration user** — a scoped access type for individuals or systems consuming the API and webhooks; access level (read-only or read/write) is governed by the account's plan and the specific API key's configured scope
- **Administrator** — creates and manages API keys, configures webhook endpoints, and sets IP allowlisting and rate limit preferences within account-level constraints
- **Security / Compliance reviewer** — available at Professional and Enterprise tiers, with access to API audit logs without broader administrative or case-data access
- **Corvex Technical Account Manager (Enterprise)** — a Corvex-side role, not a customer role, providing dedicated technical support for complex Enterprise integrations

Role definitions and permission granularity align with the broader Corvex Cloud role-based access model described in the platform's Security Features.

---

## 12. Limitations

- API access on the Starter plan is read-only; customers requiring write access or webhook support must be on Professional or Enterprise
- Rate limits scale by plan tier (60 requests/minute on Starter, 300 requests/minute on Professional, elevated and custom limits on Enterprise); high-volume automated use cases should be scoped to an appropriate plan
- A sandbox testing environment is available only to Enterprise customers; Starter and Professional integration development and testing must be conducted carefully against live data or within a customer-provisioned test account
- The API Platform exposes data and actions available within Corvex Cloud; it does not provide a mechanism to extend the platform's underlying data model with entirely new object types beyond supported custom field configurations
- Custom integration development support from Corvex is available at Professional and Enterprise tiers but is scoped to reasonable implementation assistance, not full bespoke software development on the customer's behalf

---

## 13. Subscription Availability

CloudDesk API Platform access scales by plan tier as follows:

| Capability | Starter | Professional | Enterprise |
|---|---|---|---|
| REST API access | Read-only | Read/write | Read/write |
| Rate limit | 60 req/min | 300 req/min | Elevated / custom |
| Webhook support | — | Included | Included, dedicated infrastructure |
| Integration marketplace access | — | Included | Included |
| Custom integration support from Corvex | — | Included | Included, priority |
| Sandbox environment | — | — | Included |
| Early access to new endpoints | — | — | Included |
| Corvex partner API access | — | — | Included |

Full plan pricing, seat minimums, and billing terms are defined in the official Corvex Cloud Pricing Guide.

---

## 14. Common Use Cases

- **Custom internal tooling** — building internal dashboards or workflows that pull live case data from Corvex Cloud into a company's own systems
- **E-commerce order sync automation** — using webhooks to trigger internal fulfillment or refund workflows automatically when a related ticket changes status
- **Fintech compliance workflows** — programmatically extracting audit-relevant case data into a customer's own compliance recordkeeping systems
- **Custom in-product support experiences** — B2B SaaS customers building bespoke support interfaces embedded in their own product, backed by Corvex Cloud as the underlying engine
- **Business intelligence consolidation** — Enterprise customers using data warehouse export to combine support data with broader business metrics in a single analytics environment

---

## 15. Future Roadmap

Consistent with the broader Corvex Cloud long-term roadmap, planned directions for CloudDesk API Platform include:

- **Near term:** Expanded event coverage for webhooks, improved developer documentation and code samples, and continued rate limit and reliability improvements for high-volume accounts
- **Mid term:** Broader sandbox environment availability beyond Enterprise-only access, and expanded partner API capabilities to support a growing integration marketplace
- **Long term:** Continued evolution of the API Platform as the foundation not only for third-party integrations but for Corvex's own AI-assisted and automation capabilities across the CloudDesk suite, consistent with Corvex's broader commitment to building automation that remains transparent and auditable

Specific feature names, timelines, and release commitments are subject to change and are governed by the Corvex Product organization; this roadmap section is directional rather than a binding delivery commitment.

---

*This Product Overview describes CloudDesk API Platform as offered under the Corvex Cloud platform by Corvex Technologies, Inc. For pricing details, refer to the official Corvex Cloud Pricing Guide. For company background, refer to the official Corvex Technologies Company Overview.*
