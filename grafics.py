import pygame as pg

config={'sheight':800,'swidth':700,'gheight':20,'gwidth':10, 'block_size':30}
forms_colors = [(242,65,80), (134,244,127), (31,175,191), (191,137,115), (89,89,89), (249,107,55), (202,52,134)]



def draw_window(surface, grid, config):
    surface.fill((242,242,242)) # background
    
    
    font = pg.font.SysFont('Vintage', 70)
    label = font.render('*******', 1, (31,175,191))
    surface.blit(label, (config['swidth']/2 - (label.get_width()/2), 725)) #swidth -labelwidth könnte negativ sein! #HÖHE (30) NOCH RICHTIG SETZEN
        
    
    for i in range(config['gheight']):
        for j in range(config['gwidth']):
            pg.draw.rect(surface, (242,242,242) if grid[i][j] == 8 else forms_colors[grid[i][j]], ((config['swidth'] - 30*config['gwidth'])//2 + j*config['block_size'], config['sheight'] - 30*config['gheight'] + i*config['block_size'] -125, 25, 25))
            
    pg.draw.rect(surface, (244,171,171), ((config['swidth'] - config['block_size']*config['gwidth'])//2, config['sheight'] - config['block_size']*config['gheight'] -125, config['gwidth']*config['block_size'], config['gheight']*config['block_size']), 10)   #draw rect around playing area   
    draw_grid(surface, grid, config)   
    

def draw_grid(surface, grid, config):
    sx = (config['swidth'] - config['block_size']*config['gwidth'])//2
    sy = config['sheight'] - config['block_size']*config['gheight']
    
    for i in range(config['gheight']):
        pg.draw.line(surface, (242,242,242), (sx, sy + i*config['block_size']-125), (sx + config['gwidth']*config['block_size'], sy + i*config['block_size'] -125))
        for j in range(config['gwidth']):
            pg.draw.line(surface, (242,242,242), (sx + j*config['block_size'], sy -125), (sx + j*config['block_size'], sy + config['gheight']*config['block_size'] -125))


def draw_next_form(tetromino, surface):
    font = pg.font.SysFont('Vintage', 30)
    label = font.render('Next Tetromino', 1, (31,175,191))
    
    sx = ((config['swidth'] - config['block_size']*config['gwidth'])//2 - label.get_width())//2  #set position of next piece display
    sy = 550 #TODO
    
    format = tetromino.form[tetromino.rotation % len(tetromino.form)]
    
    for i,line in enumerate(format): #Form des Tetrominos herausfinden und zeichnen
        line = list(line)
        c = 0
        if tetromino.color in forms_colors[2:4]: #check if tetromino is an I- or O-shape (so if it has an even number of horizontal blocks)
            c = (label.get_width()-4*config['block_size'])//2  #if so, add a variable to center it
        for j, column in enumerate(line):
            if column == '0':
                pg.draw.rect(surface, tetromino.color, (sx + c + j*config['block_size'], sy + i*config['block_size'], config['block_size'] - 5,config['block_size'] - 5), 0)
    surface.blit(label, (sx, sy)) #'Next Tetromino' blitten
    
    
def draw_lvlscore(lvl, score, surface):
    font = pg.font.SysFont('Vintage', 30)
    label = font.render('Score - cleared', 1, (31,175,191))
    label2 = font.render(str(score[0]) + ' - ' + str(score[1]), 1, (31,175,191))
    lvl = font.render('Level - ' + str(lvl), 1, (31,175,191))
    
    sx = config['swidth'] - ((config['swidth'] - config['block_size']*config['gwidth'])//2) #set position of score display
    sy = 550 #TODO

    surface.blit(label, (sx + (config['swidth'] - sx - label.get_width())//2, sy)) #'Score - cleared' blitten
    surface.blit(label2, (sx + (config['swidth'] - sx - label2.get_width())//2, sy + label.get_height())) #Punkte blitten
    surface.blit(lvl, (sx + (config['swidth'] - sx - lvl.get_width())//2, sy - 2*lvl.get_height())) #Lvl blitten




def text_middle(surface, text, size, color, offset = (0,0)):
    font = pg.font.SysFont("Verdana", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, ((config['swidth'] - label.get_width())//2 + offset[0], config['gheight']*config['block_size']//2 + offset[1]))