import random
import string

# Configuration
WIDTH = 10
HEIGHT = 10
WORDS = ["PYTHON", "CASIO", "JEUX", "CODE", "PROG"]

def clear_screen():
    print("\n" * 10)

def create_grid():
    # Créer une grille vide
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    placed_words = []
    
    # Placer les mots
    for word in WORDS:
        placed = False
        attempts = 50
        
        while not placed and attempts > 0:
            # Choisir une direction (horizontale ou verticale)
            direction = random.choice(["H", "V"])
            
            if direction == "H":
                x = random.randint(0, WIDTH - len(word))
                y = random.randint(0, HEIGHT - 1)
                can_place = all(grid[y][x+i] == " " for i in range(len(word)))
                
                if can_place:
                    for i, letter in enumerate(word):
                        grid[y][x+i] = letter
                    placed_words.append((word, y, x, "H"))
                    placed = True
            else:
                x = random.randint(0, WIDTH - 1)
                y = random.randint(0, HEIGHT - len(word))
                can_place = all(grid[y+i][x] == " " for i in range(len(word)))
                
                if can_place:
                    for i, letter in enumerate(word):
                        grid[y+i][x] = letter
                    placed_words.append((word, y, x, "V"))
                    placed = True
            
            attempts -= 1
    
    # Remplir les espaces vides avec des lettres aléatoires
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] == " ":
                grid[y][x] = random.choice(string.ascii_uppercase)
    
    return grid, placed_words

def draw_game(grid, found_words, score):
    clear_screen()
    print("=== MOTS MÊLÉS - nailec.fr ===")
    print(f"Score: {score}")
    print("\nMots à trouver:")
    for word in WORDS:
        status = "✓" if word in found_words else " "
        print(f"[{status}] {word}")
    
    print("\n  " + " ".join(str(i) for i in range(WIDTH)))
    for i, row in enumerate(grid):
        print(f"{i} " + " ".join(row))

def get_word_input():
    while True:
        try:
            print("\nFormat: 'mot ligne colonne direction'")
            print("Direction: H (horizontal) ou V (vertical)")
            inp = input("Votre réponse: ").upper().split()
            if len(inp) != 4:
                continue
            word, row, col, direction = inp
            row, col = int(row), int(col)
            if direction not in ["H", "V"]:
                continue
            return word, row, col, direction
        except ValueError:
            continue

def check_word(word, row, col, direction, grid, placed_words):
    for w, y, x, d in placed_words:
        if (w == word and y == row and x == col and d == direction):
            return True
    return False

def main():
    grid, placed_words = create_grid()
    found_words = set()
    score = 0
    
    print("=== MOTS MÊLÉS by nailec.fr ===")
    print("Trouvez les mots cachés!")
    print("q: Quitter")
    input("Appuyez sur Entrée pour commencer...")
    
    while len(found_words) < len(WORDS):
        draw_game(grid, found_words, score)
        
        inp = input("\nCommande (ou mot): ").upper()
        if inp == "Q":
            break
        
        try:
            word, row, col, direction = get_word_input()
            if word in WORDS and word not in found_words:
                if check_word(word, row, col, direction, grid, placed_words):
                    print("Mot trouvé!")
                    found_words.add(word)
                    score += len(word) * 10
                else:
                    print("Position incorrecte!")
            else:
                print("Mot invalide ou déjà trouvé!")
        except:
            print("Format invalide!")
        
        input("Appuyez sur Entrée pour continuer...")
    
    if len(found_words) == len(WORDS):
        print("=== VICTOIRE! ===")
    else:
        print("=== JEU TERMINÉ ===")
    print(f"Score final: {score}")
    print("=== nailec.fr ===")
    input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main() 