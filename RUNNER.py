import random
import time

# Configuration
WIDTH = 21
HEIGHT = 7
PLAYER_CHAR = "A"
OBSTACLE_CHAR = "X"
GROUND_CHAR = "_"

class Player:
    def __init__(self):
        self.x = 5
        self.y = HEIGHT - 2
        self.jumping = False
        self.jump_count = 0
        self.score = 0

class Obstacle:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT - 2

def clear_screen():
    print("\n" * 10)

def draw_game(player, obstacles):
    clear_screen()
    board = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # Dessiner le sol
    for x in range(WIDTH):
        board[HEIGHT-1][x] = GROUND_CHAR
    
    # Dessiner le joueur
    board[player.y][player.x] = PLAYER_CHAR
    
    # Dessiner les obstacles
    for obs in obstacles:
        if 0 <= obs.x < WIDTH:
            board[obs.y][obs.x] = OBSTACLE_CHAR
    
    print("=== RUNNER - nailec.fr ===")
    print(f"Score: {player.score}")
    
    # Afficher le plateau
    for row in board:
        print("".join(row))

def main():
    player = Player()
    obstacles = []
    game_speed = 0.2
    last_spawn = 0
    spawn_rate = 15
    
    print("=== RUNNER by nailec.fr ===")
    print("8: Sauter")
    print("q: Quitter")
    input("Appuyez sur Entrée pour commencer...")
    
    while True:
        draw_game(player, obstacles)
        
        # Gestion des touches
        key = input("Commande: ")
        
        if key == "q":
            break
        elif key == "8" and not player.jumping:
            player.jumping = True
            player.jump_count = 3
        
        # Gestion du saut
        if player.jumping:
            if player.jump_count > 0:
                player.y -= 1
                player.jump_count -= 1
            elif player.y < HEIGHT - 2:
                player.y += 1
            else:
                player.jumping = False
        
        # Déplacer les obstacles
        for obs in obstacles:
            obs.x -= 1
        obstacles = [obs for obs in obstacles if obs.x >= 0]
        
        # Générer de nouveaux obstacles
        if len(obstacles) == 0 or obstacles[-1].x < WIDTH - spawn_rate:
            obstacles.append(Obstacle(WIDTH-1))
        
        # Vérifier les collisions
        for obs in obstacles:
            if obs.x == player.x and obs.y == player.y:
                print("=== GAME OVER ===")
                print(f"Score final: {player.score}")
                print("=== nailec.fr ===")
                input("Appuyez sur Entrée pour continuer...")
                return
        
        # Augmenter le score
        player.score += 1
        
        # Augmenter la difficulté
        if player.score % 100 == 0 and game_speed > 0.1:
            game_speed -= 0.01
        
        time.sleep(game_speed)

if __name__ == "__main__":
    main() 