---
name: general-structure-reconstruction
description: Reconstruct physical structures from drawings, images, point clouds, schedules, inspection records, and engineering notes as traceable, reviewable models. Use for buildings, bridges, frames, trusses, supports, platforms, equipment structures, and other constructed assemblies when identifying elements, associating evidence across sources, recovering topology and interfaces, solving geometry, managing ambiguity, validating constraints, or preparing coordination-grade CAD/BIM/digital-twin outputs. Also use for structural reconstruction, drawing-to-model, scan-to-model, as-built modeling, 结构重构, 图纸转模型, 逆向建模, 竣工模型, or 工程数字孪生.
---

# NeuBE-Structural-Rebuild

Neural Building Engine Structural Rebuild.

Turn heterogeneous evidence into a reviewable model of a physical structure. Treat visual plausibility as a hypothesis, not proof.

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

## Use bundled resources

- Start from [assets/public-ir-template.json](assets/public-ir-template.json).
- Use [assets/public-ir.schema.json](assets/public-ir.schema.json) as the public field contract.
- Use [assets/synthetic-frame-example.json](assets/synthetic-frame-example.json) only as a synthetic format example.
- Read [references/public-safety-boundary.md](references/public-safety-boundary.md) before adding real data or domain rules.
