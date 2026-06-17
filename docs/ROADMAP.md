# ROADMAP.md

## Overview

**beta‑browser‑access** is a lightweight, browser‑deployment management tool that guarantees beta or secondary browsers are prominently displayed and easily accessible to end‑users. By automating the promotion of experimental browsers, we increase feedback collection and streamline the testing workflow across the Axentx product portfolio.

This roadmap outlines the path from a minimum‑viable product (MVP) to a fully‑featured, production‑ready solution. All milestones are grounded in the current repo state, the Axentx runbook, and our existing data assets.

---

## 1. MVP – “Launch‑Ready Core”

| # | Feature | Owner | Acceptance Criteria | Notes |
|---|---------|-------|---------------------|-------|
| 1 | **Browser Promotion Engine** | Dev | • Detect installed browsers.<br>• Mark beta/secondary browsers as “prominent” in the OS UI.<br>• Persist state across reboots. | Uses OS APIs (Windows, macOS, Linux). |
| 2 | **Central Configuration Service** | Dev | • JSON/YAML config file.<br>• Supports per‑environment overrides.<br>• Hot‑reload on change. | Stored in `/etc/beta-browser-access/` or user‑home. |
| 3 | **CLI Tool** | Dev | • `beta-browser-access list` – list all browsers and status.<br>• `beta-browser-access promote <browser>` – promote a browser.<br>• `beta-browser-access demote <browser>` – demote a browser. | Built with Rust (cargo‑build). |
| 4 | **Telemetry & Feedback Hook** | Dev | • Emit events to Axentx telemetry pipeline (Kafka/PGVector).<br>• Capture usage metrics (promoted count, click‑through). | Uses existing `auto` dataset schema. |
| 5 | **Unit & Integration Tests** | QA | • ≥80 % coverage.<br>• CI pipeline passes on every PR. | Leverage `messages` dataset for test vectors. |
| 6 | **Documentation** | Docs | • README with install & usage.<br>• Quick‑start guide. | Markdown + example config. |
| 7 | **Packaging** | Ops | • Debian, RPM, Homebrew, Chocolatey packages.<br>• Docker image for CI. | Use `surrogate-1-harvest` repo as base. |

**MVP‑Critical**: Features 1‑4. They deliver the core value proposition – users can see and use beta browsers without manual configuration.

---

## 2. Phase 1 – “Feature Expansion”

| # | Theme | Feature | Owner | Acceptance Criteria |
|---|-------|---------|-------|---------------------|
| 1 | **Cross‑Platform UI** | System tray icon + context menu | UI | • Tray icon shows status.<br>• Menu lists browsers with promote/demote actions. |
| 2 | **Policy Engine** | Role‑based promotion rules | Dev | • Admin can define rules (e.g., “promote Chrome Beta to 70% of users”).<br>• Rules evaluated at startup and on config change. |
| 3 | **Analytics Dashboard** | Web UI (React) | Frontend | • Visualize promotion stats.<br>• Export CSV. |
| 4 | **Self‑Healing** | Auto‑rollback on failure | Dev | • Detect failed promotion and revert.<br>• Notify admin via email. |
| 5 | **Beta‑Browser Marketplace** | Integration with external repos | Dev | • Pull latest beta builds from GitHub releases.<br>• Auto‑install if not present. |
| 6 | **Security Hardening** | Signed binaries & sandboxing | Ops | • Verify binary signatures.<br>• Run in restricted user context. |

**Phase 1 Goal**: Deliver a polished, cross‑platform experience with policy control and analytics, enabling teams to manage beta browsers at scale.

---

## 3. Phase 2 – “Ecosystem Integration”

