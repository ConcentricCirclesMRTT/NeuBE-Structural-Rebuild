# Domain Profiles

Choose the smallest profile that describes the target. Extend it in project data rather than silently changing core meanings.

## Frame

Elements: column, beam, brace, slab, wall, footing. Relationships: joint, support, bearing, adjacency. Typical sources: plans, elevations, sections, schedules, site images, scans.

## Truss or lattice

Elements: chord, web, post, node plate, support. Relationships: node incidence, panel membership, connection assembly. Preserve front/rear physical identity when projections overlap.

## Bridge

Elements: deck segment, girder, cross-frame, pier, bearing, abutment. Relationships: span, bearing interface, expansion interface, support. Do not infer load rating or inspection disposition from reconstructed geometry.

## Equipment support or platform

Elements: frame member, plate, bracket, platform, stair, guard, anchor. Relationships: attachment, support, clearance interface, assembly containment. Keep equipment geometry and supporting structure as separate systems.

## Unsupported by the public core

Treat reinforcement detailing, weld procedure qualification, proprietary connection design, code checking, load rating, fabrication tolerances, machine routing, and NC generation as external authorized domain packages.
