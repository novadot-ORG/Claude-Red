# Security Policy

`codex-red` is an offensive security tooling library. Its content describes attack methodologies for use by authorized red team operators, penetration testers, and security researchers.

## Intended Use

These skills are intended for:

- Authorized penetration testing engagements with documented scope and rules of engagement
- Bug bounty programs with explicit written permission for the techniques described
- CTF competitions and security training environments
- Independent vulnerability research with responsible disclosure

These skills are **not** intended for unauthorized access to systems you do not own or do not have explicit, written permission to test. Misuse may violate computer-misuse laws in your jurisdiction (CFAA in the US, Computer Misuse Act in the UK, equivalent statutes elsewhere).

## Reporting a Vulnerability in This Fork

If you discover a security issue in this repository — for example a malicious payload accidentally committed, a credential leaked in an example, a typosquat-prone install path, or an unsafe shell command in `install.sh` — please report it privately rather than opening a public issue.

For issues introduced by this fork, contact the NovaDot repository maintainers privately through an established channel. For issues in the original library, the upstream contact is **security@snailsploit.com**. Do not publish credentials or client data in an issue.

Please include:

- Affected file(s) and commit hash
- A description of the issue and its impact
- Reproduction steps if applicable
- Any suggested remediation

Response timelines for this fork are determined by its maintainers.

## Reporting a Vulnerability Found Using This Library

If you discover a vulnerability in a third-party product or service while using `codex-red`'s methodologies, follow that vendor's responsible disclosure process. The [`offensive-reporting`](Skills/utility/offensive-reporting/SKILL.md) skill includes guidance on responsible disclosure, evidence handling, and report writing.

If the vendor has no published security contact:

- Try `security@<vendor-domain>`, then their PSIRT page, then `report` mailing addresses
- For ICS/OT vendors, escalate via [CISA ICS-CERT](https://www.cisa.gov/uscert/ics)
- For broad-impact bugs, request a CVE via [MITRE CNAs](https://www.cve.org/PartnerInformation/ListofPartners)
- Allow at least 90 days before public disclosure unless the vulnerability is being actively exploited

## Supply Chain Integrity

Check the repository origin and inspect commit signatures when assessing provenance:

```bash
git remote -v
git log --show-signature
```

If you receive a `codex-red` archive from a third party (mirror, pastebin, package manager), compare it with this fork and its upstream history before using it. Upstream authorship does not imply endorsement of fork changes.

## Scope

| In scope | Out of scope |
|---|---|
| Issues in repository content (skills, scripts, install logic) | Vulnerabilities in third-party tools mentioned in skills |
| Malicious payloads in examples | OpenAI or other model-provider services (use the provider reporting channel) |
| Unsafe installation defaults | Bugs in tools you find using this library |
| Leaked credentials in example traffic | Bugs in your own implementation of techniques described |

## Acknowledgements

We credit researchers who report security issues responsibly in the project [CHANGELOG](CHANGELOG.md). Let us know if you'd prefer to remain anonymous.
