# Testing jsonschema error printing capabilities
import jsonschema
import json

# Custom printing of errors (skip no-information messages)
# TODO: solve repetition of same error (with different paths)
def print_errors(errors, indent=0):
    for error in errors:
        msg = error.message
        print(' '*indent, end='')
        if error.validator in ['anyOf', 'oneOf', 'allOf']:
            if 'questionid' in error.instance:
                print('Question with ID {} is not valid:'.format(error.instance['questionid']))
            elif 'chapterid' in error.instance:
                print('Chapter with ID {} is not valid:'.format(error.instance['chapterid']))
            else:
                print(msg)
        else:
            print(msg)
        print_errors(sorted(error.context, key=lambda e: e.schema_path), indent+2)

with open('../schema.alt.json') as f:
    schema = json.load(f)
with open('../datamodel/core/chapter1.json') as f:
    instance = json.load(f)
v = jsonschema.Draft4Validator(schema)
errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
print_errors(errors)
