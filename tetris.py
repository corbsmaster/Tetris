import random, grafics, time, highscore
import pygame as pg
from math import ceil
from os import path
from tkinter import messagebox


config={'sheight':800,'swidth':700,'gheight':20,'gwidth':10, 'block_size':30}

S = [['.....',
      '..00.',
      '.00..',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.00..',
      '..00.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '0000.',
      '.....',
      '.....',
      '.....'],
     ['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....']]

O = [['.....',
      '.00..',
      '.00..',
      '.....',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

forms = [S, Z, I, O, J, L, T]
forms_colors = [(242,65,80), (134,244,127), (31,175,191), (191,137,115), (89,89,89), (249,107,55), (202,52,134)]
# index 0 - 6 represent shape
 
class Tetromino():
    def __init__(self):
        self.x = ceil(config['gwidth']/2)
        self.y = 0 #oder doch eins (damit es sicher ganz am bildschirm ist)
        self.form = random.choice(forms)
        self.color = forms_colors[forms.index(self.form)]
        self.rotation = 0
 
def cgrid(stoned):
    grid=[[8 for x in range(config['gwidth'])]for y in range(config['gheight'])] #create Matrix
    
    for i in range(config['gheight']): #check if gridpos is occupied
        for j in range(config['gwidth']):
            if (i,j) in stoned:
                color=stoned[(i,j)]
                grid[i][j]=color                    
    return grid
 
def convert_form_format(tetromino):
    positions = list()
    rotation = tetromino.form[tetromino.rotation % len(tetromino.form)]
    
    for i, line in enumerate(rotation):
        line = list(line)
        for j, column in enumerate(line):
            if column == '0':
                positions.append((tetromino.y + i, tetromino.x + j))
                
    for i, pos in enumerate(positions): #wieder zentrieren, da die Listen einen Offset produzieren 
        positions[i] = (pos[0] - 1, pos[1] - 2)
        
    return positions
    
def islegal(form, grid):
    empty_pos = [[(i,j) for i in range(config['gheight']) if grid[i][j] == 8] for j in range(config['gwidth'])]
    empty_pos = [i for sub in empty_pos for i in sub] #umschreiben weil wer kommt da so drauf (+es geht anders^^)
    
    formatted = convert_form_format(form)
    
    for pos in formatted:
        if pos not in empty_pos:
            if pos[0] > 0:
                return False
    return True
 
def check_gameover(positions): #ev umschreiben und beim spawnen checken ob islegal (wenn nein -> gameover)
    for pos in positions:
        y,x = pos
        if y < 1:
            return True
    return False
    
def clear_lines(grid, stoned):
    
    counter = 0
    line_indizes = []
    for i in range(config['gheight']-1,-1,-1):
        line = grid[i]
        if 8 not in line:
            counter +=1
            line_indizes.append(i)
            for j in range(config['gwidth']):
                del stoned[(i,j)]
    
    while len(line_indizes) < 4: #line_indizes mit 0 auf 4 Stellen auffüllen
        line_indizes.append(-1)
             
    if counter > 0: #verbleibende Reihen verschieben
        for key in sorted(list(stoned), key = lambda x: x[0])[::-1]: #stoned nach y value sortieren
            y,x = key
            if y < line_indizes[0] and y > line_indizes[1]: #move down all lines between 1st and 2nd cleared line by 1
                newKey = (y + 1, x)
                stoned[newKey] = stoned.pop(key)
            elif y < line_indizes[1] and y > line_indizes[2]: #move down all lines between 2nd and 3rd cleared line by 2
                newKey = (y + 2, x)
                stoned[newKey] = stoned.pop(key)
            elif y < line_indizes[2] and y > line_indizes[3]: #move down all lines between 3rd and 4th cleared line by 3
                newKey = (y + 3, x)
                stoned[newKey] = stoned.pop(key)
            elif y < line_indizes[3]: #move down all lines above 4th cleared line by 4
                newKey = (y + 4, x)
                stoned[newKey] = stoned.pop(key)
    
    return counter


def main():
    win = pg.display.set_mode((config['swidth'], config['sheight']))
    pg.display.set_caption('Tetris')

    
    stoned = {}
    go_to_next = False
    current = Tetromino()
    coming = Tetromino()
    clock = pg.time.Clock()
    fall_time = 0
    fall_speed = 0.3
    clears_in_lvl = 0
    lvl = 0
    score=[0,0] #[points, lines cleared]
    
    run = True
    paused = False
        
    
    #load sounds and music
    try:
        pathname = path.dirname(__file__) #get directory of this file
        Ssuck = pg.mixer.Sound(pathname+'\Sounds\Effects\you suck.wav')
        Slvl_up = pg.mixer.Sound(pathname+'\Sounds\Effects\Lvl up.wav')
        Scan_u_keep_up = pg.mixer.Sound(pathname+'\Sounds\Effects\can you keep up.wav')
        Sgame_over = pg.mixer.Sound(pathname+'\Sounds\Effects\game over.wav')
        Su_failed = pg.mixer.Sound(pathname+'\Sounds\Effects\you failed.wav')
        Sclick1 = pg.mixer.Sound(pathname+'\Sounds\Effects\click 1.wav')
        Sclick2 = pg.mixer.Sound(pathname+'\Sounds\Effects\click 2.wav')
        Sblob11 = pg.mixer.Sound(pathname+'\Sounds\Effects\\blob1 1.wav')
        Sblob12 = pg.mixer.Sound(pathname+'\Sounds\Effects\\blob1 2.wav')
        Sblob13 = pg.mixer.Sound(pathname+'\Sounds\Effects\\blob1 3.wav')
        Sblob14 = pg.mixer.Sound(pathname+'\Sounds\Effects\\blob1 4.wav')
        Sblob21 = pg.mixer.Sound(pathname+'\Sounds\Effects\\blob2 1.wav')
        Sblob22 = pg.mixer.Sound(pathname+'\Sounds\Effects\\blob2 2.wav')
        Sblob23 = pg.mixer.Sound(pathname+'\Sounds\Effects\\blob2 3.wav')
        Sblob24 = pg.mixer.Sound(pathname+'\Sounds\Effects\\blob2 4.wav')
        Swin = pg.mixer.Sound(pathname+'\Sounds\Effects\Win_Org.wav')
    except:
        messagebox.showerror("Soundfile missing", "Couldn't find all the effectsounds in subdirectory 'Effects' of 'Sounds'.\nPlease make sure, that your 'Effects'-folder is complete and restart the game!")
        pg.display.quit()
        return 'Error'
        
    try:    
        M_Marimba_1st = [pathname+'\Sounds\Marimba 1st '+str(x)+'.mp3' for x in range(13)]
        M_Marimba_2st = [pathname+'\Sounds\Marimba 2st '+str(x)+'.mp3' for x in range(13)]
        M_Marimba_3st = [pathname+'\Sounds\Marimba 3st '+str(x)+'.mp3' for x in range(13)]
        M_Marimba_Quint = [pathname+'\Sounds\Marimba Quint '+str(x)+'.mp3' for x in range(13)]
        M_Acapella = [pathname+'\Sounds\Acapella '+str(x)+'.mp3' for x in range(13)]
        M_Acapella_fills = [pathname+'\Sounds\Acapella fills '+str(x)+'.mp3' for x in range(13)]    
        M_Variations = [M_Marimba_1st, M_Marimba_2st, M_Marimba_3st, M_Marimba_Quint, M_Acapella, M_Acapella_fills]
        music = random.choice(M_Variations)[0]
        
        pg.mixer.music.stop()
        pg.mixer.music.load(music)
        pg.mixer.music.play(-1)
        
    except:
        messagebox.showerror("Soundfile missing", "Couldn't find '"+music+"' in subdirectory 'Sounds'!\nNo music for you for a while :(")
    

    while run:
        grid = cgrid(stoned)
        fall_time += clock.get_rawtime()
        clock.tick()

                
        for event in pg.event.get():    
            if event.type == pg.QUIT:
                run = False
                pg.mixer.music.fadeout(500)
                time.sleep(.501)
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: #get back to menu
                     run = False
                     pg.mixer.music.fadeout(500)
                     time.sleep(.501)

                if event.key == pg.K_p: #pause the game
                     paused = True
                     
                     try: #start pause music
                         pg.mixer.music.stop()
                         pg.mixer.music.load(pathname+'\Sounds\Jeopardy Theme.mp3')
                         pg.mixer.music.play(-1)
                     except:
                         messagebox.showerror("Soundfile missing", "Couldn't find 'Jeopardy Theme' in subdirectory 'Sounds'!\nNo music while pausing for you :(")
                         
                     grafics.text_middle(win, 'GAME PAUSED', 80, (0,0,0))
                     grafics.text_middle(win, 'press p to unpause', 30, (0,0,0), (0,90))
                     pg.display.update()
                if event.key == pg.K_LEFT: #shift left
                    current.x -= 1
                    if not(islegal(current, grid)):
                        current.x += 1
                if event.key == pg.K_RIGHT: #shift right
                    current.x += 1
                    if not(islegal(current, grid)):
                        current.x -= 1
                if event.key == pg.K_DOWN: #softdrop
                    current.y += 1
                    score[0] += 1
                    if not(islegal(current, grid)):
                        current.y -= 1
                        score[0] -= 1
                if event.key == pg.K_UP: #rotate clockwise
                    current.rotation += 1
                    if not(islegal(current, grid)):
                        current.rotation -= 1
                if event.key == pg.K_SPACE: #harddrop
                    done = False
                    while not done:
                        if islegal(current, grid):
                            current.y += 1
                            score[0] += 1
                        else:
                            current.y -= 1
                            score[0] -= 1
                            go_to_next = True
                            done = True
                            
        while paused: #Endlessloop to pause
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    paused = False
                    run = False
                    pg.mixer.music.fadeout(500)
                    time.sleep(.501)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE: #get back to menu
                        paused = False
                        run = False
                        pg.mixer.music.fadeout(500)
                        time.sleep(.501)
                    if event.key == pg.K_p: #unpause
                        paused = False
                        
                        try: #return to game music
                            pg.mixer.music.stop()
                            music = random.choice(M_Variations)[lvl//2 +lvl%2]
                            pg.mixer.music.load(music)
                            pg.mixer.music.play(-1)
                        except:
                            messagebox.showerror("Soundfile missing", "Couldn't find '"+music+"' in subdirectory 'Sounds'!\nNo music for you for a while :(")


        if fall_time/1000 > fall_speed: #next tick
            fall_time = 0
            current.y += 1
            if not islegal(current, grid) and current.y > 0:
                current.y -= 1
                go_to_next = True
 
       
        form_pos = convert_form_format(current)
        
        for j in range(len(form_pos)): #set grid to color of current Tetromino
            x,y = form_pos[j]
            if y > -1:
                grid[x][y] = forms_colors.index(current.color)
                        
        if go_to_next: #spawn next
            for p in form_pos:
                stoned[p] = forms_colors.index(current.color)
            current = coming
            coming = Tetromino()
            go_to_next = False
            counter = clear_lines(grid, stoned)
            clears_in_lvl += counter
            
            score[1] += counter
            if counter == 0:
                random.choice([Sclick1,Sclick2]).play()
            elif counter == 1:
                random.choice([Sblob11,Sblob21]).play()
                score[0] += 40*(lvl+1)
            elif counter == 2:
                random.choice([Sblob12,Sblob22]).play()
                score[0] += 100*(lvl+1)
            elif counter == 3:
                random.choice([Sblob13,Sblob23]).play()
                score[0] += 300*(lvl+1)
            elif counter == 4:
                random.choice([Sblob14,Sblob24]).play()
                score[0] += 1200*(lvl+1)
                
            #lvl up
            if clears_in_lvl >= 10:
                clears_in_lvl -= 10
                lvl += 1
                if lvl % 2 == 1 and lvl < 25: #Alternatively: in (1,3,5,7,10,12,15,18,21,24,27,30): #pitch up
                    try: #start pitched music
                        pg.mixer.music.stop()
                        music = random.choice(M_Variations)[lvl//2 +lvl%2]
                        pg.mixer.music.load(music)
                        pg.mixer.music.play(-1)
                    except:
                        messagebox.showerror("Soundfile missing", "Couldn't find '"+music+"' in subdirectory 'Sounds'!\nNo music for you for a while :(")
                if random.randint(0,2) < 2:
                    Slvl_up.play()
                else:
                    Scan_u_keep_up.play()
                fall_speed -= 0.009
            
            
        grafics.draw_window(win, grid, config)
        grafics.draw_lvlscore(lvl, score, win)
        grafics.draw_next_form(coming, win)
                        
        pg.display.update()
        
        if check_gameover(stoned):
            Swin.play()
            if score[0] < 160: #tell the sucker that he's bad
                Ssuck.play()
                grafics.text_middle(win, 'YOU SUCK!', 80, (0,0,0))
                text = 'YOU SUCK!'
                pg.display.update()
            else:
                if random.randint(0,2) < 2:
                    Sgame_over.play()
                    grafics.text_middle(win, 'GAME OVER!', 80, (0,0,0))
                    text = 'GAME OVER!'
                    pg.display.update()
                else:
                    Su_failed.play()
                    grafics.text_middle(win, 'YOU FAILED!', 80, (0,0,0))
                    text = 'YOU FAILED!'
                    pg.display.update()

            run = False
            pg.mixer.music.fadeout(500)
            
            name = ''
            valid = "^1234567890ß´qwertzuiopü+asdfghjklöä#<yxcvbnm,.-"
            valid_shift = "°!2§$%&/()=?`QWERTZUIOPÜ*ASDFGHJKLÖÄ'>YXCVBNM;:_"
            shift = False
            submitted = False
            while not submitted:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        submitted = True    
                    if event.type == pg.KEYUP:
                        if event.key in [pg.K_RSHIFT, pg.K_LSHIFT]:
                            shift = False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE: #get back to menu
                            submitted = True
                        if event.key == pg.K_RETURN:
                            submitted = True
                        if event.key == pg.K_BACKSPACE:
                            name = name[:-1]
                        if event.key in [pg.K_RSHIFT, pg.K_LSHIFT]:
                            shift = True
                        if event.key == pg.K_MODE:
                            shift = True
                        if event.key == pg.K_SPACE:
                            name += ' '
                        if chr(event.key) in valid and shift == False:
                            if chr(event.key) == 'z':
                                name += 'y'
                            elif chr(event.key) == 'y':
                                name += 'z'
                            else:   
                                name += chr(event.key)
                        if chr(event.key) in valid and shift == True:
                            if valid_shift[valid.index(chr(event.key))] == 'Z':
                                name += 'Y'
                            elif valid_shift[valid.index(chr(event.key))] == 'Y':
                                name += 'Z'
                            elif valid_shift[valid.index(chr(event.key))] == '2':
                                name += '"'
                            else:
                                name += valid_shift[valid.index(chr(event.key))]
                grafics.draw_window(win, grid, config)
                grafics.draw_lvlscore(lvl, score, win)
                grafics.draw_next_form(coming, win)
                grafics.text_middle(win, text, 80, (0,0,0))
                grafics.text_middle(win, 'type your name', 30, (0,0,0), (0,90))
                grafics.text_middle(win, name, 30, (0,0,0), (0,120))
                grafics.text_middle(win, 'press enter to submit', 30, (0,0,0), (0,150))
                pg.display.update()
                        

            if name != '':
                highscore.writescore(score[0],score[1], name)
            else:
                highscore.writescore(score[0],score[1])
                        
            time.sleep(.501)          
    pg.display.quit()
    

#win = pg.display.set_mode((config['swidth'], config['sheight']))
pg.display.set_caption('Tetris')
#main() # start game