import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = yaml.safe_load((ROOT / "schemas" / "dpdl-v1.yaml").read_text(encoding="utf-8"))


class DpdlSchemaTests(unittest.TestCase):
    def test_schema_is_valid_draft_2020_12(self):
        Draft202012Validator.check_schema(SCHEMA)

    def test_template_is_valid(self):
        template = yaml.safe_load(
            (ROOT / "templates" / "employee.yaml").read_text(encoding="utf-8")
        )
        Draft202012Validator(SCHEMA).validate(template)

    def test_required_fields_and_unknown_fields_are_rejected(self):
        definition = {
            "id": "customer-support",
            "name": "Customer Support",
            "version": "1.0.0",
            "description": "Helps customers.",
            "role": "Support",
            "capabilities": ["answer-questions"],
            "unexpected": True,
        }
        errors = list(Draft202012Validator(SCHEMA).iter_errors(definition))
        self.assertTrue(any("unexpected" in error.message for error in errors))
        del definition["id"]
        errors = list(Draft202012Validator(SCHEMA).iter_errors(definition))
        self.assertTrue(any("'id' is a required property" in error.message for error in errors))

    def test_invalid_identifier_version_and_empty_capabilities_are_rejected(self):
        definition = {
            "id": "Not Valid",
            "name": "Customer Support",
            "version": "latest",
            "description": "Helps customers.",
            "role": "Support",
            "capabilities": [],
        }
        errors = list(Draft202012Validator(SCHEMA).iter_errors(definition))
        self.assertEqual({"id", "version", "capabilities"}, {error.path[0] for error in errors})


if __name__ == "__main__":
    unittest.main()
