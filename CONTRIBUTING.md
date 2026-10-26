# Contributing to Codex Red

This fork adapts [Claude-Red](https://github.com/SnailSploit/Claude-Red) for OpenAI Codex. Keep original source attribution and the MIT licence intact.

## Skill format

A skill lives at `Skills/<category>/<skill-name>/SKILL.md`. The category is for repository navigation; installation places `<skill-name>/` directly in a Codex skills root.

```yaml
---
name: assessment-topic
description: "Explain the task this skill supports and when Codex should use it."
metadata:
  source: "https://example.com/original-reference"
---
```

The `name` must match the folder, use lowercase letters, digits and single hyphens, and contain at most 64 characters. Names must be unique across categories. Preserve existing names; renames are breaking changes.

The `description` must be a nonempty string of at most 1,024 characters without angle brackets. Keep it concise and specific enough to distinguish the skill from neighboring topics. Put detailed coverage, commands and references in the body. Optional `metadata.source` records the original source of inherited material.

Use provider-neutral instruction headings. Retain product names where the content actually concerns that product. A skill can bundle `scripts/`, `references/` and `assets/`; installation and export must preserve these resources.

See the official OpenAI [skill authoring guide](https://learn.chatgpt.com/docs/build-skills). Optional `agents/openai.yaml` may be added when a skill needs UI metadata or declared tool dependencies.

## Content conventions

- Prefer one focused workflow or attack surface per skill.
- Cite original research, vendor advisories and relevant CWE, OWASP or MITRE references.
- Keep methodology clear, with ordered steps where sequence matters and language tags on code blocks.
- Do not hardcode victim infrastructure, real client data or credentials.
- Preserve documented scope, authorization boundaries, evidence handling and remediation guidance.
- Review AI-generated technical content before accepting it.

## Local checks

Use Python 3.10 or later and a local virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python tools/build_manifest.py
python tools/build_manifest.py --check
python -m unittest discover -s tests -v
./install.sh --skill offensive-reporting --dry-run
```

The inventory builder rejects missing, invalid or duplicate YAML metadata, mismatched names, duplicate skill identifiers and invalid descriptions. `--check` verifies the checked-in inventory without rewriting it. Tests exercise packaging with isolated fixtures; they do not run security techniques or contact targets.

## Adding or changing a skill

1. Create or update its `SKILL.md` and any required resources.
2. Preserve the identifier and attribution for existing skills.
3. Update the README index, category counts and MINDMAP when adding or reorganizing skills.
4. Note material changes in CHANGELOG.
5. Regenerate `codex-skills.json` and run the local checks above.
6. Review the diff for technical accuracy, resource preservation and unintended changes.

Keep pull requests focused. When splitting a broad skill, retain its existing identifier as an overview that links to the focused skills, and update the inventory and navigation.

## Review

Reviewers check technical accuracy, clear scope, evidence and references, compatible metadata, and safe installation behavior. Content with destructive defaults, malicious helpers, unlicensed copying or unreviewed technical claims should be revised before merging. Report sensitive repository issues privately as described in [SECURITY.md](SECURITY.md).
