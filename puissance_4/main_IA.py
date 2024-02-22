"""
module qui gère les appels de fonction pour faire tourner le jeu
"""
import puissance_4.interface_graphique as interface_graphique
import puissance_4.conditions as conditions
import puissance_4.IA as IA


def main():
    jouer = True
    while jouer:
        # on vient créer nos objets et appeler les fonction qui dessinent le plateau 
        # et font apparaître les boutons pour jouer
        jeu = conditions.Puissance_4()
        plateau = interface_graphique.Graphique_jeu()
        ordi = IA.IA()

        gagnant = 0

        while True:        
            pion_placer = False
            while not pion_placer:
                plateau.fenetre.mainloop()            
                # permet de jouer tant qu'il n'y a pas de vainqueur
                # la première ligne permet d'obtenir la colonne jouée quand le joueur à cliquer sur un bouton
                # ( il n'y a pas besoin d'attente car la mainloop empêche la ligne de s'exécuter tant qu'elle tourne, et elle ne 
                # s'arrête que quand le joueur clique sur un bouton)
                colonne = plateau.retourner_colonne()
                
                # on passe la colonne choisie, et on ressoit True si il y avait de la place et sinon False
                # permet aussi de mettre la case choisi dans le plateau de la class Puissance_4
                pion_placer, case = jeu.jouer(colonne)

            # vérifie si le symbole a pu être placé, et si c'est la cas on va dessiner le symbole
            # on passe en argument la case et le tour de jeu pour avoir la couleur à mettre
            plateau.afficher_symbole(case, jeu.tour%2, 1)

            # on définit le temps après lequel la mainloop doit appeler la fonction stop mainloop qui va 
            # arrêter la mainloop. Permet que celle-ci s'arrête sans évènement de l'utilisateur, et va donc 
            # permettre d'afficher le pion du joueur puis de faire jouer l'ordi sans intervention du joueur
            plateau.fenetre.after(1, plateau.stop_mainloop)
            plateau.fenetre.mainloop()

            # on vérifie ensuite s'il y a match nul (on retourne 3, sinon 0) puis s'il y a un vainqueur.
            # si c'est la cas on retourne le numéro du vaniqueur, sinon 0
            gagnant = jeu.verification_match_null()
            if gagnant == 0:
                gagnant = jeu.verification_victoire(case)
            if gagnant != 0:
                break

            pion_placer = False
            while not pion_placer:
                colonne = ordi.recursion(jeu.plateau, 3, 2)[1]
                pion_placer, case = jeu.jouer(colonne)
            plateau.afficher_symbole(case, jeu.tour%2, 2)
            gagnant = jeu.verification_match_null()
            if gagnant == 0:
                gagnant = jeu.verification_victoire(case)

            if gagnant != 0:
                break

        if gagnant == 1 or gagnant == 2:
            # on vient appeler la fonction pour montrer le gagnant
            plateau.gagner(gagnant)

            # on demande aux joueur s'ils veulent rejouer, et on relance si oui, on arrête sinon
            plateau.continuer_jouer()
            jouer = plateau.retourner_rejouer()

        elif gagnant == 3:
            plateau.cacher()
            jouer = plateau.continuer_jouer()


if __name__ == "__main__":
    main()