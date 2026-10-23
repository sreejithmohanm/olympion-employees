# Repository architecture

- `engineering/` contains engineering standards and implementation guidance.
- `business/` contains business capabilities and domain definitions.
- `schemas/` contains versioned machine-readable contracts. `dpdl-v1.yaml` is the DPDL v1 JSON Schema.
- `templates/` contains starting employee definitions; CI validates every YAML file here against the v1 schema.
- `examples/` contains complete, schema-conforming employee definitions.
- `docs/` contains repository and authoring documentation.

The npm package `@olympion/dpdl-schema` publishes the versioned schemas directory.
