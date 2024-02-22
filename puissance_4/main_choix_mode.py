from puissance_4.interface_graphique import Graphique_choix_mode
import puissance_4.main_IA as main_IA
import puissance_4.main_jcj as main_jcj
import puissance_4.puissance_4_main_terminal as main_terminal

def main_puissance_4():
    choix_mode = Graphique_choix_mode()
    mode = choix_mode.retourner_mode()

    # on appelle la main adaptée au mode de jeu choisi
    if mode == 1:
        main_IA.main()
    elif mode == 2:
        main_jcj.main()
    elif mode == 3:
        main_terminal.main()

if __name__ == "__main__":
    try: 
        main_puissance_4()
    except:
        pass