# curik

Curriculum development agent.

## Initial version

This repository now includes an initial Python implementation based on
`curik-project-plan.md`, focused on:

- Project scaffolding with `curik init`
- `.course/` state container creation
- Phase 1 spec document seeding
- Basic phase tracking and gated Phase 1 → Phase 2 transition

### Usage

```bash
python -m pip install -e .
curik init --path .
curik get-phase --path .
```
