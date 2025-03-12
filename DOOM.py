import math
import time

# Configuration
WIDTH = 21
HEIGHT = 15
FOV = 60  # Champ de vision en degrés
DEPTH = 8  # Profondeur de rendu maximale
MOVE_SPEED = 0.5
ROTATION_SPEED = 10

# Caractères pour le rendu
WALL_CHARS = "█▓▒░ "  # Du plus proche au plus loin
ENEMY_CHAR = "M"
WEAPON_CHAR = "⌐╛"
EMPTY = " "

# Carte du niveau (0 = vide, 1 = mur, 2 = ennemi)
MAP = [
    [1,1,1,1,1,1,1,1],
    [1,0,0,0,0,2,0,1],
    [1,0,1,0,1,0,0,1],
    [1,0,0,0,0,0,2,1],
    [1,0,1,0,1,0,0,1],
    [1,0,0,2,0,0,0,1],
    [1,0,1,0,1,0,0,1],
    [1,1,1,1,1,1,1,1]
]

class Player:
    def __init__(self):
        self.x = 1.5
        self.y = 1.5
        self.angle = 0
        self.health = 100
        self.ammo = 50
        self.score = 0

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.is_alive = True

class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.load_enemies()
        self.frame_buffer = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
        
    def load_enemies(self):
        for y in range(len(MAP)):
            for x in range(len(MAP[0])):
                if MAP[y][x] == 2:
                    self.enemies.append(Enemy(x + 0.5, y + 0.5))

    def cast_ray(self, angle):
        # Calcul des composantes du rayon
        ray_x = math.cos(math.radians(angle))
        ray_y = math.sin(math.radians(angle))
        
        # Position actuelle
        pos_x = self.player.x
        pos_y = self.player.y
        
        distance = 0
        hit_enemy = None
        
        while distance < DEPTH:
            # Avancer le rayon
            pos_x += ray_x * 0.1
            pos_y += ray_y * 0.1
            distance += 0.1
            
            # Vérifier collision avec mur
            map_x = int(pos_x)
            map_y = int(pos_y)
            
            if MAP[map_y][map_x] == 1:
                return distance, None
            
            # Vérifier collision avec ennemis
            for enemy in self.enemies:
                if enemy.is_alive:
                    dx = pos_x - enemy.x
                    dy = pos_y - enemy.y
                    dist_to_enemy = math.sqrt(dx*dx + dy*dy)
                    if dist_to_enemy < 0.5:
                        return distance, enemy
                        
        return DEPTH, None

    def render_frame(self):
        # Effacer le buffer
        self.frame_buffer = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
        
        # Calculer les rayons
        for x in range(WIDTH):
            # Calculer l'angle du rayon
            ray_angle = self.player.angle - FOV/2 + (x/WIDTH) * FOV
            
            # Lancer le rayon
            distance, enemy = self.cast_ray(ray_angle)
            
            # Calculer la hauteur de la colonne
            wall_height = int((HEIGHT / distance) * 2)
            if wall_height > HEIGHT:
                wall_height = HEIGHT
                
            # Dessiner la colonne
            start = (HEIGHT - wall_height) // 2
            end = start + wall_height
            
            # Choisir le caractère en fonction de la distance
            char_index = int((distance / DEPTH) * (len(WALL_CHARS) - 1))
            wall_char = WALL_CHARS[char_index]
            
            # Dessiner le mur ou l'ennemi
            for y in range(HEIGHT):
                if y < start:  # Ciel
                    self.frame_buffer[y][x] = EMPTY
                elif y < end:  # Mur ou ennemi
                    if enemy and enemy.is_alive:
                        self.frame_buffer[y][x] = ENEMY_CHAR
                    else:
                        self.frame_buffer[y][x] = wall_char
                else:  # Sol
                    self.frame_buffer[y][x] = EMPTY
                    
        # Dessiner l'arme
        weapon_y = HEIGHT - 2
        weapon_x = WIDTH // 2 - 1
        self.frame_buffer[weapon_y][weapon_x] = WEAPON_CHAR[0]
        self.frame_buffer[weapon_y][weapon_x + 1] = WEAPON_CHAR[1]

    def move_player(self, direction):
        new_x = self.player.x
        new_y = self.player.y
        
        if direction == "8":  # Avancer
            new_x += math.cos(math.radians(self.player.angle)) * MOVE_SPEED
            new_y += math.sin(math.radians(self.player.angle)) * MOVE_SPEED
        elif direction == "2":  # Reculer
            new_x -= math.cos(math.radians(self.player.angle)) * MOVE_SPEED
            new_y -= math.sin(math.radians(self.player.angle)) * MOVE_SPEED
        elif direction == "4":  # Tourner à gauche
            self.player.angle -= ROTATION_SPEED
        elif direction == "6":  # Tourner à droite
            self.player.angle += ROTATION_SPEED
            
        # Vérifier les collisions
        if MAP[int(new_y)][int(new_x)] != 1:
            self.player.x = new_x
            self.player.y = new_y

    def shoot(self):
        if self.player.ammo <= 0:
            return False
            
        self.player.ammo -= 1
        
        # Vérifier si un ennemi est touché
        distance, enemy = self.cast_ray(self.player.angle)
        if enemy and enemy.is_alive and distance < 5:
            enemy.health -= 50
            if enemy.health <= 0:
                enemy.is_alive = False
                self.player.score += 100
            return True
            
        return False

def clear_screen():
    print("\n" * 10)

def draw_game(game):
    clear_screen()
    
    # Afficher le HUD
    print(f"=== DOOM - nailec.fr ===")
    print(f"Vie: {game.player.health} | Munitions: {game.player.ammo} | Score: {game.player.score}")
    
    # Afficher le monde 3D
    for row in game.frame_buffer:
        print("".join(row))
        
    # Afficher les contrôles
    print("8: Avancer | 2: Reculer")
    print("4: Gauche | 6: Droite")
    print("5: Tirer | q: Quitter")

def main():
    game = Game()
    
    print("=== DOOM by nailec.fr ===")
    print("8: Avancer, 2: Reculer")
    print("4: Gauche, 6: Droite")
    print("5: Tirer, q: Quitter")
    input("Appuyez sur Entrée pour commencer...")
    
    while True:
        game.render_frame()
        draw_game(game)
        
        if game.player.health <= 0:
            print("=== GAME OVER ===")
            print(f"Score final: {game.player.score}")
            print("=== nailec.fr ===")
            break
            
        # Vérifier la victoire (tous les ennemis éliminés)
        if all(not enemy.is_alive for enemy in game.enemies):
            print("=== VICTOIRE! ===")
            print(f"Score final: {game.player.score}")
            print("=== nailec.fr ===")
            break
        
        action = input("Action: ")
        
        if action == "q":
            break
        elif action in ["8", "2", "4", "6"]:
            game.move_player(action)
        elif action == "5":
            game.shoot()
        
        time.sleep(0.1)

if __name__ == "__main__":
    main() 
