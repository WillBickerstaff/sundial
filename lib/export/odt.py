from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties, FontFace
from odf.text import H, P, Span

class Doc(object):
    
    def __init__(self, matchobj):
        self.__doc = OpenDocumentText()
        self.__createStyles()
        self.__createHeading(matchobj)
        self.__createContent(matchobj)
        
    def __createHeading(self, matchobj):
        HdgTxt = '{0:d} words, Solved \'{1:s}\' in {2:.3f} seconds'.format(
            len(matchobj.match), matchobj.chars.upper(), matchobj.completeTime)
        self.__doc.text.addElement(H(outlinelevel = 1, text=HdgTxt))
        txt=P(text='Check the results, some may be acronyms, names or slang terms.')
        self.__doc.text.addElement(txt)
 
    def __wordHeading(self, wordlist):
        return '{0:d} - {1:d} Letter words'.format(len(wordlist), len(wordlist[0]))
    
    def __createContent(self, words):
        splitList = self.__splitbylength(words.match)
        for wordlist in splitList:
            self.__doc.text.addElement(H(outlinelevel = 2, 
                                         text=self.__wordHeading(wordlist)))
            self.__doc.text.addElement(P(text=', '.join(word for word in wordlist)))
            
        self.__doc.text.addElement(P(text='\n\nhttps://github.com/WillBickerstaff/sundial'))
    
    def __splitbylength(self, wordlist):
        initlen = len(wordlist[0])
        lastlen = len(wordlist[-1])
        splitlist = []
        for i in range(initlen, lastlen+1):
            curlist = []
            for x in wordlist:
                if len(x) == i: curlist.append(x)
            splitlist.append(curlist)
        return splitlist        
    
    def __createStyles(self):
        self.__addFonts
        self.__setDefaultStyle()
        self.__setHeadingStyle()
        
    def __setHeadingStyle(self):
        HdgStyle = Style(name="Heading", family='paragraph', parentstylename="Standard")
        HdgStyle.addElement(TextProperties(
                            fontweight='bold',
                            fontfamily='FreeSans',
                            fontsize='120%'))
        self.__doc.styles.addElement(HdgStyle)
        
        ''' Heading 1 '''
        HdgStyle = Style(name="Heading_20_1", family='paragraph', parentstylename="Heading")
        HdgStyle.addElement(TextProperties(fontsize='120%'))
        self.__doc.styles.addElement(HdgStyle)
        
        ''' Heading 2 '''
        HdgStyle = Style(name='Heading_20_2', family='paragraph', parentstylename='Heading')
        HdgStyle.addElement(TextProperties(fontsize='110%', color='#808080'))
        self.__doc.styles.addElement(HdgStyle)        
        
    def __setDefaultStyle(self):
        DefaultStyle = Style(name="Standard", family='paragraph')
        DefaultStyle.addElement(TextProperties(
            fontfamily='FreeSans', 
            fontsize='10pt'))
        DefaultStyle.addElement(ParagraphProperties(
            margintop='0.423cm',
            marginbottom='0.212cm'))
        self.__doc.styles.addElement(DefaultStyle)
        
        ''' Text Body '''
        txt = Style(name='text_20_body', family='paragraph', parentstylename='Standard')
        self.__doc.styles.addElement(txt)
        
    def __addFonts(self):
        self.__doc.fontfacedecls.addElement((FontFace(
                name="FreeSans",fontfamily="FreeSans", 
                fontfamilygeneric="swiss",fontpitch="variable")))
        self.__doc.fontfacedecls.addElement((FontFace(
                name="Nimbus Mono", fontfamily="&apos;Nimbus Mono L&apos", 
                fontfamilygeneric="modern", fontpitch="fixed")))
        
    def write(self, filename):
        self.__doc.save(filename)
