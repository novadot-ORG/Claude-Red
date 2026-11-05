# Novadot website — initial black-box assessment

> **6 November remediation update:** The dependency, CSP and analytics-source actions below have now been implemented, deployed and verified for the agreed scope. See the [deployment results](../../remediation/2026-11-06/deployment/report.md). Original observations and evidence below describe the 2 November assessment.

Date: 2026-11-02. Initial evidence captured between 18:07 and 18:10 UTC; user-agent follow-up at 18:13 UTC. Updated 2026-11-03 with the subsequent [source review](SOURCE-REVIEW.md) and [completed email tests](../../manual-tests/2026-11-02/EMAIL-DELIVERY.md).
Target: `https://novadot.co.uk/`, with one HTTP request to check the HTTPS redirect.

## Result

The 11 public pages listed in the sitemap returned HTTP 200 and consistently supplied useful browser protections. HTTPS certificate verification succeeded and a normal handshake negotiated TLS 1.3. This limited review identified one confirmed security-hardening issue. An initial API availability concern was cleared by the user-agent follow-up below. It does not establish that the website is free of vulnerabilities.

The site serves Astro-generated assets, and its contact and event workflows depend on `/api/enquiry.php`. Initial requests using Python’s default user agent received HTTP 403; repeating the contextual request with a browser user agent returned HTTP 200 and a nonempty JSON token. An endpoint outage was not established. Subsequent authorised Contact and Events submissions both showed success, and the user confirmed each email arrived exactly once. Received-email screenshots support the contents, and Events reply-recipient selection is verified; see the [delivery and reply evidence](../../manual-tests/2026-11-02/EMAIL-DELIVERY.md).

## Scope and method

The user identified Novadot as their employer, supplied this website and requested testing. This phase covered ordinary public GET requests, response headers, linked JavaScript inspection and one certificate-validating TLS handshake. There were 21 recorded GET responses: 11 HTML pages, four JavaScript assets, robots.txt, sitemap.xml, the HTTP homepage and three enquiry preparation requests. A web reader also consulted the public homepage; the evidence count covers the direct captures only.

During the initial GET-only phase, no forms were submitted, emails sent, accounts accessed, payloads injected or load tests performed. No source repository, hosting configuration or server logs were available for the initial public phase. The user subsequently supplied the local website source; its review is recorded separately. The separate `scanner.novadot.co.uk` service was identified from the site's markup but was not requested or assessed. JavaScript was inspected as text during that phase. The later user-authorised follow-up used native Computer Use to submit one Contact and one Events enquiry; both deliveries were confirmed. No Playwright was used for those submissions. The analytics service was not separately assessed during the browser follow-up.

Selected methodology: public-surface mapping from `offensive-fast-checking`, certificate/transport observations from `offensive-tls-attacks`, and evidence/severity guidance from `offensive-reporting`. Reference version: `codex/openai-compatibility` at `32c3386c8c72d4120563bfbf2fed2718d9ff840f`. Only applicable parts were used; these skills were read from Git without installing them or merging branches.

## ND-OBS-001 — Initial enquiry 403 responses were request-context dependent

**Classification:** Resolved assessment discrepancy, not a confirmed outage or security vulnerability.

**Affected flows:** `/contact/` and `/events/`.

Both public form bundles import `enquiry-form.BeFRChKr.js`. After client-side validation, it requests a token with GET `/api/enquiry.php`, then POSTs the enquiry. Two Python-urllib GETs returned HTTP 403 HTML, including one with the contact Referer and same-origin Fetch Metadata headers.

After the source handoff identified historical user-agent filtering, the contextual request was repeated with only the User-Agent changed to a browser value. It returned HTTP 200, JSON with a nonempty string token, no-store caching and security headers. This supports request-context filtering rather than a demonstrated outage; the precise filtering layer was not inspected. No controls were changed or bypassed to access protected data: the response is the normal public form-preparation token.

**Evidence:** [shared form code](evidence/enquiry-form-js.body), [initial request](evidence/enquiry-api-context.json), [initial response](evidence/enquiry-api-context.headers), [browser-agent request](evidence/enquiry-api-browser-agent.json), [successful response headers](evidence/enquiry-api-browser-agent.headers), and [redacted token shape](evidence/enquiry-api-browser-agent-shape.json). Token values were not retained.

**Follow-up verification — passed (2026-11-03 local date):** The later authorised Contact and Events submissions each displayed “Enquiry submitted”; the user confirmed **“Both arrived once.”** Received-email screenshots show the expected test contents. Events reply-composer and expanded-recipient screenshots verify that Reply selects `website-test@example.com`, the submitted visitor address. See the [completed delivery and reply checks](../../manual-tests/2026-11-02/EMAIL-DELIVERY.md). The earlier delivery limitation is closed for these two submissions; no repeat submission is needed. Original 403 evidence is retained to explain the corrected interpretation. Contact reply selection was not separately exercised; the Events check establishes address selection, not delivery to the synthetic reply address.

