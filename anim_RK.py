import keyboard
from nbody import (NBody, Body, Active_Body)
from anim import Anim
from integrator import *
import random
from distance_matrix import *
from math import sqrt, cos, sin, radians

trajectory_dict = {}  # Dictionnaire pour stocker les coordonnées

# Première partie : ligne droite
for t in range(0, 218):
    t = round(t * 0.001, 3)  # Convertit le pas de temps en secondes
    x = 3.167 / 0.217 * t
    y = -0.069 + (-0.069 + 2.443) / 0.217 * t
    trajectory_dict[t] = Vector(x, y)

# Deuxième partie : orbite autour de la Lune
for t in range(218, 278):
    t = round(t * 0.001, 3)  # Convertit le pas de temps en secondes
    x = cos(radians(360 * t / 2.09)) * 4 + 0.019 * 0.019 * cos(radians(127.38 - 360 * (t - 0.218) / 0.005714))
    y = sin(radians(360 * t / 2.09)) * 4 + 0.019 * sin(radians(127.38 - 360 * (t - 0.218) / 0.005714))
    trajectory_dict[t] = Vector(x, y)

tous_scores = []
v_x = []
v_y = []
count = 0

for i in range(10000000):
    n_body = NBody(
        [
            Body(597, 0, 0, 0, 0),
            Body(7.34, 4, 0, 0, 12.21679),
            Active_Body(0.2887e-17, 0, - 0.069, round(random.uniform(100, 130), 6), round(random.uniform(30, 60), 6), 0.002678, 10, False)

        ]
    )
    integrator = BaseIntegrator(0.001, n_body)
    v_x.append(n_body.n_body[2].v.x)
    v_y.append(n_body.n_body[2].v.y)

    score = 0
    while integrator.t < 0.278:
        t = integrator.t
        pos_theorique = trajectory_dict[round(integrator.t, 3)]

        # Calculez la distance entre la position actuelle et la position théorique
        score += (n_body.n_body[2].r - pos_theorique).norm()

        integrator.get_new_positions()

    tous_scores.append(score)
    count += 1
    print(count)

    if keyboard.is_pressed("l"):
        m = min(tous_scores)
        p = [i for i, j in enumerate(tous_scores) if j == m]
        print(str(v_x[p[0]]) + ",", v_y[p[0]], "score:", m)



for i in range(1000):
    m = min(tous_scores)
    p = [i for i, j in enumerate(tous_scores) if j == m]
    a = v_x[p[0]]
    b = v_y[p[0]]
    print(str(a) + ",", b, "score:", m)

    tous_scores.remove(m)
    v_x.remove(a)
    v_y.remove(b)
