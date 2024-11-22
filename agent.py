from algo import Algo

class Agent:
    
    def __init__(self,algo_name):
        self.algo_name = algo_name

    def play(self,environement):
        if self.algo_name == "greedy":
            return Algo.glouton(environement)

        if self.algo_name == "random":
            return Algo.random(environement)

        else:
            print("NO ALGO DEFINED")
        


    