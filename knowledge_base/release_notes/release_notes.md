# Corvex Cloud
## Release Notes

*One entry per shipped version, organized by product, most recent release first. Entries reference known issue IDs (BUG-###) where a fix corresponds to an entry in `known_issues.json`, and feature entries are consistent with the capabilities described in `products.json` and the corresponding Product Overview documents.*

---

## CloudDesk Chat

### v4.1 — 2026-07-01

**Added**
- AI-assisted response suggestions (Enterprise), drawing on expanded automation capacity within the conversation composer.
- Expanded proactive trigger conditions, including scroll-depth and repeat-visit signals.

**Fixed**
- BUG-201 — Widget rendering twice on sites using both a page-specific template and a global footer snippet.
- BUG-203 — Pre-chat form field mapping breaking when a custom field was renamed rather than recreated.
- BUG-205 — Multi-language widget falling back to the default language for regional locale variants (e.g. en-GB, es-MX).

**Known Issues Carried Forward**
- BUG-204, BUG-206, BUG-207, BUG-208 remain open or under investigation; see `known_issues.json` for current status.

---

### v4.0 — 2025-06-01

**Added**
- Proactive chat triggers based on time-on-page and cart value.
- Mobile SDK v2 for iOS and Android, replacing the prior embed-only integration path.
- Full custom widget branding options (Enterprise).
- CSAT and NPS post-conversation surveys.

**Changed**
- Widget installation snippet updated to load asynchronously by default, improving host page load performance.

**Known Issues Introduced**
- BUG-201, BUG-203, BUG-205 (later fixed in v4.1); BUG-208 (Won't Fix).

---

### v3.0 — 2022-03-15

**Added**
- Advanced routing and automation rules (Professional and Enterprise).
- Multi-channel support, including early social messaging integration.
- Team-level performance analytics feeding into the newly launched CloudDesk Analytics module.

**Changed**
- Canned response management moved into a dedicated settings section, separate from general widget configuration.

---

### v2.0 — 2019-05-01

**Added**
- Zapier connectivity and the first version of the Corvex integration marketplace.
- Customer context panel showing prior conversation history alongside an active chat.
- Basic satisfaction (CSAT) surveys.

---

### v1.0 — 2016-02-10

**Initial release.**
- Core real-time messaging widget embeddable on customer websites.
- Unified agent workspace with shared inbox for live conversations.
- Canned responses, conversation transfer, and internal notes.
- Basic reporting dashboard with a 30-day lookback window.

---

## CloudDesk Tickets

### v5.3 — 2026-06-01

**Added**
- AI-assisted ticket triage (Enterprise), surfacing suggested tags and priority on incoming tickets.
- Expanded bulk action limits for Enterprise accounts.

**Fixed**
- BUG-301 — SLA countdown recalculating from the time of a priority change rather than original ticket creation time.
- BUG-306 — Automation rules referencing a deleted field silently stopping instead of surfacing a configuration warning.

**Known Issues Carried Forward**
- BUG-302, BUG-303, BUG-305, BUG-307, BUG-308 remain open or under investigation; see `known_issues.json` for current status.

---

### v5.2 — 2025-08-15

**Added**
- Custom SLA rules scoped by category in addition to priority.
- Merge and split ticket actions redesigned for faster multi-select workflows.

**Known Issues Introduced**
- BUG-301, BUG-306 (later fixed in v5.3).

---

### v5.1 — 2024-11-01

**Added**
- Native integrations with additional project management and engineering tools.
- Custom ticket field validation rules.

**Known Issues Introduced**
- BUG-304 (email threading header dropped by certain legacy email clients — Won't Fix).

---

### v5.0 — 2024-02-12

**Added**
- Full SLA management rework, including business-hours-only calculation and configurable breach alerting.
- Macro system replacing the earlier, more limited canned-action shortcuts.
- Custom ticket fields and forms (Professional and Enterprise).

**Changed**
- Ticket status model expanded from three default statuses to a fully configurable set.

---

### v4.0 — 2022-09-05

**Added**
- Native e-commerce platform integrations, surfacing order data directly within a ticket.
- Assignment rules supporting round-robin and skill-tag-based routing.

---

### v3.0 — 2020-04-20

**Added**
- Web form channel for direct ticket submission from a customer's website.
- Tagging and categorization system, feeding early reporting capabilities.

---

### v2.0 — 2018-01-10

**Added**
- CRM integration support (initial release, single-platform).
- Internal notes and @mentions for cross-agent collaboration on a ticket.

---

### v1.0 — 2015-09-01

**Initial release.**
- Email-to-ticket conversion establishing the core case management workflow.
- Basic status and priority fields.
- Canned responses.

---

## CloudDesk Analytics

### v3.2 — 2026-06-15

**Added**
- AI-assisted trend and anomaly surfacing (Enterprise).
- Cross-brand and cross-region reporting (Enterprise).

**Fixed**
- BUG-401 — Custom dashboard widget cache not invalidating immediately after a referenced tag was renamed.

**Known Issues Carried Forward**
- BUG-402, BUG-403, BUG-404, BUG-406, BUG-407 remain open or under investigation; see `known_issues.json` for current status.

---

### v3.1 — 2025-09-01

**Added**
- Data warehouse export (Enterprise), with configurable dataset selection and delivery schedule.
- Scheduled report delivery to individual recipients and distribution lists.

**Known Issues Introduced**
- BUG-401 (later fixed in v3.2); BUG-405 (CSAT trend line not flagging a mid-period survey scale change — Open).

---

### v3.0 — 2023-01-20

**Added**
- Custom dashboards with configurable widgets, filters, and saved views (Professional and Enterprise).
- NPS reporting alongside existing CSAT reporting.
- Threshold alerts for team leads and administrators.

---

### v2.0 — 2020-08-11

**Added**
- Custom date range reporting beyond the standard 30-day lookback (Professional and Enterprise).
- Channel breakdown views separating chat, email, and social performance.

---

### v1.0 — 2018-05-14

**Initial release.**
- Real-time queue dashboard.
- Standard volume, first response time, and resolution time reporting.
- Basic CSAT reporting.

---

## CloudDesk API Platform

### v2.7 — 2026-05-01

**Added**
- Early access endpoint program for Enterprise customers.
- Dedicated webhook infrastructure option for high-volume Enterprise accounts.

**Fixed**
- BUG-501 — Offset-based pagination returning duplicate records when underlying data changed mid-iteration; cursor-based pagination introduced as the recommended approach.
- BUG-505 — Bulk update endpoint's per-record error array inconsistently ordered relative to the submitted batch.

**Known Issues Carried Forward**
- BUG-502, BUG-503, BUG-504, BUG-506, BUG-507 remain open or under investigation; see `known_issues.json` for current status.

---

### v2.6 — 2025-07-10

**Added**
- Sandbox testing environment (Enterprise).
- Corvex partner API for bespoke Enterprise integrations.

**Known Issues Introduced**
- BUG-501, BUG-505 (later fixed in v2.7).

---

### v2.5 — 2024-01-25

**Added**
- Webhook support (Professional and Enterprise), including signed payload verification.
- API key rotation policy configuration.

---

### v2.0 — 2021-06-18

**Added**
- Full read/write API access (Professional and Enterprise), expanding beyond the initial read-only release.
- Rate limiting tiers aligned to plan level.

---

### v1.0 — 2019-11-04

**Initial release.**
- Read-only REST API access to core case and customer data.
- Developer documentation portal.
- Initial Zapier connectivity.

---

## CloudDesk Mobile

### v6.0 — 2026-07-20

**Added**
- AI-assisted suggested responses on mobile (Enterprise), mirroring the desktop capability.
- Priority push notification infrastructure for Enterprise accounts.

**Fixed**
- BUG-601 — App crashing on launch after update on devices running the minimum supported OS version.
- BUG-603 — Revoked device sessions briefly reappearing as active due to a cached refresh token timing edge case.

**Known Issues Carried Forward**
- BUG-602, BUG-604, BUG-605, BUG-606, BUG-608 remain open or under investigation; see `known_issues.json` for current status.

---

### v5.9 — 2025-10-01

**Added**
- Team performance snapshots (Professional and Enterprise).
- Escalation approval directly from a push notification (Professional and Enterprise).

**Known Issues Introduced**
- BUG-601, BUG-603 (later fixed in v6.0); BUG-607 (MDM managed app configuration payload silently ignored on key casing mismatch — Open).

---

### v5.0 — 2024-05-14

**Added**
- Biometric app lock.
- Remote session revocation from the desktop Admin Dashboard.
- Configurable local data caching limits.

---

### v4.0 — 2022-11-08

**Added**
- SLA and breach alerting on mobile (Professional and Enterprise).
- Tablet-optimized layout for iPadOS and Android tablets.

---

### v3.0 — 2021-02-19

**Added**
- Offline draft composition with automatic queued sending on reconnect.
- Team queue view for team leads and administrators.

---

### v2.0 — 2019-09-03

**Added**
- Push notifications for new assignments, mentions, and SLA warnings.
- Customer and case history within the mobile ticket and chat view.

---

### v1.0 — 2017-06-20

**Initial release.**
- Native iOS and Android application.
- Ticket and chat inbox with basic reply capability.
- Canned response access from mobile.

---

*This release note history is maintained alongside `known_issues.json` and `products.json`. Version numbers, release dates, and fixed issue references are kept consistent across all three files.*
