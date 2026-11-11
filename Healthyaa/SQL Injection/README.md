# Healthyaa — SQL injection testing record

Recorded activity: 10 November 2026. Compiled: 11 November 2026 (Europe/London).

**Result: SQL injection was not demonstrated by the evidence supplied in this chat.** This is a limited manual testing record, not a clean bill of health or a completed penetration test. No database extraction, authentication bypass, data modification, or operating-system execution was demonstrated.

The user identified the Healthyaa staging site (`https://kaviarasank64.sg-host.com`) as authorized for testing. This compilation documents user-run requests, screenshots, reported observations, and guidance from the conversation. No new website requests were executed while preparing this folder. Embedded third-party services are not automatically included in staging authorization.

## Contents

- [Test results](TEST-RESULTS.md): observed outcomes, evidence, and limitations.
- [Commands and payloads](COMMANDS-AND-PAYLOADS.md): historical examples, with execution status distinguished from suggestions.
- [Interpretation and follow-up](INTERPRETATION-AND-FOLLOW-UP.md): validation versus injection, source review, and remaining work.
- [Evidence inventory](evidence/README.md): provenance and handling notes.
- [SHA256SUMS.txt](SHA256SUMS.txt): checksums for this folder's documentation and evidence.

## Source methodology

The discussion began with the repository's [SQL injection detection guide](../../Skills/web/offensive-sqli/SKILL.md#detection). Its payloads are query-context dependent; their presence in a request does not establish execution. This folder is an assessment record, not a new runnable skill.

## Summary

| Test | Observation | Assessment |
|---|---|---|
| Example `/products?id=12` | HTTP 404 | Hypothetical path was not found |
| Homepage numeric boolean probes | Both probes returned empty HTTP 301 responses | Redirect behavior, not evidence of boolean SQL evaluation |
| Following true-probe redirect | One redirect, HTTP 200, page downloaded | Successful HTTP retrieval only |
| Product search | User reported baseline products; true and false probes both no products | No boolean distinction demonstrated |
| Embedded booking form | Google Forms displayed submission confirmation | Accepted text does not establish SQL execution or missing validation |
| Password-reset field | HTTP 200 JSON with application error and invalid username/email notice | No SQL database error or confirmed SQL injection |

Cookies, analytics identifiers, local account paths, and complete raw browser headers are not republished. Original source files remain unchanged locally. Evidence excerpts are explicitly marked as excerpts; suggested tests are not presented as completed work.
