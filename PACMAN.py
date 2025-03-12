import random
import time

# Configuration
WIDTH = 21
HEIGHT = 15
PACMAN = "C"
GHOST = "M"
DOT = "·"
POWER = "o"
WALL = "█"
EMPTY = " "

# Directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

# Labyrinthe prédéfini
MAZE = [
    "█████████████████████",
    "█·····█·····█·····█",
    "█o███·█████·█·███o█",
    "█·················█",
    "█·███·█·███·█·███·█",
    "█·····█··█··█·····█",
    "█████·███·███·█████",
    "    █·█·····█·█    ",
    "█████·█ ███ █·█████",
    "█·········M·······█",
    "█████·█ ███ █·█████",
    "    █·█·····█·█    ",
    "█████·█████·█·█████",
    "█o····················o█",
    "█████████████████████"
]

class Entity:
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char
        self.direction = RIGHT
        self.scared = False

class Game:
    def __init__(self):
        self.board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.pacman = None
        self.ghosts = []
        self.score = 0
        self.dots_remaining = 0
        self.power_mode = 0
        self.load_maze()

    def load_maze(self):
        for y, row in enumerate(MAZE):
            for x, char in enumerate(row):
                if char == "M":
                    ghost = Entity(x, y, GHOST)
                    self.ghosts.append(ghost)
                    self.board[y][x] = EMPTY
                elif char == "C":
                    self.pacman = Entity(x, y, PACMAN)
                    self.board[y][x] = EMPTY
                else:
                    self.board[y][x] = char
                    if char == DOT or char == POWER:
                        self.dots_remaining += 1
        
        if not self.pacman:
            # Position par défaut pour Pacman si non défini
            self.pacman = Entity(1, 1, PACMAN)
        
        # Ajouter plus de fantômes si nécessaire
        while len(self.ghosts) < 4:
            x, y = self.find_empty_spot()
            self.ghosts.append(Entity(x, y, GHOST))

    def find_empty_spot(self):
        while True:
            x = random.randint(1, WIDTH-2)
            y = random.randint(1, HEIGHT-2)
            if self.board[y][x] not in [WALL, POWER] and (x, y) != (self.pacman.x, self.pacman.y):
                return x, y

    def move_entity(self, entity, direction):
        new_x = entity.x + direction[1]
        new_y = entity.y + direction[0]
        
        # Traverser les tunnels
        if new_x < 0:
            new_x = WIDTH - 1
        elif new_x >= WIDTH:
            new_x = 0
        
        if 0 <= new_y < HEIGHT and self.board[new_y][new_x] != WALL:
            entity.x = new_x
            entity.y = new_y
            return True
        return False

    def move_ghost(self, ghost):
        if random.random() < 0.2:  # 20% de chance de changer de direction aléatoirement
            ghost.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        
        if not self.move_entity(ghost, ghost.direction):
            # Si bloqué, essayer une autre direction
            directions = [UP, DOWN, LEFT, RIGHT]
            random.shuffle(directions)
            for direction in directions:
                if self.move_entity(ghost, direction):
                    ghost.direction = direction
                    break

    def update(self):
        # Mettre à jour le mode power
        if self.power_mode > 0:
            self.power_mode -= 1
            if self.power_mode == 0:
                for ghost in self.ghosts:
                    ghost.scared = False
        
        # Déplacer les fantômes
        for ghost in self.ghosts:
            self.move_ghost(ghost)
            
            # Vérifier collision avec Pacman
            if (ghost.x == self.pacman.x and ghost.y == self.pacman.y):
                if ghost.scared:
                    ghost.x, ghost.y = self.find_empty_spot()
                    self.score += 200
                else:
                    return False  # Game Over
        
        # Collecter les points
        current_cell = self.board[self.pacman.y][self.pacman.x]
        if current_cell == DOT:
            self.board[self.pacman.y][self.pacman.x] = EMPTY
            self.score += 10
            self.dots_remaining -= 1
        elif current_cell == POWER:
            self.board[self.pacman.y][self.pacman.x] = EMPTY
            self.score += 50
            self.dots_remaining -= 1
            self.power_mode = 25  # Durée du mode power
            for ghost in self.ghosts:
                ghost.scared = True
        
        return True

def clear_screen():
    print("\n" * 10)

def draw_game(game):
    clear_screen()
    print("=== PACMAN - nailec.fr ===")
    print(f"Score: {game.score}")
    
    # Créer une copie du plateau pour l'affichage
    display = [row[:] for row in game.board]
    
    # Ajouter les entités
    display[game.pacman.y][game.pacman.x] = game.pacman.char
    for ghost in game.ghosts:
        display[ghost.y][ghost.x] = "W" if ghost.scared else ghost.char
    
    # Afficher le plateau
    for row in display:
        print("".join(row))

def main():
    game = Game()
    
    print("=== PACMAN by nailec.fr ===")
    print("8: Haut, 2: Bas")
    print("4: Gauche, 6: Droite")
    print("q: Quitter")
    input("Appuyez sur Entrée pour commencer...")
    
    while True:
        draw_game(game)
        
        if game.dots_remaining == 0:
            print("=== VICTOIRE! ===")
            print(f"Score final: {game.score}")
            print("=== nailec.fr ===")
            break
        
        # Gestion des touches
        key = input("Direction: ")
        
        if key == "q":
            break
        elif key == "8":
            game.pacman.direction = UP
        elif key == "2":
            game.pacman.direction = DOWN
        elif key == "4":
            game.pacman.direction = LEFT
        elif key == "6":
            game.pacman.direction = RIGHT
        
        # Déplacer Pacman
        game.move_entity(game.pacman, game.pacman.direction)
        
        # Mettre à jour le jeu
        if not game.update():
            print("=== GAME OVER ===")
            print(f"Score final: {game.score}")
            print("=== nailec.fr ===")
            break
        
        time.sleep(0.1)

if __name__ == "__main__":
    main() 