import os, pygame, sys
from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

# Initialize screen
pygame.init()
DISPLAYSURF = pygame.display.set_mode((1000, 800),RESIZABLE)
pygame.display.set_caption('Match Point')

size = DISPLAYSURF.get_size()
width = size[0]
height = size[1]

title = pygame.Rect(((width/16)+1, (height/8)+1, 7*width/8, height/4))
menu1 = pygame.Rect(((width/4)+1, (height/2)+1, 2*width/4, height/10))
menu2 = pygame.Rect(((width/4)+1, (height/2)+1+(3*height/20), 2*width/4, height/10))
menu3 = pygame.Rect(((width/4)+1, (height/2)+1+(6*height/20), 2*width/4, height/10))

#Draws dark blue rectangles.
pygame.draw.rect(DISPLAYSURF, (0,0,150), menu1)
pygame.draw.rect(DISPLAYSURF, (0,0,150), menu2)
pygame.draw.rect(DISPLAYSURF, (0,0,150), menu3)

#Draws blue ovals on top of the rectangles.
pygame.draw.ellipse(DISPLAYSURF, (0,0,150), title)
pygame.draw.ellipse(DISPLAYSURF, (0,0,255), menu1)
pygame.draw.ellipse(DISPLAYSURF, (0,0,255), menu2)
pygame.draw.ellipse(DISPLAYSURF, (0,0,255), menu3)

#pygame.font.Font takes in a font name and an integer for its size.
#Free Sans Bold comes with Pygame (Sweigart 2012 p. 30).
font_title = pygame.font.Font('freesansbold.ttf', 64)
font_menu = pygame.font.Font('freesansbold.ttf', 32)

#Creates and draws the text.
surface_title = font_title.render('Match Point', True, (0,255,0))
rect_title = surface_title.get_rect() #get_rect() is my favorite Pygame function.
rect_title.center = (width/2,(height/4)+3)
surface_new_game = font_menu.render('Start Game', True, (0,0,0))
rect_new_game = surface_new_game.get_rect()
rect_new_game.center = (width/2,(height/2)+(height/20)+3)
surface_load_game = font_menu.render('Score Time', True, (0,0,0))
rect_load_game = surface_load_game.get_rect()
rect_load_game.center = (width/2,(height/2)+(4*height/20)+3)
surface_exit = font_menu.render('EXIT', True, (0,0,0))
rect_exit = surface_exit.get_rect()
rect_exit.center = (width/2,(height/2)+(7*height/20)+3)

while True: #main game loop
    DISPLAYSURF.blit(surface_title, rect_title)
    DISPLAYSURF.blit(surface_new_game, rect_new_game)
    DISPLAYSURF.blit(surface_load_game, rect_load_game)
    DISPLAYSURF.blit(surface_exit, rect_exit)
    for event in pygame.event.get():
        if event.type == VIDEORESIZE:
            #This line creates a new display in order to clear the screen.
          
            DISPLAYSURF = pygame.display.set_mode((event.w, event.h),RESIZABLE)

            width = event.w
            height = event.h

            #Creates the rectangle objects that will be behind the title and menu buttons.
            title = pygame.Rect(((width/16)+1, (height/8)+1, 7*width/8, height/4))
            menu1 = pygame.Rect(((width/4)+1, (height/2)+1, 2*width/4, height/10))
            menu2 = pygame.Rect(((width/4)+1, (height/2)+1+(3*height/20), 2*width/4, height/10))
            menu3 = pygame.Rect(((width/4)+1, (height/2)+1+(6*height/20), 2*width/4, height/10))

            #Draws dark blue rectangles.
            pygame.draw.rect(DISPLAYSURF, (0,0,150), menu1)
            pygame.draw.rect(DISPLAYSURF, (0,0,150), menu2)
            pygame.draw.rect(DISPLAYSURF, (0,0,150), menu3)

            #Draws blue ovals on top of the rectangles.
            pygame.draw.ellipse(DISPLAYSURF, (0,0,150), title)
            pygame.draw.ellipse(DISPLAYSURF, (0,0,255), menu1)
            pygame.draw.ellipse(DISPLAYSURF, (0,0,255), menu2)
            pygame.draw.ellipse(DISPLAYSURF, (0,0,255), menu3)

            #Creates and draws the text.
            rect_title = surface_title.get_rect()
            rect_title.center = (width/2,(height/4)+3)
            rect_new_game = surface_new_game.get_rect()
            rect_new_game.center = (width/2,(height/2)+(height/20)+3)
            rect_load_game = surface_load_game.get_rect()
            rect_load_game.center = (width/2,(height/2)+(4*height/20)+3)
            rect_exit = surface_exit.get_rect()
            rect_exit.center = (width/2,(height/2)+(7*height/20)+3)
    
            pygame.display.update() #Necessary to update the screen

        #let go of the left mouse button in the area of a button, the button does something.
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if (menu1.left < event.pos[0] < menu1.right) and (menu1.top < event.pos[1] < menu1.bottom):
                    print("Start Game")
                if (menu2.left < event.pos[0] < menu2.right) and (menu2.top < event.pos[1] < menu2.bottom):
                    print("Score Time") 
                if (menu3.left < event.pos[0] < menu3.right) and (menu3.top < event.pos[1] < menu3.bottom):
                    pygame.event.post(pygame.event.Event(QUIT)) #Exits the game

        #When you mouse-over a button, the text turns green.
        if event.type == MOUSEMOTION:
            if (menu1.left < event.pos[0] < menu1.right) and (menu1.top < event.pos[1] < menu1.bottom):
                surface_new_game = font_menu.render('Start Game', True, (0,255,255))
            else:
                surface_new_game = font_menu.render('Start Game', True, (0,0,0))
            if (menu2.left < event.pos[0] < menu2.right) and (menu2.top < event.pos[1] < menu2.bottom):
                surface_load_game = font_menu.render('Score Time', True, (0,255,0))
            else:
                surface_load_game = font_menu.render('Score Time', True, (0,0,0))
            if (menu3.left < event.pos[0] < menu3.right) and (menu3.top < event.pos[1] < menu3.bottom):
                surface_exit = font_menu.render('EXIT', True, (255,0,0))
            else:
                surface_exit = font_menu.render('EXIT', True, (0,0,0))           

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()