# Corvex Technologies, Inc.
## Security Policy

**Document Type:** Enterprise Policy
**Applies To:** Corvex Cloud (CloudDesk Chat, CloudDesk Tickets, CloudDesk Analytics, CloudDesk API Platform, CloudDesk Mobile) and supporting infrastructure
**Effective Date:** Current as of publication
**Owner:** Security & Trust, in coordination with Engineering and Legal & Compliance

---

## 1. Purpose

This Security Policy establishes the official framework governing how Corvex Technologies, Inc. ("Corvex") protects the confidentiality, integrity, and availability of customer data, End User data, and the Corvex Cloud platform itself. Its purpose is to:

- Provide customers, prospective customers, and internal Corvex teams with a clear account of the security controls and practices applied across Corvex Cloud
- Establish accountability for security decisions and incident response across Corvex's Security & Trust, Engineering, and Legal & Compliance functions
- Support the "slow is smooth, smooth is fast" and "default to transparency" values described in the Corvex Technologies Company Overview, particularly with respect to areas — like security — where mistakes are expensive to undo
- Serve as the internal reference governing how security features described in customer-facing Administrator Guides are designed, maintained, and audited

This policy addresses platform and organizational security broadly. It does not address the handling of personal data as a privacy matter, which is addressed in the Privacy Policy, or monetary billing matters, which are addressed in the Refund Policy.

---

## 2. Scope

### 2.1 Systems and Services Covered

This policy applies to:

- The Corvex Cloud platform in its entirety, including CloudDesk Chat, CloudDesk Tickets, CloudDesk Analytics, CloudDesk API Platform, and CloudDesk Mobile
- Underlying infrastructure operated by Corvex or its Sub-processors in support of Corvex Cloud
- Corvex's internal corporate systems to the extent they interact with or provide access to customer data (for example, internal tools used by Support or Customer Success)
- corvexcloud.com and associated Corvex-operated web properties

### 2.2 Who This Policy Applies To

This policy applies to:

- All Corvex Technologies employees and contractors, regardless of department or location
- Sub-processors and vendors with access to Corvex Cloud infrastructure or customer data, subject to contractual security obligations consistent with this policy
- Customers and Customer Users, to the extent Section 5.4 describes shared security responsibilities

### 2.3 What This Policy Does Not Cover

This policy does not govern:

- The security of a customer's own website, network, or internal systems, including the environment in which the CloudDesk Chat widget or mobile SDK is embedded
- A customer's own internal access control decisions (for example, which of their employees are assigned the Administrator role), beyond the platform capabilities Corvex provides to support such decisions
- Personal data handling practices addressed in the Privacy Policy

---

## 3. Definitions

**Access Control:** The set of mechanisms — including authentication, authorization, and role-based permissions — that govern who can access a given system or piece of data.

**Availability:** The security property ensuring authorized users can access systems and data when needed, distinct from Confidentiality and Integrity.

**Confidentiality:** The security property ensuring data is accessible only to those authorized to access it.

**Incident:** An event that compromises, or has the potential to compromise, the Confidentiality, Integrity, or Availability of Corvex Cloud or the data it processes.

**Integrity:** The security property ensuring data is accurate, complete, and has not been improperly altered.

**Least Privilege:** The security principle of granting a user or system only the minimum access necessary to perform its function.

**Multi-Factor Authentication (MFA):** An authentication method requiring more than one distinct form of verification, such as a password combined with a one-time code or biometric factor.

**Security Control:** A specific technical, administrative, or physical measure implemented to protect Confidentiality, Integrity, or Availability.

**Sub-processor:** A third-party service provider engaged by Corvex to support the delivery of Corvex Cloud, as defined in the Privacy Policy, and subject to security obligations consistent with this policy.

**Vulnerability:** A weakness in a system that could be exploited to compromise Confidentiality, Integrity, or Availability.

---

## 4. Policy Statements

