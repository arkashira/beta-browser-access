# user-stories.md

## Epic 1: Beta Browser Visibility & Prominence

### US-1.1 — Pin beta browser to user shortcut bar
**As an** enterprise IT administrator, **I want** to force-pin the beta/secondary browser to the taskbar, Start menu, and desktop of targeted endpoints, **so that** users can't overlook it and beta engagement starts on day one.
- Pin state is enforced via GPO/MDM payload and survives reboot + user un-pin attempts (re-pins within 1 polling cycle, default 15 min)
- Supports Windows (taskbar/Start), macOS (Dock), and managed Chrome OS shelf
- Admin can scope pinning to AD/Entra groups, not just all-or-nothing
- Audit log records pin enforcement events per endpoint
- **Complexity: L**

### US-1.2 — First-run nudge banner
**As an** IT administrator, **I want** the primary browser to display a dismissible "Try the beta — your feedback shapes it" banner linking to the beta browser, **so that** I drive adoption without blocking the user's existing workflow.
- Banner deploys as a managed extension/policy in Chrome, Edge, Firefox
- Frequency cap configurable (e.g., max 1/day, suppress after N dismissals)
- Click-through and dismiss events are tracked back to the dashboard
- Honors a per-user "stop showing" after explicit opt-out
- **Complexity: M**

### US-1.3 — Default-handler steering for low-risk traffic
**As an** IT administrator, **I want** to route a configurable allowlist of internal/test URLs to open in the beta browser by default, **so that** real usage flows through beta without disrupting production-critical sites.
- URL/domain allowlist with wildcard + regex support
- Production-critical domains can be explicitly excluded (hard block from steering)
- Fallback to primary browser if beta browser is not installed/healthy
- Dry-run mode logs what *would* be steered before enforcement
- **Complexity: L**

---

## Epic 2: Feedback Collection Pipeline

### US-2.1 — In-browser feedback widget
**As a** beta-testing end user, **I want** a one-click feedback button embedded in the beta browser chrome, **so that** I can report issues without leaving my task or filing a ticket.
- Captures screenshot, current URL, browser version, and OS automatically
- Optional free-text + sentiment (👍/👎) in under 10 seconds
- Submissions queue offline and sync when connectivity returns
- PII redaction toggle for screenshots (admin-controlled)
- **Complexity: M**

### US-2.2 — Aggregate feedback dashboard
**As an** IT administrator, **I want** a dashboard aggregating all beta feedback by browser version, site, and severity, **so that** I can prioritize fixes and report adoption ROI to leadership.
- Filter/sort by version, OS, AD group, date range, sentiment
- Export to CSV and webhook/Jira/ServiceNow integration
- Trendline of feedback volume vs. active-beta-user count
- Drill-down from aggregate to individual submission
- **Complexity: M**

### US-2.3 — Automated feedback solicitation
**As an** IT administrator, **I want** to schedule contextual feedback prompts (e.g., after 5 sessions or 30 min of beta use), **so that** I collect input from real usage instead of relying on voluntary reports.
- Trigger rules based on usage thresholds (sessions, time, specific site visits)
- Prompt content and cadence are templated and editable
- Per-user prompt fatigue cap to avoid annoyance-driven uninstalls
- Response rate visible per campaign in dashboard
- **Complexity: M**

---

## Epic 3: Deployment & Lifecycle Management

### US-3.1 — Phased beta rollout
**As an** IT administrator, **I want** to deploy the beta browser to ring-based cohorts (canary → early → broad), **so that** I limit blast radius and validate stability before wide release.
- Define rings by AD/Entra group, percentage, or device attributes
- Promote/halt/rollback a ring with one action
- Auto-halt rule when crash rate or negative feedback exceeds a threshold
- Rollout status visible per ring in real time
- **Complexity: L**

### US-3.2 — Version pinning & auto-update control
**As an** IT administrator, **I want** to pin the beta browser to a specific build and control update channels, **so that** testers evaluate a known version and I avoid surprise regressions mid-cycle.
- Pin to exact version or channel (dev/beta/stable)
- Staged update windows (e.g., maintenance hours only)
- Rollback to previous pinned build retains user profile/data
- **Complexity: M**

### US-3.3 — Clean uninstall / sunset
**As an** IT administrator, **I want** to retire a beta browser fleet-wide and optionally migrate bookmarks/settings back to the primary browser, **so that** I close out a test cycle without leaving orphaned software or data.
- One-click decommission targeting a ring or whole fleet
- Optional export/import of bookmarks, saved passwords, history to primary browser
- Removes pins, banners, and steering policies as part of teardown
- Confirmation + audit record before destructive action
- **Complexity: M**

---

## Epic 4: Governance, Security & Compliance

### US-4.1 — Role-based access control
**As a** security/compliance officer, **I want** RBAC separating who can deploy, who can view feedback, and who can read PII-bearing screenshots, **so that** beta management complies with least-privilege policy.
- At least 3 built-in roles (Deployer, Analyst, Auditor) + custom roles
- SSO/SCIM provisioning via Entra/Okta
- Screenshot/PII access gated behind a distinct elevated permission
- **Complexity: M**

### US-4.2 — Compliance audit trail
**As a** compliance officer, **I want** an immutable, exportable log of every deployment, policy change, and feedback access event, **so that** I can satisfy SOC 2 / internal audit requirements.
- Append-only log with actor, timestamp, action, target
- Export to SIEM (syslog/CEF) and tamper-evident hashing
- Retention policy configurable to meet regulatory minimums
- **Complexity: M**

### US-4.3 — Data residency & redaction controls
**As a** compliance officer, **I want** to enforce where feedback/screenshot data is stored and auto-redact sensitive fields, **so that** beta testing doesn't create a GDPR/regional data-handling violation.
- Region-scoped storage selection (US/EU/self-hosted)
- Configurable redaction rules (regex, field-level) applied at capture
- Data subject deletion request honored across feedback store
- **Complexity: L**

---

**Summary:** 12 stories across 4 epics. Complexity mix: 4×L, 8×M — the L's (pin enforcement, traffic steering, phased rollout, data residency) are the technical risk drivers and should anchor sprint sequencing.