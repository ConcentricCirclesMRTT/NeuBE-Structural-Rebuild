#!/usr/bin/env python3
"""Validate the public general-structure reconstruction IR."""

import argparse
import json
import sys
from pathlib import Path


TOP_LEVEL = {"schema_version", "project", "sources", "observations", "hypotheses", "semantic_model", "constraints", "reviews", "outputs"}
HYPOTHESIS_STATES = {"proposed", "accepted", "rejected", "review_required"}
CONSTRAINT_STATES = {"pending", "passed", "failed", "review_required"}
SOURCE_TYPES = {"drawing", "image", "point_cloud", "schedule", "inspection_record", "engineering_note", "model"}


def validate(data, public_only=True):
    if not isinstance(data, dict):
        return ["root must be an object"]
    errors = []
    missing = TOP_LEVEL - set(data)
    if missing:
        return ["missing top-level keys: " + ", ".join(sorted(missing))]
    if data["schema_version"] != "1.0-public":
        errors.append("schema_version must be 1.0-public")
    project = data["project"]
    if not isinstance(project, dict) or not str(project.get("id", "")):
        errors.append("project.id must be a non-empty string")
    elif public_only and not project["id"].startswith("DEMO-"):
        errors.append("public project.id must start with DEMO-")
    allowed_data_classes = {"synthetic_or_redistributable"} if public_only else {"synthetic_or_redistributable", "private"}
    if project.get("data_class") not in allowed_data_classes:
        errors.append("project.data_class is not allowed for this validation mode")
    if project.get("target_maturity") not in {"concept", "coordination"}:
        errors.append("public target_maturity must be concept or coordination")

    semantic = data["semantic_model"]
    if not isinstance(semantic, dict):
        return errors + ["semantic_model must be an object"]
    for key in ("elements", "joints", "assemblies", "interfaces"):
        if not isinstance(semantic.get(key), list):
            errors.append(f"semantic_model.{key} must be an array")
            semantic[key] = []
    collections = [data[key] for key in ("sources", "observations", "hypotheses", "constraints", "reviews", "outputs")]
    collections += [semantic[key] for key in ("elements", "joints", "assemblies", "interfaces")]
    ids = set()
    for collection in collections:
        if not isinstance(collection, list):
            errors.append("IR collections must be arrays")
            continue
        for item in collection:
            item_id = item.get("id") if isinstance(item, dict) else None
            if not item_id:
                errors.append("every entity must have a non-empty id")
            elif item_id in ids:
                errors.append(f"duplicate id: {item_id}")
            else:
                ids.add(item_id)

    source_ids = {item.get("id") for item in data["sources"] if isinstance(item, dict)}
    for source in data["sources"]:
        if source.get("source_type") not in SOURCE_TYPES:
            errors.append(f"{source.get('id')}: invalid source_type")
        if source.get("license_status") not in {"synthetic", "redistributable"}:
            errors.append(f"{source.get('id')}: source is not cleared for public use")
    observation_ids = {item.get("id") for item in data["observations"] if isinstance(item, dict)}
    for observation in data["observations"]:
        if observation.get("source_ref") not in source_ids:
            errors.append(f"{observation.get('id')}: unknown source_ref {observation.get('source_ref')}")
        confidence = observation.get("confidence")
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            errors.append(f"{observation.get('id')}: confidence must be between 0 and 1")
    for hypothesis in data["hypotheses"]:
        if hypothesis.get("status") not in HYPOTHESIS_STATES:
            errors.append(f"{hypothesis.get('id')}: invalid hypothesis status")
        for ref in hypothesis.get("observation_refs", []):
            if ref not in observation_ids:
                errors.append(f"{hypothesis.get('id')}: unknown observation ref {ref}")
    for entity in semantic["elements"] + semantic["joints"] + semantic["assemblies"] + semantic["interfaces"]:
        for ref in entity.get("observation_refs", []):
            if ref not in observation_ids:
                errors.append(f"{entity.get('id')}: unknown observation ref {ref}")
    for constraint in data["constraints"]:
        if constraint.get("status") not in CONSTRAINT_STATES:
            errors.append(f"{constraint.get('id')}: invalid constraint status")
        if constraint.get("status") == "passed" and constraint.get("residual", float("inf")) > constraint.get("tolerance", -1):
            errors.append(f"{constraint.get('id')}: passed constraint exceeds tolerance")
    blocked = {item.get("id") for item in data["hypotheses"] if item.get("status") in {"proposed", "review_required"}}
    blocked |= {item.get("id") for item in data["constraints"] if item.get("status") != "passed"}
    for output in data["outputs"]:
        if output.get("status") == "current" and blocked.intersection(output.get("input_refs", [])):
            errors.append(f"{output.get('id')}: current output depends on unresolved input")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ir", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.ir.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {args.ir} is a valid public structure reconstruction IR")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
