import random

# Initialisation de l'écran
def init_screen():
    clear_screen()
    # Dimensions de l'écran Casio
    global WIDTH, HEIGHT
    WIDTH = 21
    HEIGHT = 7

# Variables globales
snake = [(10, 3)]  # Position initiale du serpent
direction = (1, 0)  # Direction initiale (droite)
food = (15, 3)     # Position initiale de la nourriture
score = 0

def clear_screen():
    print("\n" * 10)

def place_food():
    global food
    while True:
        x = random.randint(0, WIDTH-1)
        y = random.randint(0, HEIGHT-1)
        if (x, y) not in snake:
            food = (x, y)
            break

def draw_game():
    clear_screen()
    # Création du tableau de jeu
    board = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # Placer le serpent
    for x, y in snake:
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            board[y][x] = "O"
    
    # Placer la nourriture
    if 0 <= food[0] < WIDTH and 0 <= food[1] < HEIGHT:
        board[food[1]][food[0]] = "X"
    
    # Afficher le tableau
    print("=== SNAKE - nailec.fr ===")
    print(f"Score: {score}")
    for row in board:
        print("".join(row))

def move_snake():
    global snake, score
    
    # Nouvelle tête
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    
    # Vérifier les collisions avec les murs
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake):
        return False
    
    snake.insert(0, new_head)
    
    # Vérifier si on mange la nourriture
    if new_head == food:
        score += 1
        place_food()
    else:
        snake.pop()
    
    return True

def main():
    global direction
    
    init_screen()
    print("=== SNAKE by nailec.fr ===")
    input("Appuyez sur Entrée pour commencer...")
    
    running = True
    while running:
        draw_game()
        
        # Gestion des touches
        key = input("Direction (8:haut, 2:bas, 4:gauche, 6:droite, q:quitter): ")
        
        if key == "q":
            running = False
        elif key == "8" and direction != (0, 1):
            direction = (0, -1)
        elif key == "2" and direction != (0, -1):
            direction = (0, 1)
        elif key == "4" and direction != (1, 0):
            direction = (-1, 0)
        elif key == "6" and direction != (-1, 0):
            direction = (1, 0)
        
        if not move_snake():
            print("=== GAME OVER ===")
            print(f"Score final: {score}")
            print("=== nailec.fr ===")
            input("Appuyez sur Entrée pour continuer...")
            break

if __name__ == "__main__":
    main() 