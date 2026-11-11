# Test results and chronology

## SQLI-01 — Example endpoint and homepage baseline

The first command targeted `/products?id=12`, an illustrative endpoint rather than a verified application route. It returned HTTP 404, 287865 bytes, in 1.977251 seconds. The user then requested the homepage with `id=12`, receiving HTTP 200, 516062 bytes, in 1.514481 seconds. Reusing `baseline.html` overwrote the earlier 404 body.

There is no evidence that the homepage uses `id` as a database selector. A successful HTTP response does not establish that a parameter is meaningful.

## SQLI-02 — Numeric true/false probes and misleading diff

Inputs: `id=12 AND 1=1` and `id=12 AND 1=2`.

Both returned HTTP 301 and zero-byte bodies (1.141172 and 1.132805 seconds respectively). Comparing `baseline.html` against `true.html` printed `@@ -1,4837 +0,0 @@` followed by the baseline HTML with minus signs. This means 4837 lines exist in the first local file and none in the second. It does not mean website content or database records were deleted. Both probe bodies were empty, so a comparison between them cannot demonstrate SQL execution.

## SQLI-03 — Redirect investigation

A header-only display using `-D - -o /dev/null` showed `x-redirect-by: WordPress`, `content-length: 0`, and a Location ending in `/?id=12%20AND%201%3D1`. The destination retains the input, with URL-encoded spaces and equals sign. URL normalization is a possible explanation; the response alone does not establish the redirect's underlying code path.

Following redirects with `-L --max-redirs 5` returned HTTP 200 after one redirect and 516138 bytes. This was the true-condition request only; the provided transcript did not establish a matched post-redirect false-condition comparison. Differences in body size alone are insufficient evidence.

## SQLI-04 — Browser-copied homepage request and search discovery

The later browser-copied curl command requested `/` without a search parameter. It included browser headers/cookies and `--insecure`, but no output-file option, so the entire HTML response printed in Terminal. `--insecure` disables TLS certificate verification; it is not a SQL injection testing requirement.

The supplied terminal transcript has 9753 lines, mostly page source and diff output. Its HTML identifies a GET product-search form with `s`, `post_type=product`, and `dgwt_wcas=1`. It also contains a separate ShopEngine advanced-search form. These are observed frontend references, not proof of which backend query each request executes.

The plugin-list screenshot identifies active FiboSearch — AJAX Search for WooCommerce, version 1.34.3. No vulnerability or version-specific advisory was established. Live suggestions and submitted search results may use different handlers.

## SQLI-05 — Product-search boolean comparison

The advised requests used `s=vitamin` as the baseline, then `vitamin' AND 1=1 -- ` and `vitamin' AND 1=2 -- `, retaining the form's other parameters. The user explicitly reported products for the baseline and no products for both probes. A screenshot shows the no-products message, but not which saved file was open. The identification of both probe outcomes therefore rests on the user's report, not independently inspected raw response files.

Both probes behaving alike is consistent with literal search text handling or a mismatch with the SQL query structure. Neither explanation is proven. No boolean SQL execution was demonstrated. The “Our Popular Tests” footer is separate from search results.

Subsequently suggested quote and parenthesis variants have no individually supplied outcome and must not be counted as completed tests.

## SQLI-06 — Booking form and educational images

One supplied photo shows `select id=1 from employee` typed in a “Tests Needed” field. Another is a whiteboard diagram of an application/database interaction. These do not establish a table named `employee` or a query execution path.

In SQL dialects that permit it, `SELECT id=1 FROM employee` evaluates a comparison for each row; `SELECT id FROM employee WHERE id=1` selects matching IDs. Neither runs merely because it is typed into a form.

A later screenshot shows Google Forms branding and “Your response has been recorded.” It demonstrates submission acceptance by an embedded form. It does not demonstrate SQL execution, absent server-side validation, or access to the WordPress database. No downstream custom database integration was established.

## SQLI-07 — Password-reset probe

The Burp screenshot shows multipart fields including:

- `user_login`: `test@test.com' AND '1'='2'-- -`
- `_xoo_el_form`: `lostPassword`
- `action`: `xoo_el_form_action`
- `display`: `popup`

The request path is outside the visible screenshot and is not inferred here. The response is HTTP/2 200 with JSON containing `error: 1`, `error_code: null`, and an HTML notice reading “Invalid username or email.”

This is an application-level failure response, not a visible SQL syntax error. HTTP 200 refers to delivery of the response, not success of the reset or injection. There is no supplied valid-account baseline or matching true-condition response. The application may reject the format or treat the whole string as an unmatched identifier; database evaluation is not established. A successful password-reset baseline can send mail, so further work should use a designated staging account.

## Overall disposition

No confirmed SQL injection finding is supported by these records. Do not assign exploit impact or claim the site is secure. Reproduction must control redirects, request context, normal application behavior, and dynamic content before attributing differences to SQL.
