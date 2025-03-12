import random

# Configuration
SIZE = 3
EMPTY = " "
MOVES = {
    "8": (-1, 0),  # Haut
    "2": (1, 0),   # Bas
    "4": (0, -1),  # Gauche
    "6": (0, 1)    # Droite
}

def clear_screen():
    print("\n" * 10)

def create_board():
    numbers = list(range(1, SIZE*SIZE))
    numbers.append(EMPTY)
    random.shuffle(numbers)
    
    # Vérifier si le puzzle est solvable
    inversions = 0
    for i in range(len(numbers)):
        if numbers[i] == EMPTY:
            continue
        for j in range(i+1, len(numbers)):
            if numbers[j] == EMPTY:
                continue
            if numbers[i] > numbers[j]:
                inversions += 1
    
    # Si le nombre d'inversions est impair, échanger deux nombres
    if inversions % 2 == 1:
        i = numbers.index(1)
        j = numbers.index(2)
        numbers[i], numbers[j] = numbers[j], numbers[i]
    
    board = []
    for i in range(SIZE):
        row = numbers[i*SIZE:(i+1)*SIZE]
        board.append(row)
    return board

def draw_game(board, moves):
    clear_screen()
    print("=== TAQUIN - nailec.fr ===")
    print(f"Déplacements: {moves}")
    print("\n+" + "-" * (SIZE*4-1) + "+")
    for row in board:
        print("|", end=" ")
        for cell in row:
            if cell == EMPTY:
                print(" ", end=" |")
            else:
                print(f"{cell:1d}", end=" |")
        print("\n+" + "-" * (SIZE*4-1) + "+")

def find_empty(board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == EMPTY:
                return i, j
    return None

def is_valid_move(board, direction):
    empty_i, empty_j = find_empty(board)
    new_i = empty_i + direction[0]
    new_j = empty_j + direction[1]
    return 0 <= new_i < SIZE and 0 <= new_j < SIZE

def make_move(board, direction):
    empty_i, empty_j = find_empty(board)
    new_i = empty_i + direction[0]
    new_j = empty_j + direction[1]
    
    board[empty_i][empty_j], board[new_i][new_j] = board[new_i][new_j], board[empty_i][empty_j]

def is_solved(board):
    numbers = list(range(1, SIZE*SIZE))
    numbers.append(EMPTY)
    
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] != numbers[i*SIZE + j]:
                return False
    return True

def main():
    board = create_board()
    moves = 0
    
    print("=== TAQUIN by nailec.fr ===")
    print("Remettez les nombres dans l'ordre!")
    print("8: Haut, 2: Bas, 4: Gauche, 6: Droite")
    print("q: Quitter")
    input("Appuyez sur Entrée pour commencer...")
    
    while not is_solved(board):
        draw_game(board, moves)
        
        key = input("Commande: ")
        
        if key == "q":
            break
        
        if key in MOVES:
            direction = MOVES[key]
            if is_valid_move(board, direction):
                make_move(board, direction)
                moves += 1
        
        if is_solved(board):
            draw_game(board, moves)
            print("=== VICTOIRE! ===")
            print(f"Puzzle résolu en {moves} coups!")
            print("=== nailec.fr ===")
            input("Appuyez sur Entrée pour continuer...")
            break

if __name__ == "__main__":
    main() 