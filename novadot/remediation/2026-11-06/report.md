# NovaDot website fixes and retest results

**Date:** 6 November 2026, Asia/Kolkata (commands and package timestamps use 5 November UTC).

**Result: all three agreed website fixes are implemented and verified locally. Production deployment is pending.** No production files, private configuration, databases or mailboxes were changed. No real enquiry emails were sent during these retests.

## What was fixed

| Finding | Change | Result |
|---|---|---|
| ND-DEP-001: dependency advisories | Updated Astro 7.2.2 to 7.4.6, Astro checker to 0.9.12, and compatible locked dependencies. Retained TypeScript 5.9.3. Node requirement is now >=22.23.4. | Fresh lockfile audit: **0 known vulnerabilities**, down from 11 (1 critical, 9 high, 1 moderate). Both build modes pass. |
| ND-HARD-001: permissive script policy | Finaliser hashes the exact inline script bytes across all 13 generated HTML pages, including noindex/error pages. Script `unsafe-inline` is removed. Event handlers, eval, base changes and objects are blocked; form destinations and framing are same-origin. Production permits the existing pinned analytics script URL. | **Passed locally:** browser blocking probes and normal interactions. Effective production Apache headers still need checking after deployment. |
| ND-OBS-002: live/source analytics difference | Earlier release records show the live tag was preserved by modifying generated HTML. Added its URL, SRI, public site ID and existing `/`, `/about`, `/contact` route allowlist to source configuration. Production emits the tag; review omits it. | **Reconciled in source:** generated-output validation checks exact attributes and one tag per production HTML page. The current public asset matched its SHA-384 integrity and returned CORS `*`. |

Existing inline styles remain permitted; removing them was not required to fix the script allowance. No new analytics routes or tracking behaviour were introduced. The public analytics asset was fetched to verify integration integrity only; its collection endpoint, stored data and service security were not assessed.

## Tests and evidence

| Check | Observed result | Evidence |
|---|---|---|
| Dependency advisory audit | Before: 11; after: 0. Point-in-time package advisory check, not proof of an attack-free website. | [Before](evidence/audit-before.json), [after](evidence/audit-after.json) |
| Source/logo validation | 26 source files and canonical logo passed in both modes. | [Review verification](evidence/verify-review.log), [production verification](evidence/verify-production-package.log) |
| PHP syntax/backend checks | All 51 passed with Microsoft calls mocked; no mail sent. | Same verification logs |
| Security regression suite | 5 tests passed, covering altered/injected scripts, noindex hash coverage, restrictive directives, analytics pin/count/build mode and Apache policy cardinality. | Same verification logs; test code in [source patch](source-changes.patch) |
| Astro and output | 34 files, zero errors/warnings/hints; both modes built and validated all 13 HTML routes and local links. Production has 11 indexable routes; case studies withheld and approved client logos retained. | Same verification logs |
| Chrome native Computer Use | Unapproved inline script, handler and eval blocked; same-origin probe executed. Both mock forms succeeded and reset. Diagnostic, architecture toggle, image dialog and responsive navigation worked. | [Browser observations](evidence/browser-checks.md), [sanitised mock requests](evidence/mock-form-requests.json) |
| Analytics integrity | Fresh live tag captured; public script HTTP 200 with matching SHA-384 and CORS header. No event submitted. | [Live tag](evidence/analytics-live-tag.json), [asset check](evidence/analytics-asset-check.json) |
| Independent source review | No material confirmed security/correctness defect. Requested browser and production checks were subsequently completed; deployment verification remains pending. | [Review record](evidence/review.md) |
| Preservation | 65 of 74 baseline files unchanged; nine intended files changed and three added. PHP handler, form implementation, page content, logos and publication switches preserved. | [Change manifest](evidence/source-change-manifest.json) |

Earlier actual Contact and Events deliveries and Events reply selection remain **passed** in the [email evidence](../../manual-tests/2026-11-02/EMAIL-DELIVERY.md). These local mock tests validate compatibility with the new build/CSP, not new mailbox delivery.

## Source and release

Source: `/Users/apple/git/novadot_website`, branch `agent/porcelain-ledger-website`, HEAD `6148cee25534a80cc039d02c6e9710fc1e743cae`. This checkout already contained substantial uncommitted work and has no remote. Changes remain in that checkout; the base commit alone cannot reproduce the release.

The [source patch](source-changes.patch) records this task's changes against its starting worktree, excluding the browser fixture. The [final fixture](serve-ui.mjs) belongs at `tests/forms/serve-ui.mjs`; its original and final hashes are recorded in the manifest. A byte copy of its pre-edit version was unavailable, so it is supplied as a separate replacement rather than an invented diff. Applying the patch requires the recorded starting files, not a clean checkout of HEAD. Do not apply it again to the already-updated local source. An isolated patch-application check confirms its resulting files match the manifest.

Frozen package:

`/Users/apple/git/novadot_website/.release/2026-11-05T18-38-08-749Z/novadot-production.tar.gz`

SHA-256: `e38510554fb33e90132c3e48e8b4fbde91d2d96d4ffd1f39c7d08d2c9ba09b8e`

The [release manifest](evidence/release-manifest.json) identifies every packaged file. The [generated Apache rules](evidence/production.htaccess) show the candidate CSP. Packaging ran production verification immediately beforehand and performed no upload.

## Remaining step and owner

The website owner must explicitly authorise production deployment under the existing publication/legal/privacy/proof/contact gates. Then the release operator should verify the current live baseline, preserve rollback, deploy the generated HTML/assets and `.htaccess` together, and check effective live headers, analytics loading and normal interactions. Do not patch generated HTML afterwards: its scripts and policy hashes must stay matched. The unrelated organisation assessments remain separate.
