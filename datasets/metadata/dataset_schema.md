# Corvex Cloud — Structured Dataset Schema

*Reference documentation for the synthetic structured data package generated for the Corvex Cloud AI Customer Support Platform project. Covers 8 files (4 CSV, 4 JSON), all cross-referenced by consistent identifiers. Row/record counts and relationships below were verified programmatically at generation time — every foreign key reference resolves with zero orphans.*

---

## Entity Relationship Overview

```
                         ┌────────────────┐
                         │  products.json │  (5 records)
                         │  PK: product_id│
                         └───────┬────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
   ┌──────────▼─────────┐ ┌──────▼──────────┐ ┌─────▼───────────────┐
   │  known_issues.json  │ │ feature_requests │ │   release_notes.md   │
   │  FK: product_id      │ │      .csv        │ │ (unstructured, one   │
   │  (38 records)        │ │  FK: product_id,  │ │  entry per version, │
   └──────────────────────┘ │      customer_id  │ │  references BUG-### │
                             │  (320 records)     │ │  from known_issues) │
                             └────────┬───────────┘ └──────────────────────┘
                                      │
                                      │
   ┌──────────────────┐     ┌────────▼─────────┐     ┌───────────────────┐
   │  employees.json    │◄────│  customers.csv    │────►│    billing.csv     │
   │  PK: employee_id    │name │  PK: customer_id  │ FK  │  FK: customer_id  │
   │  (112 records)      │ ref │  (1,000 records)  │     │  (5,135 records)  │
   └─────────▲───────────┘     └────────┬──────────┘     └────────────────────┘
             │ name ref                 │ FK
             │                          │
   ┌─────────┴───────────┐     ┌────────▼──────────┐
   │    tickets.csv        │     │     crm.json       │
   │  FK: customer_id,      │     │  FK: customer_id   │
   │      assigned_agent    │     │  (1,000 records)   │
   │  (4,200 records)       │     └────────────────────┘
   └─────────────────────────┘
```

**Primary keys** are unique within their file. **Foreign keys** always reference a primary key in another file — no dataset invents an ID that doesn't resolve elsewhere.

---

## 1. customers.csv

**Rows:** 1,000
**Primary Key:** `customer_id`
**Referenced by:** `tickets.csv.customer_id`, `billing.csv.customer_id`, `feature_requests.csv.customer_id`, `crm.json.customer_id`
**References:** `employees.json.name` (via `account_manager`)

| Column | Type | Nullable | Description |
|---|---|---|---|
| `customer_id` | string | No | Unique identifier, format `CUST-#####` |
| `full_name` | string | No | Primary contact's full name |
| `email` | string | No | Primary contact's email address |
| `company_name` | string | No | Customer organization name |
| `country` | string | No | Country of the primary contact |
| `timezone` | string | No | IANA timezone identifier |
| `phone` | string | No | Contact phone number |
| `subscription_plan` | enum | No | `Starter` \| `Professional` \| `Enterprise` |
| `account_status` | enum | No | `Active` \| `Trial` \| `Past Due` \| `Cancelled` |
| `registration_date` | date (`YYYY-MM-DD`) | No | Account creation date |
| `renewal_date` | date (`YYYY-MM-DD`) | No | Next scheduled renewal |
| `last_login` | datetime (`YYYY-MM-DD HH:MM`) | No | Most recent login |
| `preferred_language` | string | No | Customer's preferred UI/communication language |
| `support_tier` | enum | No | `Standard` \| `Priority` \| `Premium 24/7` (maps 1:1 to plan) |
| `account_manager` | string | Yes (empty string) | Name of assigned CSM; populated mainly for Enterprise — resolves against `employees.json` |
| `monthly_revenue` | float | No | Recurring monthly value in USD; `0.0` for Trial accounts |
| `lifetime_value` | float | No | Cumulative revenue to date; `0.0` for Trial accounts |

---

## 2. tickets.csv

**Rows:** 4,200
**Primary Key:** `ticket_id`
**Foreign Keys:** `customer_id` → `customers.csv.customer_id`; `assigned_agent` → `employees.json.name`

