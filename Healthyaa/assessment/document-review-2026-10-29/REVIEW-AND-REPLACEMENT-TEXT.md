# Healthyaa penetration-test draft — review and replacement text

Reviewed: 29 October 2026. Source: `Healthyaa Penetration Test.pages`, supplied by Harish. This review covers all four entries and all six full-size screenshots embedded in the file. It evaluates the supplied historical evidence; it is not a new live test. The original Pages document has not been edited.

## What to improve first

Your screenshots provide useful evidence. Add the method and expected result so a reviewer can understand how the evidence was obtained and why it supports your conclusion.

Use this sequence for every check:

1. **Objective:** What question were you trying to answer?
2. **Method / actions performed:** What did you actually do? Include tool, URL, login state, commands or menu path.
3. **Expected result:** What must happen for this particular check to pass?
4. **Actual result:** What did the response or screenshot show?
5. **Assessment:** Pass, partial pass, fail, or inconclusive, with the reason and limits.
6. **Action and retest:** What needs changing or investigating? What evidence will close the item?

Completing a test and passing a test are separate. A correctly performed test may find a failed control. Also, “no exploit demonstrated” does not mean a control passed; it describes the limits of what was tested.

Suggested status definitions:

- **Pass:** The stated expected result was observed for the tested case.
- **Partial pass:** Some separately identified requirements were met and others were not.
- **Fail:** A stated requirement was not met. This is not automatically a confirmed exploitable vulnerability.
- **Inconclusive / incomplete:** Evidence is insufficient to decide or planned verification remains outstanding.
- Record **retest pending** separately from the original result after a fix is proposed or applied.

The header baseline below is a proposed review criterion. Record agreement with your reviewer before treating it as an organisational requirement; do not imply it was a pre-existing mandatory policy.

## Fix the numbering

Your Pages document uses HYA-01 for homepage headers and HYA-02 for redirects. In the earlier assessment, HYA-01 means administrator MFA and HYA-02 means plugin updates. This could cause someone to close the wrong finding.

Use **HT-01 to HT-04 for test records** and retain **HYA-01 to HYA-08 for the earlier findings**:

| Draft entry | Suggested test ID | Related assessment finding |
|---|---|---|
| Check 1: homepage response headers | HT-01 | HYA-04 |
| Check 2: HTTP-to-HTTPS redirect | HT-02 | Positive control; supports transport review |
| Check 3: PHP compatibility | HT-03 | HYA-03 |
| Check 4: homepage header check | HT-04 | HYA-04; repeat observation of HT-01 |

Checks 1 and 4 substantially overlap. You can retain both as two observations at different times, or combine them under one header-review check with both evidence references. They are not two independent vulnerability discoveries. The draft does not yet document all eight earlier findings.

## Results supported by your document

| Test | Assessment | Why | What remains |
|---|---|---|---|
| HT-01: homepage response and headers | Partial pass against the proposed header baseline | HTTP 200 and nosniff are present; four reviewed headers are absent | Correct wording, add retrieval method, cross-reference HT-04 and plan header verification |
| HT-02: HTTP redirect | Pass for the tested root URL | HTTP 301 points to the matching HTTPS homepage | Correct the target URL and explain the method; broader redirect/TLS tests remain separate |
| HT-03: PHP compatibility | Incomplete overall; Template Kit Import update compatibility is reported failing by WordPress | PHP 8.2.35 shown; Template Kit Import 1.0.17 update warning shown; Contact Form 7 screenshot shows only installed 6.1.7 | Capture exact update requirements and full notices, investigate the warning, then staging validation |
| HT-04: homepage header recheck | Partial pass; four header-presence subchecks fail | Same reviewed headers missing, nosniff present | Correct date, record per-header results and validate any later remediation |

## HT-01 — replacement text

**Title:** HTTPS homepage response and security-header review  
**Target:** https://healthyaa.co.uk/  
**Context:** Anonymous request; production homepage.  
**Evidence:** Screenshot of `cat home.headers`; embedded file `pasted-movie-24.png`.  
**Response Date header:** 28 October 2026, 12:18:27 GMT.  
**Recorded test time:** Confirm from your notes. The draft says 11:30am, which differs from the response Date header. Keep collection time and server response time as separate fields when they differ.

