import unittest

from jsonschema import Draft202012Validator

from approved_digests import SCHEMA_SHA256, VECTORS_SHA256, digest
from case_vectors import VECTORS_PATH, case_document, load_vectors
from test_registry import references
from test_schemas import DIALECT, load_schema, schema_path
from u1_validation import (
    COMMON_NAMES, DETAIL_ID, U2_NAMES, preserved_u2_registry, schema_id, validator_for,
)


class PreservedContractTests(unittest.TestCase):
    def test_original_vectors_preserved(self):
        self.assertEqual(digest(VECTORS_PATH), VECTORS_SHA256)

    def test_u2_owned_schemas_preserved(self):
        for name in U2_NAMES:
            with self.subTest(name=name):
                self.assertEqual(digest(schema_path(name)), SCHEMA_SHA256[name])
                schema = load_schema(name)
                self.assertEqual(schema["$schema"], DIALECT)
                self.assertEqual(schema["$id"], schema_id(name))
                Draft202012Validator.check_schema(schema)

    def test_all_cases_have_an_owner(self):
        vectors = load_vectors()
        known = {schema_id(name) for name in (*COMMON_NAMES, *U2_NAMES)} | {DETAIL_ID}
        self.assertEqual(len(vectors["cases"]), 54)
        self.assertEqual(len({case["id"] for case in vectors["cases"]}), 54)
        self.assertLessEqual({case["schemaId"] for case in vectors["cases"]}, known)

    def test_u2_owned_schema_references_resolve_locally(self):
        registry = preserved_u2_registry()
        for name in U2_NAMES:
            resolver = registry.resolver(schema_id(name))
            for ref in set(references(load_schema(name))):
                with self.subTest(name=name, ref=ref):
                    resolver.lookup(ref)

    def test_u2_owned_structure_cases(self):
        registry = preserved_u2_registry()
        owned = {schema_id(name) for name in U2_NAMES}
        vectors = load_vectors()
        cases = [case for case in vectors["cases"] if case["schemaId"] in owned]
        self.assertEqual(len(cases), 11)
        for case in cases:
            with self.subTest(case=case["id"]):
                document = case_document(vectors["fixtures"], case)
                validator = validator_for(case["schemaId"], registry)
                self.assertEqual(validator.is_valid(document), case["expectedSchema"])
