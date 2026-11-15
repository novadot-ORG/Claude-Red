# Healthyaa — white-box SQL injection testing checklist

Prepared: 15 November 2026. **Status: planned checks, not completed findings.**

Scope: authorized Healthyaa staging application, its relevant PHP source, database queries, database account privileges, and configuration. This document records the requested review areas with technical corrections. No logging, server configuration, permissions, or application code was changed when preparing it.

## 1. Source code review

The booking form accepted SQL-like text, but this does not establish that the text executed as SQL or that validation is absent. The supplied confirmation identifies an embedded Google Form; identify its destination and any downstream integration before attributing behavior to WordPress. Free-text acceptance may be intentional.

The XOO Easy Login password-reset response reported “Invalid username or email.” That is an application error, not a SQL error. Review its actual handler rather than assuming that receiving a request means executing its contents as SQL.

- [ ] Identify the relevant form destination, request parameters, and backend handler.
- [ ] Trace product search, XOO password reset, registration, and custom integrations separately.
- [ ] Inspect theme code, custom plugins, must-use plugins, and relevant plugin hooks.
- [ ] Follow user-controlled values into database operations, including raw SQL fragments.
- [ ] Verify server-side validation against each field's business requirements.
- [ ] Verify safe query construction independently of validation; do not rely on SQL keyword blocking.
- [ ] Record file/line references, the input source, database operation, and actual protection.

A received or stored string is not proof of injection. Confirm whether input can change query structure.

## 2. Database query audit

Temporarily instrument staging using synthetic test data. Modify existing constants rather than adding duplicate definitions, before WordPress bootstraps:

```php
// Staging only. Replace with an existing, private, writable log path.
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', '/private/path/healthyaa-debug.log');
define('WP_DEBUG_DISPLAY', false);
define('SAVEQUERIES', true);
```

`WP_DEBUG_LOG` records errors/notices and explicitly logged messages. **SAVEQUERIES does not automatically write every SQL query to `/wp-content/debug.log`.** It collects queries, timings, and callers in `$wpdb->queries` for the current request. Inspect that collection through a debugger or restricted, request-scoped instrumentation before the request ends. A later CLI request cannot retrieve the previous web request's collection. Connections outside `$wpdb` need separate instrumentation. See [WordPress debugging documentation](https://developer.wordpress.org/advanced-administration/debug/debug-wordpress/).

- [ ] Capture a normal baseline, then each approved probe individually; correlate request, response, query, and caller.
- [ ] Keep query evidence outside publicly accessible paths; redact credentials, tokens, personal data, and real account values before publication.
- [ ] Record queries absent because validation rejected input before database access.
- [ ] Disable temporary query collection and restore configuration after the test.

### Inspect construction, not just backslashes

Do not use “the quote appears as `\'` rather than `'`” as a pass/fail rule. SQL literals legitimately contain quote delimiters; log serialization, connection settings, and SQL modes affect representations. Trace how the specific input is handled and whether it remains a value. An escaped-looking log line alone does not prove safety.

Flag direct interpolation such as:

```php
// Unsafe example: user input interpolated into SQL.
$sql = "SELECT ID FROM {$wpdb->posts} WHERE post_title LIKE '%$input%'";
```

For literal substring matching, review for this pattern:

```php
$pattern = '%' . $wpdb->esc_like($input) . '%';
$sql = $wpdb->prepare(
    "SELECT ID FROM {$wpdb->posts} WHERE post_title LIKE %s",
    $pattern
);
$rows = $wpdb->get_results($sql);
```

