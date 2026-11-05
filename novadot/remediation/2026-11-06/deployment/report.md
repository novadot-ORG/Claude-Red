# NovaDot production deployment — 6 November 2026

**Result: deployed and verified. The three agreed website actions are closed for the tested scope.** The user explicitly instructed production deployment. No database, mail configuration, private credential, enquiry-handler or sibling-host changes were made. No real test enquiry was sent.

## Release and scope

Source: `/Users/apple/git/novadot_website`, branch `agent/porcelain-ledger-website`, base HEAD `6148cee25534a80cc039d02c6e9710fc1e743cae` plus the preserved dirty worktree and reviewed fixes. Source has no remote; source patches and evidence are retained in this report repository.

Production: SiteGround `novadot.co.uk`, public root `/home/customer/www/novadot.co.uk/public_html`, static Astro pages and the existing PHP enquiry service. No database is used or changed by this release.

Installed release `2026-11-05T18-49-53-554Z`, archive SHA-256:

`3e8a2a9a435d5004ec8fac199c9825e1fd04104eb38e3b80c15a08de3d8e9123`

The originally prepared archive contained a Finder `.DS_Store` file. The finaliser now removes Finder/AppleDouble metadata and validation rejects it. Fresh production verification passed; all 67 remaining public files are byte-identical to the earlier tested candidate. The earlier archive was not deployed. See the [production log](verify-production-package.log), [final manifest](release-manifest.json), [follow-up patch](deployment-followup.patch) and [source hashes](source-followup-manifest.json).

The live baseline matched the planned change. Visible text on all 13 pages was unchanged. Seventeen files were installed: three new JavaScript assets, 13 HTML files and `.htaccess`. Existing assets were retained. Each destination was checked again immediately before cutover. Assets went first, HTML next and the restrictive CSP last, with atomic per-file replacement. An independent read-only review found no material deployment blocker. See [activation code](activate-remote.py), [receipt](deployment-receipt.json) and [content comparison](content-comparison.json).

## Verification results

| Check | Result |
|---|---|
| Server files | **Passed:** all 67 SHA-256 hashes match the final package; Finder metadata absent. |
| Rollback copies | **Passed:** all 14 overwritten pre-release files match recorded baseline hashes; backup directory mode 700. |
| Public static files | **Passed with a documented hosting transformation:** 63 exact HTTPS hashes; `robots.txt` differs only by the provider's `Crawl-delay: 10` line. |
| CSP and security headers | **Passed:** all 13 HTML route responses match the generated CSP; all 13 direct `.html` URLs also match and supply nosniff/no-cache headers. |
| Missing-page response | **Passed:** HTTP 404, exact custom error-page bytes, correct CSP. |
| Enquiry preparation | **Passed:** GET returns HTTP 200, a nonempty token and no-store headers. Token values discarded; no POST/mail was sent by this HTTP check. |
| Browser behaviour | **Passed:** native Brave Computer Use observed both forms initialise, display required-field errors and focus the first invalid field. The live homepage diagnostic advanced through all three steps. Chrome also rendered the live homepage. |
| Publication/routing | **Passed:** HTTP and www requests resolve to canonical HTTPS; case-study route remains noindex/unavailable. Eleven sitemap routes remain indexable; approved client logos retained. |
| Analytics integration | **Passed for source/release integrity:** every HTML page contains the configured pinned tag. The earlier public asset integrity check remains applicable. No analytics dashboard/event-receipt audit was performed. |

Evidence: [final server/backup hashes](server-verification-final.json), [HTTPS checks](live-verification-final.json), [all direct HTML headers](direct-html-final.json), [routing](routing-checks.json). Browser observations are recorded above; no browser trace was retained. Earlier mocked success/CSP rejection tests and actual email-delivery/reply evidence remain linked from the parent report.

## Hosting correction discovered during deployment

Initially, normal directory URLs received the new policy, but direct HTML URLs bypassed Apache and omitted its headers. The [initial evidence](live-verification-initial.json), [direct-URL samples](direct-html-headers.json) and [header comparison](header-followup.json) preserve that result.

Through native Computer Use, disabled **NGINX Direct Delivery for `novadot.co.uk` only**. SiteGround displayed a success notification; subsequent HTTPS checks confirmed the correction. Other host switches were untouched. The setting routes static requests through Apache so the site's header/cache rules apply; it trades the direct-delivery optimisation for consistent policy enforcement. This requirement is supported by [SiteGround's header guidance](https://www.siteground.com/kb/cross-origin-resource-sharing-cors) and [Direct Delivery documentation](https://www.siteground.com/tutorials/supercacher/nginx-direct-delivery).

The main host's dynamic cache was then flushed. `robots.txt` still gained only `Crawl-delay: 10`, including on a cache-MISS request, while its server bytes matched the package. This is consistent with [SiteGround's documented default crawl delay](https://www.siteground.com/es/kb/crawl-delay-en-servidores), not evidence of a stale deployed file. The [exact observed response](robots-followup.json) retains the intended `Allow: /` and sitemap. No broader SEO change was made.

## Recovery and remaining ownership

Verified rollback directory: `/home/customer/www/novadot.co.uk/.security-release-2026-11-06/before`. Stage and plan are in its parent, outside public access. Keep these and earlier backups. If rollback is needed, confirm current hashes against this release, restore the previous `.htaccess` first and then its matching HTML from the backup; new immutable assets can remain. No database restore is needed. Retaining Direct Delivery off preserves header enforcement during rollback.

The owner should monitor normal enquiries and site behaviour. Future releases must preserve the hosting setting and deploy generated HTML/CSP together. Broader organisation testing remains separate. No repeat of the completed real mailbox-delivery tests is required.
