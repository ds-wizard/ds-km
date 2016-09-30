# TODO: own exceptions


def load_chapter(km, chapter):
    chid = chapter['chapterid']
    ns = chapter['namespace']
    if exists_chapter(km, ns, chid):
        raise KeyError('Chapter {} in NS {} already exists!'.format(chid, ns))
    km[ns] = {}
    questions = {}
    for q in chapter['questions']:
        qid = q['questionid']
        if qid in questions:
            raise KeyError('Question {} in chapter {}, NS {} already exists!'.format(qid, chid, ns))
        questions[qid] = _transform_question(q, qid, chid, ns)
    chapter['questions'] = questions
    km[ns][chid] = chapter


def _transform_question(q, qid, chid, ns):
    if 'answers' in q:
        answers = {}
        for a in q['answers']:
            aid = a['id']
            if aid in answers:
                raise KeyError('Answer {} in question {}, chapter {}, NS {} alread exists!'.format(aid, qid, chid, ns))
            answers[aid] = a
        q['answers'] = answers
    return q


def exists_namespace(km, namespace):
    return namespace in km


def exists_chapter(km, namespace, chapterid):
    return exists_namespace(km, namespace) and \
           chapterid in km[namespace]


def exists_question(km, namespace, chapterid, questionid):
    return exists_chapter(km, namespace, chapterid) and \
           questionid in km[namespace][chapterid]['questions']


def exists_answer(km, namespace, chapterid, questionid, answerid):
    return exists_question(km, namespace, chapterid, questionid) and \
           'answers' in km[namespace][chapterid]['questions'][questionid] and \
           answerid in km[namespace][chapterid]['questions'][questionid]['answers']


