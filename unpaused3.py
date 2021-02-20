from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from os import *
import random
from PIL import Image,ImageTk
import cv2
from bs4 import BeautifulSoup
import requests
import re
import sqlite3
from pygame import*
player=Tk()
a1=player.winfo_screenwidth()/7
a2=player.winfo_screenheight()/10
player.geometry("+{}+{}".format(int(a1),int(a2)))
player.resizable(width=False,height=False)
player.title("UnPaused")
player.iconbitmap("icon.ico")
player.grid_columnconfigure(ALL,weight=1)
player.grid_rowconfigure(ALL,weight=1)
player["bg"]="#4d004d"
n=0
# Video display:
global videoframe
c1=Frame(player,bg="#1a001a",width=500,highlightbackground="#330033",highlightthickness=10,relief=GROOVE)
c1.grid(row=3,column=2,rowspan=2,sticky=N+S+E+W,padx=10,pady=10)
c1.grid_propagate(FALSE)
videoframe=Label(c1,bg='#1a001a')
videoframe.grid()

# lyrics database:
conn = sqlite3.connect('lyrics.db')
conn.execute('''CREATE TABLE IF NOT EXISTS lyrics
               (song TEXT ,
                lyrics TEXT);''')
c=conn.cursor()

# playlists datatbase:
conn1 = sqlite3.connect('playlists.db')
conn1.execute('''CREATE TABLE IF NOT EXISTS playlists
               (playlist TEXT ,
                songs TEXT);''')
c1=conn1.cursor()

# songs datatbase:
conn2 = sqlite3.connect('songs.db')
conn2.execute('''CREATE TABLE IF NOT EXISTS songs
               (songs TEXT,
               songpath TEXT);''')
c2=conn2.cursor()

# FUNCTIONS:
global playbool
playbool=False
def shuffun():
    global video_stream
    mixer.music.unload()
    global sel
    global sel1
    global n
    if n%2!=0:
        stopbut['state']=DISABLED
    try:
        if queuedisp.size()!=0:
            raise NameError
    except NameError:
        messagebox.showwarning("Queue Filled","clear the queue")
    else:
        a=random.sample(range(songdisp.size()),songdisp.size())
        for j in a:
            queuedisp.insert(END,songdisp.get(j))
        canvas.itemconfig(crntsong,text=queuedisp.get(0))
        try:
            songdisp.itemconfig(sel,{"fg":"red"})
            try:
                queuedisp.itemconfig(sel1,{"fg":"red"})
            except:
                pass
        except:
            pass
        queuedisp.selection_set(0)
        def cursel1():
            #global var2
            global sel5
            #var2=1
            try:
                sel5=queuedisp.get(queuedisp.curselection())
            except:
                sel5=songdisp.get(songdisp.curselection())
            if sel5==queuedisp.get(sel1):
                global var2
                var2=0
            else:
                var2=1
        queuedisp.bind("<<ListboxSelect>>",lambda x:cursel1())
        global sel5
        sel5=queuedisp.get(queuedisp.curselection()[0])
        global i
        try:
            if n%2!=0:
                n=0
            playbut['image']=play
            global move
            i=1
            move()
        except:
            pass
    n=0
    def video_stream():
        return
def stopfun():
    mixer.music.stop()
    global video_stream
    global sel
    global sel1
    global n
    try:
        queuedisp.itemconfig(sel1,{"fg":"red"})
    except:
        songdisp.itemconfig(sel,{"fg":"red"})
    n=0
    def video_stream():
        return
    global i
    i=1
    playbut['image']=play
    playbut['command']=playfun  
    move()
    stopbut['state']=DISABLED
def nextf():
    global sel5
    try:
        sel5=songdisp.get(songdisp.curselection()[0]+1)
    except:
        sel5=queuedisp.get(queuedisp.curselection()[0]+1)
    mixer.music.unload()
    global n
    global video_stream
    if n!=0:
        mixer.music.pause()
        curframe=video.get(cv2.CAP_PROP_POS_FRAMES)
        sel3=canvas.itemcget(crntsong,'text')
        def video_stream():
            return
    if n%2!=0:
        stopbut['state']=DISABLED
    try:
        global sel
        global sel1
        sel2=songdisp.curselection()
        if len(sel2)>1:
            raise NameError
        canvas.itemconfigure(crntsong, text=songdisp.get(sel2[0]+1))
        songdisp.selection_clear(0,END)
        songdisp.selection_set(sel2[0]+1)
        playbut['image']=play
        try:
            queuedisp.itemconfig(sel1,{"fg":"red"})
        except:
            pass
        global i
        if n%2!=0:
            n=0
        i=1
        try:
            move()
        except:
            pass
    except NameError:
        messagebox.showwarning("Multiple selections","Select only one song")
    except:
        try:
            sel1=queuedisp.curselection()
            canvas.itemconfigure(crntsong, text=queuedisp.get(sel1[0]+1))
            queuedisp.selection_clear(0,END)
            queuedisp.selection_set(sel1[0]+1)
            playbut['image']=play
            canvas.coords(crntsong,20,5) 
            try:
                songdisp.itemconfig(sel,{"fg":"red"})
            except:
                pass
            if n%2!=0:
                n=0
            i=1
            try:
                move()
            except:
                pass
        except:
            messagebox.showwarning("No selection","Select a song")
        else:
            queuedisp.itemconfig(sel1,{"fg":"red"})
    else:
        try:
            songdisp.itemconfig(sel,{"fg":"red"})
        except:
            pass
