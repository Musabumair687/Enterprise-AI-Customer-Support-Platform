# Product Overview
## CloudDesk Chat — by Corvex Cloud

*An official product brochure from Corvex Technologies, Inc.*

---

## 1. Product Introduction

**CloudDesk Chat** is the real-time messaging and live chat module of the Corvex Cloud platform, built to give support teams a single, intelligent workspace for handling live conversations across a website, mobile app, and messaging channels. Where a shared inbox handles asynchronous email and case work, CloudDesk Chat is purpose-built for the immediacy of live conversation — customers typing in the moment, agents responding in real time, and both sides needing context to travel with them the whole way through.

CloudDesk Chat sits natively within Corvex Cloud, sharing the same case history, customer profiles, and reporting layer as the rest of the platform, so a conversation that starts in chat and later continues by email never loses its thread.

---

## 2. Product Purpose

CloudDesk Chat exists to solve a specific problem support teams consistently report: live chat tools, when bolted on as separate systems, create fragmented customer records, duplicate work, and blind spots in reporting. CloudDesk Chat was built to be the opposite — a live chat experience that is fast and modern for the customer, and fully unified with the rest of a team's support operation for the agent and the business.

Its purpose is threefold:
- Give customers an immediate, low-friction way to reach a real person or get an instant answer
- Give agents a single, distraction-light interface for managing multiple live conversations without losing context
- Give support leaders visibility into chat performance alongside every other channel, rather than in a separate silo

---

## 3. Target Users

CloudDesk Chat is designed for:

- **Support agents** handling real-time customer conversations, often across multiple simultaneous chats
- **Team leads and supervisors** monitoring live queue volume, wait times, and conversation quality
- **Support operations and CX leadership** who need chat performance data alongside broader support metrics
- **Sales-adjacent support teams** (e.g., pre-sales chat, order support) who use live chat as a conversion and retention tool, not only a troubleshooting channel
- **IT and security administrators** configuring chat access, routing rules, and data handling policies

CloudDesk Chat is most commonly adopted by organizations already using or evaluating the broader Corvex Cloud platform, particularly in e-commerce, fintech, travel, and B2B SaaS — consistent with Corvex's core target customer base.

---

## 4. Business Benefits

- **Faster resolution for time-sensitive issues.** Live chat consistently resolves straightforward issues faster than email, reducing average handle time for qualifying case types.
- **Reduced context-switching costs.** Because CloudDesk Chat shares data with the rest of Corvex Cloud, agents don't need a second tool, a second login, or a manual copy-paste of context between systems.
- **Improved conversion and retention for commerce use cases.** Pre-purchase chat support has a measurable impact on cart abandonment and purchase confidence for e-commerce and travel customers.
- **Better staffing decisions.** Unified reporting across chat and other channels gives support leaders a true picture of team workload, rather than an incomplete view based on ticket volume alone.
- **Lower total cost of ownership.** Replacing a standalone live chat vendor with a native Corvex Cloud module removes a separate contract, a separate integration burden, and a separate data reconciliation problem.

---

## 5. Core Features

- **Real-time messaging widget** — a customizable chat widget embeddable on websites and web apps
- **Unified agent workspace** — chat conversations appear in the same interface as email and other channels, with shared customer history
- **Smart routing** — incoming chats are routed based on agent availability, skill tags, and configurable rules
- **Canned responses and shortcuts** — reusable response snippets available directly within the chat composer
- **Typing indicators and read receipts** — standard real-time conversational cues for both customer and agent
- **Conversation transfer and internal notes** — agents can transfer a chat to another agent or team, with private internal notes not visible to the customer
- **Pre-chat forms** — configurable forms to capture context (e.g., order number, issue type) before a conversation begins
- **Offline and away messaging** — automatic messaging when no agents are available, with fallback to email or a help center article
- **Basic chat analytics** — response time, resolution time, and volume reporting included at every plan tier

---

## 6. Premium Features

Available on **Professional** and **Enterprise** plans (per the Corvex Cloud Pricing Guide):

