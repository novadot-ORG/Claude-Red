# Healthyaa — initial public-surface security review

Date: 26 October 2026. Target: https://healthyaa.co.uk/ (production).

The user confirmed authorization, production scope, no test accounts, and minimal requests. This pass made four successful sequential GET requests, at least five seconds apart: HTTPS homepage, HTTP homepage, robots.txt, and the same-origin assistant JavaScript explicitly linked by the homepage. An initial sandbox DNS failure did not retrieve a page. No redirects were followed automatically, forms submitted, login attempts made, chatbot messages sent, or third-party hosts tested. This is a limited baseline, not a completed penetration test.

## Observations

| Observation | Evidence | Interpretation |
|---|---|---|
| HTTP returns 301 to HTTPS | `http.headers` | Positive transport configuration |
| HTTPS homepage has no Strict-Transport-Security header | `home.headers` | Hardening gap in this response; browser preload status and other routes were not checked |
| Homepage has no Content-Security-Policy or X-Frame-Options header; no meta CSP observed | `home.headers`, `home.html` | CSP and framing defenses not observed. Browser framing and exploitable clickjacking were not tested |
| X-Content-Type-Options: nosniff present | `home.headers` | Positive browser hardening |
| No explicit Referrer-Policy observed | `home.headers`, `home.html` | Consider an explicit policy appropriate for sensitive URLs; no referrer leak demonstrated |
| No Set-Cookie header on homepage | `home.headers` | Insufficient evidence to evaluate authentication cookie flags or session behavior |
| No HTTP URLs found in quoted src/action attributes | `home.html` | Narrow static check only, not a browser mixed-content audit |

## Technology and attack-surface map

Public resource paths indicate WordPress, WooCommerce, Elementor, OceanWP, login/recovery/registration UI, product search, a cart, and custom Healthyaa assistant and analytics components. Public asset query strings expose version-like values, but these are not authoritative installed-version evidence and were not matched to CVEs.

The homepage references third-party scripts including CookieYes, Google Tag Manager, and scanner.novadot.co.uk. These hosts were not fetched or included in testing scope. Their presence makes data-flow and third-party script review relevant; it does not establish data leakage.

robots.txt contains standard WordPress/WooCommerce exclusions and a sitemap URL. Exclusions are not access controls; the listed directories were not requested.

## Custom assistant: source-review leads, not confirmed vulnerabilities

The publicly delivered script is saved as `assistant.js`.

- Message text is rendered with `textContent`, and several HTML-template fields pass through an escaping function. These are positive implementation patterns.
- Lines 303 and 331 assign response-provided `item.url` values to link destinations without visible client-side scheme/origin validation. Review server-side URL validation and constrain destinations appropriately. Attacker control of these values was not established, so this is not a confirmed XSS finding.
- Lines 402–410 create a client session ID using `Math.random()` and a timestamp and persist it in localStorage; server responses can replace it. Determine whether the server treats this merely as a conversation identifier or as authority to access sensitive records. If it is an access credential, use server-issued cryptographically random identifiers and server-side authorization. No session access or guessing was attempted.
- Page context includes the full current URL, and the client sends JSON POST requests to its configured endpoint. Review query-string minimization, conversation/lead retention, session ownership, abuse controls, and validation in the server implementation. None of these server controls can be judged from the browser script alone.

## Recommended next steps

1. Review response-header policy across public and authenticated routes. Introduce CSP in report-only mode first, choose suitable frame-ancestors restrictions, and deploy HSTS after confirming HTTPS coverage. Include subdomains only after checking their readiness.
2. Obtain the custom assistant, analytics, and account/cart server code for a source review. This permits deeper work without additional production requests.
3. Obtain disposable test accounts and synthetic orders to evaluate account isolation, order ownership, recovery, and session behavior. Current results cannot address these controls.
4. Confirm installed component versions from the administrative inventory, then check vendor advisories. Do not infer exploitable CVEs from asset filenames alone.
5. Reserve state-changing tests, payment/booking workflows, rate-limit tests, and AI endpoint interaction for a separately specified test plan, preferably staging.

No exploitable vulnerability or patient-data exposure was confirmed in this pass. Raw response files are retained alongside this report; absent headers are observations limited to the captured responses.
