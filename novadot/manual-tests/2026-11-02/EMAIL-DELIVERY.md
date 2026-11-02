# Novadot website email delivery test

Recorded: 2026-11-02T18:35:33.289858+00:00 (local date 2026-11-03, Asia/Kolkata).

The user explicitly authorised one labelled Contact test and one labelled Events test, and required Computer Use instead of Playwright. Both were submitted once using native browser controls and synthetic data. No website code, hosting configuration or mailbox permissions were changed.

| Form | Browser | Marker in message | Website result | Inbox result |
|---|---|---|---|---|
| Contact | Google Chrome | `ND-MAIL-20261102-CONTACT-01` | Enquiry submitted; fields cleared | User confirmed arrival exactly once |
| Events | Brave Browser | `ND-MAIL-20261102-EVENT-01` | Enquiry submitted; fields cleared | User confirmed arrival exactly once |

## Expected messages

- Recipient: `hello@novadot.co.uk`.
- Contact subject: `NovaDot website: project enquiry`.
- Events subject: `NovaDot website: event enquiry`.
- Test identity: `NovaDot Website Test`, organisation `NovaDot - authorised website QA`.
- Synthetic Reply-To: `website-test@example.com`; used for field verification only, not a real reply-delivery test.
- Both messages explicitly identify themselves as tests and request no real work, callback, attendance or booking.

## Observed browser feedback

### ND-MAIL-20261102-CONTACT-01

Observed at 2026-11-02T18:31:51.876618+00:00 UTC (recorded immediately after verifying the result).

> Enquiry submitted. Thank you — we will review your message and get back to you.

### ND-MAIL-20261102-EVENT-01

Observed at 2026-11-02T18:35:33.289858+00:00 UTC (recorded immediately after verifying the result).

> Enquiry submitted. Thank you — we will review your message and get back to you. This does not confirm a booking; suitability and availability must be agreed separately.

## User-confirmed result and limits

The website displayed success after each submit. At 2026-11-02T18:36:13.676181+00:00, the user confirmed: **“Both arrived once.”** Both delivery tests therefore pass on website feedback plus user-confirmed receipt and duplicate count. No mailbox was opened, delivery status API called, or additional test sent. Individual email field rendering and actual Reply-To headers were not independently inspected.

A prepared Events draft remains in Chrome and was not submitted. The accepted Events test was submitted in Brave after unrelated Chrome window switching. Do not submit the old draft or repeat either test ; delivery has already been confirmed.

Exact submitted fields and results are in [email-delivery.json](email-delivery.json). The dated folder and markers retain the UTC date used when planning these tests.
