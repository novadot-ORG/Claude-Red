# Initial inspection and evidence record

Historical record before the user supplied runtime evidence. Superseded for current test status by the [17 November captured-evidence report](evidence/2026-11-17/REPORT.md).

## 1. Public search interface

The current chat's public-page review observed search prompts including “Search from 950+ Blood Tests...” and “Search for Products...”. These establish visible input surfaces only. Autocomplete behaviour, the submitted results page, and output encoding were not exercised in that review.

On 17 November, the archived [homepage HTML](../../assessment/home.html) was inspected locally. In that historical capture:

- Lines 888–900 show a GET search form, an input named `s`, and the blood-test search placeholder.
- Lines 921–922 contain hidden fields `post_type=product` and `dgwt_wcas=1` (see the source excerpt below for exact context).
- Line 299 references a stylesheet under `ajax-search-for-woocommerce`; this is an implementation clue, not authoritative current version or vulnerability evidence.

The form submits to the site's root. The live autocomplete endpoint was not established and must be discovered from actual browser traffic rather than guessed.

The [bounded search-form excerpt](evidence/search-form-excerpt.txt) is copied from the existing historical capture, with original line numbers. The extraction is new; the underlying page capture is historical. It contains no new network response.

## 2. Earlier security observations relevant to interpretation

The [26 October baseline review](../../assessment/REVIEW.md) records a public homepage response without a CSP header or observed meta CSP. The [captured headers](../../assessment/home.headers) and HTML support that historical observation. Missing CSP is a hardening issue, not proof of XSS; it says nothing definitive about today's search responses.

The same baseline review discusses the [assistant JavaScript](../../assessment/assistant.js): message text uses `textContent`, several template fields are escaped, and response-provided link URLs required further review. These observations concern the assistant component, **not the product-search renderer**. They cannot establish that search is safe or vulnerable. Attacker control of those URLs was not demonstrated.

The [manual draft review](../../assessment/document-review-2026-10-29/REVIEW-AND-REPLACEMENT-TEXT.md) also explains that header-only checks do not demonstrate XSS and that `X-XSS-Protection` does not establish protection.

## 3. Hacky lab 164

Source: https://hacky.uk/lab/164

The browser-visible page in this chat identified the lab as **Client-Side Validation Bypass**, created by paj, rated Novice (1 point). Its stated objective was `alert(document.cookie)`. The page linked a solution video and required login to submit a solution.

The launch interaction did not open the exercise. No working lab input, underlying implementation, successful payload, or completion result was observed. The video was not reviewed. This paragraph is a transcription of the chat's browser observation, not a saved screenshot or independent lab execution record.

Applicability to Healthyaa is conditional: if search relies on browser checks, a direct request can test the server's handling independently. Bypassing a browser restriction alone is not XSS; unsafe rendering and browser execution must also be demonstrated. No equivalent weakness was confirmed on Healthyaa.

For Healthyaa testing, use a harmless console marker rather than reading cookies. The lab objective is educational context, not a requirement to access Healthyaa session data. HttpOnly cookies are not readable through `document.cookie`, and an empty cookie alert does not disprove XSS.

## 4. Evidence boundaries

- Earlier report dates and server timestamps are retained; no historical capture is presented as a fresh 17 November response.
- Discussion of test inputs is a plan, not proof that the user ran them.
- No search execution finding, severity rating, fix, or successful retest is asserted.
- Newly added files contain documentation and a public-markup excerpt, not credentials, customer records or authenticated traffic.
