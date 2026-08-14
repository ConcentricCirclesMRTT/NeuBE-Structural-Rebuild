# Repository Layout and File Lifecycle

## Layout

```text
domains/<domain>/        reusable ontology, rules, skill, and validators
projects/<project>/      one reconstruction job and its working state
releases/<project>/      explicitly published artifacts and immutable manifest
assets/                  generic schemas, templates, fixtures, and README media
scripts/                 repository-level initialization, validation, and publishing tools
template.json            machine-readable template identity and license
LICENSE + NOTICE         reuse terms and retained template attribution
```

## Lifecycle

1. Register a source in `projects/<project>/sources/index.json` before extracting observations.
2. Keep raw source files under `sources/`; they are ignored by Git by default.
3. Store current semantic work in `workspace/ir.json` and commit it only when its data classification permits.
4. Write reproducible intermediate files to `workspace/cache/` or `outputs/`; both stay out of Git.
5. Resolve or explicitly block review items before publishing dependent artifacts.
6. Use `scripts/publish_result.py` to copy selected outputs into `releases/<project>/artifacts/` and create a hash manifest.
7. Preserve `built_from` in domain, project, and release manifests so provenance survives repository moves and detached artifacts.

Keep small, reviewable release artifacts in Git. Use Git LFS for large CAD, mesh, point-cloud, video, or model files. A domain pack that publishes to an external artifact store must extend the generic publisher with an immutable URI and hash record.

## Public and private data

- `synthetic`: safe to publish when it contains no derived confidential geometry.
- `redistributable`: publish only with a recorded license/source basis.
- `private`: never commit raw sources or generated geometry to a public fork.

`.gitignore` is a guardrail, not a security boundary. Inspect staged files and image/document metadata before every public release.

## Template derivation

Keep the upstream `LICENSE` and applicable `NOTICE` text when distributing a derived repository. Keep the visible `Built from the NeuBE-Structural-Rebuild template` line in the README unless a product surface has a better conventional attribution location. New project code, domain knowledge, source data, and generated artifacts may each have separate terms; record those terms explicitly instead of assuming the repository license covers third-party evidence or outputs.

## Naming

Use lowercase hyphenated directory IDs. Keep IDs stable after other files reference them. Rename display titles freely; do not reuse deleted IDs for different physical projects or domains.
