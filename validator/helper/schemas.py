import json
import jsonschema
import os

schema_root = 'schema'
chapter_dir = 'chapter'


# TODO: catch and provide nicer info
def load_schema(schemas, schemafile, version):
    with open(schemafile, mode='r') as f:
        schemas[version] = json.load(f)


def list_chapter_schemas():
    root = os.path.join(schema_root, chapter_dir)
    schemas = []
    for name in os.listdir(root):
        filepath = os.path.join(root, name)
        if os.path.isfile(filepath) and \
           filepath.startswith('v') and \
           filepath.endswith('.json'):
            schemas.append(filepath)
    return schemas


def extract_schemaversion(schema_filepath):
    filename = os.path.split(schema_filepath)[-1]
    return int(filename[1:-5])


# TODO: catch and provide nicer info
def check_schema(schema):
    jsonschema.Draft4Validator.check_schema(schema)


# TODO: make own JSON Schema errors as in jschematest.py
def get_validator(schema):
    return jsonschema.Draft4Validator(schema)
