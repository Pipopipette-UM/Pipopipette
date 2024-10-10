import random

class Algo:

    @staticmethod
    def random(environement):
        horizontal = random.choice([True,False]) #choix entre ligne horizontal ou vertical

        if horizontal:
            grid_name = "horizontal"
            grid = environement["horizontal_lines"]
        else:
            grid_name = "vertical"
            grid = environement["vertical_lines"]

        nb_row = len(grid)
        nb_col = len(grid[0])

        row = random.randrange(0,nb_row) #ligne et colonne aléatoire
        col = random.randrange(0,nb_col)
        while grid[row][col] != None: #tant qu'on a pas trouvé un emplacement vide

            horizontal = random.choice([True,False])

            if horizontal:
                grid_name = "horizontal"
                grid = environement["horizontal_lines"]
            else:
                grid_name = "vertical"
                grid = environement["vertical_lines"]

            nb_row = len(grid)
            nb_col = len(grid[0])

            row = random.randrange(0,nb_row)
            col = random.randrange(0,nb_col)

        return (grid_name, row,col)
            