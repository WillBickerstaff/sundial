'''
Created on 1 Sep 2012

@author: will
'''
from Tkinter import (Label, Frame, Scrollbar, Entry, N, S, E, W, DISABLED,
                     VERTICAL, Button, LEFT, ACTIVE, FLAT)
import tkFont
from tkSimpleDialog import Dialog

license_text = '''
The MIT License (MIT)
=====================

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


class AboutDialog(Dialog):

    def body(self, master):
        self.hdgFont = tkFont.Font(family="Helvetica", size=14, weight='bold')
        self.monoFont = tkFont.Font(family='Monospace', size=10)
        Label(master, text="Sundial Solver", font=self.hdgFont).grid(row=0,
                                                            sticky=E + W)
        Label(master, text="V 0.1.0").grid(row=1, sticky=E + W)
        Label(master, text=u"\u00A9 2012 Will Bickerstaff").grid(row=2,
                                                                 sticky=E + W)
        Label(master, text="<will.bickerstaff@gmail.com>").grid(row=3,
                                                                sticky=E + W)
        lictxt = Label(master, text=license_text, anchor=W)
        lictxt.grid(row=4, column=0, sticky=N + S + E + W)

    def buttonbox(self):
        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)

        box.pack()
