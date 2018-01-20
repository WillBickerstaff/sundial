import os
import sys
import time
from itertools import permutations
#tncimgeop


#functions to compute n!
def fact(n):
    """Computes n!, input n"""
    if n == 0:
        return 1
    else:
        p = 1
        while n != 1:
            p *= n
            n = n - 1
        return p


#function to compute nPr
def perm(n, r):
    """computes nPr, input n,r"""
    b = (n - r)
    a = fact(n)
    b = fact(b)
    c = a // b
    return c


class Match(object):

    def __init__(self, **kwargs):
        self.chars = ''
        self.dict = None
        self.minlen = 3
        self.match = set()
        self.__statusHandler = None
        self.mand1st=None        
        self.parse_kwargs(**kwargs)
        self.__nperms = 0
        self.__calcnPermutations()
        self.completeTime = None
        
    def __calcnPermutations(self):
        for i in range(self.minlen, len(self.chars) + 1):
            self.__nperms += perm(len(self.chars), i)

    def parse_kwargs(self, ** kwargs):
        for k in kwargs:
            kw = k.lower()
            if kw == 'minlen':
                self.minlen = kwargs[k]
                continue
            if kw in 'dictfile':
                self.dict = kwargs[k]
                continue
            if kw in ['chars', 'letters']:
                self.chars = kwargs[k]
                continue
            if kw == 'statushandler':
                self.__statusHandler = kwargs[k]
                continue
            if kw == 'mand1st':
                self.mand1st = kwargs[k]
                continue

    def status(self, text):
        if self.__statusHandler is not None:
            self.__statusHandler(text)

    def wordMatch(self):
        stime = time.time()
        match = set()
        dic = Dictionary(self.dict)
        dic.omit_seq = ["'"]
        if self.mand1st:
            dic.req_seq = [self.chars[0]]
        dictwords = dic.words()
        msg = 'Checking %d permutations of characters %s' % (self.__nperms,
                                                             self.chars)
        self.status(msg)
        for i in range(self.minlen, len(self.chars) + 1):
            s = dictwords & set(''.join(l)
                                    for l in permutations(self.chars, i))
            match = match | s

        self.completeTime = (time.time() - stime)
        msg = 'Completed in {0:.3f}s'.format(self.completeTime)
        self.status(msg)
        self.match = sorted(match, key=lambda x: len(x))
        return self.match

    def words_of_length(self, words, length):
        return sorted([x for x in words if len(x) == length])


class Dictionary(object):

    def __init__(self, dictfile=None):
        self.__dictfile = None
        self.dictfile(dictfile)
        self.req_seq = []
        self.omit_seq = []
        self._words = set()

    def words(self):
        with open(self.__dictfile, 'r') as df:
            for line in df:
                word = line.lower().strip()
                if (len([x for x in self.req_seq if x in word]) ==
                    len(self.req_seq) and
                    len([x for x in self.omit_seq if x in word]) == 0):
                    self._words.add(word)
        return self._words

    def dictfile(self, filename):
        if filename is None:
            filename = self.osDictFile()
        try:
            if filename is not None and os.path.isfile(filename):
                with open(filename, 'r'):
                    pass
                self.__dictfile = filename
                return True
        except IOError:
            pass
        msg = 'No dictionary file'
        if filename is not None:
            msg = '%s does not exist' % filename
        raise IOError(msg)

    def osDictFile(self):
        if 'linux' in sys.platform:
            self.dictfile('/usr/share/dict/words')

        return self.__dictfile
