# Product Overview
## CloudDesk Mobile — by Corvex Cloud

*An official product brochure from Corvex Technologies, Inc.*

---

## 1. Product Introduction

**CloudDesk Mobile** is the native mobile application for support agents, team leads, and administrators who need to work outside the desktop agent workspace — whether that means responding to an urgent ticket while away from a desk, monitoring queue health during off-hours, or approving an escalation from a phone. Available for iOS and Android, CloudDesk Mobile connects to the same unified case data layer used across CloudDesk Chat, CloudDesk Tickets, and CloudDesk Analytics, so nothing an agent does from a phone is out of sync with what a colleague sees at their desk moments later.

CloudDesk Mobile should not be confused with the CloudDesk Chat mobile SDK, which is a separate, customer-facing tool that lets Corvex customers embed a live chat widget inside their *own* mobile apps. CloudDesk Mobile is the internal-facing application Corvex customers' support teams use to do their jobs from a phone or tablet.

---

## 2. Product Purpose

CloudDesk Mobile exists because support work does not stop at the edge of a desktop screen. Its purpose is to extend the core CloudDesk experience — case visibility, response capability, and team oversight — to agents, team leads, and administrators wherever they are, without sacrificing the context and controls available in the full desktop workspace.

Its purpose is threefold:
- Allow agents to respond to urgent tickets and chats without being tied to a desk
- Give team leads real-time queue and SLA visibility during off-hours or while traveling
- Give administrators the ability to review alerts and take basic action without delay

---

## 3. Target Users

CloudDesk Mobile is designed for:

- **Support agents** who need to respond to time-sensitive issues while away from their desktop workspace
- **Team leads and supervisors** monitoring queue health, SLA status, and team workload outside standard desk hours
- **On-call and after-hours support staff** covering urgent issues for teams operating extended or 24/7 coverage
- **Administrators** who need visibility into critical alerts (e.g., SLA breaches, system status) without requiring desktop access
- **Executives and CX leadership** who want a quick, high-level view of support performance without opening a full dashboard

CloudDesk Mobile is most valuable to organizations with extended support hours, distributed or remote teams, or leadership that expects visibility into support performance outside standard office hours — a pattern common among Corvex's e-commerce, travel, and fintech customers in particular.

---

## 4. Business Benefits

- **Faster response to urgent issues.** Agents and team leads can act on time-sensitive tickets or chats without waiting to reach a desktop.
- **Better after-hours coverage.** On-call staff can monitor and respond to a queue from a phone, reducing the need for dedicated after-hours desktop coverage for lower-volume periods.
- **Improved leadership visibility.** Team leads and executives get real-time performance visibility without needing to be at a desk, supporting faster staffing or escalation decisions.
- **No context loss between devices.** Because CloudDesk Mobile shares the same case data layer as the desktop experience, an agent who starts a response on mobile and finishes at their desk never loses context.
- **Reduced escalation delay.** Push notifications for SLA risk and critical alerts shorten the time between an issue arising and a human noticing it.

---

## 5. Core Features

- **Ticket and chat inbox** — view and respond to assigned tickets and active chats from a mobile device
- **Push notifications** — real-time alerts for new assignments, mentions, and incoming chats
- **Canned responses** — access to the same reusable response templates available in the desktop workspace
- **Customer and case history** — full conversation and customer history available within each ticket or chat, consistent with the desktop view
- **Basic status and priority management** — update ticket status, priority, and tags directly from the mobile app
- **Team queue view** — team leads can view real-time queue status and agent availability
- **Biometric app lock** — optional fingerprint or face-based app lock, in addition to standard account authentication

---

## 6. Premium Features

Available on **Professional** and **Enterprise** plans (per the Corvex Cloud Pricing Guide):

