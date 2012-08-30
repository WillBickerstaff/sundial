import sys, itertools, textwrap, os
letters, minlen, match = (sys.argv[1].lower(), int(sys.argv[2]), set())
dictwords = set(l.lower().strip() for l in open('/usr/share/dict/british-english') if l.strip() >= minlen and letters[0] in l.lower() and "'" not in l)
for i in range(minlen, len(letters) + 1): match = match | set(dictwords & set(''.join(l) for l in itertools.permutations(letters, i)))
for l in textwrap.wrap(', '.join([x for x in match]), int(os.popen('stty size', 'r').read().split()[1])): print l