def prev():
    global sel5
    try:
        sel5=songdisp.get(songdisp.curselection()[0]-1)
    except:
        sel5=queuedisp.get(queuedisp.curselection()[0]-1)
    mixer.music.unload()
    global n
    global video_stream
    if n!=0:
        mixer.music.pause()
        curframe=video.get(cv2.CAP_PROP_POS_FRAMES)
        sel3=canvas.itemcget(crntsong,'text')
        def video_stream():
            return
    if n%2!=0:
        stopbut['state']=DISABLED
    try:
        global sel
        global sel1
        sel2=songdisp.curselection()
        if len(sel2)>1:
            raise NameError
        canvas.itemconfigure(crntsong, text=songdisp.get(sel2[0]-1))
        songdisp.selection_clear(0,END)
        songdisp.selection_set(sel2[0]-1)
        playbut['image']=play
        try:
            queuedisp.itemconfig(sel1,{"fg":"red"})
        except:
            pass
        global i
        if n%2!=0:
            n=0
        i=1
        try:
            move()
        except:
            pass
    except NameError:
        messagebox.showwarning("Multiple selections","Select only one song")
    except:
        try:
            sel1=queuedisp.curselection()
            canvas.itemconfigure(crntsong, text=queuedisp.get(sel1[0]-1))
            queuedisp.selection_clear(0,END)
            queuedisp.selection_set(sel1[0]-1)
            playbut['image']=play
            canvas.coords(crntsong,20,5) 
            try:
                songdisp.itemconfig(sel,{"fg":"red"})
            except:
                pass
            if n%2!=0:
                n=0
            i=1
            try:
                move()
            except:
                pass
        except Exception:
            messagebox.showwarning("No selection","Select a song")
        else:
            queuedisp.itemconfig(sel1,{"fg":"red"})
    else:
        try:
            songdisp.itemconfig(sel,{"fg":"red"})
        except:
            pass
global txt
def deletequeue():
    global playbool
    sel=queuedisp.curselection()
    for i in sel:
        queuedisp.delete(i)
    if queuedisp.size()==0:
        playbool=False
        curplaylist['text']=""
def clearqueue():
    try:
        mixer.music.unload()
    except:
        pass
    global sel5
    global n
    global i
    global video_stream
    global move
    try:
        del sel5
    except:
        pass
    n=0
    i=1
    def video_stream():
        return
    try:
        move()
    except:
        pass
    global playbool
    playbool=False
    curplaylist['text']=""
    queuedisp.delete(0,END)
    playbut['image']=play
def add():
    global playbool
    if playbool==True:
        messagebox.showwarning("Playlist in queue","Remove the playlist from queue",parent=player)
    else:
        for i in songdisp.curselection():
            if songdisp.get(i) not in queuedisp.get(0,END):
                queuedisp.insert(END,songdisp.get(i))

# Scroll bar for songdisp:
scrolly=Scrollbar(orient=VERTICAL)
#scrolly.grid(sticky=N+S+W,row=4,column=0,padx=5)
scrollx=Scrollbar(player,orient=HORIZONTAL)
scrollx.grid(sticky=E+W,row=5,column=1,padx=10,pady=5)

# Song display:
# Song label:
Label(text="All\nSongs",fg="white",bg="#4d004d",font=("'Eras Bold ITC'",10,'underline italic bold')).grid(row=3,column=1,padx=10)

# List Box:
global songdisp
songdisp=Listbox(bg="#1a001a",yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,height=20,width=30,selectmode=EXTENDED,fg="red",highlightbackground="#330033",highlightthickness=10,relief=GROOVE,highlightcolor="#330033")
songdisp.grid(row=4,column=1,sticky=N+S+E+W,padx=10)
for i in c2.execute("SELECT * FROM songs"):
    if path.exists(i[1]):
        songdisp.insert(END,list(i)[0])
    else:
        continue

