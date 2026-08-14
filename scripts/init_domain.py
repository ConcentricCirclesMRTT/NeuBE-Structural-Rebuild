#!/usr/bin/env python3
"""Create a domain pack from the repository template."""

import argparse
import json
import re
import shutil
from pathlib import Path


SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("domain_id")
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="A domain-specific structural reconstruction package.")
    args = parser.parse_args()

    if not SLUG.fullmatch(args.domain_id):
        parser.error("domain_id must use lowercase hyphenated words")
    source = ROOT / "domains" / "_template"
    target = ROOT / "domains" / args.domain_id
    if target.exists():
        parser.error(f"domain already exists: {target}")
    shutil.copytree(source, target)

    manifest_path = target / "domain.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update({"id": args.domain_id, "title": args.title, "description": args.description})
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    skill_path = target / "SKILL.md"
    skill_name = f"{args.domain_id}-reconstruction"
    skill = skill_path.read_text(encoding="utf-8")
    skill = skill.replace("replace-me-reconstruction", skill_name)
    skill = skill.replace("Replace Me Reconstruction", args.title)
    skill = skill.replace(
        "Replace this description with what the domain reconstructs, its accepted sources, expected outputs, and concrete trigger phrases.",
        f"Reconstruct {args.title.lower()} from domain evidence as traceable, reviewable models. Customize this description with accepted sources, outputs, and trigger phrases.",
    )
    skill_path.write_text(skill, encoding="utf-8")
    print(f"Created domain pack: {target.relative_to(ROOT)}")
    print(f"Next: edit {manifest_path.relative_to(ROOT)} and {skill_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
