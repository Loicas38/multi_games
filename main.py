import tkinter 
from functools import partial

from puissance_4.main_choix_mode import main_puissance_4
from jeu_2048.main_2048 import main_2048
from jeu_pendu.main_pendu import choix_jeu

class Main():
    def __init__(self) -> None:
        # on cré le canvas
        self.fenetre = tkinter.Tk()
        self.fenetre.title("game launcher")
        # empêche que l'on puisse redimensionner la fenêtre
        self.fenetre.resizable(0, 0)
        # fait passer la fenêtre à l'avant plan
        self.fenetre.wm_attributes("-topmost", 1)
        self.canvas = tkinter.Canvas(self.fenetre, height = 500, width = 800, bg="white")

        self.canvas.create_text(400, 50, text="choisissez votre jeu", font=("Helvetica", 30))
        self.canvas.pack()

        # stock les boutons de choix de jeu 
        self.boutons_jeux = []
        # liste des jeux
        jeux = ["puissance_4", "pendu", "2048", "mastermind"]
        # coordonées des boutons
        x = 225
        y = 150

        # permet de créer les boutons de sélection de jeu
        for nb, jeu in enumerate(jeux):
            self.creation_bouton(jeu, x, y)
            x += 200
            if nb % 2 == 1:
                y += 100
                x = 225

        self.fenetre.mainloop()

    def creation_bouton(self, jeu, x, y):
        boutton = tkinter.Button(self.fenetre, text = jeu, height=3, width=20, command = partial(self.set_choix_jeu, jeu))
        boutton.pack()
        boutton.place(x=x, y=y)
        self.boutons_jeux.append(boutton)

    def set_choix_jeu(self, jeu):
        self.choix = jeu
        self.fenetre.destroy()

    def get_jeu(self):
        return self.choix


if __name__ == "__main__":
    a = Main()

    b = a.get_jeu()

    if b == "pendu":
        choix_jeu()
    elif b == "puissance_4":
        main_puissance_4()
    elif b == "2048":
        main_2048()
    elif b == "mastermind":
        import mastermind.mastermind_définitif