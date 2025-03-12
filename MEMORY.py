import random
import time

# Configuration
WIDTH = 4
HEIGHT = 4
HIDDEN = "?"
SYMBOLS = ["A", "B", "C", "D", "E", "F", "G", "H"]

class Card:
    def __init__(self, symbol):
        self.symbol = symbol
        self.revealed = False

def clear_screen():
    print("\n" * 10)

def create_board():
    symbols = SYMBOLS * 2
    random.shuffle(symbols)
    board = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            row.append(Card(symbols[i * WIDTH + j]))
        board.append(row)
    return board

def draw_game(board, score, moves):
    clear_screen()
    print("=== MEMORY - nailec.fr ===")
    print(f"Score: {score} | Coups: {moves}")
    print("  " + " ".join(str(i) for i in range(WIDTH)))
    for i, row in enumerate(board):
        print(f"{i} " + " ".join(card.symbol if card.revealed else HIDDEN for card in row))

def get_card_position():
    while True:
        try:
            pos = input("Position (ligne colonne): ").split()
            if len(pos) != 2:
                continue
            row, col = map(int, pos)
            if 0 <= row < HEIGHT and 0 <= col < WIDTH:
                return row, col
        except ValueError:
            continue

def main():
    board = create_board()
    score = 0
    moves = 0
    pairs_found = 0
    
    print("=== MEMORY by nailec.fr ===")
    print("Trouvez les paires de symboles!")
    print("Format: 'ligne colonne' (ex: '1 2')")
    input("Appuyez sur Entrée pour commencer...")
    
    while pairs_found < len(SYMBOLS):
        draw_game(board, score, moves)
        
        # Premier choix
        while True:
            row1, col1 = get_card_position()
            if not board[row1][col1].revealed:
                break
            print("Cette carte est déjà révélée!")
        
        board[row1][col1].revealed = True
        draw_game(board, score, moves)
        
        # Deuxième choix
        while True:
            row2, col2 = get_card_position()
            if not board[row2][col2].revealed and (row1 != row2 or col1 != col2):
                break
            print("Choix invalide!")
        
        board[row2][col2].revealed = True
        draw_game(board, score, moves)
        moves += 1
        
        # Vérifier la paire
        if board[row1][col1].symbol == board[row2][col2].symbol:
            print("Paire trouvée!")
            score += 10
            pairs_found += 1
        else:
            print("Pas de paire...")
            time.sleep(1)
            board[row1][col1].revealed = False
            board[row2][col2].revealed = False
        
        input("Appuyez sur Entrée pour continuer...")
    
    print("=== VICTOIRE! ===")
    print(f"Score final: {score}")
    print(f"Nombre de coups: {moves}")
    print("=== nailec.fr ===")
    input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main() 