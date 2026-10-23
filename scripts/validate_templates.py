#!/usr/bin/env python3
"""Validate every YAML employee template against the DPDL v1 schema."""

from pathlib import Path
import sys

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "dpdl-v1.yaml"
SCAN_DIRS = ("templates", "examples", "engineering", "business")


def main() -> int:
    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    template_paths = sorted(
        path
        for pattern in ("*.yaml", "*.yml")
        for directory in SCAN_DIRS
        for path in (ROOT / directory).rglob(pattern)
    )
    if not template_paths:
        print(f"No YAML templates found in {", ".join(SCAN_DIRS)}", file=sys.stderr)
        return 1

    failed = False
    for path in template_paths:
        try:
            instance = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as error:
            print(f"{path.relative_to(ROOT)}: invalid YAML: {error}", file=sys.stderr)
            failed = True
            continue
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
        if errors:
            for error in errors:
                location = ".".join(str(part) for part in error.path) or "<root>"
                print(
                    f"{path.relative_to(ROOT)}: {location}: {error.message}",
                    file=sys.stderr,
                )
            failed = True

    if failed:
        return 1
    print(f"Validated {len(template_paths)} YAML template(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
