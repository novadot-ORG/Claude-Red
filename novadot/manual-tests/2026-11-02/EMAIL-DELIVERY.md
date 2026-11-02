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

The website displayed success after each submit. At 2026-11-02T18:36:13.676181+00:00, the user confirmed: **“Both arrived once.”** Both delivery tests therefore pass on website feedback plus user-confirmed receipt and duplicate count. No mailbox was opened, delivery status API called, or additional test sent. The user subsequently supplied both received-email screenshots. Their visible subjects, sender, name, email, organisation, message markers, field contents and privacy acknowledgements match the tests. The later Events reply screenshots verify recipient selection as `website-test@example.com` and show the original recipient as `hello@novadot.co.uk` in the quoted message.

A prepared Events draft remains in Chrome and was not submitted. The accepted Events test was submitted in Brave after unrelated Chrome window switching. Do not submit the old draft or repeat either test; delivery has already been confirmed.

Exact submitted fields and results are in [email-delivery.json](email-delivery.json). The dated folder and markers retain the UTC date used when planning these tests.

## Received-email screenshot evidence

The user explicitly supplied these screenshots as assessment evidence. Copies are unmodified; [SHA256SUMS.txt](SHA256SUMS.txt) records their hashes.

| Form | Screenshot | Message reference | Displayed received time |
|---|---|---|---|
| Contact | [Received Contact email](evidence/contact-received.png) | `582738aa-3551-40c3-ad76-43348a5d207f` | Today at 00:01 |
| Events | [Received Events email](evidence/event-received.png) | `504253dd-1979-4635-9643-600fc6fb5351` | Today at 00:04 |

Both show sender `Hello <hello@novadot.co.uk>` and recipient display label `Hello`. The Contact email includes the expected optional-field “Not provided” values. The Events email includes the submitted test-only attendee/date text and the selected values `attend` and `meeting`. The screenshot times are displayed mailbox times; full timestamp headers are not provided. Duplicate counts remain based on the user's confirmation. Raw authentication headers were not assessed.

## Events reply-address check — passed

The user clicked Reply on the received Events email. The [reply composer](evidence/event-reply-composer.png) selects **NovaDot Website Test**, and the [expanded recipient card](evidence/event-reply-recipient.png) confirms **website-test@example.com**, exactly matching the submitted visitor email. This verifies the Events reply destination in Outlook for Mac. The composer also shows the original sender and recipient as `hello@novadot.co.uk` in the quoted message.

This is an address-selection check; delivery of a reply to the synthetic address was not tested or required. Contact reply selection was not separately exercised. The two new screenshots are preserved unmodified and included in the evidence checksums.
