# Novadot client testing

Client workspace on `Client-Website-Test`. Follow the [client testing workflow](../CLIENT-WEBSITE-TESTS.md).

## Scope and status

- **Status:** Initial read-only black-box baseline completed on 2026-11-02; follow-up remains.
- **Target:** Public website `https://novadot.co.uk/`, supplied by the user, who identified themselves as a Novadot employee. User describes the frontend as Astro/TypeScript.
- **Scope used:** Public pages, linked first-party JavaScript, HTTPS/headers and GET-only enquiry preparation checks. No form submissions, payload injection, load testing or source/hosting changes.
- **Other services:** `scanner.novadot.co.uk` was identified in markup but not tested; source repositories and backend/hosting access have not been supplied.
- **Testing window and access:** Public unauthenticated observations on 2026-11-02, approximately 18:07–18:10 UTC. Broader testing arrangements remain pending.
- **Skill source:** Selected guidance read from `codex/openai-compatibility` at `32c3386c8c72d4120563bfbf2fed2718d9ff840f`; no merge or installation performed.

## Records

Keep all Novadot-specific work in this folder. Create these directories when needed:

- `assessment/YYYY-MM-DD/` — assessment notes, findings and evidence.
- `manual-tests/YYYY-MM-DD/` — test cases and observed results.
- `documents/` — reviewed reports and deliverables.

- [2026-11-02 initial assessment](assessment/2026-11-02/ASSESSMENT.md): 11 public pages and four JavaScript assets reviewed; CSP hardening and enquiry preparation HTTP 403 observations recorded with limitations.
- [Evidence summary](assessment/2026-11-02/evidence/baseline-summary.json) and [evidence checksums](assessment/2026-11-02/SHA256SUMS.txt).

Preserve historical results and distinguish retests from the original assessment.

## Next step

Obtain the website source repository, confirm whether it contains `api/enquiry.php`, and investigate the enquiry preparation 403 with browser/server evidence. Plan any submission tests against agreed test data and a test recipient or staging environment. Keep credentials and sensitive customer data out of Git.
