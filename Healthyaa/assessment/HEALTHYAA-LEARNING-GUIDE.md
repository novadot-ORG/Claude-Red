# Learning web security through the Healthyaa assessment

Prepared: 28 October 2026  
Assessment target: https://healthyaa.co.uk/  
Practice environment: PortSwigger Web Security Academy

## 1. What we actually completed

We completed repository analysis, a limited public website review, manual HTTP training in Burp Suite, one access-control training lab, and an authenticated WordPress configuration review. We also performed a small set of anonymous API access checks.

The full Healthyaa penetration test remains incomplete. No Healthyaa payment bypass, customer-data exposure, SQL injection, or XSS vulnerability has been demonstrated. No Healthyaa test email, order, booking, refund, registration, or payment was submitted, and no production settings were changed.

The important distinction is between four kinds of evidence:

| Evidence type | Example from our work | What it establishes |
|---|---|---|
| Observed configuration | SiteGround's admin/editor MFA switch is off | This plugin is not enforcing that MFA setting; other layers remain unverified |
| Tested control | An anonymous settings request returns 401 | That particular request was denied in that context |
| Investigation lead | A sandbox payment gateway is enabled | A role restriction needs verification; this does not establish a bypass |
| Demonstrated vulnerability | The Academy lab permitted a privileged deletion | Broken access control was demonstrated in that lab only |

## 2. Establish permission, scope, and constraints

You confirmed permission to test Healthyaa and identified the production website as the target. Initially there were no test accounts and you requested minimal traffic. We used one request at a time, with at least five seconds between standalone public checks.

Later you provided access to an already authenticated WordPress administrator session. You also confirmed that any test email must go only to book@healthyaa.co.uk and include “demo” in the subject. That is a recipient constraint, not permission to trigger arbitrary customer workflows.

Before a test, write down:

- The exact hostname and environment.
- Which user role you are testing as: anonymous, customer, staff, or administrator.
- The feature and expected security behavior.
- Whether a request could send an email, create an order, reserve stock, or trigger a booking.
- Request limits, evidence location, and conditions for stopping.

A browser loads scripts and background requests automatically. Our initial four-request review and later twelve standalone requests do not include all browser-generated traffic from administration pages.

## 3. Understand the tools

| Tool | How we used it |
|---|---|
| Git | Cloned the Claude-Red reference repository |
| Terminal and curl | Retrieved individual pages and saved headers/body separately |
| Text editor and small Python helpers | Examined saved source, counted repository files, and summarized bounded HTTP checks |
| Browser developer tools | Introduced the Network panel for visual inspection |
| Burp Proxy | Captured browser requests and responses during the training exercise |
| Burp Repeater | Manually resent a request and inspected the response |
| WordPress administration | Reviewed installed components and configuration |
| Markdown notes and JSON evidence | Recorded reproducible observations and limitations |

An administrator session is useful for configuration review, but it cannot establish whether a customer or anonymous visitor can bypass permissions. Those tests require separate sessions.

## 4. Review the Claude-Red repository

We cloned:

```bash
git clone https://github.com/novadot-ORG/Claude-Red.git
```

The reviewed commit was `a8de813edc9f66f60d44cfe42d47750e89d9930b`. Recording a commit makes the review repeatable even if the repository changes later.

The repository contained 79 methodology documents in 23 categories, an installer, a converter, a manifest generator, and GitHub workflows. It was a reference library, not a scanner or runnable target application.

We inspected scripts before executing limited syntax and dry-run checks. We found missing frontmatter in 28 skills, an index missing one skill, converter content-loss behavior, and installer category traversal. A comment-triggered CI workflow required further authorization review; exploitability was not confirmed.

We did not globally install the skills or execute their attack examples. The useful lesson is to treat downloaded methodology and automation as code/content requiring review, rather than assuming that every example is suitable for production.

## 5. Learn the structure of HTTP

A request asks the server to do something:

```http
GET / HTTP/1.1
Host: healthyaa.co.uk
```

