import keyboard
from nbody import (NBody, Body)
from anim import Anim
from integrator import *
import random
from distance_matrix import *

tous_scores = []
facteurs_x = []
facteurs_y = []
count = 0

for i in range(200000):
    n_body = NBody(
        [
            Body(597, 0, 0, 0, 0),
            Body(7.34, 4, 0, 0, 12),
            Body(0.2887e-17, 0, 0, 59.2626, 28.4432)
        ]
    )
    integrator = RK_4Integrator_reel(0.1, n_body, 8e-16)
    facteurs_x.append(integrator.a)
    facteurs_y.append(integrator.b)

    score = 0
    for t in range(204):
        if integrator.t > 15 and integrator.n_body.n_body[2].r == Vector(0, 0):
            score = 0
            break
        d = integrator.n_body.n_body[2].r - integrator.n_body.n_body[0].r
        d = d.norm()
        score += d
        integrator.get_new_positions()

    tous_scores.append(score)
    count += 1
    print(count)

    if keyboard.is_pressed("l"):
        m = min(tous_scores)
        p = [i for i, j in enumerate(tous_scores) if j == m]
        a = facteurs_x[p[0]]
        b = facteurs_y[p[0]]
        print(integrator.a, integrator.b, "score:", m)



for i in range(1000):
    m = min(tous_scores)
    p = [i for i, j in enumerate(tous_scores) if j == m]
    a = facteurs_x[p[0]]
    b = facteurs_y[p[0]]
    print(a, b, "score:", m)

    tous_scores.remove(m)
    facteurs_x.remove(a)
    facteurs_y.remove(b)
