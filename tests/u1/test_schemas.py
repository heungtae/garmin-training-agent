import json
import unittest

from jsonschema import Draft202012Validator

from approved_digests import SCHEMA_SHA256, digest
from u1_validation import COMMON_NAMES, SPEC, U2_NAMES, schema_id

DIALECT = "https://json-schema.org/draft/2020-12/schema"


def schema_path(name):
    return SPEC / f"{name}.schema.json"


def load_schema(name):
    return json.loads(schema_path(name).read_text(encoding="utf-8"))


class SchemaTests(unittest.TestCase):
    def test_exact_inventory(self):
        common_paths = set(SPEC.glob("*.schema.json")) - {schema_path(n) for n in U2_NAMES}
        self.assertEqual(common_paths, {schema_path(n) for n in COMMON_NAMES})

    def test_stable_identifiers(self):
        self.assertEqual(
            {load_schema(n)["$id"] for n in COMMON_NAMES},
            {schema_id(n) for n in COMMON_NAMES},
        )

    def test_dialect(self):
        for name in COMMON_NAMES:
            with self.subTest(name=name):
                self.assertEqual(load_schema(name)["$schema"], DIALECT)

    def test_metaschemas(self):
        for name in COMMON_NAMES:
            with self.subTest(name=name):
                Draft202012Validator.check_schema(load_schema(name))

    def test_approved_contents(self):
        for name in COMMON_NAMES:
            with self.subTest(name=name):
                self.assertEqual(digest(schema_path(name)), SCHEMA_SHA256[name])
