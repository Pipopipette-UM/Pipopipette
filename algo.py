import random
import copy

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
            

    @staticmethod
    def check_box_completion(environement):
        vertical_lines = environement["vertical_lines"]
        horizontal_lines = environement["horizontal_lines"]
        boxes = environement["boxes"]
        turn = environement["turn"]
        score = environement["score"]
        new_score = copy.deepcopy(score)
        GRID_SIZE = environement["GRID_SIZE"]
        # On vérifie si une boîte a été complétée après un mouvement
        completed_boxes = 0
        for row in range(GRID_SIZE - 1):
            for col in range(GRID_SIZE - 1):
                if boxes[row][col] is None:
                    if (horizontal_lines[row][col] and horizontal_lines[row + 1][col] and
                            vertical_lines[row][col] and vertical_lines[row][col + 1]):
                        new_score[turn] += 1
                        completed_boxes += 1
        #if new_score[turn] != 0 :print("new score possible : ",new_score[turn])
        return (completed_boxes,new_score[turn])

    @staticmethod
    def glouton(environement):
        vertical_lines = environement["vertical_lines"]
        horizontal_lines = environement["horizontal_lines"]
        turn = environement["turn"]
        score = environement["score"]

        vertical_move = Algo.random(environement) #on fait une action aléatoire si on ne trouve pas d'action qui rapporte des points
        better_vertical = False #True si on a trouvé une meilleure action que l'aléatoire

        for i in range( len(vertical_lines)  ):
            if better_vertical : break
            for j in range( len(vertical_lines[0])   ):
                
                if vertical_lines[i][j] == None:

                    vertical_lines_copy = copy.deepcopy(vertical_lines)
                    vertical_lines_copy[i][j] = turn
                    environement["vertical_lines"] = vertical_lines_copy
                    boxes, new_score = Algo.check_box_completion(environement)
                    #print(boxes,new_score)
                    environement["vertical_lines"] = vertical_lines
                    if(new_score > score[turn]):
                        vertical_move = ("vertical", i,j)
                        better_vertical = True
                        #print("found move: ", vertical_move)
                        break
                        

        horizontal_move = Algo.random(environement)
        better_horizontal = False

        for i in range( len(horizontal_lines)  ):
            if better_horizontal : break
            for j in range( len(horizontal_lines[0])   ):
                
                if horizontal_lines[i][j] == None:

                    horizontal_lines_copy = copy.deepcopy(horizontal_lines)
                    horizontal_lines_copy[i][j] = turn
                    environement["horizontal_lines"] = horizontal_lines_copy
                    boxes, new_score = Algo.check_box_completion(environement)
                    environement["horizontal_lines"] = horizontal_lines

                    if(new_score > score[turn]):
                        horizontal_move = ("horizontal", i,j)
                        better_horizontal = True
                        #print("found move: ", horizontal_move)
                        break
                        


        if (better_horizontal and better_vertical):
            return random.choice([horizontal_move,vertical_move])
        elif better_horizontal:
            return horizontal_move
        elif better_vertical:
            return vertical_move

        else:
            return random.choice([horizontal_move,vertical_move])