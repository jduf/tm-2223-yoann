import keyboard
from nbody import (NBody, Body)
from anim import Anim
from integrator import *
import random
from distance_matrix import *

tous_scores = []
vx_init = []
vy_init = []
count = 0

for i in range(6200000):
    n_body = NBody(
        [
            Body(597, 0, 0, 0, 0),
            Body(7.34, 4, 0, 0, 12),
            Body(0.2887e-17, 0, 0, round(random.uniform(0, 80), 2), round(random.uniform(0, 80), 2))
        ]
    )
    integrator = RK_4Integrator(0.1, n_body)
    vx_init.append(n_body.n_body[2].vx)
    vy_init.append(n_body.n_body[2].vy)

    score = 0
    while integrator.t < 10:
        d = DistanceMatrix(n_body.n_body)._get(1, 2).norm()
        score += 100 - d
        integrator.get_new_positions()

    tous_scores.append(score)
    count += 1
    print(count)

    if keyboard.is_pressed("l"):
        m = max(tous_scores)
        p = [i for i, j in enumerate(tous_scores) if j == m]
        a = vx_init[p[0]]
        b = vy_init[p[0]]
        print(a, b)


    if keyboard.is_pressed("m"):
        for i in range(50):
            m = max(tous_scores)
            p = [i for i, j in enumerate(tous_scores) if j == m]
            a = vx_init[p[0]]
            b = vy_init[p[0]]
            print(a, b)

            tous_scores.remove(m)
            vx_init.remove(a)
            vy_init.remove(b)