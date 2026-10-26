#!/usr/bin/env python3
"""Install flat Codex skill folders without changing Codex configuration."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "Skills"
NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=Path.home() / ".agents" / "skills", help="Skills root (default: ~/.agents/skills)")
    parser.add_argument("--category", help="Install a single category")
    parser.add_argument("--skill", help="Install a single skill, optionally within --category")
    parser.add_argument("--dry-run", action="store_true", help="Show destinations without writing files")
    parser.add_argument("--list", action="store_true", help="List categories and skill counts")
    args = parser.parse_args()
    try:
        for selector in (args.category, args.skill):
            if selector is not None and not NAME_RE.fullmatch(selector):
                raise ValueError(f"Invalid category or skill name: {selector!r}")
        skills = sorted(SKILLS_DIR.glob("*/*/SKILL.md"))
        if not skills:
            raise ValueError(f"No skills found in {SKILLS_DIR}")
        if args.list:
            categories = {}
            for path in skills:
                category = path.parent.parent.name
                categories[category] = categories.get(category, 0) + 1
            for category, count in categories.items():
                print(f"{category:<20} {count} skill(s)")
            return 0
        selected = [path.parent for path in skills
                    if (args.category is None or path.parent.parent.name == args.category)
                    and (args.skill is None or path.parent.name == args.skill)]
        if not selected:
            raise ValueError("No skills match the requested category or skill")
        target = args.target.expanduser().resolve()
        if target == SKILLS_DIR or SKILLS_DIR in target.parents or target in SKILLS_DIR.parents:
            raise ValueError("The install target must not overlap the source Skills directory")
        # Check the complete selection before writing anything, including dangling symlinks.
        names = set()
        for source in selected:
            if not NAME_RE.fullmatch(source.name) or source.name in names:
                raise ValueError(f"Invalid or duplicate skill folder name: {source.name}")
            names.add(source.name)
            dest = target / source.name
            if dest.exists() or dest.is_symlink():
                raise ValueError(f"Destination already exists: {dest}")
        if args.dry_run:
            for source in selected:
                print(f"[dry-run] {source} -> {target / source.name}")
            return 0
        target.mkdir(parents=True, exist_ok=True)
        for source in selected:
            dest = target / source.name
            dest.mkdir()  # Claim the directory without overwriting a concurrent installation.
            shutil.copytree(source, dest, dirs_exist_ok=True)
        print(f"Installed {len(selected)} skill(s) to {target}")
        print("Codex discovers these skills automatically. Restart it if they do not appear.")
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
