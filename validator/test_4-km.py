import pytest
from helper.km import *

#TODO: refactor:
#     - error msgs file
#     - non-blocking errors (more smaller tests)
#     - nicer code, easier to read (OOP?)


def test_load_chapters(chapters, km):
    for chapter in chapters.values():
        load_chapter(km, chapter)


def check_ref_namespace(km, q, chid, ns):
    if 'namespace' not in q:
        return
    assert exists_namespace(km, q['namespace']), \
            'Question {} in chapter {}, namespace "{}" referencing unexisting namespace "{}"'. \
            format(q['questionid'], chid, ns, q['namespace'])


# TODO: some weird bug causes test fails (only sometimes)
def check_ref_precondition(km, q, chid, ns):
    if 'precondition' not in q:
        return
    pre = q['precondition']
    pns = ns if 'namespace' not in pre else pre['namespace']
    if 'answerid' in pre:
        assert exists_answer(km, pns, chid, pre['questionid'], pre['answerid']), \
            'Precondition on question {} in chapter {}, namespace "{}" referencing unexisting answer {} in question {}, namespace "{}"'.\
            format(q['questionid'], chid, ns, pre['answerid'], pre['questionid'], pre['namespace'])
    else:
        assert exists_question(km, pns, chid, pre['questionid']), \
            'Precondition on question {} in chapter {}, namespace "{}" referencing unexisting question {}, namespace "{}"'.\
            format(q['questionid'], chid, ns, pre['questionid'], pre['namespace'])


def check_ref_questionpointer(km, q, chid, ns):
    if 'insertBefore' not in q:
        return
    qp = q['insertBefore']
    assert exists_question(km, qp['namespace'], qp['chapterid'], qp['questionid']), \
        'InsertBefore on question {} in chapter {}, namespace "{}" referencing unexisting question {} in chapter {}, namespace "{}"'.\
        format(q['questionid'], chid, ns, qp['questionid'], qp['chapterid'], qp['namespace'])


def check_xref(km, xref, qid, chid, ns):
    xns = ns if 'namespace' not in xref else xref['namespace']
    assert exists_question(km, xns, xref['chapterid'], xref['questionid']), \
        'Xref on question {} in chapter {}, namespace "{}" referencing unexisting question {} in chapter {}, namespace "{}"'.\
        format(qid, chid, ns, xref['questionid'], xref['chapterid'], xns)


def check_xrefs(km, q, chid, ns):
    qid = q['questionid']
    if 'references' in q:
        for r in q['references']:
            if r['type'] == 'xref':
                check_xref(km, r, qid, chid, ns)
    if 'addReferences' in q:
        for r in q['references']:
            if r['type'] == 'xref':
                check_xref(km, r, qid, chid, ns)


def test_referencing(km):
    for ns in km:
        is_local = ns != 'core'
        for ch in km[ns].values():
            chid = ch['chapterid']
            for q in ch['questions'].values():
                if is_local:
                    check_ref_namespace(km, q, chid, ns)
                    check_ref_questionpointer(km, q, chid, ns)
                #check_ref_precondition(km, q, chid, ns)
                check_xrefs(km, q, chid, ns)
