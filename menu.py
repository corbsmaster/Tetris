"""
@author: Lukas Thalhammer, Ivan Todorović, Daniel Menczigar
"""

import tkinter as tk
from tkinter import messagebox
from pygame import mixer, init, version
from os import path
import tetris, time, pickle
import webbrowser



def new_game():
    if __name__ == '__main__':
        app = tetris
        mixer.music.fadeout(500) #stop menu music
        #Sstart.play() #play startsound
        s = app.main()
        
        if s == 'Error':
            mainmenu.destroy()
            return
        #return to menu & start menu music
        mixer.music.load(pathname+'\Sounds\Menu.mp3') #Load menu music
        mixer.music.play(-1) #start menu music (as loop)
        mainmenu.deiconify() #open menu

    
def highscore():
    with open('highscore','rb') as hs:
        scorelist=pickle.load(hs)
    if scorelist == []:
        scorelist.append('--empty--')
    root = tk.Tk()
    root.title('TETRIS HIGHSCORE')
    label = tk.Label(root, text = 'Highscore Top 10\n\n'+str(scorelist).replace('], [','\n')[2:-2], font = ('Vintage', '16'), fg = 'lightgrey', bg = 'black')
    label.pack(fill = tk.BOTH)
    Return = tk.Button(root, text = 'Return to Menu', command = lambda: [mainmenu.deiconify(), root.destroy()], font = ('Vintage', '12'), fg = 'lightgrey', bg = 'black') #return back to Mainmenu
    Return.pack(fill = tk.BOTH, expand = 1)
    root.protocol("WM_DELETE_WINDOW", lambda: [mixer.music.fadeout(200), time.sleep(.201), Sbye.play(), root.destroy(), mainmenu.destroy(), time.sleep(2), mixer.quit()])
    mainmenu.withdraw()
    
    
def options():
    root = tk.Tk()
    root.title('TETRIS INFO')
    label = tk.Label(root, text = 'UP = rotate clockwise\n LEFT/RIGHT = shift left/right \nDOWN = softdrop\nSPACE = harddrop\n\nP = pause/unpause\nESC = back to menu', font = ('Vintage', '14'), fg = 'lightgrey', bg = 'black')
    label.pack(fill = tk.BOTH)
    link1 = tk.Label(root, text="Scoring system - followed by the original TETRIS rules (Hyperlink)", fg = 'blue')
    link1.pack(fill = tk.BOTH, expand = 1)
    link1.bind("<Button-1>", lambda e: webbrowser.open_new("https://tetris.fandom.com/wiki/Scoring"))
    Return = tk.Button(root, text = 'Return to Menu', command = lambda: [mainmenu.deiconify(), root.destroy()], font = ('Vintage', '12'), fg = 'lightgrey', bg = 'black') #return back to Mainmenu
    Return.pack(fill = tk.BOTH, expand = 1)
    root.protocol("WM_DELETE_WINDOW", lambda: [mixer.music.fadeout(200), time.sleep(.201), Sbye.play(), root.destroy(), mainmenu.destroy(), time.sleep(2), mixer.quit()])
    mainmenu.withdraw()
    
    
def stop_playing():
    ok = messagebox.askyesno('REAL LIFE?!?!','DEIN ERNST?!')
    if ok:
        mixer.music.fadeout(200)
        time.sleep(.201)
        Sbye.play()
        mainmenu.destroy()
        time.sleep(2)
        mixer.quit()
        

#Initialize pygame and pygame.mixer [Menu.mp3 has to be in subdirectory 'Sounds'!!!]
pathname = path.dirname(__file__) #get directory of this file
init()
mixer.init()


#render main menu
mainmenu = tk.Tk()
mainmenu.geometry('500x325')
mainmenu.title('Tetris')
title = tk.Label(mainmenu, text = 'TETRIS', font = ('Vintage','18'), fg = 'lightgrey', bg = 'black')
Start = tk.Button(mainmenu ,text = 'PLAY', font = ('Vintage','18'), fg = 'lightgrey', bg = 'black', command = lambda: [mainmenu.withdraw(), new_game()])
Start.pack(fill = tk.X, padx = 60, pady = 15)
Info = tk.Button(mainmenu,text = 'INFO', font = ('Vintage','18'), fg = 'lightgrey', bg = 'black', command = options)
Info.pack(fill = tk.X, padx = 60, pady = 15)
Highscore = tk.Button(mainmenu, text = 'HIGHSCORE', font = ('Vintage','18'), fg = 'lightgrey', bg = 'black', command = highscore)
Highscore.pack(fill = tk.X,padx = 60, pady = 15)
button4 = tk.Button(mainmenu,text = 'EXIT', font = ('Vintage','18'), fg = 'lightgrey', bg = 'black', command = stop_playing)
button4.pack(fill = tk.X, padx = 60, pady = 15)


#Load Sounds and Music
Error = False
try:
    mixer.music.load(pathname+'\Sounds\Menu.mp3') #Load menu music
    Sstart = mixer.Sound(pathname+'\Sounds\Effects\Ladies Gentleman.wav') #Load startsound
    Sbye = mixer.Sound(pathname+'\Sounds\Effects\Win XP Shutdown Sound.ogg') #Load quitsound
    mixer.music.play(-1) #start menu music (as loop)
except:
    messagebox.showerror("Soundfile missing", "Couldn't find all the necessary sounds/music in subdirectory 'Sounds'!\nPlease make sure they are there, and start the game again.")
    mainmenu.destroy()
    Error = True
    

#init Highscore System
try:
    with open('highscore','rb') as hs:
        scorelist=pickle.load(hs)
except:
    with open('highscore','wb') as hs: #wenn nicht, erstelle sie
        scorelist=list() #und die darin enthaltene Liste
        pickle.dump(scorelist, hs)
        pos=0 #-> Platzierung 0

#start window
if not Error:
    mainmenu.protocol("WM_DELETE_WINDOW", lambda: [mixer.music.fadeout(200), time.sleep(.201), Sbye.play(), mainmenu.destroy(), time.sleep(2), mixer.quit()])
    if int(version.ver.replace('.','')) < 196:
        messagebox.showerror("Outdated Pygame Version", "You are using an old pygame version featuring soundbugs. Please consider updating for full game experience!")
    mainmenu.mainloop()