- **SLA and breach alerting** — push notifications specifically tied to configured SLA thresholds, mirroring desktop SLA management
- **Team performance snapshots** — condensed, mobile-optimized views of team-level analytics from CloudDesk Analytics
- **Advanced filtering and saved views** — mobile access to saved dashboard and queue filters configured on desktop
- **Approval and escalation actions** — team leads can approve escalations or reassign tickets directly from a mobile alert

**Enterprise-exclusive additions:**

- **Custom SLA-backed alert configuration**, aligned to the customer's negotiated contract terms
- **AI-assisted suggested responses on mobile**, extending the same Enterprise automation capacity available on desktop
- **Priority push notification infrastructure**, ensuring critical alerts are delivered with minimal delay even under high account-wide notification volume

---

## 7. Supported Platforms

- **iOS** — native application, supporting current and prior major iOS releases
- **Android** — native application, supporting current and prior major Android releases
- **Tablet support** — optimized layouts for both iOS and Android tablets, in addition to phone form factors
- **Offline draft support** — replies composed without connectivity are queued and sent automatically once connectivity is restored

CloudDesk Mobile does not currently offer a dedicated Windows or other desktop-native mobile-style application; desktop users are served by the standard web-based agent workspace described in the CloudDesk Chat, Tickets, and Analytics product overviews.

---

## 8. Integrations

CloudDesk Mobile does not introduce separate integrations of its own; instead, it surfaces the results of integrations configured elsewhere in Corvex Cloud:

- **CRM and e-commerce data** configured via the desktop workspace is visible within relevant tickets and chats on mobile (Professional and Enterprise)
- **Collaboration tool alerts** configured for SLA breaches or escalations may be mirrored as mobile push notifications
- **Single Sign-On (SSO)** integrations used for desktop authentication extend to mobile login where supported by the customer's identity provider

Mobile-specific API or webhook configuration is not applicable; all API Platform capabilities described in the CloudDesk API Platform product overview apply at the account level, independent of whether access originates from desktop or mobile.

---

## 9. Security Features

- **Encryption in transit and at rest**, consistent with Corvex Cloud's platform-wide standard (TLS 1.2+ in transit, AES-256 at rest)
- **Role-based access control**, mirroring the same permissions an agent, team lead, or administrator holds on desktop
- **Single Sign-On (SAML 2.0)** support at the Professional and Enterprise tiers, extended to mobile login
- **Biometric app lock**, adding a device-level authentication layer beyond account login
- **Remote session revocation**, allowing administrators to immediately log out a lost or compromised mobile device from the desktop admin console
- **Configurable data caching limits**, controlling how much case data is retained locally on a device for offline access
- **Audit logging** of mobile-originated actions, indistinguishable in the audit trail from equivalent desktop actions, retained per the customer's plan tier

CloudDesk Mobile does not store customer payment information locally on the device under any circumstance.

---

## 10. Architecture Overview (Conceptual)

CloudDesk Mobile is built as a native client application connecting to the same underlying case data layer and APIs used by the desktop agent workspace, rather than as a separately maintained mobile-specific backend. At a conceptual level:

- **Native client layer** — the iOS and Android applications themselves, responsible for local rendering, offline draft queuing, and push notification handling
- **Synchronization layer** — connects the mobile client to the same case data layer used across Corvex Cloud, ensuring real-time consistency between mobile and desktop views
- **Notification delivery layer** — evaluates account and user-level alert conditions (new assignment, SLA risk, mention) and delivers push notifications through standard mobile platform notification services
- **Local security layer** — manages biometric lock, local data caching limits, and remote session revocation at the device level
- **Shared access control layer** — applies the same role-based permissions used elsewhere in Corvex Cloud, ensuring mobile access never exceeds a user's desktop-equivalent permissions

Because CloudDesk Mobile reads from and writes to the same case data layer as the rest of Corvex Cloud, an action taken on mobile is reflected on desktop, and vice versa, without any separate synchronization step. This overview is intentionally conceptual; detailed technical architecture is documented separately for internal and technical partner audiences.

---

## 11. User Roles

