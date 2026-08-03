# Product Overview
## CloudDesk Analytics — by Corvex Cloud

*An official product brochure from Corvex Technologies, Inc.*

---

## 1. Product Introduction

**CloudDesk Analytics** is the reporting and business intelligence module of the Corvex Cloud platform — the layer that turns every chat, ticket, and customer interaction handled across CloudDesk Chat and CloudDesk Tickets into structured, actionable insight. Rather than existing as a separate reporting tool bolted onto the support workflow, CloudDesk Analytics draws directly from the same unified case data layer used across the platform, so every dashboard reflects the full, current state of support operations — not a delayed or partial export.

CloudDesk Analytics is built for two audiences at once: the team lead who needs a real-time view of today's queue, and the CX executive who needs a defensible, exportable picture of quarter-over-quarter performance. Both are served from the same underlying data, viewed at different levels of depth.

---

## 2. Product Purpose

CloudDesk Analytics exists to answer the question every support organization eventually has to answer to its own leadership: *is this working, and how do we know?* Its purpose is to replace guesswork, anecdote, and manually assembled spreadsheets with a single, trustworthy source of truth for support performance.

Its purpose is threefold:
- Give day-to-day team leads real-time visibility into queue health, workload, and SLA status
- Give support and CX leadership reliable, historical performance data to guide staffing, process, and strategy decisions
- Give the broader business — Product, Engineering, and executive stakeholders — a structured feedback loop from customer conversations into decisions, consistent with Corvex's own internal "support informs product" philosophy

---

## 3. Target Users

CloudDesk Analytics is designed for:

- **Team leads and supervisors** monitoring live queue status, agent workload, and SLA adherence throughout the day
- **Support operations and CX leadership** analyzing trends, backlog health, CSAT/NPS performance, and team benchmarking over time
- **Executives and cross-functional stakeholders** who need summarized, exportable reporting without needing to work inside the day-to-day support tools
- **Product and engineering stakeholders** reviewing tagged and categorized ticket trends to identify recurring product issues
- **IT and security administrators** managing report access permissions and data export controls

As with the rest of Corvex Cloud, CloudDesk Analytics is most widely used by mid-market and enterprise support organizations in e-commerce, fintech, travel, and B2B SaaS.

---

## 4. Business Benefits

- **One source of truth.** Because CloudDesk Analytics draws from the same case data layer as CloudDesk Chat and CloudDesk Tickets, there is no reconciliation gap between what agents see and what leadership reports on.
- **Faster, better-informed decisions.** Real-time queue and SLA visibility lets team leads intervene before a backlog becomes a customer-facing problem, rather than discovering it after the fact.
- **Defensible reporting for the business.** Exportable, custom-range reporting gives CX leadership a credible basis for staffing requests, process changes, and board- or leadership-level updates.
- **A structured product feedback loop.** Tagged and categorized ticket trends give Product and Engineering a quantifiable view of recurring customer pain points, rather than relying on isolated anecdotes from support agents.
- **Reduced manual reporting effort.** Replacing manually assembled spreadsheets with native, always-current dashboards frees team leads and operations staff from recurring reporting overhead.

---

## 5. Core Features

- **Real-time queue dashboard** — live view of open tickets, active chats, wait times, and agent availability
- **Standard performance reporting** — ticket and chat volume, first response time, and resolution time, with a 30-day lookback
- **CSAT reporting** — aggregated customer satisfaction results across chat and ticket channels
- **Channel breakdown views** — performance segmented by channel (email, chat, social, web form)
- **Agent activity summaries** — individual agent volume and response time visibility for team leads
- **Exportable standard reports** — CSV export of standard dashboard views
- **Saved views** — team leads can save frequently used filter and dashboard configurations

---

## 6. Premium Features

Available on **Professional** and **Enterprise** plans (per the Corvex Cloud Pricing Guide):

- **Advanced reporting with custom date ranges** — historical analysis beyond the standard 30-day window, with fully custom reporting periods
- **Team-level performance analytics** — agent and team benchmarking on resolution time, CSAT, NPS, and volume, including trend-over-time views
- **NPS reporting** — Net Promoter Score aggregation and trend analysis alongside CSAT
- **Custom dashboards** — build and configure dashboards tailored to a specific team, role, or business question
- **Scheduled report delivery** — automatic recurring report delivery by email to selected stakeholders

