import puissance_4.conditions as conditions
import puissance_4.puissance_4_terminal as puissance_4_terminal

def main():
    continuer_jouer = True
    while continuer_jouer:
        jeu = conditions.Puissance_4()
        terminal = puissance_4_terminal.Terminal()
        gagnant = 0
        jouer = False

        while gagnant == 0:
            terminal.afficher(jeu.plateau)
            while not jouer:
                colonne = terminal.choisir_ligne(jeu.tour)
                jouer, case = jeu.jouer(colonne)
            jouer = False
            gagnant = jeu.verification_victoire(case)
            if gagnant == 0:
                jeu.verification_match_null()

        terminal.afficher(jeu.plateau)
        print()
        print(f"bravo au joueur {gagnant} avec le symbole {terminal.symboles[gagnant-1]} qui a gagné")
        print()

        # permet de demander à l'utilisateur s'il veut rejouer, et de recommencer le pogramme si demandé
        try:
            continuer_jouer = int(input("tapez 1 pour continuer à jouer, sinon ce que vous voulez "))
            if continuer_jouer != 1:
                raise ValueError
            else:
                continuer_jouer = True
        except ValueError:
            continuer_jouer = False
            print()
            print("Merci d'avoir jouer et à bientôt ;)")

if __name__ == "__main__":
    main()