import copy
import json
from pathlib import Path


VECTORS_PATH = Path(__file__).with_name("contract-cases.json")


def load_vectors():
    return json.loads(VECTORS_PATH.read_text(encoding="utf-8"))


def case_document(fixtures, case):
    document = copy.deepcopy(fixtures[case["fixture"]])
    for edit in case["edits"]:
        *parents, key = edit["path"]
        target = document
        for part in parents:
            target = target[part]
        match edit["op"]:
            case "remove":
                del target[key]
            case "add" | "replace":
                target[key] = copy.deepcopy(edit["value"])
            case _:
                raise ValueError(f"Unknown fixture operation: {edit['op']}")
    return document
