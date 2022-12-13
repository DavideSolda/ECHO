import unittest
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "model"))
import shortcuts as p

sys.path.insert(1, os.path.join(current_dir, "..", "engines", 'mae_epddl_planning'))
from epddl_engine import solve


class TestProblem2EPDDL(unittest.TestCase):

    def setUp(self):
        self.position = p.EnumType('position', ['one', 'two', 'three'])
        self.double_position = p.StructType('double_position', [self.position,
                                                                self.position])
        self.vpos = p.Variable('P', self.position)
        self.cpos = p.Fluent('current_position', self.position)
        self.safe = p.Fluent('safe')
        self.position_in_plain = p.Fluent('pos_in_plain', self.position)
        self.agent_names = p.AgentType(['agent_1', 'agent_2'])
        self.vagent = p.Variable('ag1', self.agent_names)
        self.vagent2 = p.Variable('ag2', self.agent_names)
        self.b_pos = p.BeliefPredicate([self.vagent], self.cpos('one'))
        self.move_action = p.MEAction(name='move',
                                      params=[],
                                      type=p.MEActionType.sensing,
                                      precondition=[self.b_pos, self.cpos(self.vpos)],
                                      effects=[- self.b_pos],
                                      full_obs=['agent_1'],
                                      partial_obs = [])

    def test_coin_in_the_box(self):

        #  problem
        coinintheboxmep = p.MEPlanningProblem()
        #  types:
        agents = p.AgentType(['a', 'b', 'c'])
        #  variables:
        ag = p.Variable('ag', agents)
        ag2 = p.Variable('ag2', agents)
        ag3 = p.Variable('ag2', agents)
        #  fluents:
        opened = p.Fluent(name='opened')
        has_key = p.Fluent('has_key', agents)
        looking = p.Fluent('looking', agents)
        tail = p.Fluent(name='tail')
        in_room_box = p.Fluent('in_room_box', agents)
        in_room_empty = p.Fluent('in_room_empty', agents)
        #  predicates:
        in_room_empty__ag = in_room_empty(ag)
        in_room_box__ag = in_room_box(ag)
        #  actions:
        move_to_box = p.MEAction('movetobox',
                                 params = [ag],
                                 precondition=[p.B([ag], in_room_empty__ag),
                                          in_room_empty__ag],
                                 effects=[-in_room_empty__ag,
                                          in_room_box(ag)],
                                 full_obs=[p.Forall(ag2, who=ag2)])

        move_to_empty = p.MEAction('movetoempty',
                                   params = [ag],
                                   precondition=[p.B([ag], in_room_box__ag),
                                            in_room_box__ag],
                                   effects=[in_room_empty__ag,
                                            -in_room_box(ag)],
                                   full_obs=[p.Forall(ag2, who=ag2)])

        _open = p.MEAction('open',
                           params = [ag],
                           precondition=[has_key(ag), p.B([ag], has_key(ag)), in_room_box(ag)],
                           effects=[opened()],
                           full_obs=[p.Forall(ag2, neq=p.neq(ag2, ag),
                                              who=ag2)])

        peek = p.MEAction('peek',
                          params = [ag],
                          precondition=[p.B([ag], opened()),
                                   p.B([ag], looking(ag)),
                                   looking(ag),
                                   opened(),
                                   in_room_box(ag)],
                          effects=[p.When(looking(ag), tail())],
                          full_obs=[ag],
                          partial_obs=[p.Forall(ag2, neq=p.neq(ag2, ag),
                                             when=looking(ag2) and in_room_box(ag2),
                                             who=ag2)],
                          type=p.MEActionType.sensing)

        signal = p.MEAction('signal',
                            params = [ag],
                            precondition=[p.B([ag], opened()),
                                     p.B([ag], looking(ag)),
                                     looking(ag),
                                     opened(),
                                     in_room_box(ag)],
                            effects=[p.When(looking(ag), tail())],
                            full_obs=[ag],
                            type=p.MEActionType.sensing)

        distract = p.MEAction('distract',
                              params = [ag, ag2],
                              precondition=[p.B([ag], looking(ag)),
                                       p.B([ag2], looking(ag2))],
                              effects=[-looking(ag2)],
                              full_obs=[p.Forall(ag3, neq=p.neq(ag2, ag3),
                                                 when=looking(ag3), who=ag3),
                                        ag2],
                              type=p.MEActionType.announcement)
        coinintheboxmep.name = 'coininthebox'
        coinintheboxmep.add_type(agents)
        coinintheboxmep.add_variable(ag)
        coinintheboxmep.add_variable(ag2)
        coinintheboxmep.add_variable(ag3)
        coinintheboxmep.add_fluent(opened)
        coinintheboxmep.add_fluent(has_key)
        coinintheboxmep.add_fluent(looking)
        coinintheboxmep.add_fluent(tail)
        coinintheboxmep.add_action(move_to_box)
        coinintheboxmep.add_action(move_to_empty)
        coinintheboxmep.add_action(_open)
        coinintheboxmep.add_action(peek)
        coinintheboxmep.add_action(signal)
        coinintheboxmep.add_action(distract)

        coinintheboxmep.add_initial_values(in_room_empty('a'),
                                           in_room_empty('b'),
                                           in_room_empty('c'),
                                           tail(),
                                           has_key('a'),
                                           looking('a'),
                                           p.B(['a', 'b', 'c'], has_key('a')),
                                           p.B(['a', 'b', 'c'], has_key('a')),
                                           p.B(['a', 'b', 'c'], -has_key('b')),
                                           p.B(['a', 'b', 'c'], -has_key('c')),
                                           p.B(['a', 'b', 'c'], -opened()),
                                           p.B(['a', 'b', 'c'], looking('a')),
                                           p.B(['a', 'b', 'c'], -looking('b')),
                                           p.B(['a', 'b', 'c'], -looking('c')),
                                           p.B(['a', 'b', 'c'], in_room_empty('a')),
                                           p.B(['a', 'b', 'c'], in_room_empty('b')),
                                           p.B(['a', 'b', 'c'], in_room_empty('c')),
                                           p.B(['a', 'b', 'c'], -in_room_box('a')),
                                           p.B(['a', 'b', 'c'], -in_room_box('b')),
                                           p.B(['a', 'b', 'c'], -in_room_box('c')))
        coinintheboxmep.add_goals(p.B(['a'], opened()))
        res = solve(coinintheboxmep)
        for action, var_inst in res:
            print(action.name, f'{var_inst}')
if __name__ == "__main__":
    unittest.main()