def choosesongs():
    global song
    global finalsongs
    song=filedialog.askopenfilenames(initialdir=r"d:/",title="Choose songs that you want to add to the player",filetypes=(("Audio files","*.mp3"),))
    finalsongs=[]
    for i in song:
        i=i.split("/")
        i[len(i)-1]=i[len(i)-1].replace(".mp3","")
        finalsongs.append(i[len(i)-1])
    for i in finalsongs:
        for k in songdisp.get(0,END):
            if i==k:
                break
        else:
            songdisp.insert(END,str(i))   
        for j in c2.execute("SELECT * FROM songs"):
            if i==list(j)[0]:
                break
        else:
            c2.execute('INSERT INTO songs VALUES(?,?)',
                       (i,song[finalsongs.index(i)]))
            conn2.commit()
def lyrics():
    global l1
    global addmanually
    try:
        try:
            sel4=songdisp.curselection() 
            if len(sel4)==0:
                raise Exception
        except:
            sel4=queuedisp.curselection()
        if len(sel4)>1:
            raise NameError
        if len(sel4)==0:
            raise TypeError
    except NameError:
        messagebox.showwarning("Multiple selections","Select only one song")
    except TypeError:
        messagebox.showwarning("No selection","Select a song")
    else:
        def addmanually():
            def save1():
                try:
                    c.execute("INSERT INTO lyrics(song,lyrics) VALUES (?,?)",
                              (songdisp.get(sel4),str(lyricstxt.get(1.0,END))))
                except:
                    c.execute("INSERT INTO lyrics(song,lyrics) VALUES (?,?)",
                    (queuedisp.get(sel4),str(lyricstxt.get(1.0,END))))
                conn.commit()
                lyrics.destroy()
            scroll.pack(side=RIGHT, padx=10, pady=10, fill=Y)
            lyricstxt.insert(END,"Enter lyrics here",'center')
            lyricstxt.pack()
            save1=Button(lyrics,text="Save",command=save1,fg="white",bg="#4d004d",font=("Agency FB",15,'bold','underline'),activebackground="#4d004d",activeforeground="red")
            save1.pack(pady=5)
            songname.destroy()
            save.destroy()
            l1.destroy()
            addmanually.destroy()
        def delete():
            try:
                sel4=songdisp.curselection() 
                if len(sel4)==0:
                    raise Exception
                c.execute("DELETE from lyrics WHERE song=(?)",
                          (songdisp.get(sel4),)) 
            except:
                sel4=queuedisp.curselection()
                c.execute("DELETE from lyrics WHERE song=(?)",
                          (queuedisp.get(sel4),))
            songdisp["state"]=NORMAL
            queuedisp["state"]=NORMAL
            conn.commit()
            lyrics.destroy()
        def save():
            try:
                songnameget = songname.get()
                songnameget = songnameget.lower()
                songnameget = songnameget.split()
                songnameget = '-'.join((songnameget))
                lyrics1 = requests.get('https://www.ilyricshub.com/'+songnameget).text
                soup = BeautifulSoup(lyrics1, 'lxml')
                final = soup.find('div', class_="song_lyrics")
                if final == None:
                    raise Exception
                heading = soup.find('h1', class_="post-title entry-title").text
                final = re.split('<br/>|<p>|</p>| |<div|class="song_lyrics">|</div>', str(final))
                count = 1
                final1 = heading+"\n\n"
                for i in final:
                    if i != "":
                        count += 1
                        final1 += i
                        final1 += ' '
                    if count == 5:
                        final1 += '\n'
                        count = 1
                try:
                    c.execute("INSERT INTO lyrics(song,lyrics) VALUES (?,?)",
                              (songdisp.get(sel4),str(final1)))
                except:
                    c.execute("INSERT INTO lyrics(song,lyrics) VALUES (?,?)",
                              (queuedisp.get(sel4),str(final1)))
                conn.commit()
                scroll.pack(side=RIGHT, padx=10, pady=10, fill=Y)
                lyricstxt.insert(END, final1, 'center')
                lyricstxt['state'] = DISABLED
                lyricstxt.pack(pady=10)
                songname.destroy()
                save.destroy()
                l1.destroy()
                addmanually.destroy()
            except:
                songname.delete(0,END)
                messagebox.showwarning("Sorry","No results found! You can add lyrics manually",parent=lyrics)
        global lyricswin
        global lyrics
        try:
            if lyricswin==1:
                lyrics.withdraw()
        except:
            pass
        lyrics=Toplevel()
        lyricswin=1
        lyrics.resizable(width=False,height=False)
        scroll = Scrollbar(lyrics, orient=VERTICAL)
        lyricstxt = Text(lyrics, font="Times 15", fg="red", bg="#330033", yscrollcommand=scroll.set)
        scroll.config(command=lyricstxt.yview)
        lyricstxt.tag_configure("center", justify='center')
        lyricstxt.tag_add("center", 1.0, END)
        try:
            sel4=songdisp.curselection() 
            if len(sel4)==0:
                raise Exception
            lyrics.title("Lyrics of "+songdisp.get(sel4))
        except:
            sel4=queuedisp.curselection()
            lyrics.title("Lyrics of "+queuedisp.get(sel4))
        lyrics.iconbitmap("icon.ico")
        lyrics['bg']="#4d004d"
        access=c.execute("SELECT * FROM lyrics")
        conn.commit()
        var=0
        for i in access:
            try:
                sel4=songdisp.curselection() 
                if len(sel4)==0:
                    raise Exception
                if songdisp.get(sel4) in i:
                    songdisp["state"]=DISABLED
                    queuedisp["state"]=DISABLED
                    var=1
                    lyricstxt.insert(END, i[1], 'center')
                    lyricstxt['state'] = DISABLED
                    scroll.pack(side=RIGHT, padx=10, pady=10, fill=Y)
                    lyricstxt.pack(pady=10)
                    Button(lyrics,text="Delete lyrics",command=delete,fg="white",bg="#4d004d",font=("Agency FB",15,'bold','underline'),activebackground="#4d004d",activeforeground="red").pack(pady=5)
                    try:
                        l1.destroy()
                        addmanually.destroy()
                    except:
                        pass
                    break
            except:
                sel4=queuedisp.curselection()
                if queuedisp.get(sel4) in i:
                    songdisp["state"]=DISABLED
                    queuedisp["state"]=DISABLED
                    var=1
                    lyricstxt.insert(END, i[1], 'center')
                    lyricstxt['state'] = DISABLED
                    scroll.pack(side=RIGHT, padx=10, pady=10, fill=Y)
                    lyricstxt.pack(pady=10)
                    Button(lyrics,text="Delete lyrics",command=delete,fg="white",bg="#4d004d",font=("Agency FB",15,'bold','underline'),activebackground="#4d004d",activeforeground="red").pack(pady=5)
                    try:
                        l1.destroy()
                        addmanually.destroy()
                    except:
                        pass
                    break
        def on_closing():
            songdisp["state"]=NORMAL
            queuedisp["state"]=NORMAL
            lyrics.destroy()
        lyrics.protocol("WM_DELETE_WINDOW", on_closing)
        conn.commit()
        if var==0:
            l1=Label(lyrics,text="Enter song name:",font="Times 15",bg="#4d004d",fg="red",padx=10)
            l1.pack()
            songname=Entry(lyrics,bg="#330033",fg="red")
            songname.pack()
            save=Button(lyrics,text="GO",command=save,fg="white",bg="#4d004d",font=("Agency FB",15,'bold','underline'),activebackground="#4d004d",activeforeground="red")
            save.pack(pady=5)
            addmanually=Button(lyrics,text="Add lyrics manually",command=addmanually,fg="white",bg="#4d004d",font=("Agency FB",15,'bold','underline'),activebackground="#4d004d",activeforeground="red")
            addmanually.pack(pady=5)
