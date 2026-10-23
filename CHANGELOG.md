# Changelog

## 1.0.0

Initial DPDL v1 contract, packaged as `@olympion/dpdl-schema` version 1.0.0.
The root definition contains:

- `id` (string), `name` (string), `version` (semantic-version string),
  `description` (string), `domain` (enum), `role` (string), and `capabilities`
  (non-empty array of strings).
- Optional `skills` and `tools` arrays of unique strings, a `responsibilities`
  array of strings, and an `extensions` object for namespaced custom fields.
- Optional `memoryModel`, whose required `scope` is one of `none`, `session`,
  `user`, or `organization`.
- Optional `workflows` array of objects with required `name` and `role`, and
  optional `description` and ordered `steps`.
- Optional `guardrails` array of objects with required `description` and
  `severity`.

The `domain` values are `business`, `engineering`, `finance`, `operations`,
`retail`, and `security`. Workflow `role` values are `primary`, `supporting`,
and `fallback`. Guardrail `severity` values are `low`, `medium`, `high`, and
`critical`.
