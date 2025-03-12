import random
import time

# Configuration
WIDTH = 10
HEIGHT = 12
BLOCK_CHAR = "█"
EMPTY_CHAR = " "

# Pièces de Tetris simplifiées
PIECES = [
    [[1, 1],
     [1, 1]],  # Carré
    
    [[1, 1, 1],
     [0, 1, 0]],  # T
    
    [[1, 1, 1, 1]],  # I
    
    [[1, 1, 0],
     [0, 1, 1]],  # Z
]

class Piece:
    def __init__(self):
        self.shape = random.choice(PIECES)
        self.x = WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

def clear_screen():
    print("\n" * 10)

def create_board():
    return [[EMPTY_CHAR for _ in range(WIDTH)] for _ in range(HEIGHT)]

def draw_game(board, piece, score):
    clear_screen()
    temp_board = [row[:] for row in board]
    
    # Dessiner la pièce courante
    if piece:
        for y in range(len(piece.shape)):
            for x in range(len(piece.shape[0])):
                if piece.shape[y][x] and 0 <= piece.y + y < HEIGHT and 0 <= piece.x + x < WIDTH:
                    temp_board[piece.y + y][piece.x + x] = BLOCK_CHAR
    
    print("=== TETRIS - nailec.fr ===")
    print(f"Score: {score}")
    print("+" + "-" * WIDTH + "+")
    for row in temp_board:
        print("|" + "".join(row) + "|")
    print("+" + "-" * WIDTH + "+")

def check_collision(board, piece, dx=0, dy=0):
    for y in range(len(piece.shape)):
        for x in range(len(piece.shape[0])):
            if piece.shape[y][x]:
                new_x = piece.x + x + dx
                new_y = piece.y + y + dy
                if (new_x < 0 or new_x >= WIDTH or
                    new_y >= HEIGHT or
                    (new_y >= 0 and board[new_y][new_x] == BLOCK_CHAR)):
                    return True
    return False

def merge_piece(board, piece):
    for y in range(len(piece.shape)):
        for x in range(len(piece.shape[0])):
            if piece.shape[y][x]:
                board[piece.y + y][piece.x + x] = BLOCK_CHAR

def remove_lines(board):
    lines_cleared = 0
    y = HEIGHT - 1
    while y >= 0:
        if all(cell == BLOCK_CHAR for cell in board[y]):
            lines_cleared += 1
            del board[y]
            board.insert(0, [EMPTY_CHAR for _ in range(WIDTH)])
        else:
            y -= 1
    return lines_cleared

def rotate_piece(piece):
    # Rotation simple 90° sens horaire
    rows = len(piece.shape)
    cols = len(piece.shape[0])
    rotated = [[0 for _ in range(rows)] for _ in range(cols)]
    for y in range(rows):
        for x in range(cols):
            rotated[x][rows-1-y] = piece.shape[y][x]
    return rotated

def main():
    board = create_board()
    current_piece = Piece()
    score = 0
    fall_time = 0
    fall_speed = 0.5  # Secondes entre chaque chute
    last_fall = time.time()
    
    print("=== TETRIS by nailec.fr ===")
    print("4: Gauche, 6: Droite")
    print("8: Rotation, 2: Descente rapide")
    print("q: Quitter")
    input("Appuyez sur Entrée pour commencer...")
    
    while True:
        draw_game(board, current_piece, score)
        
        # Gestion des touches
        key = input("Commande: ")
        
        if key == "q":
            break
        elif key == "4" and not check_collision(board, current_piece, dx=-1):
            current_piece.x -= 1
        elif key == "6" and not check_collision(board, current_piece, dx=1):
            current_piece.x += 1
        elif key == "2":
            while not check_collision(board, current_piece, dy=1):
                current_piece.y += 1
            merge_piece(board, current_piece)
            score += remove_lines(board) * 100
            current_piece = Piece()
            if check_collision(board, current_piece):
                break
        elif key == "8":
            rotated_shape = rotate_piece(current_piece.shape)
            old_shape = current_piece.shape
            current_piece.shape = rotated_shape
            if check_collision(board, current_piece):
                current_piece.shape = old_shape
        
        # Chute automatique
        current_time = time.time()
        if current_time - last_fall > fall_speed:
            if not check_collision(board, current_piece, dy=1):
                current_piece.y += 1
            else:
                merge_piece(board, current_piece)
                score += remove_lines(board) * 100
                current_piece = Piece()
                if check_collision(board, current_piece):
                    break
            last_fall = current_time
    
    print("=== GAME OVER ===")
    print(f"Score final: {score}")
    print("=== nailec.fr ===")
    input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main() 