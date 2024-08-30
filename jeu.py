import pygame
import random
import streamlit as st
from pygame import surfarray
import numpy as np

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Dimensions de la grille et de la fenêtre
GRID_SIZE = 10
CELL_SIZE = 40
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

# Création de la fenêtre virtuelle (sans affichage)
window = pygame.Surface((WIDTH, HEIGHT))

# Initialisation de la grille
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Initialisation des joueurs
players = {
    "Player": {"color": RED, "territory": 1, "is_human": True},
    "AI1": {"color": BLUE, "territory": 1, "is_human": False},
    "AI2": {"color": GREEN, "territory": 1, "is_human": False},
    "AI3": {"color": YELLOW, "territory": 1, "is_human": False},
}

# Position initiale des joueurs
grid[0][0] = players["Player"]["color"]
grid[GRID_SIZE-1][GRID_SIZE-1] = players["AI1"]["color"]
grid[0][GRID_SIZE-1] = players["AI2"]["color"]
grid[GRID_SIZE-1][0] = players["AI3"]["color"]

def draw_grid():
    """Dessine la grille sur l'écran."""
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = grid[x][y] if grid[x][y] else WHITE
            pygame.draw.rect(window, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(window, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def get_adjacent_cells(x, y):
    """Retourne les cellules adjacentes à une position donnée."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            neighbors.append((nx, ny))
    return neighbors

def conquer_territory(player_name, x, y):
    """Conquérir un territoire pour le joueur donné."""
    if grid[x][y] is None:
        grid[x][y] = players[player_name]["color"]
        players[player_name]["territory"] += 1
        return True
    return False

def player_turn(pos, player_name):
    """Gère le tour du joueur."""
    x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
    if grid[x][y] is None:
        for nx, ny in get_adjacent_cells(x, y):
            if grid[nx][ny] == players[player_name]["color"]:
                conquer_territory(player_name, x, y)
                return True
    return False

def ai_turn(player_name):
    """Gère le tour d'une IA."""
    available_moves = []
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == players[player_name]["color"]:
                for nx, ny in get_adjacent_cells(x, y):
                    if grid[nx][ny] is None:
                        available_moves.append((nx, ny))
    
    if available_moves:
        x, y = random.choice(available_moves)
        conquer_territory(player_name, x, y)

def game_over():
    """Vérifie si la partie est terminée (aucun territoire libre)."""
    for row in grid:
        if None in row:
            return False
    return True

def display_scores():
    """Affiche les scores (territoires) des joueurs à l'écran."""
    font = pygame.font.Font(None, 36)
    y_offset = 10
    for player_name, data in players.items():
        score_text = f"{player_name}: {data['territory']} territories"
        score_surface = font.render(score_text, True, data["color"])
        window.blit(score_surface, (10, y_offset))
        y_offset += 30

# Streamlit interface setup
st.title("Territorial.io - Simplifié avec Streamlit")
st.write("Cliquez sur la grille pour jouer. Les IA joueront après vous.")

# Boucle principale du jeu
player_turn_active = True
turns = list(players.keys())  # Liste des joueurs par ordre de tour

def update_game():
    global player_turn_active
    window.fill(WHITE)
    draw_grid()
    display_scores()
    
    # Convert the Pygame surface to an image that can be displayed in Streamlit
    img_array = surfarray.array3d(window)
    img_array = np.transpose(img_array, (1, 0, 2))
    st.image(img_array)

    if not player_turn_active:
        for ai in ["AI1", "AI2", "AI3"]:
            ai_turn(ai)
        player_turn_active = True

    if game_over():
        winner = max(players.items(), key=lambda p: p[1]["territory"])
        st.write(f"Le jeu est terminé! {winner[0]} gagne avec {winner[1]['territory']} territoires!")
        st.stop()

# Gestion de l'entrée de l'utilisateur
if st.button('Recommencer'):
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    grid[0][0] = players["Player"]["color"]
    grid[GRID_SIZE-1][GRID_SIZE-1] = players["AI1"]["color"]
    grid[0][GRID_SIZE-1] = players["AI2"]["color"]
    grid[GRID_SIZE-1][0] = players["AI3"]["color"]
    for player in players.values():
        player["territory"] = 1
    player_turn_active = True

clicked = st.empty()
if clicked.button("Jouer (Cliquez sur la grille ci-dessous)"):
    update_game()

# Position du clic sur la grille
x_pos = st.slider("Sélectionnez la position X:", 0, GRID_SIZE-1)
y_pos = st.slider("Sélectionnez la position Y:", 0, GRID_SIZE-1)

if st.button("Conquérir ce territoire"):
    if player_turn_active:
        if player_turn((x_pos * CELL_SIZE, y_pos * CELL_SIZE), "Player"):
            player_turn_active = False
            update_game()

update_game()