def playlistsfun():
    def delplaylist():
        try:
            c1.execute("DELETE FROM playlists WHERE playlist=(?)",
                       (playlistdisp.get(playlistdisp.curselection())[0],))
            conn1.commit()
            playlistdisp.delete(playlistdisp.curselection())
        except Exception as e:
            print(e)
            messagebox.showwarning("No selection","Select a playlist",parent=playlists)
            
    def renameplaylist():
        try:
            z=playlistdisp.curselection()
            if len(z)==0:
                raise Exception
            def save():
                existing=c1.execute("SELECT playlist FROM playlists")
                try:
                    for i in existing:
                        if playlistname.get()==i[0]:
                            raise Exception
                    else:        
                        c1.execute("UPDATE playlists SET playlist=(?) WHERE playlist=(?)",
                                   (playlistname.get(),playlistdisp.get(z)[0]))
                        conn1.commit()
                except:
                    messagebox.showwarning(playlistname.get()+" already exists","Choose a different name",parent=playlists)
                else:
                    playlistdisp.delete(z)
                    playlistdisp.insert(z,playlistname.get())
                    playlistname.destroy()
                    save.destroy()
            playlistname=Entry(playlists,bg="#330033",fg="red")
            playlistname.grid(row=0,sticky=E+W,padx=60,pady=5,column=0,columnspan=3)
            save=Button(playlists,text="SAVE",command=save,fg="white",bg="#4d004d",font=("Agency FB",15,'bold','underline'),activebackground="#4d004d",activeforeground="red")
            save.grid(row=1,sticky=E+W+N,padx=120,column=0,columnspan=3)
        except Exception:
            messagebox.showwarning("No selection","Select a playlist",parent=playlists)
            
    #def clearplaylist():
    #    playlistdisp.delete(0,END)
        
    def currentqueue():
        try:
            if queuedisp.size()==0:
                raise Exception 
            def save():
                global queuedisp
                global playlistname
                try:
                    if playlistname.get()=='':
                        raise Exception
                except:
                    messagebox.showwarning("No name","Input a name for the playlist",parent=playlists)
                else:
                    existing=c1.execute("SELECT playlist FROM playlists")
                    try:
                        for i in existing:
                            print(i)
                            print(playlistname.get())
                            if playlistname.get()==i[0]:
                                raise Exception
                        else:
                            sel=queuedisp.get(0,END)
                            name=playlistname.get()
                            playlistdisp.insert(END,playlistname.get())
                            playlistname.destroy()
                            save.destroy()
                            l=[]
                            for i in sel:
                                l.append(i)
                            c1.execute("INSERT INTO playlists VALUES(?,?)",
                                       (name,str(l)))
                            conn1.commit()
                    except Exception as e:
                        print(e)
                        messagebox.showwarning(playlistname.get()+" already exists","Choose a different name",parent=playlists)
            global playlistname
            playlistname=Entry(playlists,bg="#330033",fg="red")
            playlistname.grid(row=0,sticky=E+W,padx=60,pady=5,column=0,columnspan=3)
            save=Button(playlists,text="SAVE",command=save,fg="white",bg="#4d004d",font=("Agency FB",15,'bold','underline'),activebackground="#4d004d",activeforeground="red")
            save.grid(row=1,sticky=E+W+N,padx=120,column=0,columnspan=3)
        except:
            messagebox.showwarning("Empty queue","Add songs to queue",parent=playlists)
    global playlistwin
    global playlists
    try:
        if playlistwin==1:
            playlists.withdraw()
    except:
        pass
    playlists=Toplevel()
    playlistwin=1
    playlists.resizable(width=False,height=False)
    playlists.title("Playlists")
    playlists.iconbitmap("icon.ico")
    playlists['bg']="#4d004d"
    
    def playlisttoqueue():
        try:
            if len(playlistdisp.curselection())==0:
                raise NameError
            global playbool
            playbool=True
            global playlistname
            playlistname=playlistdisp.get(playlistdisp.curselection())[0]
            queuedisp.delete(0,END)
            songs=c1.execute("SELECT songs FROM playlists WHERE playlist=(?)",
                       (playlistdisp.get(playlistdisp.curselection())[0],))
            for i in songs:
                final=i[0]
                for j in ['"[',']"',"'",'[']:
                    final=final.replace(j,"")
                final=final.split(", ")
            for i in final:
                queuedisp.insert(END,i)
        except NameError:
             messagebox.showwarning("No selection","Select a playlist",parent=player)
            
    # Label:
    Label(playlists,text="Your Playlists:",fg="red",font="Fixedsys 10 bold",bg="#4d004d").grid(sticky=W,row=2,column=0,padx=10,pady=5)
    
    # Scroll bar for playlistdisp:
    scrolly2=Scrollbar(playlists,orient=VERTICAL)
    #scrolly2.grid(sticky=N+S,row=3,column=1,padx=5)

    # Playlist display:
    global playlistdisp
    playlistdisp=Listbox(playlists,bg="#1a001a",yscrollcommand=scrolly2.set,height=10,width=50,fg="red",highlightbackground="#330033",highlightthickness=10,relief=GROOVE,highlightcolor="#330033")
    playlistdisp.grid(padx=10,row=3,column=0)
    playlistnames=c1.execute("SELECT playlist from playlists")
    for i in playlistnames:
        playlistdisp.insert(END,i)
        
    # Schroll config:
    scrolly2.config(command=playlistdisp.yview)
    
    # delete, rename, clear, current queue, add to queue buttons:
    f=Frame(playlists,bg="#4d004d")
    f.grid(row=4,column=0,sticky=E+W,padx=10)
    delplaylist=Button(f,text="Delete",command=delplaylist,fg="white",bg="#4d004d",activebackground="#4d004d",activeforeground="red",font=("Agency FB",10,'bold'))
    delplaylist.grid(row=0,column=0,pady=5)
    renameplaylist=Button(f,text="Rename",command=renameplaylist,fg="white",bg="#4d004d",activebackground="#4d004d",activeforeground="red",font=("Agency FB",10,'bold'))
    renameplaylist.grid(row=0,column=1,pady=5,padx=5)
    #clearplaylist=Button(f,text="Clear",command=clearplaylist,fg="red",bg="#4d004d",activebackground="#4d004d",activeforeground="red",font=("Agency FB",10,'bold'))
    #clearplaylist.grid(row=0,column=2)
    currentqueue=Button(playlists,text="Create a playlist\nof the current queue",command=currentqueue,fg="white",bg="#4d004d",activebackground="#4d004d",activeforeground="red",font=("Agency FB",12,'bold'))
    currentqueue.grid(row=2,column=0,sticky=E,padx=10,pady=5)  
    playlisttoqueue=Button(playlists,text="Add playlist\nto queue",fg="white",bg="#4d004d",activebackground="#4d004d",activeforeground="red",font=("Agency FB",10,'bold'),command=playlisttoqueue)
    playlisttoqueue.grid(row=4,column=0,pady=5,padx=10,sticky=E)
    
