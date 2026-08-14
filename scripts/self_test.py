#!/usr/bin/env python3
"""Exercise the Domain Builder lifecycle in an isolated repository copy."""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(repo, *args, expect=0):
    result = subprocess.run([sys.executable, *args], cwd=repo, text=True, capture_output=True)
    if result.returncode != expect:
        raise AssertionError(f"command failed ({result.returncode}): {' '.join(args)}\n{result.stdout}{result.stderr}")
    return result


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    with tempfile.TemporaryDirectory(prefix="neube-builder-test-") as temp:
        repo = Path(temp) / "repo"
        shutil.copytree(ROOT, repo, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        run(repo, "scripts/init_domain.py", "demo-frame", "--title", "Demo Frame")
        run(repo, "scripts/init_project.py", "sample-project", "--domain", "demo-frame", "--title", "Sample Project")
        run(repo, "scripts/validate_workspace.py")

        project_path = repo / "projects" / "sample-project" / "project.json"
        project = json.loads(project_path.read_text(encoding="utf-8"))
        if project.get("built_from", {}).get("template") != "NeuBE-Structural-Rebuild":
            raise AssertionError("project does not preserve template origin")
        original_origin = project["built_from"]
        project["built_from"] = {**original_origin, "repository": "https://example.invalid/removed-origin"}
        write_json(project_path, project)
        run(repo, "scripts/validate_workspace.py", "--project", "sample-project", expect=1)
        project["built_from"] = original_origin
        project["status"] = "reviewed"
        write_json(project_path, project)
        artifact = repo / "projects" / "sample-project" / "outputs" / "model.json"
        artifact.write_text('{"kind":"synthetic-result"}\n', encoding="utf-8")
        run(repo, "scripts/publish_result.py", "sample-project", "--artifact", "model.json")

        manifest_path = repo / "releases" / "sample-project" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("built_from") != project.get("built_from"):
            raise AssertionError("release does not preserve project template origin")
        if manifest.get("template_license") != "Apache-2.0":
            raise AssertionError("release does not preserve template license")
        published = repo / "releases" / "sample-project" / manifest["artifacts"][0]["path"]
        if manifest["artifacts"][0]["sha256"] != digest(published):
            raise AssertionError("published artifact hash does not match")

        project["status"] = "working"
        write_json(project_path, project)
        run(repo, "scripts/publish_result.py", "sample-project", "--artifact", "model.json", "--force", expect=1)
    print("OK: domain -> project -> validation -> reviewed release lifecycle")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
