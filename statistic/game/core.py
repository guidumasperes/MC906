"""Flappy, game inspired by Flappy Bird.

Exercises

1. Keep score. -> point per time alive , f(t) = t*a, function
2. Vary the speed. -> alter obstacle speed
3. Vary the size of the balls -> alter obstacle diameter diameter.
4. Allow the bird to move forward and back
5 .change ball density spawn rate over time

ATTENTION!!!
The original code for this game is property of Grant Jenks https://github.com/grantjenks/free-python-games with all
rights reserved and for educational purposes was modified to implement fuzzy logic control system

"""
from time import time
from random import randrange
from turtle import *
from freegames import vector
from game.fuzzy_player import BasePlayer


# overlap


class Game:
    FLAPPY_DIAMETER = 10

    # spawn rate = 0 a 20 (0% a 100% - >) inteiros
    def __init__(self, ceil, ground, vy, tapY_mov, obstacle_diameter, refresh_timeout_ms, obstac_spawn_rate,
                 obstacle_speed, birdx, birdy, proximity_threshold, extracting_metrics=False):
        self.start_birdx = birdx
        self.start_birdy = birdy
        self.time = time()
        self.in_game = True
        self.bird = vector(birdx, birdy)
        self.proximity_threshold = proximity_threshold
        self.balls = []
        self.ceil = ceil
        self.ground = ground
        self.vy = vy
        self.tapY_mov = tapY_mov
        self.obstacle_diam = obstacle_diameter
        self.refresh_timeout_ms = refresh_timeout_ms
        self.obsta_spawn_rate = obstac_spawn_rate
        self.obstacle_speed = obstacle_speed
        self.player = BasePlayer(self)

    def play(self):
        self.player.perform_a_play()

    # initially, by deafault, the balls that are considered a threaten to 'flappy' are only the
    # ones in the range of colision only taking the X coordinate into account.

    def tap(self):
        "Move bird up in response to screen tap."
        up = vector(0, self.tapY_mov)
        self.bird.move(up)

    def inside(self, point):
        "Return True if point on screen."
        return self.ground < point.x < self.ceil and self.ground < point.y < self.ceil

    def draw(self, alive):
        "Draw screen objects."
        clear()

        goto(self.bird.x, self.bird.y)

        if alive:
            dot(self.FLAPPY_DIAMETER, 'green')
        else:
            dot(self.FLAPPY_DIAMETER, 'red')

        for ball in self.balls:
            goto(ball.x, ball.y)
            dot(self.obstacle_diam, 'black')

        update()

    def move(self):
        "Update object positions."
        self.bird.y += self.vy  # -5

        for ball in self.balls:
            ball.x += self.obstacle_speed  # -3

        if randrange(20) <= self.obsta_spawn_rate:
            y = randrange(self.ground + 1, self.ceil - 1)
            ball = vector(self.ceil - 1, y)
            self.balls.append(ball)

        while len(self.balls) > 0 and not self.inside(self.balls[0]):
            self.balls.pop(0)

        if not self.inside(self.bird):
            self.draw(False)
            self.in_game = False
            self.time = time() - self.time
            with open('data/coeficientscorrelation', 'a') as f:
                f.write("{},{},{},{},{},{},{}\n".format(self.start_birdy, self.obsta_spawn_rate,
                                                        self.obstacle_diam, self.obstacle_speed, self.vy,
                                                        self.proximity_threshold, self.time))

                f.flush()
                f.close()
                print("escrevi")
            return

        for ball in self.balls:
            if abs(ball - self.bird) < self.obstacle_diam / 2 + 5:
                self.draw(False)
                self.time = time() - self.time
                with open('data/coeficientscorrelation', 'a') as f:
                    f.write(
                        "{},{},{},{},{},{},{}\n".format(self.start_birdy, self.obsta_spawn_rate,
                                                        self.obstacle_diam, self.obstacle_speed, self.vy,
                                                        self.proximity_threshold, self.time))

                    f.flush()
                    f.close()
                    print("escrevi")
                return

        self.draw(True)
        self.play()
        ontimer(self.move, self.refresh_timeout_ms)

    def game_main_loop(self):
        setup(420, 420, 370, 0)
        hideturtle()
        up()
        tracer(False)
        y = randrange(self.ground + 1, self.ceil - 1)
        ball = vector(self.ceil - 1, y)
        self.balls.append(ball)
        self.move()
        done()
