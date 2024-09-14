import pygame
import sys

# On initialise pygame
pygame.init()

# Couleurs
BACKGROUND_COLOR = (52, 50, 62)
DOTS_COLOR = (250, 251, 248)
RED_LINE_COLOR = (245, 106, 121)
BLUE_LINE_COLOR = (127, 207, 248)
RED_SQUARE_COLOR = (211, 22, 38)
BLUE_SQUARE_COLOR = (0, 121, 200)

# Paramètres du jeu
WIDTH, HEIGHT = 600, 640 # en px
GRID_SIZE = 6  # Nombre de points dans une rangée/colonne
DOT_RADIUS = 15
MARGIN = 50 # Marge autour de la grille en px
MARGIN_TOP = 40
CLICK_RADIUS = 14
LINE_WIDTH = 18

SPACING = (WIDTH - 2 * MARGIN) // (GRID_SIZE - 1) # Espacement entre deux points

# On créé la fenêtre de jeu avec Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dots and Boxes")

# Variables du jeu
horizontal_lines = [[None] * (GRID_SIZE - 1) for _ in range(GRID_SIZE)] # None = ligne non tracée, "BLUE" ou "RED" = ligne tracée
vertical_lines = [[None] * GRID_SIZE for _ in range(GRID_SIZE - 1)] # None = ligne non tracée, "BLUE" ou "RED" = ligne tracée
boxes = [[None] * (GRID_SIZE - 1) for _ in range(GRID_SIZE - 1)] # None = boîte non complétée, "BLUE" ou "RED" = boîte complétée
turn = "BLUE"  # Le joueur bleu commence
score = {"BLUE": 0, "RED": 0}

# Police pour afficher le score
font = pygame.font.SysFont(None, 36)


def reset_game():
    global horizontal_lines, vertical_lines, boxes, turn, score
    horizontal_lines = [[None] * (GRID_SIZE - 1) for _ in range(GRID_SIZE)]
    vertical_lines = [[None] * GRID_SIZE for _ in range(GRID_SIZE - 1)]
    boxes = [[None] * (GRID_SIZE - 1) for _ in range(GRID_SIZE - 1)]
    turn = "BLUE"
    score = {"BLUE": 0, "RED": 0}


def check_victory():
    total_boxes = (GRID_SIZE - 1) ** 2
    filled_boxes = sum(1 for row in boxes for box in row if box) # Python pythonesque pour compter les boîtes remplies
    if filled_boxes == total_boxes:  # Si toutes les boîtes sont remplies
        if score["BLUE"] > score["RED"]:
            print("Blue wins!")
        elif score["RED"] > score["BLUE"]:
            print("Red wins!")
        else:
            print("It's a tie!")
        reset_game()  # On réinitialise le jeu après avoir affiché le gagnant


def draw_grid():
    # On remplit l'arrière-plan
    screen.fill(BACKGROUND_COLOR)

    # On dessine les carrés
    for row in range(GRID_SIZE - 1):
        for col in range(GRID_SIZE - 1):
            if boxes[row][col]:
                pygame.draw.rect(
                    screen,  # Surface sur laquelle le rectangle est dessiné
                    BLUE_SQUARE_COLOR if boxes[row][col] == "BLUE" else RED_SQUARE_COLOR,  # Couleur selon le joueur
                    (MARGIN + col * SPACING,  # Position x (en partant du coin supérieur gauche)
                     MARGIN + row * SPACING + MARGIN_TOP,  # Position y (en partant du coin supérieur gauche)
                     SPACING,  # Largeur du rectangle
                     SPACING)  # Hauteur du rectangle
                )

    # On dessine les lignes horizontales
    for row in range(GRID_SIZE):  # Pour chaque ligne
        for col in range(GRID_SIZE - 1):  # Pour chaque colonne
            if horizontal_lines[row][col]:
                pygame.draw.line(
                    screen,
                    BLUE_LINE_COLOR if horizontal_lines[row][col] == "BLUE" else RED_LINE_COLOR,
                    (MARGIN + col * SPACING, MARGIN + row * SPACING + MARGIN_TOP), # Start x, y
                    (MARGIN + (col + 1) * SPACING, MARGIN + row * SPACING + MARGIN_TOP), # End x, y
                    LINE_WIDTH
                )

    # On dessine les lignes verticales
    for row in range(GRID_SIZE - 1):  # Pour chaque ligne
        for col in range(GRID_SIZE):  # Pour chaque colonne
            if vertical_lines[row][col]:
                pygame.draw.line(
                    screen,
                    BLUE_LINE_COLOR if vertical_lines[row][col] == "BLUE" else RED_LINE_COLOR,
                    (MARGIN + col * SPACING, MARGIN + row * SPACING + MARGIN_TOP),
                    (MARGIN + col * SPACING, MARGIN + (row + 1) * SPACING + MARGIN_TOP),
                    LINE_WIDTH
                )

    # On dessine les points
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.circle(screen, DOTS_COLOR, (MARGIN + col * SPACING, MARGIN + row * SPACING + MARGIN_TOP), DOT_RADIUS)