A response includes a status, headers, a blank line, and usually a body:

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>...</html>
```

The method describes the operation; the path identifies the resource. Headers carry metadata. The body contains content such as HTML or JSON.

| Status | Usual interpretation | Caution |
|---|---|---|
| 200 | Request succeeded | Inspect the body; it might contain an empty result or application error |
| 301/302 | Redirect | Inspect Location to see the destination |
| 401 | Authentication is missing or insufficient | Verify the actual error and context |
| 403 | Request is forbidden | This does not establish that every related operation is protected |
| 404 | Resource not found | Some systems intentionally use it to conceal protected resources |
| 500 | Server-side error | Avoid repeated probing; preserve the minimum evidence |

GET is conventionally read-only, but poorly designed applications can perform actions through GET. The Academy deletion link was an example. Always inspect a URL's purpose before requesting it.

## 6. Collect a public homepage baseline

These commands reproduce the initial capture. They make a new request when run; use the existing evidence when practising offline.

```bash
mkdir -p ~/Documents/healthyaa-manual-review
cd ~/Documents/healthyaa-manual-review
curl --version

curl --silent --show-error --max-time 30 \
  --dump-header home.headers \
  --output home.html \
  https://healthyaa.co.uk/

cat home.headers
```

`mkdir` creates the evidence folder; `cd` enters it. `curl --version` only inspects your local tool. The second curl command fetches the homepage once. `cat` reads a local file and sends no request.

Curl does not run page JavaScript or automatically fetch embedded images. Without `-L`, it does not follow redirects. Open the HTML in a text editor when you want an offline inspection; rendering it in a browser could load remote resources.

We examined headers and searched the HTML for scripts, forms, links, and metadata. Resource paths suggested WordPress, WooCommerce, Elementor, OceanWP, and custom Healthyaa components. Later administrator access supplied stronger installed-version evidence. Asset URL version strings alone are not authoritative.

## 7. Check HTTPS redirection and security headers

We made a separate HTTP request:

```bash
sleep 5
curl --silent --show-error --max-time 30 \
  --dump-header http.headers \
  --output http.body \
  http://healthyaa.co.uk/

