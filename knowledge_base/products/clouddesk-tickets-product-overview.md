# Product Overview
## CloudDesk Tickets — by Corvex Cloud

*An official product brochure from Corvex Technologies, Inc.*

---

## 1. Product Introduction

**CloudDesk Tickets** is the case and ticket management module of the Corvex Cloud platform — the system of record for every customer support conversation, regardless of where it originated. Email, live chat, social messaging, and web form submissions all resolve into a single, structured ticket within CloudDesk Tickets, giving support teams one consistent workflow for tracking, prioritizing, and resolving customer issues from first contact to close.

Where CloudDesk Chat is built for the immediacy of live conversation, CloudDesk Tickets is built for structured, trackable resolution — the backbone that ensures nothing is dropped, every case has an owner, and every resolution is measurable. The two modules share the same underlying case data, so a conversation that begins in chat and needs follow-up becomes a ticket without any manual re-entry.

---

## 2. Product Purpose

CloudDesk Tickets exists to answer a question every growing support team eventually asks: *where did that issue go, and who owns it?* Its purpose is to remove ambiguity from support operations by giving every customer issue a defined status, a defined owner, and a visible history — from the moment it's raised to the moment it's resolved and beyond.

Its purpose is threefold:
- Ensure no customer issue is lost, forgotten, or left without a clear owner
- Give agents the context and tools to resolve issues efficiently, without duplicate work
- Give support leaders accurate, trustworthy data on volume, performance, and recurring issues

---

## 3. Target Users

CloudDesk Tickets is designed for:

- **Support agents** managing a queue of assigned or unassigned tickets across channels
- **Team leads and supervisors** overseeing ticket assignment, workload balance, and SLA adherence
- **Support operations and CX leadership** analyzing ticket trends, backlog health, and team performance
- **Product and engineering stakeholders** who rely on tagged, categorized ticket data to identify recurring product issues
- **IT and security administrators** configuring access controls, data retention, and ticket routing policies

As with the rest of Corvex Cloud, CloudDesk Tickets is most widely adopted by mid-market and enterprise support organizations in e-commerce, fintech, travel, and B2B SaaS.

---

## 4. Business Benefits

- **Nothing falls through the cracks.** Every inbound issue, regardless of channel, becomes a tracked ticket with a defined status — eliminating the "lost email" problem common in unstructured inboxes.
- **Clear accountability.** Explicit ownership and assignment rules mean every ticket has a responsible agent or team at every stage.
- **Faster resolution through context.** Full customer and conversation history is attached to every ticket, reducing time agents spend gathering background before they can help.
- **Data-driven staffing and process decisions.** Accurate backlog, volume, and SLA reporting gives support leaders the information needed to staff appropriately and identify process bottlenecks.
- **Product feedback loop.** Tagged and categorized ticket data gives Product and Engineering teams a structured, quantifiable view of recurring customer pain points, consistent with Corvex's own internal "support informs product" philosophy.

---

## 5. Core Features

- **Unified ticket queue** — every channel (email, chat handoff, social, web form) consolidates into a single, filterable ticket queue
- **Status and priority workflows** — configurable ticket statuses (e.g., New, Open, Pending, Resolved, Closed) and priority levels
- **Assignment and ownership** — manual and rule-based ticket assignment to individual agents or teams
- **Tagging and categorization** — customizable tags and categories for reporting and trend analysis
- **Canned responses and macros** — reusable response templates and multi-step macros (e.g., "apply tag, set status, send reply")
- **Merge and split tickets** — combine duplicate tickets or split a multi-issue ticket into separate trackable items
- **Full conversation and customer history** — every prior interaction with a customer, across all channels, visible within the ticket view
- **Standard reporting dashboard** — ticket volume, resolution time, and backlog reporting included at every plan tier
- **Internal notes and @mentions** — private, customer-invisible collaboration within a ticket

---

## 6. Premium Features

Available on **Professional** and **Enterprise** plans (per the Corvex Cloud Pricing Guide):