def addtoplaylist():
    def save():
        global songdisp
        global playlistname
        try:
            if playlistname.get()=='':
                raise Exception
        except:
            messagebox.showwarning("No name","Input a name for the playlist",parent=playlists)
        else:
            existing=c1.execute("SELECT playlist FROM playlists")
            try:
                for i in existing:
                    if playlistname.get()==i[0]:
                        raise Exception
                else:
                    l=[]
                    for i in songdisp.curselection():
                        l.append(songdisp.get(i))
                    name=playlistname.get()
                    playlistdisp.insert(END,playlistname.get())
                    playlistname.destroy()
                    save.destroy()
                    c1.execute("INSERT INTO playlists VALUES(?,?)",
                               (name,str(l)))
                    conn1.commit()
            except:
                messagebox.showwarning(playlistname.get()+" already exists","Choose a different name",parent=playlists)
    try:
        sel=songdisp.curselection()
        if len(sel)==0:
            raise Exception
    except:
        messagebox.showwarning("No selection","Select one or more song(s)",parent=player)
    else:
        try:
            if playlistwin==1:
                playlists.withdraw()
        except:
            pass
        global playlistname
        playlistsfun()
        playlistname=Entry(playlists,bg="#330033",fg="red")
        playlistname.grid(row=0,sticky=E+W,padx=60,pady=5,column=0,columnspan=3)
        save=Button(playlists,text="SAVE",command=save,fg="white",bg="#4d004d",font=("Agency FB",15,'bold','underline'),activebackground="#4d004d",activeforeground="red")
        save.grid(row=1,sticky=E+W+N,padx=120,column=0,columnspan=3)