cat http.headers
```

The response returned 301 with Location pointing to the HTTPS homepage. That verified redirection for this URL.

On the HTTPS homepage, `X-Content-Type-Options: nosniff` was present. HSTS, CSP, X-Frame-Options, and explicit Referrer-Policy were absent from the captured response.

- HSTS tells supporting browsers to enforce HTTPS for a period.
- CSP can restrict scripts, connections, framing, and other browser behavior.
- X-Frame-Options or CSP frame-ancestors can restrict framing.
- Referrer-Policy controls how much referring URL information is sent.

Absence is a hardening observation. It does not demonstrate XSS, clickjacking, or interception. Header policy also needs functional testing: an overly restrictive CSP can break checkout or payment integrations.

No Set-Cookie header appeared on the homepage capture, so it provided no basis for evaluating authenticated session cookies.

## 8. Read robots.txt

We retrieved `/robots.txt` once. It contained crawler exclusions for WooCommerce directories, cart-action URLs, and `/wp-admin/`, with an exception for `/wp-admin/admin-ajax.php`.

`User-agent: *` selects all matching crawlers. `Disallow` asks compliant crawlers to avoid a path. `Allow` provides an exception. The file supplies instructions rather than enforcing access control.

The Healthyaa entries did not establish that any logs or uploads were publicly accessible. We did not request the excluded directories merely because they were listed.

## 9. Inspect public JavaScript

We fetched one assistant script already linked in the homepage. Reading its source did not send a chatbot message.

We inspected message rendering, link creation, session identifiers, browser storage, and the shape of requests to the backend. Message text used `textContent`, and several template fields were escaped. Those were positive patterns.

We also saw response-provided link destinations and a client-created session identifier. These became source-review questions:

- Does the server validate link destinations?
- Does the session identifier merely label a conversation, or authorize access to it?
- Is conversation ownership enforced on the server?
- What personal information is retained or passed to integrations?

The client code alone could not answer those questions. We did not report an unproven XSS or session takeover.

## 10. Learn Burp on a practice page

You opened Burp Community Edition, started a temporary project, left Proxy interception off, and used its built-in browser to visit the Academy homepage.

Proxy HTTP history recorded the traffic. Intercept off allows requests to proceed without pausing; it does not disable capture.

You selected `GET /web-security`, switched the request from Hex to Raw, and examined the request and response. Hex shows bytes; Raw is easier for learning HTTP. You found the response title after the blank line separating headers from HTML.

Then you sent the request to Repeater and clicked Send once without changing it. Repeater produced a fresh response. This established a baseline before modifying inputs.

We also saw a playful SQL-like value in PortSwigger's Server response header. That text was not evidence that SQL executed. Always interpret the location and context of a string.

## 11. Understand the solved access-control lab

In the disposable “Unprotected admin functionality” lab, you discovered the administration URL, requested it, and received a user-management interface. Its HTML exposed a deletion link for the fictional user carlos. Requesting that action caused the lab to mark the objective solved.

The flaw was missing server-side authorization. The server should have checked that the requester had administrator permission before returning the interface and again before performing deletion.

Authentication answers “Who is this user?” Authorization answers “May this user perform this action?” A session cookie can represent an anonymous session; its presence alone does not prove administrator authentication.

The solved banner confirmed the lab objective. Your screenshot still showed carlos in the displayed list, so that visible list alone was not reliable proof of current backend state; the screenshot may have retained earlier content. We did not investigate that display behavior.

The next lab you selected uses an unpredictable administration URL. Its learning goal is that hiding a route does not replace permission checks. We have not recorded its completion.

These lab results do not establish the same weakness on Healthyaa.

## 12. Review WordPress with administrator access

When we opened Healthyaa's WordPress administration, it was already signed in. We did not enter your password or test the login process.

We inspected these areas without saving changes:

| Screen | Purpose | Observation |
|---|---|---|
| Plugins | Identify installed code and maintenance backlog | 23 update notices; 35 active and 14 inactive plugins shown on this screen |
| Site Health Info | Establish runtime and environment | WordPress 7.1.3, PHP 8.2.35, production environment |
| Security Optimizer — Login | Review login protections | Admin/editor MFA off; login attempt limit set to five |
| Security Optimizer — Site | Review hardening switches | XML-RPC and code editor disabling enabled; system-folder protection enabled |
| WooCommerce Payments | Identify gateways and test isolation | Stripe active; administrator-only sandbox gateway enabled |
| Stripe settings | Determine whether payments are real | Test mode unchecked; live webhook processing reported |
| Accounts & Privacy | Identify account flows and retention settings | Guest checkout and WooCommerce registration enabled; password setup email enabled |
| Emails | Identify notification side effects | Customer notifications enabled; some administrative recipients use a placeholder address |

The plugin screen and Site Health reported different inactive counts (14 versus 11). We recorded the plugin-screen count rather than claiming all inventory views agreed. A filesystem inventory would resolve the discrepancy.

Core WordPress registration being disabled does not contradict WooCommerce allowing customer registration: these are different controls and entry points.

SiteGround's MFA setting being off establishes that particular configuration; it does not rule out an external identity or hosting MFA layer. Likewise, setting a five-attempt limit does not prove runtime enforcement. We did not deliberately lock out accounts.

## 13. Perform bounded anonymous access checks

We used a separate HTTP client without browser cookies so the administrator session could not accidentally grant access. Requests were sequential, with five-second gaps between requests in each batch.

| Requested resource | Observed result | Conclusion |
|---|---|---|
| `/wp-admin/plugins.php` | 302 to login | Anonymous plugin administration was denied |
| `/wp-json/wp/v2/settings` | 401 | Settings request required authorization |
| `/wp-json/wp/v2/users?context=edit&per_page=1` | 401 | Edit-context user request was denied |
| `/wp-json/wc/v3/settings` | 401 | WooCommerce settings request was denied |
| `/wp-json/healthyaa/v1/abandoned-carts` | 403 | Custom abandoned-cart request was denied |
| `/xmlrpc.php` via GET | 403 | This GET request was blocked |
| One nonexistent page | 404 | A not-found status was returned |
| `/wp-json/wctr-api/v1/tyrules/fetch` | 200 with an empty data array | No sensitive data disclosure demonstrated |

We also read the public API index to identify custom routes. Route visibility is normal API discovery and does not establish permission failure. The first read was truncated by our size limit; a subsequent bounded read obtained complete JSON. That was a collection limitation, not a site error.

A successful test of one endpoint cannot prove all endpoints, HTTP methods, user roles, or data objects are protected. Those are separate test cases.

## 14. Why payment testing remains unfinished

Stripe is in live mode, customer notifications are enabled, and fulfilment isolation has not been established. Choosing an administrator-only sandbox gateway might still create a real production order or trigger downstream actions.

You asked that real customers receive no test emails. A subject containing “demo” does not prevent delivery to an unintended recipient. We must control recipients and integrations before creating test records.

A proper staging setup should have synthetic customers, isolated payment test credentials, outgoing email restricted to the approved inbox or an email sink, and clinic/booking/fulfilment integrations disconnected or stubbed. Scheduled jobs and copied webhook endpoints need review too. Simply cloning production can copy sensitive records and live credentials.

We have not created staging or changed the live gateway mode.

## 15. The remaining practical learning plan

For each scenario, first document expected behavior, then make a baseline request, vary one input, compare the complete response and backend state, and record the result.

1. Create two disposable customers in isolated staging. Confirm each can read its own synthetic order and cannot read the other's.
2. Exercise successful, failed, cancelled, and pending test payments. Verify only the permitted paid state triggers fulfilment.
3. Check that server-calculated totals govern payment, and that return-page navigation alone cannot mark an order paid.
4. Review webhook signature, amount/currency binding, order association, and replay handling using test-mode events.
5. Confirm ordinary customers cannot select the administrator-only sandbox payment method.
6. Test coupon eligibility and single-use limits with dummy products and bounded requests.
7. Verify session expiry, logout invalidation, password recovery, and account-change controls using the approved test inbox.
8. Review custom plugin and MU-plugin source for permission checks, validation, output encoding, and conversation ownership.
9. Match installed versions to vendor advisories and verify applicability. An available update is not automatically a known exploitable vulnerability.
10. Retest confirmed findings after fixes and record both expected and actual results.

## 16. Write findings that another person can verify

Use this template:

```text
Finding ID and title:
Assessment date:
Affected environment and resource:
Test identity/role:
Expected behavior:
Observed behavior:
Minimal reproduction steps:
Evidence filenames:
Demonstrated impact:
Unverified assumptions and limitations:
Recommended remediation:
Retest result:
```

Example from our actual assessment:

```text
Title: Administrator/editor MFA disabled in Security Optimizer
Environment: Healthyaa production
Evidence: Login Security screen shows the relevant switch off
Impact: This plugin is not enforcing a second factor for those roles
Limitations: Other MFA layers and actual login behavior were not tested
Remediation: Establish MFA coverage and recovery procedures; validate on staging
Retest: Pending
```

Avoid presenting a WordPress “critical” performance warning as a critical exploitable vulnerability. Severity depends on demonstrated impact, prerequisites, and exposure.

## 17. Evidence and references

Local evidence is in `healthyaa-review/2026-10-28/`, including the interim assessment, plugin inventory, login-control screenshot, and JSON summaries of public requests. Earlier baseline files are in `healthyaa-review/`.

Keep evidence access restricted. Redact session cookies, credentials, tokens, and customer information before sharing screenshots or request exports. Hashes can help establish that evidence files have not changed, but do not independently prove when or how evidence was collected.

Useful official references consulted during the learning process:

- curl options: https://curl.se/docs/manpage.html
- Chrome Network panel: https://developer.chrome.com/docs/devtools/network/reference/
- Burp Proxy tutorial: https://portswigger.net/burp/documentation/desktop/getting-started/intercepting-http-traffic
- First access-control lab: https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality
- Next access-control lab: https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality-with-unpredictable-url
- PHP support schedule: https://www.php.net/supported-versions.php

On 28 October 2026, PHP 8.2 remained under security support until 31 December 2026. Recheck vendor information when using this guide later. This guide records observed work and teaching steps; it is not a security certification or a claim that the full penetration test is complete.
