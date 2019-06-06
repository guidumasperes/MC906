# todo
# time alive x ball spawn time - data generated
# time alive x proximity threshold - data generated
# box plot time alive % percentage  - data generated
# heat map colision times per coordinate (hexagon plot) - data generated
# matrix correlation spawn time, time alive,obstacle diameter, fall speed, obstacle speed, fall speed

from matplotlib import pyplot as plt
from game.core import Game
from random import randint
from scipy.stats import gaussian_kde
import numpy as np
import sys

"""
hexbin is an axes method or pyplot function that is essentially
a pcolor of a 2-D histogram with hexagonal cells.  It can be
much more informative than a scatter plot; in the first subplot
below, try substituting 'scatter' for 'hexbin'.
"""


def time_alive_per_obstacle_spawn_time():
    rand_density = randint(1, 8)
    flappy_game = Game(200, -200, -5, 30, 20, 1, rand_density, -3, 0, 0, 5, True)
    flappy_game.game_main_loop()

def time_alive_proximity_threshold():
    proximity = randint(1, 70)
    flappy_game = Game(200, -200, -5, 30, 20, 1, 1, -3, 0, 0, proximity, True)
    flappy_game.game_main_loop()

def time_alive_box_plot():
    flappy_game = Game(200, -200, -5, 30, 20, 1, 1, -3, 0, 0, 5, True)
    flappy_game.game_main_loop()

def colision_coordinates_plot():
    flappy_game = Game(200, -200, -5, 30, 20, 1, 1, -3, 0, 0, 5, True)
    flappy_game.game_main_loop()

def plot_spawn_time_metric():
    spt = []
    tal = []
    with open("data/spawnxtimealive","r") as f:
        for line in f.readlines():
            data = line.split(",")
            tal.append(data[0])
            spt.append(data[1])

    plt.scatter(spt, tal, alpha=0.5)
    plt.show()

if __name__ == '__main__':
    plot_spawn_time_metric()
