import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


SPEC = Path(__file__).resolve().parents[2] / "spec/u1"
DETAIL_ID = "urn:gta:contract:C03:1.0.0#/$defs/Detail"
COMMON_NAMES = ("common", *(f"C{i:02}" for i in range(1, 9)))
U2_NAMES = ("LLM_REQUEST", "LLM_RESPONSE", "EVALUATION")


def schema_id(name):
    return f"urn:gta:contract:{name}:1.0.0"


def registry_resources(manifest, names):
    inventory = {schema_id(name): f"{name}.schema.json" for name in names}
    schemas = {}
    for entry in manifest["schemas"]:
        identifier = entry["id"]
        if identifier in schemas:
            raise ValueError(f"Duplicate registry entry: {identifier}")
        filename = inventory.get(identifier)
        if filename is None or filename != entry["file"]:
            raise ValueError(f"Unexpected registry entry: {identifier}")
        path = SPEC / filename
        schema = json.loads(path.read_text(encoding="utf-8"))
        if schema["$id"] != identifier:
            raise ValueError(f"Schema identifier mismatch: {identifier}")
        schemas[identifier] = Resource.from_contents(schema)
    if schemas.keys() != inventory.keys():
        raise ValueError("Schema inventory and registry differ")
    return schemas.items()


def load_registry(manifest):
    if manifest["fragments"] != [DETAIL_ID]:
        raise ValueError("Unexpected registered fragments")

    # Registry's default retrieval refuses every resource outside the local set.
    registry = Registry().with_resources(registry_resources(manifest, COMMON_NAMES))
    registry.resolver().lookup(DETAIL_ID)
    return registry


def fixed_registry():
    manifest = json.loads((SPEC / "registry.json").read_text(encoding="utf-8"))
    return load_registry(manifest)


def preserved_u2_registry():
    manifest = json.loads((SPEC / "u2-owned-registry.json").read_text(encoding="utf-8"))
    return fixed_registry().with_resources(registry_resources(manifest, U2_NAMES))


def validator_for(identifier, registry=None):
    if registry is None:
        registry = fixed_registry()
    if identifier not in registry and identifier != DETAIL_ID:
        raise KeyError(identifier)
    return Draft202012Validator(
        {"$ref": identifier}, registry=registry,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )
