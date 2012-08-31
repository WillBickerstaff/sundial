import sys, itertools, textwrap, os
ltrs, minlen, wd = (sys.argv[1].lower(), int(sys.argv[2]), set())
dictwords = set(l.lower().strip() for l in open('/usr/share/dict/words') if l.strip() >= minlen and ltrs[0] in l.lower() and "'" not in l)
for i in range(minlen, len(ltrs) + 1): wd = wd | set(dictwords & set(''.join(l) for l in itertools.permutations(ltrs, i)))
for l in textwrap.wrap(' '.join([x for x in sorted(wd, key=lambda x: len(x))]), int(os.popen('stty size', 'r').read().split()[1])): print l
