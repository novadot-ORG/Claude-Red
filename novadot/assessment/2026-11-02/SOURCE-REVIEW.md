# Novadot website — source and dependency review

Date: 2026-11-02. Source: `/Users/apple/git/novadot_website`, explicitly supplied by the user. Branch: `agent/porcelain-ledger-website`; HEAD: `6148cee25534a80cc039d02c6e9710fc1e743cae`.

The source already contained tracked changes and untracked implementation. This review examined the current working files, whose [SHA-256 manifest](evidence/source-manifest.json) identifies the exact versions; HEAD alone does not reproduce them. Existing implementation and dependencies were preserved. No website fixes, production changes, private credential access, SSH connections or live mail submissions were made. The local handoff was updated separately.

## Result and priority

1. **Prioritise dependency maintenance:** the lockfile audit flags 11 packages, including a critical Astro advisory. Package vulnerability presence is confirmed; live website exploitability is not established.
2. **Harden CSP:** the live inline-script allowance is also present in `public/.htaccess:7`. Follow [ND-HARD-001](ASSESSMENT.md#nd-hard-001--content-security-policy-can-be-tightened).
3. **Reconcile source with production:** live pages include an analytics script absent from the supplied layout/build source; do not assume rebuilding this checkout exactly reproduces production.
4. **Complete delivery verification later:** form preparation returned HTTP 200 with a browser user agent. All 51 mocked backend checks passed, but no email was sent and inbox receipt remains unverified.

## ND-DEP-001 — Locked development dependencies have published advisories

**Status:** Confirmed dependency finding. **Priority:** Address before the next release. **Severity:** Upstream package ratings below; no production exploit severity or application CVSS assigned.

`npm audit --package-lock-only --ignore-scripts --json` returned 11 flagged packages: one critical, nine high and one moderate. This count is packages in npm's severity buckets, not 11 independently demonstrated website vulnerabilities. Every flagged package has the lockfile's `dev` marker. Development dependencies still affect build/development safety, and the marker alone does not prove that no dependency code reaches generated browser assets.

| Locked package | Version | npm severity |
|---|---|---|
| astro | 7.2.2 | Critical |
| devalue | 5.9.0 | High |
| fast-uri | 3.1.5 | High |
| js-yaml | 4.3.1 | High |
| sharp | 0.35.3 | High |
| smol-toml | 1.8.0 | Moderate |
| source-map-js | 1.2.1 | High |
| svgo | 4.0.2 | High |
| undici | 8.10.0 | High |
| vite | 8.2.1 | High |
| zod | 4.4.3 | High |

**Applicability:** Astro's [AVIF image optimisation advisory](https://github.com/withastro/astro/security/advisories/GHSA-26w7-cxv4-gfx2) affects versions before 7.2.8 when an attacker can make Astro process an untrusted AVIF image. The supplied configuration uses `output: 'static'`; no `astro:assets` image-service use or runtime Astro server was identified in the reviewed source. A remotely reachable image-processing exploit on this website was not demonstrated. The [JSX/MDX advisory](https://github.com/advisories/GHSA-98hj-9722-w3j8) requires untrusted data in particular script/style rendering contexts; no MDX integration or JSX/MDX source was found here. These observations narrow known paths; they do not clear every transitive advisory.

**Evidence:** [complete npm audit](evidence/dependency-audit.json), [audit command/time](evidence/dependency-audit-meta.json), [locked versions and severity summary](evidence/dependency-summary.json), and source manifest for `package.json`, `package-lock.json` and `astro.config.mjs`. npm reports a fix available for each entry. Only the noted Astro advisories received contextual source triage in this pass; remaining records require their own applicability review.

**Remediation:** Update Astro and affected transitive dependencies to compatible patched versions in an isolated change, review the resulting lockfile, rerun the audit and full verification, and check generated site/form behaviour. Astro 7.2.8 fixes the cited AVIF issue but does not resolve every newer advisory in this audit; do not treat it as a complete target version. No `npm audit fix`, installation or lockfile modification was performed. A production deployment remains a separate action subject to the website's publication gates.

## ND-OBS-002 — Supplied source does not fully describe live analytics

**Classification:** Release reproducibility/documentation follow-up, not a demonstrated exploit.

All 11 captured pages include `https://scanner.novadot.co.uk/novadot-analytics.v1.072ff0e7fc53.js` with integrity metadata. The supplied `src/layouts/BaseLayout.astro` has no corresponding analytics include, and a targeted search of `src/`, `scripts/` and `config/` found no scanner/analytics reference. `public/.htaccess:7` allows the scanner origin, while `README.md:100` says no analytics are included. This may reflect another build/deployment step or source drift; the mechanism is unverified.

**Action:** Identify and document the authoritative source/build step for the live analytics tag before rebuilding or changing CSP. Verify the intended data collection and integrity policy separately if the service is added to scope. Do not classify the public site identifier as a private key merely because it looks token-like. The scanner service was not fetched or tested.

## Form and browser-code review

An independent read-only security review of `public/api/enquiry.php` and `tests/forms/backend.php` found no material confirmed vulnerability in that bounded scope. Focused main-thread inspection and existing tests support these observations:

- `enquiry.php:45–90`: signed expiring form tokens, exact host/origin checks, JSON-only POSTs and a request-size limit. A public token endpoint is expected for this anonymous form and is not an authentication bypass.
- `enquiry.php:145–170`: fixed recipient/subject, structured Graph JSON, a plain-text email body and TLS-verified HTTPS transport. No demonstrated arbitrary-recipient, mail-header injection or request-controlled destination path was found.
- `enquiry.php:198–280`: nonblocking global lock, atomic state replacement, keyed hashes and a persisted pending record before sending. Existing tests exercise duplicate/conflicting requests and conservative handling after uncertain delivery.
- `enquiry.php:288–330`: generic external errors and cache restrictions; the CLI test include does not invoke the live request entrypoint.
- `src/scripts/enquiry-form.ts`: feedback uses `textContent`, enquiry data is kept in memory, and uncertain attempts reuse their identifier instead of blindly resending.
- `src/pages/contact.astro:199–203`: query text goes into a textarea value. `ProblemDiagnostic.astro:331` builds markup from bundled constant choices. `BaseLayout.astro:57` serialises source-owned site metadata. No attacker-controlled route into these HTML-rendering contexts was established.

These are source observations, not verification of the deployed PHP bytes or private configuration. Remaining gaps include real multiprocess concurrency, every quota/expiry boundary, HTTP entrypoint serialization, actual proxy-to-`REMOTE_ADDR` mapping, Microsoft mailbox permission scope and end-to-end delivery. Origin checks and public tokens constrain browser requests but do not authenticate arbitrary non-browser clients; abuse resistance also depends on rate limits and hosting controls.

## Validation performed

| Check | Result | Evidence |
|---|---|---|
| PHP syntax and isolated backend tests | 51 checks passed; Microsoft transport mocked; no mail sent | [backend output](evidence/source-backend-tests.txt) |
| Source validation | 26 source files and canonical logo passed | [validation output](evidence/source-validation.txt) |
| Astro checking | 34 files; zero errors, warnings or hints | [typecheck output](evidence/source-typecheck.txt) |
| Dependency audit | 11 flagged packages; audit exit 1 reflects findings | [audit metadata](evidence/dependency-audit-meta.json) |
| Public preparation GET, browser user agent | HTTP 200, nonempty token shape, no-store headers | [request](evidence/enquiry-api-browser-agent.json) and [shape](evidence/enquiry-api-browser-agent-shape.json) |

Commands and exit codes are saved in [source-checks.json](evidence/source-checks.json). Saved diagnostic text has trailing whitespace normalized. The full build/verify chain was not run: no website code was changed, and generated-build validation is required again when remediation changes are made. The test fixture used synthetic credentials in a temporary `.release/form-tests-*` directory and cleaned up after itself.

Next owner action: choose a dependency/CSP remediation change, reconcile the analytics build source, and arrange a controlled delivery test. Preserve the current source worktree and the historical assessment evidence.
