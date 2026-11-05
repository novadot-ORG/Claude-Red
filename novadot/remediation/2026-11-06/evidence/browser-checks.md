# Native Chrome browser observations

6 November 2026 Asia/Kolkata, against review output at `http://127.0.0.1:4340`.
Control: native Google Chrome application through Computer Use accessibility actions; no Playwright. This is an observed-result record, not a saved browser trace or screenshot archive.

The local fixture used the exact CSP read from the generated review `.htaccess`; Astro preview was not used for header enforcement. Production analytics was absent from this review build. Server mock records are in `mock-form-requests.json`.

| Interaction | Visible result |
|---|---|
| Open `/__qa/csp` | `PASS: unapproved inline script, event handler and eval blocked; same-origin script ran.` |
| Contact: enter synthetic required fields and consent, submit | `Enquiry submitted`; fields cleared. One accepted mock POST, HTTP 202. |
| Follow Events navigation link | Events page rendered and submit control initialised. |
| Events: submit while email remained empty during native input | `Check your enquiry` and valid-email guidance; no POST recorded. |
| Complete synthetic Events email and submit | `Enquiry submitted` with booking qualification; fields and consent reset. One accepted mock POST, HTTP 202. |
| Homepage diagnostic: Business Systems → Spreadsheets | Step 2, then Step 3; `Understand the workflow first` recommendation appeared. |
| Software services architecture toggle | Before unselected, After selected; connected system content replaced silos. |
| Review case-study image enlargement | Image dialog opened with expected image/caption; Close dismissed it. |
| Responsive navigation at 175% zoom | Menu opened, exposing service and contact links; Close dismissed it. Zoom restored to 100%. |
| Final CSP probe | Same PASS result. |

Mock summary: two preparation token requests, exactly two accepted POSTs (one contact, one event), zero unknown fields, zero unexpected native submissions. No credentials, PHP mail execution or real email delivery were involved. Server stopped after the browser checks; production packaging was validated separately.
