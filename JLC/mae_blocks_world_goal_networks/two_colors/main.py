import os
import sys

import time
from mae_blocks_world import *


if __name__ == '__main__':


    #alpha
    alpha = [B(["alice"], (on_table("red")))]

    #beta
    beta = [B(["alice"], owner("alice", "red")), free_table()]

    #gamma
    gamma = [B(["alice"], owner("alice", "red")), B(["alice"], on_table("orange"))]

    #delta
    delta = [B(["alice", "bob"], owner("alice", "red")), B(["alice", "bob"], owner("alice", "orange"))]

    #two colors
    color = EnumType("color", ["red", "orange"])

    #classical
    initially = [on_stack('red', 1), free_stack(2), free_stack(3),
                 free_stack(4), free_stack(5), free_stack(6),
                 top('orange'), on_block('orange', 'red'),
                 free_gripper('bob'), free_gripper('alice'),
                 owner('bob', 'red'), owner('bob', 'orange'),
                 in_front_of('bob', 1), in_front_of('bob', 2), in_front_of('bob', 3),
                 in_front_of('alice', 4), in_front_of('alice', 5), in_front_of('alice', 6),
                 free_table()]

    #epistemic
    epistemic_initially = [owner('bob', 'red'), owner('bob', 'orange'),
                           free_table(), B(["bob", "alice"], free_table()),
                           B(["bob", "alice"], -on_table("red")),
                           B(["bob", "alice"], -on_table("orange"))]

    two_color_time = []
    for goal in [beta, gamma, delta]:
        t = time.time()
        run(color, initially, epistemic_initially, goal, True)
        two_color_time.append(time.time()-t)

    print(two_color_time)
