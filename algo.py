import random
import copy

class Algo:

    @staticmethod
    def random(environement):
        horizontal = random.choice([True, False])
        if horizontal:
            grid_name = "horizontal"
            grid = environement["horizontal_lines"]
        else:
            grid_name = "vertical"
            grid = environement["vertical_lines"]

        nb_row = len(grid)
        nb_col = len(grid[0])

        row = random.randrange(0, nb_row)
        col = random.randrange(0, nb_col)
        while grid[row][col] is not None:
            horizontal = random.choice([True, False])
            if horizontal:
                grid_name = "horizontal"
                grid = environement["horizontal_lines"]
            else:
                grid_name = "vertical"
                grid = environement["vertical_lines"]

            nb_row = len(grid)
            nb_col = len(grid[0])

            row = random.randrange(0, nb_row)
            col = random.randrange(0, nb_col)

        return (grid_name, row, col)

    @staticmethod
    def check_box_completion(line_direction, row, col, environement):
        vertical_lines = environement["vertical_lines"]
        horizontal_lines = environement["horizontal_lines"]
        boxes = environement["boxes"]
        turn = environement["turn"]
        score = environement["score"]
        new_score = copy.deepcopy(score)
        GRID_SIZE = environement["GRID_SIZE"]
        completed_boxes = 0
        if line_direction == "horizontal":
            if row > 0 and col < GRID_SIZE - 1 and horizontal_lines[row][col] and horizontal_lines[row - 1][col] and vertical_lines[row - 1][col] and vertical_lines[row - 1][col + 1]:
                new_score[turn] += 1
                completed_boxes += 1
            if row < GRID_SIZE - 1 and col < GRID_SIZE - 1 and horizontal_lines[row][col] and horizontal_lines[row + 1][col] and vertical_lines[row][col] and vertical_lines[row][col + 1]:
                new_score[turn] += 1
                completed_boxes += 1
        elif line_direction == "vertical":
            if row < GRID_SIZE - 1 and col > 0 and vertical_lines[row][col] and vertical_lines[row][col - 1] and horizontal_lines[row][col - 1] and horizontal_lines[row + 1][col - 1]:
                new_score[turn] += 1
                completed_boxes += 1
            if row < GRID_SIZE - 1 and col < GRID_SIZE - 1 and vertical_lines[row][col] and vertical_lines[row][col + 1] and horizontal_lines[row][col] and horizontal_lines[row + 1][col]:
                new_score[turn] += 1
                completed_boxes += 1
        return (completed_boxes, new_score[turn])

    @staticmethod
    def glouton(environement):
        vertical_lines = environement["vertical_lines"]
        horizontal_lines = environement["horizontal_lines"]
        turn = environement["turn"]
        score = environement["score"][turn]

        best_move = Algo.random(environement)
        best_score = score

        for i in range(len(vertical_lines)):
            for j in range(len(vertical_lines[0])):
                if vertical_lines[i][j] is None:
                    vertical_lines_copy = copy.deepcopy(vertical_lines)
                    vertical_lines_copy[i][j] = turn
                    environement["vertical_lines"] = vertical_lines_copy
                    _, new_score = Algo.check_box_completion("vertical", i, j, environement)
                    environement["vertical_lines"] = vertical_lines
                    if new_score > best_score:
                        best_score = new_score
                        best_move = ("vertical", i, j)

        for i in range(len(horizontal_lines)):
            for j in range(len(horizontal_lines[0])):
                if horizontal_lines[i][j] is None:
                    horizontal_lines_copy = copy.deepcopy(horizontal_lines)
                    horizontal_lines_copy[i][j] = turn
                    environement["horizontal_lines"] = horizontal_lines_copy
                    _, new_score = Algo.check_box_completion("horizontal", i, j, environement)
                    environement["horizontal_lines"] = horizontal_lines
                    if new_score > best_score:
                        best_score = new_score
                        best_move = ("horizontal", i, j)
                        #print("best horizontal", best_move)

        return best_move