- **Advanced routing and automation rules** — route by customer value, conversation sentiment signals, or custom business logic
- **Proactive chat triggers** — automatically initiate a chat invitation based on visitor behavior (e.g., time on page, cart value)
- **Multi-language chat widget** — customer-facing widget available in multiple languages simultaneously (Professional: up to 5 languages; Enterprise: unlimited)
- **Custom widget branding** — full visual customization of the chat widget beyond standard color/logo options
- **Chat-based CSAT and NPS surveys** — post-conversation satisfaction and sentiment surveys
- **Team performance analytics** — agent- and team-level performance dashboards beyond baseline reporting

**Enterprise-exclusive additions:**

- **AI-assisted response suggestions** drawing on expanded automation capacity, as described in the Corvex Cloud Pricing Guide
- **Custom SLA-backed response time guarantees** for live chat specifically
- **Dedicated infrastructure options** for customers with strict performance isolation requirements
- **Multi-brand widget support** for organizations managing multiple customer-facing brands from a single account

---

## 7. Supported Platforms

- **Web:** Embeddable JavaScript widget compatible with all modern browsers (current and prior major versions of Chrome, Firefox, Safari, and Edge)
- **Mobile web:** Responsive widget behavior for mobile browsers
- **Native mobile SDKs:** Available for iOS and Android, allowing CloudDesk Chat to be embedded directly within a customer's mobile application
- **Agent workspace:** Web-based agent application, accessible from any modern desktop browser; no local software installation required
- **Desktop notifications:** Browser-based push notifications for agents when the agent workspace is open in a background tab

---

## 8. Integrations

CloudDesk Chat inherits the full Corvex Cloud integration layer, including:

- **CRM platforms** — customer and conversation data sync with major CRM systems (Professional and Enterprise)
- **E-commerce platforms** — order and cart data displayed alongside live conversations for commerce customers
- **Collaboration tools** — chat escalations and internal notifications routed to team messaging tools
- **Zapier** — connect CloudDesk Chat events (new conversation, conversation closed, CSAT received) to thousands of third-party apps
- **Webhooks** — real-time event delivery for custom-built integrations (Professional and Enterprise)
- **Corvex integration marketplace** — pre-built connectors maintained by Corvex and technology partners

Starter plan accounts have access to a limited set of Zapier-based connections and one native web chat widget integration; broader native integrations require Professional or Enterprise, consistent with platform-wide integration availability.

---

## 9. Security Features

- **Encryption in transit and at rest**, consistent with Corvex Cloud's platform-wide standard (TLS 1.2+ in transit, AES-256 at rest)
- **Role-based access control**, governing which agents and administrators can view, transfer, or export chat conversations
- **Single Sign-On (SAML 2.0)** support at the Professional and Enterprise tiers
- **SCIM-based user provisioning** at the Enterprise tier for automated access management
- **Audit logging** of key chat administration actions (widget configuration changes, routing rule edits), retained per the customer's plan tier
- **IP allowlisting** available for agent workspace access at Professional and Enterprise tiers
- **Data residency options** for chat transcript storage, available to Enterprise customers with regional compliance requirements
- **Configurable data retention** for chat transcripts, aligned with each plan's overall case history retention policy

CloudDesk Chat does not store customer payment information; any payment-related data referenced during a chat (e.g., order numbers) is handled according to the customer organization's own data-handling configuration and is never processed as payment data by Corvex.

---

## 10. Architecture Overview (Conceptual)

CloudDesk Chat is built as a natively integrated module within the broader Corvex Cloud platform, rather than a bolted-on or acquired separate system. At a conceptual level:

- **Widget layer** — the customer-facing chat interface, embedded via a lightweight script on the customer's website or mobile app, responsible for establishing and maintaining a real-time connection
- **Messaging layer** — handles real-time message delivery between customer and agent, including presence signals (typing, online/offline status) and delivery confirmation
- **Unified case layer** — every chat conversation is represented as a case within the same underlying data model used across email, social, and other channels, allowing shared history and reporting
- **Routing and automation layer** — evaluates incoming conversations against configured rules (skills, availability, priority) to determine agent assignment, shared with the routing logic used elsewhere in Corvex Cloud
- **Reporting layer** — aggregates chat-specific and cross-channel metrics into the same analytics environment used by the rest of the platform

This shared-layer approach is the architectural basis for CloudDesk Chat's core value proposition: conversations move fluidly between channels without requiring data migration or duplicate record-keeping. This overview is intentionally conceptual; detailed technical architecture is documented separately for internal and technical partner audiences.

