# Client website testing

Branch: **Client-Website-Test**

Keep one top-level folder per client. Each folder contains its own scope, evidence, reports, learning material and dated retests.

| Client | Target | Records | Status |
|---|---|---|---|
| Healthyaa | https://healthyaa.co.uk/ | [Healthyaa](Healthyaa/README.md) | Assessment in progress |

## Adding another client

Create a new folder named for that client alongside `Healthyaa/`, then add it to the index above. Use this structure as a starting point:

```text
ClientName/
  README.md
  assessment/
    YYYY-MM-DD/
  manual-tests/
    YYYY-MM-DD/
  documents/
```

The client README should identify the authorised target and scope, assessment status, evidence dates, report links and restrictions. Keep test IDs distinct from finding IDs. Preserve historical results, and label new fixes and retests separately.

Confirm the repository audience is appropriate for each client before adding their internal findings. Do not commit passwords, session credentials, private keys, live payment secrets or real customer exports. This branch's existence does not grant authorisation to test a new client.
