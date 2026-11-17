# Healthyaa search XSS — existing browser evidence review

Reviewed 17 November 2026 (Europe/London). Target: kaviarasank64.sg-host.com. No production-domain result is inferred.

## Work performed

Inspected the user's existing Chrome tab and preserved Network history. Exported the nine document requests matching HY-XSS through Chrome's Export HAR (sanitized) control. Parsed that exported file offline and recorded marker contexts, request values, response status, timestamps and response hashes. No new search payload was submitted, no page reloaded, no cart link followed and no configuration changed.

The current URL has the plain HY-XSS-HTML-001 marker; its response is entry 8. The full strong-tag marker is preserved in earlier entry 3. These must not be conflated.

## Main conclusions

1. The full HTML-marker request was sent at 12:32:33.060 GMT and received HTTP 200. Its decoded s value is `<strong>HY-XSS-HTML-001</strong>`.
2. All 11 occurrences in that response were inspected and classified below. They appear as encoded attribute data, encoded URLs, or URL data inside JSON/JavaScript strings. This test does not demonstrate an injected strong element or executable script.
3. The complete SVG console-marker payload was also submitted twice. This corrects the previous screenshot-only uncertainty: the preserved requests now establish submission, though not execution.
4. The current Console shows CookieYes URL mismatch, a Grammarly permissions-policy message, jQuery Migrate information and an analytics 403. No execution marker is visible. However, this console belongs to the later plain-marker page, with two messages hidden; it is not a contemporaneous console capture for either SVG request. Historical execution is therefore unconfirmed, not disproved.
5. The exported view contains document requests only. Autocomplete response handling was not evaluated by this review. No client-side validation bypass was demonstrated.

## All 11 HTML-marker contexts

| Match | Location | Observed representation |
|---|---|---|
| 1 | Open Graph og:url metadata | Percent-encoded tag characters within URL |
| 2 | JSON-LD SearchResultsPage @id | Percent-encoded tag characters within URL string |
| 3 | JSON-LD SearchResultsPage url | Percent-encoded tag characters within URL string |
| 4 | Search input 1 value | `&lt;strong&gt;HY-XSS-HTML-001&lt;/strong&gt;` |
| 5 | Search input 2 value | Same HTML entity encoding |
| 6 | Search form hidden _wp_http_referer | URL-encoded input; query separators HTML-encoded |
| 7 | Login hidden xoo_el_redirect | URL-encoded input; query separators HTML-encoded |
| 8 | Registration hidden xoo_el_redirect | URL-encoded input; query separators HTML-encoded |
| 9 | Password-recovery hidden _wp_http_referer | URL-encoded input; query separators HTML-encoded |
| 10 | Login redirect JavaScript configuration | Percent-encoded payload within a quoted URL string |
| 11 | Assistant pageContext URL configuration | Percent-encoded payload within a quoted URL string |

These are 11 occurrences, not 11 vulnerabilities. JSON-LD is structured data; appearance inside a script element does not itself establish executable JavaScript injection. Subsequent decoding or DOM insertion by scripts remains a separate review question.

See [all HTML-marker excerpts](entry-3-contexts.md); the full response is retained locally.

## SVG request and response evidence

Decoded s value:

```html
<svg onload="console.log('HY-XSS-EXEC-001')"></svg>
```

- Entry 4: 2026-11-17T12:36:58.634Z; status 200; 35 response matches. [Contexts](entry-4-contexts.md).
- Entry 5: 2026-11-17T12:37:20.684Z; status 200; 35 response matches. [Contexts](entry-5-contexts.md).

In the search input values, the SVG payload is HTML-encoded, including angle brackets, double quotes and apostrophes. Additional occurrences appear in a hidden search field, product add-to-cart URLs and pagination URLs, alongside the metadata/redirect/configuration contexts. Those URLs were not followed. The tested string is data in these inspected source locations; no raw injected SVG element was established. This is a bounded source observation, not a comprehensive DOM-XSS clearance.

## Evidence and limitations

- [Request register](request-register.json): timestamps, decoded inputs, status and response hashes; no request cookies or authentication headers included.
- Current console screenshot reviewed locally: later plain-marker page only, not proof of historical SVG execution or non-execution. See [screenshot review](SCREENSHOT-REVIEW.md).
- Raw Chrome sanitized HAR remains local in Downloads as healthyaa-search-evidence-2026-11-17.har. Browser sanitization is not a guarantee that response bodies contain no identifiers; it has not been published.
- Full response files are local inert text evidence and can contain public runtime nonces/configuration. Review before external publication.
- Publication update: the user subsequently requested this evidence be pushed to GitHub. This package publishes bounded response excerpts, the cookie-free request register, screenshot review and provenance hashes. Original screenshots, full HTML responses and the HAR remain local to avoid publishing cookie values, runtime identifiers and unrelated browser details.

## Next verification needed

For a runtime conclusion, capture a fresh execution test with the outgoing full s value, matching response, live DOM and console recorded for that same navigation. Also inspect the autocomplete response separately. This review reused existing evidence rather than rerunning the test. Existing evidence supports 'payload submitted and encoded in inspected response contexts; XSS execution not demonstrated'.
