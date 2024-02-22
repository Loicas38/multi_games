""" 
module qui gère l'interface tkinter du jeu
"""

from tkinter import*
from functools import partial

class Graphique_jeu():
    """ class qui gère l'interface graphique du jeu """
    def __init__(self):
        """ permet d'initialiser l'interface graphique en créant le canvas, réglage des attributs. 
        on crée aussi la grille, le pion au dessu et les rectangles bleus. 
        Activation de la détection des mouvements de la souris et du clic gauche. """
        # on cré le canvas
        self.fenetre = Tk()
        self.fenetre.title("puissance 4")
        # empêche que l'on puisse redimensionner la fenêtre
        self.fenetre.resizable(0, 0)
        # fait passer la fenêtre à l'avant plan
        self.fenetre.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.fenetre, height = 900, width = 900, bg="white")
        self.canvas.pack()

        # création de la grille
        # taille des carrés 
        taille = 110
        # coordonées de départ de la grille, donc du premier carré
        x1 = 50
        y1 = 150
        x2 = x1 + taille
        y2 = y1 + taille

        # stocke tous les éléments créés sur le canvas (ou presque)
        self.id_elements = {"grille":[], "rectangles":[], "pion_attente":None, "pions":[], 
                            "infos_grille":{"taille":taille, "x1":x1, "y1":y1}}

        # création des rectangles bleus, puis on les cache
        for x in range(x1, x1+7*taille, taille):
            id = self.canvas.create_rectangle(x, y1, x + taille, y1+taille*6, fill="#58EAFF")
            self.id_elements["rectangles"].append(id)
            self.canvas.pack()
            self.canvas.itemconfigure(id, state="hidden")
        self.id_elements["rectangles"].append(0)

        # création de la grile 
        for ligne in range(6):
            for colonne in range(7):
                id = self.canvas.create_rectangle(x1, y1, x2, y2)
                self.id_elements["grille"].append(id)
                self.canvas.pack()
                x1 += taille
                x2 += taille
            x1 = self.id_elements["infos_grille"]["x1"]
            y1 += taille
            x2 = self.id_elements["infos_grille"]["x1"]+taille
            y2 += taille

        self.id_elements["pion_attente"] = self.canvas.create_oval(self.id_elements["infos_grille"]["x1"], 20, self.id_elements["infos_grille"]["x1"]+self.id_elements["infos_grille"]["taille"], self.id_elements["infos_grille"]["taille"]+20, fill="yellow")
        self.canvas.pack()

        self.fenetre.bind('<Motion>', self.position_souris)
        self.fenetre.bind('<Button-1>', self.colonne_pion)

    def position_souris(self, position):
        """ permet au pion de suivre le pointeur de souris """
        x_souris = position.x - 50
        # coordonées du pion
        x_pion = self.canvas.coords(self.id_elements["pion_attente"])
        # coordonée x du pion
        x_pion = x_pion[0]
        # déplace le pion de sa place actuelle au pointeur de souris
        self.canvas.move(self.id_elements["pion_attente"], x_souris-x_pion, 0)

        # cache
        self.canvas.itemconfigure(self.id_elements["rectangles"][7], state="hidden")

        # défini la colonne où l'on se trouve
        colonne = (position.x-self.id_elements["infos_grille"]["x1"])//self.id_elements["infos_grille"]["taille"]
        if colonne > 6:
            colonne = 6

        self.id_elements["rectangles"][7] = self.id_elements["rectangles"][colonne]
        # affiche le rectangle de cette colonne
        self.canvas.itemconfigure(self.id_elements["rectangles"][colonne], state = "normal")
    
    def retourner_colonne(self):
        """ retourne la colonne choisie par le joueur """
        return self.colonne

    def stop_mainloop(self):
        """ permet de quitter la mainloop quand appelé """
        self.fenetre.quit()

    def colonne_pion(self, position):
        """ calcule la colonne où l'on a cliqué et si elle est valide met la variable colonne à la colonne choisie """
        # on récupère les coordonées x du clique. On lui enlève la distance entre le bord de la fenêtre et la 
        # première case, puis on divise par la taille d'une case et on obtient la colonne 
        colonne = (position.x-self.id_elements["infos_grille"]["x1"])//self.id_elements["infos_grille"]["taille"]
        # le résultat est plus grand que 6 si cliqué à droite du plateau, on le met donc à 6 pour avoir une colonne
        if colonne > 6:
            colonne = 6
        elif colonne < 0:
            colonne = 0

        # on met la valeur dans une variable où elle pourra être récupérée par une autre fonction et renvoyée
        self.colonne = colonne
        # on arrête la mainloop pour pouvoir venir récupérer la valeur avec la fonction retourner_colonne
        self.fenetre.quit()

    def afficher_symbole(self, case, joueur, type_joueur):
        """ permet d'afficher le symbole joué dans la bonne case
        case = case jouée et où il faut placer le symbole, joueur le numéro du joueur pour la couleur
        et type joueur si c'est l'ordi ou le vrai joueur : 1 = joueur, 2 = ordi"""
        colonne = case%7
        ligne = case//7
        x1 = self.id_elements["infos_grille"]["x1"] + self.id_elements["infos_grille"]["taille"] * colonne
        x2 = x1 + self.id_elements["infos_grille"]["taille"]
        y1 = self.id_elements["infos_grille"]["y1"] + self.id_elements["infos_grille"]["taille"] * ligne
        y2 = y1 + self.id_elements["infos_grille"]["taille"]
        # on définit la couleur du pion à créer et celle du pion en attente (au dessus de la grille)
        if joueur == 0:
            couleur_pion = 'red'
            couleur_attente = 'yellow'
        else:
            couleur_pion = 'yellow'
            couleur_attente = 'red'
        
        # on vérifie si c'est l'ordi ou le joueur qui joue
        if type_joueur == 1:
            # on récupère la position du pion en attente
            position = self.canvas.coords(self.id_elements["pion_attente"])
            # on récupère son abscisse
            x = position[0]
            # on définit l'endroit où l'on veut qu'il aille, CAD au-dessus de la colonne qui vient d'être choisie
            # et au milieu de celle-ci 
            objectif = x2-100
            # correspond au déplacement que le pion va devoir effectuer pour se placer à l'emplacement souhaité.
            x_deplacement = objectif - x


            # on fait bouger le pion pour le placer
            self.canvas.move(self.id_elements["pion_attente"], x_deplacement, 0)

        # on crée le nouveau pion qui vient d'être placé
        id = self.canvas.create_oval(x1-1, y1-1, x2-1, y2-1, fill = couleur_pion)
        # on change la couleur du pion au dessus de la grille
        self.canvas.itemconfigure(self.id_elements["pion_attente"], fill=couleur_attente)
        # on enregiste l'identifiant du pion créé
        self.id_elements["pions"].append(id)
        self.canvas.pack()

    def cacher(self):
        """ cache la grille et les pions"""
        # désactive le suivi du capteur de la souris et son clique
        self.fenetre.unbind('<Motion>')
        self.fenetre.unbind('<Button-1>')

        # cache le pion au dessu de la grille
        self.canvas.itemconfigure(self.id_elements["pion_attente"], state="hidden")

        # cache les pions
        for id in self.id_elements["pions"]:
            self.canvas.itemconfigure(id, state="hidden")

        for id in self.id_elements["grille"]:
            self.canvas.itemconfigure(id, state="hidden")

        # permet de cacher le rectangle bleu 
        self.canvas.itemconfigure(self.id_elements["rectangles"][7], state="hidden")

    def montrer(self):
        """ permet d'afficher la grille et les pions joués, avec un bouton pour retourner sur la fenêtre du gagnant"""
        # affiche les pions
        for id in self.id_elements["pions"]:
            self.canvas.itemconfigure(id, state="normal")

        # affiche la grille
        for id in self.id_elements["grille"]:
            self.canvas.itemconfigure(id, state="normal")

        # cache le pion géant du gagnant et le texte
        self.canvas.itemconfigure(self.pion_gagnant, state = "hidden")
        self.canvas.itemconfigure(self.text_gagnant, state = "hidden")
        # détruit le bouton qui permet de revenir à la partie
        self.bouton_grille.destroy()
        # crée un bouton pour revenir sur la page du gagnant
        self.bouton_gagnant = Button(self.fenetre, height = 3, text = "retourner à la\nfenêtre précédente", command = partial(self.gagner, self.gagnant))
        self.bouton_gagnant.pack()
        self.bouton_gagnant.place(x=20, y=20)

    def gagner(self, joueur):
        """ affiche un pion génant de la couleur du vainqueur ainsi qu'un petit texte"""
        self.gagnant = joueur
        self.cacher()
        # on supprime le bouton permettant de revenir à cette fenêtre et créer dans la fonction
        # montrer. On le détruit s'il a été créer, sinon il ne faut pas d'erreur
        try:
            self.bouton_gagnant.destroy()
        except:
            pass

        # on défini la couleur du joueur gagnant
        if joueur == 2:
            couleur = 'red'
        elif joueur == 1:
            couleur = 'yellow'

        # on crée le pion géant pour le gagnant et le texte de vainqueur
        self.pion_gagnant = self.canvas.create_oval(50, 5, 750, 750, fill = couleur)
        self.text_gagnant = self.canvas.create_text(400, 400, font=('', 60), justify='center', text="bravo au joueur\navec le pion")
        # bouton qui permet de revenir voir le plateau à la fin de la partie
        self.bouton_grille = Button(self.fenetre, width = 15, height = 3, text = "pour revoir la partie,\ncliquez ici", command = self.montrer)
        self.bouton_grille.pack()
        self.bouton_grille.place(x=20, y=20)
        self.canvas.pack()

    def rejouer(self, relancer):
        """ est appelée quand le joueurs clique sur le bouton rejouer, 
        et met donc la variable rejouer à True, pour relancer une partie.
        On détruit aussi la fenêtre actuelle pour ne pas en avoir plusieurs ouvertes par la suite"""
        self.relancer = relancer
        self.fenetre.destroy()

    def retourner_rejouer(self):
        return self.relancer

    def continuer_jouer(self):
        """ est appelé à la fin de la partie pour proposer aux joueurs de rejouer, via deux bouttons"""
        self.continuer_play = Button(self.fenetre, width = 20, height = 3, text="si vous voulez rejouer,\ncliquez sur le bouton", command = partial(self.rejouer, True))
        self.fin = Button(self.fenetre, width = 20, height = 3, text="pour arrêter de jouer,\nc'est ici", command = partial(self.rejouer, False))
        self.continuer_play.pack()
        self.fin.pack()
        self.continuer_play.place(x = 650, y=20)
        self.fin.place(x = 20, y = 780)
        self.canvas.pack()
        self.fenetre.mainloop()
        return self.relancer