| Column | Type | Nullable | Description |
|---|---|---|---|
| `ticket_id` | string | No | Unique identifier, format `TKT-######` |
| `customer_id` | string | No | Requesting customer |
| `created_date` | datetime (`YYYY-MM-DD HH:MM`) | No | Ticket creation timestamp |
| `priority` | enum | No | `Low` \| `Normal` \| `High` \| `Urgent` |
| `department` | enum | No | `Technical Support` \| `Billing` \| `Account Management` \| `Onboarding` \| `Product & Feature Requests` \| `Security` |
| `category` | string | No | Sub-classification within department (Title Case, derived from subject) |
| `subject` | string | No | Short ticket title |
| `message` | string | No | Full customer-submitted message, coherent with `subject` |
| `assigned_agent` | string | No | Handling agent's full name — resolves against `employees.json` |
| `resolution` | string | Yes (empty string) | Resolution note; populated only when `status` is `Resolved`/`Closed` |
| `status` | enum | No | `Open` \| `Pending` \| `Resolved` \| `Closed` |
| `sentiment` | enum | No | `Positive` \| `Neutral` \| `Negative` |
| `resolution_time` | float (hours) | Yes (empty) | Time to resolution; empty for unresolved tickets |
| `escalation` | enum | No | `Yes` \| `No` |

---

## 3. billing.csv

**Rows:** 5,135
**Primary Key:** `invoice_id`
**Foreign Key:** `customer_id` → `customers.csv.customer_id`