### 4.1 Data Encryption

All customer and End User data processed through Corvex Cloud is encrypted in transit using TLS 1.2 or higher, and encrypted at rest using AES-256, applied consistently across all plan tiers as a non-negotiable platform baseline, as described in the CloudDesk Chat Administrator Guide. These settings are managed by Corvex and are not independently configurable by customers, ensuring a consistent security baseline account-wide.

### 4.2 Access Control and Authentication

Corvex Cloud enforces role-based access control across all products, governing what a given user can view, edit, or configure based on their assigned role, as described in the relevant Administrator Guide for each CloudDesk product. Customers on Professional and Enterprise plans may additionally configure:

- Single Sign-On (SSO) via SAML 2.0, optionally enforced as mandatory account-wide
- SCIM-based automated user provisioning and deprovisioning (Enterprise)
- IP allowlisting restricting workspace and Admin Dashboard access to approved network ranges
- Custom roles scoped to the minimum permissions necessary for a given function, consistent with the Least Privilege principle

Corvex internally applies Least Privilege and, where applicable, Multi-Factor Authentication to its own employee access to production systems and customer data, with access reviewed periodically and revoked promptly upon role change or departure.

### 4.3 API and Credential Security

CloudDesk API Platform enforces API key-based authentication, with keys scoped as read-only or read/write and independently rotatable by customer administrators. API key secret values are displayed only once at creation and are never retrievable afterward, consistent with the CloudDesk API Platform Administrator Guide. All API and webhook traffic is HTTPS-only, and webhook payloads are cryptographically signed to allow receiving systems to verify authenticity.

### 4.4 Audit Logging

Corvex Cloud maintains an audit log of security- and configuration-relevant actions across all products, including user role changes, authentication configuration changes, integration connections, and API key activity. Audit log retention is 90 days on Professional, with extended, custom retention available on Enterprise, as described in the relevant Administrator Guide.

### 4.5 Infrastructure Security

Corvex maintains infrastructure-level security controls, including network segmentation, monitoring, and infrastructure-level backup practices, as described in the relevant Administrator Guides' Backup and Restore sections. Enterprise customers with strict isolation requirements may request dedicated infrastructure options, established during contracting.

### 4.6 Vulnerability Management

Corvex maintains a program for identifying, evaluating, and remediating Vulnerabilities across the Corvex Cloud platform, including regular security testing and monitoring of underlying infrastructure and dependencies. Vulnerabilities are prioritized for remediation based on severity and potential impact to Confidentiality, Integrity, or Availability.

### 4.7 Incident Response

Corvex maintains an incident response process for identifying, containing, investigating, and remediating security Incidents. Where an Incident is determined to have affected customer data, Corvex will notify affected customers without undue delay, consistent with applicable law and the customer's Order Form where applicable, and will provide relevant detail to support the customer's own incident response obligations.

### 4.8 Change Management

Changes to production systems supporting Corvex Cloud follow an internal review and testing process before deployment, consistent with the "slow is smooth, smooth is fast" principle described in the Corvex Technologies Company Overview, particularly for changes touching security-sensitive areas such as authentication, encryption, or access control.

### 4.9 Sub-processor Security

Corvex evaluates the security practices of Sub-processors before engagement and on an ongoing basis, as part of vendor risk management led by Security & Trust. Sub-processors are contractually bound to security obligations consistent with this policy.

### 4.10 Data Residency and Regional Controls

Enterprise customers with regional compliance or data residency requirements may request specific infrastructure configurations, established during contracting with their Customer Success Manager, as described in the CloudDesk Chat Administrator Guide and the Privacy Policy.

### 4.11 Employee Security Practices

Corvex requires employees and contractors with access to production systems or customer data to complete security awareness training and to follow Corvex's internal acceptable use and access control requirements. Access to production systems is granted on a Least Privilege basis and reviewed periodically.

### 4.12 Physical Security

