# NovaDot website test report

**Report updated:** 4 November 2026  
**Testing dates:** 2–3 November 2026 (Asia/Kolkata)  
**Website:** https://novadot.co.uk/  
**Scope:** Public website, supplied Astro/TypeScript and PHP source, and Contact/Events email workflows.

## Overall result

**The checks listed as passed below succeeded. Three items remain open for improvement or investigation.** The agreed website review is complete; fixes and checks after those fixes are still pending.

Both Contact and Events test emails arrived exactly once, as confirmed by the user. The supplied screenshots show the expected message contents. Clicking Reply on the Events message selected the visitor’s submitted email address correctly.

The open items are dependency updates, a tighter browser security policy, and explaining a difference between the live website and its supplied source. No website code or hosting settings were changed during testing. The user has deferred fixes until after the broader NovaDot assessment.

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
| Run Astro code checks | **Passed** | 34 files checked with zero errors, warnings or hints. A full production build was not run. |
| Review enquiry handling and selected browser code | **Reviewed; no confirmed vulnerability found in this scope** | Reviewed controls include form tokens, input/request restrictions, a fixed mail recipient, duplicate handling and safe display of feedback. This was a bounded review, not exhaustive attack testing. |
| Check dependency versions for published advisories | **Needs updates and review** | The recorded audit flagged 11 packages. See item 1 below. |
| Review Content Security Policy (CSP) | **Needs tightening** | The policy allows inline scripts and leaves some restrictions unset. See item 2 below. |
| Compare live analytics with the supplied source | **Needs investigation** | The live website includes an analytics script absent from the reviewed layout/build source. See item 3 below. |

Public and source results: [public assessment](assessment/2026-11-02/ASSESSMENT.md) and [source review](assessment/2026-11-02/SOURCE-REVIEW.md). Email results: [delivery and reply report](manual-tests/2026-11-02/EMAIL-DELIVERY.md).

## What needs tightening

| Open item | Why it matters | Required action | How to confirm completion |
|---|---|---|---|
| **1. Dependencies — ND-DEP-001** | The recorded audit flagged 11 packages: one critical, nine high and one moderate by upstream package ratings. These are package findings; exploitation of the live website was not demonstrated. | Review applicability and update Astro and affected dependencies to compatible patched versions before the next release. | Rerun the audit, code checks, backend tests and full build; check site and form behaviour. Review any remaining advisory individually. |
| **2. Browser security policy — ND-HARD-001** | The current CSP allows inline scripts and lacks explicit restrictions on page base URLs and form destinations. This is a **low-severity hardening gap**; no script-injection attack was demonstrated. | Tighten the policy while accommodating legitimate scripts and required services. | Test the candidate policy before enforcement; verify navigation, diagnostics and forms still work and unapproved inline scripts are blocked. |
| **3. Live/source analytics difference — ND-OBS-002** | Rebuilding the supplied checkout may not reproduce the live website because the analytics inclusion is unexplained. | Identify and document where the analytics script is added and which source/build process is authoritative. | Compare the intended build output with the deployed pages and resolve the documentation difference. |

All three items remain **open**. They are not marked fixed merely because the review is complete.

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

Continue the broader NovaDot assessment with an asset and access inventory. Keep the three website actions open for the agreed remediation phase, then record the fixes and their retest results here alongside the detailed assessments. Preserve the dated evidence so readers can distinguish the original findings from later changes.
