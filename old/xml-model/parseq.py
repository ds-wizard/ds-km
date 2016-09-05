# Parse a question tree into a series of web pages.
#
import xml.etree.ElementTree as ET
import glob
import os

class FileNamer(object):
    """ Make sure we have systematic file names"""
    generate_toplevel = 'result'
    url_toplevel = ''
    generate_extension = '.html'
    url_extension = '.html'

    def __init__(self):
        """ Create object.
        
            c = chapter, q = question, a = answer. Each of them are elements in the
            element tree.
        """
        self.c = None
        self.q = None
        self.a = None

    def set(self, c=None, q=None, a=None):
        """ A single set function to 'locate' the state of the name to the right spot"""
        if c is not None:
            self.c = c
        if q is not None:
            self.q = q
        if a is not None:
            self.a = a

    def copy(self, c=None, q=None, a=None):
        """ Return a modified copy of myself"""
        other = self.__class__()
        other.set(c=self.c, q=self.q, a=self.a)
        other.set(c=c, q=q, a=a)
        return other
    
    def chapterdir(self):
        """ The name of the folder used for the current chapter"""
        return "c"+self.c.get('id')

    def chapter(self):
        """ The basename of the main file describing the current chapter"""
        return os.path.join(self.chapterdir(), 'index')

    def question(self):
        """ The basename of the file describing the current question"""
        return os.path.join(self.chapterdir(), 'q'+self.q.get('id'))

    def answer(self):
        """ The basename of the file describing the current answer"""
        s = self.a.get('id')
        if s is None:
            s = self.a.get('label')
            for c in ' :;/.,\'\"':
                s = s.replace(c,'')
            s = s.lower()
        return os.path.join(self.question()+"-"+s)

    def chapterfile(self):
        """ The filename where the current chapter description should be written
            on the local file system"""
        return os.path.join(self.generate_toplevel, self.chapter()+self.generate_extension)

    def chapterlink(self):
        """ The relative hyperlink from the top where the current chapter can be found"""
        return os.path.join(self.url_toplevel, self.chapter()+self.url_extension)

    def questionfile(self):
        """ The filename where the current question description should be written
            on the local file system"""
        return os.path.join(self.generate_toplevel, self.question()+self.generate_extension)

    def questionlink(self):
        """ The relative hyperlink from the top where the current chapter can be found"""
        return os.path.join(self.url_toplevel, self.question()+self.url_extension)

    def answerfile(self):
        """ The filename where the current answer description should be written
            on the local file system"""
        return os.path.join(self.generate_toplevel, self.answer()+self.generate_extension)

    def answerlink(self):
        """ The relative hyperlink from the top where the current answer can be found"""
        return os.path.join(self.url_toplevel, self.answer()+self.url_extension)

    def mkdir(self):
        """ Create the directory on the local file system where the files for the current chapter will be
            written, if it does not yet exist"""
        fn = os.path.join(self.generate_toplevel, self.chapterdir())
        if not os.path.isdir(fn):
            os.mkdir(fn)

class HTFileNamer(FileNamer):
    """ A version of the filenamer that knows about the conventions for the ht2html template processor"""
    generate_extension = '.en.ht'

def getq(id):
    """ Retrieve the question node with the given id"""
    return root.find(".//question[@id='%s']" % id)

class QPath(object):
    """ The route to the current question"""
    def __init__(self):
        self.qdata = []
        self.adata = {}
        self.qnext = {}

    def addq(self, q):
        self.qdata.append(q)

    def adda(self, a):
        q = self.topq()
        self.adata[q.get('id')] = a

    def addfollowuprow(self, row):
        for i in range(len(row)-1):
            if row[i] in self.qnext:
                raise ValueError("Conflicting values for next question")
            self.qnext[row[i].get('id')] = row[i+1]

    def pop(self):
        q = self.qdata.pop()
        try:
            del self.adata[q.get('id')]
        except KeyError:
            pass # Open question

    def iterqa(self):
        for q in self.qdata:
            yield q, self.adata[q.get('id')]

    def topq(self):
        return self.qdata[-1]
    
    def toptitle(self):
        return self.topq().get('title')

    def nextq(self):
        # Figure out in the element tree what the next question would be
        level = len(self.qdata)-1
        while level >= 0:
            q = self.qdata[level]
            try:
                return self.qnext[q.get('id')]
            except KeyError:
                level -= 1
        return None
    
