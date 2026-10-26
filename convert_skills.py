#!/usr/bin/env python3
"""Export the validated library as flat Codex skill folders and optional ZIPs.

Skills/ is already in Codex format. This exporter copies each complete skill;
it never reparses methodology text or rewrites the source files.
"""
from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path

from tools.build_manifest import ROOT, SKILLS_DIR, load_skills


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "codex-skills", help="Destination for flat skill folders")
    parser.add_argument("--zip-dir", type=Path, help="Also create one ZIP per skill in this directory")
    args = parser.parse_args()
    try:
        skills = load_skills()
        requested_roots = [args.output.expanduser()]
        if args.zip_dir:
            requested_roots.append(args.zip_dir.expanduser())
        for root in requested_roots:
            if root.exists() or root.is_symlink():
                raise ValueError(f"Export destination already exists: {root}")
        output = requested_roots[0].resolve()
        zip_dir = requested_roots[1].resolve() if args.zip_dir else None
        roots = [output] + ([zip_dir] if zip_dir else [])
        for root in roots:
            if root == SKILLS_DIR or SKILLS_DIR in root.parents or root in SKILLS_DIR.parents:
                raise ValueError("Export directories must not overlap the source Skills directory")
            if root.exists() or root.is_symlink():
                raise ValueError(f"Export destination already exists: {root}")
        if zip_dir and (zip_dir == output or zip_dir in output.parents or output in zip_dir.parents):
            raise ValueError("Skill and ZIP destinations must not overlap")
        output.mkdir(parents=True)
        if zip_dir:
            zip_dir.mkdir(parents=True)
        for skill in skills:
            dest = output / skill["name"]
            shutil.copytree(skill["path"].parent, dest)
            if zip_dir:
                with zipfile.ZipFile(zip_dir / f"{skill['name']}.zip", "w", zipfile.ZIP_DEFLATED) as archive:
                    for path in sorted(dest.rglob("*")):
                        if path.is_file():
                            archive.write(path, path.relative_to(output))
        print(f"Exported {len(skills)} Codex skills to {output}")
        if zip_dir:
            print(f"Created {len(skills)} skill ZIPs in {zip_dir}")
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
