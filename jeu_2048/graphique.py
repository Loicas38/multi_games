import tkinter
from functools import partial

class Graphique():
    def __init__(self, high_score, high_nb) -> None:

        self.couleurs = {2:"white", 4:"grey87", 8:"coral", 16:"coral1", 32:"IndianRed1",
                        64: "firebrick3", 128: "#fff633", 256: "#ffe333", 512: "#ffce33", 
                        1024: "#ffc133", 2048: "#ffaf33", 4096: "#ff6433", 8192:"#ff4233",
                        16384: "#33ceff" }

        # we create the canvas
        self.fenetre = tkinter.Tk()
        self.fenetre.title("2048")
        # prevent window resize
        self.fenetre.resizable(0, 0)
        # send the window to the front
        self.fenetre.wm_attributes("-topmost", 1)
        self.canvas = tkinter.Canvas(self.fenetre, height = 850, width = 850, bg="white")
        self.canvas.pack()

        self.grille()
        self.create_numbers(high_score, high_nb)

    def grille(self):
        """crée la grille"""
        self.canvas.create_rectangle(100, 180, 700, 780, fill = 'grey66', outline="")

        x1 = 120
        y1 = 200
        x2 = 237
        y2 = 317

        # info des rectangles
        self.rectangles = {}
        count = 0
        for colonne in range(4):
            for ligne in range(4):
                x10 = x1 + 147 * ligne
                y10 = y1 + 147*colonne
                x20 = x2+ 147* ligne
                y20 = y2 + 147*colonne

                rectangle = self.canvas.create_rectangle(x10,y10 ,x20 ,y20 , fill = 'grey91', outline="")
                self.rectangles[count] = {'id': rectangle, 
                                          "x1": x10, 'x2': x20, 
                                          'y1': y10, 'y2': y20, 
                                          "x_milieu": (x10+x20)/2, "y_milieu": (y10+y20)/2,
                                          "chiffre": None}
                
                count += 1

    def create_numbers(self, high_score, high_nb):
        self.numbers = {}
        for id in range(16):
            self.numbers[id] = self.canvas.create_text(self.rectangles[id]["x_milieu"], 
                                    self.rectangles[id]["y_milieu"], 
                                    text = 0,
                                    font = ("Arial", 30),
                                    state = 'hidden')
            
        self.score = self.canvas.create_text(160, 160, text = "score : 0", font = ("Helvetica", 20))
        self.canvas.create_text(600, 160, text = f"high score : {high_score}", font = ("Helvetica", 20))
        self.canvas.create_text(600, 120, text=f"meilleure tuile : {high_nb}", font = ("Helvetica", 20))

    def affiche_plateau(self, tray: 'list[int]', score: int = None) -> None:
        """ displays the tray in a tkinter window 
        tray = tray of the game 
        score = score of the game, if any score is given, it will be written "not calculated" """

        #print(tray)
        for id, elt in enumerate(tray):
            if elt != 0:
                self.canvas.itemconfigure(self.rectangles[id]['id'], fill=self.couleurs[elt])
                self.canvas.itemconfigure(self.numbers[id], text = elt, state = 'normal')
            if elt == 0:
                self.canvas.itemconfigure(self.rectangles[id]['id'], fill='grey91')
                self.canvas.itemconfigure(self.numbers[id], text = elt, state = 'hidden')
        
        if score == None:
            self.canvas.itemconfigure(self.score, text = "score : not calculated")
        else:
            self.canvas.itemconfigure(self.score, text = f"score : {score}")

    def get_mouvement(self) -> str:
        """ return the deplacement that has been chosen by the user, with a letter 
        b = down, h = top, d = right, g = left """
        return self.deplacement

    def movement_chose(self, direction, _) -> None:
        """ only call by the class, it's to stock the chosen direction and stop the mainloop """
        self.fenetre.quit()
        self.deplacement = direction
        
    def mouvements(self):
        """ call to wait the movement of the player.
        when a direction has been chosen, the mainloop ends and 
        the fonction get_mouvement can be call to get the movement chose """
        self.canvas.bind_all("<Down>", partial(self.movement_chose, 'd'))
        self.canvas.bind_all("<Up>", partial(self.movement_chose, 'u'))
        self.canvas.bind_all("<Left>", partial(self.movement_chose, 'l'))
        self.canvas.bind_all("<Right>", partial(self.movement_chose, 'r'))
        self.fenetre.mainloop()

    def victory(self, win: bool) -> None:
        """ win is a boolean which mean if the player won or not: 
        True = victory, 
        False = lose
        It's a fonction to call when the party is over, and which makes the end of the game """

        if win:
            self.end_game_text = self.canvas.create_text(430, 70, text = "Congratulations, you win !", font=('Tekton Pro', 50, 'italic'), fill = '#FFC700')
        else:
            self.end_game_text = self.canvas.create_text(430, 50, text = "You lose, try again !", font=('Tekton Pro', 50, 'italic'), fill = '#FF3232')
        
        self.canvas.bind_all("<Down>", partial(self.new_game, True))
        self.canvas.bind_all("<Up>", partial(self.new_game, True))
        self.canvas.bind_all("<Left>", partial(self.new_game, True))
        self.canvas.bind_all("<Right>", partial(self.new_game, True))
        self.canvas.bind_all("<Return>", partial(self.new_game, False))

        self. play_again_text = self.canvas.create_text(430, 110, text = "to continue playing, press an arrow, to stop playing press enter", font = ("Helvetica", 20))    
        self.fenetre.mainloop()

    def new_game(self, play, _) -> None:
        """ call by the class when the player lost and decided to play again or not """
        self.fenetre.quit()
        if play:
            self.play = True
            self.canvas.itemconfigure(self.play_again_text, state = 'hidden')
            self.canvas.itemconfigure(self.end_game_text, state = 'hidden')
        else:
            self.play = False

    def get_play_again(self):
        """ fonction to call at the end of the game, when the player lost and when he made the choice to play again or not 
        return True if the player wants to play a new game, False if he wants to stop playing """
        return self.play




if __name__ == "__main__":
    a = Graphique()
    a.affiche_plateau([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384])
    a.fenetre.mainloop()
