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

    def test_delivery_planner_definition_is_complete_and_valid(self):
        planner = yaml.safe_load(
            (
                ROOT
                / "business"
                / "planner"
                / "v1.0.0"
                / "planner.yaml"
            ).read_text(encoding="utf-8")
        )
        Draft202012Validator(SCHEMA).validate(planner)

        for field in (
            "identity",
            "profile",
            "responsibilities",
            "skills",
            "capabilities",
            "knowledgeDomains",
            "workflows",
            "kpis",
            "memoryModel",
            "collaborationModel",
            "guardrails",
            "runtime",
        ):
            with self.subTest(field=field):
                self.assertIn(field, planner)

        self.assertEqual(
            {
                "roadmap.write",
                "roadmap.read",
                "backlog.read",
                "backlog.write",
                "story.create",
                "story.update",
                "story.read",
                "task.create",
                "task.read",
            },
            set(planner["capabilities"]),
        )
        self.assertIn("Principal Engineer", planner["collaborationModel"]["canDelegate"])
        self.assertTrue(planner["runtime"]["model"])

    def test_required_fields_and_unknown_fields_are_rejected(self):
        definition = {
            "id": "customer-support",
            "name": "Customer Support",
            "version": "1.0.0",
            "description": "Helps customers.",
            "domain": "business",
            "role": "Support",
            "capabilities": ["answer-questions"],
            "unexpected": True,
        }
        errors = list(Draft202012Validator(SCHEMA).iter_errors(definition))
        self.assertTrue(any("unexpected" in error.message for error in errors))
        del definition["id"]
        errors = list(Draft202012Validator(SCHEMA).iter_errors(definition))
        self.assertTrue(any("'id' is a required property" in error.message for error in errors))

    def test_required_fields_are_documented_and_typed(self):
        for field in SCHEMA["required"]:
            with self.subTest(field=field):
                property_schema = SCHEMA["properties"][field]
                self.assertTrue(property_schema.get("description"))
                self.assertIn("type", property_schema)

        nested_schemas = (
            SCHEMA["properties"]["memoryModel"],
            SCHEMA["properties"]["workflows"]["items"],
            SCHEMA["properties"]["guardrails"]["items"],
        )
        for object_schema in nested_schemas:
            for field in object_schema["required"]:
                with self.subTest(field=field):
                    property_schema = object_schema["properties"][field]
                    self.assertTrue(property_schema.get("description"))
                    self.assertIn("type", property_schema)

    def test_enum_fields_reject_unsupported_values(self):
        definition = {
            "id": "customer-support",
            "name": "Customer Support",
            "version": "1.0.0",
            "description": "Helps customers.",
            "domain": "unknown",
            "role": "Support",
            "capabilities": ["answer-questions"],
            "memoryModel": {"scope": "global"},
            "workflows": [{"name": "answer", "role": "tertiary"}],
            "guardrails": [{"description": "Protect credentials.", "severity": "urgent"}],
        }
        errors = list(Draft202012Validator(SCHEMA).iter_errors(definition))
        self.assertEqual(
            {"domain", "memoryModel", "workflows", "guardrails"},
            {error.path[0] for error in errors},
        )

    def test_invalid_identifier_version_and_empty_capabilities_are_rejected(self):
        definition = {
            "id": "Not Valid",
            "name": "Customer Support",
            "version": "latest",
            "description": "Helps customers.",
            "domain": "business",
            "role": "Support",
            "capabilities": [],
        }
        errors = list(Draft202012Validator(SCHEMA).iter_errors(definition))
        self.assertEqual({"id", "version", "capabilities"}, {error.path[0] for error in errors})


if __name__ == "__main__":
    unittest.main()