- **Advanced automation and triggers** — automatically assign, tag, escalate, or route tickets based on configurable business rules
- **Custom ticket fields and forms** — capture structured, business-specific data on every ticket
- **SLA management and alerts** — define response and resolution time targets by priority or category, with automated breach alerts
- **Advanced reporting with custom date ranges** — exportable dashboards and deeper historical analysis
- **Team-level performance analytics** — agent and team benchmarking on resolution time, CSAT, and volume
- **Bulk actions and advanced macros** — apply multi-step actions across large sets of tickets simultaneously

**Enterprise-exclusive additions:**

- **AI-assisted ticket triage and suggested responses**, drawing on expanded automation capacity as described in the Corvex Cloud Pricing Guide
- **Custom SLA-backed resolution guarantees**, tied to the customer's negotiated contract terms
- **Dedicated infrastructure options** for customers with strict performance isolation requirements
- **Custom data warehouse export** for tickets and related reporting data

---

## 7. Supported Platforms

- **Web-based agent workspace** — accessible from any modern desktop browser (current and prior major versions of Chrome, Firefox, Safari, and Edge); no local software installation required
- **Mobile web** — responsive ticket management for agents accessing the workspace from a mobile browser
- **Email-to-ticket** — inbound email is automatically converted into tickets via standard email routing configuration
- **Web form submission** — embeddable contact forms that generate tickets directly
- **Desktop and browser notifications** — real-time alerts for new assignments, mentions, and SLA warnings

---

## 8. Integrations

CloudDesk Tickets inherits the full Corvex Cloud integration layer, including:

- **CRM platforms** — two-way sync of customer and ticket data with major CRM systems (Professional and Enterprise)
- **E-commerce platforms** — order, shipment, and account data surfaced directly within relevant tickets
- **Collaboration tools** — ticket escalations, SLA breach alerts, and mentions routed to team messaging tools
- **Project and engineering tools** — ticket-to-issue linking with common project management and engineering tracking systems, for surfacing product-related tickets to the teams who can act on them
- **Zapier** — connect ticket events (created, updated, resolved) to thousands of third-party apps
- **Webhooks** — real-time event delivery for custom-built integrations (Professional and Enterprise)
- **Corvex integration marketplace** — pre-built connectors maintained by Corvex and technology partners

Starter plan accounts have access to a limited set of Zapier-based connections; broader native integrations, including CRM and project tool sync, require Professional or Enterprise.

---

## 9. Security Features

- **Encryption in transit and at rest**, consistent with Corvex Cloud's platform-wide standard (TLS 1.2+ in transit, AES-256 at rest)
- **Role-based access control**, governing which agents and administrators can view, edit, reassign, or export tickets
- **Single Sign-On (SAML 2.0)** support at the Professional and Enterprise tiers
- **SCIM-based user provisioning** at the Enterprise tier for automated access management
- **Audit logging** of key ticket actions (status changes, reassignments, field edits, deletions), retained per the customer's plan tier
- **IP allowlisting** available for agent workspace access at Professional and Enterprise tiers
- **Data residency options** for ticket storage, available to Enterprise customers with regional compliance requirements
- **Configurable data retention** for ticket history, aligned with each plan's overall case history retention policy defined in the Pricing Guide

CloudDesk Tickets does not store customer payment information as part of the ticket record; any payment-related references (such as an order number) are handled according to the customer organization's own data-handling configuration.

---

## 10. Architecture Overview (Conceptual)

CloudDesk Tickets is built as the central case data layer of Corvex Cloud, with other channels — including CloudDesk Chat — writing into the same underlying structure rather than maintaining separate records. At a conceptual level:

- **Intake layer** — normalizes inbound issues from email, chat handoff, web forms, and social channels into a common ticket structure
- **Case data layer** — the unified data model shared across Corvex Cloud modules, storing ticket status, history, tags, and associated customer records
- **Workflow and automation layer** — evaluates tickets against configured rules (assignment, SLA, escalation, tagging) and triggers corresponding actions, shared with the automation logic used elsewhere in the platform
- **Collaboration layer** — supports internal notes, mentions, and multi-agent visibility on a single ticket without exposing internal activity to the customer
- **Reporting layer** — aggregates ticket-specific and cross-channel metrics into the same analytics environment used by the rest of Corvex Cloud

