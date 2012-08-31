import os
import sys
from itertools import permutations
#tncimgeop


class Match(object):

    def __init__(self, **kwargs):
        self.chars = ''
        self.dict = None
        self.minlen = 4
        self.match = set()
        self.parse_kwargs(**kwargs)

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

    def wordMatch(self):
        match = set()
        dic = Dictionary(self.dict)
        dic.req_seq = [self.chars[0]]
        dic.omit_seq = ["'"]
        dictwords = dic.words()

        for i in range(self.minlen, len(self.chars) + 1):
            s = dictwords & set(''.join(l)
                                    for l in permutations(self.chars, i))
            match = match | s

        return sorted(match, key=lambda x: len(x))

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
            msg = '%s is not a dictionary file' % filename
        raise IOError(msg)

    def osDictFile(self):
        if 'linux' in sys.platform:
            self.dictfile('/usr/share/dict/words')

        return self.__dictfile
