import copy
import unittest

from case_vectors import case_document, load_vectors
from u1_validation import DETAIL_ID, fixed_registry, schema_id, validator_for


class ContractCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = fixed_registry()
        vectors = load_vectors()
        cls.fixtures = vectors["fixtures"]
        accepted_ids = {*cls.registry, DETAIL_ID}
        cls.cases = [case for case in vectors["cases"] if case["schemaId"] in accepted_ids]

    def check_cases(self, prefix):
        cases = [case for case in self.cases if case["id"].startswith(prefix)]
        self.assertTrue(cases)
        for case in cases:
            with self.subTest(case=case["id"]):
                document = case_document(self.fixtures, case)
                validator = validator_for(case["schemaId"], self.registry)
                self.assertEqual(validator.is_valid(document), case["expectedSchema"])

    def test_positive_cases(self):
        self.check_cases("V")

    def test_negative_cases(self):
        self.check_cases("N")

    def test_boundary_cases(self):
        self.check_cases("B")

    def test_declared_formats_are_enforced(self):
        release = copy.deepcopy(self.fixtures["RELEASE"])
        release["contracts"][0]["schemaId"] = "relative/path"
        analysis = copy.deepcopy(self.fixtures["ANALYSIS"])
        analysis["generatedAt"] = "2026-02-30T00:00:00Z"
        for name, document, key in (
            ("C01", release, "schemaId"),
            ("C03", analysis, "generatedAt"),
        ):
            with self.subTest(contract=name):
                validator = validator_for(schema_id(name), self.registry)
                self.assertTrue(any(
                    error.validator == "format" and error.path[-1] == key
                    for error in validator.iter_errors(document)
                ))

    def test_every_case_group_has_unique_identity(self):
        keys = [case["id"] for case in self.cases]
        self.assertEqual(len(keys), 43)
        self.assertEqual(len(set(keys)), 43)
        self.assertEqual({key[0] for key in keys}, {"V", "N", "B"})
