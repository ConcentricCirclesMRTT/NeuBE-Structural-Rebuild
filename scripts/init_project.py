#!/usr/bin/env python3
"""Create a reconstruction project bound to a domain pack."""

import argparse
import json
import re
import shutil
from pathlib import Path


SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ROOT = Path(__file__).resolve().parents[1]


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_id")
    parser.add_argument("--domain", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--data-class", choices=["synthetic", "redistributable", "private"], default="synthetic")
    parser.add_argument("--target-maturity", choices=["concept", "coordination"], default="coordination")
    args = parser.parse_args()

    for label, value in (("project_id", args.project_id), ("domain", args.domain)):
        if not SLUG.fullmatch(value):
            parser.error(f"{label} must use lowercase hyphenated words")
    if not (ROOT / "domains" / args.domain / "domain.json").is_file():
        parser.error(f"unknown domain pack: {args.domain}")
    source = ROOT / "projects" / "_template"
    target = ROOT / "projects" / args.project_id
    if target.exists():
        parser.error(f"project already exists: {target}")
    shutil.copytree(source, target)

    manifest_path = target / "project.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update({
        "id": args.project_id,
        "title": args.title,
        "domain_ref": args.domain,
        "data_class": args.data_class,
        "target_maturity": args.target_maturity,
    })
    write_json(manifest_path, manifest)

    ir_path = target / "workspace" / "ir.json"
    ir = json.loads(ir_path.read_text(encoding="utf-8"))
    public = args.data_class in {"synthetic", "redistributable"}
    ir["project"].update({
        "id": ("DEMO-" if public else "PRIVATE-") + args.project_id.upper(),
        "structure_class": args.domain,
        "data_class": "synthetic_or_redistributable" if public else "private",
        "target_maturity": args.target_maturity,
    })
    write_json(ir_path, ir)
    print(f"Created project: {target.relative_to(ROOT)}")
    print(f"Raw evidence belongs in {target.relative_to(ROOT)}/sources/ and is ignored by Git")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