class HTGenerator(object):
    """ A Question Tree Generator that produces input for the ht2html framework"""
    def __init__(self):
        self.namer = HTFileNamer()
        self.qpath = QPath()

    def setallq(self, allq):
        self.allq = allq
        self.doneq = set()

    def toplevelq(self):
        """ Find out which questions are not referred to by any "followup" statements"""
        called_ids = set()
        for q in self.allq:
            for q2 in q.findall('answer/ask'):
                q2id = q2.get('id')
                if q2id in called_ids:
                    raise ValueError("Same question is followup to two answers: %s" % q2id)
                called_ids.add(q2id)
        tlq = []
        for q in self.allq:
            if not q.get('id') in called_ids:
                tlq.append(q)
        return tlq

    def qdone(self, q):
        self.doneq.add(q)

    def qcheck(self):
        # print "DBG> doneq", self.doneq
        # print "DBG> allq", self.allq
        leftq = set(self.allq) - self.doneq
        if len(leftq) > 0:
            print "Some questions have not been generated:"
            for q in leftq:
                print "==>",q.attrib
    
    def makechapter(self, c, endlink):
        self.endlink = endlink
        self.namer.set(c=c)
        self.namer.mkdir()
        fn = self.namer.chapterfile()
        self.setallq(c.findall('question'))
        f = open(fn, 'w')
        f.write("Title: %s\n\n" % c.get('title'))
        f.write("<p>%s</p>\n" % c.text)
        f.write("<p>The questions in this chapter address the following issues:</p>\n")
        f.write("<p><ol>\n")
        qrow = self.toplevelq()
        self.qpath.addfollowuprow(qrow)
        for q in qrow:
            f.write('<li><a href="../%s">%s</a>\n' % (self.namer.copy(q=q).questionlink(), q.get('title')))
            self.makequestion(q)
        f.write("</ol></p>\n")
        self.namer.set(q=qrow[0])
        f.write('<p><a href="../%s">Let\'s get started</a></p>\n' % self.namer.questionlink())
        f.close()
        # Check whether all questions have been processed
        self.qcheck()

    def makequestion(self, q):
        self.qdone(q)
        oldnamer = self.namer.copy()
        try:
            self.namer.set(q=q)
            self._makequestion(q)
        finally:
            # Ugly, but this is the consequence of using a "global" variable namer....
            # It could have been clobbered by recursive questions
            self.namer = oldnamer

    def _makequestion(self, q):
        fn = self.namer.questionfile()
        f = open(fn, 'w')
        f.write("Title: %s\n\n" % q.get('title'))
        first = True
        for (q2, a2) in self.qpath.iterqa():
            if first:
                f.write('<h2>How we got here</h2>\n<ul>\n')
                first = False
            f.write("<li>%s %s!</li>\n" % (q2.get('title'), a2.get('label')))
        if not first:
            f.write('</ul>\n')
        f.write("<h1>%s</h1>\n" % q.get('title'))
        if q.text is not None:
            f.write("<p>%s</p>\n" % q.text)
        s = []
        self.qpath.addq(q)
        # Some sanity in anwers
        labels = [answer.get('label') for answer in q.iter('answer')]
        if 'Yes' in labels and 'No' not in labels:
            print "WARNING: question %s has Yes but lacks No answer" % q.get('id')
        if 'No' in labels and 'Yes' not in labels:
            print "WARNING: question %s has No but lacks Yes answer" % q.get('id')
        for answer in q.iter('answer'):
            self.namer.set(a=answer)
            # If the answer has only one followup question, and there is no answer text,
            # link there immediately. Otherwise, jump to the page with the answer.
            if (answer.get('responsetype') == 'followup' and
                len(answer.text.strip()) == 0 and
                len(answer.findall('ask')) == 1):
                q2 = getq(answer.find('ask').get('id'))
                s.append('<a href="../%s">%s</a>' % (
                    self.namer.copy(q=q2).questionlink(), answer.get('label')))
            elif (answer.get('responsetype') == 'ok'):
                if answer.text is not None and len(answer.text.strip()) > 0:
                    print "WARNING: OK-type answer has text for %s %s" % (
                        q.get('id'), answer.get('label'))
                assert self.qpath.topq() == q
                q2 = self.qpath.nextq()
                if q2 is not None:
                    s.append('<a href="../%s">%s</a> (go to next subject)' % (
                        self.namer.copy(q=q2).questionlink(), answer.get('label')))
                else:
                    s.append('<a href="../../%s">%s</a>' % (
                        self.endlink, answer.get('label')))
            else:
                s.append('<a href="../%s">%s</a>' % (
                    self.namer.answerlink(), answer.get('label')))
            self.makeanswer(answer)
        if len(s) == 0:
            # Open Question
            f.write("<p>This is an open question. There are no followup questions. "
                    "If you have answered this for yourself, we can continue.</p>\n")
            q2 = self.qpath.nextq()
            if q2 is not None:
                s.append('<a href="../%s">Got that, next question please!</a>' % (
                    self.namer.copy(q=q2).questionlink()))
            else:
                s.append('<a href="../../%s">Got that. Continue.</a>' % self.endlink)
        f.write("<p>"+" | ".join(s)+"</p>\n")
        self.qpath.pop()
        # TODO: show the expert, from this level or any higher level.
        f.close()

    def makeanswer(self, a):
        self.namer.set(a=a)
        self.qpath.adda(a)
        if a.get('responsetype') == 'ok':
            pass
        elif a.get('responsetype') == 'advice':
            self.makeadvice(a)
        elif a.get('responsetype') == 'followup':
            self.makefollowup(a)
        else:
            raise ValueError("Unknown responsetype %s" % a.get('responsetype'))
            
    def makeadvice(self, a):
        fn = self.namer.answerfile()
        f = open(fn, 'w')
        f.write("Title: %s %s\n\n" % (self.qpath.toptitle(), a.get('label')))
        f.write("<H2>%s You answered: %s</H2>\n" % (self.qpath.toptitle(), a.get('label')))
        f.write("<p>%s</p>\n" % a.text)
        # Where can we go from here?
        f.write("<p>")
        thisqlink = self.namer.copy(q=self.qpath.topq()).questionlink()
        f.write('<a href="../%s">Answer this question again</a>' % thisqlink)
        f.write(' | ')
        nextq = self.qpath.nextq()
        if nextq is None:
            # This was the last question of this chapter.
            # TODO: jump to next chapter, or offer jump to finish page
            f.write("This was the last question.\n")
        else:
            nextqlink = self.namer.copy(nextq).questionlink()        
            f.write('<a href="../%s">Go to next question</a>' % nextqlink)
        f.write("</p>\n")

    def makefollowup(self, a):
        fn = self.namer.answerfile()
        f = open(fn, 'w')
        f.write("Title: %s %s\n\n" % (self.qpath.toptitle(), a.get('label')))
        f.write("<H2>%s You answered: %s</H2>\n" % (self.qpath.toptitle(), a.get('label')))
        f.write("<p>%s</p>\n" % a.text)
        f.write("<p>The following questions now need to be addressed:</p>\n")
        f.write("<p><ol>\n")
        qra = []
        for aa in a.findall('ask'):
            q = getq(id=aa.get('id'))
            if q is None:
                 raise ValueError("Referenced Question '%s' does not exist" % aa.get('id'))
            else:
                qra.append(q)
        # Store the array to be able to "calculate the next question".
        if len(qra) == 0:
            raise ValueError("No answers in followup for %s" % self.qpath.toptitle())
        self.qpath.addfollowuprow(qra)
        for q in qra:
            f.write('<li><a href="../%s">%s</a>\n' % (self.namer.copy(q=q).questionlink(), q.get('title')))
            self.makequestion(q)
        f.write("</ol></p>\n")
        f.write('<p><a href="../%s">Let\'s continue</a></p>\n' % self.namer.copy(q=qra[0]).questionlink())
        f.close()

