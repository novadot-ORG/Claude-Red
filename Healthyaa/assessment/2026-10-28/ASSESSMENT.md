# Healthyaa security assessment — interim findings

Date: 28 October 2026. Target: https://healthyaa.co.uk/ (production).

## Assessment status

In progress. Authenticated configuration review and a bounded unauthenticated baseline have been performed. This is not a completed full penetration test and does not certify the site secure. No payment bypass or customer-data exposure has been demonstrated.

The user authorized testing and confirmed that the only permitted email destination is book@healthyaa.co.uk, with “demo” in the subject. No test emails, orders, bookings, registrations, refunds, or payment requests were submitted. No configuration, plugins, passwords, or customer records were changed.

## Confirmed observations

| ID | Observation | Priority and next action |
|---|---|---|
| HYA-01 | SiteGround Security Optimizer's administrator/editor two-factor setting is off. | High hardening priority: establish MFA with recovery procedures. Other independent MFA layers were not verified. |
| HYA-02 | Plugin screen reports 23 available updates, 35 active plugins and 14 inactive plugins; all 49 listed plugins have WordPress auto-updates disabled. | Review release notes and test updates in staging. These counts do not imply 23 vulnerabilities. Hosting-level patching was not assessed. |
| HYA-03 | Contact Form 7 and Template Kit Import update notices state PHP incompatibility. Site Health reports PHP 8.2.35. | Plan a compatible PHP migration and plugin regression tests. PHP 8.2 is still in security support on the assessment date, ending 31 December 2026. |
| HYA-04 | Anonymous homepage response lacks HSTS, CSP, X-Frame-Options, and explicit Referrer-Policy. nosniff is present. | Stage an appropriate header policy; verify sensitive routes and framing impact. No XSS or clickjacking exploitation established. |
| HYA-05 | SandBox Payment is enabled in production and described as administrator-only. | Verify the server-side role check in source and with a disposable non-admin account on staging. UI text alone does not establish enforcement or a bypass. |
| HYA-06 | Post SMTP reports that FluentSMTP overrides wp_mail; both plugins are active. | Reconcile mail ownership and delivery testing; this is an operational conflict, not a demonstrated breach. |
| HYA-07 | Several operational WooCommerce email recipients are user@example.com, including the payment-gateway-enabled notification. | Confirm the intended monitored recipient; placeholder addresses can prevent security/operations notifications reaching staff. |
| HYA-08 | Multiple inactive versions of the custom Healthyaa AI Assistant remain installed. | Review and remove obsolete copies through the normal change process after backup; inactivity alone does not guarantee all bundled files are inaccessible. |

Site Health also reports outdated WooCommerce theme template overrides, inactive themes, autoloaded-option performance concerns, and missing shipping methods while shipping is enabled. These are reported by WordPress; its “critical” performance label is not a penetration-test severity rating. Shipping configuration may be intentional for service products and requires business confirmation.

## Positive controls and completed checks

- Anonymous GET /wp-admin/plugins.php returns 302 to the WordPress login page.
- Anonymous GET /wp-json/wp/v2/settings returns 401 rest_forbidden.
- Anonymous GET /wp-json/wp/v2/users?context=edit&per_page=1 returns 401 rest_forbidden_context.
- Anonymous GET /wp-json/wc/v3/settings returns 401 woocommerce_rest_cannot_view.
- Anonymous GET /wp-json/healthyaa/v1/abandoned-carts returns 403 healthyaa_rest_forbidden.
- GET /xmlrpc.php returns 403; the security plugin also shows XML-RPC disabled. This checks GET behavior, not every protocol method.
- A single nonexistent-page request returns 404. The body was not audited for every possible information leak.
- The security plugin shows a five-attempt login limit, system-folder protection and theme/plugin editor disabling enabled. Runtime enforcement of each setting has not been independently tested.
- Anonymous GET /wp-json/wctr-api/v1/tyrules/fetch returns HTTP 200 with an empty data array. No sensitive configuration was demonstrated; this is an investigation lead, not a confirmed disclosure.

## Payment and email context

Stripe is enabled and its test-mode checkbox is unchecked (live mode). The settings page reports its most recent live webhook was processed successfully and at least one webhook is pending; this does not independently verify signature validation. Deferred capture and debug logging are unchecked. WooPayments requests completion of setup. The administrator-only sandbox gateway is enabled, but email and fulfilment isolation have not been established. WooCommerce customer notifications are enabled for processing/on-hold/failed orders, refunds, account creation, reset password, and other events. Completed-order notification appears disabled. No real customer orders were opened or modified.

An administrator deliberately placing a sandbox order is not evidence of a payment bypass. To establish a business-logic vulnerability, test the behavior of an ordinary customer and confirm unauthorized fulfilment using synthetic records only.

## Remaining test matrix

| Area | Required verification | Prerequisite |
|---|---|---|
| Customer isolation | Account A cannot access account B's synthetic orders, bookings, or assistant conversation | Two disposable customer accounts and synthetic records |
| Payment integrity | Server ignores client-supplied totals; rejects forged/replayed confirmations; unpaid/failed/cancelled payments do not fulfil | Staging, test gateway, controlled fulfilment and email sink |
| Sandbox gateway | Server rejects non-admin selection even if supplied directly | Source review plus staging customer account |
| Discounts and concurrency | Coupon eligibility/usage limits hold, including concurrent submissions | Staging with bounded test cases |
| Sessions and recovery | Cookie controls, expiry, logout invalidation, recovery token use and account changes | Disposable accounts; confirmed demo email routing |
| Custom code | REST permission callbacks, nonces, input validation, output encoding, session ownership and data retention | Read-only source copy of custom plugins and MU plugins |
| Input and upload handling | Context-specific XSS/injection/file processing checks | Mapped endpoints, synthetic data, staging for persistent probes |
| Dependency vulnerabilities | Match installed versions and prerequisites against primary vendor advisories | Full vendor advisory review; update backlog alone is insufficient |
| Availability and recovery | Rate controls, load resilience, backup restoration | Separately scheduled staging tests and hosting access |

No staging URL or isolated testing configuration has yet been supplied. Production checkout and persistent-input tests are therefore pending the user's no-real-customer-email/fulfilment constraint. A blanket “full test” cannot be marked complete from public GET checks and admin settings alone.

## Evidence

- public-checks.json: seven sequential anonymous GET responses, minimum five-second gaps. The first API index read was capped at 1.5 MB and could not be parsed; a later bounded read obtained the full 1.84 MB index.
- custom-route-inventory.json: selected custom route names and methods from the public API index; listing a route is not a vulnerability.
- custom-access-checks.json: three additional anonymous GET checks.
- thankyou-api-response-shape.json: follow-up response structure only, with no customer records retained.
- plugin-inventory.txt: observed component versions and activation/update labels.
- login-controls.txt and login-controls.png: observed login security configuration.

Total standalone public requests in this assessment: 12. Browser administration navigation and its background requests are additional and were not subject to a measured request cap. No high-volume scans were run.

## Reference

PHP support dates: https://www.php.net/supported-versions.php
