# Reconstruction Method

## Cross-source association

Associate observations using identity, geometry, neighborhood, attributes, revision, and coordinate registration. Agreement in one projection or nearest-neighbor distance alone is insufficient. Store candidate matches and contradictory evidence.

## Semantic topology

Represent physical objects as elements. Represent relationships separately:

- `joint`: a structural or assembly connection among elements;
- `interface`: contact, attachment, bearing, clearance, or boundary surface;
- `assembly`: a named group with a meaningful construction or functional identity;
- `contains`: spatial or assembly containment;
- `supports`: a declared load-path or support relationship, only when evidence justifies it.

Do not infer structural capacity from geometry alone.

## Geometry solving

Convert dimensions, scan measurements, alignments, and incidence into explicit constraints with frames, units, tolerances, and provenance. Report maximum and root-mean-square residuals. Low residual proves consistency with encoded inputs, not completeness or code compliance.

## Change control

Record output dependencies on accepted hypotheses and passed constraints. Mark affected outputs stale after upstream changes. Preserve superseded interpretations and decisions for auditability.
