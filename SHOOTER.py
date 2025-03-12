import random
import time

# Configuration
WIDTH = 21
HEIGHT = 7
PLAYER_CHAR = "A"
ENEMY_CHAR = "V"
BULLET_CHAR = "|"
EXPLOSION_CHAR = "*"

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 1
        self.bullets = []
        self.score = 0

class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH-1)
        self.y = 0
        self.direction = random.choice([-1, 1])

def clear_screen():
    print("\n" * 10)

def draw_game(player, enemies, explosions):
    clear_screen()
    board = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # Dessiner le joueur
    board[player.y][player.x] = PLAYER_CHAR
    
    # Dessiner les balles
    for bullet in player.bullets:
        if 0 <= bullet[1] < HEIGHT:
            board[bullet[1]][bullet[0]] = BULLET_CHAR
    
    # Dessiner les ennemis
    for enemy in enemies:
        if 0 <= enemy.y < HEIGHT:
            board[enemy.y][enemy.x] = ENEMY_CHAR
    
    # Dessiner les explosions
    for exp in explosions:
        if 0 <= exp[1] < HEIGHT:
            board[exp[1]][exp[0]] = EXPLOSION_CHAR
    
    # Afficher le score
    print("=== SPACE SHOOTER - nailec.fr ===")
    print(f"Score: {player.score}")
    
    # Afficher le plateau
    for row in board:
        print("".join(row))

def main():
    player = Player()
    enemies = [Enemy()]
    explosions = []
    game_over = False
    
    print("=== SPACE SHOOTER by nailec.fr ===")
    input("Appuyez sur Entrée pour commencer...")
    
    while not game_over:
        draw_game(player, enemies, explosions)
        
        # Contrôles
        key = input("4:gauche, 6:droite, 8:tirer, q:quitter: ")
        
        if key == "q":
            break
        elif key == "4" and player.x > 0:
            player.x -= 1
        elif key == "6" and player.x < WIDTH-1:
            player.x += 1
        elif key == "8":
            player.bullets.append([player.x, player.y-1])
        
        # Mise à jour des balles
        new_bullets = []
        for bullet in player.bullets:
            bullet[1] -= 1
            if bullet[1] >= 0:
                new_bullets.append(bullet)
        player.bullets = new_bullets
        
        # Mise à jour des ennemis
        if random.random() < 0.1:  # 10% de chance d'ajouter un nouvel ennemi
            enemies.append(Enemy())
        
        new_enemies = []
        for enemy in enemies:
            enemy.x += enemy.direction
            if enemy.x <= 0 or enemy.x >= WIDTH-1:
                enemy.direction *= -1
                enemy.y += 1
            
            if enemy.y >= HEIGHT-1:
                game_over = True
                break
                
            new_enemies.append(enemy)
        enemies = new_enemies
        
        # Collisions
        new_enemies = []
        for enemy in enemies:
            hit = False
            new_bullets = []
            for bullet in player.bullets:
                if bullet[0] == enemy.x and bullet[1] == enemy.y:
                    hit = True
                    explosions.append([enemy.x, enemy.y])
                    player.score += 10
                else:
                    new_bullets.append(bullet)
            player.bullets = new_bullets
            if not hit:
                new_enemies.append(enemy)
        enemies = new_enemies
        
        # Mise à jour des explosions
        explosions = [[x, y] for x, y in explosions if y >= 0]
        for exp in explosions:
            exp[1] += 1
        explosions = [[x, y] for x, y in explosions if y < HEIGHT]
        
        time.sleep(0.1)
    
    print("=== GAME OVER ===")
    print(f"Score final: {player.score}")
    print("=== nailec.fr ===")
    input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main() 