if __name__ == "__main__":
    g = HTGenerator()

    # Index all the chapters
    chapters = {}
    for fn in glob.glob('q*.xml'):
        tree = ET.parse(fn)
        root = tree.getroot()

        for chapter in root.findall('chapter'):
            chapid = int(chapter.get('id'))
            assert chapid not in chapters, "Duplicate chapter id"
            chapters[chapid] = chapter.get('title')
            if len(chapter.findall('answer'))>0:
                   print "WARNING: There are answers outside of questions"

    # Create the pages for all the questions in the chapters
    for fn in glob.glob('q*.xml'):
        tree = ET.parse(fn)
        root = tree.getroot()

        for chapter in root.findall('chapter'):
            print "Running chapter", chapter.attrib
            chapid = int(chapter.get('id'))
            if chapid+1 in chapters:
                endlink = "c%d/" % (chapid+1)
            else:
                assert chapid == len(chapters), "Chapter ids not sequential?"
                # TODO: make this page, and ask people for feedback
                endlink = "end.html"
            g.makechapter(chapter, endlink=endlink)

    # Create top level index with all chapters
    f = open(os.path.join(FileNamer.generate_toplevel, 'start.en.ht'), 'w')
    f.write('Title: The Data Stewardship Questionnaire: chapter index\n\n')
    f.write("The questionnaire has the following chapters:\n")
    f.write("<ul>\n")
    for chapno, chaptitle in chapters.items():
        f.write('<li><b>%s</b>: <a href="c%s/">%s</a>\n' % (
            chapno, chapno, chaptitle))
    f.write("</ul>\n")
    f.write('<p><a href="c1/">Start at the beginning</a>\n')
    f.close()