| Column | Type | Nullable | Description |
|---|---|---|---|
| `invoice_id` | string | No | Unique identifier, format `INV-######` |
| `customer_id` | string | No | Billed customer (never a Trial-status customer) |
| `plan` | enum | No | `Starter` \| `Professional` \| `Enterprise` (matches customer's plan) |
| `amount` | float | No | Invoice amount in the listed `currency` |
| `currency` | enum | No | `USD` \| `EUR` \| `GBP` \| `AUD` \| `CAD` |
| `payment_status` | enum | No | `Paid` \| `Pending` \| `Failed` \| `Refunded` |
| `payment_method` | enum | No | `Credit Card` \| `ACH Bank Transfer` \| `Wire Transfer` \| `PayPal` |
| `due_date` | date (`YYYY-MM-DD`) | No | Invoice due date |
| `paid_date` | date (`YYYY-MM-DD`) | Yes (empty) | Payment date; empty for `Pending`/`Failed` |
| `refund_status` | enum | No | `Not Requested` \| `Requested` \| `Approved - Refunded` \| `Denied` |

**Note:** Invoice history is capped to a recent ~18-month window per customer rather than full account lifetime, matching how a real billing export typically surfaces recent invoices.

---

## 4. feature_requests.csv

**Rows:** 320
**Primary Key:** `request_id`
**Foreign Keys:** `customer_id` → `customers.csv.customer_id`; `product_id`/`product_name` → `products.json.product_id`; `assigned_product_manager` → `employees.json.name`

| Column | Type | Nullable | Description |
|---|---|---|---|
| `request_id` | string | No | Unique identifier, format `FR-#####` |
| `customer_id` | string | No | Requesting customer |
| `customer_plan` | enum | No | Denormalized copy of the customer's plan at time of request |
| `product_id` | string | No | Target product, references `products.json` |
| `product_name` | string | No | Denormalized product name |
| `category` | string | No | Request category (e.g. Automation, Reporting, Integrations) |
| `title` | string | No | Short request title |
| `description` | string | No | Full request description |
| `submitted_date` | date (`YYYY-MM-DD`) | No | Submission date |
| `status` | enum | No | `Under Review` \| `Planned` \| `In Progress` \| `Shipped` \| `Declined` \| `Duplicate` |
| `priority` | enum | No | `Low` \| `Medium` \| `High` \| `Critical` (internal triage priority) |
| `votes` | integer | No | Customer upvote count; correlates with request age and account plan |
| `assigned_product_manager` | string | Yes (empty string) | Owning PM from the Product department; blank for many `Under Review` items |

---

## 5. employees.json

**Records:** 112
**Primary Key:** `employee_id`
**Referenced by:** `tickets.csv.assigned_agent`, `customers.csv.account_manager`, `feature_requests.csv.assigned_product_manager` (all via `name`, not `employee_id`)

| Field | Type | Nullable | Description |
|---|---|---|---|
| `employee_id` | string | No | Unique identifier, format `EMP###` |
| `name` | string | No | Full name — the join key used by other datasets |
| `department` | enum | No | One of 14 departments (Technical Support, Engineering, Customer Success, Sales, Product, Data & AI Research, Marketing, Finance & Operations, Security & Trust, People (HR), Design, Legal & Compliance, Support / Customer Experience, Executive Leadership) |
| `role` | string | No | Job title |
| `skills` | array[string] | No | 3–5 relevant skills, department-appropriate |

```json
{
  "employee_id": "EMP001",
  "name": "Sarah Chen",
  "department": "Technical Support",
  "role": "Support Engineer",
  "skills": ["CRM Systems", "Authentication", "Cloud"]
}
```

---

## 6. products.json

**Records:** 5 (one per CloudDesk module)
**Primary Key:** `product_id`
**Referenced by:** `known_issues.json.product_id`, `feature_requests.csv.product_id`, `release_notes.md` (version headers)

| Field | Type | Nullable | Description |
|---|---|---|---|
| `product_id` | string | No | Unique identifier, format `P###` |
| `name` | string | No | Product name (e.g. "CloudDesk Chat") |
| `category` | string | No | Product category label |
| `version` | string | No | Current shipped version number |
| `status` | string | No | Lifecycle status (`Active`) |
| `release_date` | date (`YYYY-MM-DD`) | No | Original v1.0 release date |
| `description` | string | No | One-paragraph product summary |
| `supported_platforms` | array[string] | No | Platforms/access modes the product runs on |
| `available_plans` | array[string] | No | Plan tiers the product is included in |
| `features` | array[string] | No | Core and premium feature list |
| `integrations` | array[string] | No | Supported integration categories |
| `security_features` | array[string] | No | Security capabilities specific to the product |

---

## 7. crm.json

**Records:** 1,000 (one per customer)
**Primary Key:** `customer_id` (also functions as the sole key — one CRM record per customer)
**Foreign Key:** `customer_id` → `customers.csv.customer_id`

| Field | Type | Nullable | Description |
|---|---|---|---|
| `customer_id` | string | No | References `customers.csv` |
| `health_score` | integer (5–99) | No | Account health score; correlates with `account_status` |
| `renewal_probability` | float (0.0–1.0) | No | Predicted renewal likelihood; correlates with `health_score` |
| `last_meeting` | date (`YYYY-MM-DD`) | Yes (null) | Most recent CSM touchpoint; null if no dedicated manager or account is Cancelled |
| `next_follow_up` | date (`YYYY-MM-DD`) | Yes (null) | Next scheduled touchpoint; null for Cancelled accounts |
| `notes` | string | No | Free-text CSM note; tone (healthy/neutral/at-risk/churned) matches `health_score` |

---

## 8. known_issues.json

**Records:** 38
**Primary Key:** `issue_id`
**Foreign Key:** `product_id` → `products.json.product_id`
**Referenced by:** `release_notes.md` (via `issue_id` in "Fixed" entries)

| Field | Type | Nullable | Description |
|---|---|---|---|
| `issue_id` | string | No | Unique identifier, format `BUG-###` |
| `product_id` | string | No | Affected product |
| `product_name` | string | No | Denormalized product name |
| `title` | string | No | Short issue summary |
| `severity` | enum | No | `Low` \| `Medium` \| `High` \| `Critical` |
| `affected_version` | string | No | Version the issue was first observed in |
| `status` | string | No | `Open` \| `Investigating` \| `Won't Fix` \| `Fixed in X.X` |
| `reported_date` | date (`YYYY-MM-DD`) | No | Date first reported |
| `workaround` | string | No | Suggested interim workaround |
| `related_documentation` | string | No | Cross-reference to the relevant Troubleshooting Guide (often with a specific `CDW-####`/`CDT-####`/etc. code) |

---

## Bonus: release_notes.md (unstructured companion file)

Not a structured dataset, but tightly linked: 30 version entries across all 5 products. Every `"Fixed in X.X"` status in `known_issues.json` has a matching **Fixed** bullet in the corresponding version entry (verified — 10/10 match), and every "Known Issues Introduced" note in a version cross-references a real `issue_id`.

---

## Cross-File Join Cheat Sheet

| To join... | Use |
|---|---|
| A ticket to its customer | `tickets.csv.customer_id` = `customers.csv.customer_id` |
| A ticket to its handling agent's full profile | `tickets.csv.assigned_agent` = `employees.json.name` |
| A customer to their invoices | `billing.csv.customer_id` = `customers.csv.customer_id` |
| A customer to their CRM health record | `crm.json.customer_id` = `customers.csv.customer_id` |
| A customer to their assigned CSM's profile | `customers.csv.account_manager` = `employees.json.name` |
| A feature request to its target product | `feature_requests.csv.product_id` = `products.json.product_id` |
| A feature request to its owning PM | `feature_requests.csv.assigned_product_manager` = `employees.json.name` |
| A known issue to its product | `known_issues.json.product_id` = `products.json.product_id` |
| A known issue to its fix in release history | `known_issues.json.issue_id` appears in `release_notes.md` |

---

*All datasets were generated with a fixed random seed per file for reproducibility and validated post-generation for referential integrity (zero orphaned foreign keys across all files) and internal consistency (e.g., no Trial-status customer has invoices; no Cancelled account has a future `next_follow_up`).*
