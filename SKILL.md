---
name: general-structure-reconstruction
description: Turn expert knowledge from drawing-centered industries into domain-specific reconstruction skills, then use them to reconstruct physical structures from drawings, images, point clouds, schedules, inspection records, and engineering notes as traceable, reviewable 3D models. Use when domain experts and builders need to co-create or extend a domain pack, define terminology and judgment rules, initialize a reconstruction project, manage evidence and generated files, recover topology and interfaces, validate constraints, review ambiguity, or publish CAD/BIM/digital-twin results. Also use for structural reconstruction templates, domain packs, drawing-to-model, scan-to-model, as-built modeling, 行业专家共创, 结构重构, 领域模板, 图纸转模型, 逆向建模, 竣工模型, or 工程数字孪生.
---

# NeuBE-Structural-Rebuild

Neural Building Engine Structural Rebuild.

Use this repository as a forkable AI Agent Skill template. Turn heterogeneous evidence and expert knowledge into a reviewable model of a physical structure. Treat visual plausibility as a hypothesis, not proof.

Everything in 3D. Precisely. As an AI Agent Skill.

## Choose the operating mode

- `Domain Builder`: create or extend reusable ontology, rules, validators, and a domain-specific Skill under `domains/<domain>/`.
- `Project Builder`: apply one domain pack to evidence and working state under `projects/<project>/`.
- `Publisher`: promote only reviewed outputs into `releases/<project>/` with hashes and provenance.

When creating a new domain pack, read [references/create-domain-3d-rebuild-skill.md](references/create-domain-3d-rebuild-skill.md) before initialization.

## Co-create with domain experts

- Ask experts for a sanitized representative drawing, glossary, acceptance rules, and peer-reviewable target result.
- Capture literal domain knowledge before translating it into schemas or code.
- Separate expert authority over meaning and acceptance from tool-builder authority over implementation.
- Turn repeated expert decisions into ontology entries, deterministic validators, bounded review questions, or evaluation fixtures.
- Never imply that an expert must write code to propose or review a domain pack.

Read [references/repository-layout.md](references/repository-layout.md) before creating, moving, committing, or publishing project files.

## Bootstrap a domain and project

Create a domain pack instead of editing `_template` directly:

```bash
python3 scripts/init_domain.py <domain-id> --title "<Domain title>"
python3 scripts/init_project.py <project-id> --domain <domain-id> --title "<Project title>"
```

Customize `domains/<domain>/domain.json`, its `SKILL.md`, ontology, rules, and validators. Keep reusable domain knowledge out of project directories. Keep project evidence, interpretations, reviews, and outputs out of the domain package.

## Preserve six layers

1. `sources`: documents, images, scans, tables, revisions, and coordinate frames;
2. `observations`: literal text, geometry, detections, measurements, and confidence;
3. `hypotheses`: candidate identity, type, association, material, and relationship;
4. `semantic_model`: physical elements, joints, assemblies, interfaces, and topology;
5. `constraints`: dimensions, incidence, alignment, symmetry, continuity, and domain rules;
6. `outputs`: solved geometry and downstream artifacts with provenance, maturity, and status.

Never replace an observation with an interpretation. Never promote an unresolved hypothesis to current geometry.

## Follow the workflow

### 1. Define scope and output maturity

- State the structure boundary, source set, coordinate convention, intended use, and exclusions.
- Choose `concept`, `coordination`, `detailing`, or `fabrication` as the target maturity.
- Limit this public skill to concept or coordination grade unless an authorized domain package supplies additional rules and validation.

### 2. Inventory and normalize sources

- Render drawings before interpreting linework.
- Preserve document revision, page, view, image region, scan frame, unit, and raw value.
- Register coordinate systems explicitly; do not mix pixels, local scan coordinates, and world coordinates.
- Record source conflicts rather than selecting a convenient value silently.

Read [references/reconstruction-method.md](references/reconstruction-method.md) before associating observations across sources.

### 3. Build observations and hypotheses

- Give every source, observation, and hypothesis a stable ID.
- Link each hypothesis to supporting and conflicting observation IDs.
- Keep alternatives for ambiguous identity, occlusion, projection overlap, connection, or material.
- Mark each hypothesis `proposed`, `accepted`, `rejected`, or `review_required`.

### 4. Build semantics before detailed geometry

- Create physical element instances rather than one entity per drawing line or scan segment.
- Define joints, assemblies, contact interfaces, and containment explicitly.
- Separate objects that overlap in projection or point-cloud space unless identity evidence supports merging.
- Reconcile element counts and attributes against schedules when available.
- Select a domain profile from [references/domain-profiles.md](references/domain-profiles.md) and declare any unsupported element or connection type.

### 5. Solve geometry and constraints

- Convert dimensions, datums, measured points, and declared rules into explicit constraints.
- Record solver, inputs, units, tolerance, residual, and coordinate frame.
- Detect underconstraint, overconstraint, registration drift, and rigid-body freedom.
- Validate connectivity and interface compatibility independently of appearance.
- Represent symmetry and repetition as explicit transforms; verify handedness and exceptions.

### 6. Validate in gates

Run these gates in order:

1. source license, revision, and traceability;
2. observation completeness and coordinate-frame integrity;
3. physical-instance separation and cross-source association;
4. semantic topology, joints, assemblies, and schedule reconciliation;
5. constraint solvability, residuals, and tolerance policy;
6. domain-profile checks and declared unsupported cases;
7. output identity, maturity, and stale-state propagation.

Run `scripts/validate_public_ir.py <ir.json>`. Any error blocks release. A `review_required` dependency blocks promotion but remains visible for review.

### 7. Request bounded human review

Ask one decision-oriented question at a time. Include observations, alternatives, consequences, and affected outputs. Never ask a reviewer to approve an opaque whole model.

### 8. Export and report honestly

- Generate CAD, BIM, meshes, or digital-twin assets only downstream of accepted semantics and passed constraints.
- Embed semantic IDs and an input IR hash where the target tool permits it.
- Mark dependent outputs `stale` after an accepted upstream fact changes.
- State what is observed, interpreted, solved, unresolved, unsupported, and omitted.
- Do not claim structural adequacy, code compliance, detailing, or fabrication readiness unless separately calculated and authorized.

### 9. Validate and publish results

- Run `python3 scripts/validate_workspace.py --project <project-id>` before review.
- Set project status to `reviewed` only after the declared reviewer resolves release-blocking decisions.
- Write intermediate generated files under `projects/<project>/outputs/`; they are ignored by Git by default.
- Publish selected results with `python3 scripts/publish_result.py <project-id> --artifact <relative-output-path>`.
- Commit `releases/<project>/manifest.json` and its selected artifacts only when their data classification permits publication.
- Preserve the `built_from` origin and template license in project and release manifests.
- Never copy private raw evidence into a public release to make it self-contained.

## Use bundled resources

- Start from [assets/public-ir-template.json](assets/public-ir-template.json).
- Use [assets/public-ir.schema.json](assets/public-ir.schema.json) as the public field contract.
- Use [assets/synthetic-frame-example.json](assets/synthetic-frame-example.json) only as a synthetic format example.
- Read [references/public-safety-boundary.md](references/public-safety-boundary.md) before adding real data or domain rules.
- Use `domains/_template/` and `projects/_template/` only through the initialization scripts; do not store active work in template directories.
