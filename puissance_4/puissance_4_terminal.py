class Terminal():
    def __init__(self):
        self.symboles = ["X", "O"]

    def afficher(self, plateau):
        """ permet d'afficher le plateau mis en forme """
        # on affiche une lettre par colonne pour les indices des cases pour jouer
        print()
        for place in range(1, 8):
            print(place, end =" ")
        print("\n", end="")

        # on affiche maintenant le plateau avec les jetons de chaque joueur, et on retourne à la ligne tous les 7 éléments
        # on affiche aussi la nombre de chaque ligne
        for indice, element in enumerate(plateau):
            # on fait correspondre l'élément du plateau à un symbole
            if element == 0:
                symbole = "-"
            elif element == 1:
                symbole = self.symboles[element - 1]
            elif element == 2:
                symbole = self.symboles[element - 1]
            # pour retourner à la ligne :
            if indice % 7 == 6:
                print(symbole)
            # dans un cas "normal"
            else:
                print(symbole, end = " ")


    def choisir_ligne(self, tour):
        """ permet à l'utilisateur de choisir la ligne où il veut jouer, et gère les problèmes de valeur 
        retourne False si la valeur est invalide et la colonne où placer le symbole si la valeur est valide"""
        # on demande une colonne au joueur, et il doit entrer un nombre entre 1 et 7 (le nombre de colonnes)
        # si la valeur entrée n'est pas un nombre ou n'est pas comprise dans l'intervalle, on lève une exception
        case = None
        case = input(f"c'est le tour du joueur {(tour % 2) + 1}, symbole {self.symboles[tour % 2]}, quell colonne ? ")
        try :
            case = int(case)
            if case < 1 or case > 7:
                raise ValueError
            # on fait "correspondre" le numéro entré à notre liste ( même s'il faudra multiplier, du fait de la liste unique)
            case -= 1
            return case
        except ValueError:
            case = None
            print("\nValeur invalide")
            case = self.choisir_ligne(tour)
            return case
        except:
            print("oups, une erreur c'est produite (problème dans le programme)")
    