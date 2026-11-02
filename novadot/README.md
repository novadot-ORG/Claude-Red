# Novadot client testing

Client workspace on `Client-Website-Test`. Follow the [client testing workflow](../CLIENT-WEBSITE-TESTS.md).

## Scope and status

- **Status:** Initial public/source reviews complete. Two authorised email tests passed: website success and user-confirmed receipt exactly once each. Remediation remains.
- **Target:** Public website `https://novadot.co.uk/`, supplied by the user, who identified themselves as a Novadot employee. User describes the frontend as Astro/TypeScript.
- **Scope used:** Initial public pages, linked first-party JavaScript, HTTPS/headers, GET-only enquiry preparation, local source review and isolated mocked tests; subsequently one user-authorised Contact submission and one Events submission through native Computer Use. No payload injection, load testing or website implementation/hosting changes.
- **Source:** User supplied `/Users/apple/git/novadot_website`; reviewed its existing dirty worktree on `agent/porcelain-ledger-website`, HEAD `6148cee25534a80cc039d02c6e9710fc1e743cae`. File hashes are recorded in the assessment.
- **Other services:** `scanner.novadot.co.uk` was identified in markup but not tested; private hosting/Microsoft configuration was not accessed.
- **Testing window and access:** Public unauthenticated observations and local checks on 2026-11-02. Per-request/check timestamps are retained in evidence; broader testing arrangements remain pending.
- **Skill source:** Selected guidance read from `codex/openai-compatibility` at `32c3386c8c72d4120563bfbf2fed2718d9ff840f`; no merge or installation performed.

## Records

Keep all Novadot-specific work in this folder. Create these directories when needed:

- `assessment/YYYY-MM-DD/` — assessment notes, findings and evidence.
- `manual-tests/YYYY-MM-DD/` — test cases and observed results.
- `documents/` — reviewed reports and deliverables.

- [2026-11-02 public assessment](assessment/2026-11-02/ASSESSMENT.md): 11 public pages and four JavaScript assets reviewed; CSP hardening confirmed. Initial Python-user-agent 403 responses resolved to HTTP 200 with a browser user agent; no outage established.
- [2026-11-02 source review](assessment/2026-11-02/SOURCE-REVIEW.md): 51 mocked backend checks and Astro checking passed; dependency audit flags 11 packages. Production exploitability is not established. Live/source analytics differences require reconciliation.
- [Email delivery tests](manual-tests/2026-11-02/EMAIL-DELIVERY.md): Contact and Events each showed success after one submission. The user confirmed each email arrived exactly once; received-email screenshots verify the visible message contents, and Events reply-recipient selection is verified. Do not resend either test or submit the old Chrome Events draft.
- [Evidence summary](assessment/2026-11-02/evidence/baseline-summary.json) and [evidence checksums](assessment/2026-11-02/SHA256SUMS.txt).

Preserve historical results and distinguish retests from the original assessment.

## Next step

Prioritise a reviewed dependency update and CSP hardening, and reconcile the analytics build source. Keep credentials and sensitive customer data out of Git. No website fixes or deployment were performed during this assessment.
