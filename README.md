# Olympion Employee Catalog

This repository contains Digital Professional Definition Language (DPDL) employee definitions and the stable DPDL v1 JSON Schema.

## Repository layout

- `engineering/` — engineering standards and implementation guidance.
- `business/` — business capabilities and domain definitions.
- `schemas/` — versioned DPDL schemas.
- `templates/` — employee definition templates validated in CI.
- `examples/` — complete example definitions.
- `docs/` — authoring, validation, and architecture documentation.

## Author an employee definition

1. Copy `templates/employee.yaml` into `examples/` or the appropriate catalog location.
2. Set a unique kebab-case `id`, a human-readable `name`, a semantic `version`, and a concise `description` and `role`.
3. Add one or more `capabilities`, then optionally list `skills`, `responsibilities`, `tools`, `guardrails`, and custom `extensions`.
4. Validate the YAML against the DPDL v1 schema:

   ```sh
   python -m pip install -r requirements-dev.txt
   python scripts/validate_templates.py
   python -m unittest discover -s tests -v
   ```

The schema defines all required fields, types, and constraints. CI validates every `.yaml` and `.yml` file under `templates/` on each pull request.

## Schema package

The repository is configured as the public npm package `@olympion/dpdl-schema`. The package includes and exports `schemas/dpdl-v1.yaml` as `@olympion/dpdl-schema/dpdl-v1.yaml`. After publication, consumers can install it with:

```sh
npm install @olympion/dpdl-schema
```

To publish a new schema package version, update `version` in `package.json` and publish from a configured npm account:

```sh
npm publish --access public
```

See [`docs/architecture.md`](docs/architecture.md) for repository responsibilities.
