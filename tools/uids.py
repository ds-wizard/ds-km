import click
import json
import os
import uuid
import sys

import pyperclip


MAX_TRIES = 1000


def real_warning(msg):
    print('Warning: ' + msg, file=sys.stderr)


warn = real_warning


def generate_uuid(existing):
    new_uuid = uuid.uuid4()
    i = 0
    while new_uuid in existing:
        new_uuid = uuid.uuid4()
        i += 1
        if i > MAX_TRIES:
            raise RuntimeError(
                'Generated UUID not unique within {} tries'.format(MAX_TRIES)
            )
    return new_uuid


def iter_datamodel_chapter(root):
    for act_dir, dirs, files in os.walk(root):
        for name in files:
            if name.startswith('chapter') and name.endswith('.json'):
                with open(os.path.join(act_dir, name)) as f:
                    try:
                        x=json.load(f)
                    except:
                        sys.stderr.write("ERR loading> %s\n"%f)
                        raise
                    yield x


# TODO: distinguish core/local
def walk_datamodel_uids(root):
    uuids = set()
    for chapter in iter_datamodel_chapter(root):
        if 'uuid' not in chapter:
            warn('UUID not set for chapter "{}"'.format(chapter['title']))
        #elif chapter['uuid'] in uuids:
        #    warn('UUID not unique for chapter "{}"'.format(chapter['title']))
        else:
            uuids.add(chapter['uuid'])

        for question in chapter['questions']:
            if 'uuid' not in question:
                warn('UID not set for question "{}"'.format(question['title']))
            #elif question['uuid'] in uuids:
            #    warn('UID not unique for question "{}"'.format(question['title']))
            else:
                uuids.add(question['uuid'])

            for answer in question.get('answers', []):
                if 'uuid' not in answer:
                    warn('UID not set for answer "{}" in question "{}"'.format(answer['label'], question['title']))
                #elif answer['uid'] in uuids:
                #    warn('UID not unique for answer "{}" in question "{}"'.format(answer['label'], question['title']))
                else:
                    uuids.add(answer['uuid'])
    return uuids


@click.group()
@click.argument('dskm-root', type=click.Path())
@click.option('-q', '--quiet', is_flag=True)
@click.version_option(version='0.1', prog_name='DS KM UID generator')
@click.pass_context
def cli(ctx, dskm_root, quiet):
    ctx.obj['root'] = dskm_root
    if quiet:
        global warn
        warn = lambda msg: None


@cli.command()
@click.option('-n', '--count', default=1, type=int)
@click.option('-i', '--iterative', is_flag=True)
@click.option('-j', '--json-line', is_flag=True)
@click.pass_context
def generate(ctx, count, iterative, json_line):
    root = ctx.obj['root']
    uuids = walk_datamodel_uids(root)

    print_uid = lambda uid: print(uid)
    if json_line:
        print_uid = lambda uid: print('"uuid": "{}",'.format(uid))

    if iterative:
        x = generate_uuid(uuids)
        uuids.add(x)
        print_uid(x)
        pyperclip.copy(str(x))
        for _ in sys.stdin:
            x = generate_uuid(uuids)
            uuids.add(x)
            print_uid(x)
            pyperclip.copy(str(x))
    else:
        for i in range(count):
            x = generate_uuid(uuids)
            uuids.add(x)
            print_uid(x)


@cli.command()
@click.pass_context
def list(ctx):
    root = ctx.obj['root']
    uids = walk_datamodel_uids(root)
    for uid in uids:
        print(uid)

@cli.command()
@click.pass_context
def fill_filter(ctx):
    root = ctx.obj['root']
    uuids = walk_datamodel_uids(root)
    for line in sys.stdin:
        x = line.replace('"uuid": ""', '"uuid": "{}"'.format(
                generate_uuid(uuids)
            ))
        print(x, end='')

if __name__ == '__main__':
    cli(obj={})
