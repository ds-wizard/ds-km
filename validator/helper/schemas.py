import json
import jsonschema


def load_schema(schemas, schemafile, version):
    with open(schemafile, mode='r') as f:
        schemas[version] = json.load(f)


def check_schema(schema):
    jsonschema.Draft4Validator.check_schema(schema)


# TODO: make own JSON Schema errors as in jschematest.py
def get_validator(schema):
    return jsonschema.Draft4Validator(schema)
