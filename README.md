# NeuBE-Structural-Rebuild

**Neural Building Engine Structural Rebuild**

NeuBE-Structural-Rebuild is a reusable template for building domain-specific AI skills that reconstruct physical structures from heterogeneous evidence.

It is not a universal model that already understands every engineering domain. It provides the common workflow, data boundaries, validation gates, and review states needed to teach an AI agent a new reconstruction domain safely.

## The core idea

Many reconstruction systems jump directly from a drawing, image, or scan to a 3D model. That result may look plausible while hiding uncertain identities, conflicting dimensions, missing connections, or stale downstream geometry.

This template preserves an auditable chain:

```text
Sources
  -> Observations
  -> Hypotheses
  -> Domain Semantic Model
  -> Deterministic Constraints
  -> Human Review
  -> Versioned Outputs
```

The AI proposes bounded interpretations. Domain tools solve and validate deterministic facts. Human experts decide the ambiguities that carry engineering responsibility.

## A template for domain skills

The repository separates reusable behavior from domain knowledge.

| Reusable core | Domain-specific extension |
| --- | --- |
| Evidence provenance and stable IDs | Domain source types and extraction conventions |
| Observation versus interpretation | Domain entities, attributes, and relationships |
| Hypothesis and review states | Domain ambiguity patterns and review questions |
| Constraint records and residuals | Domain solvers, tolerances, and engineering rules |
| Release gates and stale propagation | Domain maturity criteria and output adapters |
| Public safety boundary | Authorized standards, catalogs, and project policy |

A suitable domain is one where practitioners can define:

1. what counts as evidence;
2. which physical or conceptual entities exist;
3. which constraints and rules can be tested;
4. which unresolved decisions must block release;
5. what output maturity means.

The same pattern can support building frames, bridges, trusses, equipment supports, industrial assemblies, or non-structural professional domains with an equivalent evidence-to-decision workflow.

## Angle-tower reconstruction as a proof case

Angle-tower reconstruction is one domain-specific instance of this template, not the definition of the template itself.

It is a useful validation case because it combines:

- dense multi-view engineering drawings;
- projected members that can represent different physical instances;
- structural topology and shared connections;
- orientation, symmetry, dimension, and geometry constraints;
- high-consequence ambiguity that should require expert review;
- downstream CAD and manufacturing artifacts that must become stale after upstream changes.

In an angle-tower skill, the generic semantic entities become members, nodes, structural faces, connection assemblies, holes, and fasteners. Generic constraints become face incidence, member orientation, length closure, hole pattern, connection stack, and fabrication checks. Those specialized rules belong in the domain package; they are intentionally absent from this public generic template.

This relationship is:

```text
Domain Skill Template
  -> Structure Reconstruction Template
      -> Angle-Tower Reconstruction Skill
```

The angle-tower case demonstrates that the template can organize real domain reasoning, deterministic programs, review decisions, and traceable outputs. It does not imply that one generic prompt can solve every domain without specialization.

## Create a domain-specific version

1. Fork or copy this repository.
2. Keep the six-layer evidence-to-output contract in `SKILL.md`.
3. Define the domain ontology and source conventions in `references/`.
4. Extend the public IR schema with domain entities and typed relationships.
5. Add deterministic parsers, solvers, and validators under `scripts/`.
6. Add synthetic or redistributable fixtures that contain both passing and blocked cases.
7. Define maturity levels, review authority, unsupported cases, and release blockers.
8. Forward-test the skill on representative tasks before making capability claims.

Do not copy confidential examples or private rule catalogs into a public specialization. A public example should be synthetic or explicitly redistributable and should preserve the reasoning challenge without allowing a protected project to be reconstructed.

## Repository contents

- [`SKILL.md`](SKILL.md): agent workflow and behavioral contract;
- [`assets/public-ir.schema.json`](assets/public-ir.schema.json): public generic IR schema;
- [`assets/public-ir-template.json`](assets/public-ir-template.json): empty project template;
- [`assets/synthetic-frame-example.json`](assets/synthetic-frame-example.json): synthetic cross-source example;
- [`references/domain-profiles.md`](references/domain-profiles.md): starter structural profiles;
- [`references/reconstruction-method.md`](references/reconstruction-method.md): association, topology, solving, and change-control method;
- [`references/public-safety-boundary.md`](references/public-safety-boundary.md): publication and engineering safety limits;
- [`scripts/validate_public_ir.py`](scripts/validate_public_ir.py): zero-dependency public IR validator.

## Validate the example

```bash
python3 scripts/validate_public_ir.py assets/synthetic-frame-example.json
```

Expected result:

```text
OK: assets/synthetic-frame-example.json is a valid public structure reconstruction IR
```

## Scope

This public repository supports concept- and coordination-grade reconstruction. Geometric consistency does not establish structural capacity, safety, regulatory compliance, detailing completeness, or fabrication readiness. Consequential use requires authorized domain rules, independent validation, and appropriately qualified engineering review.
