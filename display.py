import model
import pygame
from pygame.locals import *
from PIL import Image
import numpy as np


pygame.init()

black=(0,0,0)
white=(255,255,255)

class Images():
    def __init__(self,x,y,name_file):
        self._x=x
        

class Rectangle():
    def __init__(self, x, y, width, height, color, text, text_color, font):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color = color 
        self._text = text
        self._text_color=text_color
        self._font = font
        
    def display(self, window):
        #Object text
        object_text = pygame.font.Font.render(self._font,self._text,True,self._text_color)
        text_ini_width,text_ini_height=object_text.get_size()
        
        #Resize object text
        coef=min((self._width-(self._height/2))/text_ini_width,(self._height-(self._height/2))/text_ini_height)
        text_width=coef*text_ini_width
        text_height=coef*text_ini_height
        object_text = pygame.transform.scale(object_text,(text_width,text_height))
        
        #Display
        button = pygame.Rect(self._x-(self._width/2), self._y-(self._height/2), self._width, self._height)
        pygame.draw.rect(window, self._color, button)
        text_rect = object_text.get_rect(center=(self._x, self._y))
        window.blit(object_text, text_rect)
        
    def set_text(self,new_text):
        self._text=new_text




class Button(Rectangle):
    def __init__(self, x, y, width, height, color, text, text_color, font, cover_color):
        super().__init__(x, y, width, height, color, text, text_color, font)
        self._cover_color = cover_color
    
    # def __init__(self, x, y, width, height, color, text, text_color, font):
    #     super().__init(x, y, width, height, color, text, text_color, font)
    #     self._cover_color = self._color
        
    def covered(self, event): #true si couvert false sinon
        if event.type == MOUSEMOTION:
            if event.pos[0]<(self._x+(self._width/2)) and event.pos[0]>self._x-(self._width/2) and event.pos[1]>self._y-(self._height/2) and event.pos[1]<(self._y+(self._height/2)) :
                return True
        return False
    
    def display(self, window, event):
        if self.covered(event):
            temp_color=self._color
            self._color=self._cover_color
            super().display(window)
            self._color=temp_color
            
        else :
            super().display(window)
        
    def click(self, event): #true si click false sinon
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[0]<(self._x+(self._width/2)) and event.pos[0]>self._x-(self._width/2) and event.pos[1]>self._y-(self._height/2) and event.pos[1]<(self._y+(self._height/2)) :
                    return True
        return False
    
    

class disp_cards():
    def __init__(self, card, x, y, width, height):
        self._x = x
        self._y = y
        self._card = card
        col=card.color()
        r=card.rank()
        noun_file=str(r)+"_"+col+".png"
        self._im_card = pygame.image.load(noun_file).convert_alpha()
      
    
    def resize(self, new_width, new_height):
        self._im_card = pygame.transform.scale(self._im_card, (new_width, new_height))
        
    def repos(self, new_x, new_y):
        self._x=new_x
        self._y=new_y

    def display(self, window):
        window.blit(self._im_card, (self._x, self._y))


#Ecran d'acceuil

#chargement image fond pour recuperer la taille
im_fond = Image.open('fond_vert.jpg')
fond_width,fond_height=im_fond.size

#Ouverture de la fenêtre Pygame
window_width=1000
prop_fond=window_width/fond_width
window_height=int(prop_fond*fond_height)
window = pygame.display.set_mode((window_width,window_height))
window.fill(white)





######## PREMIERE PAGE ###############

Rect_page_nb_joueurs=[]

### TITRE ###
title_blackjack_font = pygame.font.Font(pygame.font.get_default_font(), 36)
title_blackjack=Rectangle(window_width/2,window_height/5,window_width/2,window_height/6,black,"BlackJack",white,title_blackjack_font)
Rect_page_nb_joueurs+=[title_blackjack]

### QUESTION ###
question_font = pygame.font.Font(pygame.font.get_default_font(), 36)
question = Rectangle(window_width/2,2*window_height/5,window_width/3,window_height/6,white,"Nombre de joueurs :",black,question_font)
Rect_page_nb_joueurs+=[question]

