import random
import time

# Configuration
GRID_SIZE = 4
EMPTY = 0

def clear_screen():
    print("\n" * 10)

class Game2048:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) 
                      if self.grid[i][j] == EMPTY]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        moved = False
        if direction in ["8", "2"]:  # Vertical
            for j in range(GRID_SIZE):
                column = [self.grid[i][j] for i in range(GRID_SIZE)]
                if direction == "2":  # Bas
                    column.reverse()
                new_column, score = self.merge(column)
                if direction == "2":
                    new_column.reverse()
                if new_column != [self.grid[i][j] for i in range(GRID_SIZE)]:
                    moved = True
                    for i in range(GRID_SIZE):
                        self.grid[i][j] = new_column[i]
                self.score += score

        elif direction in ["4", "6"]:  # Horizontal
            for i in range(GRID_SIZE):
                row = self.grid[i][:]
                if direction == "6":  # Droite
                    row.reverse()
                new_row, score = self.merge(row)
                if direction == "6":
                    new_row.reverse()
                if new_row != self.grid[i]:
                    moved = True
                    self.grid[i] = new_row
                self.score += score

        return moved

    def merge(self, line):
        # Supprimer les zéros
        line = [x for x in line if x != EMPTY]
        score = 0
        
        # Fusion des tuiles identiques
        i = 0
        while i < len(line) - 1:
            if line[i] == line[i + 1]:
                line[i] *= 2
                score += line[i]
                line.pop(i + 1)
            i += 1
        
        # Compléter avec des zéros
        while len(line) < GRID_SIZE:
            line.append(EMPTY)
            
        return line, score

    def is_game_over(self):
        # Vérifier s'il y a des cases vides
        if any(EMPTY in row for row in self.grid):
            return False

        # Vérifier s'il y a des mouvements possibles
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 1):
                # Vérifier horizontalement
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                # Vérifier verticalement
                if self.grid[j][i] == self.grid[j + 1][i]:
                    return False
        return True

    def has_won(self):
        return any(2048 in row for row in self.grid)

def format_number(n):
    if n == 0:
        return "    "
    return f"{n:4d}"

def draw_game(game):
    clear_screen()
    print("=== 2048 - nailec.fr ===")
    print(f"Score: {game.score}")
    print("┌────┬────┬────┬────┐")
    for i, row in enumerate(game.grid):
        print("│" + "│".join(format_number(cell) for cell in row) + "│")
        if i < GRID_SIZE - 1:
            print("├────┼────┼────┼────┤")
    print("└────┴────┴────┴────┘")

def main():
    game = Game2048()
    
    print("=== 2048 by nailec.fr ===")
    print("8: Haut, 2: Bas")
    print("4: Gauche, 6: Droite")
    print("q: Quitter")
    input("Appuyez sur Entrée pour commencer...")
    
    while True:
        draw_game(game)
        
        if game.has_won():
            print("=== VICTOIRE! ===")
            print(f"Score final: {game.score}")
            print("=== nailec.fr ===")
            break
            
        if game.is_game_over():
            print("=== GAME OVER ===")
            print(f"Score final: {game.score}")
            print("=== nailec.fr ===")
            break
        
        move = input("Direction: ")
        if move == "q":
            break
        elif move in ["8", "2", "4", "6"]:
            if game.move(move):
                game.add_new_tile()
        
        time.sleep(0.1)

if __name__ == "__main__":
    main() 