import sys
import tkFileDialog
import tkMessageBox
from Tkinter import (Frame, Spinbox, Entry, Label, Button, E, W, END, SUNKEN)
from lib.gui.results import ResultPane
from lib.wordmatch import Match


class Application(Frame):
    MAXWORDLEN = 20
    DEFAULTWORDLEN = 4

    def __init__(self, master=None):
        Frame.__init__(self, master, padx=3, pady=3)
        self.params = self.__createWidgets()
        self.params.grid(row=0, column=0, sticky=W)
        self.__res_pane = Frame()
        self.__res_pane.grid(row=1, column=0, sticky=E + W)
        self.__status = Label(anchor=W, relief=SUNKEN)
        self.__status.grid(row=2, column=0, sticky=E + W)

    def __createWidgets(self):
        params = Frame(padx=5, pady=5)
        Label(text='Letters: ', anchor=E).grid(row=0, column=0,
                                               sticky=E, in_=params)
        self.__char_entry = Entry(width=10)
        self.__char_entry.grid(row=0, column=2, columnspan=2,
                               sticky=W, in_=params)
        Label(text='Minimum length word: ', anchor=E).grid(row=1, column=0,
                                                           sticky=E,
                                                           in_=params)
        self.__word_length_ctrl = Spinbox(from_=1, to=Application.MAXWORDLEN,
                                          width=2)
        self.__word_length_ctrl.delete(0, END)
        self.__word_length_ctrl.insert(0, Application. DEFAULTWORDLEN)
        self.__word_length_ctrl.grid(row=1, column=2, in_=params, sticky=E)
        self.__go_button = Button(text='Go', command=self.__findWords)
        self.__go_button.grid(row=1, column=3, sticky=E, in_=params)
        return params

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
        self.__res_pane.grid(row=1, column=0, sticky=E + W)

    def __getres(self, minlen, chars):
        firstpass = True
        dfile = ''
        while True:
            try:
                matchobj = None
                if firstpass:
                    matchobj = Match(minlen=minlen, chars=chars,
                                      statushandler=self.status)
                    firstpass = False
                else:
                    matchobj = Match(minlen=minlen, chars=chars, dict=dfile,
                                     statushandler=self.status)
                res = matchobj.wordMatch()
                return res
            except IOError:
                ans = tkMessageBox.askyesno(title='No Dictionary',
                      message='''No dictionary file was found, would
 you like to choose a dictionary file? (No) aborts the application''')
                if ans:
                    dfile = tkFileDialog.askopenfile(mode='r').name
                else:
                    sys.exit()