Because CloudDesk Tickets and CloudDesk Chat share this same case data layer, a live chat that escalates into a longer-running issue continues as the same case record — with full history intact — rather than starting over as a disconnected ticket. This overview is intentionally conceptual; detailed technical architecture is documented separately for internal and technical partner audiences.

---

## 11. User Roles

- **Agent** — works assigned tickets, applies tags and macros, adds internal notes, and communicates with customers; no administrative configuration access
- **Team Lead / Supervisor** — includes all Agent capabilities, plus visibility into team queues, the ability to reassign tickets, monitor SLA status, and access team-level reporting
- **Administrator** — configures ticket fields, statuses, automation rules, SLAs, and integrations; manages user roles and permissions within CloudDesk Tickets
- **Read-only / Reporting user** — available at Professional and Enterprise tiers, allowing stakeholders (e.g., a product manager reviewing tagged issues) to view ticket data and reporting without edit access

Role definitions and permission granularity align with the broader Corvex Cloud role-based access model described in the platform's Security Features.

---

## 12. Limitations

- CloudDesk Tickets is designed around structured, trackable case resolution and is not intended as a real-time messaging tool; live, in-the-moment conversation is handled by CloudDesk Chat and flows into CloudDesk Tickets when longer-term tracking is needed
- Custom ticket fields and advanced SLA management are not available on the Starter plan
- Bulk actions are limited in scope on Starter and Professional relative to Enterprise, where higher-volume bulk operations are supported
- AI-assisted triage and suggested responses are Enterprise-exclusive and are not available on Starter or Professional
- Ticket-to-engineering-tool linking depends on the availability of a supported native integration or Zapier connection for the customer's specific project management system

---

## 13. Subscription Availability

CloudDesk Tickets is included as the core case management engine across all three Corvex Cloud subscription plans, with feature availability scaling by tier as described throughout this document:

| Capability | Starter | Professional | Enterprise |
|---|---|---|---|
| Unified ticket queue & workflows | Included | Included | Included |
| Canned responses, tagging, merge/split | Included | Included | Included |
| Advanced automation & triggers | — | Included | Included |
| Custom ticket fields & forms | — | Included | Included |
| SLA management & alerts | — | Included | Included, with custom SLA-backed guarantees |
| Advanced reporting & analytics | Basic (30-day) | Advanced (custom range) | Advanced + data warehouse export |
| Bulk actions | Limited | Standard | High-volume |
| AI-assisted triage & suggestions | — | — | Included |

Full plan pricing, seat minimums, and billing terms are defined in the official Corvex Cloud Pricing Guide.

---

## 14. Common Use Cases

- **E-commerce order and returns management** — tracking multi-step issues like returns, refunds, or shipping disputes from first contact through resolution
- **Fintech account and compliance-sensitive cases** — maintaining a fully auditable record of account-related support issues, with role-based access suited to regulated environments
- **Travel and hospitality booking issues** — tracking cases that span multiple touchpoints (booking, travel dates, post-trip follow-up) with a persistent record
- **B2B SaaS technical support** — capturing structured, tagged tickets that feed directly into engineering and product prioritization
- **Healthcare technology support operations** — maintaining structured, auditable case histories consistent with the governance needs of regulated customers

---

## 15. Future Roadmap

Consistent with the broader Corvex Cloud long-term roadmap, planned directions for CloudDesk Tickets include:

- **Near term:** Expanded automation rule conditions, deeper integration with e-commerce and CRM data directly within the ticket view, and continued improvements to bulk operations for high-volume teams
- **Mid term:** Broader AI-assisted triage and categorization capabilities extending beyond Enterprise-only availability over time, always with an emphasis on transparency and agent oversight of any automated or suggested action
- **Long term:** Continued convergence of ticket-based and real-time channels under a single conversational and case framework, in line with Corvex's broader vision of removing the artificial distinction between self-service and human-assisted support

Specific feature names, timelines, and release commitments are subject to change and are governed by the Corvex Product organization; this roadmap section is directional rather than a binding delivery commitment.

---

*This Product Overview describes CloudDesk Tickets as offered under the Corvex Cloud platform by Corvex Technologies, Inc. For pricing details, refer to the official Corvex Cloud Pricing Guide. For company background, refer to the official Corvex Technologies Company Overview.*