def check_box_completion():
    # On vérifie si une boîte a été complétée après un mouvement
    completed_boxes = 0
    for row in range(GRID_SIZE - 1):
        for col in range(GRID_SIZE - 1):
            if boxes[row][col] is None:
                if horizontal_lines[row][col] and horizontal_lines[row + 1][col] and vertical_lines[row][col] and vertical_lines[row][col + 1]:
                    boxes[row][col] = turn
                    score[turn] += 1
                    completed_boxes += 1
    return completed_boxes


def draw_score():
    # Permet d'afficher le score des deux joueurs
    blue_score_text = font.render(f"Blue: {score['BLUE']}", True, BLUE_SQUARE_COLOR)
    red_score_text = font.render(f"Red: {score['RED']}", True, RED_SQUARE_COLOR)
    screen.blit(blue_score_text, (10, 10))
    screen.blit(red_score_text, (WIDTH - 150, 10))


def handle_click(pos):
    global turn

    x, y = pos
    clicked = False  # Pour savoir si un clic valide a été détecté

    # Traitement des lignes horizontales
    row = 0
    while row < GRID_SIZE and not clicked:
        col = 0
        while col < GRID_SIZE - 1:
            line_x1 = MARGIN + col * SPACING
            line_y1 = MARGIN + row * SPACING + MARGIN_TOP
            line_x2 = line_x1 + SPACING
            line_y2 = line_y1

            # Si on clique près de cette ligne horizontale
            if line_x1 - CLICK_RADIUS < x < line_x2 + CLICK_RADIUS and line_y1 - CLICK_RADIUS < y < line_y2 + CLICK_RADIUS:
                if not horizontal_lines[row][col]:  # Si la ligne n'est pas déjà tracée
                    horizontal_lines[row][col] = turn  # On trace la ligne pour le joueur actuel
                    clicked = True
                    break  # Sort de la boucle des colonnes pour éviter de dessiner plusieurs lignes
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

                # Si on clique près de cette ligne verticale
                if line_x1 - CLICK_RADIUS < x < line_x2 + CLICK_RADIUS and line_y1 - CLICK_RADIUS < y < line_y2 + CLICK_RADIUS:
                    if not vertical_lines[row][col]:  # Si la ligne n'est pas déjà tracée
                        vertical_lines[row][col] = turn  # On trace la ligne pour le joueur actuel
                        clicked = True
                        break  # Sort de la boucle des colonnes pour éviter de dessiner plusieurs lignes
                col += 1
            row += 1

    # Changement de joueur si aucune boîte n'a été complétée
    if clicked and check_box_completion() == 0:
        turn = "RED" if turn == "BLUE" else "BLUE"
    check_victory()

# Boucle de jeu principale
running = True
while running:
    draw_grid()
    draw_score()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())

pygame.quit()
sys.exit()
