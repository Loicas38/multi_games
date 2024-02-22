import jeu_2048.graphique as graphique
import jeu_2048.jeu as jeu


def main_2048():
    rejouer = True

    while rejouer:
        mecha = jeu.Jeu2048()
        graph = graphique.Graphique(mecha.get_score_nb()[0], mecha.get_score_nb()[1])


        movement = True
        gagne = False
        while True:
            if movement:
                mecha.apparition_chiffre()

            tray = mecha.get_plateau()
            score = mecha.get_score()
            
            graph.affiche_plateau(tray, score)

            graph.mouvements()

            tray_before = mecha.get_plateau()

            mov = graph.get_mouvement()

            mecha.deplacement(mov)

            movement = tray_before != mecha.get_plateau() 

            if not gagne:
                if mecha.victoire():
                    graph.affiche_plateau(mecha.get_plateau())
                    graph.victory(True)

                    gagne = True
                    rejouer = graph.get_play_again()
                    if not rejouer:
                        break

            if mecha.defaite():
                graph.affiche_plateau(mecha.get_plateau())
                graph.victory(False)
                rejouer = graph.get_play_again()
                graph.fenetre.destroy()
                break

if __name__ == "__main__":
    main_2048()