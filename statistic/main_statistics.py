# todo
# time alive x ball spawn time - data generated - graphic generated | DONE
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


# def __init__(self, ceil, ground, vy, tapY_mov, obstacle_diameter, refresh_timeout_ms, obstac_spawn_rate,
#                  obstacle_speed, birdx, birdy, proximity_threshold, extracting_metrics=False):
# matrix correlation spawn time, time alive,obstacle diameter, fall speed, obstacle speed, fall speed
def correlation_data():
    start_bird_y = randint(-199, 199)
    rand_density = randint(1, 9)
    obstacle_diameter = randint(10, 50)
    obstacle_speed = - randint(1, 5)
    fall_speed = - randint(10, 30)
    proximity = randint(2, 30)
    flappy_game = Game(200, -200, fall_speed, 30, obstacle_diameter, 1, rand_density, obstacle_speed, 0,
                       start_bird_y, proximity, True)
    flappy_game.game_main_loop()


def plot_spawn_time_metric():
    spt = []
    tal = []
    with open("data/spawnxtimealive", "r") as f:
        for line in f.readlines():
            data = line.strip().split(",")
            tal.append(round(float(data[0]), 3))
            spt.append(round(float(data[1]), 3))
    plt.title("tempo de colisão x taxa de geração de obstáculos")
    plt.ylabel("tempo para colidir (s)")
    plt.xlabel("chance de aparecimento de obstáculo por refresh(%)")
    plt.scatter(spt, tal, alpha=0.3)
    plt.savefig("plots/spawnxcolisao")


def plot_proximity_threshold_metric():
    prox = []
    tal = []
    with open("data/proximityxtimealive", "r") as f:
        for line in f.readlines():
            data = line.strip().split(",")
            tal.append(round(float(data[0]), 3))
            prox.append(round(float(data[1]), 3))
    plt.title("tempo de colisão x limite de proximidade do obstáculo")
    plt.ylabel("tempo para colidir (s)")
    plt.xlabel("limite de proximidade do obstáculo")
    plt.scatter(prox, tal, alpha=0.3, color='g')
    plt.savefig("plots/proximitycolisao")


def plot_box_plot_time_alive():
    tal = []
    with open("data/boxplotalive", "r") as f:
        for line in f.readlines():
            data = line.rstrip()
            tal.append(round(float(data), 3))
    plt.title("box plot, tempo de vida do pássaro")
    plt.ylabel("tempo de vida (s)")
    plt.boxplot(tal, 'red', 'tan')
    plt.savefig("plots/boxplotalive", alpha=0.5)


def histogram_coolision_plot():
    colision = []
    with open("data/colisioncoordinates", "r") as f:
        for line in f.readlines():
            data = line.rstrip()
            colision.append(round(float(data), 3))

    plt.title("histograma, coordenada y de colisão x número de colisões")
    plt.ylabel("numero de colisoes")
    plt.xlabel("coordenada y da colisão")
    plt.hist(colision)
    plt.savefig("plots/colisionhistogram")


def coefficients_correlations():
    # start_bird_y = randint(-199, 199)
    # rand_density = randint(1, 9)
    # obstacle_diameter = randint(10, 50)
    # obstacle_speed = - randint(1, 5)
    # fall_speed = - randint(10, 30)
    # proximity = randint(2, 30)
    # colision time
    with open("plots/correlations", "w") as output:
        with open("data/coeficientscorrelation") as input:
            bird_y = []
            rand_density = []
            obstacle_diameter = []
            obstacle_speed = []
            vy_bird = []
            proximity_th = []
            survival_time = []
            for line in input.readlines():
                data = line.strip().split(",")
                bird_y.append(round(float(data[0]), 3))
                rand_density.append(round(float(data[1]), 3))
                obstacle_diameter.append(round(float(data[2]), 3))
                obstacle_speed.append(round(float(data[3]), 3))
                vy_bird.append(round(float(data[4]), 3))
                proximity_th.append(round(float(data[5]), 3))
                survival_time.append(round(float(data[6]), 3))

            output.write("relacao entre posicao inicial do passaro (y) e tempo de sobrevivencia: {}\n".format(
                np.corrcoef(bird_y, survival_time)[0, 1]))
            output.write("relacao entre chance de spawn de bolas por timeout e tempo de sobrevivencia: {}\n".format(
                np.corrcoef(rand_density, survival_time)[0, 1]))
            output.write("relacao entre diametro dos obstaculos e tempo de sobrevivencia: {}\n".format(
                np.corrcoef(obstacle_diameter, survival_time)[0, 1]))
            output.write("relacao entre velocidade do obstaculo e tempo de sobrevivencia: {}\n".format(
                np.corrcoef(obstacle_speed, survival_time)[0, 1]))
            output.write("relacao entre velocidade do passaro (vy) e tempo de sobrevivencia: {}\n".format(
                np.corrcoef(vy_bird, survival_time)[0, 1]))
            output.write("relacao entre o threhold de proximidade do obstaculo e tempo de sobrevivencia: {}\n".format(
                np.corrcoef(proximity_th, survival_time)[0, 1]))


if __name__ == '__main__':
    # histogram_coolision_plot()
    # plot_box_plot_time_alive()
    plot_spawn_time_metric()
    # plot_proximity_threshold_metric()
    #coefficients_correlations()