`esc_like()` escapes LIKE wildcard characters; it is not a replacement for SQL preparation. Apply it before `prepare()`. Dynamic column names, sort directions, and other SQL structure require separate controls, such as explicit allowlists. See [WordPress esc_like reference](https://developer.wordpress.org/reference/classes/wpdb/esc_like/).

## 3. Second-order SQL injection

Second-order injection occurs when input is stored and later reused unsafely in a new SQL query. Safe initial storage does not make later concatenation safe.

- [ ] Trace registration and profile values from storage through retrieval to every subsequent database operation.
- [ ] Include administrative searches, reports, exports, scheduled jobs, and custom integrations where relevant.
- [ ] Use a synthetic staging account and identifiable test values; document both the initial write and later consumer.
- [ ] Verify safe query construction at each later use, even when the value came from the database.
- [ ] Capture evidence of the second query and its caller; do not report second-order SQL injection merely because SQL-like text was stored.

## 4. Database user permissions audit

Inspect the account WordPress actually uses, not only an administrator account. Run read-only checks in the appropriate MySQL session:

```sql
SELECT CURRENT_USER(), USER(), DATABASE();
SHOW GRANTS FOR CURRENT_USER;
```

`CURRENT_USER()` identifies the matched privilege account. On versions supporting roles, inspect active roles and their effective grants as well; direct grants alone may not describe all access. See [MySQL SHOW GRANTS documentation](https://dev.mysql.com/doc/refman/8.4/en/show-grants.html).

- [ ] Scope application access to the intended application database; investigate access to unrelated application databases. Metadata visibility is not automatically unauthorized data access.
- [ ] Flag `FILE`, `SUPER`, broad administrative/dynamic privileges, and `GRANT OPTION` for removal unless explicitly justified.
- [ ] Review `EXECUTE`; ordinary application operation may not require stored routines, but validate actual dependencies before revoking it.
- [ ] Review `ALL PRIVILEGES` at its granted scope. Global `*.*` access differs substantially from grants on the application's database alone.
- [ ] Define minimum runtime privileges and separately account for installation, migrations, and updates that may require schema changes.
- [ ] Have the database administrator review proposed revocations and test application functionality before applying them.

Do not blindly revoke privileges from a production account. This checklist performs an audit, not automatic remediation.

## 5. WordPress and PHP security configuration review

Inspect `wp-config.php` privately; do not commit database passwords, salts, or the whole configuration file.

| Setting | Review criterion |
|---|---|
| `DB_HOST` | Record local/socket versus remote database topology. A remote database is not inherently a flaw; review network restrictions and transport protection as appropriate. |
| `WP_DEBUG` | Normally false in production; temporary staging diagnostics must be removed after review. |
| `WP_DEBUG_DISPLAY` | False when diagnostics are enabled so errors are not sent to visitors. |
| `DISALLOW_FILE_EDIT` | True to disable the dashboard's theme/plugin code editors. This does not prevent every possible filesystem write or plugin installation. |
| `SAVEQUERIES` | Disabled after investigation; collection adds overhead. |

See [WordPress hardening guidance](https://developer.wordpress.org/advanced-administration/security/hardening/).

### PHP error display

Check the configuration on the web server, not the tester's Mac. The original suggested command is an initial file search only:

```bash
grep -i 'display_errors' /etc/php/*/php.ini
```

PHP installations may instead use nested SAPI directories, pool overrides, `.user.ini`, or hosting controls. A broader file search is:

```bash
rg -n '^[[:space:]]*(display_errors|display_startup_errors|log_errors)[[:space:]]*=' /etc/php
```

Confirm effective values for the PHP process serving WordPress, not just CLI PHP. Target production behavior is `display_errors = Off`, `display_startup_errors = Off`, and protected server-side error logging. Suppress public error display, not all diagnostic logging. Do not expose a public `phpinfo()` page for this check. See [PHP error configuration](https://www.php.net/manual/en/errorfunc.configuration.php).

### MySQL general query log

```sql
SHOW GLOBAL VARIABLES LIKE 'general_log';
SHOW GLOBAL VARIABLES LIKE 'log_output';
```

Normally keep `general_log` OFF in production outside a controlled troubleshooting window. It records statements received by the server and can introduce overhead and sensitive-data exposure; a logged statement alone does not establish successful execution. It is distinct from WordPress debug logging. See [MySQL general query log documentation](https://dev.mysql.com/doc/refman/8.4/en/query-log.html).

## Evidence and completion record

For each check record: date, environment, reviewer, source location/configuration scope, sanitized evidence, observed result, limitations, and remediation/retest status. Keep all checklist items pending until actually verified. Link confirmed observations to [the existing test results](TEST-RESULTS.md); do not convert this plan into a claim of completed testing.