**Actions performed:** I used curl in Terminal to retrieve the HTTPS homepage and save its response headers and HTML locally. I then ran `cat home.headers` to display the saved response headers and compared them with the headers under review. The curl retrieval step is supported by our earlier working conversation; this particular screenshot shows the file-reading step. Include your original retrieval command or raw evidence file alongside the screenshot.

**Expected result:** A successful homepage response and the agreed security-header baseline. Assess each header separately rather than treating HTTP 200 as a security pass.

**Actual result:** The saved response returned HTTP/2 200 with `Content-Type: text/html; charset=UTF-8` and `X-Content-Type-Options: nosniff`. The response did not include `Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`, or `Referrer-Policy`.

**Assessment:** Homepage retrieval and the nosniff subcheck passed. The four named header-presence subchecks did not meet the proposed baseline. No XSS or clickjacking exploitation was performed or demonstrated by this header review. These results apply to this response only.

**Next action:** Link this evidence to HT-04/HYA-04. Review policy requirements and other relevant page responses before implementing headers and retesting.

**Specific correction:** Replace “included no X-Content-Options: no sniff” with “included `X-Content-Type-Options: nosniff`.” The original sentence incorrectly implies the header was absent and uses the wrong header name.

## HT-02 — replacement text

**Title:** HTTP-to-HTTPS homepage redirect  
**Target:** http://healthyaa.co.uk/ — the starting URL uses HTTP.  
**Evidence:** `http-redirect.headers`, `http-redirect.body`, and screenshot `pasted-movie-26.png`.  
**Response Date header:** 28 October 2026, 12:41:05 GMT. The draft's 12:35pm may be a start time; verify rather than silently replacing it.

**Actions performed:** I sent an anonymous GET request to the HTTP homepage using the following curl command. I saved the headers and response body, then displayed the headers. I did not enable automatic redirect following, so the output shows the initial HTTP response.

```bash
curl --silent --show-error --max-time 30 \
  --dump-header http-redirect.headers \
  --output http-redirect.body \
  http://healthyaa.co.uk/

cat http-redirect.headers
```

**Expected result:** The HTTP root URL redirects to the equivalent HTTPS URL on the intended host.

**Actual result:** The server returned `HTTP/1.1 301 Moved Permanently` with `Location: https://healthyaa.co.uk/`.

**Assessment:** Pass for the root-URL redirect check. The command demonstrates a redirect instruction; it does not itself follow that redirect or audit the TLS configuration. A separate HTTPS request returned HTTP 200. Other paths and hosts were not covered by this case.

**Next action:** No correction is indicated for this specific redirect. Keep HSTS review separate: passing the redirect check does not close the missing-HSTS observation.

## HT-03 — replacement text

**Title:** PHP version and plugin-update compatibility review  
**Context:** Authenticated WordPress configuration inspection.  
**Evidence:** Site Health screenshot `pasted-movie-28.png`; Contact Form 7 row `pasted-movie-30.png`; Template Kit Import row and warning `pasted-movie-32.png`.  
**Time:** Site Health shows 28 October 2026, 14:47:39 UTC. Exact acquisition times of the plugin screenshots are not shown; add them from your notes if known.

**Actions performed:** I inspected WordPress Tools → Site Health → Info → Server and recorded the PHP version. I then inspected Plugins → Installed Plugins and recorded the installed versions and any visible update warnings for Contact Form 7 and Template Kit Import.

**Expected result:** The server PHP version meets the documented requirements for the plugin versions selected for update, and those updates work after staging validation. Version inventory alone cannot establish functional compatibility.

**Actual result:** Site Health reports PHP 8.2.35. Contact Form 7 is installed at 6.1.7; its screenshot does not show an update warning or a required PHP version. Template Kit Import is installed at 1.0.16. WordPress advertises version 1.0.17 and warns that it does not work with the site's PHP version. The minimum PHP requirement for that update is not visible in the screenshot.

**Assessment:** Incomplete overall. A reported update-compatibility problem is evidenced for Template Kit Import. Contact Form 7 update compatibility cannot be decided from its included screenshot. The earlier assessment recorded a Contact Form 7 warning, but the current document needs that full evidence before making the same claim. No update, PHP migration, or post-change functional test is evidenced here.

