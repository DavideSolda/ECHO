import os
import sys

import time
from mae_blocks_world import *


if __name__ == '__main__':


    #alpha
    alpha = [B(["alice"], (on_table("red")))]

    #beta
    beta = [B(["alice"], owner("alice", "red")), free_table()]

    #one color
    color = EnumType("color", ["red"])

    #classical
    initially = [on_stack('red', 1), free_stack(2), free_stack(3),
                 free_stack(4), free_stack(5), free_stack(6),
                 top('red'),
                 free_gripper('bob'), free_gripper('alice'),
                 owner('bob', 'red'),
                 in_front_of('bob', 1), in_front_of('bob', 2), in_front_of('bob', 3),
                 in_front_of('alice', 4), in_front_of('alice', 5), in_front_of('alice', 6),
                 free_table()]

    #epistemic
    epistemic_initially = [owner('bob', 'red'), free_table(), B(["bob", "alice"], free_table()),
                           B(["bob", "alice"], -on_table("red"))]

    one_color_time = []
    for goal in [alpha, beta]:
        t = time.time()
        run(color, initially, epistemic_initially, goal, True)
        one_color_time.append(time.time()-t)

    print(one_color_time)
