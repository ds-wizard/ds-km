import os


def extract_chapterid(filepath):
    try:
        filename = os.path.split(filepath)[-1]
        if filename[0:7] == 'chapter' and filename[-5:] == '.json':
            return int(filename[7:-5])
        else:
            return 0
    except ValueError:
        return -1


def is_chapter(filepath):
    return extract_chapterid(filepath) > 0


def kmfs2dict(root):
    kmfs = {'dirs': {}, 'files': []}
    for name in os.listdir(root):
        filepath = os.path.join(root, name)
        if os.path.isfile(filepath):
            kmfs['files'].append(filepath)
        elif os.path.isdir(filepath) and not name.startswith('.'):
            kmfs['dirs'][name] = kmfs2dict(filepath)
        else:
            pass
    return kmfs


if __name__ == '__main__':
    kmfs = kmfs2dict('./datamodel')
    print(kmfs)
    print(extract_chapterid('datamodel/core/chapter1.json'))