Corvex's own office locations (Austin, Dublin, and Singapore) maintain standard physical access controls appropriate to a professional office environment. Corvex Cloud's underlying infrastructure is hosted with Sub-processors who maintain data center physical security controls consistent with industry-standard practices, evaluated as part of Corvex's Sub-processor security review.

### 4.13 Business Continuity

Corvex maintains infrastructure-level backup practices supporting the recovery of customer data in the event of a platform-level incident, as described in the Backup and Restore sections of the relevant Administrator Guides. Corvex's business continuity planning addresses both technical infrastructure recovery and operational continuity of customer-facing functions such as Support and Customer Success.

---

## 5. Responsibilities

### 5.1 Security & Trust

Security & Trust is responsible for:

- Defining and maintaining the security controls described in this policy
- Leading incident response for security Incidents affecting Corvex Cloud
- Conducting Sub-processor security risk assessments
- Maintaining Corvex's vulnerability management program
- Advising other departments on security requirements for new features, integrations, and infrastructure changes

### 5.2 Engineering

Engineering is responsible for:

- Implementing security controls within the Corvex Cloud platform, including encryption, access control, and API security described in Section 4
- Participating in the change management process for security-sensitive production changes
- Remediating Vulnerabilities identified through Corvex's vulnerability management program within timeframes appropriate to their severity

### 5.3 Legal & Compliance

Legal & Compliance is responsible for:

- Reviewing this policy for consistency with applicable law and customer contractual commitments
- Supporting Security & Trust in the notification process for Incidents with legal or regulatory implications
- Reviewing Sub-processor agreements for consistency with this policy's security obligations

### 5.4 Customers and Customer Users

Corvex Cloud operates on a shared responsibility model. Customers and their Customer Users are responsible for:

- Configuring available security features (SSO, IP allowlisting, custom roles, MFA where applicable through their identity provider) appropriately for their organization's needs
- Assigning user roles consistent with the Least Privilege principle within their own account
- Safeguarding their own login credentials and API keys, and rotating API keys consistent with the guidance in the CloudDesk API Platform Administrator Guide
- Promptly deactivating departing employees' access, as described in the relevant Administrator Guide's offboarding guidance
- Securing their own website, network, and any environment in which the CloudDesk Chat widget or mobile SDK is embedded
- Reporting any suspected security concern involving their account to Corvex Support

### 5.5 All Corvex Personnel

All Corvex employees and contractors are responsible for:

- Following Corvex's internal security and acceptable use requirements
- Completing required security awareness training
- Reporting any suspected security concern or Incident promptly to Security & Trust

---

## 6. Exceptions

### 6.1 Enterprise Order Form Variations

Enterprise customers may negotiate specific security terms, including enhanced service level commitments related to security incident notification timelines, as part of their signed Order Form. Where such negotiated terms differ from this policy's default provisions, the Order Form takes precedence for that customer's account.

### 6.2 Legal Process

Corvex may take actions otherwise inconsistent with the general provisions of this policy where required to comply with a valid legal process, subject to Corvex's standard practice of notifying affected customers where legally permitted to do so.

### 6.3 Emergency Security Actions

In the event of an active security threat, Corvex's Security & Trust team may take immediate protective action — including temporarily restricting access or suspending a specific feature — that falls outside standard change management processes described in Section 4.8, in order to contain a threat to Confidentiality, Integrity, or Availability. Such actions are reviewed and documented after the fact.

### 6.4 Customer-Configured Deviations

Where a customer's own configuration choices (for example, declining to enable SSO or IP allowlisting where available) result in a lower security posture than Corvex's available controls would otherwise support, this is understood as a customer decision within the shared responsibility model described in Section 5.4, rather than a deviation from this policy by Corvex.

---

## 7. Compliance

### 7.1 Regulatory and Framework Alignment

