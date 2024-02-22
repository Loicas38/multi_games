from random import choice
import pickle
import os

class Jeu2048:
    def __init__(self) -> None:
        self.score_file = "jeu_2048/score"

        if not os.path.exists(self.score_file):
            with open(self.score_file, "wb") as f:
                self.high_score = 0
                self.high_nb = 0
        else:
            try:
                with open(self.score_file, "rb") as f:
                    data = pickle.load(f)
                    self.high_score = data["high_score"]
                    # meilleure tuile obtenue dnas la fiche de score
                    self.high_nb = data["high_number"]
            except:
                self.high_score = 0
                self.high_nb = 0

        self.score = 0
        self.plateau = [0 for x in range(16)]
        for x in range(1):
            self.apparition_chiffre()
        
    def get_score_nb(self) -> int:
        return self.high_score, self.high_nb


    def get_plateau(self) -> list[int]:
        """ return a copy of the game board """
        return self.plateau.copy()

    def affichage(self):
        count = 0
        for elt in self.plateau:
            count += 1
            if elt == 0:
                affiche = '.'
            else:
                affiche = elt
            print(affiche, end = "     ")
            if count == 4:
                print('\n\n')
                count = 0
        print('\n\n\n\n')

    def apparition_chiffre(self):
        """ generate a new number at the beginning of a new turn  """
        case = self.place_choice()
        if case != None:
            self.plateau[case] = self.number_choice()

    def cases_vides(self):
        """ return the number of empty squares """
        cases_vides = []
        for id, elt in enumerate(self.plateau):
            if elt == 0:
                cases_vides.append(id)

        return cases_vides
    
    def place_choice(self) -> int:
        """ return a square randomly chosen among the free if there is one, None otherwise """
        liste = self.cases_vides()
        if len(liste) == 0:
            return None
        else:
            return choice(liste)

    def number_choice(self, coef2: int = 7, coef4: int = 3) -> int:
        """
        coef 2 = the probability to have a 2 among 10
        coef4 = the probability to have a 4 among 10
        return the number on the square which has to be had """
        # we create a list in which will be chosen the number of the new square
        liste = [2 for x in range(coef2)] + [4 for x in range(coef4)]

        return choice(liste)
    
    def fusion(self, id1: int, id2: int, sens: str) -> None:
        """
        id1 = id of the first square
        id2 = id of the second square
        sens = way of the fusion d = rught, g = left, h = up, b = down
        make the fusion between the two squares if it's possible """

        # check if the two elements are the same
        if self.plateau[id1] == self.plateau[id2] and self.plateau[id1] != 0:
            # dans le cas où on va 'dans le sens des indices' on met l'addition 
            # dans la bonne case et l'autre à 0, puis invrsement pour l'autre cas

            if sens == 'h' or sens == 'g':
                self.score += self.plateau[id1] * 2
                self.plateau[id1] = self.plateau[id1] * 2
                self.plateau[id2] = 0
            elif sens == 'd' or sens == 'b':
                self.score += self.plateau[id2] * 2
                self.plateau[id2] = self.plateau[id2] * 2 
                self.plateau[id1] = 0

    def get_score(self) -> int:
        """ return the score in a int """
        return self.score

    def deplacement_haut(self):
        """ make a deplacement upward """

        # déplace tout en haut
        for colonne in range(4):
            nb_0 = 0
            for id_elt in range(colonne, 16, 4):
                if self.plateau[id_elt] ==0:
                    nb_0 += 1
                else:
                    if nb_0 != 0:
                        self.plateau[id_elt-4*nb_0] = self.plateau[id_elt]
                        self.plateau[id_elt] = 0

    def deplacement_bas(self):
        """ make a deplacement downward """
        # déplace tout en bas
        for colonne in range(4):
            nb_0 = 0
            for id_elt in range(15-colonne, -1, -4):
                if self.plateau[id_elt] == 0:
                    nb_0 += 1
                else:
                    if nb_0 != 0:
                        self.plateau[id_elt+4*nb_0] = self.plateau[id_elt]
                        self.plateau[id_elt] = 0

    def deplacement_droite(self):
        """ make the deplacement to the right without fusioning the squares """
        for ligne in range(0, 13, 4):
            nb_0 = 0
            for id_elt in range(ligne + 3, ligne-1, -1):
                if self.plateau[id_elt] == 0:
                    nb_0 += 1
                else:
                    if nb_0 != 0:
                        self.plateau[id_elt + nb_0] = self.plateau[id_elt]
                        self.plateau[id_elt] = 0

    def deplacement_gauche(self):
        """ send everything to the left without fusioning the sqquares """
        for ligne in range(0, 13, 4):
            nb_0 = 0
            for id_elt in range(ligne, ligne+4):
                if self.plateau[id_elt] == 0:
                    nb_0 += 1
                else:
                    if nb_0 != 0:
                        self.plateau[id_elt - nb_0] = self.plateau[id_elt]
                        self.plateau[id_elt] = 0

    def deplacement(self, direction: str) -> None:
        """ direction = direction of the deplacement : r = right, l = left, u = up, d = down"""
        if direction == 'u':
            self.deplacement_haut()

            # make the fusions
            for colonne in range(4):
                for id_elt in range(colonne+4, 16, 4):
                    self.fusion(id_elt-4, id_elt, 'h')

            self.deplacement_haut()

        elif direction == 'd':
            self.deplacement_bas()

            # the same
            for colonne in range(12, 16):
                for id_elt in range(colonne, colonne%4, -4):
                    self.fusion(id_elt-4, id_elt, 'b')

            self.deplacement_bas()


        elif direction == 'r':
            self.deplacement_droite()

            for ligne in range(0, 13, 4):
                for id_elt in range(ligne + 3, ligne, -1):
                    self.fusion(id_elt-1, id_elt, 'd')

            self.deplacement_droite()


        elif direction == 'l':
            self.deplacement_gauche()

            for ligne in range(0, 13, 4):
                for id_elt in range(ligne, ligne+3):
                    self.fusion(id_elt, id_elt+1, 'g')

            self.deplacement_gauche()

    def defaite(self) -> bool:
        """ check if a player wone : true if lost, false if not """
        if not 0 in self.plateau:
            # copy of the board to avoir changing it
            plateau_temp = self.plateau.copy()
            # try all directions
            for x in ['b', 'g', 'h', 'd']:
                self.deplacement(x)
            
            if not 0 in self.plateau:
                self.plateau = plateau_temp

                data = {"high_score":self.high_score, "high_number":self.high_nb}
                if self.score > self.high_score:
                    data["high_score"] = self.score
                if self.high_nb < max(self.plateau):
                    data['high_number'] = max(self.plateau)
                    
                with open(self.score_file, "wb") as f:
                    pickle.dump(data, f)

                return True
            else:
                self.plateau = plateau_temp
                return False

    def victoire(self) -> bool:
        """ check if the player wone by looking if 2048 is on the playing board """
        if 2048 in self.plateau:
            return True
        else:
            return False


if __name__ == "__main__":
    jeu = Jeu2048()
    jeu.defaite()



    """plateau_avant = 0
    plateau_apres = 1
    while True:
        # ne fait apparaitre un chiffre que si deplacement effectué
        if plateau_apres != plateau_avant:
            jeu.apparition_chiffre()
        jeu.affichage()

        direction = input("quele direction (b, d, h, g) ? ")

        plateau_avant = jeu.get_plateau()
        jeu.deplacement(direction)
        plateau_apres = jeu.get_plateau()

        if plateau_avant == plateau_apres:
            print("deplacement impossible ! ")
        
        perdu = jeu.defaite()
        if perdu:
            print("vous avez perdu !")
            break

        gagne = jeu.victoire()
        if gagne:
            print("tu as gagné !")
            break
    
    jeu.affiche()"""