# the idea here is to make many players , not just one, in order to test different approaches.


import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl
from freegames import vector

# this player doesn'take left movimentation in account when making a decision.
class BasePlayer:

    def __init__(self, game):
        self.game = game
        self.wall = self._wall_antecedent()
        self.tap_ball_threat, self.no_tap_ball_threat = self._threatening_balls_antecedents(game.proximity_threshold)
        self.rules = []

    def perform_a_play(self):
        self.proximity = self._ball_proximity_antecedent()
        press = ctrl.Consequent(np.arange(0, 11, 1), 'press')
        press['no'] = fuzz.trimf(press.universe, [0, 0, 0.5])
        press["maybe"] = fuzz.trimf(press.universe, [0.4, 0.5, 0.5])
        press['yes'] = fuzz.trimf(press.universe, [0.5, 1, 1])
        rules = self.generate_rules(press)
        pressing_ctrl = ctrl.ControlSystem(rules)
        pressing = ctrl.ControlSystemSimulation(pressing_ctrl)
        pressing.input['wall'] = self.game.bird.y
        no_tap_dist, tap_dist = self._distance_nearest_ball()
        pressing.input['no_tap_bad'] = no_tap_dist  # parameter = the distance to the nearest ball if no tap is performed
        pressing.input['tap_bad'] = tap_dist  # parameter =  the distance to the nearest ball if tap no tap is performed
        pressing.input['proximity'] = self._sum_distance_to_obstacles(self.game.bird, after_timeout=False) # proximity = the actual sum of the distance to all points
        pressing.compute()
        if pressing.output['press'] > 0.5:
            self.game.tap()

    def _wall_antecedent(self):
        wall = ctrl.Antecedent(np.arange(self.game.ground, self.game.ceil, 100), "wall")
        wall.automf(3)
        return wall

    # rule to maximize the distance between Flap and obstacles
    # 2 possibilities, tap or dont tap -> either way the distance will increase or decrease
    # the possibility to go up has the most significative difference in distance , because vy < vytap
    # the the minimal interval is the min dont tap variation and the maximum is the tap variation, the step is one

    def _ball_proximity_antecedent(self):
        bird_after_tap = self.game.bird + vector(0, self.game.vy + self.game.tapY_mov)
        distance_with_tap = self._sum_distance_to_obstacles(bird_after_tap, True)
        bird_after_no_tap = self.game.bird + vector(0, self.game.vy)
        distance_without_tap = self._sum_distance_to_obstacles(bird_after_no_tap, True)

        self.greater_distance_tap = False

        if distance_without_tap > distance_with_tap:
            proximity = ctrl.Antecedent(np.arange(0, distance_without_tap, distance_with_tap), 'proximity')


        else:
            proximity = ctrl.Antecedent(np.arange(0, distance_with_tap, distance_without_tap), 'proximity')
            self.greater_distance_tap = True

        proximity.automf(3)
        return proximity

    def _threatening_balls_antecedents(self, proximity_threshold):
        proximity_range = self.game.obstacle_diam / 2 + proximity_threshold
        no_tap_ball_threat = ctrl.Antecedent(np.arange(0, proximity_range * 4, proximity_range), 'no_tap_bad')
        no_tap_ball_threat.automf(3)
        tap_threat = ctrl.Antecedent(np.arange(0, proximity_range * 4, proximity_range), 'tap_bad')
        tap_threat.automf(3)
        return no_tap_ball_threat, tap_threat

    def _distance_nearest_ball(self):
        tap_option_no = vector(self.game.bird.x, self.game.bird.y + self.game.vy)
        tap_option_yes = vector(self.game.bird.x, self.game.bird.y + self.game.vy + self.game.tapY_mov)
        absolute_distance_tp_no = lambda ball: abs(ball - tap_option_no)
        absolute_distance_tp_yes = lambda ball: abs(ball - tap_option_yes)
        balls_in_front = lambda ball: ball.x + self.game.obstacle_diam/2 >= self.game.bird.x + self.game.FLAPPY_DIAMETER/2
        balls_after_tic = (map(lambda ball: ball + vector(self.game.obstacle_speed, 0), self.game.balls))
        balls_in_front_after_tic = list(filter(balls_in_front, balls_after_tic))

        if len(balls_in_front_after_tic) == 0:
            balls_in_front_after_tic = balls_after_tic

        no_tap_dist = abs(min(balls_in_front_after_tic, key=absolute_distance_tp_no))
        tap_dist = abs(min(balls_in_front_after_tic, key=absolute_distance_tp_yes))
        return no_tap_dist, tap_dist

    def generate_rules(self, press):
        no_tap_bad_rule = ctrl.Rule(self.no_tap_ball_threat['poor'], press['yes'])
        tap_bad_rule = ctrl.Rule(self.tap_ball_threat['poor'], press['no'])
        wall_rule_1 = ctrl.Rule(self.wall['poor'], press['yes'])
        wall_rule_2 = ctrl.Rule(self.wall['good'], press['no'])
        composed_proximity_predicate = self.tap_ball_threat['average'] or self.tap_ball_threat['good']
        composed_proximity_predicate = composed_proximity_predicate and (self.no_tap_ball_threat['average'] or self.no_tap_ball_threat['good'])
        conditionalTap = press["yes"] if self.greater_distance_tap else press["no"]
        proximity_rule = ctrl.Rule((composed_proximity_predicate and self.proximity['poor']), conditionalTap)
        rules = [no_tap_bad_rule, tap_bad_rule, wall_rule_1, wall_rule_2, proximity_rule]
        return rules

    def _sum_distance_to_obstacles(self, bird, after_timeout=False):
        dist = 0
        for ball in self.game.balls:
            if after_timeout:
                ball_after_tick = ball + vector(self.game.obstacle_speed, 0)
            else:
                ball_after_tick = ball
            dist += abs(ball_after_tick - bird)
        return dist
