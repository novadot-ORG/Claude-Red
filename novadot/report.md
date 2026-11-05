# NovaDot website test report

**Report updated:** 6 November 2026

**Testing dates:** 2–3 November 2026; remediation and retests 5–6 November 2026 (Asia/Kolkata)

**Website:** https://novadot.co.uk/

**Scope:** Public website, supplied Astro/TypeScript and PHP source, and Contact/Events email workflows.

## Overall result

**The three website findings have been addressed in the local source and passed the checks below. Production deployment and live verification are pending.** The original assessment and email evidence remain valid for their recorded scope.

Both Contact and Events test emails arrived exactly once, as confirmed by the user. The supplied screenshots show the expected message contents. Clicking Reply on the Events message selected the visitor’s submitted email address correctly.

The user subsequently authorised the website fixes. Astro and affected dependencies were updated, the browser security policy now uses exact script hashes, and the existing analytics integration is generated from source. Hosting settings have not been changed by this remediation. See the [remediation report and evidence](remediation/2026-11-06/report.md).

“Passed” applies to the specific check performed. It does not mean every possible attack or configuration has been tested.

## What was tested and what happened

| Test | Result | What this means |
|---|---|---|
| Open the 11 public pages listed in the sitemap | **Passed** | All 11 returned successful responses. Hidden or unlisted pages were not searched for. |
| Redirect the HTTP homepage to HTTPS | **Passed** | The homepage redirected to the encrypted HTTPS address. |
| Check the HTTPS certificate and make an encrypted connection | **Passed** | Certificate hostname/chain validation succeeded; the connection used TLS 1.3. Older protocol acceptance was not tested. |
| Check standard browser protection headers | **Passed for sampled pages** | All 11 HTML pages supplied HTTPS enforcement, framing restrictions and other protective headers. The separate content security policy improvement is listed below. |
| Look for unencrypted resource links in page markup | **Passed for inspected markup** | No HTTP script, stylesheet, image or iframe links were found. Dynamically loaded resources were not fully inspected. |
| Prepare an enquiry using a browser-style request | **Passed** | The enquiry endpoint returned HTTP 200 and the expected form token. Earlier 403 responses depended on request context; no endpoint outage was established. |
| Submit one Contact enquiry through the website | **Passed** | Chrome displayed “Enquiry submitted” and cleared the fields. The user confirmed the email arrived once. |
| Submit one Events enquiry through the website | **Passed** | Brave displayed “Enquiry submitted” and cleared the fields. The user confirmed the email arrived once. |
| Check the received email contents | **Passed** | User screenshots show the expected subjects, test details and privacy acknowledgements for both messages. |
| Click Reply on the Events email | **Passed** | Outlook selected the submitted visitor address, confirmed by the expanded recipient screenshot. |
| Run the isolated PHP backend checks | **Passed** | All 51 checks passed. These used a simulated Microsoft mail service; actual delivery was checked separately above. |
| Validate source files and the logo | **Passed** | The existing validator passed for 26 source files and the canonical logo. |
| Run Astro code checks | **Passed** | 34 files checked with zero errors, warnings or hints. Review and production builds now also pass (13 HTML routes each). |
| Review enquiry handling and selected browser code | **Reviewed; no confirmed vulnerability found in this scope** | Reviewed controls include form tokens, input/request restrictions, a fixed mail recipient, duplicate handling and safe display of feedback. This was a bounded review, not exhaustive attack testing. |
| Check dependency versions for published advisories | **Passed after local update** | The fresh audit fell from 11 flagged packages to zero. This is a point-in-time advisory check. |
| Review Content Security Policy (CSP) | **Local checks passed; deployment pending** | Generated hashes authorise known scripts. Chrome blocked unapproved inline scripts, event handlers and eval; forms and interactive controls worked. |
| Compare live analytics with the supplied source | **Reconciled in source; deployment pending** | Earlier deployments added the tag to generated HTML. Production builds now emit the existing pinned tag; review builds omit it. Public asset SRI matched. |

Public and source results: [public assessment](assessment/2026-11-02/ASSESSMENT.md) and [source review](assessment/2026-11-02/SOURCE-REVIEW.md). Email results: [delivery and reply report](manual-tests/2026-11-02/EMAIL-DELIVERY.md).

## Fixes and remaining actions

| Item | What changed | Result | Remaining action |
|---|---|---|---|
| **Dependencies — ND-DEP-001** | Astro 7.2.2 → 7.4.6; compatible transitive updates; Astro checker 0.9.12. Minimum Node 22.23.4. | **Local fix verified:** zero audit findings; full review and production checks passed. | Use the updated toolchain and deploy the verified release. |
| **Browser policy — ND-HARD-001** | Exact inline-script hashes generated from all HTML; no script `unsafe-inline` or `unsafe-eval`; explicit base, object, form and framing restrictions. | **Local fix verified:** negative CSP probes, both mock forms, navigation, diagnostic and architecture controls passed in Chrome through native Computer Use. | Deploy HTML and generated `.htaccess` together, then confirm the effective live header and normal browser behaviour. Existing inline styles remain allowed. |
| **Analytics source — ND-OBS-002** | Existing live URL, integrity and route allowlist moved into production build configuration. No new tracking routes. | **Source discrepancy resolved:** production validates one pinned tag per HTML page; review excludes it; downloaded public script matched its integrity value. | Verify the deployed tag and browser loading after release. The analytics service itself is outside this security assessment. |

The release package is prepared but **has not been uploaded or deployed**. These are local remediation results, not claims that the live website already has the new policy. The [detailed report](remediation/2026-11-06/report.md) identifies the package, checks, source changes and evidence.

## Email evidence and clarification

- [Contact email received](manual-tests/2026-11-02/evidence/contact-received.png).
- [Events email received](manual-tests/2026-11-02/evidence/event-received.png).
- [Events reply composer](manual-tests/2026-11-02/evidence/event-reply-composer.png) and [confirmed reply address](manual-tests/2026-11-02/evidence/event-reply-recipient.png).

The user confirmed **“Both arrived once.”** The website sends from and to `hello@novadot.co.uk` and saves a sent copy. Seeing the message in both Sent and Inbox is expected for that arrangement and does not establish a duplicate submission. A separate sending mailbox is optional organisation work, not a fix required by these test results.

Contact reply selection was not separately exercised. The Events reply check verified the selected destination; sending a reply to the synthetic test address was not required. **No repeat of the completed delivery tests is needed.**

## What this report does not cover

OVH servers, Microsoft 365 tenant security, Git organisation settings, Confluence, the password manager, WireGuard, employee devices, backups and client-owned servers have **not yet been assessed** under this work. Website email delivery passing does not establish that those systems are secure.

The website review also did not establish exhaustive concurrency/rate-limit behaviour, server/proxy configuration, Microsoft application permission scope, email authentication headers, or the separate analytics service’s security. No load testing or live attack-payload testing was performed.

## Next step

Obtain explicit production deployment instruction for the prepared release, check the publication gates and backup/rollback plan, then verify live headers, assets and browser behaviour. The previously completed real email tests do not need to be repeated for these changes. Broader organisation assessment can continue separately with an asset and access inventory.