**Enterprise-exclusive additions:**

- **Custom data warehouse export**, allowing customers to pipe raw support and analytics data into their own business intelligence environment
- **Custom SLA compliance reporting**, tied to the customer's negotiated contract terms
- **Cross-brand and cross-region reporting**, for large organizations managing multiple brands or regional support operations under one account
- **AI-assisted trend and anomaly surfacing**, drawing on expanded automation capacity as described in the Corvex Cloud Pricing Guide, to highlight notable shifts in volume, sentiment, or performance without requiring a manually built report

---

## 7. Supported Platforms

- **Web-based analytics dashboard** — accessible from any modern desktop browser (current and prior major versions of Chrome, Firefox, Safari, and Edge); no local software installation required
- **Mobile web** — responsive, view-only access to key dashboards from a mobile browser, intended for quick status checks rather than full report building
- **Scheduled email delivery** — reports delivered as email attachments or links on a configurable recurring schedule (Professional and Enterprise)
- **Data warehouse export** — structured data delivery to a customer-owned business intelligence environment (Enterprise)

---

## 8. Integrations

CloudDesk Analytics inherits the full Corvex Cloud integration layer, including:

- **Business intelligence tools** — data warehouse export designed for consumption by common BI platforms (Enterprise)
- **Collaboration tools** — scheduled report delivery and threshold-based alerts routed to team messaging tools
- **CRM platforms** — reporting that reflects CRM-sourced customer and account data where CRM integration is active (Professional and Enterprise)
- **Zapier** — connect analytics events (e.g., a report threshold being crossed) to thousands of third-party apps
- **Webhooks** — real-time delivery of reporting-related events for custom-built integrations (Professional and Enterprise)
- **Corvex integration marketplace** — pre-built connectors maintained by Corvex and technology partners

Because CloudDesk Analytics reports on data generated elsewhere in the platform, its practical integration depth is directly tied to which other Corvex Cloud integrations (CRM, e-commerce, etc.) are active on the account.

---

## 9. Security Features

- **Encryption in transit and at rest**, consistent with Corvex Cloud's platform-wide standard (TLS 1.2+ in transit, AES-256 at rest)
- **Role-based access control**, governing who can view, export, or configure reports and dashboards, independent of underlying ticket or chat edit permissions
- **Single Sign-On (SAML 2.0)** support at the Professional and Enterprise tiers
- **SCIM-based user provisioning** at the Enterprise tier for automated access management
- **Audit logging** of report exports and dashboard configuration changes, retained per the customer's plan tier
- **IP allowlisting** available for dashboard access at Professional and Enterprise tiers
- **Data residency options** for analytics data storage, available to Enterprise customers with regional compliance requirements
- **Configurable data retention**, aligned with each plan's overall case history retention policy defined in the Pricing Guide

CloudDesk Analytics reports on operational support data (tickets, chats, satisfaction scores) and does not process or store customer payment information.

---

## 10. Architecture Overview (Conceptual)

CloudDesk Analytics is built as a reporting and aggregation layer sitting on top of Corvex Cloud's shared case data layer, rather than as a separately maintained data copy. At a conceptual level:

- **Data aggregation layer** — continuously reads from the unified case data layer shared with CloudDesk Chat and CloudDesk Tickets, avoiding batch delays or separate data pipelines for standard reporting
- **Metrics and calculation layer** — applies consistent, platform-wide definitions for metrics such as first response time, resolution time, and SLA compliance, ensuring the same metric means the same thing everywhere it appears in Corvex Cloud
- **Dashboard and visualization layer** — renders real-time and historical views, including saved views and custom dashboards at higher tiers
- **Export and delivery layer** — handles CSV export, scheduled email delivery, and, for Enterprise customers, structured data warehouse export
- **Access control layer** — governs reporting visibility independently from operational (ticket/chat edit) permissions, shared with the broader Corvex Cloud role-based access model

