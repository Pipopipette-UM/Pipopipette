import pygame
import sys
from time import sleep
from api import API
# On initialise pygame
pygame.init()

# Couleurs
BACKGROUND_COLOR = (52, 50, 62)
DOTS_COLOR = (250, 251, 248)
RED_LINE_COLOR = (245, 106, 121)
BLUE_LINE_COLOR = (127, 207, 248)
DEFAULT_LINE_COLOR = (56, 54, 66)
RED_SQUARE_COLOR = (211, 22, 38)
BLUE_SQUARE_COLOR = (0, 121, 200)

# Paramètres du jeu
WIDTH, HEIGHT = 600, 640 # en px
GRID_SIZE = 5  # Nombre de points par rangée/colonne
DOT_RADIUS = 15
MARGIN = 50 # Marge autour de la grille
MARGIN_TOP = 40
CLICK_RADIUS = 14
LINE_WIDTH = 18

SPACING = (WIDTH - 2 * MARGIN) // (GRID_SIZE - 1) # Espacement entre deux points

# On créé la fenêtre de jeu avec Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dots and Boxes")

# Police pour afficher le score
font = pygame.font.SysFont(None, 36)

class Game:
    def __init__(self):
        self.horizontal_lines = [[None] * (GRID_SIZE - 1) for _ in range(GRID_SIZE)] # None = ligne non tracée, "BLUE" ou "RED" = ligne tracée
        self.vertical_lines = [[None] * GRID_SIZE for _ in range(GRID_SIZE - 1)] # None = ligne non tracée, "BLUE" ou "RED" = ligne tracée
        self.boxes = [[None] * (GRID_SIZE - 1) for _ in range(GRID_SIZE - 1)] # None = boîte non complétée, "BLUE" ou "RED" = boîte complétée
        self.turn = "BLUE"  # Le joueur bleu commence
        self.score = {"BLUE": 0, "RED": 0}
        self.wins = {"BLUE":0, "RED":0}

    def get_environement(self):
        return {
            "horizontal_lines" : self.horizontal_lines,
            "vertical_lines" : self.vertical_lines,
            "boxes" : self.boxes,
            "turn" : self.turn,
            "score" : self.score,
            "GRID_SIZE" : GRID_SIZE
        }

    def make_move(self,move):
        if move[0] == "horizontal":
            row = move[1]
            col = move[2]
            self.horizontal_lines[row][col] = self.turn

        elif move[0] == "vertical":
            row = move[1]
            col = move[2]
            self.vertical_lines[row][col] = self.turn

        if  self.check_box_completion() == 0:
            self.turn = "RED" if self.turn == "BLUE" else "BLUE"
        self.check_victory()


    def draw_grid(self):
        # On remplit l'arrière-plan
        screen.fill(BACKGROUND_COLOR)

        # On dessine les carrés
        for row in range(GRID_SIZE - 1):
            for col in range(GRID_SIZE - 1):
                if self.boxes[row][col]:
                    pygame.draw.rect(
                        screen,  # Surface sur laquelle le rectangle est dessiné
                        BLUE_SQUARE_COLOR if self.boxes[row][col] == "BLUE" else RED_SQUARE_COLOR,  # Couleur selon le joueur
                        (MARGIN + col * SPACING,  # Position x (en partant du coin supérieur gauche)
                         MARGIN + row * SPACING + MARGIN_TOP,  # Position y (en partant du coin supérieur gauche)
                         SPACING,  # Largeur du rectangle
                         SPACING)  # Hauteur du rectangle
                    )

        # On dessine les lignes horizontales
        for row in range(GRID_SIZE):  # Pour chaque ligne
            for col in range(GRID_SIZE - 1):  # Pour chaque colonne
                pygame.draw.line(
                    screen,
                    DEFAULT_LINE_COLOR if not self.horizontal_lines[row][col] else (BLUE_LINE_COLOR if self.horizontal_lines[row][col] == "BLUE" else RED_LINE_COLOR),
                    (MARGIN + col * SPACING, MARGIN + row * SPACING + MARGIN_TOP), # Start x, y
                    (MARGIN + (col + 1) * SPACING, MARGIN + row * SPACING + MARGIN_TOP), # End x, y
                    LINE_WIDTH
                )

        # On dessine les lignes verticales
        for row in range(GRID_SIZE - 1):  # Pour chaque ligne
            for col in range(GRID_SIZE):  # Pour chaque colonne
                pygame.draw.line(
                    screen,
                    DEFAULT_LINE_COLOR if not self.vertical_lines[row][col] else (BLUE_LINE_COLOR if self.vertical_lines[row][col] == "BLUE" else RED_LINE_COLOR),
                    (MARGIN + col * SPACING, MARGIN + row * SPACING + MARGIN_TOP),
                    (MARGIN + col * SPACING, MARGIN + (row + 1) * SPACING + MARGIN_TOP),
                    LINE_WIDTH
                )

        # On dessine les points
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                pygame.draw.circle(screen, DOTS_COLOR, (MARGIN + col * SPACING, MARGIN + row * SPACING + MARGIN_TOP), DOT_RADIUS)


    def check_box_completion(self):
        # On vérifie si une boîte a été complétée après un mouvement
        completed_boxes = 0
        for row in range(GRID_SIZE - 1):
            for col in range(GRID_SIZE - 1):
                if self.boxes[row][col] is None:
                    if (self.horizontal_lines[row][col] and self.horizontal_lines[row + 1][col] and
                            self.vertical_lines[row][col] and self.vertical_lines[row][col + 1]):
                        self.boxes[row][col] = self.turn
                        self.score[self.turn] += 1
                        completed_boxes += 1
        return completed_boxes


    def draw_score(self):
        # Permet d'afficher le score des deux joueurs
        blue_score_text = font.render(f"Blue: {self.score['BLUE']}", True, BLUE_SQUARE_COLOR)
        red_score_text = font.render(f"Red: {self.score['RED']}", True, RED_SQUARE_COLOR)
        screen.blit(blue_score_text, (10, 10))
        screen.blit(red_score_text, (WIDTH - 150, 10))


    def handle_click(self, pos):
        x, y = pos
        clicked = False

        # Traitement des lignes horizontales
        row = 0
        while row < GRID_SIZE and not clicked:
            col = 0
            while col < GRID_SIZE - 1:
                line_x1 = MARGIN + col * SPACING
                line_y1 = MARGIN + row * SPACING + MARGIN_TOP
                line_x2 = line_x1 + SPACING
                line_y2 = line_y1

                if line_x1 - CLICK_RADIUS < x < line_x2 + CLICK_RADIUS and line_y1 - CLICK_RADIUS < y < line_y2 + CLICK_RADIUS:
                    if not self.horizontal_lines[row][col]: # Si la ligne n'est pas déjà tracée
                        self.horizontal_lines[row][col] = self.turn # On trace la ligne pour le joueur actuel
                        clicked = True
                        break # On sort de la boucle des colonnes pour éviter de dessiner plusieurs lignes
                col += 1
            row += 1

        # On traite les lignes verticales seulement si aucun clic horizontal n'a été traité
        if not clicked:
            row = 0
            while row < GRID_SIZE - 1 and not clicked:
                col = 0
                while col < GRID_SIZE:
                    line_x1 = MARGIN + col * SPACING
                    line_y1 = MARGIN + row * SPACING + MARGIN_TOP
                    line_x2 = line_x1
                    line_y2 = line_y1 + SPACING

                    if line_x1 - CLICK_RADIUS < x < line_x2 + CLICK_RADIUS and line_y1 - CLICK_RADIUS < y < line_y2 + CLICK_RADIUS:
                        if not self.vertical_lines[row][col]: # Si la ligne n'est pas déjà tracée
                            self.vertical_lines[row][col] = self.turn # On trace la ligne pour le joueur actuel
                            clicked = True
                            break # On sort de la boucle des colonnes pour éviter de dessiner plusieurs lignes
                    col += 1
                row += 1

        # On change de joueur si aucune boîte n'a été complétée
        if clicked and self.check_box_completion() == 0:
            self.turn = "RED" if self.turn == "BLUE" else "BLUE"
        self.check_victory()


    def check_victory(self):
        total_boxes = (GRID_SIZE - 1) ** 2
        filled_boxes = sum(1 for row in self.boxes for box in row if box)  # Python pythonesque pour compter les boîtes remplies

        if filled_boxes == total_boxes: # Si toutes les boîtes sont remplies
            if self.score["BLUE"] > self.score["RED"]:
                print("Le joueur BLEU a gagné !")
            elif self.score["RED"] > self.score["BLUE"]:
                print("Le joueur ROUGE a gagné !")
            else:
                print("Match nul !")
            self.reset_game()  # On réinitialise le jeu après avoir affiché le gagnant


    def reset_game(self):
        # On réinitialise l'état du jeu
        self.__init__()


def main() :
    game = Game()
    api = API(game)
    # Boucle de jeu principale
    running = True
    while running:
        game.draw_grid()
        game.draw_score()
        pygame.display.flip()

        #sleep(0.5)
        api.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #game.handle_click(pygame.mouse.get_pos())
                api.play()
                print("cbon")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()