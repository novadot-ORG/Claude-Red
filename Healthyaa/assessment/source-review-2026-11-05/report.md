# Healthyaa — source code security review

**Review date:** 5 November 2026 · **Status:** Completed for the bounded source scope below; remediation pending.

**Source supplied:** `/Users/apple/git/healthyaa-wordpress/public_html/`

**Report repository/branch:** `Claude-Red` / `Client-Website-Test`.

## Result in plain language

**The reviewed code needs tightening. Six source-level findings were identified: four medium and two low.** The main concerns are protected content being available to the public AI assistant, analytics records being matched without proving ownership, and sensitive URL values being retained in analytics.

Several controls worked in isolated checks, including the sandbox gateway's administrator restriction, analytics API token validation and delivery-fee validation. These positive results do not cancel the findings.

This review covers source code only. Your colleague's other analysis remains separate. No live requests, accounts, orders, payments, bookings or emails were created or changed. No source fixes or deployment were performed.

## Important source limitation

The supplied directory has **no Git metadata**. Its existing handoff describes `public_html` as a historical July copy that was not refreshed during the later migration. The local WordPress version file reports **7.0**; this is an inventory fact, not a statement about current production or a vulnerability finding.

Exact reviewed-file hashes are recorded in [source-manifest.json](evidence/source-manifest.json). Active plugin/theme state, current database settings and equivalence to the live website were not established. Every runtime impact below depends on the relevant code being active and the stated prerequisites existing. No production exploit or customer-data breach was demonstrated.

## What was examined

| Area | Work performed | Result |
|---|---|---|
| Canonical Healthyaa AI Assistant 0.5.3 | Public chat input, product suggestions, knowledge-base indexing/retrieval, session handling, administrator actions and output rendering | **Needs tightening:** findings SRC-01 and SRC-02 |
| Healthyaa Analytics MU plugin and tracker | Public write endpoints, cart matching, token-protected reads, SQL handling, rate limits and collected data | **Needs tightening:** findings SRC-03, SRC-04 and SRC-05 |
| Custom checkout and OceanWP theme additions | Delivery options/fees, consent/date fields, account creation and removal of legacy AJAX handlers | **Mixed:** useful fee protections; SRC-06 needs tightening |
| Other custom MU plugins | Focused input/output and side-effect review of landing pages, cart display, SEO and popup controls | No additional material vulnerability established in this bounded review; lead-form abuse controls need follow-up |
| Thank You Page sandbox gateway and REST API | Role filtering, rule-reading/writing permissions and selected WooCommerce checkout call paths | Administrator filter confirmed in isolation; no payment bypass established; public rule-read endpoint noted below |
| Supplied dependencies | File-header inventory: 48 plugin entries, including four archived AI copies | Inventory only; no full dependency/CVE audit or active-plugin verification |
| Syntax | PHP lint on 43 files and JavaScript parsing on three files | **Passed: 46/46** with local PHP 8.5.10 and Node v26.10.0; not a production PHP compatibility test |

Theme WooCommerce templates received syntax coverage and a focused request-input search, not a complete manual security audit. WordPress core and the other third-party packages were not reviewed in full.

## Findings requiring action

Severity describes the bounded source risk, not a measured production incident. IDs use `HYA-SRC-*` to avoid conflicting with the existing HYA-01–HYA-08 findings or your colleague's test IDs.

| ID | Severity | Finding | Recommended action |
|---|---|---|---|
| HYA-SRC-01 | Medium | Public AI suggestions can include nonpublic product details | Enforce public product access before every product lookup/result |
| HYA-SRC-02 | Medium | AI knowledge base can index password-protected published content | Exclude restricted content, purge old indexed copies and recheck access when retrieving |
| HYA-SRC-03 | Medium | Analytics can reuse another visitor's record based on an unverified email | Bind updates to a server-controlled session; verify identity before cross-session merging |
| HYA-SRC-04 | Low | Changing User-Agent resets the analytics rate-limit bucket | Apply an atomic limit using a stable server-controlled identity; add an overall cap |
| HYA-SRC-05 | Medium | Analytics retains complete URLs, including sensitive query values | Store a minimal path and allowlisted attribution fields; redact sensitive values before persistence |
| HYA-SRC-06 | Low | Checkout consent/date validation accepts invalid values | Validate an explicit affirmative consent value and enforce date rules on the server |

### HYA-SRC-01 — Nonpublic product details in public AI suggestions

**Evidence:** `plugins/healthyaa-ai-assistant/includes/class-healthyaa-ai-assistant.php`, lines 85–109, 198–214, 897–900, 1896–1930 and 2474–2478. Paths in this report are relative to `public_html/wp-content/` unless stated otherwise.

The anonymous chat endpoint accepts a client-supplied `page_context.product_id`. Its suggestion path calls `wc_get_product()` and formats the result without checking published status or password protection. The isolated probe passed a synthetic private product to the actual suggestion method and received its private name and description summary.

