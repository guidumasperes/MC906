"""Flappy, game inspired by Flappy Bird.

Exercises

1. Keep score.
2. Vary the speed.
3. Vary the size of the balls.
4. Allow the bird to move forward and back.

ATTENTION!!!
The original code for this game is property of Grant Jenks https://github.com/grantjenks/free-python-games with all
rights reserved and for educational purposes was modified to implement fuzzy logic control system

"""
from random import *
from turtle import *
from freegames import vector
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


bird = vector(0, 0)
balls = []

def fuzzy_play():
    teto = ctrl.Antecedent(np.arange(-201, 201, 1), 'teto')
    chao = ctrl.Antecedent(np.arange(-201, 201, 1), 'chao')
    press = ctrl.Consequent(np.arange(0, 2, 1), 'press')
    teto.automf(3)
    chao.automf(3)
    press['no'] = fuzz.trimf(press.universe, [0, 0, 1]) #talvez de merda aqui#
    press['yes'] = fuzz.trimf(press.universe, [0, 1, 1])
    rule1 = ctrl.Rule(teto['good'], press['no'])
    rule2 = ctrl.Rule(chao['poor'], press['yes'])
    pressing_ctrl = ctrl.ControlSystem([rule1, rule2])
    pressing = ctrl.ControlSystemSimulation(pressing_ctrl)
    print('bird.y = ', bird.y)
    pressing.input['teto'] = bird.y
    pressing.input['chao'] = bird.y
    pressing.compute()
    print(pressing.output['press'])
    if pressing.output['press'] > 0.6:
        tap()

def tap():
    "Move bird up in response to screen tap."
    up = vector(0, 30)
    bird.move(up)

def inside(point):
    "Return True if point on screen."
    return -200 < point.x < 200 and -200 < point.y < 200

def draw(alive):
    "Draw screen objects."
    clear()

    goto(bird.x, bird.y)

    if alive:
        dot(10, 'green')
    else:
        dot(10, 'red')

    for ball in balls:
        goto(ball.x, ball.y)
        dot(20, 'black')

    update()

def move():
    "Update object positions."
    bird.y -= 5

    for ball in balls:
        ball.x -= 3

    if randrange(10) == 0:
        y = randrange(-199, 199)
        ball = vector(199, y)
        balls.append(ball)

    while len(balls) > 0 and not inside(balls[0]):
        balls.pop(0)

    if not inside(bird):
        draw(False)
        return

    for ball in balls:
        if abs(ball - bird) < 15:
            draw(False)
            return

    draw(True)
    fuzzy_play()
    ontimer(move, 50)

setup(420, 420, 370, 0)
hideturtle()
up()
tracer(False)
move()
done()
