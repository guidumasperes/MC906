from game.core import Game

if __name__ == '__main__':
    flappy_game = Game(200, -200, -5, 30, 20, 50, 1, -3, 0, 0, 5)
    flappy_game.main_looop()
