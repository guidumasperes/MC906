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

from random import randrange
from turtle import *
from freegames import vector
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class Game:
    def __init__(self, ceil, ground, vy, tapY_mov, obstacle_diameter, refresh_timeout_ms, obstac_spawn_rate, obstacle_speed):
        self.bird = vector(0, 0)
        self.balls = []
        self.ceil = ceil
        self.ground = ground
        self.vy = vy
        self.tapY_mov = tapY_mov
        self.obstacle_diam = obstacle_diameter
        self.refresh_timeout_ms = refresh_timeout_ms
        self.obsta_spawn_rate = obstac_spawn_rate
        self.obstacle_speed = obstacle_speed

    def play(self, player):
        wall = ctrl.Antecedent(np.arange(-201, 201, 1), 'wall')
        press = ctrl.Consequent(np.arange(0, 1.25, 0.25), 'press')
        wall.automf(3)

        press['no'] = fuzz.trimf(press.universe, [0, 0, 0.5])  # talvez de merda aqui#
        press["maybe"] = fuzz.trimf(press.universe, [0, 0.5, 1])
        press['yes'] = fuzz.trimf(press.universe, [0.5, 1, 1])

        rule1 = ctrl.Rule(wall['good'], press['no'])
        rule2 = ctrl.Rule(wall['poor'], press['yes'])
        rule3 = ctrl.Rule(wall['average'], press['no'])
        pressing_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
        pressing = ctrl.ControlSystemSimulation(pressing_ctrl)
        print('bird.y = ', self.bird.y)
        pressing.input['wall'] = self.bird.y
        pressing.compute()
        print(pressing.output['press'])
        if pressing.output['press'] > 0.6:
            self.tap()

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
            dot(10, 'green')
        else:
            dot(10, 'red')

        for ball in balls:
            goto(ball.x, ball.y)
            dot(20, 'black')

        update()

    def move(self):
        "Update object positions."
        self.bird.y -= 5

        for ball in self.balls:
            ball.x -= 3

        if randrange(10) == 0:
            y = randrange(-199, 199)
            ball = vector(199, y)
            self.balls.append(ball)

        while len(self.balls) > 0 and not inside(self.balls[0]):
            self.balls.pop(0)

        if not inside(bird):
            draw(False)
            return

        for ball in self.balls:
            if abs(ball - self.bird) < 15:
                draw(False)
                return

        draw(True)
        fuzzy_play()
        ontimer(move, self.refresh_timeout_ms)

    setup(420, 420, 370, 0)
    hideturtle()
    up()
    tracer(False)
    move()
    done()
