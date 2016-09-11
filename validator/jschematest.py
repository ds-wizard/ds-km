# Testing jsonschema error printing capabilities
import jsonschema
import json


# Custom printing of errors (skip no-information messages)
# TODO: solve repetition of same error (with different paths)
def print_errors(errors, indent=0):
    next_indent = indent + 2
    for error in errors:
        msg = error.message
        print(' '*indent, end='')
        if error.validator in ['anyOf', 'oneOf', 'allOf']:
            if 'questionid' in error.instance:
                qid = error.instance['questionid']
                print('Question with ID {} is not valid:'.format(qid))
            elif 'chapterid' in error.instance:
                chid = error.instance['chapterid']
                print('Chapter with ID {} is not valid:'.format(chid))
            else:
                print(msg)
        else:
            print(msg)
        new_errors = sorted(error.context, key=lambda e: e.schema_path)
        print_errors(new_errors, next_indent)

with open('../schema.alt.json') as f:
    schema = json.load(f)
with open('../datamodel/core/chapter1.json') as f:
    instance = json.load(f)
v = jsonschema.Draft4Validator(schema)
errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
print_errors(errors)
