import streamlit as st
import numpy as np
import random

# Dimensions de la grille
GRID_SIZE = 10

# Initialisation de la grille
grid = np.zeros((GRID_SIZE, GRID_SIZE))

# Initialisation des joueurs
players = {
    "Player": {"id": 1, "color": 1, "territory": 1},
    "AI1": {"id": 2, "color": 2, "territory": 1},
    "AI2": {"id": 3, "color": 3, "territory": 1},
    "AI3": {"id": 4, "color": 4, "territory": 1},
}

# Position initiale des joueurs
grid[0][0] = players["Player"]["id"]
grid[GRID_SIZE-1][GRID_SIZE-1] = players["AI1"]["id"]
grid[0][GRID_SIZE-1] = players["AI2"]["id"]
grid[GRID_SIZE-1][0] = players["AI3"]["id"]

# Couleurs pour l'affichage
color_map = {
    0: (200, 200, 200),  # Gris pour les cellules vides
    1: (255, 0, 0),      # Rouge pour le joueur
    2: (0, 0, 255),      # Bleu pour AI1
    3: (0, 255, 0),      # Vert pour AI2
    4: (255, 255, 0),    # Jaune pour AI3
}

def draw_grid():
    """Affiche la grille sous forme d'image."""
    img = np.zeros((GRID_SIZE, GRID_SIZE, 3), dtype=int)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            img[x, y] = color_map[grid[x, y]]
    st.image(img, width=400)

def get_adjacent_cells(x, y):
    """Retourne les cellules adjacentes à une position donnée."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            neighbors.append((nx, ny))
    return neighbors

def conquer_territory(player_id, x, y):
    """Conquérir un territoire pour le joueur donné."""
    if grid[x, y] == 0:
        grid[x, y] = player_id
        return True
    return False

def ai_turn(player_id):
    """Gère le tour d'une IA."""
    available_moves = []
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x, y] == player_id:
                for nx, ny in get_adjacent_cells(x, y):
                    if grid[nx, ny] == 0:
                        available_moves.append((nx, ny))
    
    if available_moves:
        x, y = random.choice(available_moves)
        conquer_territory(player_id, x, y)

def game_over():
    """Vérifie si la partie est terminée (aucun territoire libre)."""
    return np.all(grid != 0)

# Streamlit interface
st.title("Territorial.io Simplifié")

draw_grid()

# Entrée du joueur
x_pos = st.slider("Sélectionnez la position X:", 0, GRID_SIZE-1)
y_pos = st.slider("Sélectionnez la position Y:", 0, GRID_SIZE-1)

if st.button("Conquérir ce territoire"):
    if conquer_territory(players["Player"]["id"], x_pos, y_pos):
        for ai in ["AI1", "AI2", "AI3"]:
            ai_turn(players[ai]["id"])

    draw_grid()

    if game_over():
        st.write("Le jeu est terminé!")