def playfun():
    global sel5
    global var
    var=0
    global n
    global i
    global y 
    y=0
    i=0
    global move
    def move():
        x1,y1,x2,y2 = canvas.bbox(crntsong)
        if(x2<0 or i==1): 
            if i==1:
                canvas.coords(crntsong,20,5)
            else:
                canvas.coords(crntsong,500,5)
                move()
        else:
            canvas.move(crntsong, -0.5, 0)
            canvas.after(10,move)
    if n%2==0:
        global curframe
        global sel3
        try:
            if curplaylist['text']!="":
                curplaylist['text']=""    
            global sel
            global sel1
            sel=songdisp.curselection()
            sel1=queuedisp.curselection()
            if len(sel)>1:
                raise NameError
            canvas.itemconfigure(crntsong, text=songdisp.get(sel))
        except NameError:
            messagebox.showwarning("Multiple selections","Select only one song")
        except:
            try:
                try:
                    if queuedisp.size()!=0:
                        global playbool
                        if playbool==True:
                            curplaylist['text']=("Current playlist: "+playlistname)
                except:
                    pass
                canvas.itemconfigure(crntsong, text=queuedisp.get(sel1))
            except:
                messagebox.showwarning("No selection","Select a song")
            else:
                def cursel2():
                    #global var2
                    global sel5
                    #var2=1
                    try:
                        sel5=queuedisp.get(queuedisp.curselection())
                    except:
                        sel5=songdisp.get(songdisp.curselection())
                    if sel5==queuedisp.get(sel1):
                        global var2
                        var2=0
                    else:
                        var2=1
                queuedisp.bind("<<ListboxSelect>>",lambda x:cursel2())
                try:
                    try:
                        global var2
                        #global sel5
                        if sel5==sel or var2==0:
                            mixer.music.unpause()
                    except:
                        mixer.music.unpause()
                    if mixer.music.get_busy()==0:
                        raise Exception 
                except:
                    try:
                        s=c2.execute("SELECT songpath FROM songs WHERE songname=(?)",
                                     (sel5,))
                        for i in s:
                            s=list(i)    
                            mixer.music.load(s[0])
                            mixer.music.play(-1)
                    except:
                        s=c2.execute("SELECT songpath FROM songs WHERE songs=(?)",
                                     (queuedisp.get(sel1),))
                        for i in s:
                            s=list(i)
                            mixer.init()
                            mixer.music.load(s[0])
                            mixer.music.play(-1)
                if n!=0:
                    try:
                        del sel5
                    except:
                        pass
                #global video
                #global video_stream
                videos = [f for f in listdir(r'videos')]
                if n==0:
                    video=cv2.VideoCapture(r'videos\\'+str(random.choice(videos)))
                if n!=0:
                    if sel3==canvas.itemcget(crntsong,'text'):
                        video.set(cv2.CAP_PROP_POS_FRAMES,curframe)
                    else:
                        video=cv2.VideoCapture(r'videos\\'+str(random.choice(videos)))
                def video_stream():
                    global video
                    a,videoimage=video.read()
                    try:
                        if a==False:
                            raise Exception
                    except:
                        video=cv2.VideoCapture(r'videos\\'+str(random.choice(videos)))
                        a,videoimage=video.read()
                    img = cv2.cvtColor(videoimage, cv2.COLOR_BGR2RGBA)
                    img=Image.fromarray(img)
                    img=img.resize((480,355),Image.ANTIALIAS)
                    imgtk = ImageTk.PhotoImage(image=img)
                    videoframe.imgtk = imgtk
                    videoframe['image']=imgtk
                    videoframe.after(10, video_stream)
                video_stream()
                stopbut['state']=NORMAL
                try:
                    queuedisp.itemconfig(sel1,{"fg":"white"})
                    n+=1
                    playbut['image']=pause
                    playbut['command']=playfun
                    move()
                except:
                    pass
        else:
            def cursel1():
                #global var2
                global sel5
                #var2=1
                try:
                    sel5=songdisp.get(songdisp.curselection())
                except:
                    sel5=queuedisp.get(queuedisp.curselection())
                if sel5==songdisp.get(sel):
                    global var1
                    var1=0
                else:
                    var1=1
            songdisp.bind("<<ListboxSelect>>",lambda x:cursel1())
            try:
                try:
                    global var1
                    global sel5
                    if sel5==sel or var1==0:
                        mixer.music.unpause()
                except:
                    mixer.music.unpause()
                if mixer.music.get_busy()==0:
                    raise Exception 
            except:
                try:
                    s=c2.execute("SELECT songpath FROM songs WHERE songname=(?)",
                                 (sel5,))
                    for i in s:
                        s=list(i)    
                        mixer.music.load(s[0])
                        mixer.music.play(-1)
                except:
                    s=c2.execute("SELECT songpath FROM songs WHERE songs=(?)",
                             (songdisp.get(sel),))
                    for i in s:
                        s=list(i)
                        mixer.init()
                        mixer.music.load(s[0])
                        mixer.music.play(-1)
            if n!=0:
                try:
                    del sel5
                except:
                    pass
            global video
            global video_stream
            videos = [f for f in listdir(r'videos')]
            if n==0:
                video=cv2.VideoCapture(r'videos\\'+str(random.choice(videos)))
            if n!=0:
                if sel3==canvas.itemcget(crntsong,'text'):
                    video.set(cv2.CAP_PROP_POS_FRAMES,curframe)
                else:
                    video=cv2.VideoCapture(r'videos\\'+str(random.choice(videos)))
            def video_stream():
                global video
                a,videoimage=video.read()
                try:
                    if a==False:
                        raise Exception
                except:
                    video=cv2.VideoCapture(r'videos\\'+str(random.choice(videos)))
                    a,videoimage=video.read()
                img = cv2.cvtColor(videoimage, cv2.COLOR_BGR2RGBA)
                img=Image.fromarray(img)
                img=img.resize((480,355),Image.ANTIALIAS)
                img = ImageTk.PhotoImage(image=img)
                videoframe.imgtk = img
                videoframe['image']=img
                videoframe.after(10, video_stream)
            video_stream()
            stopbut['state']=NORMAL
            try:
                songdisp.itemconfig(sel,{"fg":"white"})
                n+=1
                playbut['image']=pause
                playbut['command']=playfun
                move()
            except:
                pass
    else:
        try:
            mixer.music.pause()
        except:
            pass
        curframe=video.get(cv2.CAP_PROP_POS_FRAMES)
        sel3=canvas.itemcget(crntsong,'text')
        def video_stream():
            return
        stopbut['state']=DISABLED
        try:
            queuedisp.itemconfig(sel1,{"fg":"red"})
        except:
            try:
                songdisp.itemconfig(sel,{"fg":"red"})
            except:
                pass
        n+=1
        i=1
        playbut['image']=play
        playbut['command']=playfun  
               