### NB JOUEURS ###
buttons_nb_players_font = pygame.font.Font(pygame.font.get_default_font(), 36)
buttons_nb_player_size=int(window_width//9)
buttons_nb_players_color=(200,200,200)
buttons_nb_players_cover_color=(100,100,100)
buttons_nb_players=np.empty((6),dtype=Button)

for k in range (3):
    x=(5/2)*buttons_nb_player_size+(2*k*buttons_nb_player_size)
    y1=int(3*window_height/5)
    y2=int(4*window_height/5)
    buttons_nb_players[k]=Button(x, y1, buttons_nb_player_size, buttons_nb_player_size, buttons_nb_players_color,  str(k+1), black, buttons_nb_players_font, buttons_nb_players_cover_color)
    buttons_nb_players[k+3]=Button(x, y2, buttons_nb_player_size, buttons_nb_player_size, buttons_nb_players_color, str(k+4), black, buttons_nb_players_font, buttons_nb_players_cover_color)




################ DEUXIEME PAGE ###############
red=(255,0,0)
black_red=(200,0,0)

grey=(200,200,200)
black_grey=(100,100,100)
font = pygame.font.Font(pygame.font.get_default_font(), 36)

Rect_page_nom_joueur=[]
Butt_page_nom_joueur=[]

button_retour = Button(window_width/10, window_height/14, window_width/10, window_height/14, red, "RETOUR", black, font, black_red)
button_IA = Button(window_width*(1/2-1/9), window_height/2, window_width/8, window_height/12, grey, "IA", black, font, black_grey)
button_humain = Button(window_width*(1/2+1/9), window_height/2, window_width/8, window_height/12, grey, "HUMAIN", black, font, black_grey)

Butt_page_nom_joueur+=[button_retour,button_IA, button_humain]




rect_num_joueur = Rectangle(window_width/2,window_height/4,window_width/3,window_height/10,white,"Joueur k",black,font)
rect_nom_joueur = Rectangle(window_width/2,3*window_height/4,window_width/3,window_height/10,grey," ",black,font)

Rect_page_nom_joueur+=[rect_num_joueur]
# button_type_joueur = Button(x, y2, buttons_nb_player_size, buttons_nb_player_size, buttons_nb_players_color, str(k+4), black, buttons_nb_players_font, buttons_nb_players_cover_color)





################# PLAY #################
window_open=True
page_nb_joueurs=True
page_nom_joueur=False
type_joueur=-1
page_jeu=False
while window_open :
    pygame.display.flip()
    for event in pygame.event.get():
        if page_nb_joueurs:
            for elem in Rect_page_nb_joueurs:
                elem.display(window)
            for k in range (len(buttons_nb_players)) :
                buttons_nb_players[k].display(window,event)
                if buttons_nb_players[k].click(event):
                    nb_players=k+1
                    print(nb_players)
                    page_nb_joueurs=False
                    page_nom_joueur=True
                    window.fill(white)
                    user_text = " "
                    i=0
                    Joueurs=[[] for j in range (nb_players)]
                    break
            pygame.display.flip()
        
        elif page_nom_joueur:
            if i==nb_players:
                print(Joueurs)
                print(i)
                page_nom_joueur=False
                page_jeu=True
                print(page_nom_joueur)
                print(page_jeu)
            else:
                window.fill(white)
                rect_num_joueur.set_text("Joueur "+str(i+1))
                for elem in Rect_page_nom_joueur:
                    elem.display(window)
                for elem in Butt_page_nom_joueur:
                    elem.display(window,event)
                
                if button_humain.click(event):
                    type_joueur=1
                elif button_IA.click(event):
                    type_joueur=0
                    Joueurs[i]=[0]
                    i+=1
                    print(i)
                    type_joueur=-1
                elif type_joueur==1:
                    rect_nom_joueur.display(window)
                    if event.type == pygame.KEYDOWN:
                        # Check for backspace
                        if event.key == pygame.K_BACKSPACE:
                            # get text input from 0 to -1 i.e. end.
                            if len(user_text)==1:
                                user_text=" "
                            else :
                                user_text = user_text[:-1]
                        elif event.key==pygame.K_RETURN:
                            Joueurs[i]=[1,user_text]
                            i+=1
                            print(i)
                            type_joueur=-1
                            user_text=" "
                        # Unicode standard is used for string formation
                        else:
                            user_text += event.unicode
                        rect_nom_joueur.set_text(user_text)
                elif button_retour.click(event):
                    if i==0:
                        page_nb_joueurs=True
                        page_nom_joueur=False
                        window.fill(white)
                    else :
                        i-=1   
                
                
                pygame.display.flip()
            
        elif page_jeu:
            window.fill(white)
            pygame.display.flip() 
            
        if event.type == QUIT:
            page_nb_joueurs = False
            pygame.quit()
            window_open=False











#pygame.quit()

