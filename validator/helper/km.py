# TODO: own exceptions


def load_chapter(km, chapter):
    chid = chapter['uuid']
    ns = chapter['namespace']
    if exists_chapter(km, ns, chid):
        raise KeyError('Chapter {} in NS {} already exists!'.format(chid, ns))
    elif ns not in km:
        km[ns] = dict()
    questions = dict()
    for q in chapter['questions']:
        qid = q['uuid']
        if qid in questions:
            raise KeyError('Question {} in chapter {}, NS {} already exists!'.format(qid, chid, ns))
        questions[qid] = _transform_question(q, qid, chid, ns)
    chapter['questions'] = questions
    km[ns][chid] = chapter


def build_uuid_dict(km):
    result = dict()

    def add(objtype, obj):
        if obj['uuid'] in result:
            raise KeyError('UUID duplicity: {}'.format(obj['uuid']))
        result[obj['uuid']] = (objtype, obj)

    chapters = []
    for chid in km["core"]:  # TODO: all ns
        chapters.append(km["core"][chid])
    for chapter in chapters:
        add('chapter', chapter)
        for question in chapter['questions'].values():
            add('question', question)
            for answer in question.get('experts', dict()).values():
                add('answer', answer)
            for expert in question.get('experts', []):
                add('expert', expert)
            for reference in question.get('references', []):
                add('reference', reference)
    return result


def _transform_question(q, qid, chid, ns):
    if 'answers' in q:
        answers = {}
        for a in q['answers']:
            aid = a['uuid']
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
