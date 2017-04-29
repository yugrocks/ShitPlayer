__author__ = 'Yugal'

from tkinter import ttk
from tkinter import *

class ProgressBar():

    def __init__(self, parent,length=300):
        self.progress=ttk.Progressbar(parent, orient="horizontal", length=length, mode="determinate")
        self.progress["value"]=0
        self.progress["maximum"] =self.progress["length"]


    def setValue(self,percent):
        self.progress["value"]=percent*self.progress["length"]/100

    def place(self,relx=0.5,rely=0.5,anchor=CENTER):
        self.progress.place(relx=relx,rely=rely,anchor=anchor)

    def getValue(self):
        return self.progress["value"]

