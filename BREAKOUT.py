import random
import time

# Configuration
WIDTH = 21
HEIGHT = 12
PADDLE_CHAR = "="
BALL_CHAR = "O"
BRICK_CHAR = "#"
PADDLE_SIZE = 3

class Paddle:
    def __init__(self):
        self.x = WIDTH // 2 - PADDLE_SIZE // 2
        self.size = PADDLE_SIZE

class Ball:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 2
        self.dx = random.choice([-1, 1])
        self.dy = -1

def clear_screen():
    print("\n" * 10)

def create_bricks():
    bricks = []
    for y in range(3):
        for x in range(2, WIDTH-2):
            bricks.append([x, y+1])
    return bricks

def draw_game(paddle, ball, bricks, score):
    clear_screen()
    board = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # Dessiner la raquette
    for x in range(paddle.x, min(paddle.x + paddle.size, WIDTH)):
        board[HEIGHT-1][x] = PADDLE_CHAR
    
    # Dessiner la balle
    if 0 <= ball.y < HEIGHT and 0 <= ball.x < WIDTH:
        board[ball.y][ball.x] = BALL_CHAR
    
    # Dessiner les briques
    for brick in bricks:
        board[brick[1]][brick[0]] = BRICK_CHAR
    
    print("=== BREAKOUT - nailec.fr ===")
    print(f"Score: {score}")
    
    # Afficher le plateau
    for row in board:
        print("".join(row))

def main():
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    score = 0
    game_speed = 0.1
    
    print("=== BREAKOUT by nailec.fr ===")
    print("4: Gauche, 6: Droite")
    print("q: Quitter")
    input("Appuyez sur Entrée pour commencer...")
    
    while True:
        draw_game(paddle, ball, bricks, score)
        
        # Gestion des touches
        key = input("Commande: ")
        
        if key == "q":
            break
        elif key == "4" and paddle.x > 0:
            paddle.x -= 1
        elif key == "6" and paddle.x < WIDTH - paddle.size:
            paddle.x += 1
        
        # Déplacer la balle
        ball.x += ball.dx
        ball.y += ball.dy
        
        # Collision avec les murs
        if ball.x <= 0 or ball.x >= WIDTH-1:
            ball.dx *= -1
        if ball.y <= 0:
            ball.dy *= -1
        
        # Collision avec la raquette
        if ball.y == HEIGHT-1 and paddle.x <= ball.x < paddle.x + paddle.size:
            ball.dy = -1
            # Ajuster la direction horizontale selon la position sur la raquette
            relative_x = ball.x - paddle.x
            if relative_x < paddle.size // 3:
                ball.dx = -1
            elif relative_x > (paddle.size * 2) // 3:
                ball.dx = 1
        
        # Collision avec les briques
        new_bricks = []
        for brick in bricks:
            if brick[0] == ball.x and brick[1] == ball.y:
                ball.dy *= -1
                score += 10
            else:
                new_bricks.append(brick)
        bricks = new_bricks
        
        # Conditions de fin
        if ball.y >= HEIGHT:  # Balle perdue
            print("=== GAME OVER ===")
            print(f"Score final: {score}")
            print("=== nailec.fr ===")
            input("Appuyez sur Entrée pour continuer...")
            break
        
        if not bricks:  # Victoire
            print("=== VICTOIRE! ===")
            print(f"Score final: {score}")
            print("=== nailec.fr ===")
            input("Appuyez sur Entrée pour continuer...")
            break
        
        time.sleep(game_speed)

if __name__ == "__main__":
    main() 