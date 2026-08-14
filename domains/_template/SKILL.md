---
name: replace-me-reconstruction
description: Replace this description with what the domain reconstructs, its accepted sources, expected outputs, and concrete trigger phrases.
---

# Replace Me Reconstruction

Apply the repository's evidence-to-output contract to this domain.

## Define the domain

- Read `domain.json` before creating project entities or constraints.
- Preserve raw observations separately from interpretations.
- Use only entity, relation, constraint, and output types declared by the domain package.
- Record unsupported cases instead of approximating them silently.

## Validate and release

- Run the domain validators declared in `domain.json`.
- Keep unresolved decisions visible and block dependent current outputs.
- Do not promote a result above the domain package's maturity ceiling.