Corvex designs its security program with reference to widely recognized security principles and control frameworks relevant to cloud-based SaaS platforms. Because Corvex serves customers across multiple industries and jurisdictions, specific compliance obligations may vary; customers with particular regulatory requirements should discuss them with their Customer Success Manager.

### 7.2 Independent Assessment

Corvex's security program is subject to periodic independent assessment as part of standard practice for enterprise SaaS platforms. Enterprise customers seeking specific compliance documentation should contact their Customer Success Manager or Legal & Compliance.

### 7.3 Internal Audit

Security controls described in this policy are subject to periodic internal audit by Security & Trust to confirm ongoing effectiveness and alignment with this policy.

### 7.4 Customer Security Reviews

Corvex supports reasonable customer security review requests, particularly for Enterprise prospects and customers conducting vendor risk assessments, coordinated through the sales or Customer Success relationship.

### 7.5 Policy Review Cadence

This policy is reviewed at least annually by Security & Trust and Legal & Compliance, and additionally whenever a material change to Corvex Cloud's architecture, infrastructure, or the threat landscape warrants earlier review.

---

## 8. Frequently Asked Questions

**How is my data encrypted?**
All data is encrypted in transit using TLS 1.2 or higher and at rest using AES-256, applied consistently across all plans as a non-configurable baseline.

**Does Corvex support Single Sign-On?**
Yes, via SAML 2.0, available on Professional and Enterprise plans, and configurable as optional or mandatory account-wide.

**Can I restrict access to my account by IP address?**
Yes, on Professional and Enterprise plans, using IP allowlisting configured under Admin Dashboard > Security.

**What happens if there's a security incident affecting my data?**
Corvex will notify affected customers without undue delay, consistent with applicable law and any specific terms in your Order Form, and provide relevant detail to support your own incident response.

**Does Corvex ever store my API key value where I can retrieve it later?**
No. API key secret values are displayed only once at creation and cannot be retrieved afterward for security reasons; a lost key must be replaced with a new one.

**Who is responsible for securing the environment where I've embedded the chat widget or mobile SDK?**
That falls under your organization's own responsibility, consistent with the shared responsibility model described in Section 5.4. Corvex secures the platform itself; you are responsible for your own website, app, and network environment.

**Does Corvex review the security practices of the vendors it uses?**
Yes. Sub-processors are evaluated for security practices before engagement and on an ongoing basis as part of Corvex's vendor risk management program.

**Can Enterprise customers request dedicated infrastructure?**
Yes. Dedicated infrastructure options are available to Enterprise customers with strict isolation requirements, established during contracting.

**How often does Corvex review this Security Policy?**
At least annually, and additionally whenever a material change to the platform, infrastructure, or threat landscape warrants earlier review.

**Who do I contact to report a security concern?**
See Section 10 for Corvex's security contact information.

---

## 9. Revision History

| Version | Date | Summary of Changes | Approved By |
|---|---|---|---|
| 1.0 | Initial publication | Initial publication of the Corvex Cloud Security Policy | Security & Trust, Legal & Compliance |

---

## 10. Contact Information

**To report a security concern or suspected vulnerability:**
Security & Trust, Corvex Technologies, Inc. — Austin, Texas headquarters.

**For Enterprise customers with security review or compliance documentation requests:**
Contact your assigned Customer Success Manager, or Security & Trust directly.

**For general account security questions (SSO, IP allowlisting, API key management):**
Refer to the relevant CloudDesk Administrator Guide, or contact Corvex Support through the channel appropriate to your plan tier.

**For legal or contractual questions related to this policy:**
Legal & Compliance, Corvex Technologies, Inc.

---

*This Security Policy is a Corvex Technologies, Inc. governance document describing our security practices across Corvex Cloud. It works in conjunction with, and does not replace, any Data Processing Agreement, Enterprise Order Form, or other signed agreement between Corvex and a customer. In the event of a conflict between this policy and such a signed agreement, the signed agreement takes precedence for that customer.*