- **Agent** — views assigned tickets and chats, responds, updates status, and applies tags; permissions mirror the Agent role in CloudDesk Chat and CloudDesk Tickets
- **Team Lead / Supervisor** — includes all Agent capabilities, plus team queue visibility, escalation approval, and access to team performance snapshots
- **Administrator** — manages mobile-specific settings such as remote session revocation and mobile notification configuration, in addition to standard administrative permissions
- **Read-only / Reporting user** — available at Professional and Enterprise tiers, allowing stakeholders to view condensed performance snapshots without case-level access

Role definitions and permission granularity align with the broader Corvex Cloud role-based access model described in the platform's Security Features; CloudDesk Mobile does not introduce any mobile-specific roles beyond those already defined across the platform.

---

## 12. Limitations

- CloudDesk Mobile is designed for responsive, on-the-go case handling and monitoring; complex configuration tasks (automation rules, custom fields, integration setup) are not available on mobile and require the desktop web experience
- Offline support is limited to draft composition; full case history and new incoming items require connectivity to load
- Custom dashboard building, available on desktop CloudDesk Analytics, is not available on mobile; mobile access to Analytics is limited to condensed, pre-defined snapshot views
- SLA and breach alerting on mobile is available only on Professional and Enterprise plans, consistent with SLA management availability on desktop
- CloudDesk Mobile requires a currently supported iOS or Android version; older, unsupported device operating systems are not guaranteed to run the application

---

## 13. Subscription Availability

CloudDesk Mobile is included as the mobile access layer across all three Corvex Cloud subscription plans, with feature availability scaling by tier as described throughout this document:

| Capability | Starter | Professional | Enterprise |
|---|---|---|---|
| Ticket & chat inbox, response, status updates | Included | Included | Included |
| Push notifications for assignments & mentions | Included | Included | Included |
| Biometric app lock, offline drafts | Included | Included | Included |
| SLA & breach alerting | — | Included | Included, custom-configured |
| Team performance snapshots | — | Included | Included |
| Approval & escalation actions | — | Included | Included |
| AI-assisted suggested responses (mobile) | — | — | Included |
| Priority push notification infrastructure | — | — | Included |

Full plan pricing, seat minimums, and billing terms are defined in the official Corvex Cloud Pricing Guide.

---

## 14. Common Use Cases

- **After-hours on-call coverage** — support teams handling low-volume overnight or weekend coverage from mobile devices rather than staffing a full desktop shift
- **Field and travel-based response** — team leads at e-commerce or travel companies responding to urgent escalations while traveling or away from the office
- **Executive spot-checks** — CX leadership reviewing team performance snapshots between meetings without needing to open the full desktop dashboard
- **Retail and hospitality floor staff support** — customer-facing staff without a dedicated desk using mobile to check on customer issues tied to their location or shift
- **Rapid escalation approval** — team leads approving urgent escalations from a phone to avoid delay while away from their desk

---

## 15. Future Roadmap

Consistent with the broader Corvex Cloud long-term roadmap, planned directions for CloudDesk Mobile include:

- **Near term:** Expanded offline capability beyond draft composition, deeper customization of mobile notification preferences, and continued performance improvements for large ticket volumes on mobile devices
- **Mid term:** Broader AI-assisted suggested response availability beyond Enterprise-only access over time, and expanded team performance snapshot customization
- **Long term:** Continued convergence of the mobile and desktop experiences toward full feature parity where appropriate, while preserving a deliberately focused, on-the-go interface for scenarios where a full desktop-equivalent experience is not the right fit

Specific feature names, timelines, and release commitments are subject to change and are governed by the Corvex Product organization; this roadmap section is directional rather than a binding delivery commitment.

---

*This Product Overview describes CloudDesk Mobile as offered under the Corvex Cloud platform by Corvex Technologies, Inc. For pricing details, refer to the official Corvex Cloud Pricing Guide. For company background, refer to the official Corvex Technologies Company Overview.*