---

## 11. User Roles

- **Agent** — handles live conversations, uses canned responses, transfers chats, and adds internal notes; no administrative configuration access
- **Team Lead / Supervisor** — includes all Agent capabilities, plus visibility into live queue status, the ability to monitor and reassign conversations, and access to team-level reporting
- **Administrator** — configures the chat widget, routing rules, integrations, and security settings; manages user roles and permissions within CloudDesk Chat
- **Read-only / Reporting user** — available at Professional and Enterprise tiers, allowing stakeholders (e.g., a CX leader or executive) to view chat analytics without conversation or configuration access

Role definitions and permission granularity align with the broader Corvex Cloud role-based access model described in the platform's Security Features.

---

## 12. Limitations

- CloudDesk Chat is a real-time channel and is not designed as a substitute for asynchronous case management on long-running or multi-day issues; such conversations are best transitioned to the standard case workflow
- The number of simultaneous chats an agent can effectively manage is a configurable soft limit, not a hard product cap, and Corvex recommends teams set this based on issue complexity rather than maximizing concurrency
- Multi-language widget support is capped at 5 languages on Professional; unlimited language support requires Enterprise
- Proactive chat triggers and AI-assisted response suggestions are not available on the Starter plan
- Native mobile SDKs require a minimum supported OS version consistent with current Corvex Cloud platform requirements; older device operating systems may only support the mobile web widget experience
- CloudDesk Chat does not currently support voice or video calling; live chat is text-based messaging only

---

## 13. Subscription Availability

CloudDesk Chat is included as a core channel across all three Corvex Cloud subscription plans, with feature availability scaling by tier as described throughout this document:

| Capability | Starter | Professional | Enterprise |
|---|---|---|---|
| Core live chat & unified workspace | Included | Included | Included |
| Canned responses, transfer, internal notes | Included | Included | Included |
| Advanced routing & proactive triggers | — | Included | Included |
| Multi-language widget | — | Up to 5 languages | Unlimited |
| CSAT / NPS chat surveys | Basic CSAT only | CSAT + NPS | CSAT + NPS |
| Team performance analytics | — | Included | Included |
| AI-assisted response suggestions | — | — | Included |
| Custom SLA-backed response times | — | — | Included |
| Dedicated infrastructure / multi-brand | — | — | Included |

Full plan pricing, seat minimums, and billing terms are defined in the official Corvex Cloud Pricing Guide.

---

## 14. Common Use Cases

- **E-commerce pre- and post-purchase support** — answering product questions before checkout and resolving order issues after purchase, with order data visible directly in the conversation
- **Fintech account support** — providing responsive, auditable live support for account and transaction questions, with role-based access controls suited to regulated environments
- **Travel and hospitality time-sensitive issues** — handling urgent booking, cancellation, or itinerary questions where response speed materially affects customer experience
- **B2B SaaS in-app support** — embedding CloudDesk Chat directly within a customer's own product to provide contextual, real-time help without redirecting users to a separate support site
- **Lead qualification and pre-sales chat** — using proactive triggers and routing to connect prospective customers with the right team before a purchase decision

---

## 15. Future Roadmap

Consistent with the broader Corvex Cloud long-term roadmap, planned directions for CloudDesk Chat include:

- **Near term:** Expanded proactive trigger conditions, deeper e-commerce and CRM data surfacing within the chat interface, and continued reliability improvements to the real-time messaging layer
- **Mid term:** Broader AI-assisted capabilities extending beyond response suggestions, always with an emphasis on transparency and agent oversight of any automated or suggested action
- **Long term:** Continued convergence of chat with other real-time and near-real-time channels under a single conversational framework, in line with Corvex's broader vision of removing the artificial distinction between self-service and human-assisted support

Specific feature names, timelines, and release commitments are subject to change and are governed by the Corvex Product organization; this roadmap section is directional rather than a binding delivery commitment.

---

*This Product Overview describes CloudDesk Chat as offered under the Corvex Cloud platform by Corvex Technologies, Inc. For pricing details, refer to the official Corvex Cloud Pricing Guide. For company background, refer to the official Corvex Technologies Company Overview.*