class Graphique_choix_mode():
    """ classe qui gère l'interface graphique pour choisir le mode de jeu """
    def __init__(self):
        # on crée le canvas
        self.fenetre = Tk()
        self.fenetre.title("puissance 4")
        # empêche que l'on puisse redimensionner la fenêtre
        self.fenetre.resizable(0, 0)
        # fait passer la fenêtre à l'avant plan
        self.fenetre.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.fenetre, height = 250, width = 400, bg="white")
        self.canvas.pack()

        # création des boutons pour choix du mode de jeu 
        bouton_joueur = Button(self.fenetre, width = 15, heigh = 3, text = "Jouer contre\nquelqu'un", command = self.joueur)
        bouton_joueur.pack()
        bouton_joueur.place (x=50, y=50)
        bouton_ordi = Button(self.fenetre, width = 15, heigh = 3, text = "jouer contre\nl'ordi", command = self.ordi)
        bouton_ordi.pack()
        bouton_ordi.place(x = 250, y = 50)
        self.canvas.pack()
        bouton_ordi = Button(self.fenetre, width = 15, heigh = 3, text = "jouer dans le\nterminal en jcj", command = self.terminal)
        bouton_ordi.pack()
        bouton_ordi.place(x = 150, y = 150)
        self.canvas.pack()
        self.fenetre.mainloop()


    def ordi(self):
        """ est appelé si le joueur veut jouer contre l'ordi """
        self.fenetre.quit()
        self.mode_jeu = 1

    def joueur(self):
        """ est appelé si le joueur veut jouer contre un autre joueur """
        self.fenetre.quit()
        self.mode_jeu = 2
    
    def terminal(self):
        """ est appelé si le joeur veut jouer dans le terminal """
        self.fenetre.quit()
        self.mode_jeu = 3
    
    def retourner_mode(self):
        """ retourne le mode de jeu souhaité et détruit la fenêtre """
        self.fenetre.destroy()
        return self.mode_jeu
    