**Prerequisites/impact:** The plugin must be active, a restricted product must exist, and the caller must identify its numeric ID. Product names, summaries, prices and related metadata can be disclosed. This does not demonstrate access to customer orders.

**Fix and retest:** Use a shared public-product access predicate across context, suggestion, lookup and formatting paths. Test public, draft, private and password-protected products; only products intended for anonymous viewing should appear. Evidence: [AI probes](evidence/ai-source-probes.json).

### HYA-SRC-02 — Password-protected content enters the AI knowledge base

**Evidence:** `plugins/healthyaa-ai-assistant/includes/class-healthyaa-ai-knowledge-base.php`, lines 211–236, 334–352, 570–591, 633–702 and 808–816; public response paths in `class-healthyaa-ai-assistant.php`, lines 333–338, 398–402, 433–437 and 488–492.

Indexing selects published pages/posts/products without excluding `post_password`. The source builder reads content without a public-access check; retrieval filters indexed rows by `active`, and public chat responses can include snippets. The actual source-builder method retained a synthetic password-protected page's content in the isolated probe. This disclosure path is not dependent solely on an AI model following a malicious prompt.

**Prerequisites/impact:** Protected published content must exist and be indexed. Its text can enter public source snippets or AI grounding. No real protected content or database was accessed during this review.

**Fix and retest:** Enforce access rules during indexing and retrieval. Remove existing indexed content when its visibility/password changes. Verify that protected content never appears in snippets or model context, including fallback responses. Evidence: [AI probes](evidence/ai-source-probes.json).

### HYA-SRC-03 — Analytics record matching does not prove visitor ownership

**Evidence:** `mu-plugins/healthyaa-analytics.php`, lines 1100–1170, 1480–1599 and 1602–1668.

The public tracking path accepts an email, computes its hash, and first searches for an unordered analytics record with that email hash. If cart hashes match, it reuses the record without requiring the same visitor/session. The subsequent update can replace contact, user-ID and attribution fields.

The isolated probe used a synthetic existing record and different visitor/session IDs. The actual lookup selected that record based on the email match and matching cart. The overwrite consequence follows from inspection of the subsequent update code; a real database update was not performed.

**Prerequisites/impact:** The caller needs a known email and a reusable existing record, normally with the same cart contents/hash. This is an **analytics integrity/attribution issue**, not demonstrated WooCommerce cart takeover, order modification or anonymous reading of the record. Public form tokens and request-context checks do not prove ownership of the email.

**Fix and retest:** Keep anonymous records tied to server-controlled sessions. Permit cross-session merging only after authenticated or verified identity. With two synthetic visitors sharing an email/cart, visitor B must not overwrite A's record. Evidence: [local probes](evidence/local-source-probes.json).

### HYA-SRC-04 — User-Agent changes bypass the application rate cap

**Evidence:** `mu-plugins/healthyaa-analytics.php`, lines 916–930, 1015–1017, 1117–1119 and 1370–1384.

The limiter hashes the IP address together with the caller's User-Agent. Changing that header creates a new bucket. In isolation, the actual limiter blocked the next request at its configured cap, then accepted another request from the same IP after only the User-Agent changed.

**Impact/limits:** A caller with acceptable request context and a public nonce can bypass this application's per-bucket cap, increasing analytics writes/resource use. No load test, denial of service or hosting-wide limit bypass was performed. The read-then-write transient counter is also not an atomic concurrency guarantee.

**Fix and retest:** Use stable server-controlled keys and atomic counters, with per-session/IP and overall limits appropriate to the service. Varying User-Agent must not reset the intended cap. Evidence: [local probes](evidence/local-source-probes.json).

### HYA-SRC-05 — Sensitive URL values are unnecessarily retained

**Evidence:** `mu-plugins/healthyaa-analytics/assets/analytics-tracker.js:221`; `mu-plugins/healthyaa-analytics.php`, lines 216, 617–648, 1039, 1071–1082 and 1506. Supporting source: `plugins/woocommerce/includes/class-wc-order.php`, lines 1916–1943.

The tracker collects `window.location.href`, including the query string and fragment, and the PHP handler stores the URL without removing sensitive parameters. Cart records also retain `last_page`, which is returned through the token-protected integration API. WooCommerce's order URL helpers include order keys in payment/received URLs.

A synthetic JavaScript probe retained an example order key, email query value and fragment in the actual payload function. Source inspection establishes the persistence path; no real order key was collected.

**Impact/limits:** Sensitive URL values can spread into analytics storage and integration responses beyond their original use. This is not evidence of public exposure: API reads require a token, administrator tracking is skipped, and the browser tracker honours Do Not Track.

**Fix and retest:** Minimise URLs before sending and again before storing. Prefer paths plus explicitly allowed campaign fields; exclude credentials, order/reset keys, personal information and fragments. Review historical analytics data under the normal retention process. Synthetic secret markers must be absent from stored/exported fields. Evidence: [payload probe](evidence/analytics-payload-probe.json).

### HYA-SRC-06 — Custom checkout accepts false consent and invalid dates

