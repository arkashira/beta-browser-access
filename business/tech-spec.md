`tech-spec.md` generated at `/tmp/tech-spec.md` for **beta-browser-access** (v1).

Key engineering opinions baked in:

- **Go static-binary agent, not Electron** — IT will not push a 150 MB Node runtime to 10k seats; ~8 MB single binary deploys via existing MDM (Intune/Jamf/GPO).
- **Signed (Ed25519) immutable manifests** — the agent's `set_default` capability is the highest-risk action in the product, so manifest integrity + pinned-key verification is the core security control; rollback = re-point version, no redeploy.
- **`events` table as the north-star** — directly measures the hypothesis ("prominently displayed → more feedback") via `prompt_shown`/`launch`/`feedback_opened`, and doubles as the analytics source so there's no third-party tracker to trip enterprise data-residency reviews.
- **WorkOS SSO/SCIM as the monetization gate** — free until enterprise auth, which is exactly where this buyer pays.
- **Code-signing (Authenticode + notarization) flagged non-negotiable for v1** — unsigned agents get blocked by endpoint protection, killing adoption silently.

Cost at 0–100 tenants ≈ $0/mo (Railway + Neon + Upstash + R2 zero-egress).

Note: the file previously held a spec for a different product (`glucose-sentry`); I overwrote it since the task targets this repo.