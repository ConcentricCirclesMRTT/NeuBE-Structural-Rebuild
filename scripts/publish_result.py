#!/usr/bin/env python3
"""Publish reviewed project outputs with an immutable hash manifest."""

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from validate_public_ir import validate as validate_ir


ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_id")
    parser.add_argument("--artifact", action="append", required=True, help="Path relative to the project's outputs directory; repeat for multiple files")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    project_dir = ROOT / "projects" / args.project_id
    try:
        project = json.loads((project_dir / "project.json").read_text(encoding="utf-8"))
        ir_path = project_dir / project["current_ir"]
        ir = json.loads(ir_path.read_text(encoding="utf-8"))
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot load project: {exc}", file=sys.stderr)
        return 1
    if project.get("status") != "reviewed":
        print("ERROR: project status must be reviewed before publishing", file=sys.stderr)
        return 1
    public = project.get("data_class") in {"synthetic", "redistributable"}
    errors = validate_ir(ir, public_only=public)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    output_root = (project_dir / project["output_dir"]).resolve()
    release_dir = ROOT / "releases" / args.project_id
    if release_dir.exists() and not args.force:
        print(f"ERROR: release exists: {release_dir.relative_to(ROOT)}; use --force to replace it", file=sys.stderr)
        return 1
    artifacts = []
    resolved = []
    for relative in args.artifact:
        source = (output_root / relative).resolve()
        try:
            clean_relative = source.relative_to(output_root)
        except ValueError:
            print(f"ERROR: artifact escapes output directory: {relative}", file=sys.stderr)
            return 1
        if not source.is_file():
            print(f"ERROR: artifact does not exist: {relative}", file=sys.stderr)
            return 1
        resolved.append((source, clean_relative))
    if release_dir.exists():
        shutil.rmtree(release_dir)
    artifact_root = release_dir / "artifacts"
    artifact_root.mkdir(parents=True)
    for source, relative in resolved:
        target = artifact_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        artifacts.append({"path": str(Path("artifacts") / relative), "sha256": digest(target), "bytes": target.stat().st_size})
    manifest = {
        "schema_version": "1.0",
        "project_id": args.project_id,
        "domain_ref": project["domain_ref"],
        "maturity": project["target_maturity"],
        "published_at": datetime.now(timezone.utc).isoformat(),
        "input_ir": {"path": project["current_ir"], "sha256": digest(ir_path)},
        "artifacts": artifacts,
    }
    (release_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Published {len(artifacts)} artifact(s) to {release_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
