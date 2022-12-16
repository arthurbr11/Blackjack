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
        self._y=y
        self._image=pygame.image.load(name_file).convert_alpha()
    
    def reshape(self,width,height):
        self._image = pygame.transform.scale(self._image, (width,height))
    
    def display(self, window):
        window.blit(self._image, (self._x,self._y))
        

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
im_fond = Image.open('assets/fond_vert.jpg')
fond_width,fond_height=im_fond.size



#Ouverture de la fenêtre Pygame
window_width=1000
prop_fond=window_width/fond_width
fond_width=int(prop_fond*fond_width)
fond_height=int(prop_fond*fond_height)

#dim rect
white_rect_width=fond_width
white_rect_height=white_rect_width/15
white_rect_x=0
white_rect_y=fond_height
white_rect=pygame.Rect(white_rect_x,white_rect_y,white_rect_width,white_rect_height)

window_height=fond_height+white_rect_height
window = pygame.display.set_mode((window_width,window_height))
window.fill(white)


grey=(200,200,200)
black_grey=(100,100,100)
font = pygame.font.Font(pygame.font.get_default_font(), 36)

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
buttons_nb_player_size=int(window_width//9)
buttons_nb_players=np.empty((6),dtype=Button)

for k in range (3):
    x=(5/2)*buttons_nb_player_size+(2*k*buttons_nb_player_size)
    y1=int(3*window_height/5)
    y2=int(4*window_height/5)
    buttons_nb_players[k]=Button(x, y1, buttons_nb_player_size, buttons_nb_player_size, grey,  str(k+1), black, font, black_grey)
    buttons_nb_players[k+3]=Button(x, y2, buttons_nb_player_size, buttons_nb_player_size, grey, str(k+4), black, font, black_grey)




################ DEUXIEME PAGE ###############
red=(255,0,0)
black_red=(200,0,0)



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


################ TROISIEME PAGE #################

#fond
fond=Images(0,0,"assets/fond_vert.jpg")
fond.reshape(fond_width,fond_height)


#dim jeton
taille_jeton=white_rect_height/2
jetons_y=white_rect_y+(white_rect_height/4)
jeton1_x=white_rect_height/2
jeton5_x=white_rect_height*5/4
jeton10_x=white_rect_height*2
jeton25_x=white_rect_height*11/4
jeton100_x=white_rect_height*7/2

#jetons
#1
jeton1 = Images(jeton1_x, jetons_y, "assets/jeton.png")
jeton1.reshape(taille_jeton,taille_jeton)
jeton5 = Images(jeton5_x, jetons_y, "assets/jeton.png")
jeton5.reshape(taille_jeton,taille_jeton)
jeton10 = Images(jeton10_x, jetons_y, "assets/jeton.png")
jeton10.reshape(taille_jeton,taille_jeton)
jeton25 = Images(jeton25_x, jetons_y, "assets/jeton.png")
jeton25.reshape(taille_jeton,taille_jeton)
jeton100 = Images(jeton100_x, jetons_y, "assets/jeton.png")
jeton100.reshape(taille_jeton,taille_jeton)

jetons=[jeton1,jeton5,jeton10,jeton25,jeton100]

#dim boutons
button_width=white_rect_height*(3/2)
button_height=white_rect_height/2
button_y=white_rect_y+white_rect_height/2
button_doubler_x=23*white_rect_height/4
button_rester_x=white_rect_height*15/2
button_tirer_x=white_rect_height*37/4

#boutons
button_doubler=Button(button_doubler_x,button_y,button_width,button_height, grey, "Doubler", black, font, black_grey)
button_rester=Button(button_rester_x,button_y,button_width,button_height, grey, "Rester", black, font, black_grey)
button_tirer=Button(button_tirer_x,button_y,button_width,button_height, grey, "Tirer", black, font, black_grey)
Butt_page_jeu=[button_doubler,button_rester,button_tirer]

#dim argent
rect_argent_x=25*white_rect_height/2
rect_argent_y=white_rect_y+white_rect_height/2
rect_argent_width=3*white_rect_height
rect_argent_height=white_rect_height/2
rect_argent = Rectangle(rect_argent_x,rect_argent_y,rect_argent_width,rect_argent_height,grey,"Argent : 1000 euros",black,font)

#loading cartes

#dimension
im_carte = Image.open("assets/cartes/1_clubs.png")
carte_ini_width,carte_ini_height=im_carte.size
carte_height=int(window_height/6)
prop_carte=carte_height/carte_ini_height
carte_width=int(prop_carte*carte_ini_width)

rank=1
color="spades"
nom_carte=str(rank)+"_"+str(color)
chemin_acces="assets/cartes/"+nom_carte+".png"
carte_test=Images(0,0,chemin_acces)
carte_test.reshape(carte_width,carte_height)



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
                elem.display(window, )
            for k in range (len(buttons_nb_players)) :
                buttons_nb_players[k].display(window, event)
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
                page_nom_joueur=False
                page_jeu=True
            else:
                window.fill(white)
                rect_num_joueur.set_text("Joueur "+str(i+1))
                for elem in Rect_page_nom_joueur:
                    elem.display(window, )
                for elem in Butt_page_nom_joueur:
                    elem.display(window, event)
                
                if button_humain.click(event):
                    type_joueur=0
                elif button_IA.click(event):
                    type_joueur=1
                    Joueurs[i]=[1]
                    i+=1
                    type_joueur=-1
                elif type_joueur==0:
                    rect_nom_joueur.display(window)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            if len(user_text)==1:
                                user_text=" "
                            else :
                                user_text = user_text[:-1]
                        elif event.key==pygame.K_RETURN:
                            Joueurs[i]=[0,user_text]
                            i+=1
                            type_joueur=-1
                            user_text=" "
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
            fond.display(window)
            carte_test.display(window)
            for jeton in jetons :
                jeton.display(window)
            for butt in Butt_page_jeu :
                butt.display(window,event)
            rect_argent.display(window)
            
            pygame.display.flip() 
            
        if event.type == QUIT:
            page_nb_joueurs = False
            pygame.quit()
            window_open=False











#pygame.quit()

