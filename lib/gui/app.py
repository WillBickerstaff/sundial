import sys
import tkFileDialog
import tkMessageBox
from Tkinter import (Frame, Spinbox, Entry, Label, Button, E, W, END, SUNKEN,
                     Menu)
from os.path import expanduser
from lib.gui.results import ResultPane
from lib.gui.about import AboutDialog
from lib.wordmatch import Match
from lib.export.odt import Doc
from tkFileDialog import asksaveasfilename


class Application(Frame):
    MAXWORDLEN = 20
    DEFAULTWORDLEN = 4

    def __init__(self, master=None):
        Frame.__init__(self, master, padx=3, pady=3)
        self.dictionaryfile = None
        self.menubar = Menu()
        self.__createWidgets()
        self.menubar.add_cascade(label='File', menu=self.__File)
        self.menubar.add_cascade(label='Options', menu=self.__Options)
        self.menubar.add_command(label='About', command=self.__about)
        self.__params.grid(row=0, column=0, sticky=W)
        self.__res_pane = Frame()
        self.__res_pane.grid(row=2, column=0, sticky=E + W)
        self.__status = Label(anchor=W, relief=SUNKEN)
        self.__status.grid(row=3, column=0, sticky=E + W)
        self.osDictFile()
        self.matchobj = None
        if self.dictionaryfile is None:
            self.status('No dictionary defined!')
        master.config(menu=self.menubar)

    def __createWidgets(self):
        self.__params = Frame(padx=5, pady=5)
        Label(text='Letters: ', anchor=E).grid(row=0, column=0,
                                               sticky=E, in_=self.__params)
        self.__char_entry = Entry(width=10)
        Label(text='First letter appears in every result ', anchor=W).grid(
            row=0, column=3, sticky=E, in_=self.__params)
        self.__char_entry.grid(row=0, column=1, columnspan=2,
                               sticky=W, in_=self.__params)
        Label(text='Minimum length of result words: ', anchor=E).grid(
            row=1, column=0, sticky=E, in_=self.__params)
        self.__word_length_ctrl = Spinbox(from_=1, to=Application.MAXWORDLEN,
                                          width=2)
        self.__word_length_ctrl.delete(0, END)
        self.__word_length_ctrl.insert(0, Application. DEFAULTWORDLEN)
        self.__word_length_ctrl.grid(row=1, column=1, in_=self.__params,
                                     sticky=W)
        self.__go_button = Button(text='Go', command=self.__findWords)
        self.__go_button.grid(row=1, column=2, sticky=E, in_=self.__params)
        self.__Options = Menu()
        self.__Options.add_command(label='Choose dictionary',
                                           command=self.__choosedict)
        self.__File = Menu()
        self.__File.add_command(label='Export as ODT (Open document text)', command=self.__export)

    def __choosedict(self):
        try:
            self.dictionaryfile = tkFileDialog.askopenfile(mode='r').name
            self.status('')
        except AttributeError:
            pass

    def osDictFile(self):
        if 'linux' in sys.platform:
            self.dictionaryfile = '/usr/share/dict/words'

    def __about(self):
        AboutDialog(self)

    def status(self, text):
        self.__status.config(text=text)
        self.__status.update_idletasks()

    def __findWords(self):
        self.__res_pane.grid_forget()
        chars = self.__char_entry.get()
        minlen = int(self.__word_length_ctrl.get())
        if len(chars) < minlen:
            tkMessageBox.showerror(title='Not enough letters',
                        message='''Not enough letters given\n
You must give at least as many letters as the minimum required word length''')
            return
        res = self.__getres(minlen, chars)
        self.__res_pane = ResultPane(res)
        self.__res_pane.grid(row=2, column=0, sticky=E + W)

    def __getres(self, minlen, chars):
        firstpass = True
        while True:
            try:
                self.matchobj = None
                if firstpass and self.dictionaryfile is None:
                    self.matchobj = Match(minlen=minlen, chars=chars,
                                      statushandler=self.status)
                    firstpass = False
                else:
                    self.matchobj = Match(minlen=minlen, chars=chars,
                                     dict=self.dictionaryfile,
                                     statushandler=self.status)
                res = self.matchobj.wordMatch()
                return res
            except IOError:
                ans = tkMessageBox.askyesno(title='No Dictionary',
                      message='''No dictionary file was found, would
 you like to choose a dictionary file? (No) aborts the application''')
                if ans:
                    self.__choosedict()
                else:
                    sys.exit()

    def __export(self):
        f = tkFileDialog.asksaveasfilename(defaultextension='.odt', 
                                           initialdir=expanduser('~'),
                                           initialfile=self.__char_entry.get())
        if not f: return
        outfile = Doc(self.matchobj)
        outfile.write(f)
        print f