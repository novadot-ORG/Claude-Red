# Search-term XSS procedure

This document preserves the original plan. Some submission/reflection steps are now evidenced in the [captured-evidence report](evidence/2026-11-17/REPORT.md); consult the [status matrix](TEST-STATUS.csv) rather than treating all steps as completed or unexecuted.

## Preparation and tools

Use a confirmed authorised staging copy with synthetic data. Keep the exact staging origin in scope and preserve the existing Healthyaa restrictions in the parent README. Do not assume the supplied sg-host address is staging until confirmed. No new active testing is authorised merely by publishing this document.

Chrome DevTools is sufficient for the first manual pass. Burp Suite Community adds request inspection and Repeater; its automated scanner is not included. ZAP active scanning is optional and not needed for this focused first pass. Claude-Red is a methodology library, not evidence of completed tests.

## Manual workflow

1. Open staging search with DevTools Network, Elements and Console available. Record browser, build, URL, account context and timestamp/timezone.
2. Search for `HY-XSS-SEARCH-001`. Inspect live suggestions, submitted results and no-results messaging separately. Observe the real requests and parameter names; do not infer the autocomplete endpoint from the archived form.
3. Locate the marker in Network Response and live Elements. Record whether it enters text, an attribute, JSON, a URL or JavaScript. A reflected string is not a vulnerability.
4. Try the HTML marker below in a plain-text search field. Record literal text, rejection, sanitization or an actual HTML element. Formatting alone establishes neither script execution nor XSS.
5. On staging, try the console marker below. Submit using the real application flow, clear the console first and enable informational logs. Do not paste JavaScript into Console or insert elements manually through DevTools as proof.
6. Confirm any execution by repeating the normal application interaction. Capture the request, response, rendered output and console marker, with secrets removed.
7. Check the dynamically updated suggestions as well as full-page results. Compare raw response and live DOM; client-side insertion may need separate source review. Reflected/stored describe delivery and persistence, while DOM-based describes a rendering mechanism; they can overlap.
8. If normal UI checks reject input, capture an ordinary request with Burp, send it to Repeater, and alter only the search parameter while preserving encoding and required session fields. Inspect server handling independently of browser validation.
9. Confirm suspected rendering through the browser. Repeater itself does not execute JavaScript. Do not mistake a request accepted by the server for an XSS finding.
10. Record the result per output location; inspect any persistence only if it actually exists and is in scope. Remove test content where applicable.

### Discussed test values

Plain marker:

```text
HY-XSS-SEARCH-001
```

HTML interpretation marker:

```html
<strong>HY-XSS-HTML-001</strong>
```

Harmless execution marker:

```html
<svg onload="console.log('HY-XSS-EXEC-001')"></svg>
```

The chat also used `HY-VALIDATION-001` and `HY-XSS-CHECK` as alternative marker labels. The SVG and HTML marker submissions are now recorded in the dated evidence report; alternative labels remain examples unless separately evidenced. A single HTML-context example does not test every attribute, JavaScript or URL context.

## Interpretation

| Observation | Record as |
|---|---|
| UI blocks input but direct request accepts it | Browser restriction bypassed; XSS unproven |
| Marker appears as literal text | This specific output/test handled safely |
| Real markup appears, no script execution | HTML interpretation/injection lead; investigate context |
| Console marker executes through the application | Confirmed execution for that path; preserve reproducible evidence |
| CSP blocks the inline handler | Execution blocked in this configuration; inspect unsafe rendering separately |
| No visible output or execution | Inconclusive for broader XSS coverage |

Do not report PASS for all XSS because one payload did not execute. Do not report session theft, customer impact or administrator compromise without supporting evidence.

## Finding template

```text
Test ID:
Environment / build:
Date / time / timezone:
Browser and authentication context:
Page / request / parameter:
Output location and rendering context:
Exact submitted value:
Reproduction steps:
Expected result:
Actual result:
Redacted evidence paths:
Assessment and limits:
Affected code/component:
Fix and retest status:
```

## Remediation and retest guidance

Developers should trace the search term from request to rendering. Use text APIs for plain text, context-appropriate encoding, and a maintained sanitizer where HTML is intentionally supported. Avoid unsafe raw-HTML insertion. Apply CSP as defence in depth, not a replacement for safe rendering.

After a fix, repeat the failing case across every affected search output and verify ordinary searches with apostrophes, ampersands and international characters. Add a regression test for the actual unsafe path. No fix or retest has yet been recorded for this search assessment.

## References

- [Claude-Red web application index](https://github.com/novadot-ORG/Claude-Red#web-application)
- [OWASP XSS explanation](https://owasp.org/www-community/attacks/xss/)
- [OWASP XSS prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [Burp getting started](https://portswigger.net/burp/documentation/desktop/getting-started)
- [ZAP active scanning](https://www.zaproxy.org/docs/desktop/start/features/ascan/)
- [Hacky lab 164](https://hacky.uk/lab/164)
