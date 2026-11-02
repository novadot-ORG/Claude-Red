# Client website testing

Branch: **Client-Website-Test**

Keep one top-level folder per client. Each folder contains its own scope, evidence, reports, learning material and dated retests.

Develop shared skills on `codex/openai-compatibility`. Keep client-specific testing work and results on `Client-Website-Test`, inside the relevant client's folder. Record the skill branch and commit used for each assessment so results can be reproduced.

| Client | Target | Records | Status |
|---|---|---|---|
| Healthyaa | https://healthyaa.co.uk/ | [Healthyaa](Healthyaa/README.md) | Assessment in progress |
| Novadot | Not yet specified | [novadot](novadot/README.md) | Workspace created; scope pending |

## Adding another client

**Whenever a new client comes in, create a new top-level folder for that client before adding any testing work.** Never reuse another client's folder or mix client evidence.

1. Work on `Client-Website-Test`.
2. Create a unique folder named for the client alongside `Healthyaa/` and `novadot/`. Use lowercase names with hyphens for new folders; preserve existing folder names.
3. Add a `README.md` identifying the client, authorised targets and scope, restrictions, current status and next step. Mark unknown details as pending.
4. Add the client to the index above.
5. Keep that client's plans, evidence, reports and dated retests in its folder. Create the subdirectories below as needed, and update its README as work progresses.
6. Review the files being committed and push client work to `Client-Website-Test`.

Use this structure as a starting point:

```text
client-name/
  README.md
  assessment/
    YYYY-MM-DD/
  manual-tests/
    YYYY-MM-DD/
  documents/
```

The client README should identify the authorised target and scope, assessment status, evidence dates, report links and restrictions. Keep test IDs distinct from finding IDs. Preserve historical results, and label new fixes and retests separately.

Confirm the repository audience is appropriate for each client before adding their internal findings. Do not commit passwords, session credentials, private keys, live payment secrets or real customer exports. This branch's existence does not grant authorisation to test a new client.
