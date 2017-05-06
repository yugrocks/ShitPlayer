__author__ = 'Yugal'
from tkinter import *
from progressBar import ProgressBar
from functools import partial
import pygame

#some dummy data to test
songs=["dummy",
       "2Pac ft. Eminem & Big Syke - Cradle 2 The Grave (with Lyrics) HD 2013   mp3 download.mp3",
       "02 - Maiyya Yashoda (Jamuna Mix).mp3",
       "02 - Tu Hai Ki Nahi.mp3",
       "2pac - Raise Up.mp3",
       "04 - Aafreen - DownloadMing.SE[1].mp3",
       "08 - Wish I Was Your Lover.mp3",
       "rockabye.mp3",
       "monster.mp4",
       "warzone.mp3"
       ]

class MainUi(Tk):
    song_counter=0 #this increases by 20 each time a button is added
    current_list=["dummy"]
    current_playing_index=0
    current_focus_index=0
    paused=False
    def __init__(self,*args, **kwargs):
        Tk.__init__(self,*args, **kwargs)
        pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
        pygame.init()
        pygame.mixer.init()
        self.sWidth=self.winfo_screenwidth()
        self.sHeight=self.winfo_screenheight()
        self.title("Media Player")
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))


        self.frame1=Frame(height=self.percent(self.sHeight,80),width=self.percent(self.sWidth,100))
        self.frame1.pack()
        self.frame1.pack_propagate(0)

        self.frame3=Frame(self.frame1,height=self.percent(self.sHeight,80),width=self.percent(self.sWidth,20))
        self.frame3.pack(side=LEFT)

        self.frame4=Frame(self.frame1,height=self.percent(self.sHeight,80),width=self.percent(self.sWidth,80))
        self.frame4.config(background="white")
        self.frame4.pack(side=RIGHT)
        self.frame4.pack_propagate(0)
        self.frame2=Frame(height=self.percent(self.sHeight,20),width=self.percent(self.sWidth,100))
        self.frame2.config(background="gray53")
        self.frame2.pack(fill=BOTH, expand = YES)
        self.frame2.pack_propagate(0)

        self.pbar=ProgressBar(self.frame2,length=self.percent(self.sWidth,80))
        self.pbar.progress.pack(fill=X, expand = YES)
        self.pbar.place(relx=0.5,rely=0.3,anchor=CENTER)
        self.pbar.progress.bind("<Configure>",self.increm)
        self.pbar.setValue(30)

        self.frame5=Frame(self.frame2,height=self.percent(self.sHeight,5),width=self.percent(self.sWidth,15))
        self.frame5.config(background="gray53")
        self.frame5.place(x=10,y=50)

        self.play=Button(self.frame5,text="Play",width=5)
        self.play.config(background="white")
        self.play.pack(side=LEFT)
        self.pause=Button(self.frame5,text="pause",width=5,command=self.pause)
        self.pause.config(background="white")
        self.pause.pack(side=LEFT)
        self.previous=Button(self.frame5,text="preious",width=5,command=self.playprevious)
        self.previous.config(background="white")
        self.previous.pack(side=LEFT)
        self.stop=Button(self.frame5,text="stop",width=5)
        self.stop.config(background="white")
        self.stop.pack(side=LEFT)
        self.next=Button(self.frame5,text="next",width=5,command=self.playnext)
        self.next.config(background="white")
        self.next.pack(side=LEFT)

    def percent(self,perc,value):
        return value*perc/100

    def increm(self,event):
        self.pbar.progress["length"]=self.percent(self.winfo_width(),80)

    def color_config(self,widget, color, event):
        if not self.isFocused(widget):
            widget.configure(bg=color)

    def isFocused(self,widget):
        return self.current_focus_index==self.current_list.index(widget)

    def setFocus(self,label,event):
        if self.current_focus_index!=0 and self.current_list.index(label)!=self.current_focus_index:
            self.current_list[self.current_focus_index].configure(bg="white")
        label.focus_set()
        self.color_config(label,"yellow",event)
        self.current_focus_index=self.current_list.index(label)

    def setFocusNext(self,event):
        if not self.current_focus_index>=len(self.current_list)-1:
            self.current_focus_index+=1
            self.setFocus(self.current_list[self.current_focus_index],event)

    def setFocusPrev(self,event):
        if not self.current_focus_index<=1:
            self.current_focus_index-=1
            self.setFocus(self.current_list[self.current_focus_index],event)

    def playSong(self,id,event):
        pygame.mixer.music.load(songs[id])
        pygame.mixer.music.play()
        self.current_playing_index=id

    def playnext(self):
        if len(self.current_list)>self.current_playing_index+1:
            self.playSong(self.current_playing_index+1,"")

    def playprevious(self):
        if 1<self.current_playing_index:
            self.playSong(self.current_playing_index-1,"")


        
    def pause(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.pause.configure(text="Play")
        else:
            pygame.mixer.music.unpause()
            self.pause.configure(text="Pause")
        self.paused= not self.paused
        
    def addButton(self):
        ld=Button(self.frame4,height=2,anchor=W,text="song.mp3",width=130,bg="white",relief=GROOVE,state=DISABLED)
        ld.pack(side=LEFT)
        ld.place(y=self.song_counter)
        ld.bind('<Enter>',partial(self.color_config,ld,"SteelBlue2"))
        ld.bind('<Down>',self.setFocusNext)
        ld.bind('<Up>',self.setFocusPrev)
        ld.bind('<Leave>',partial(self.color_config,ld,"white"))
        ld.bind('<Button-1>',partial(self.setFocus,ld))
        self.current_list.append(ld)
        ld.configure(text=songs[self.current_list.index(ld)])
        ld.bind('<Double-Button-1>',partial(self.playSong,self.current_list.index(ld)))
        ld.bind('<Return>',partial(self.playSong,self.current_list.index(ld)))
        self.song_counter+=40



a=MainUi();
for _ in range(len(songs)-1):
    a.addButton()
    
a.mainloop()