**Next action:** Capture full update details for both plugins, including the exact required PHP version and target version. Compare requirements with the PHP version WordPress actually uses. If the requirement appears satisfied despite the warning, investigate update metadata and the environment with the host/vendor before assuming an upgrade is needed. If migration is required, back up, use an isolated staging copy, select a mutually supported version, update individually, and test forms, templates and ecommerce functionality with synthetic data. Keep customer email and live fulfilment isolated.

**Closure evidence:** Verified requirements, final PHP/plugin versions, resolved warnings or a documented explanation, functional test results, and a successful production retest after the approved change. Do not describe PHP 8.2.35 as vulnerable merely because an update warning appears.

## HT-04 — replacement text

**Title:** Repeat HTTPS homepage security-header review  
**Target:** https://healthyaa.co.uk/  
**Context:** Anonymous GET; production homepage.  
**Evidence:** `hya04-home.headers`, `hya04-home.html`, screenshot `pasted-movie-34.png`.  
**Response Date header:** 28 October 2026, 16:11:32 GMT. The draft says 28 September 2026, 3:45pm; correct the month and reconcile the time against your collection notes.

**Actions performed:** I retrieved the homepage using curl, saved the headers and HTML, and displayed `hya04-home.headers`. I checked for the following five headers. The full command was recorded in the working conversation; retain it in the report for reproducibility.

```bash
curl --silent --show-error --max-time 30 \
  --dump-header hya04-home.headers \
  --output hya04-home.html \
  https://healthyaa.co.uk/

cat hya04-home.headers
```

| Subcheck | Evidence | Result against proposed baseline |
|---|---|---|
| Successful homepage response | HTTP/2 200 | Pass for retrieval |
| X-Content-Type-Options | nosniff | Pass |
| Strict-Transport-Security | Absent | Fail: header absent |
| Content-Security-Policy | Absent | Fail: header absent |
| Framing restriction via X-Frame-Options or CSP frame-ancestors | Neither header present | Fail: no header-based framing restriction observed |
| Explicit Referrer-Policy header | Absent | Fail: explicit header absent |

**Observation:** An anonymous HTTPS GET returned HTTP 200. The response contained `X-Content-Type-Options: nosniff` but did not contain the other four reviewed headers. This repeats the earlier homepage observation. No exploitation was demonstrated.

**Assessment:** Partial pass overall against the proposed baseline. This is a hardening observation, not proof of XSS, clickjacking, or data leakage. The presence of the legacy `X-XSS-Protection` header does not establish protection against XSS. Absence of an explicit Referrer-Policy header does not mean browsers send unrestricted referrers. This header-only review also does not inspect possible HTML-delivered policies or all browser behaviour.

**Next action:** Agree an appropriate header policy with the site maintainer. Check account and checkout responses separately, including redirects and login context. Test policy changes on staging, including payment integrations and legitimate embedding. Introduce CSP carefully, initially observing violations where appropriate before enforcement. Plan HSTS duration and any subdomain scope deliberately. Retest the delivered headers and browser behaviour after deployment. The item remains open until evidence verifies the chosen controls.

## Presentation and evidence improvements

- Add a scope statement: draft, production site, limited manual checks, dates, and whether requests were anonymous or authenticated. State that this is not a completed full penetration test.
- Keep test IDs, finding IDs and screenshot labels distinct.
- Add captions to all screenshots: evidence ID, target/page, relevant result and time where known. Retain raw headers as well as images.
- Server Date headers are response timestamps, not independently verified capture timestamps. Do not invent missing times.
- Replace repeated blank lines with paragraph spacing and page breaks. Keep each screenshot next to the method and observation it supports.
- Use exact header names. Replace “X-Frame” with `X-Frame-Options` and “strict transport security” with `Strict-Transport-Security` where naming the header.
- Separate recommendations from completed actions. “Update PHP on staging” is a next step until you have actually done and verified it.
- Record reviewer feedback, owner, action status and retest evidence. An accepted report does not automatically mean the website control passed.

## Copyable template for later checks

**Test ID / related finding:**  
**Title / objective:**  
**Target and environment:**  
**Date, time and timezone:**  
**Authentication context:**  
**Tool and actions performed:**  
**Expected result / pass criterion:**  
**Actual result:**  
**Evidence references:**  
**Assessment and limitations:**  
**Recommended action / owner:**  
**Retest date, evidence and status:**

For checks requiring a login or request credentials, redact secrets from report copies while retaining protected originals according to your team's evidence-handling process.
