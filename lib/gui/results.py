'''
Created on 27 Aug 2012

@author: will
'''
from Tkinter import (Frame, Listbox, Scrollbar, Button, Label, N, S, E, W,
                     VERTICAL, HORIZONTAL, SINGLE, END)


class ResultPane(Frame):

    def __init__(self, resultlist, master=None):
        Frame.__init__(self, master, padx=3, pady=5)
        self.resultlist = resultlist
        self.__splitlist()
        self.__createWidgets()

    def __splitlist(self):
        minwordlen = len(min(self.resultlist, key=lambda x: len(x)))
        maxwordlen = len(max(self.resultlist, key=lambda x: len(x)))
        self.wordsbylength = [[] for x in range((maxwordlen - minwordlen) + 1)]
        for word in self.resultlist:
            listidx = len(word) - minwordlen
            self.wordsbylength[listidx].append(word)
        for i, rlist in enumerate(self.wordsbylength):
            self.wordsbylength[i] = sorted(rlist)

    def __createWidgets(self):
        col = 0
        for rlist in self.wordsbylength:
            if len(rlist) > 0:
                wordlen = len(rlist[0])
                lbl = Label(text='(%d)' % len(rlist))
                res = ResultList()
                res.fill(rlist)
                res.lbl.config(text='%d Letters' % wordlen)
                res.grid(row=0, column=col, in_=self)
                res.width(wordlen)
                lbl.grid(row=1, column=col, in_=self)
                col += 1
        Label(text='%d Words' % len(self.resultlist)).grid(row=2, column=0,
                                                           columnspan=col + 1,
                                                           in_=self)


class ResultList(Frame):
    '''
    Result List widget
    '''

    def __init__(self, master=None):
        Frame.__init__(self, master, padx=3, pady=3)
        self.columnconfigure(0, weight=1, minsize=50)
        self.columnconfigure(1, weight=1000)
        self.columnconfigure(2, weight=1, minsize=10)
        self.__createWidgets()
        self.show()

    def __createWidgets(self):
        self.lbl = Label(text='')
        self.lbl.grid(row=1, column=0, in_=self)
        self.__hide_button = Button(text='Hide', command=self.hide)
        self.__hide_button.grid(row=0, column=0, in_=self)
        self.__xScroll = Scrollbar(orient=HORIZONTAL)
        self.__yScroll = Scrollbar(orient=VERTICAL)
        self.list = Listbox(xscrollcommand=self.__xScroll.set,
                            yscrollcommand=self.__yScroll.set,
                            selectmode=SINGLE)
        self.__xScroll.config(command=self.list.xview)
        self.__yScroll.config(command=self.list.yview)

    def show(self):
        self.__hide_button.config(text='Hide', command=self.hide)
        self.list.grid(row=2, column=0, columnspan=2,
                        sticky=N + S + E + W, in_=self)
        self.__xScroll.grid(row=3, column=0, columnspan=2,
                            sticky=N + E + W, in_=self)
        self.__yScroll.grid(row=2, column=2, sticky=W + N + S, in_=self)

    def hide(self):
        self.__hide_button.config(text='Show', command=self.show)
        self.list.grid_forget()
        self.__xScroll.grid_forget()
        self.__yScroll.grid_forget()

    def clear(self):
        self.list.delete(0, END)

    def fill(self, valList):
        self.clear()
        for v in valList:
            self.list.insert(END, v)
        self.list.see(0)
        self.select(0)

    def append(self, val):
        self.list.insert(END, val)
        self.list.see(END)

    def select(self, index=0):
        self.list.selection_set(index)

    def selected(self):
        return int(self.list.curselection()[0])

    def width(self, width):
        self.list.config(width=width)
