import random
import time

# Configuration
WIDTH = 21
HEIGHT = 7
BIRD_CHAR = ">"
PIPE_CHAR = "|"
GAP_SIZE = 3

class Bird:
    def __init__(self):
        self.x = 5
        self.y = HEIGHT // 2
        self.velocity = 0
        self.score = 0

class Pipe:
    def __init__(self, x):
        self.x = x
        gap_pos = random.randint(1, HEIGHT - GAP_SIZE - 1)
        self.gaps = range(gap_pos, gap_pos + GAP_SIZE)

def clear_screen():
    print("\n" * 10)

def draw_game(bird, pipes):
    clear_screen()
    board = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # Dessiner l'oiseau
    if 0 <= bird.y < HEIGHT:
        board[bird.y][bird.x] = BIRD_CHAR
    
    # Dessiner les tuyaux
    for pipe in pipes:
        if 0 <= pipe.x < WIDTH:
            for y in range(HEIGHT):
                if y not in pipe.gaps:
                    board[y][pipe.x] = PIPE_CHAR
    
    print("=== FLAPPY BIRD - nailec.fr ===")
    print(f"Score: {bird.score}")
    
    # Afficher le plateau
    for row in board:
        print("".join(row))

def main():
    bird = Bird()
    pipes = [Pipe(WIDTH-1)]
    game_speed = 0.2
    gravity = 0.5
    
    print("=== FLAPPY BIRD by nailec.fr ===")
    print("8: Sauter")
    print("q: Quitter")
    input("Appuyez sur Entrée pour commencer...")
    
    while True:
        draw_game(bird, pipes)
        
        # Gestion des touches
        key = input("Commande: ")
        
        if key == "q":
            break
        elif key == "8":
            bird.velocity = -1
        
        # Physique
        bird.velocity += gravity
        bird.y = int(bird.y + bird.velocity)
        
        # Déplacer les tuyaux
        for pipe in pipes:
            pipe.x -= 1
        pipes = [p for p in pipes if p.x >= 0]
        
        # Générer de nouveaux tuyaux
        if len(pipes) == 0 or pipes[-1].x < WIDTH - 10:
            pipes.append(Pipe(WIDTH-1))
        
        # Vérifier les collisions
        game_over = False
        for pipe in pipes:
            if pipe.x == bird.x:
                if bird.y not in pipe.gaps:
                    game_over = True
                else:
                    bird.score += 1
        
        # Collision avec les bords
        if bird.y < 0 or bird.y >= HEIGHT:
            game_over = True
        
        if game_over:
            print("=== GAME OVER ===")
            print(f"Score final: {bird.score}")
            print("=== nailec.fr ===")
            input("Appuyez sur Entrée pour continuer...")
            break
        
        time.sleep(game_speed)

if __name__ == "__main__":
    main() 