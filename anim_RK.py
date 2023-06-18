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

for i in range(2000000):
    n_body = NBody(
        [
            Body(597, 0, 0, 0, 0),
            Body(7.34, 4, 0, 0, 12),
            Body(0.2887e-17, 0, 0, round(random.uniform(59.2, 59.3), 4), round(random.uniform(28.4, 28.5), 4))
        ]
    )
    integrator = RK_4Integrator(0.1, n_body)
    vx_init.append(n_body.n_body[2].vx)
    vy_init.append(n_body.n_body[2].vy)

    score = 0
    while integrator.t < 40:
        d = integrator.n_body.n_body[2].r - integrator.n_body.n_body[1].r
        d = d.norm()
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
        print(a, b, "score:", m)



for i in range(1000):
    m = max(tous_scores)
    p = [i for i, j in enumerate(tous_scores) if j == m]
    a = vx_init[p[0]]
    b = vy_init[p[0]]
    print(a, b, "score:", m)

    tous_scores.remove(m)
    vx_init.remove(a)
    vy_init.remove(b)
