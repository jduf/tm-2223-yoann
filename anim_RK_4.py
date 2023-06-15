import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from integrator import BaseIntegrator
from nbody import (NBody, Body)
from anim import Anim
from vector_finished import Vector
from integrator import RK_4Integrator

n_body = NBody(
    [
            Body(1, 0, 0, 0, - 0.5),
            Body(1, 2, 0, 0, 0.5)
    ]
)
integrator = RK_4Integrator(0.01, n_body)
anim = Anim(integrator)
anim.go(10)