## ND-HARD-001 — Content security policy can be tightened

**Severity:** Low, defence-in-depth configuration. **Status:** Confirmed on all 11 sampled HTML pages; no injection vulnerability demonstrated. CVSS not assigned.

The policy contains `script-src 'self' 'unsafe-inline' https://scanner.novadot.co.uk` without script hashes or nonces. If an attacker separately obtains an HTML injection opportunity, this policy does not provide the usual block on inline JavaScript. The missing `base-uri` and `form-action` directives also leave those specific restrictions unset: they do not inherit `default-src`. These are hardening gaps, not proof that such an injection exists. See [MDN script-src](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src), [base-uri](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/base-uri) and [form-action](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/form-action).

**Evidence:** [homepage headers](evidence/home.headers), [contact headers](evidence/contact.headers), [all-page comparison](evidence/baseline-summary.json), and [inline scripts](evidence/inline-scripts.json). Existing navigation code is inline, so simply deleting `unsafe-inline` could break functionality.

**Remediation:** Move executable inline code into same-origin assets or generate hashes from the exact deployed inline script bytes. For static builds, do not use a fixed reusable nonce. Review `base-uri 'none'`, `object-src 'none'`, an appropriate `form-action`, and `frame-ancestors 'self'` alongside the existing framing protection. The forms currently use JavaScript fetch, so their network requests are governed by `connect-src`, not `form-action`. Validate a candidate policy in staging or report-only mode before enforcement; exercise navigation, diagnostics, enquiry forms and analytics. No production policy was changed.

**Retest:** Capture the deployed policy, verify intended scripts still execute, and confirm unapproved inline script is blocked in an isolated test. Keep required analytics permissions narrowly scoped.

## Positive observations and limits

| Check | Observed result | Limit |
|---|---|---|
| HTTP transport | Homepage returns 301 to the HTTPS homepage | Only root redirect checked |
| Certificate | Hostname/chain verification succeeded; certificate expires 2027-01-01 00:11:43 UTC | Revocation and full chain configuration not independently audited |
| TLS | Default handshake negotiated TLS 1.3 with TLS_AES_256_GCM_SHA384 | Older protocol/cipher acceptance not tested |
| HSTS | One-year max-age, includeSubDomains and preload token on all HTML pages | Actual browser preload-list membership not checked |
| Browser headers | nosniff, SAMEORIGIN, strict-origin-when-cross-origin, and camera/microphone/geolocation restrictions on all HTML pages | API 403 responses did not contain these same headers |
| Public routes | All 11 sitemap URLs returned HTTP 200 | No hidden-route discovery performed |
| Script integrity | Analytics script tag has SHA-384 integrity and anonymous CORS attributes | Script bytes, matching hash, CORS response and runtime behaviour not verified |
| DOM review | Contact topic query is assigned to a textarea value; diagnostic innerHTML uses bundled constant choices | No observed attacker-controlled flow into that sink; not a full DOM-XSS audit |
| Credentials | No obvious private credential observed in the reviewed first-party scripts | No source/configuration secret scan; public analytics site identifier is not by itself evidence of a leaked secret |
| Mixed content | No HTTP script, stylesheet, image or iframe URL in parsed page markup | CSS resources, dynamically created requests and browser traffic not fully inspected |

The privacy page describes server-side enquiry handling and retention. These are published claims, not controls verified by this assessment. No conclusions about legal compliance or analytics collection are drawn.

## Applicable next work

For this site, focus on web/DOM safety, the enquiry API, transport, dependencies and reporting. Login, JWT, OAuth and account-isolation tests are not currently indicated by the observed public surface. Wireless, Active Directory and infrastructure exploitation are outside this website baseline.

The user supplied `/Users/apple/git/novadot_website`, which includes the PHP handler; see the [source review and dependency findings](SOURCE-REVIEW.md). Testing the separate analytics service still requires adding that service to scope.

## Evidence and reproduction

The [machine-readable summary](evidence/baseline-summary.json) indexes every recorded GET, its timestamp and response status. Each normal capture has `.headers`, `.body` and `.json` metadata. Header text has normalized line endings and trailing whitespace; body captures are unchanged. API captures retain only response shape and redacted headers. [SHA256SUMS.txt](SHA256SUMS.txt) records hashes of the evidence files.

These commands reproduce the public observations without submitting forms:

```bash
curl -sS -D - -o /dev/null http://novadot.co.uk/
curl -sS -D - -o /dev/null https://novadot.co.uk/
curl -sS -D - -o /dev/null -H 'Accept: application/json' \
  -H 'Referer: https://novadot.co.uk/contact/' \
  -H 'Sec-Fetch-Site: same-origin' -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' https://novadot.co.uk/api/enquiry.php
```

Responses can vary by time and request context. Redact cookie values from any newly saved output.
