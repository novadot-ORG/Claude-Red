"""Regression checks for metadata and installation/export filesystem behavior."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.build_manifest import load_skills, parse_frontmatter

ROOT = Path(__file__).resolve().parent.parent


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex-red-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "fixture-repo"
        (self.repo / "tools").mkdir(parents=True)
        for name in ("install_skills.py", "build_manifest.py"):
            shutil.copyfile(ROOT / "tools" / name, self.repo / "tools" / name)
        shutil.copyfile(ROOT / "convert_skills.py", self.repo / "convert_skills.py")
        self.skills = self.repo / "Skills"
        for category, name in (("alpha", "first-skill"), ("alpha", "second-skill"), ("beta", "other-skill")):
            folder = self.skills / category / name
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(f'---\nname: {name}\ndescription: "Review a test document."\n---\n\n# Instructions\n\nPreserve the supplied text.\n')
        self.first = self.skills / "alpha" / "first-skill"
        (self.first / "references").mkdir()
        (self.first / "references" / "guide.bin").write_bytes(b"reference\x00\xff\n")
        self.target = self.base / "installed skills"

    def run_script(self, script, *args):
        return subprocess.run([sys.executable, str(self.repo / script), *map(str, args)], cwd=self.repo, capture_output=True, text=True)

    def install(self, *args):
        return self.run_script("tools/install_skills.py", "--target", self.target, *args)

    def test_install_all_flat_and_preserve_resources(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual({p.name for p in self.target.iterdir()}, {"first-skill", "second-skill", "other-skill"})
        self.assertEqual((self.target / "first-skill" / "references" / "guide.bin").read_bytes(), b"reference\x00\xff\n")
        self.assertEqual((self.target / "first-skill" / "SKILL.md").read_bytes(), (self.first / "SKILL.md").read_bytes())

    def test_category_and_skill_filter(self):
        result = self.install("--category", "alpha", "--skill", "second-skill")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([p.name for p in self.target.iterdir()], ["second-skill"])

    def test_category_installs_only_its_members(self):
        result = self.install("--category", "alpha")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual({p.name for p in self.target.iterdir()}, {"first-skill", "second-skill"})

    def test_dry_run_writes_nothing(self):
        result = self.install("--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("[dry-run]"), 3)
        self.assertFalse(self.target.exists())

    def test_later_collision_prevents_all_copies(self):
        existing = self.target / "second-skill"
        existing.mkdir(parents=True)
        sentinel = existing / "keep.txt"
        sentinel.write_text("existing content")
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.target / "first-skill").exists())
        self.assertEqual(sentinel.read_text(), "existing content")

    def test_dangling_skill_symlink_is_not_followed(self):
        self.target.mkdir()
        missing = self.base / "missing-target"
        (self.target / "second-skill").symlink_to(missing, target_is_directory=True)
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(missing.exists())
        self.assertFalse((self.target / "first-skill").exists())

    def test_invalid_selection_writes_nothing(self):
        for args in (("--category", "../alpha"), ("--category", "unknown"), ("--skill", "unknown"), ("--skill", "")):
            with self.subTest(args=args):
                self.assertNotEqual(self.install(*args).returncode, 0)
                self.assertFalse(self.target.exists())

    def test_missing_option_value_is_an_error(self):
        self.assertNotEqual(self.run_script("tools/install_skills.py", "--target").returncode, 0)

    def test_normalized_or_symlinked_source_target_is_rejected(self):
        alias = self.base / "source-link"
        alias.symlink_to(self.skills, target_is_directory=True)
        for target in (self.skills / "alpha" / "..", alias, self.repo):
            with self.subTest(target=target):
                result = self.run_script("tools/install_skills.py", "--target", target)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.skills / "first-skill").exists())

    def test_listing_does_not_install(self):
        result = self.install("--list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"alpha\s+2 skill\(s\)")
        self.assertRegex(result.stdout, r"beta\s+1 skill\(s\)")
        self.assertFalse(self.target.exists())

    def test_export_folders_and_zip_preserve_bytes(self):
        output, archives = self.base / "export", self.base / "archives"
        result = self.run_script("convert_skills.py", "--output", output, "--zip-dir", archives)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list(output.iterdir())), 3)
        self.assertEqual(len(list(archives.glob("*.zip"))), 3)
        with zipfile.ZipFile(archives / "first-skill.zip") as archive:
            self.assertEqual(archive.read("first-skill/SKILL.md"), (self.first / "SKILL.md").read_bytes())
            self.assertEqual(archive.read("first-skill/references/guide.bin"), b"reference\x00\xff\n")
        self.assertEqual((output / "first-skill" / "SKILL.md").read_bytes(), (self.first / "SKILL.md").read_bytes())

    def test_existing_zip_destination_blocks_export_before_writes(self):
        output, archives = self.base / "export", self.base / "archives"
        archives.mkdir()
        result = self.run_script("convert_skills.py", "--output", output, "--zip-dir", archives)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())

    def test_export_dangling_destination_symlinks_are_rejected(self):
        for option in ("--output", "--zip-dir"):
            with self.subTest(option=option):
                missing = self.base / (option[2:] + "-missing")
                link = self.base / (option[2:] + "-link")
                link.symlink_to(missing, target_is_directory=True)
                output = self.base / "export"
                args = [option, link] if option == "--output" else ["--output", output, option, link]
                result = self.run_script("convert_skills.py", *args)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(missing.exists())
                self.assertFalse(output.exists())

    def test_overlapping_export_destinations_are_rejected(self):
        output = self.base / "export"
        result = self.run_script("convert_skills.py", "--output", output, "--zip-dir", output / "zip")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())

    def test_bad_metadata_blocks_export_before_writes(self):
        (self.first / "SKILL.md").write_text("# No metadata\n")
        output = self.base / "export"
        result = self.run_script("convert_skills.py", "--output", output)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())

    def test_manifest_check_detects_stale_inventory(self):
        generated = self.run_script("tools/build_manifest.py")
        self.assertEqual(generated.returncode, 0, generated.stderr)
        result = self.run_script("tools/build_manifest.py", "--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.repo / "codex-skills.json").read_text())
        self.assertEqual(data["skill_count"], 3)
        with (self.first / "SKILL.md").open("a") as stream:
            stream.write("\nAdditional instructions.\n")
        self.assertEqual(self.run_script("tools/build_manifest.py", "--check").returncode, 0)
        text = (self.first / "SKILL.md").read_text().replace("Review a test document.", "Review another test document.")
        (self.first / "SKILL.md").write_text(text)
        self.assertNotEqual(self.run_script("tools/build_manifest.py", "--check").returncode, 0)

    def test_metadata_rejects_duplicate_keys(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            parse_frontmatter('---\nname: first-skill\nname: second-skill\ndescription: text\n---\nBody')

    def test_folded_yaml_description(self):
        data = parse_frontmatter('---\nname: first-skill\ndescription: >\n  First sentence.\n  Second sentence.\n---\nBody')
        self.assertEqual(data["description"].strip(), "First sentence. Second sentence.")

    def test_invalid_skill_names_and_descriptions(self):
        original = (self.first / "SKILL.md").read_text()
        variants = [original.replace("name: first-skill", "name: wrong-name"),
                    original.replace("Review a test document.", "x" * 1025),
                    original.replace("Review a test document.", ""),
                    original.replace("Review a test document.", "Use <placeholder>"),
                    "---\nname: first-skill\ndescription: Text\n---\n"]
        for text in variants:
            with self.subTest(text=text[:100]):
                (self.first / "SKILL.md").write_text(text)
                with self.assertRaises(ValueError):
                    load_skills(self.skills)

    def test_duplicate_skill_names_across_categories(self):
        duplicate = self.skills / "beta" / "first-skill"
        shutil.copytree(self.first, duplicate)
        with self.assertRaisesRegex(ValueError, "unique"):
            load_skills(self.skills)


if __name__ == "__main__":
    unittest.main()
