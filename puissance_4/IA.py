from random import randint
from math import inf

class IA():
    def __init__(self):
        pass


    def cherche_case(self, colonne, plateau):
        for place in range(colonne +35, colonne -1, -7):
            if plateau[place] == 0:
                return place
        return None 

    def eval_score(self, p, case, joueur, compteur):
        """ permet d'attribuer un score à la case testée
        p : prend le plateau en argument, 
        case : la case à tester et joueur : le numéro de l'ordi sur le plateau 
        retourne le score de la case en fonction de ce qu'elle permet """
        if case == None:
            return -100000

        plateau = p.copy()
        plateau[case] = joueur

        # liste des suites
        suite = []

        # définit la ligne et la colonne de la case
        ligne = case // 7
        colonne = case % 7

        debut_colonne = colonne
        fin_colonne = colonne
        for x in range(3):
            debut_colonne -= 1
            if debut_colonne < 0 or plateau[debut_colonne + 7 * ligne] != joueur:
                debut_colonne += 1
                break
        
        for x in range(3):
            fin_colonne += 1
            if fin_colonne > 6 or plateau[fin_colonne + 7 * ligne] != joueur:
                fin_colonne -= 1
                break

        suite_horizontale = fin_colonne - debut_colonne + 1
        suite.append(suite_horizontale)


        debut_ligne = ligne
        fin_ligne = ligne
        for x in range(3):
            debut_ligne -= 1
            if debut_ligne < 0 or plateau[colonne + 7 * debut_ligne] != joueur:
                debut_ligne += 1
                break
        
        for x in range(3):
            fin_ligne += 1
            if fin_ligne > 5 or plateau[colonne + 7 * fin_ligne] != joueur:
                fin_ligne -= 1
                break

        suite_verticale = fin_ligne - debut_ligne + 1
        suite.append(suite_verticale)


        debut_ligne, fin_ligne = ligne, ligne
        debut_colonne, fin_colonne = colonne, colonne

        for x in range(3):
            debut_ligne -= 1
            debut_colonne -= 1
            if debut_colonne < 0 or debut_ligne < 0 or plateau[debut_colonne + 7 * debut_ligne] != joueur:
                debut_ligne += 1
                debut_colonne += 1
                break

        for x in range(3):
            fin_colonne += 1
            fin_ligne += 1
            if fin_ligne > 5 or fin_colonne > 6 or plateau[fin_colonne + 7 * fin_ligne] != joueur:
                fin_colonne -= 1
                fin_ligne -= 1
                break

        suite_diagonale_hb_gd = fin_colonne - debut_colonne + 1
        suite.append(suite_diagonale_hb_gd)


        debut_ligne, fin_ligne = ligne, ligne
        debut_colonne, fin_colonne = colonne, colonne

        for x in range(3):
            debut_colonne -= 1
            debut_ligne += 1
            if debut_ligne > 5 or debut_colonne < 0 or plateau[debut_colonne + 7 * debut_ligne] != joueur:
                debut_colonne += 1
                debut_ligne -= 1
                break

        for x in range(3):
            fin_colonne += 1
            fin_ligne -= 1
            if fin_colonne > 6 or fin_ligne < 0 or plateau[fin_colonne + 7 * fin_ligne] != joueur:
                fin_colonne -= 1
                fin_ligne += 1

        suite_diagonale_bh_dg = fin_colonne - debut_colonne + 1
        suite.append(suite_diagonale_bh_dg)

        # on calcul le score que rapporte ette case si on place le pion ici
        # (le score est défini par moi-même et c'est peut-être pas le meilleur)
        score = 0
        for nombre in suite:
            if nombre == 4:
                score = 1000000
                break
            else:
                score += nombre

        if compteur == 0:
            # on ajoute au score le score que pourrait réaliser l'adversaire, car ce sont des possibilités évitées.
            score += self.eval_score(p, case, joueur%2+1, compteur+1)
        return score


    def recursion(self, plateau, profondeur, joueur):
        """ prend en argument le plateau actuel et retourne la colonne où l'ordi veut jouer """
        # permet de ne pas répéter indéfiniement la fonction eval score qui s'appelle toute seule indéfiniement sinon
        compteur = 0
        score = [0 for x in range(7)]

        # test des 7 colonnes 
        for x in range(7):
            # on cherche où le pion sera mis si on joue cette colonne, case la plus basse libre dans
            # la colonne. On reçoit le numéro de la case si libre, sinon none si colonne pleine
            case = self.cherche_case(x, plateau)

            score[x] = self.eval_score(plateau, case, joueur, compteur)

            if profondeur != 0:
                if joueur == 1:
                    score[x] -= self.recursion(plateau, profondeur-1, joueur%2+1)[0]
                else:
                    score[x] += self.recursion(plateau, profondeur-1, joueur%2+1)[0]

        return sum(score), score.index(max(score))