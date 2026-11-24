import json
import unittest

from referencing.exceptions import Unresolvable

from test_schemas import load_schema
from u1_validation import (
    COMMON_NAMES, DETAIL_ID, SPEC, U2_NAMES, fixed_registry, load_registry,
    schema_id, validator_for,
)


def references(node):
    if isinstance(node, dict):
        if "$ref" in node:
            yield node["$ref"]
        for child in node.values():
            yield from references(child)
    elif isinstance(node, list):
        for child in node:
            yield from references(child)


class RegistryTests(unittest.TestCase):
    def test_exact_registered_ids(self):
        self.assertEqual(set(fixed_registry()), {schema_id(n) for n in COMMON_NAMES})

    def test_registered_detail_fragment(self):
        self.assertEqual(validator_for(DETAIL_ID).schema, {"$ref": DETAIL_ID})
        self.assertEqual(
            fixed_registry().resolver().lookup(DETAIL_ID).contents,
            load_schema("C03")["$defs"]["Detail"],
        )

    def test_all_schema_references_resolve_locally(self):
        registry = fixed_registry()
        for name in COMMON_NAMES:
            resolver = registry.resolver(schema_id(name))
            for ref in set(references(load_schema(name))):
                with self.subTest(name=name, ref=ref):
                    resolver.lookup(ref)

    def test_unknown_version_rejected(self):
        for identifier in ("urn:gta:contract:C03:2.0.0", *(schema_id(n) for n in U2_NAMES)):
            with self.subTest(identifier=identifier), self.assertRaises(KeyError):
                validator_for(identifier)

    def test_unregistered_fragment_rejected(self):
        with self.assertRaises(KeyError):
            validator_for(schema_id("C03") + "#/$defs/Activity")

    def test_remote_references_are_unresolvable(self):
        with self.assertRaises(Unresolvable):
            fixed_registry().resolver().lookup("https://example.invalid/schema")

    def test_duplicate_registry_ids_rejected(self):
        manifest = json.loads((SPEC / "registry.json").read_text(encoding="utf-8"))
        manifest["schemas"].append(manifest["schemas"][0])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            load_registry(manifest)

    def test_missing_registry_entry_rejected(self):
        manifest = json.loads((SPEC / "registry.json").read_text(encoding="utf-8"))
        manifest["schemas"].pop()
        with self.assertRaisesRegex(ValueError, "inventory"):
            load_registry(manifest)
