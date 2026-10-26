#!/usr/bin/env python3
"""Validate the skill library and generate its informational Codex inventory."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "Skills"
OUT = ROOT / "codex-skills.json"
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---(?:\n|$)", re.DOTALL)
NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys rather than silently replacing metadata."""


def _mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str) or key in result:
            raise ValueError(f"Invalid or duplicate metadata key: {key!r}")
        result[key] = loader.construct_object(value_node, deep=True)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("Missing or invalid YAML frontmatter")
    try:
        data = yaml.load(match.group(1), Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML frontmatter: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Frontmatter must be a mapping")
    return data


def load_skills(skills_dir: Path = SKILLS_DIR) -> list[dict]:
    """Load all skills, failing before any generated file is written."""
    paths = sorted(skills_dir.glob("*/*/SKILL.md"))
    if not paths:
        raise ValueError(f"No skills found in {skills_dir}")
    entries = []
    names = set()
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            name, description = fm.get("name"), fm.get("description")
            if not isinstance(name, str) or not NAME_RE.fullmatch(name) or len(name) > 64:
                raise ValueError("name must be a hyphenated identifier of at most 64 characters")
            if name != path.parent.name or name in names:
                raise ValueError("name must match its folder and be unique across categories")
            if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                raise ValueError("description must contain 1–1024 characters")
            if "<" in description or ">" in description:
                raise ValueError("description must not contain angle brackets")
            if not text[FRONTMATTER_RE.match(text).end():].strip():
                raise ValueError("Skill instructions must not be empty")
        except (ValueError, OSError) as exc:
            raise ValueError(f"{path}: {exc}") from exc
        names.add(name)
        entries.append({
            "name": name,
            "category": path.parent.parent.name,
            "path": path,
            "description": description.strip(),
        })
    return entries


def build_manifest(skills_dir: Path = SKILLS_DIR) -> dict:
    manifest = {
        "name": "codex-red",
        "version": "0.4.0",
        "license": "MIT",
        "homepage": "https://github.com/novadot-ORG/Claude-Red",
        "upstream": "https://github.com/SnailSploit/Claude-Red",
        "runtime": "codex",
        "categories": {},
        "skills": [],
    }
    for entry in load_skills(skills_dir):
        manifest["categories"].setdefault(entry["category"], []).append(entry["name"])
        manifest["skills"].append({**entry, "path": entry["path"].relative_to(ROOT).as_posix()})
    manifest["skill_count"] = len(manifest["skills"])
    manifest["category_count"] = len(manifest["categories"])
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate skills and check the saved inventory without writing")
    args = parser.parse_args()
    try:
        manifest = build_manifest()
        rendered = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        if args.check:
            if not OUT.is_file() or OUT.read_text(encoding="utf-8") != rendered:
                raise ValueError("codex-skills.json is stale; run python tools/build_manifest.py")
            print(f"Validated {manifest['skill_count']} skills across {manifest['category_count']} categories; inventory is current.")
        else:
            OUT.write_text(rendered, encoding="utf-8")
            print(f"Wrote {OUT.name}: {manifest['skill_count']} skills in {manifest['category_count']} categories.")
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