Because CloudDesk Analytics reads from the same data layer in real time, there is no separate "sync delay" between an agent resolving a ticket and that resolution appearing in a dashboard. This overview is intentionally conceptual; detailed technical architecture is documented separately for internal and technical partner audiences.

---

## 11. User Roles

- **Agent** — has access to their own individual performance summary only; no team- or account-level reporting access by default
- **Team Lead / Supervisor** — full access to team-level dashboards, real-time queue views, and standard reporting for their team
- **Administrator** — configures report access permissions, custom dashboards, scheduled delivery, and data export settings; manages analytics-specific roles within CloudDesk Analytics
- **Read-only / Reporting user** — available at Professional and Enterprise tiers, allowing stakeholders (e.g., an executive or product manager) to view dashboards and reports without any ticket, chat, or configuration access

Role definitions and permission granularity align with the broader Corvex Cloud role-based access model described in the platform's Security Features.

---

## 12. Limitations

- CloudDesk Analytics reports on data generated within Corvex Cloud; it does not ingest or report on support data originating from third-party systems outside the platform unless that data has been integrated into Corvex Cloud first
- Custom date ranges and historical trend analysis beyond 30 days are not available on the Starter plan
- Custom dashboards and scheduled report delivery are not available on Starter
- Data warehouse export and cross-brand/cross-region reporting are Enterprise-exclusive capabilities
- AI-assisted trend and anomaly surfacing is Enterprise-exclusive and is not available on Starter or Professional
- Mobile access is intended for status checks and standard dashboard viewing; full report building and configuration require the desktop web experience

---

## 13. Subscription Availability

CloudDesk Analytics is included as the core reporting layer across all three Corvex Cloud subscription plans, with feature availability scaling by tier as described throughout this document:

| Capability | Starter | Professional | Enterprise |
|---|---|---|---|
| Real-time queue dashboard | Included | Included | Included |
| Standard reporting (30-day) | Included | Included | Included |
| CSAT reporting | Included | Included | Included |
| NPS reporting | — | Included | Included |
| Custom date ranges & historical trends | — | Included | Included |
| Custom dashboards & scheduled delivery | — | Included | Included |
| Team performance analytics | — | Included | Included |
| Data warehouse export | — | — | Included |
| Cross-brand / cross-region reporting | — | — | Included |
| AI-assisted trend & anomaly surfacing | — | — | Included |

Full plan pricing, seat minimums, and billing terms are defined in the official Corvex Cloud Pricing Guide.

---

## 14. Common Use Cases

- **Daily queue management** — team leads using the real-time dashboard to rebalance workload and catch SLA risk before it affects customers
- **Quarterly business reviews** — CX leadership exporting custom-range performance data to report on team performance to executive stakeholders
- **Seasonal staffing planning** — e-commerce and travel customers analyzing historical volume trends to plan staffing around known seasonal spikes
- **Product feedback prioritization** — Product and Engineering teams reviewing tagged ticket trend data surfaced through CloudDesk Analytics to prioritize fixes and improvements
- **Regulated reporting requirements** — fintech and healthcare technology customers using audit logs and custom SLA compliance reporting to support internal governance and compliance review

---

## 15. Future Roadmap

Consistent with the broader Corvex Cloud long-term roadmap, planned directions for CloudDesk Analytics include:

- **Near term:** Expanded custom dashboard configuration options, deeper channel-level breakdowns, and continued performance improvements to real-time dashboard rendering at high data volumes
- **Mid term:** Broader AI-assisted trend and anomaly surfacing extending beyond Enterprise-only availability over time, always with an emphasis on transparency around how a surfaced trend or anomaly was identified
- **Long term:** Continued development of CloudDesk Analytics as the unified measurement layer across all current and future Corvex Cloud channels, in line with Corvex's broader vision of giving support organizations one trustworthy picture of performance rather than a fragmented, tool-by-tool view

Specific feature names, timelines, and release commitments are subject to change and are governed by the Corvex Product organization; this roadmap section is directional rather than a binding delivery commitment.

---

*This Product Overview describes CloudDesk Analytics as offered under the Corvex Cloud platform by Corvex Technologies, Inc. For pricing details, refer to the official Corvex Cloud Pricing Guide. For company background, refer to the official Corvex Technologies Company Overview.*