# Top Bar:    
framecolor="#4d004d"
global frame
frame=Frame(player,bg=framecolor)
frame.grid(row=0,columnspan=5,sticky=W+E)
global curplaylist
curplaylist=Label(frame,text=(""),font="Forte 20",fg="red",bg="#4d004d")
curplaylist.pack(side=RIGHT,padx=10,pady=5)
Button(frame,text="Your library",bg="#4d004d",command=choosesongs,fg="white",font=("Agency FB",15,'bold','underline'),relief=RAISED,padx=5,activebackground="#4d004d",activeforeground="red").pack(side=LEFT,padx=10,pady=5)
Button(frame,text="Lyrics",command=lyrics,bg="#4d004d",fg="white",font=("Agency FB",15,'bold','underline'),relief=RAISED,padx=5,activebackground="#4d004d",activeforeground="red").pack(side=LEFT,pady=5)
Button(frame,text="Playlists",command=playlistsfun,bg="#4d004d",fg="white",font=("Agency FB",15,'bold','underline'),relief=RAISED,padx=5,activebackground="#4d004d",activeforeground="red").pack(side=LEFT,padx=10,pady=5)

# Title:
frame1=Frame(bg="#1a001a",height=100,highlightbackground="#330033",highlightthickness=10)
frame1.grid(row=1,columnspan=5,pady=5,sticky=N+W+E+S,padx=10)
Label(frame1,text="UnPaused",font="Algerian 28 underline",fg="red",bg="#1a001a").pack()
Label(frame1,text="Sing along to your favourite song",font="Aharoni 20 italic",fg="red",bg="#1a001a").pack()

