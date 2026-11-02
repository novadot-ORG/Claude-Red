# Novadot website — initial black-box assessment

Date: 2026-11-02. Evidence captured between 18:07 and 18:10 UTC.
Target: `https://novadot.co.uk/`, with one HTTP request to check the HTTPS redirect.

## Result

The 11 public pages listed in the sitemap returned HTTP 200 and consistently supplied useful browser protections. HTTPS certificate verification succeeded and a normal handshake negotiated TLS 1.3. This limited review identified one confirmed security-hardening issue and one operational concern requiring follow-up. It does not establish that the website is free of vulnerabilities.

The site serves Astro-generated assets, but it is not exclusively static: the contact and event forms depend on `/api/enquiry.php`. Both recorded GET requests to this endpoint returned HTTP 403 with HTML rather than the JSON token expected by the browser code. Check this path before treating enquiries as working.

## Scope and method

The user identified Novadot as their employer, supplied this website and requested testing. This phase covered ordinary public GET requests, response headers, linked JavaScript inspection and one certificate-validating TLS handshake. There were 20 recorded GET responses: 11 HTML pages, four JavaScript assets, robots.txt, sitemap.xml, the HTTP homepage and two enquiry preparation requests. A web reader also consulted the public homepage; the evidence count covers the direct captures only.

No forms were submitted, emails sent, accounts accessed, payloads injected or load tests performed. No source repository, hosting configuration or server logs were supplied. The separate `scanner.novadot.co.uk` service was identified from the site's markup but was not requested or assessed. JavaScript was inspected as text; no browser execution or end-to-end delivery test occurred.

Selected methodology: public-surface mapping from `offensive-fast-checking`, certificate/transport observations from `offensive-tls-attacks`, and evidence/severity guidance from `offensive-reporting`. Reference version: `codex/openai-compatibility` at `32c3386c8c72d4120563bfbf2fed2718d9ff840f`. Only applicable parts were used; these skills were read from Git without installing them or merging branches.

## ND-OBS-001 — Enquiry preparation endpoint returned HTTP 403

**Classification:** Operational follow-up; security severity not assigned. **Status:** Response confirmed; cause and customer impact unverified.

**Affected flows:** `/contact/` and `/events/`.

The public bundles for both pages import `enquiry-form.BeFRChKr.js`. After client-side validation, that module sends a GET to `/api/enquiry.php` and expects a successful JSON response with a nonempty `token`. Only then does it POST the enquiry. Both the basic JSON GET and a second GET with the contact Referer and same-origin Fetch Metadata headers returned HTTP 403, `Content-Type: text/html`, with 52-byte bodies.

**Impact:** If real visitors receive these responses, form preparation fails and enquiries cannot be submitted. The script handles this with an unavailable/error message. The result could instead depend on request context, user agent, network filtering or hosting rules; this assessment did not reproduce the failure in an actual browser. It is not evidence of an authentication bypass, data exposure or an exploitable PHP flaw.

**Evidence:** [shared form code](evidence/enquiry-form-js.body), [first response](evidence/enquiry-api.headers), [contextual request metadata](evidence/enquiry-api-context.json), [second response](evidence/enquiry-api-context.headers). Response values were not retained; [shape records](evidence/enquiry-api-context-shape.json) capture format and length only.

**Next action:** Inspect the handler and its hosting/access rules, then correlate the two UTC timestamps with server logs. In an approved browser test, inspect the preparation GET before testing delivery. Confirm it returns the expected JSON and appropriate cache/session controls. Do not relax access controls indiscriminately to remove the 403. Use a designated test recipient or staging environment for a later submission test.

**Retest:** Verify successful preparation in a supported browser, then separately verify one agreed test enquiry reaches its destination and duplicate/error handling works. Server-side validation, anti-spam controls, token validation and rate limiting remain untested.

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

Next, obtain the website source repository and confirm whether it includes the PHP handler. Review its validation, email construction, token/session handling, duplicate controls and abuse protections, plus the Astro build and hosting policy. Select additional skills based on that code. Testing the separate analytics service requires adding that service to scope.

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
