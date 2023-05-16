import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from integrator import BaseIntegrator
from nbody import (NBody, Body)
from anim import Anim
from vector_finished import Vector
from integrator import RKIntegrator

v_init = 0.5
n_body = NBody(
    [
            Body(1, 0, 0, 0, - v_init),
            Body(1, 2, 0, 0, v_init)
    ]
)
integrator = RKIntegrator(0.01, n_body)
anim = Anim(integrator)
anim.go(10)
