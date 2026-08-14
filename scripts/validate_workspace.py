#!/usr/bin/env python3
"""Validate domain packs, reconstruction projects, and their references."""

import argparse
import json
import re
import sys
from pathlib import Path

from validate_public_ir import validate as validate_ir


SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ROOT = Path(__file__).resolve().parents[1]
DOMAIN_KEYS = {"schema_version", "id", "title", "description", "source_types", "entity_types", "relation_types", "constraint_types", "output_types", "maturity_ceiling", "validators"}
PROJECT_KEYS = {"schema_version", "id", "title", "domain_ref", "data_class", "target_maturity", "status", "source_register", "current_ir", "review_log", "output_dir"}


def read_json(path, errors):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return None


def resolve_inside(base, relative, errors, label):
    candidate = (base / relative).resolve()
    try:
        candidate.relative_to(base.resolve())
    except ValueError:
        errors.append(f"{label}: path escapes its project directory: {relative}")
        return None
    return candidate


def validate_domain(path, errors):
    manifest = read_json(path / "domain.json", errors)
    if not isinstance(manifest, dict):
        return None
    missing = DOMAIN_KEYS - set(manifest)
    if missing:
        errors.append(f"domains/{path.name}/domain.json: missing {', '.join(sorted(missing))}")
    if manifest.get("id") != path.name:
        errors.append(f"domains/{path.name}: manifest id must match directory")
    for key in ("source_types", "entity_types", "relation_types", "constraint_types", "output_types", "validators"):
        if not isinstance(manifest.get(key), list) or not manifest.get(key):
            errors.append(f"domains/{path.name}: {key} must be a non-empty array")
    if manifest.get("maturity_ceiling") not in {"concept", "coordination", "detailing", "fabrication"}:
        errors.append(f"domains/{path.name}: invalid maturity_ceiling")
    if not (path / "SKILL.md").is_file():
        errors.append(f"domains/{path.name}: missing SKILL.md")
    for validator in manifest.get("validators", []):
        resolved = resolve_inside(path, validator, errors, f"domains/{path.name}")
        if resolved and not resolved.is_file():
            errors.append(f"domains/{path.name}: missing validator {validator}")
    return manifest


def validate_project(path, domains, errors):
    manifest = read_json(path / "project.json", errors)
    if not isinstance(manifest, dict):
        return
    missing = PROJECT_KEYS - set(manifest)
    if missing:
        errors.append(f"projects/{path.name}/project.json: missing {', '.join(sorted(missing))}")
    if manifest.get("id") != path.name:
        errors.append(f"projects/{path.name}: manifest id must match directory")
    if manifest.get("domain_ref") not in domains:
        errors.append(f"projects/{path.name}: unknown domain_ref {manifest.get('domain_ref')}")
    if manifest.get("data_class") not in {"synthetic", "redistributable", "private"}:
        errors.append(f"projects/{path.name}: invalid data_class")
    if manifest.get("status") not in {"working", "review_required", "reviewed", "released"}:
        errors.append(f"projects/{path.name}: invalid status")
    for field in ("source_register", "current_ir", "review_log", "output_dir"):
        resolved = resolve_inside(path, manifest.get(field, ""), errors, f"projects/{path.name}")
        if resolved and not resolved.exists():
            errors.append(f"projects/{path.name}: missing {field} path {manifest.get(field)}")
    ir_path = resolve_inside(path, manifest.get("current_ir", ""), errors, f"projects/{path.name}")
    if ir_path and ir_path.is_file():
        ir = read_json(ir_path, errors)
        if isinstance(ir, dict):
            public = manifest.get("data_class") in {"synthetic", "redistributable"}
            for error in validate_ir(ir, public_only=public):
                errors.append(f"projects/{path.name}/{manifest.get('current_ir')}: {error}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain")
    parser.add_argument("--project")
    args = parser.parse_args()
    errors = []
    domains = {}
    domain_paths = [ROOT / "domains" / args.domain] if args.domain else sorted((ROOT / "domains").iterdir())
    for path in domain_paths:
        if not path.is_dir() or path.name == "_template":
            continue
        if not SLUG.fullmatch(path.name):
            errors.append(f"domains/{path.name}: directory must use lowercase hyphenated words")
            continue
        manifest = validate_domain(path, errors)
        if manifest:
            domains[path.name] = manifest
    if args.project:
        project_paths = [ROOT / "projects" / args.project]
    else:
        project_paths = sorted((ROOT / "projects").iterdir())
    for path in project_paths:
        if path.is_dir() and path.name != "_template":
            validate_project(path, domains, errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {len(domains)} domain pack(s) and {sum(1 for p in project_paths if p.is_dir() and p.name != '_template')} project(s) are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
