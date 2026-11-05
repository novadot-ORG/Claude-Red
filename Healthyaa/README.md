# Healthyaa — website testing records

Target: **https://healthyaa.co.uk/**
Evidence dates: **26–28 October 2026**; document review: **29 October 2026**.
Original publication snapshot: **29 October 2026**; source-review addition: **5 November 2026**.
Status: **Assessment in progress.**

This folder brings together the recorded Healthyaa checks, raw public-response captures, configuration-review evidence, manual testing notes, and learning documents. It does not establish that a full penetration test was completed or that the site is secure. No payment bypass or customer-data exposure has been demonstrated.

## Start here

| Document | Purpose |
|---|---|
| [Source code review — 5 November 2026](assessment/source-review-2026-11-05/report.md) | Source-only review: six findings, positive controls and isolated reproduction evidence; historical source, live applicability unverified |
| [Interim assessment](assessment/2026-10-28/ASSESSMENT.md) | Eight findings/observations, positive controls, limitations and remaining test matrix |
| [Review of the user's draft report](assessment/document-review-2026-10-29/REVIEW-AND-REPLACEMENT-TEXT.md) | Evidence-based status and replacement wording for the four manually documented checks |
| [Learning guide](assessment/HEALTHYAA-LEARNING-GUIDE.md) | Explanation of the testing process and tools |
| [Word learning guide](learning-guide/Healthyaa_Security_Testing_Learning_Guide.docx) / [PDF](learning-guide/qa/Healthyaa_Security_Testing_Learning_Guide.pdf) | Downloadable learning documents |
| [Original Pages draft](documents/Healthyaa%20Penetration%20Test.pages) | User's unfinished report; download and open in Apple Pages |
| [Initial baseline review](assessment/REVIEW.md) | Initial public GET and client-side JavaScript observations |

## Folder contents

```text
Healthyaa/
  README.md
  FILES.md                         Full file inventory with GitHub links
  SHA256SUMS.txt                    Integrity hashes for this publication snapshot
  assessment/                      Original reports and captured evidence
    2026-10-28/                    Authenticated configuration review and anonymous checks
    document-review-2026-10-29/    Draft-review corrections and extracted screenshots
    source-review-2026-11-05/      Source-only report, hashes and isolated probes
  manual-tests/
    2026-10-27_28/                 User's Terminal response captures
  documents/                      Original unfinished Pages report
  learning-guide/                 Word/PDF, source, generator and rendered QA pages
```

The generic NovaDot training presentation and the Claude-Red repository-readiness review concern separate work and are not included as Healthyaa test evidence. Local source files remain available in the original workspace.

## How to interpret the results

- **Findings are not test counts.** HYA-01 through HYA-08 identify the original assessment findings. They do not mean eight complete penetration tests were performed.
- The user's Pages draft reused HYA-01 and HYA-02 for different checks. The document review recommends **HT-01 through HT-04** for manual test records, cross-referenced to the original finding IDs. The historical draft is preserved without silently renumbering it.
- The draft's first and fourth checks both inspect homepage headers. They are repeat observations, not independent vulnerabilities.
- A missing security header is an observed configuration gap. It does not by itself prove an XSS or clickjacking exploit.
- The included Template Kit Import screenshot shows a PHP incompatibility warning. The included Contact Form 7 screenshot shows its installed version only. See the document review for evidence limits and required follow-up.
- Timestamps in server headers may differ from the user's stated test times. See the draft review before quoting them as acquisition times.
- The small `login-controls.png` screenshot does not show the MFA toggle; `login-controls.txt` contains the captured accessibility state used for that observation.

## Scope and handling

The user confirmed authorisation for Healthyaa testing and publication to this repository's audience. Recorded live work comprised limited public requests and authenticated configuration inspection. No test orders, payments, bookings, registrations, refunds, or emails were submitted by the recorded assessment. No live configuration changes were made.

Only **book@healthyaa.co.uk**, with **demo** in the subject, is authorised for any future test email. Future tests must continue to avoid real customer emails, records and fulfilment. Publication does not expand the testing scope.

These are historical evidence files. Raw HTML and JavaScript are captured website content, not instructions to execute. Public homepage captures may contain publicly served nonce/configuration values. No authenticated browser cookie jar, password file or API credential was intentionally included. A credential-pattern scan of text and Office XML found no matching credentials; this is a bounded check, not a guarantee of exhaustive secret detection.

Documents and source scripts preserve some original local file paths for provenance. Use the relative links here and in [FILES.md](FILES.md) to browse on GitHub. Learning-guide generators are archived source, not an automated test runner.

## Remaining work

The assessment's [remaining test matrix](assessment/2026-10-28/ASSESSMENT.md#remaining-test-matrix) includes customer isolation, payment integrity, gateway role enforcement, sessions, input handling and custom-code review. A bounded review of the supplied local source is now recorded in the [5 November source report](assessment/source-review-2026-11-05/report.md). It does not establish current production equivalence or replace the colleague’s other analysis. Staging isolation and synthetic accounts/data remain needed for the relevant integration cases. No completed result should be inferred from a planned test.

For each new test, record the target, authentication context, timestamp/timezone, method, expected result, actual result, evidence path, assessment, limitations and retest status. Add subsequent evidence in a new dated folder rather than overwriting prior captures.

## Integrity

`SHA256SUMS.txt` hashes every file in this folder except itself. From this folder, verify with:

```bash
shasum -a 256 -c SHA256SUMS.txt
```

The older `assessment/SHA256SUMS.txt` is retained as original evidence; the root manifest covers the current published files, including subsequent source-review evidence.