**Evidence:** `themes/oceanwp/functions.php`, lines 1762–1776 and 1820–1858.

The custom consent validator checks only whether the field exists. The actual validator accepted `healthyaa_consent='0'`; its save function recorded “No”. The appointment validator checks only that the field is nonempty and accepted `not-a-date`. Browser datepicker restrictions do not validate a crafted request.

**Prerequisites/impact:** The theme/custom hooks must be active in the relevant classic-checkout path. These defects can allow inconsistent consent/date records. No complete order, payment bypass or booking was tested. The intended booking schedule must be agreed from business requirements; a source comment and the datepicker implementation disagree.

**Fix and retest:** Require the explicit accepted consent value. Parse the date strictly and validate the permitted date range/schedule server-side. Test missing, false, malformed, past and disallowed dates, plus valid controls. Evidence: [local probes](evidence/local-source-probes.json).

## Controls confirmed and additional hardening notes

- **Analytics read access:** Missing/wrong tokens are rejected; a correct header token succeeds in isolated tests. Prepared SQL and default rejection of untrusted forwarded-IP headers were observed. Query-string tokens are also accepted at analytics lines 119–130; prefer header-only credentials to reduce URL logging/history exposure. No actual token was read.
- **Checkout:** Invalid delivery options and missing required fees were rejected in isolated checks. The MU plugin removes legacy anonymous delivery AJAX handlers. Their presence in the theme alone is therefore not evidence of an active bypass.
- **Sandbox payments / historical HYA-05:** The source filter removes the gateway for non-admins, reproduced in isolation. Classic and Store API checkout paths check available gateways. The payment method itself lacks a second role guard, so one would add defence in depth, but no reachable non-admin bypass was established. This source result does not close your colleague's live/staging role test.
- **AI administration/rendering:** Reviewed administrator actions use `manage_options` and action nonces; browser text/output escaping is present. The active AI generation path supplies no executable tools. No order/payment mutation path was found in that bounded review.
- **AI session hardening:** The client session identifier is a bearer identifier and uses `Math.random()` plus a timestamp. Prefer a cryptographically strong, server-issued session identifier with appropriate binding and expiry. No practical guessing or independent cross-session compromise was demonstrated.
- **Lead submission:** The landing-page handler has validation and a fixed recipient, but no application-level rate/deduplication control was found in that handler. The AI setting labelled “Enable lead capture prompt” disables prompts; an isolated observation that submissions still work is **not classified as a vulnerability**, because it is not labelled as a submission kill switch. No mail was sent.
- **Third-party rules/old copies:** `wc-thanks-redirect/src/Api.php` makes rule fetching public while writes require `manage_options`; sensitive rule contents were not established from source. Four archived AI plugin copies remain in the supplied files, supporting the historical HYA-08 cleanup observation. No direct execution exploit was established.

WordPress nonces are not authentication or ownership controls and do not guarantee one-time use; see the [official WordPress nonce guidance](https://developer.wordpress.org/apis/security/nonces/). This distinction matters for the anonymous analytics and lead paths.

## Evidence, validation and reproduction

| Evidence | Meaning |
|---|---|
| [Source hashes](evidence/source-manifest.json) | Exact 46 selected source files; hashes rechecked before publication |
| [Syntax results](evidence/syntax-checks.json) | 43 PHP and three JavaScript syntax checks passed |
| [Component inventory](evidence/component-inventory.json) | Local file versions only; active/current production state unknown |
| [Local source probes](evidence/local-source-probes.json) | 21 expected observations reproduced, including weaknesses; **not 21 security passes** |
| [AI source probes](evidence/ai-source-probes.json) | Two synthetic protected-content behaviours reproduced; prompt-setting behaviour recorded separately |
| [Analytics payload probe](evidence/analytics-payload-probe.json) | Full query/fragment retention reproduced with synthetic values |

The PHP harnesses invoke selected actual functions/methods with synthetic WordPress/WooCommerce dependencies. The JavaScript harness evaluates the tracker in a synthetic context. They do not reproduce a full WordPress installation, database, HTTP request lifecycle or production configuration. Source findings and caveats received an independent read-only review.

From this report's directory, with the supplied source still available:

```bash
php evidence/local-source-probes.php /Users/apple/git/healthyaa-wordpress
php evidence/ai-source-probes.php /Users/apple/git/healthyaa-wordpress
node evidence/analytics-payload-probe.js /Users/apple/git/healthyaa-wordpress
```

A successful harness run means the documented behaviour was reproduced, including defective behaviour. After fixes, convert those cases to regression assertions for the corrected behaviour rather than expecting the defects to remain.

Private configuration, credential storage, database dumps, customer records and migration scripts were excluded. Full third-party audits, live exploitation, network/hosting assessment and transactional testing remain outside this source-only review. No conclusion about legal compliance is made.

**Next action:** Match these file hashes/code paths to the intended maintained source, fix the applicable issues in reviewed changes, and use synthetic records in an isolated environment for integration retests. Keep the colleague's broader assessment and this source report linked without treating either as a replacement for the other.
