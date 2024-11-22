
from agent import Agent

class API:
    def __init__(self, game):
        self.game = game
        self.J1 = Agent("random")
        self.J2 = Agent("greedy")


    def play(self):
        environement = self.game.get_environement()

        if environement["turn"] == "BLUE":
            move = self.J1.play(environement)
        else:
            move = self.J2.play(environement)

        self.game.make_move(move)