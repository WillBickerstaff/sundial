import sys, os
from itertools import permutations
from textwrap import wrap, TextWrapper
#tncimgeop

letters = sys.argv[1].lower()
dictfile = '/usr/share/dict/words'
minlen = 4
match = set()
dictwords = set()

if len(sys.argv) > 2:
    minlen = int(sys.argv[2])
    if len(sys.argv) > 3:
        dictfile = sys.argv[3]

## This bit does the work
with open(dictfile, 'r') as file:
    for line in file:
        w = line.lower().strip()
        if (len(w) >= minlen and letters[0] in w and "'" not in w):
            dictwords.add(w)

for i in range(minlen, len(letters) + 1): 
    s = dictwords & set(''.join(l) for l in permutations(letters, i))
    match = match | s

## Below here is all just making the output pretty
width = int(os.popen('stty size', 'r').read().split()[1])
count = 0
lastlen = minlen
match = sorted(match, key=lambda x: len(x))
ostr = '%s\n%d Letters:\n' % ('-' * width, lastlen)
for w in match:
    wlen = len(w)
    if wlen != lastlen:
        ostr = ostr[:-1] + '\n(%d)\n%s\n%d Letters:\n' % (count,
                                                          '-' * width,
                                                          wlen)
        lastlen = wlen
        count = 0
    count += 1
    ostr += '%s ' % w
ostr = ostr[:-1] + '\n(%d)\n%s\n%d Words' % (count, '-' * width, len(match))

T = TextWrapper(replace_whitespace=False, width=width)
for line in T.wrap(ostr): print line

    
                    
