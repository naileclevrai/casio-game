import random
import time

# Configuration
WIDTH = 21
HEIGHT = 7
PADDLE_HEIGHT = 3
BALL_CHAR = "O"
PADDLE_CHAR = "|"

class Paddle:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT // 2
        self.score = 0

class Ball:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

def clear_screen():
    print("\n" * 10)

def draw_game(paddle1, paddle2, ball):
    clear_screen()
    board = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # Dessiner les raquettes
    for y in range(max(0, paddle1.y - PADDLE_HEIGHT//2), 
                   min(HEIGHT, paddle1.y + PADDLE_HEIGHT//2 + 1)):
        board[y][paddle1.x] = PADDLE_CHAR
    
    for y in range(max(0, paddle2.y - PADDLE_HEIGHT//2), 
                   min(HEIGHT, paddle2.y + PADDLE_HEIGHT//2 + 1)):
        board[y][paddle2.x] = PADDLE_CHAR
    
    # Dessiner la balle
    if 0 <= ball.x < WIDTH and 0 <= ball.y < HEIGHT:
        board[ball.y][ball.x] = BALL_CHAR
    
    # Afficher le score
    print(f"=== PONG - nailec.fr ===")
    print(f"Score: {paddle1.score} - {paddle2.score}")
    
    # Afficher le plateau
    for row in board:
        print("".join(row))

def main():
    paddle1 = Paddle(1)
    paddle2 = Paddle(WIDTH-2)
    ball = Ball()
    
    print("=== PONG by nailec.fr ===")
    input("Appuyez sur Entrée pour commencer...")
    
    while True:
        draw_game(paddle1, paddle2, ball)
        
        # Contrôles
        key = input("J1:8/2, J2:5/0, q:quitter: ")
        
        if key == "q":
            break
        elif key == "8" and paddle1.y > 1:
            paddle1.y -= 1
        elif key == "2" and paddle1.y < HEIGHT-2:
            paddle1.y += 1
        elif key == "5" and paddle2.y > 1:
            paddle2.y -= 1
        elif key == "0" and paddle2.y < HEIGHT-2:
            paddle2.y += 1
        
        # Mouvement de la balle
        ball.x += ball.dx
        ball.y += ball.dy
        
        # Collision avec les murs
        if ball.y <= 0 or ball.y >= HEIGHT-1:
            ball.dy *= -1
        
        # Collision avec les raquettes
        if (ball.x == paddle1.x + 1 and 
            paddle1.y - PADDLE_HEIGHT//2 <= ball.y <= paddle1.y + PADDLE_HEIGHT//2):
            ball.dx *= -1
        
        if (ball.x == paddle2.x - 1 and 
            paddle2.y - PADDLE_HEIGHT//2 <= ball.y <= paddle2.y + PADDLE_HEIGHT//2):
            ball.dx *= -1
        
        # Points
        if ball.x <= 0:
            paddle2.score += 1
            ball.reset()
        elif ball.x >= WIDTH-1:
            paddle1.score += 1
            ball.reset()
        
        time.sleep(0.1)  # Ralentir le jeu

if __name__ == "__main__":
    main() 