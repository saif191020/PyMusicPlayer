from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import threading
import time
from mutagen.mp3 import  MP3
from pygame import mixer

#####GLOBAL VARIABLE####
wasPlaying=False
filepath=''
mute =False
currentVolume=60
paused=False
rewinded =False
index =0
songs=[]



#Buttton Functions
def showDetails():
    global filepath
    ext=filepath.split('/')[-1].split('.')[-1]
    print(ext)
    if ext == 'mp3':
        #asa
        audio =MP3(filepath)
        total_length =audio.info.length
    else:
        a=mixer.Sound(filepath)
        total_length =a.get_length()

    min,sec =divmod(total_length,60)
    min     =round(min)
    sec     =round(sec)
    timeformat ='{:02d}:{:02d}'.format(int(min),sec)
    weltag['text']='Playing - '+filepath.split('/')[-1]
    totalen['text']='Total Length: '+timeformat
    thr =threading.Thread(target=showCurLen,args=(total_length,))
    thr.start()

def showCurLen(t):
    Curr_time=0
    global paused,rewinded
    while Curr_time<t and mixer.music.get_busy():
        if paused:
            continue
        else:
            min,sec =divmod(Curr_time,60)
            min     =round(min)
            sec     =round(sec)
            timeformat ='{:02d}:{:02d}'.format(int(min),sec)
            currentlen['text']='Current Time: '+timeformat
            time.sleep(1)
            Curr_time=Curr_time+1
            if rewinded:
                rewinded=False
                Curr_time=0
    print('threadexit')

def clickedPlay():
    global wasPlaying,paused,filepath
    if paused and filepath==songs[int(playlist.curselection()[0])]:

        mixer.music.unpause()
        paused=False
        statusBar['text']= 'Music Playing ... | '+   filepath.split('/')[-1]
        
    else:
        try:
            clickedStop()
            time.sleep(1)
            selsong=playlist.curselection()
            filepath=songs[int(selsong[0])]
            mixer.music.load(filepath)
            mixer.music.play()
            paused=False
            statusBar['text']= 'Music Playing ... | '+   filepath.split('/')[-1]
            showDetails()
            wasPlaying=True
        except :
            tkinter.messagebox.showerror("ERROR","MPlayer Could not Find File.\nPlease Select File First.")
    print('Clicked Play button')

def clickedStop():
    global wasPlaying,paused
    mixer.music.stop()
    wasPlaying=False
    statusBar['text']='Music Stopped .'
    paused=False
    print('Clicked Stop button')

def clickedPause():
    global paused
    mixer.music.pause()
    statusBar['text']='Music Paused . | '+filepath.split('/')[-1]
    paused=True
    print('Clicked Pause button')

def clickedRewind():
    global wasPlaying,rewinded,paused
    if paused:
        clickedStop()
        clickedPlay()
    else:
        try:
            mixer.music.load(filepath)
            mixer.music.play()
            statusBar['text']= 'Music Rewinded | '+   filepath.split('/')[-1]
            paused=False
            rewinded=True
            
            wasPlaying=True

        except :
            tkinter.messagebox.showerror("ERROR","MPlayer Could not Find File.\nPlease Select File First.")

def clickedVolume():
    global mute,currentVolume
    if mute:
        volumebtn.config(image=volumeimage)
        mixer.music.set_volume(currentVolume/100)
        volumeSlider.set(currentVolume)
        mute=False
    else :
        volumebtn.config(image =muteimage)
        currentVolume=volumeSlider.get()
        mixer.music.set_volume(0)
        volumeSlider.set(0)
        mute=True

def setVol(val):
    mixer.music.set_volume(int(val)/100) #volume is 0 ~ 1

def about_us():
    tkinter.messagebox.showinfo("MPlayer",' Version : 1.0\n MPlayer was created by Saif Basheer Ahamed')

def openFile():
    global filepath,wasPlaying
    filepath =tkinter.filedialog.askopenfilename()
    print(filepath)
    addToPlaylist(filepath)
    wasPlaying=False

def addToPlaylist(fp):
    fn =fp.split('/')[-1]
    global index
    if(fn!=''):
        playlist.insert(index,fn)
        songs.insert(index,fp)
        index+=1

def onClosing():
    mixer.music.stop()
    root.destroy()

#Window Defenition 
root =Tk()
mixer.init() #mixer Initalization
root.geometry('450x300')
root.title('MPlayer')
root.iconbitmap(r'Images/mplayer.ico')




#############MENU STUFF##################
menubar =Menu(root)
root.config(menu=menubar)
FileMenu =Menu(menubar,tearoff=0)
HelpMenu =Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=FileMenu)
menubar.add_cascade(label='Help',menu=HelpMenu)
FileMenu.add_command(label='Open',command=openFile)
FileMenu.add_command(label='Exit',command=onClosing)
HelpMenu.add_command(label='About Us',command =about_us)


#Frame
lFrame =Frame(root)
rFrame =Frame(root)
timerFrame =Frame(rFrame)
controlsFrame =Frame(rFrame)
volumeFrame =Frame(rFrame)



#Widgets
weltag      =Label(root, text="Welcome to the Music Player!!")
totalen     =Label(timerFrame, text='Total Length: --:--')
currentlen  =Label(timerFrame, text='Current Time: --:--')
statusBar   =Label(root,text='Welcome to MPlayer',bd=1, relief=SUNKEN, anchor =W)
playimage   =PhotoImage(file='Images/play.png')
pauseimage  =PhotoImage(file="Images/pause.png")
stopimage   =PhotoImage(file='Images/stop.png')
rewindimage =PhotoImage(file='Images/rewind.png')
muteimage   =PhotoImage(file='Images/mute.png')
volumeimage =PhotoImage(file='Images/volume.png')
playbtn     =Button(controlsFrame,image=playimage, command=clickedPlay)
stopbtn     =Button(controlsFrame,image=stopimage, command=clickedStop)
pausebtn    =Button(controlsFrame,image=pauseimage, command=clickedPause)
rewindbtn   =Button(volumeFrame,image=rewindimage, command=clickedRewind)
volumebtn   =Button(volumeFrame,image=volumeimage, command=clickedVolume)
loadbtn     =Button(lFrame,text='Load Music', command=openFile)
deletebtn   =Button(lFrame,text='Delete Music')
playlist    =Listbox(lFrame)
volumeSlider=Scale(volumeFrame,from_=0,to=100,orient=HORIZONTAL,command=setVol)


volumeSlider.set(60)
mixer.music.set_volume(60/100)



#Packing/Placing/Griding
#weltag.pack(side=TOP)
statusBar.pack(side=BOTTOM,fill=X)
lFrame.pack(side=LEFT,padx=10)
rFrame.pack(side=RIGHT)
timerFrame.pack()
controlsFrame.pack(padx=10,pady=35)
volumeFrame.pack(side=BOTTOM,pady=10)
totalen.pack(side=TOP)
currentlen.pack(side=TOP)
playbtn.grid(row=0,column=0,padx=3)
pausebtn.grid(row=0,column=1,padx=3)
stopbtn.grid(row=0,column=2,padx=3)
rewindbtn.grid(row=0,column=0)
volumebtn.grid(row=0,column=1)
volumeSlider.grid(row=0,column=2)
playlist.pack(pady=5,padx=17)
loadbtn.pack(side=LEFT,pady=2,padx=2)
deletebtn.pack(side=LEFT,pady=2,padx=2)


root.protocol("WM_DELETE_WINDOW",onClosing)
root.mainloop()