# "Add to queue" button
Button(text="Add\nto queue",command=add,fg="white",bg="#4d004d",activebackground="#4d004d",activeforeground="red",font=("Agency FB",10,'bold')).grid(row=3,column=1,pady=5,padx=10,sticky=W)
# "Add to playlist" button
Button(text="Create\nplaylist",command=addtoplaylist,fg="white",bg="#4d004d",activebackground="#4d004d",activeforeground="red",font=("Agency FB",10,'bold')).grid(row=3,column=1,sticky=E,padx=10,pady=5)


# Scroll bar for queuedisp:
scrolly1=Scrollbar(orient=VERTICAL)
#scrolly1.grid(sticky=N+S+E,row=4,column=4,padx=5)
scrollx1=Scrollbar(player,orient=HORIZONTAL)
scrollx1.grid(sticky=E+W,row=5,column=3,padx=10,pady=5)


# Queue display:
# Queue label:
Label(text="Queued\nSongs",fg="white",bg="#4d004d",font=("'Eras Bold ITC'",10,'underline italic bold')).grid(row=3,column=3,padx=10)

# Clear Queue button:
Button(text="Clear\nqueue",fg="white",bg="#4d004d",activebackground="#4d004d",activeforeground="red",command=clearqueue,font=("Agency FB",10,'bold'),padx=5).grid(row=3,column=3,pady=5,padx=10,sticky=W)

# Delete button:
Button(text="Delete",fg="white",bg="#4d004d",activebackground="#4d004d",activeforeground="red",command=deletequeue,font=("Agency FB",10,'bold'),padx=5).grid(row=3,column=3,padx=10,sticky=E,pady=5)

queuedisp=Listbox(bg="#1a001a",yscrollcommand=scrolly1.set,xscrollcommand=scrollx1.set,height=20,width=30,fg="red",highlightbackground="#330033",highlightthickness=10,relief=GROOVE,highlightcolor="#330033")
queuedisp.grid(row=4,column=3,sticky=N+S+E+W,padx=10)
    
# Current song rolling text:
canvas=Canvas(height=15,width=5,bg='#330033')
canvas.grid(row=5,column=2,sticky=N+S+E+W,padx=10)
crntsong=canvas.create_text(20,5,text="Current song will be displayed here",fill="red",anchor=NW,font=('Californian FB',11,'bold'))
    
# Schroll1 config:
scrolly.config(command=songdisp.yview)
scrollx.configure(command=songdisp.xview)

# Schroll2 config:
scrolly1.config(command=queuedisp.yview)
scrollx1.configure(command=queuedisp.xview)

# Control images:
play=PhotoImage(file="play.png")
previous=PhotoImage(file="previous.png")
next=PhotoImage(file="next.png")
shuffle=PhotoImage(file="shuffle.png")
stop=PhotoImage(file="stop.png")
pause=PhotoImage(file="pause.png")

# Controls frame
bg="#1a001a"
frame2=Frame(player,pady=10,bg=bg,highlightbackground="#330033",highlightthickness=10)
frame2.grid(row=6,columnspan=6,pady=10,sticky=W+E,padx=10)
frame2.grid_columnconfigure((0,1,3,4),weight=1)

# Adding buttons
playbut=Button(frame2,image=play,borderwidth=0,command=playfun,bg=bg,activebackground=bg)
playbut.grid(row=0,column=2)
prevbut=Button(frame2,image=previous,borderwidth=0,command=prev,bg=bg,activebackground=bg).grid(row=0,column=1,sticky=W+E+N+S)
nextbut=Button(frame2,image=next,borderwidth=0,command=nextf,bg=bg,activebackground=bg).grid(row=0,column=3,sticky=W+E+N+S)
shufbut=Button(frame2,image=shuffle,borderwidth=0,anchor=W,command=shuffun,bg=bg,activebackground=bg).grid(row=0,column=4,sticky=W+E+N+S)
stopbut=Button(frame2,image=stop,borderwidth=0,anchor=E,command=stopfun,state=DISABLED,bg=bg,activebackground=bg)
stopbut.grid(row=0,column=0,sticky=W+E+N+S)
def on_closing1():
    try:
        global sel5
        del sel5
    except:
        pass
    try:
        mixer.music.unload()  
    except:
        pass
    player.destroy()
player.protocol("WM_DELETE_WINDOW", on_closing1)
player.mainloop()
