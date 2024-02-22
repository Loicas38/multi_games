""" module qui gère la mécanique du jeu """

class Puissance_4():
    def __init__(self):
        # tout le plateau est contenu dans une seule liste, plateau de 7*7
        self.plateau = [0 for x in range(42)]
        # on stocke le symbole en cours de vérification pour la condition de victoire
        self.symbole = None
        self.element = None
        # définit à quel joueur c'est de jouer
        self.tour = 0

    def jouer(self, colonne):
        """ permet de jouer et retourne True si le symbole a été placé, False si la colonne est pleine 
        on doit passer la colonne où le joueur veut jouer en argument"""
        for place in range(colonne +35, colonne -1, -7):
            if self.plateau[place] == 0:
                self.plateau[place] = self.tour%2 + 1
                self.tour += 1
                return True, place
        return False, None              


    def verification_match_null(self):
        """ vérifie si le plateau est plein sans vainqueur """
        if self.tour == 42:
            return 3
        else:
            return 0

    def verification_victoire(self, case):
        """
        vérifie s'il y a un vainqueur dans tous les cas possible. Prends en argument la dernière case 
        jouée et retourne le numéro du joueur gagant s'il y en a un, sinon 0
        """
        # définit la ligne et la colonne de la case
        ligne = case // 7
        colonne = case % 7

        # définit le joueur qui a placé le dernier pion
        joueur = self.plateau[case]


        # verif verticale
        # prendra le numéro de la ligne la plus haute contenant un symbole à la suite de celui placé en dernier
        debut_ligne = ligne
        # même chose vers le bas
        fin_ligne = ligne

        # on cherche la ligne la plus haute. On vérfie si la ligne est dans le plateau et si le pion de cette
        # case appartient au joueur ayant placé le dernier. Si oui on continue, sinon on arrête et remet 
        # à la dernière valeur qui fonctionne
        for x in range(3):
            debut_ligne -= 1
            if debut_ligne < 0 or self.plateau[colonne + 7 * debut_ligne] != joueur:
                debut_ligne += 1
                break
        
        # même chose vers le bas
        for x in range(3):
            fin_ligne += 1
            if fin_ligne > 5 or self.plateau[colonne + 7 * fin_ligne] != joueur:
                fin_ligne -= 1
                break

        # on calcul le nombre de pions à la suite 
        suite = fin_ligne - debut_ligne + 1

        # si un joueur a gagné on retourne son numéro
        if suite == 4:
            return joueur
        

        # verif horizontale
        debut_colonne = colonne
        fin_colonne = colonne
        for x in range(3):
            debut_colonne -= 1
            if debut_colonne < 0 or self.plateau[debut_colonne + 7 * ligne] != joueur:
                debut_colonne += 1
                break
        
        for x in range(3):
            fin_colonne += 1
            if fin_colonne > 6 or self.plateau[fin_colonne + 7 * ligne] != joueur:
                fin_colonne -= 1
                break

        suite = fin_colonne - debut_colonne + 1

        if suite == 4:
            return joueur
        

        # verif en diagonal de gauche à droite et de haut en bas 
        debut_ligne, fin_ligne = ligne, ligne
        debut_colonne, fin_colonne = colonne, colonne

        for x in range(3):
            debut_ligne -= 1
            debut_colonne -= 1
            if debut_colonne < 0 or debut_ligne < 0 or self.plateau[debut_colonne + 7 * debut_ligne] != joueur:
                debut_ligne += 1
                debut_colonne += 1
                break

        for x in range(3):
            fin_colonne += 1
            fin_ligne += 1
            if fin_ligne > 5 or fin_colonne > 6 or self.plateau[fin_colonne + 7 * fin_ligne] != joueur:
                fin_colonne -= 1
                fin_ligne -= 1
                break

        suite = fin_colonne - debut_colonne + 1

        if suite == 4:
            return joueur


        # verif diagonale gauche droite de bah en haut
        debut_ligne, fin_ligne = ligne, ligne
        debut_colonne, fin_colonne = colonne, colonne

        for x in range(3):
            debut_colonne -= 1
            debut_ligne += 1
            if debut_ligne > 5 or debut_colonne < 0 or self.plateau[debut_colonne + 7 * debut_ligne] != joueur:
                debut_colonne += 1
                debut_ligne -= 1
                break

        for x in range(3):
            fin_colonne += 1
            fin_ligne -= 1
            if fin_colonne > 6 or fin_ligne < 0 or self.plateau[fin_colonne + 7 * fin_ligne] != joueur:
                fin_colonne -= 1
                fin_ligne += 1

        suite = fin_colonne - debut_colonne + 1

        if suite == 4:
            return joueur
        else:
            return 0