| # | Theme | Feature | Owner | Acceptance Criteria |
|---|-------|---------|-------|---------------------|
| 1 | **Axentx Product Sync** | Auto‑detect Axentx product usage | Dev | • Detect when a product launches.<br>• Auto‑promote recommended browsers. |
| 2 | **Feedback Loop** | In‑app feedback widget | UX | • Users can submit feedback directly.<br>• Feedback stored in PGVector. |
| 3 | **AI‑Driven Recommendations** | Use `instr-resp` dataset to suggest browsers | ML | • Model predicts optimal browser per user profile.<br>• A/B test results show 15 % higher engagement. |
| 4 | **Compliance & Auditing** | Log all promotion actions | Ops | • Immutable audit log.<br>• Export to SIEM. |
| 5 | **Internationalization** | Multi‑language support | Dev | • UI strings in 5 languages.<br>• Locale detection. |
| 6 | **Marketplace API** | Public API for 3rd‑party tools | Dev | • CRUD endpoints for browser bundles.<br>• OAuth2 auth. |

**Phase 2 Goal**: Embed beta‑browser‑access into the Axentx ecosystem, turning it into a central hub for browser testing, feedback, and AI‑powered recommendations.

---

## 4. Phase 3 – “Enterprise‑Ready & Scaling”

| # | Theme | Feature | Owner | Acceptance Criteria |
|---|-------|---------|-------|---------------------|
| 1 | **High‑Availability** | Distributed deployment (K8s) | Ops | • Zero‑downtime upgrades.<br>• Horizontal scaling. |
| 2 | **Advanced Policy Language** | DSL for complex rules | Dev | • Supports time‑based, demographic, and usage‑based conditions.<br>• Syntax validated by parser. |
| 3 | **Marketplace Marketplace** | Public browser repository | Dev | • Search, filter, and rate browser bundles.<br>• Community contributions. |
| 4 | **Compliance Certifications** | SOC2, ISO 27001 | Compliance | • Pass internal audit.<br>• External certification. |
| 5 | **Analytics & ML Ops** | Continuous model training | ML | • Retrain recommendation model weekly.<br>• Deploy via CI/CD. |
| 6 | **User‑Facing Portal** | Self‑service portal | Frontend | • Users can view and manage their promoted browsers.<br>• Export logs. |

**Phase 3 Goal**: Deliver a fully‑scalable, compliant, and feature‑rich platform that can be adopted by large enterprises and integrated into CI/CD pipelines.

---

## 5. Release Cadence

| Release | Target Date | Scope |
|---------|-------------|-------|
| **v0.1 (MVP)** | Q3 2026 | Features 1‑4 of MVP |
| **v1.0** | Q4 2026 | Phase 1 features + MVP |
| **v2.0** | Q2 2027 | Phase 2 features |
| **v3.0** | Q4 2027 | Phase 3 features |

All releases will follow the Axentx runbook: commit → CI → automated tests → staging → production. Feature flags will be used for gradual rollout of risky features.

---

## 6. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Promotion Adoption** | ≥70 % of beta browsers promoted | Telemetry |
| **Feedback Volume** | 10 % increase in user feedback | Feedback widget |
| **System Uptime** | 99.9 % | Monitoring |
| **Model Accuracy** | >0.85 precision | ML evaluation |
| **Security Incidents** | 0 | Incident logs |

---

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| OS API changes | High | Abstract API layer, maintain unit tests |
| User resistance to beta browsers | Medium | Provide clear opt‑in/out UI |
| Data privacy concerns | High | Enforce GDPR, anonymize telemetry |
| Model bias | Medium | Regular audits, diverse training data |

---

## 8. Dependencies

- **Axentx Runbook** – CI/CD, packaging, telemetry pipelines.
- **Existing Datasets** – `auto`, `instr-resp`, `messages` for telemetry and ML.
- **External Repos** – GitHub releases for beta browsers.
- **Infrastructure** – Kubernetes cluster, PostgreSQL, Kafka.

---

### Final Note

This roadmap is a living document. As we iterate, we will refine milestones, adjust timelines, and incorporate feedback from the product and engineering teams. The goal remains clear: deliver a robust, user‑centric tool that turns beta browsers into a competitive advantage for Axentx and its partners.
