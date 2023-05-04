import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from integrator import BaseIntegrator
from nbody import (NBody, Body)
from anim import Anim
from vector_finished import Vector
from integrator import RKIntegrator

v_init = 1
n_body = NBody(
    [
            Body(1, 0, 0, 0, - v_init),
            Body(1, 2, 0, 0, v_init)
    ]
)
integrator = RKIntegrator(0.01, n_body)
anim = Anim(integrator)
anim.go(1)

"""n_body = NBody([Body(1, 2, 0, 0, 0.5)])
dt = 0.01
a_i = Vector(-0.25, 0)

F1 = n_body.n_body[0].r
F2 = 0.5 * a_i * dt ** 2 / 4 + n_body.n_body[0].v * dt / 2 + F1 * dt / 2
F3 = 0.5 * a_i * dt ** 2 / 4 + n_body.n_body[0].v * dt / 2 + F2 * dt / 2
F4 = 0.5 * a_i * dt ** 2 + n_body.n_body[0].v * dt + F3 * dt
r_i = n_body.n_body[0].r + 1 / 6 * (F1 + 2 * F2 + 2 * F3 + F4) * dt
n_body.n_body[0].r = r_i


F1_v = n_body.n_body[0].v
F2_v = a_i * dt / 2 + n_body.n_body[0].v + n_body.n_body[0].v * dt / 2
F3_v = a_i * dt / 2 + n_body.n_body[0].v + F2_v * dt / 2
F4_v = a_i * dt + n_body.n_body[0].v + F3_v * dt
v_i = n_body.n_body[0].v + dt / 6 * (F1_v + 2 * F2_v + 2 * F3_v + F4_v)
n_body.n_body[0].v = v_i"""
