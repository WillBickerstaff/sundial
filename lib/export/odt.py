from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties, FontFace
from odf.text import H, P, Span

class doc(object):
    
    def __init__(self, letters, words, wordCount, solvedTime, filename):
        self.__doc = OpenDocumentText()
        self.__createStyles()
        self.__createHeading(letters, solvedTime, wordCount)
        self.__createContent(words)
        self.__doc.save(filename, 'odt')

        
    def __createHeading(self, letters, solvedTime, totalWords):
        HdgTxt = '{0:d} words, Solved \'{1:s}\' in {2:.3f} seconds'.format(
            totalWords, letters.upper(), solvedTime)
        self.__doc.text.addElement(H(outlinelevel = 1, text=HdgTxt))
 
    def __wordHeading(self, wordlist):
        return '{0:d} - {1:d} Letter words'.format(len(wordlist), len(wordlist[0]))
    
    def __createContent(self, words):
        for wordlist in words:
            self.__doc.text.addElement(H(outlinelevel = 2, 
                                         txt=self.__wordHeading(wordlist)))
            self.__doc.text.addElement(P(text=', '.join(word for word in wordlist)))
    
    
    def __createStyles(self):
        self.__addFonts
        s = self.__doc.styles
        self.__setDefaultStyle(s)
        self.__setHeadingStyle(s)
        
    def __setHeadingStyle(self):
        HdgStyle = Style(name="Heading", family='paragraph', parentstylename="Standard")
        HdgStyle.addAttribute('class', 'text')
        HdgStyle.addAttribute(TextProperties(
            fontweight="bold",
            fontweightasian="bold",
            fontweightcomplex="bold"))
        self.__doc.styles.addElement(HdgStyle)
        
        ''' Heading 1 '''
        HdgStyle = Style(name="Heading_20_1", family='paragraph', parentstylename="Heading")
        HdgStyle.addAttribute('class', 'text')
        HdgStyle.addAttribute('displayname', 'Heading 1')
        HdgStyle.addElement(TextProperties(fontsize='120%'))
        self.__doc.styles.addElement(HdgStyle)
        
        ''' Heading 2 '''
        HdgStyle = Style(name='Heading_20_2', family='paragraph', parentstylename='Heading')
        HdgStyle.addAttribute('class', 'text')
        HdgStyle.addAttribute('displayname', 'Heading 2')
        HdgStyle.addElement(TextProperties(fontsize='110%', color='#808080'))
        self.__doc.styles.addElement(HdgStyle)
        
    def __setDefaultStyle(self):
        DefaultStyle = Style(name="Standard", family='paragraph')
        DefaultStyle.addAttribute('class','text')
        DefaultStyle.addAttribute('font-name', 'FreeSans')
        DefaultStyle.addElement(TextProperties(
            fontfamily='FreeSans', 
            fontsize='12pt'))
        DefaultStyle.addElement(ParagraphProperties(
            margintop='0.423cm',
            marginbottom='0.212cm'))
        self.__doc.styles.addElement(DefaultStyle)
        
        ''' Text Body '''
        txtBody = Style(name='text_20_body', family='paragraph', parentstylename='Standard')
        txtBody.addAttribute('class', 'text')
        txtBody.addAttribude('displayname', 'Text Body')
        self.__doc.styles.addElement(txtBody)
        
    def __addFonts(self):
        self.__doc.fontfacedecls.addElement((FontFace(
                name="FreeSans",fontfamily="FreeSans", 
                fontfamilygeneric="swiss",fontpitch="variable")))
        self.__doc.fontfacedecls.addElement((FontFace(
                name="Nimbus Mono", fontfamily="&apos;Nimbus Mono L&apos", 
                fontfamilygeneric="modern", fontpitch="fixed")))
