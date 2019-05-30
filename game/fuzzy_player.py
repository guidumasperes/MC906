# the idea here is to make many players , not just one, in order to test different approaches.

from self.game.core import self.game
import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl
from freeself.games import vector


# this player doesn'take left movimentation in account when making a decision.
class BasePlayer:

    def __init__(self, game, proximity_threshold):
        self.game = self.game
        self.wall = self._wall_antecedent()
        self.tap_ball_threat, self.no_tap_ball_threat = self._threatening_balls_antecedents(proximity_threshold)
        self.rules = []

    # in a risky threshold , wall > ball proximity > ball density

    def perform_a_play(self):
        self.proximity = self._ball_proximity_antecedent()
        press = ctrl.Consequent(np.arange(0, 1.25, 0.25), 'press')
        press['no'] = fuzz.trimf(press.universe, [0, 0, 0.5])
        press["maybe"] = fuzz.trimf(press.universe, [0, 0.5, 1])
        press['yes'] = fuzz.trimf(press.universe, [0.5, 1, 1])
        rules = self.generate_rules(press)
        pressing_ctrl = ctrl.ControlSystem(rules)
        pressing = ctrl.ControlSystemSimulation(pressing_ctrl)

        pressing.input['wall'] = self.game.bird.y

        # pressing.input['no_tap_bad'] # parameter = the distance to the nearest ball if no tap is performed
        # pressing.input['tap_bad']   # parameter =  the distance to the nearest ball if tap no tap is performed
        # pressing.input['proximity'] # proximity = the actual sum of the distance to all points

        pressing.compute()
        print(pressing.output['press'])
        if pressing.output['press'] > 0.6:
            self.game.tap()

    pass

    def _wall_antecedent(self):
        wall = ctrl.Antecedent(np.arange(self.game.ground, self.game.ceil, 1), "wall")
        wall.automf(3)
        return wall

    # rule to maximize the distance between Flap and obstacles
    # 2 possibilities, tap or dont tap -> either way the distance will increase or decrease
    # the possibility to go up has the most significative difference in distance , because vy < vytap
    # the the minimal interval is the min dont tap variation and the maximum is the tap variation, the step is one

    def _ball_proximity_antecedent(self):
        bird_after_tap = self.game.bird + (0, self.game.vy + self.game.tapY_mov)
        distance_with_tap = self._sum_distance_to_obstacles(self.game, bird_after_tap, True)
        bird_after_no_tap = self.game.bird + (0, self.game.vy)
        distance_without_tap = self._sum_distance_to_obstacles(self.game, bird_after_no_tap, True)

        self.lesser_proximity_tap = False

        if distance_without_tap > distance_with_tap:
            proximity = ctrl.Antecedent(np.arange(0, distance_without_tap, distance_with_tap), 'proximity')

        else:
            proximity = ctrl.Antecedent(np.arange(0, distance_with_tap, distance_without_tap), 'proximity')
            self.lesser_proximity_tap = True

        proximity.automf(3)
        return proximity

    def _threatening_balls_antecedents(self, proximity_threshold):
        proximity_range = self.self.game.obstacle_diam / 2 + proximity_threshold
        # no_tap_threat_filter = lambda ball: absolute_distance(tap_option_no, ball) < proximity_range
        # tap_threat_filter = lambda ball: absolute_distance(tap_option_yes, ball) < proximity_range
        # no_tap_threats = filter(no_tap_threat_filter, self.game.balls)
        # tap_threats = filter(tap_threat_filter, self.game.balls)
        # if len(no_tap_threats) != 0:
        # 1/4  = 1 proximity range?
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
        balls_after_tic = map(lambda ball: ball + (self.game.obstacle_speed, 0))
        min(balls_after_tic, )

    def generate_rules(self, press):
        no_tap_bad_rule = ctrl.Rule(self.no_tap_ball_threat['good'], press['yes'])
        tap_bad_rule = ctrl.Rule(self.tap_ball_threat['good'], press['no'])
        wall_rule_1 = ctrl.Rule(self.wall['poor'], press['yes'])
        wall_rule_2 = ctrl.Rule(self.wall['good'], press['no'])
        composed_proximity_predicate = self.tap_ball_threat['average'] and self.no_tap_ball_threat['average']
        conditionalTap = press["yes"] if self.lesser_proximity_tap else press["no"]
        proximity_rule = ctrl.Rule((composed_proximity_predicate and self.proximity['poor']), conditionalTap)
        return [no_tap_bad_rule, tap_bad_rule, wall_rule_1, wall_rule_2, proximity_rule]

    def _sum_distance_to_obstacles(self, bird, after_timeout=False):
        dist = 0
        for ball in self.game.balls:
            if after_timeout:
                ball_after_tick = ball + (self.game.obstacle_speed, 0)
            else:
                ball_after_tick = ball
            dist += abs(ball_after_tick - bird)
        return dist


# in this class we need to consider the possibility of the bird to perform a left movement, this is the only difference
class AdvancedPlayer(BasePlayer):
    pass
