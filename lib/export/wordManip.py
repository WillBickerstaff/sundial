def splitbylength(wordlist):
        initlen = len(wordlist[0])
        lastlen = len(wordlist[-1])
        splitlist = []
        for i in range(initlen, lastlen+1):
            curlist = []
            for x in wordlist:
                if len(x) == i: curlist.append(x.capitalize())
            splitlist.append(sorted(curlist))
        return splitlist
