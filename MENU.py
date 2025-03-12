def clear_screen():
    print("\n" * 10)

def afficher_menu():
    clear_screen()
    print("=== MENU DES JEUX ===")
    print("1. Snake")
    print("2. Pong")
    print("3. Space Shooter")
    print("4. Tetris")
    print("5. Runner")
    print("6. Memory")
    print("7. Flappy Bird")
    print("8. Breakout")
    print("9. Mots Mêlés")
    print("10. Taquin")
    print("11. Pacman")
    print("12. 2048")
    print("13. DOOM")
    print("14. Quitter")
    print("==================")
    print("    nailec.fr")
    print("==================")
    return input("Choisissez un jeu (1-14): ")

def main():
    while True:
        choix = afficher_menu()
        
        if choix == "1":
            import SNAKE
            SNAKE.main()
        elif choix == "2":
            import PONG
            PONG.main()
        elif choix == "3":
            import SHOOTER
            SHOOTER.main()
        elif choix == "4":
            import TETRIS
            TETRIS.main()
        elif choix == "5":
            import RUNNER
            RUNNER.main()
        elif choix == "6":
            import MEMORY
            MEMORY.main()
        elif choix == "7":
            import FLAPPY
            FLAPPY.main()
        elif choix == "8":
            import BREAKOUT
            BREAKOUT.main()
        elif choix == "9":
            import WORDSEARCH
            WORDSEARCH.main()
        elif choix == "10":
            import PUZZLE
            PUZZLE.main()
        elif choix == "11":
            import PACMAN
            PACMAN.main()
        elif choix == "12":
            import G2048
            G2048.main()
        elif choix == "13":
            import DOOM
            DOOM.main()
        elif choix == "14":
            print("Au revoir!")
            print("nailec.fr")
            break
        else:
            print("Choix invalide!")
            input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main() 
